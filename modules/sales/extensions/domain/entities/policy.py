from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class PolicyAction(str, Enum):
    BLOCK = 'block'
    WARN = 'warn'
    REQUEST_APPROVAL = 'request_approval'
    FORCE_PAYMENT_METHOD = 'force_payment_method'


class PolicyScope(str, Enum):
    GLOBAL = 'global'
    CUSTOMER = 'customer'
    ITEM = 'item'
    CUSTOMER_CLASS = 'customer_class'
    CHANNEL = 'channel'


@dataclass
class SalesPolicy:
    name: str
    code: str = ''
    description: str = ''
    scope: PolicyScope = PolicyScope.GLOBAL
    action: PolicyAction = PolicyAction.WARN
    condition_field: str = ''
    condition_operator: str = 'equals'
    condition_value: str = ''
    action_value: str = ''
    active: bool = True
    priority: int = 0
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def evaluate(self, context: dict) -> dict:
        field_val = context.get(self.condition_field, '')
        matched = False
        if self.condition_operator == 'equals':
            matched = str(field_val) == self.condition_value
        elif self.condition_operator == 'greater_than':
            matched = float(field_val) > float(self.condition_value)
        elif self.condition_operator == 'less_than':
            matched = float(field_val) < float(self.condition_value)
        elif self.condition_operator == 'contains':
            matched = self.condition_value in str(field_val)
        if matched:
            return {'matched': True, 'action': self.action.value,
                    'action_value': self.action_value, 'policy_name': self.name}
        return {'matched': False}
