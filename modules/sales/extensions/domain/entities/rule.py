from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class RuleCondition(str, Enum):
    CUSTOMER_TYPE = 'customer_type'
    QUANTITY = 'quantity'
    TOTAL = 'total'
    CHANNEL = 'channel'
    ITEM_CATEGORY = 'item_category'
    PAYMENT_METHOD = 'payment_method'


class RuleAction(str, Enum):
    APPLY_PRICE_LIST = 'apply_price_list'
    APPLY_DISCOUNT = 'apply_discount'
    APPLY_COMMISSION = 'apply_commission'
    BLOCK = 'block'
    REQUEST_APPROVAL = 'request_approval'


@dataclass
class SalesRule:
    name: str
    code: str = ''
    description: str = ''
    condition_field: str = ''
    condition_operator: str = 'equals'
    condition_value: str = ''
    action_field: RuleAction = RuleAction.APPLY_DISCOUNT
    action_value: str = ''
    priority: int = 0
    active: bool = True
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def evaluate(self, context: dict) -> dict:
        field_val = context.get(self.condition_field, str(context.get(self.condition_field, '')))
        matched = False
        if self.condition_operator == 'equals':
            matched = str(field_val) == self.condition_value
        elif self.condition_operator == 'greater_than':
            matched = float(field_val) > float(self.condition_value)
        elif self.condition_operator == 'less_than':
            matched = float(field_val) < float(self.condition_value)
        elif self.condition_operator == 'in':
            matched = str(field_val) in [s.strip() for s in self.condition_value.split(',')]
        if matched:
            return {'matched': True, 'action': self.action_field.value,
                    'action_value': self.action_value, 'rule_name': self.name}
        return {'matched': False}
