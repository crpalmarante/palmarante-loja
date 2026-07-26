from dataclasses import dataclass, field


@dataclass
class CreateWorkflow:
    name: str
    code: str
    description: str = ''
    document_type: str = ''


@dataclass
class AddState:
    workflow_id: str
    name: str
    code: str
    type: str = 'intermediate'
    color: str = '#1a73e8'
    description: str = ''
    sort_order: int = 0


@dataclass
class AddTransition:
    workflow_id: str
    name: str
    code: str
    from_state_id: str
    to_state_id: str
    requires_approval: bool = False
    approval_count: int = 1
    sort_order: int = 0


@dataclass
class AddRule:
    workflow_id: str
    name: str
    rule_type: str = 'condition'
    transition_id: str = ''
    field: str = ''
    operator: str = 'equals'
    value: str = ''
    error_message: str = ''
    target_role: str = ''


@dataclass
class StartWorkflow:
    workflow_id: str
    document_type: str
    document_id: str
    document_data: dict = None


@dataclass
class ExecuteTransition:
    instance_id: str
    transition_code: str = ''
    to_state_id: str = ''
    comment: str = ''
    performed_by: str = ''


@dataclass
class ApproveTransition:
    approval_id: str
    user: str = ''
    comment: str = ''


@dataclass
class RejectTransition:
    approval_id: str
    user: str = ''
    comment: str = ''


@dataclass
class CancelInstance:
    instance_id: str
    reason: str = ''
