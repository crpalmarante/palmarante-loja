from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class PurchaseOrderStatus(Enum):
    DRAFT = 'draft'
    PENDING_APPROVAL = 'pending_approval'
    APPROVED = 'approved'
    SENT = 'sent'
    CONFIRMED = 'confirmed'
    PARTIAL = 'partial'
    RECEIVED = 'received'
    CANCELLED = 'cancelled'
    CLOSED = 'closed'


@dataclass
class PurchaseOrderLine:
    item_id: str
    item_code: str = ''
    item_name: str = ''
    quantity: float = 1.0
    unit: str = 'UN'
    unit_price: float = 0.0
    discount_pct: float = 0.0
    discount_value: float = 0.0
    tax_value: float = 0.0
    total: float = 0.0
    received_qty: float = 0.0
    delivery_date: str = ''
    notes: str = ''
    sort_order: int = 0
    _id: str = ''

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price

    @property
    def pending_qty(self) -> float:
        return self.quantity - self.received_qty


@dataclass
class PurchasePaymentTerms:
    method: str = 'boleto'
    installments: int = 1
    due_days: int = 30
    notes: str = ''


@dataclass
class PurchaseInstallment:
    number: int
    due_date: str
    value: float
    status: str = 'pending'
    _id: str = ''


@dataclass
class PurchaseOrder:
    document_id: str
    document_number: str = ''
    document_type: str = 'purchase_order'
    supplier_id: str = ''
    supplier_name: str = ''
    supplier_document: str = ''
    quotation_id: str = ''
    requisition_id: str = ''
    rfq_id: str = ''
    lines: list = None
    installments: list = None
    payment_terms: PurchasePaymentTerms = None
    subtotal: float = 0.0
    discount_total: float = 0.0
    tax_total: float = 0.0
    freight: float = 0.0
    total: float = 0.0
    status: PurchaseOrderStatus = PurchaseOrderStatus.DRAFT
    expected_delivery: str = ''
    delivery_address: str = ''
    shipping_notes: str = ''
    notes: str = ''
    internal_notes: str = ''
    created_by: str = ''
    approved_by: str = ''
    created_at: datetime = None
    updated_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.lines is None:
            self.lines = []
        if self.installments is None:
            self.installments = []
        if self.payment_terms is None:
            self.payment_terms = PurchasePaymentTerms()
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

    def add_line(self, line: PurchaseOrderLine):
        self.lines.append(line)
        self.recalc()

    def recalc(self):
        self.subtotal = sum(l.subtotal for l in self.lines)
        self.discount_total = sum(l.discount_value for l in self.lines)
        self.tax_total = sum(l.tax_value for l in self.lines)
        self.total = self.subtotal - self.discount_total + self.tax_total + self.freight

    def approve(self, by: str = ''):
        self.status = PurchaseOrderStatus.APPROVED
        self.approved_by = by
        self.updated_at = datetime.now()

    def send(self):
        self.status = PurchaseOrderStatus.SENT
        self.updated_at = datetime.now()

    def receive_line(self, line_id: str, qty: float):
        for line in self.lines:
            if line._id == line_id:
                line.received_qty += qty
                break
        pending = sum(l.pending_qty for l in self.lines)
        self.status = PurchaseOrderStatus.RECEIVED if pending == 0 else PurchaseOrderStatus.PARTIAL
        self.updated_at = datetime.now()

    def cancel(self):
        self.status = PurchaseOrderStatus.CANCELLED
        self.updated_at = datetime.now()
