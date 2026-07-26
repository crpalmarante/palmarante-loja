from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class BundleItem:
    item_id: str
    item_name: str = ''
    quantity: float = 1.0
    unit: str = 'UN'
    optional: bool = False


@dataclass
class SalesBundle:
    name: str
    code: str = ''
    description: str = ''
    items: list = None
    bundle_price: float = 0.0
    savings_pct: float = 0.0
    active: bool = True
    valid_from: str = ''
    valid_to: str = ''
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.items is None:
            self.items = []
        if self.created_at is None:
            self.created_at = datetime.now()

    def get_total_standalone(self, price_engine=None) -> float:
        total = 0.0
        for bi in self.items:
            if price_engine:
                total += price_engine.get_item_price(bi.item_id) * bi.quantity
        return total
