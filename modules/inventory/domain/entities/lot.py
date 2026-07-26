from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum


class LotStatus(Enum):
    ACTIVE = 'active'
    BLOCKED = 'blocked'
    EXPIRED = 'expired'
    CONSUMED = 'consumed'


@dataclass
class Lot:
    item_id: str
    warehouse_id: str
    lot_number: str
    supplier_lot: str = ''
    manufacturing_date: date = None
    expiry_date: date = None
    origin: str = ''
    status: LotStatus = LotStatus.ACTIVE
    notes: str = ''
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    @property
    def is_expired(self) -> bool:
        if not self.expiry_date:
            return False
        return date.today() > self.expiry_date

    @property
    def days_to_expiry(self) -> int | None:
        if not self.expiry_date:
            return None
        return (self.expiry_date - date.today()).days

    def block(self):
        self.status = LotStatus.BLOCKED

    def mark_expired(self):
        self.status = LotStatus.EXPIRED
