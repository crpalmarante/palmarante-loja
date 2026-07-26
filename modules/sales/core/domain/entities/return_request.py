from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ReturnStatus(Enum):
    REQUESTED = 'requested'
    AUTHORIZED = 'authorized'
    RECEIVED = 'received'
    INSPECTED = 'inspected'
    REFUNDED = 'refunded'
    REPLACED = 'replaced'
    REJECTED = 'rejected'


@dataclass
class ReturnItem:
    item_id: str
    item_name: str = ''
    quantity: float = 0
    reason: str = ''
    condition: str = ''
    action: str = 'refund'


@dataclass
class ReturnRequest:
    document_id: str
    document_number: str = ''
    customer_id: str = ''
    customer_name: str = ''
    status: ReturnStatus = ReturnStatus.REQUESTED
    items: list = None
    reason: str = ''
    sales_rep: str = ''
    notes: str = ''
    created_at: datetime = None
    updated_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.items is None:
            self.items = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
