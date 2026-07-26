from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AgreementPriceItem:
    item_id: str
    item_code: str = ''
    item_name: str = ''
    price: float = 0.0
    max_discount_pct: float = 0.0
    min_quantity: float = 0.0
    notes: str = ''


@dataclass
class SupplierAgreement:
    supplier_id: str
    supplier_name: str = ''
    name: str = ''
    number: str = ''
    description: str = ''
    items: list = None
    max_discount_pct: float = 0.0
    payment_method: str = ''
    installments: int = 1
    due_days: int = 30
    delivery_term: str = ''
    warranty: str = ''
    valid_from: str = ''
    valid_to: str = ''
    auto_renew: bool = False
    active: bool = True
    notes: str = ''
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

    def get_item_price(self, item_id: str) -> float | None:
        for i in self.items:
            if i.item_id == item_id:
                return i.price
        return None
