from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class CreditStatus(str, Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    LIMIT_EXCEEDED = 'limit_exceeded'


@dataclass
class CustomerCredit:
    customer_id: str
    customer_name: str = ''
    credit_limit: float = 0.0
    used_balance: float = 0.0
    available_balance: float = 0.0
    status: CreditStatus = CreditStatus.PENDING
    last_check: datetime = None
    notes: str = ''
    created_at: datetime = None
    updated_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        self.available_balance = self.credit_limit - self.used_balance

    def check_order(self, order_total: float) -> CreditStatus:
        needed = self.used_balance + order_total
        if self.credit_limit <= 0:
            return CreditStatus.PENDING
        if needed > self.credit_limit:
            self.status = CreditStatus.LIMIT_EXCEEDED
        else:
            self.status = CreditStatus.APPROVED
        self.last_check = datetime.now()
        self.updated_at = datetime.now()
        return self.status
