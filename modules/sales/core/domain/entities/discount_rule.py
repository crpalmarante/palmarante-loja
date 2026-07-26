from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class DiscountType(Enum):
    PERCENTAGE = 'percentage'
    FIXED = 'fixed'
    TIERED = 'tiered'


class DiscountScope(Enum):
    GLOBAL = 'global'
    CATEGORY = 'category'
    ITEM = 'item'
    CUSTOMER = 'customer'
    CUSTOMER_GROUP = 'customer_group'


@dataclass
class DiscountTier:
    min_quantity: float = 0
    min_value: float = 0
    discount_pct: float = 0
    discount_value: float = 0


@dataclass
class DiscountRule:
    name: str
    code: str
    discount_type: DiscountType = DiscountType.PERCENTAGE
    scope: DiscountScope = DiscountScope.GLOBAL
    value: float = 0.0
    tiers: list = None
    item_ids: list = None
    customer_ids: list = None
    min_order_value: float = 0.0
    max_discount_value: float = 0.0
    active: bool = True
    priority: int = 0
    valid_from: str = ''
    valid_to: str = ''
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.tiers is None:
            self.tiers = []
        if self.item_ids is None:
            self.item_ids = []
        if self.customer_ids is None:
            self.customer_ids = []
        if self.created_at is None:
            self.created_at = datetime.now()

    def calculate(self, price: float, quantity: float = 1,
                  order_total: float = 0.0) -> float:
        if self.discount_type == DiscountType.FIXED:
            return min(self.value, price)
        elif self.discount_type == DiscountType.TIERED:
            for t in sorted(self.tiers, key=lambda x: x.min_quantity, reverse=True):
                if quantity >= t.min_quantity and order_total >= t.min_value:
                    return price * t.discount_pct / 100 if t.discount_pct else t.discount_value
            return 0.0
        else:
            disc = price * self.value / 100
            if self.max_discount_value > 0:
                disc = min(disc, self.max_discount_value)
            return disc
