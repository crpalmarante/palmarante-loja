from dataclasses import dataclass
from datetime import datetime
from modules.inventory.domain.value_objects.movement_type import MovementType, MovementStatus


@dataclass
class StockMovement:
    item_id: str
    warehouse_id: str
    movement_type: MovementType
    quantity: float
    location_id: str = ''
    lot_id: str = ''
    serial_number: str = ''
    reference_type: str = ''
    reference_id: str = ''
    document_number: str = ''
    unit_cost: float = 0.0
    notes: str = ''
    created_by: str = ''
    status: MovementStatus = MovementStatus.PENDING
    created_at: datetime = None
    confirmed_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def confirm(self):
        self.status = MovementStatus.CONFIRMED
        self.confirmed_at = datetime.now()

    def cancel(self):
        self.status = MovementStatus.CANCELLED

    @property
    def is_entry(self) -> bool:
        return self.movement_type in (MovementType.IN, MovementType.RETURN, MovementType.PRODUCTION)

    @property
    def is_exit(self) -> bool:
        return self.movement_type in (MovementType.OUT, MovementType.CONSUMPTION)

    @property
    def is_reservation(self) -> bool:
        return self.movement_type == MovementType.RESERVE

    @property
    def net_effect(self) -> float:
        if self.is_entry:
            return self.quantity
        if self.is_exit:
            return -self.quantity
        return 0.0
