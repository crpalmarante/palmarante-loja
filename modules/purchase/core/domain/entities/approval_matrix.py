from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ApprovalScope(Enum):
    PURCHASE_ORDER = 'purchase_order'
    REQUISITION = 'requisition'
    RFQ = 'rfq'
    AGREEMENT = 'agreement'


@dataclass
class ApprovalMatrixRule:
    scope: ApprovalScope = ApprovalScope.PURCHASE_ORDER
    min_value: float = 0.0
    max_value: float = float('inf')
    approver_role: str = 'supervisor'
    approver_name: str = ''
    priority: int = 0
    active: bool = True
    notes: str = ''
    _id: str = ''

    def matches(self, value: float) -> bool:
        return self.min_value <= value <= self.max_value

    def description(self) -> str:
        if self.max_value == float('inf'):
            return f'Acima de {self.min_value:.0f} → {self.approver_role}'
        return f'{self.min_value:.0f} a {self.max_value:.0f} → {self.approver_role}'


class ApprovalEngine:
    def __init__(self, rules: list = None):
        self._rules = rules or []

    def set_rules(self, rules: list):
        self._rules = rules

    def find_approver(self, value: float, scope: ApprovalScope = ApprovalScope.PURCHASE_ORDER) -> str:
        candidates = [r for r in self._rules if r.active and r.scope == scope and r.matches(value)]
        if not candidates:
            return 'buyer'
        candidates.sort(key=lambda r: r.priority, reverse=True)
        return candidates[0].approver_role

    def needs_approval(self, value: float, scope: ApprovalScope = ApprovalScope.PURCHASE_ORDER) -> bool:
        role = self.find_approver(value, scope)
        return role != 'buyer'
