from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class WorkflowStatus(Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


@dataclass
class Workflow:
    name: str
    code: str
    description: str = ''
    document_type: str = ''
    initial_state_id: str = ''
    status: WorkflowStatus = WorkflowStatus.ACTIVE
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def activate(self):
        self.status = WorkflowStatus.ACTIVE

    def deactivate(self):
        self.status = WorkflowStatus.INACTIVE
