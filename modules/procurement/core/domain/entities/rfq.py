from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class RFQStatus(Enum):
    DRAFT = 'draft'
    OPEN = 'open'
    IN_NEGOTIATION = 'in_negotiation'
    AWARDED = 'awarded'
    CANCELLED = 'cancelled'
    CLOSED = 'closed'


@dataclass
class TechnicalSpec:
    field: str
    value: str
    unit: str = ''
    is_differentiator: bool = False


@dataclass
class RFQItem:
    item_id: str
    item_code: str = ''
    item_name: str = ''
    description: str = ''
    quantity: float = 1.0
    unit: str = 'UN'
    expected_price: float = 0.0
    required_date: str = ''
    technical_specs: list = None
    category: str = ''
    notes: str = ''
    sort_order: int = 0
    _id: str = ''

    def __post_init__(self):
        if self.technical_specs is None:
            self.technical_specs = []

    def add_spec(self, field: str, value: str, unit: str = '', is_differentiator: bool = False):
        self.technical_specs.append(TechnicalSpec(field=field, value=value, unit=unit,
                                                   is_differentiator=is_differentiator))


@dataclass
class RFQ:
    title: str
    number: str = ''
    description: str = ''
    items: list = None
    invited_suppliers: list = None
    status: RFQStatus = RFQStatus.DRAFT
    delivery_address: str = ''
    payment_terms: str = ''
    valid_until: str = ''
    requires_technical_evaluation: bool = False
    notes: str = ''
    internal_notes: str = ''
    created_by: str = ''
    created_at: datetime = None
    updated_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.items is None: self.items = []
        if self.invited_suppliers is None: self.invited_suppliers = []
        if self.created_at is None: self.created_at = datetime.now()
        if self.updated_at is None: self.updated_at = datetime.now()

    def open(self):
        self.status = RFQStatus.OPEN
        self.updated_at = datetime.now()

    def close(self):
        self.status = RFQStatus.CLOSED
        self.updated_at = datetime.now()

    def cancel(self):
        self.status = RFQStatus.CANCELLED
        self.updated_at = datetime.now()
