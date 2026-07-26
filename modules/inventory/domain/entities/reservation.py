from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ReservationStatus(Enum):
    ACTIVE = 'active'
    CONSUMED = 'consumed'
    CANCELLED = 'cancelled'
    EXPIRED = 'expired'


@dataclass
class Reservation:
    item_id: str
    warehouse_id: str
    quantity: float
    order_type: str = ''
    order_id: str = ''
    location_id: str = ''
    lot_id: str = ''
    status: ReservationStatus = ReservationStatus.ACTIVE
    notes: str = ''
    created_by: str = ''
    created_at: datetime = None
    expires_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def consume(self):
        self.status = ReservationStatus.CONSUMED

    def cancel(self):
        self.status = ReservationStatus.CANCELLED

    @property
    def is_expired(self) -> bool:
        if not self.expires_at:
            return False
        return datetime.now() > self.expires_at
