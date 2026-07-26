from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class SerialStatus(Enum):
    AVAILABLE = 'available'
    RESERVED = 'reserved'
    SOLD = 'sold'
    RETURNED = 'returned'
    LOST = 'lost'
    WARRANTY = 'warranty'


@dataclass
class SerialNumber:
    item_id: str
    warehouse_id: str
    serial: str
    lot_id: str = ''
    location_id: str = ''
    status: SerialStatus = SerialStatus.AVAILABLE
    notes: str = ''
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def reserve(self):
        if self.status != SerialStatus.AVAILABLE:
            raise ValueError(f'Serial {self.serial} is {self.status.value}')
        self.status = SerialStatus.RESERVED

    def sell(self):
        if self.status not in (SerialStatus.AVAILABLE, SerialStatus.RESERVED):
            raise ValueError(f'Serial {self.serial} is {self.status.value}')
        self.status = SerialStatus.SOLD

    def mark_returned(self):
        self.status = SerialStatus.RETURNED
