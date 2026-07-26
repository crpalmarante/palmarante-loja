from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class RequestStatus(Enum):
    DRAFT = 'draft'
    PENDING = 'pending'
    APPROVED = 'approved'
    CONSOLIDATED = 'consolidated'
    REJECTED = 'rejected'
    CANCELLED = 'cancelled'


@dataclass
class PurchaseRequestItem:
    item_id: str
    item_code: str = ''
    item_name: str = ''
    quantity: float = 1.0
    unit: str = 'UN'
    estimated_price: float = 0.0
    estimated_total: float = 0.0
    required_date: str = ''
    justification: str = ''
    notes: str = ''
    _id: str = ''


@dataclass
class PurchaseRequest:
    title: str
    number: str = ''
    department: str = ''
    requestor: str = ''
    requestor_email: str = ''
    items: list = None
    status: RequestStatus = RequestStatus.DRAFT
    urgency: str = 'medium'
    justification: str = ''
    notes: str = ''
    approved_by: str = ''
    rejected_reason: str = ''
    consolidated_to: str = ''
    created_at: datetime = None
    updated_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.items is None:
            self.items = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

    @property
    def estimated_total(self) -> float:
        return sum(i.estimated_total for i in self.items)

    def approve(self, by: str = ''):
        self.status = RequestStatus.APPROVED
        self.approved_by = by
        self.updated_at = datetime.now()

    def reject(self, reason: str = ''):
        self.status = RequestStatus.REJECTED
        self.rejected_reason = reason
        self.updated_at = datetime.now()
