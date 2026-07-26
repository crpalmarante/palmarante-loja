from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class CountStatus(Enum):
    DRAFT = 'draft'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'


@dataclass
class CountLine:
    item_id: str
    expected_quantity: float = 0.0
    actual_quantity: float = 0.0
    location_id: str = ''
    lot_id: str = ''
    notes: str = ''

    @property
    def difference(self) -> float:
        return self.actual_quantity - self.expected_quantity


@dataclass
class InventoryCount:
    warehouse_id: str
    lines: list = None
    status: CountStatus = CountStatus.DRAFT
    counted_by: str = ''
    notes: str = ''
    created_at: datetime = None
    completed_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.lines is None:
            self.lines = []
        if self.created_at is None:
            self.created_at = datetime.now()

    def add_line(self, line: CountLine):
        self.lines.append(line)

    def complete(self):
        self.status = CountStatus.COMPLETED
        self.completed_at = datetime.now()

    @property
    def total_difference(self) -> float:
        return sum(l.difference for l in self.lines)

    @property
    def line_count(self) -> int:
        return len(self.lines)
