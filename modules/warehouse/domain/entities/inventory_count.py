from dataclasses import dataclass
from datetime import datetime


@dataclass
class InventoryCount:
    warehouse_id: str
    item_id: str
    expected_quantity: float = 0.0
    actual_quantity: float = 0.0
    counted_by: str = ''
    notes: str = ''
    counted_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.counted_at is None:
            self.counted_at = datetime.now()

    @property
    def difference(self) -> float:
        return self.actual_quantity - self.expected_quantity
