from datetime import datetime, date
from modules.inventory.domain.entities.stock_movement import StockMovement
from modules.inventory.domain.value_objects.movement_type import MovementStatus
from modules.inventory.domain.entities.location import Location
from modules.inventory.domain.entities.lot import Lot, LotStatus
from modules.inventory.domain.entities.serial_number import SerialNumber, SerialStatus
from modules.inventory.domain.entities.reservation import Reservation, ReservationStatus
from modules.inventory.domain.entities.transfer_order import TransferOrder
from modules.inventory.domain.entities.inventory_count import InventoryCount
from modules.inventory.domain.repositories.inventory_repository import InventoryRepository


class InMemoryInventoryRepository(InventoryRepository):
    def __init__(self):
        self._movements: list[StockMovement] = []
        self._locations: dict[str, Location] = {}
        self._lots: dict[str, Lot] = {}
        self._serials: dict[str, SerialNumber] = {}
        self._reservations: list[Reservation] = []
        self._transfers: dict[str, TransferOrder] = {}
        self._counts: list[InventoryCount] = []
        self._ids = 0

    def _next_id(self) -> str:
        self._ids += 1
        return str(self._ids)

    # ── Stock Ledger ─────────────────────────────────────────
    def save_movement(self, movement: StockMovement) -> StockMovement:
        if not movement._id:
            movement._id = self._next_id()
        self._movements.append(movement)
        return movement

    def find_movement_by_id(self, mov_id: str) -> StockMovement | None:
        for m in self._movements:
            if m._id == mov_id:
                return m
        return None

    def find_movements(self, item_id: str = '', warehouse_id: str = '',
                       movement_type: str = '', reference_type: str = '',
                       limit: int = 100) -> list[StockMovement]:
        result = [m for m in self._movements
                  if (not item_id or m.item_id == item_id)
                  and (not warehouse_id or m.warehouse_id == warehouse_id)
                  and (not movement_type or m.movement_type.value == movement_type)
                  and (not reference_type or m.reference_type == reference_type)]
        result.sort(key=lambda m: m.created_at or datetime.min, reverse=True)
        return result[:limit]

    def compute_balance(self, item_id: str, warehouse_id: str = '',
                        location_id: str = '', lot_id: str = '') -> float:
        balance = 0.0
        for m in self._movements:
            if m.item_id != item_id:
                continue
            if warehouse_id and m.warehouse_id != warehouse_id:
                continue
            if location_id and m.location_id != location_id:
                continue
            if lot_id and m.lot_id != lot_id:
                continue
            if m.status != MovementStatus.CONFIRMED:
                continue
            balance += m.net_effect
        return balance

    def compute_available(self, item_id: str, warehouse_id: str = '') -> float:
        physical = self.compute_balance(item_id, warehouse_id)
        reserved = sum(r.quantity for r in self._reservations
                       if r.item_id == item_id
                       and (not warehouse_id or r.warehouse_id == warehouse_id)
                       and r.status == ReservationStatus.ACTIVE)
        return physical - reserved

    # ── Locations ────────────────────────────────────────────
    def save_location(self, loc: Location) -> Location:
        key = f'{loc.warehouse_id}:{loc.code}'
        if not loc._id:
            loc._id = key
        self._locations[key] = loc
        return loc

    def find_locations_by_warehouse(self, warehouse_id: str) -> list[Location]:
        return [l for l in self._locations.values() if l.warehouse_id == warehouse_id]

    def find_location_by_code(self, warehouse_id: str, code: str) -> Location | None:
        return self._locations.get(f'{warehouse_id}:{code}')

    # ── Lots ─────────────────────────────────────────────────
    def save_lot(self, lot: Lot) -> Lot:
        if not lot._id:
            lot._id = self._next_id()
        self._lots[lot._id] = lot
        return lot

    def find_lot_by_id(self, lot_id: str) -> Lot | None:
        return self._lots.get(lot_id)

    def find_lots_by_item(self, item_id: str, warehouse_id: str = '') -> list[Lot]:
        return [l for l in self._lots.values()
                if l.item_id == item_id
                and (not warehouse_id or l.warehouse_id == warehouse_id)
                and l.status == LotStatus.ACTIVE]

    def find_expiring_lots(self, days: int) -> list[Lot]:
        today = date.today()
        return [l for l in self._lots.values()
                if l.status == LotStatus.ACTIVE and l.expiry_date
                and 0 <= (l.expiry_date - today).days <= days]

    def find_expired_lots(self) -> list[Lot]:
        today = date.today()
        return [l for l in self._lots.values()
                if l.expiry_date and l.expiry_date < today]

    # ── Serials ──────────────────────────────────────────────
    def save_serial(self, serial: SerialNumber) -> SerialNumber:
        if not serial._id:
            serial._id = serial.serial
        self._serials[serial.serial] = serial
        return serial

    def find_serial(self, serial: str) -> SerialNumber | None:
        return self._serials.get(serial)

    def find_serials(self, item_id: str = '', warehouse_id: str = '',
                     status: str = '') -> list[SerialNumber]:
        return [s for s in self._serials.values()
                if (not item_id or s.item_id == item_id)
                and (not warehouse_id or s.warehouse_id == warehouse_id)
                and (not status or s.status.value == status)]

    # ── Reservations ─────────────────────────────────────────
    def save_reservation(self, reservation: Reservation) -> Reservation:
        if not reservation._id:
            reservation._id = self._next_id()
        self._reservations.append(reservation)
        return reservation

    def find_reservations(self, item_id: str = '', warehouse_id: str = '',
                          status: str = '', order_type: str = '',
                          order_id: str = '') -> list[Reservation]:
        return [r for r in self._reservations
                if (not item_id or r.item_id == item_id)
                and (not warehouse_id or r.warehouse_id == warehouse_id)
                and (not status or r.status.value == status)
                and (not order_type or r.order_type == order_type)
                and (not order_id or r.order_id == order_id)]

    def find_expired_reservations(self) -> list[Reservation]:
        now = datetime.now()
        return [r for r in self._reservations
                if r.status == ReservationStatus.ACTIVE
                and r.expires_at and r.expires_at < now]

    # ── Transfers ────────────────────────────────────────────
    def save_transfer(self, transfer: TransferOrder) -> TransferOrder:
        if not transfer._id:
            transfer._id = self._next_id()
        self._transfers[transfer._id] = transfer
        return transfer

    def find_transfer_by_id(self, transfer_id: str) -> TransferOrder | None:
        return self._transfers.get(transfer_id)

    def find_transfers(self, warehouse_id: str = '', status: str = '') -> list[TransferOrder]:
        return [t for t in self._transfers.values()
                if (not warehouse_id or t.from_warehouse_id == warehouse_id or t.to_warehouse_id == warehouse_id)
                and (not status or t.status.value == status)]

    # ── Counts ───────────────────────────────────────────────
    def save_count(self, count: InventoryCount) -> InventoryCount:
        if not count._id:
            count._id = self._next_id()
        self._counts.append(count)
        return count

    def find_counts_by_warehouse(self, warehouse_id: str) -> list[InventoryCount]:
        return [c for c in self._counts if not warehouse_id or c.warehouse_id == warehouse_id]


from modules.inventory.domain.value_objects.movement_type import MovementStatus
