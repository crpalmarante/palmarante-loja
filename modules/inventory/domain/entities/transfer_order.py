from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TransferStatus(Enum):
    DRAFT = 'draft'
    SENT = 'sent'
    IN_TRANSIT = 'in_transit'
    RECEIVED = 'received'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'


@dataclass
class TransferItem:
    item_id: str
    quantity: float
    lot_id: str = ''
    unit_cost: float = 0.0


@dataclass
class TransferOrder:
    from_warehouse_id: str
    to_warehouse_id: str
    items: list = None
    status: TransferStatus = TransferStatus.DRAFT
    notes: str = ''
    created_by: str = ''
    created_at: datetime = None
    sent_at: datetime = None
    received_at: datetime = None
    completed_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.items is None:
            self.items = []
        if self.created_at is None:
            self.created_at = datetime.now()

    def add_item(self, item: TransferItem):
        self.items.append(item)

    def send(self):
        self.status = TransferStatus.SENT
        self.sent_at = datetime.now()

    def mark_in_transit(self):
        self.status = TransferStatus.IN_TRANSIT

    def receive(self):
        self.status = TransferStatus.RECEIVED
        self.received_at = datetime.now()

    def complete(self):
        self.status = TransferStatus.COMPLETED
        self.completed_at = datetime.now()

    def cancel(self):
        self.status = TransferStatus.CANCELLED
