from dataclasses import dataclass
from modules.warehouse.domain.entities.stock_movement import MovementType


@dataclass
class CreateWarehouse:
    name: str
    code: str
    description: str = ''
    address: str = ''
    responsible: str = ''


@dataclass
class AdjustStock:
    warehouse_id: str
    item_id: str
    quantity: float
    notes: str = ''


@dataclass
class RecordMovement:
    item_id: str
    warehouse_id: str
    movement_type: MovementType
    quantity: float
    reference_type: str = ''
    reference_id: str = ''
    notes: str = ''
    target_warehouse_id: str = ''


@dataclass
class CreateInventoryCount:
    warehouse_id: str
    item_id: str
    expected_quantity: float
    actual_quantity: float
    counted_by: str = ''
    notes: str = ''
