from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class RuleType(Enum):
    CONDITION = 'condition'
    VALIDATION = 'validation'
    APPROVAL = 'approval'
    NOTIFICATION = 'notification'
    TIMER = 'timer'


class RuleOperator(Enum):
    EQUALS = 'equals'
    NOT_EQUALS = 'not_equals'
    GREATER_THAN = 'greater_than'
    LESS_THAN = 'less_than'
    GREATER_OR_EQUAL = 'greater_or_equal'
    LESS_OR_EQUAL = 'less_or_equal'
    CONTAINS = 'contains'
    IN = 'in'


@dataclass
class WorkflowRule:
    workflow_id: str
    name: str
    rule_type: RuleType = RuleType.CONDITION
    transition_id: str = ''
    field: str = ''
    operator: RuleOperator = RuleOperator.EQUALS
    value: str = ''
    error_message: str = ''
    target_role: str = ''
    sort_order: int = 0
    active: bool = True
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def evaluate(self, document: dict) -> bool:
        if not self.field or not document:
            return True
        actual = document.get(self.field)
        expected = self.value
        try:
            if self.operator == RuleOperator.EQUALS:
                return str(actual) == expected
            elif self.operator == RuleOperator.NOT_EQUALS:
                return str(actual) != expected
            elif self.operator == RuleOperator.GREATER_THAN:
                return float(actual or 0) > float(expected)
            elif self.operator == RuleOperator.LESS_THAN:
                return float(actual or 0) < float(expected)
            elif self.operator == RuleOperator.GREATER_OR_EQUAL:
                return float(actual or 0) >= float(expected)
            elif self.operator == RuleOperator.LESS_OR_EQUAL:
                return float(actual or 0) <= float(expected)
            elif self.operator == RuleOperator.CONTAINS:
                return expected in str(actual or '')
            elif self.operator == RuleOperator.IN:
                return str(actual or '') in [x.strip() for x in expected.split(',')]
        except (ValueError, TypeError):
            return False
        return True
