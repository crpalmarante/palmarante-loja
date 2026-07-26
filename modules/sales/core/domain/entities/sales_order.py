from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class SalesOrderStatus(Enum):
    DRAFT = 'draft'
    PENDING_APPROVAL = 'pending_approval'
    APPROVED = 'approved'
    RESERVED = 'reserved'
    PICKING = 'picking'
    SHIPPED = 'shipped'
    INVOICED = 'invoiced'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    RETURNED = 'returned'


class PaymentMethod(Enum):
    BOLETO = 'boleto'
    CREDIT_CARD = 'credit_card'
    DEBIT_CARD = 'debit_card'
    PIX = 'pix'
    TRANSFER = 'transfer'
    CASH = 'cash'
    CHECK = 'check'


class InstallmentStatus(Enum):
    PENDING = 'pending'
    PAID = 'paid'
    OVERDUE = 'overdue'
    CANCELLED = 'cancelled'


@dataclass
class SalesPaymentTerms:
    method: PaymentMethod = PaymentMethod.PIX
    installments: int = 1
    due_days: int = 30
    notes: str = ''


@dataclass
class SalesInstallment:
    number: int
    due_date: str
    value: float
    status: InstallmentStatus = InstallmentStatus.PENDING
    paid_at: str = ''
    paid_value: float = 0.0
    _id: str = ''


@dataclass
class SalesCondition:
    field: str
    operator: str = 'equals'
    value: str = ''
    description: str = ''


@dataclass
class SalesOrderLine:
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
    notes: str = ''
    sort_order: int = 0
    _id: str = ''

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price

    @property
    def net_total(self) -> float:
        return self.subtotal - self.discount_value + self.tax_value


@dataclass
class SalesShipment:
    document_id: str = ''
    document_number: str = ''
    carrier: str = ''
    tracking_code: str = ''
    status: str = 'pending'
    origin_warehouse: str = ''
    destination: str = ''
    shipped_at: datetime = None
    delivered_at: datetime = None
    items: list = None
    notes: str = ''
    _id: str = ''

    def __post_init__(self):
        if self.items is None:
            self.items = []

    def ship(self, tracking: str = ''):
        self.status = 'shipped'
        self.tracking_code = tracking or self.tracking_code
        self.shipped_at = datetime.now()

    def deliver(self):
        self.status = 'delivered'
        self.delivered_at = datetime.now()


@dataclass
class SalesRepresentative:
    rep_id: str
    name: str = ''
    commission_rate: float = 0.0
    role: str = 'seller'
    email: str = ''


@dataclass
class SalesCommission:
    rep_id: str
    rep_name: str = ''
    rate: float = 0.0
    base_amount: float = 0.0
    value: float = 0.0
    status: str = 'pending'
    _id: str = ''

    def calculate(self, base: float, rate: float = None):
        r = rate or self.rate
        self.base_amount = base
        self.value = base * r / 100

    def pay(self):
        self.status = 'paid'


@dataclass
class SalesOrder:
    document_id: str
    document_number: str = ''
    document_type: str = 'sale_order'

    customer_id: str = ''
    customer_name: str = ''
    sales_rep: SalesRepresentative = None

    payment_terms: SalesPaymentTerms = None
    conditions: list = None
    lines: list = None
    shipments: list = None
    commissions: list = None
    installments: list = None

    subtotal: float = 0.0
    discount_total: float = 0.0
    tax_total: float = 0.0
    freight: float = 0.0
    total: float = 0.0

    status: SalesOrderStatus = SalesOrderStatus.DRAFT
    notes: str = ''
    opportunity_id: str = ''
    expected_delivery: str = ''

    # Sales Experience fields
    channel: str = ''
    tags: list = None
    classification: str = ''
    source_order_id: str = ''  # for duplicates/templates

    created_by: str = ''
    created_at: datetime = None
    updated_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.conditions is None:
            self.conditions = []
        if self.lines is None:
            self.lines = []
        if self.shipments is None:
            self.shipments = []
        if self.commissions is None:
            self.commissions = []
        if self.installments is None:
            self.installments = []
        if self.tags is None:
            self.tags = []
        if self.payment_terms is None:
            self.payment_terms = SalesPaymentTerms()
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

    def duplicate(self, customer_id: str = '', customer_name: str = '') -> 'SalesOrder':
        from copy import deepcopy
        new = deepcopy(self)
        new._id = ''
        new.document_id = ''
        new.document_number = ''
        new.source_order_id = self._id or self.document_number
        new.status = SalesOrderStatus.DRAFT
        new.created_at = datetime.now()
        new.updated_at = datetime.now()
        new.shipments = []
        new.commissions = []
        new.installments = []
        if customer_id:
            new.customer_id = customer_id
            new.customer_name = customer_name or customer_name
        return new

    def add_line(self, line: SalesOrderLine):
        self.lines.append(line)
        self._recalc()

    def remove_line(self, line_id: str):
        self.lines = [l for l in self.lines if l._id != line_id]
        self._recalc()

    def _recalc(self):
        self.subtotal = sum(l.subtotal for l in self.lines)
        self.discount_total = sum(l.discount_value for l in self.lines)
        self.tax_total = sum(l.tax_value for l in self.lines)
        self.total = self.subtotal - self.discount_total + self.tax_total + self.freight

    def recalc(self):
        self._recalc()

    def approve(self):
        self.status = SalesOrderStatus.APPROVED
        self.updated_at = datetime.now()

    def cancel(self):
        self.status = SalesOrderStatus.CANCELLED
        self.updated_at = datetime.now()

    def add_shipment(self, shipment: SalesShipment):
        self.shipments.append(shipment)
        self.status = SalesOrderStatus.PICKING
        self.updated_at = datetime.now()

    def add_commission(self, commission: SalesCommission):
        self.commissions.append(commission)

    def generate_installments(self) -> list:
        if not self.payment_terms or self.payment_terms.installments <= 1:
            self.installments = [SalesInstallment(
                number=1,
                due_date=self._calc_due_date(0),
                value=self.total,
            )]
        else:
            n = self.payment_terms.installments
            installment_value = round(self.total / n, 2)
            diff = self.total - installment_value * n
            self.installments = []
            for i in range(n):
                value = installment_value + (diff if i == n - 1 else 0)
                self.installments.append(SalesInstallment(
                    number=i + 1,
                    due_date=self._calc_due_date(i * self.payment_terms.due_days),
                    value=value,
                ))
        return self.installments

    def _calc_due_date(self, days_offset: int) -> str:
        from datetime import timedelta
        d = self.created_at + timedelta(days=days_offset)
        return d.strftime('%Y-%m-%d')
