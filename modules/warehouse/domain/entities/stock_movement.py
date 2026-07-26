from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class MovementType(Enum):
    IN = 'in'
    OUT = 'out'
    TRANSFER = 'transfer'
    ADJUSTMENT = 'adjustment'
    RESERVATION = 'reservation'
    CANCELLATION = 'cancellation'


class MovementStatus(Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'


@dataclass
class StockMovement:
    item_id: str
    warehouse_id: str
    movement_type: MovementType
    quantity: float
    reference_type: str = ''
    reference_id: str = ''
    notes: str = ''
    status: MovementStatus = MovementStatus.PENDING
    created_at: datetime = None
    confirmed_at: datetime = None
    target_warehouse_id: str = ''
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def confirm(self):
        self.status = MovementStatus.CONFIRMED
        self.confirmed_at = datetime.now()

    def cancel(self):
        self.status = MovementStatus.CANCELLED
