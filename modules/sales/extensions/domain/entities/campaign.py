from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class CampaignType(str, Enum):
    PERCENTAGE = 'percentage'
    FIXED = 'fixed'
    FREE_SHIPPING = 'free_shipping'
    BUY_X_GET_Y = 'buy_x_get_y'


class CampaignTarget(str, Enum):
    ALL = 'all'
    CUSTOMER_CLASS = 'customer_class'
    SPECIFIC_CUSTOMERS = 'specific_customers'
    FIRST_PURCHASE = 'first_purchase'


@dataclass
class Campaign:
    name: str
    code: str = ''
    campaign_type: CampaignType = CampaignType.PERCENTAGE
    target: CampaignTarget = CampaignTarget.ALL
    value: float = 0.0
    min_order_value: float = 0.0
    customer_classes: list = None
    customer_ids: list = None
    item_ids: list = None
    valid_from: str = ''
    valid_to: str = ''
    active: bool = True
    usage_limit: int = 0
    used_count: int = 0
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.customer_classes is None:
            self.customer_classes = []
        if self.customer_ids is None:
            self.customer_ids = []
        if self.item_ids is None:
            self.item_ids = []
        if self.created_at is None:
            self.created_at = datetime.now()

    def is_valid(self, customer_id: str = '', customer_class: str = '',
                 order_total: float = 0.0) -> bool:
        if not self.active:
            return False
        if self.usage_limit > 0 and self.used_count >= self.usage_limit:
            return False
        if self.min_order_value > 0 and order_total < self.min_order_value:
            return False
        if self.target == CampaignTarget.CUSTOMER_CLASS:
            return customer_class in self.customer_classes
        if self.target == CampaignTarget.SPECIFIC_CUSTOMERS:
            return customer_id in self.customer_ids
        if self.target == CampaignTarget.FIRST_PURCHASE:
            return True
        return True

    def apply(self, order_total: float) -> float:
        if self.campaign_type == CampaignType.PERCENTAGE:
            return order_total * self.value / 100
        elif self.campaign_type == CampaignType.FIXED:
            return min(self.value, order_total)
        return 0.0
