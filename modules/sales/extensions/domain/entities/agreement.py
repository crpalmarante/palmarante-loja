from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CustomerAgreement:
    customer_id: str
    customer_name: str = ''
    name: str = ''
    price_list_id: str = ''
    max_discount_pct: float = 0.0
    payment_method: str = ''
    installments: int = 1
    due_days: int = 30
    delivery_term: str = ''
    sales_rep: str = ''
    valid_from: str = ''
    valid_to: str = ''
    active: bool = True
    notes: str = ''
    created_at: datetime = None
    updated_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

    def is_valid(self) -> bool:
        if not self.active:
            return False
        from datetime import date
        today = date.today().isoformat()
        if self.valid_from and today < self.valid_from:
            return False
        if self.valid_to and today > self.valid_to:
            return False
        return True

    def apply_to_order(self, order: dict) -> dict:
        if self.price_list_id:
            order['price_list_id'] = self.price_list_id
        if self.payment_method:
            order['payment_method'] = self.payment_method
        if self.installments:
            order['installments'] = self.installments
        if self.due_days:
            order['due_days'] = self.due_days
        if self.delivery_term:
            order['delivery_term'] = self.delivery_term
        if self.sales_rep:
            order['sales_rep'] = self.sales_rep
        return order
