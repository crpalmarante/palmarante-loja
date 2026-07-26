from modules.workflow.domain.entities.workflow import Workflow
from modules.workflow.domain.entities.state import WorkflowState
from modules.workflow.domain.entities.transition import WorkflowTransition
from modules.workflow.domain.entities.rule import WorkflowRule
from modules.workflow.domain.entities.instance import WorkflowInstance
from modules.workflow.domain.entities.history import WorkflowHistory
from modules.workflow.domain.entities.approval import WorkflowApproval
from modules.workflow.domain.entities.assignment import WorkflowAssignment
from modules.workflow.domain.repositories.workflow_repository import WorkflowRepository


class InMemoryWorkflowRepository(WorkflowRepository):
    def __init__(self):
        self._workflows: dict[str, Workflow] = {}
        self._states: dict[str, WorkflowState] = {}
        self._transitions: dict[str, WorkflowTransition] = {}
        self._rules: list[WorkflowRule] = []
        self._instances: dict[str, WorkflowInstance] = {}
        self._history: list[WorkflowHistory] = []
        self._approvals: list[WorkflowApproval] = []
        self._assignments: list[WorkflowAssignment] = []
        self._ids = 0

    def _next_id(self) -> str:
        self._ids += 1
        return str(self._ids)

    def save_workflow(self, wf: Workflow) -> Workflow:
        if not wf._id:
            wf._id = self._next_id()
        self._workflows[wf._id] = wf
        return wf

    def find_workflow_by_id(self, wf_id: str) -> Workflow | None:
        return self._workflows.get(wf_id)

    def find_workflow_by_code(self, code: str) -> Workflow | None:
        for w in self._workflows.values():
            if w.code == code:
                return w
        return None

    def find_all_workflows(self, document_type: str = '') -> list[Workflow]:
        return [w for w in self._workflows.values()
                if not document_type or w.document_type == document_type]

    def save_state(self, state: WorkflowState) -> WorkflowState:
        if not state._id:
            state._id = self._next_id()
        self._states[state._id] = state
        return state

    def find_states_by_workflow(self, workflow_id: str) -> list[WorkflowState]:
        return sorted([s for s in self._states.values() if s.workflow_id == workflow_id],
                      key=lambda s: s.sort_order)

    def find_state_by_id(self, state_id: str) -> WorkflowState | None:
        return self._states.get(state_id)

    def save_transition(self, t: WorkflowTransition) -> WorkflowTransition:
        if not t._id:
            t._id = self._next_id()
        self._transitions[t._id] = t
        return t

    def find_transitions_by_workflow(self, workflow_id: str) -> list[WorkflowTransition]:
        return sorted([t for t in self._transitions.values() if t.workflow_id == workflow_id],
                      key=lambda t: t.sort_order)

    def find_transitions_from_state(self, workflow_id: str, state_id: str) -> list[WorkflowTransition]:
        return [t for t in self._transitions.values()
                if t.workflow_id == workflow_id and t.from_state_id == state_id and t.active]

    def save_rule(self, rule: WorkflowRule) -> WorkflowRule:
        if not rule._id:
            rule._id = self._next_id()
        self._rules.append(rule)
        return rule

    def find_rules_by_transition(self, transition_id: str) -> list[WorkflowRule]:
        return [r for r in self._rules if r.transition_id == transition_id and r.active]

    def find_rules_by_workflow(self, workflow_id: str) -> list[WorkflowRule]:
        return [r for r in self._rules if r.workflow_id == workflow_id]

    def save_instance(self, instance: WorkflowInstance) -> WorkflowInstance:
        if not instance._id:
            instance._id = self._next_id()
        self._instances[instance._id] = instance
        return instance

    def find_instance_by_id(self, inst_id: str) -> WorkflowInstance | None:
        return self._instances.get(inst_id)

    def find_instances_by_document(self, document_type: str, document_id: str) -> list[WorkflowInstance]:
        return [i for i in self._instances.values()
                if i.document_type == document_type and i.document_id == document_id]

    def find_instances_by_workflow(self, workflow_id: str, status: str = '') -> list[WorkflowInstance]:
        return [i for i in self._instances.values()
                if i.workflow_id == workflow_id
                and (not status or i.status.value == status)]

    def find_instances_by_state(self, state_id: str) -> list[WorkflowInstance]:
        return [i for i in self._instances.values() if i.current_state_id == state_id]

    def save_history(self, h: WorkflowHistory) -> WorkflowHistory:
        if not h._id:
            h._id = self._next_id()
        self._history.append(h)
        return h

    def find_history_by_instance(self, instance_id: str) -> list[WorkflowHistory]:
        return sorted([h for h in self._history if h.instance_id == instance_id],
                      key=lambda h: h.created_at)

    def save_approval(self, a: WorkflowApproval) -> WorkflowApproval:
        if not a._id:
            a._id = self._next_id()
        self._approvals.append(a)
        return a

    def find_approvals_by_instance(self, instance_id: str) -> list[WorkflowApproval]:
        return [a for a in self._approvals if a.instance_id == instance_id]

    def find_pending_approvals(self, role: str = '') -> list[WorkflowApproval]:
        return [a for a in self._approvals if a.is_pending
                and (not role or a.role == role)]

    def save_assignment(self, a: WorkflowAssignment) -> WorkflowAssignment:
        if not a._id:
            a._id = self._next_id()
        self._assignments.append(a)
        return a

    def find_assignments_by_transition(self, transition_id: str) -> list[WorkflowAssignment]:
        return [a for a in self._assignments if a.transition_id == transition_id and a.active]
