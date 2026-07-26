from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class InstanceStatus(Enum):
    ACTIVE = 'active'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    SUSPENDED = 'suspended'


@dataclass
class WorkflowInstance:
    workflow_id: str
    document_type: str
    document_id: str
    current_state_id: str
    document_data: dict = None
    status: InstanceStatus = InstanceStatus.ACTIVE
    started_at: datetime = None
    completed_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.document_data is None:
            self.document_data = {}
        if self.started_at is None:
            self.started_at = datetime.now()

    def advance(self, to_state_id: str):
        self.current_state_id = to_state_id

    def complete(self):
        self.status = InstanceStatus.COMPLETED
        self.completed_at = datetime.now()

    def cancel(self):
        self.status = InstanceStatus.CANCELLED
        self.completed_at = datetime.now()

    def suspend(self):
        self.status = InstanceStatus.SUSPENDED
