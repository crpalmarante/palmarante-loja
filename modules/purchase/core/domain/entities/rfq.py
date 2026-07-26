from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class RFQStatus(Enum):
    DRAFT = 'draft'
    OPEN = 'open'
    CLOSED = 'closed'
    CANCELLED = 'cancelled'


@dataclass
class RFQItem:
    item_id: str
    item_code: str = ''
    item_name: str = ''
    quantity: float = 1.0
    unit: str = 'UN'
    expected_price: float = 0.0
    required_date: str = ''
    technical_spec: str = ''
    notes: str = ''
    sort_order: int = 0
    _id: str = ''


@dataclass
class RFQ:
    title: str
    number: str = ''
    requisition_id: str = ''
    description: str = ''
    items: list = None
    invited_suppliers: list = None
    status: RFQStatus = RFQStatus.DRAFT
    delivery_address: str = ''
    payment_terms: str = ''
    valid_until: str = ''
    notes: str = ''
    internal_notes: str = ''
    created_by: str = ''
    created_at: datetime = None
    updated_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.items is None:
            self.items = []
        if self.invited_suppliers is None:
            self.invited_suppliers = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

    def open(self):
        self.status = RFQStatus.OPEN
        self.updated_at = datetime.now()

    def close(self):
        self.status = RFQStatus.CLOSED
        self.updated_at = datetime.now()
