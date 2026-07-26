from dataclasses import dataclass
from datetime import datetime


@dataclass
class WorkflowHistory:
    instance_id: str
    from_state_id: str = ''
    to_state_id: str = ''
    transition_id: str = ''
    action: str = 'transition'
    comment: str = ''
    performed_by: str = ''
    metadata: dict = None
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = datetime.now()
