from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class AwardMethod(Enum):
    SINGLE = 'single'            # one winner for everything
    PER_ITEM = 'per_item'        # best per item
    PER_LOT = 'per_lot'          # best per group of items
    SPLIT = 'split'              # distribute qty among suppliers


@dataclass
class AwardItem:
    item_id: str
    item_name: str = ''
    quantity: float = 0.0
    supplier_id: str = ''
    supplier_name: str = ''
    quotation_id: str = ''
    unit_price: float = 0.0
    total: float = 0.0
    delivery_days: int = 0
    notes: str = ''


@dataclass
class AwardDecision:
    rfq_id: str
    method: AwardMethod = AwardMethod.SINGLE
    items: list = None
    created_by: str = ''
    notes: str = ''
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.items is None: self.items = []
        if self.created_at is None: self.created_at = datetime.now()


@dataclass
class GeneratedPO:
    document_id: str = ''
    document_number: str = ''
    supplier_id: str = ''
    supplier_name: str = ''
    total: float = 0.0
    items: list = None
    status: str = 'draft'
    _id: str = ''

    def __post_init__(self):
        if self.items is None: self.items = []
