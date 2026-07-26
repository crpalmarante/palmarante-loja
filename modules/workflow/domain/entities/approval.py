from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ApprovalStatus(Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    CANCELLED = 'cancelled'


@dataclass
class WorkflowApproval:
    instance_id: str
    transition_id: str
    required_count: int = 1
    status: ApprovalStatus = ApprovalStatus.PENDING
    role: str = ''
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def approve(self, user: str = '', comment: str = ''):
        self.status = ApprovalStatus.APPROVED

    def reject(self, user: str = '', comment: str = ''):
        self.status = ApprovalStatus.REJECTED

    @property
    def is_pending(self) -> bool:
        return self.status == ApprovalStatus.PENDING

    @property
    def is_approved(self) -> bool:
        return self.status == ApprovalStatus.APPROVED
