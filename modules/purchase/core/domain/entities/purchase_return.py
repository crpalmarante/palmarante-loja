from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ReturnStatus(Enum):
    DRAFT = 'draft'
    SENT = 'sent'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    CANCELLED = 'cancelled'


@dataclass
class PurchaseReturnLine:
    item_id: str
    item_code: str = ''
    item_name: str = ''
    quantity: float = 1.0
    unit_price: float = 0.0
    total: float = 0.0
    reason: str = ''
    notes: str = ''
    _id: str = ''


@dataclass
class PurchaseReturn:
    po_id: str
    po_number: str = ''
    supplier_id: str = ''
    supplier_name: str = ''
    document_id: str = ''
    lines: list = None
    status: ReturnStatus = ReturnStatus.DRAFT
    reason: str = ''
    notes: str = ''
    created_by: str = ''
    created_at: datetime = None
    updated_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.lines is None:
            self.lines = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

    @property
    def total(self) -> float:
        return sum(l.total for l in self.lines)
