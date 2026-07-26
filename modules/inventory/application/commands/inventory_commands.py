from dataclasses import dataclass
from datetime import date


@dataclass
class RecordMovement:
    item_id: str
    warehouse_id: str
    movement_type: str
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
    auto_confirm: bool = True


@dataclass
class CreateLocation:
    warehouse_id: str
    code: str
    name: str = ''
    parent_id: str = ''
    type: str = 'rack'


@dataclass
class CreateLot:
    item_id: str
    warehouse_id: str
    lot_number: str
    supplier_lot: str = ''
    manufacturing_date: str = ''
    expiry_date: str = ''
    origin: str = ''
    notes: str = ''


@dataclass
class RegisterSerial:
    item_id: str
    warehouse_id: str
    serial: str
    lot_id: str = ''
    location_id: str = ''
    notes: str = ''


@dataclass
class CreateReservation:
    item_id: str
    warehouse_id: str
    quantity: float
    order_type: str = ''
    order_id: str = ''
    location_id: str = ''
    lot_id: str = ''
    expires_at: str = ''
    notes: str = ''
    created_by: str = ''


@dataclass
class CancelReservation:
    reservation_id: str


@dataclass
class CreateTransfer:
    from_warehouse_id: str
    to_warehouse_id: str
    items: list = None
    notes: str = ''
    created_by: str = ''


@dataclass
class CompleteTransfer:
    transfer_id: str


@dataclass
class CreateInventoryCount:
    warehouse_id: str
    lines: list = None
    counted_by: str = ''
    notes: str = ''


@dataclass
class CompleteInventoryCount:
    count_id: str
