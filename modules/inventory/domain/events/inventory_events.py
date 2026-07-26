from dataclasses import dataclass
from datetime import datetime


@dataclass
class StockReceived:
    movement_id: str
    item_id: str
    warehouse_id: str
    quantity: float
    location_id: str
    lot_id: str
    document_number: str
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class StockReserved:
    reservation_id: str
    item_id: str
    warehouse_id: str
    quantity: float
    order_type: str
    order_id: str
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class StockReleased:
    reservation_id: str
    item_id: str
    warehouse_id: str
    quantity: float
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class StockTransferred:
    transfer_id: str
    from_warehouse: str
    to_warehouse: str
    item_id: str
    quantity: float
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class StockAdjusted:
    movement_id: str
    item_id: str
    warehouse_id: str
    old_quantity: float
    new_quantity: float
    reason: str
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class StockConsumed:
    movement_id: str
    item_id: str
    warehouse_id: str
    quantity: float
    reference_type: str
    reference_id: str
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class StockReturned:
    movement_id: str
    item_id: str
    warehouse_id: str
    quantity: float
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class InventoryCountCompleted:
    count_id: str
    warehouse_id: str
    total_lines: int
    total_difference: float
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


@dataclass
class ExpiryAlert:
    lot_id: str
    item_id: str
    lot_number: str
    days_to_expiry: int
    quantity: float
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
