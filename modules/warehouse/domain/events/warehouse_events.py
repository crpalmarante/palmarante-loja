from dataclasses import dataclass
from datetime import datetime


@dataclass
class StockMovementCreated:
    movement_id: str
    item_id: str
    warehouse_id: str
    movement_type: str
    quantity: float
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class StockMovementConfirmed:
    movement_id: str
    item_id: str
    warehouse_id: str
    quantity: float
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class LowStockAlert:
    item_id: str
    warehouse_id: str
    current_quantity: float
    min_stock: float
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
