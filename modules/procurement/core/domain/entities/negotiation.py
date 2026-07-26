from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class NegotiationRound(Enum):
    INITIAL = 'initial'
    COUNTER = 'counter'
    FINAL = 'final'


@dataclass
class CounterProposal:
    round: NegotiationRound = NegotiationRound.INITIAL
    proposed_by: str = ''  # 'buyer' or 'supplier'
    supplier_id: str = ''
    quotation_id: str = ''
    items: list = None
    total: float = 0.0
    freight: float = 0.0
    grand_total: float = 0.0
    delivery_days: int = 0
    payment_method: str = ''
    installments: int = 0
    notes: str = ''
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.items is None: self.items = []
        if self.created_at is None: self.created_at = datetime.now()


@dataclass
class NegotiationItem:
    item_id: str
    unit_price: float = 0.0
    quantity: float = 0.0
    discount_pct: float = 0.0
    delivery_days: int = 0
    notes: str = ''
