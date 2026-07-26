from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class SalesChannel(str, Enum):
    STORE = 'store'
    PDV = 'pdv'
    ECOMMERCE = 'ecommerce'
    MARKETPLACE = 'marketplace'
    REPRESENTATIVE = 'representative'
    PHONE = 'phone'
    WHATSAPP = 'whatsapp'
    API = 'api'


class CustomerClass(str, Enum):
    BRONZE = 'bronze'
    SILVER = 'silver'
    GOLD = 'gold'
    DIAMOND = 'diamond'


@dataclass
class SalesTag:
    name: str
    color: str = '#6b7280'
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class FavoriteItem:
    customer_id: str
    item_id: str
    item_name: str = ''
    item_code: str = ''
    unit: str = 'UN'
    sort_order: int = 0
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class PriceHistoryEntry:
    item_id: str
    price: float
    price_list_id: str = ''
    price_list_name: str = ''
    recorded_by: str = ''
    source: str = 'manual'
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class ApprovalMatrixRule:
    name: str
    min_value: float = 0.0
    max_value: float = 0.0
    approver_role: str = 'seller'
    active: bool = True
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def matches(self, order_value: float) -> bool:
        if self.max_value > 0:
            return self.min_value <= order_value <= self.max_value
        return order_value >= self.min_value
