from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class CommissionType(Enum):
    PERCENTAGE = 'percentage'
    FIXED = 'fixed'
    TIERED = 'tiered'


@dataclass
class CommissionRule:
    name: str
    code: str
    commission_type: CommissionType = CommissionType.PERCENTAGE
    rate: float = 0.0
    fixed_value: float = 0.0
    tiers: list = None
    item_ids: list = None
    customer_group_ids: list = None
    sales_rep_ids: list = None
    active: bool = True
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.tiers is None:
            self.tiers = []
        if self.item_ids is None:
            self.item_ids = []
        if self.customer_group_ids is None:
            self.customer_group_ids = []
        if self.sales_rep_ids is None:
            self.sales_rep_ids = []
        if self.created_at is None:
            self.created_at = datetime.now()

    def calculate(self, amount: float, quantity: float = 1) -> float:
        if self.commission_type == CommissionType.FIXED:
            return self.fixed_value * quantity
        elif self.commission_type == CommissionType.TIERED:
            for t in sorted(self.tiers, key=lambda x: x.get('min_amount', 0), reverse=True):
                if amount >= t.get('min_amount', 0):
                    rate = t.get('rate', self.rate)
                    return amount * rate / 100
            return amount * self.rate / 100
        else:
            return amount * self.rate / 100


@dataclass
class CommissionStatement:
    sales_rep_id: str
    sales_rep_name: str = ''
    period: str = ''
    document_ids: list = None
    lines: list = None
    total_commission: float = 0.0
    status: str = 'pending'
    paid_at: datetime = None
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.document_ids is None:
            self.document_ids = []
        if self.lines is None:
            self.lines = []
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class CommissionLine:
    document_id: str
    document_number: str
    base_amount: float
    rate: float
    commission_value: float
    item_id: str = ''
