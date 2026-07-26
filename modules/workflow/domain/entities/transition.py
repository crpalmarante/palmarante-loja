from dataclasses import dataclass
from datetime import datetime


@dataclass
class WorkflowTransition:
    workflow_id: str
    name: str
    code: str
    from_state_id: str
    to_state_id: str
    description: str = ''
    requires_approval: bool = False
    approval_count: int = 1
    sort_order: int = 0
    active: bool = True
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
