import pytest
from modules.workflow.domain.entities.workflow import Workflow, WorkflowStatus
from modules.workflow.domain.entities.state import WorkflowState, StateType
from modules.workflow.domain.entities.transition import WorkflowTransition
from modules.workflow.domain.entities.rule import WorkflowRule, RuleType, RuleOperator
from modules.workflow.domain.entities.instance import WorkflowInstance, InstanceStatus
from modules.workflow.domain.entities.history import WorkflowHistory
from modules.workflow.domain.entities.approval import WorkflowApproval, ApprovalStatus
from modules.workflow.domain.entities.assignment import WorkflowAssignment, AssignmentType
from modules.workflow.infrastructure.postgres.memory_repository import InMemoryWorkflowRepository
from modules.workflow.application.services.workflow_engine import WorkflowEngine


# ══════════════════════════════════════════════════════════════
# Domain Entities
# ══════════════════════════════════════════════════════════════
class TestWorkflow:
    def test_create(self):
        w = Workflow(name='Pedido de Venda', code='SALE', document_type='sale_order')
        assert w.code == 'SALE' and w.status == WorkflowStatus.ACTIVE

    def test_activate_deactivate(self):
        w = Workflow(name='Test', code='TST')
        w.deactivate()
        assert w.status == WorkflowStatus.INACTIVE
        w.activate()
        assert w.status == WorkflowStatus.ACTIVE


class TestWorkflowState:
    def test_create_initial(self):
        s = WorkflowState(workflow_id='w1', name='Rascunho', code='draft', type=StateType.INITIAL)
        assert s.is_initial and not s.is_final

    def test_final_state(self):
        s = WorkflowState(workflow_id='w1', name='Concluído', code='done', type=StateType.FINAL)
        assert s.is_final

    def test_approval_state(self):
        s = WorkflowState(workflow_id='w1', name='Aprovação', code='approval', type=StateType.APPROVAL)
        assert s.is_approval


class TestTransition:
    def test_create(self):
        t = WorkflowTransition(workflow_id='w1', name='Aprovar', code='approve',
                               from_state_id='s1', to_state_id='s2')
        assert t.code == 'approve' and t.active is True

    def test_requires_approval(self):
        t = WorkflowTransition(workflow_id='w1', name='Aprovar', code='approve',
                               from_state_id='s1', to_state_id='s2', requires_approval=True)
        assert t.requires_approval


class TestRule:
    def test_condition(self):
        r = WorkflowRule(workflow_id='w1', name='Valor > 1000', rule_type=RuleType.CONDITION,
                         field='total', operator=RuleOperator.GREATER_THAN, value='1000')
        assert r.evaluate({'total': 1500}) is True
        assert r.evaluate({'total': 500}) is False

    def test_equals(self):
        r = WorkflowRule(workflow_id='w1', name='Tipo = venda',
                         field='type', operator=RuleOperator.EQUALS, value='sale')
        assert r.evaluate({'type': 'sale'}) is True
        assert r.evaluate({'type': 'purchase'}) is False

    def test_in(self):
        r = WorkflowRule(workflow_id='w1', name='Status in',
                         field='status', operator=RuleOperator.IN, value='active,pending')
        assert r.evaluate({'status': 'active'}) is True
        assert r.evaluate({'status': 'cancelled'}) is False


class TestInstance:
    def test_create(self):
        i = WorkflowInstance(workflow_id='w1', document_type='sale', document_id='doc-1',
                             current_state_id='s1')
        assert i.status == InstanceStatus.ACTIVE

    def test_flow(self):
        i = WorkflowInstance(workflow_id='w1', document_type='sale', document_id='doc-1',
                             current_state_id='s1')
        i.advance('s2')
        assert i.current_state_id == 's2'
        i.complete()
        assert i.status == InstanceStatus.COMPLETED
        assert i.completed_at is not None

    def test_cancel(self):
        i = WorkflowInstance(workflow_id='w1', document_type='sale', document_id='doc-1',
                             current_state_id='s1')
        i.cancel()
        assert i.status == InstanceStatus.CANCELLED


class TestApproval:
    def test_pending(self):
        a = WorkflowApproval(instance_id='i1', transition_id='t1')
        assert a.is_pending

    def test_approve(self):
        a = WorkflowApproval(instance_id='i1', transition_id='t1')
        a.approve()
        assert a.is_approved


# ══════════════════════════════════════════════════════════════
# Workflow Engine — o cérebro
# ══════════════════════════════════════════════════════════════
class TestWorkflowEngine:
    @pytest.fixture
    def repo(self):
        return InMemoryWorkflowRepository()

    @pytest.fixture
    def engine(self, repo):
        return WorkflowEngine(repo)

    @pytest.fixture
    def sale_workflow(self, repo):
        w = Workflow(name='Pedido Venda', code='SALE', document_type='sale_order')
        repo.save_workflow(w)
        s1 = WorkflowState(workflow_id=w._id, name='Rascunho', code='draft', type=StateType.INITIAL, sort_order=0)
        s2 = WorkflowState(workflow_id=w._id, name='Aprovado', code='approved', type=StateType.INTERMEDIATE, sort_order=1)
        s3 = WorkflowState(workflow_id=w._id, name='Concluído', code='completed', type=StateType.FINAL, sort_order=2)
        repo.save_state(s1)
        repo.save_state(s2)
        repo.save_state(s3)
        t1 = WorkflowTransition(workflow_id=w._id, name='Aprovar', code='approve',
                                from_state_id=s1._id, to_state_id=s2._id, sort_order=0)
        t2 = WorkflowTransition(workflow_id=w._id, name='Concluir', code='complete',
                                from_state_id=s2._id, to_state_id=s3._id, sort_order=1)
        repo.save_transition(t1)
        repo.save_transition(t2)
        return w

    def test_start_workflow(self, repo, engine, sale_workflow):
        instance = engine.start(sale_workflow._id, 'sale_order', 'ord-001', {'total': 500})
        assert instance.status == InstanceStatus.ACTIVE
        assert instance.document_id == 'ord-001'

    def test_initial_state(self, repo, engine, sale_workflow):
        instance = engine.start(sale_workflow._id, 'sale_order', 'ord-001')
        states = repo.find_states_by_workflow(sale_workflow._id)
        initial = [s for s in states if s.is_initial][0]
        assert instance.current_state_id == initial._id

    def test_transition(self, repo, engine, sale_workflow):
        instance = engine.start(sale_workflow._id, 'sale_order', 'ord-001')
        states = repo.find_states_by_workflow(sale_workflow._id)
        instance = engine.execute_transition(instance._id, transition_code='approve')
        approved = [s for s in states if s.code == 'approved'][0]
        assert instance.current_state_id == approved._id

    def test_complete_flow(self, repo, engine, sale_workflow):
        instance = engine.start(sale_workflow._id, 'sale_order', 'ord-001')
        engine.execute_transition(instance._id, transition_code='approve')
        engine.execute_transition(instance._id, transition_code='complete')
        instance = repo.find_instance_by_id(instance._id)
        assert instance.status == InstanceStatus.COMPLETED

    def test_history_generated(self, repo, engine, sale_workflow):
        instance = engine.start(sale_workflow._id, 'sale_order', 'ord-001')
        engine.execute_transition(instance._id, transition_code='approve', performed_by='admin')
        history = repo.find_history_by_instance(instance._id)
        assert len(history) >= 2  # start + transition
        assert history[0].action == 'started'
        assert history[1].action == 'transition'
        assert history[1].performed_by == 'admin'

    def test_cancel(self, repo, engine, sale_workflow):
        instance = engine.start(sale_workflow._id, 'sale_order', 'ord-001')
        engine.cancel(instance._id, 'Cancelado pelo cliente')
        instance = repo.find_instance_by_id(instance._id)
        assert instance.status == InstanceStatus.CANCELLED

    def test_rule_blocks_transition(self, repo, engine, sale_workflow):
        w = sale_workflow
        states = repo.find_states_by_workflow(w._id)
        t = repo.find_transitions_from_state(w._id, states[0]._id)[0]
        rule = WorkflowRule(workflow_id=w._id, name='Valor mínimo',
                            rule_type=RuleType.VALIDATION, transition_id=t._id,
                            field='total', operator=RuleOperator.GREATER_OR_EQUAL, value='100',
                            error_message='Valor mínimo é 100')
        repo.save_rule(rule)

        instance = engine.start(w._id, 'sale_order', 'ord-002', {'total': 50})
        with pytest.raises(ValueError, match='Valor mínimo é 100'):
            engine.execute_transition(instance._id, transition_code='approve')

    def test_approval_workflow(self, repo, engine, sale_workflow):
        w = sale_workflow
        states = repo.find_states_by_workflow(w._id)
        transitions = repo.find_transitions_from_state(w._id, states[0]._id)
        for t in transitions:
            t.requires_approval = True
            repo.save_transition(t)

        instance = engine.start(w._id, 'sale_order', 'ord-003', {'total': 5000})
        instance = engine.execute_transition(instance._id, transition_code='approve')

        approvals = repo.find_pending_approvals()
        assert len(approvals) == 1

        instance = engine.approve(approvals[0]._id, user='manager')
        states = repo.find_states_by_workflow(w._id)
        approved = [s for s in states if s.code == 'approved'][0]
        assert instance.current_state_id == approved._id


class TestWorkflowRepository:
    @pytest.fixture
    def repo(self):
        return InMemoryWorkflowRepository()

    def test_workflow_crud(self, repo):
        w = Workflow(name='Test', code='TST')
        repo.save_workflow(w)
        assert repo.find_workflow_by_id(w._id).name == 'Test'
        assert repo.find_workflow_by_code('TST').name == 'Test'

    def test_states_sorted(self, repo):
        w = Workflow(name='Test', code='TST')
        repo.save_workflow(w)
        repo.save_state(WorkflowState(workflow_id=w._id, name='B', code='b', sort_order=2))
        repo.save_state(WorkflowState(workflow_id=w._id, name='A', code='a', sort_order=1))
        states = repo.find_states_by_workflow(w._id)
        assert states[0].code == 'a'

    def test_transitions_from_state(self, repo):
        w = Workflow(name='Test', code='TST')
        repo.save_workflow(w)
        s1 = WorkflowState(workflow_id=w._id, name='S1', code='s1')
        s2 = WorkflowState(workflow_id=w._id, name='S2', code='s2')
        s3 = WorkflowState(workflow_id=w._id, name='S3', code='s3')
        repo.save_state(s1); repo.save_state(s2); repo.save_state(s3)
        repo.save_transition(WorkflowTransition(workflow_id=w._id, name='T1', code='t1', from_state_id=s1._id, to_state_id=s2._id))
        repo.save_transition(WorkflowTransition(workflow_id=w._id, name='T2', code='t2', from_state_id=s1._id, to_state_id=s3._id))
        repo.save_transition(WorkflowTransition(workflow_id=w._id, name='T3', code='t3', from_state_id=s2._id, to_state_id=s3._id))
        assert len(repo.find_transitions_from_state(w._id, s1._id)) == 2
        assert len(repo.find_transitions_from_state(w._id, s2._id)) == 1

    def test_rules_by_transition(self, repo):
        w = Workflow(name='Test', code='TST')
        repo.save_workflow(w)
        t = WorkflowTransition(workflow_id=w._id, name='T', code='t', from_state_id='s1', to_state_id='s2')
        repo.save_transition(t)
        r1 = WorkflowRule(workflow_id=w._id, name='R1', transition_id=t._id)
        r2 = WorkflowRule(workflow_id=w._id, name='R2', transition_id=t._id)
        r3 = WorkflowRule(workflow_id=w._id, name='R3')
        repo.save_rule(r1); repo.save_rule(r2); repo.save_rule(r3)
        assert len(repo.find_rules_by_transition(t._id)) == 2

    def test_instances_by_document(self, repo):
        w = Workflow(name='Test', code='TST')
        repo.save_workflow(w)
        repo.save_instance(WorkflowInstance(workflow_id=w._id, document_type='sale', document_id='d1', current_state_id='s1'))
        repo.save_instance(WorkflowInstance(workflow_id=w._id, document_type='sale', document_id='d2', current_state_id='s1'))
        repo.save_instance(WorkflowInstance(workflow_id=w._id, document_type='purchase', document_id='d1', current_state_id='s1'))
        assert len(repo.find_instances_by_document('sale', 'd1')) == 1
        assert len(repo.find_instances_by_document('sale', '')) == 0

    def test_pending_approvals(self, repo):
        a1 = WorkflowApproval(instance_id='i1', transition_id='t1', status=ApprovalStatus.PENDING)
        a2 = WorkflowApproval(instance_id='i1', transition_id='t2', status=ApprovalStatus.APPROVED)
        a3 = WorkflowApproval(instance_id='i2', transition_id='t1', status=ApprovalStatus.PENDING)
        repo.save_approval(a1); repo.save_approval(a2); repo.save_approval(a3)
        assert len(repo.find_pending_approvals()) == 2
