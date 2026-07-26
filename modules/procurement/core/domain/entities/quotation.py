from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class QuotationStatus(Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    WITHDRAWN = 'withdrawn'
    COUNTERED = 'countered'


@dataclass
class QuotationItem:
    item_id: str
    item_code: str = ''
    item_name: str = ''
    description: str = ''
    quantity: float = 1.0
    unit_price: float = 0.0
    discount_pct: float = 0.0
    discount_value: float = 0.0
    total: float = 0.0
    delivery_days: int = 0
    warranty_days: int = 0
    technical_response: dict = None  # specs the supplier is offering
    notes: str = ''

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price

    def recalc(self):
        self.discount_value = self.subtotal * self.discount_pct / 100
        self.total = self.subtotal - self.discount_value

    def __post_init__(self):
        if self.technical_response is None:
            self.technical_response = {}


@dataclass
class SupplierQuotation:
    rfq_id: str
    supplier_id: str
    supplier_name: str = ''
    supplier_document: str = ''
    supplier_email: str = ''
    supplier_phone: str = ''
    items: list = None
    total: float = 0.0
    freight: float = 0.0
    insurance: float = 0.0
    other_costs: float = 0.0
    grand_total: float = 0.0
    payment_method: str = 'boleto'
    installments: int = 1
    due_days: int = 30
    delivery_estimate_days: int = 0
    valid_until: str = ''
    warranty_description: str = ''
    notes: str = ''
    terms_acceptance: str = ''
    status: QuotationStatus = QuotationStatus.PENDING
    score: float = 0.0
    score_detail: dict = None
    created_at: datetime = None
    updated_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.items is None: self.items = []
        if self.score_detail is None: self.score_detail = {}
        if self.created_at is None: self.created_at = datetime.now()
        if self.updated_at is None: self.updated_at = datetime.now()

    def recalc(self):
        self.total = sum(i.total for i in self.items)
        self.grand_total = self.total + self.freight + self.insurance + self.other_costs

    def accept(self):
        self.status = QuotationStatus.ACCEPTED
        self.updated_at = datetime.now()

    def reject(self):
        self.status = QuotationStatus.REJECTED
        self.updated_at = datetime.now()

    def mark_countered(self):
        self.status = QuotationStatus.COUNTERED
        self.updated_at = datetime.now()
