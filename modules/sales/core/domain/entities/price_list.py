from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class PriceListItem:
    item_id: str
    price: float
    min_price: float = 0.0
    currency: str = 'BRL'
    effective_from: str = ''
    effective_to: str = ''


@dataclass
class PriceList:
    name: str
    code: str
    items: dict = None
    active: bool = True
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.items is None:
            self.items = {}
        if self.created_at is None:
            self.created_at = datetime.now()

    def get_price(self, item_id: str) -> float | None:
        item = self.items.get(item_id)
        return item.price if item else None

    def set_price(self, item_id: str, price: float, min_price: float = 0.0):
        self.items[item_id] = PriceListItem(item_id=item_id, price=price, min_price=min_price)
