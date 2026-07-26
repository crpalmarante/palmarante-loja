from modules.workflow.domain.entities.instance import WorkflowInstance, InstanceStatus
from modules.workflow.domain.entities.history import WorkflowHistory
from modules.workflow.domain.entities.approval import WorkflowApproval, ApprovalStatus
from modules.workflow.domain.entities.transition import WorkflowTransition
from modules.workflow.domain.repositories.workflow_repository import WorkflowRepository


class WorkflowEngine:
    def __init__(self, repo: WorkflowRepository):
        self._repo = repo

    def start(self, workflow_id: str, document_type: str,
              document_id: str, document_data: dict = None) -> WorkflowInstance:
        wf = self._repo.find_workflow_by_id(workflow_id)
        if not wf:
            raise ValueError(f'Workflow {workflow_id} not found')
        states = self._repo.find_states_by_workflow(workflow_id)
        initial = [s for s in states if s.is_initial]
        if not initial:
            raise ValueError(f'Workflow {workflow_id} has no initial state')

        instance = WorkflowInstance(
            workflow_id=workflow_id,
            document_type=document_type,
            document_id=document_id,
            current_state_id=initial[0]._id,
            document_data=document_data or {},
        )
        instance = self._repo.save_instance(instance)

        history = WorkflowHistory(instance_id=instance._id, action='started',
                                  to_state_id=initial[0]._id,
                                  comment=f'Workflow started for {document_type} {document_id}')
        self._repo.save_history(history)
        return instance

    def execute_transition(self, instance_id: str, transition_code: str = '',
                           to_state_id: str = '', comment: str = '',
                           performed_by: str = '') -> WorkflowInstance:
        instance = self._repo.find_instance_by_id(instance_id)
        if not instance:
            raise ValueError(f'Instance {instance_id} not found')
        if instance.status != InstanceStatus.ACTIVE:
            raise ValueError(f'Instance is {instance.status.value}')

        transitions = self._repo.find_transitions_from_state(
            instance.workflow_id, instance.current_state_id)

        if transition_code:
            t = next((t for t in transitions if t.code == transition_code), None)
        elif to_state_id:
            t = next((t for t in transitions if t.to_state_id == to_state_id), None)
        else:
            raise ValueError('Provide transition_code or to_state_id')

        if not t:
            raise ValueError(f'No valid transition from current state')

        rules = self._repo.find_rules_by_transition(t._id)
        for rule in rules:
            if not rule.evaluate(instance.document_data):
                raise ValueError(rule.error_message or f'Rule "{rule.name}" blocked transition')

        self._repo.save_history(WorkflowHistory(
            instance_id=instance._id, from_state_id=instance.current_state_id,
            to_state_id=t.to_state_id, transition_id=t._id,
            action='transition', comment=comment or t.name, performed_by=performed_by,
            metadata={'transition_code': t.code, 'transition_name': t.name},
        ))

        if t.requires_approval:
            approval = WorkflowApproval(
                instance_id=instance._id, transition_id=t._id,
                required_count=t.approval_count,
            )
            self._repo.save_approval(approval)
            return instance

        from modules.workflow.domain.entities.state import StateType
        instance.advance(t.to_state_id)
        to_state = self._repo.find_state_by_id(t.to_state_id)

        if to_state and to_state.type == StateType.FINAL:
            instance.complete()
            self._repo.save_history(WorkflowHistory(
                instance_id=instance._id, action='completed',
                to_state_id=t.to_state_id, performed_by=performed_by))

        self._repo.save_instance(instance)
        return instance

    def approve(self, approval_id: str, user: str = '',
                comment: str = '') -> WorkflowInstance:
        approvals = self._repo.find_pending_approvals()
        approval = next((a for a in approvals if a._id == approval_id), None)
        if not approval:
            raise ValueError(f'Approval {approval_id} not found or not pending')

        approval.approve(user, comment)
        self._repo.save_approval(approval)

        instance = self._repo.find_instance_by_id(approval.instance_id)
        if not instance:
            raise ValueError('Instance not found')

        transition = self._repo.find_transitions_by_workflow(instance.workflow_id)
        t = next((tr for tr in transition if tr._id == approval.transition_id), None)
        if t:
            instance.advance(t.to_state_id)
            self._repo.save_instance(instance)

        self._repo.save_history(WorkflowHistory(
            instance_id=instance._id, action='approved',
            transition_id=approval.transition_id,
            comment=comment or 'Approved', performed_by=user))
        return instance

    def reject(self, approval_id: str, user: str = '',
               comment: str = '') -> WorkflowApproval:
        approvals = self._repo.find_pending_approvals()
        approval = next((a for a in approvals if a._id == approval_id), None)
        if not approval:
            raise ValueError(f'Approval {approval_id} not found')

        approval.reject(user, comment)
        self._repo.save_approval(approval)

        self._repo.save_history(WorkflowHistory(
            instance_id=approval.instance_id, action='rejected',
            transition_id=approval.transition_id,
            comment=comment or 'Rejected', performed_by=user))
        return approval

    def cancel(self, instance_id: str, reason: str = '') -> WorkflowInstance:
        instance = self._repo.find_instance_by_id(instance_id)
        if not instance:
            raise ValueError(f'Instance {instance_id} not found')
        instance.cancel()
        self._repo.save_instance(instance)
        self._repo.save_history(WorkflowHistory(
            instance_id=instance._id, action='cancelled',
            comment=reason or 'Cancelled'))
        return instance

    def get_dashboard(self) -> dict:
        all_instances = []
        for wf in self._repo.find_all_workflows():
            all_instances.extend(self._repo.find_instances_by_workflow(wf._id))
        active = [i for i in all_instances if i.status == InstanceStatus.ACTIVE]
        completed = [i for i in all_instances if i.status == InstanceStatus.COMPLETED]
        pending_approvals = self._repo.find_pending_approvals()
        return {
            'total_instances': len(all_instances),
            'active': len(active),
            'completed': len(completed),
            'pending_approvals': len(pending_approvals),
        }
