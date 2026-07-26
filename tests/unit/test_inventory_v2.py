import pytest
from datetime import date, datetime, timedelta
from modules.inventory.domain.entities.stock_movement import StockMovement
from modules.inventory.domain.entities.location import Location
from modules.inventory.domain.entities.lot import Lot, LotStatus
from modules.inventory.domain.entities.serial_number import SerialNumber, SerialStatus
from modules.inventory.domain.entities.reservation import Reservation, ReservationStatus
from modules.inventory.domain.entities.transfer_order import TransferOrder, TransferItem, TransferStatus
from modules.inventory.domain.entities.inventory_count import InventoryCount, CountLine, CountStatus
from modules.inventory.domain.value_objects.movement_type import MovementType, MovementStatus
from modules.inventory.infrastructure.postgres.memory_repository import InMemoryInventoryRepository
from modules.inventory.application.use_cases.record_movement import RecordMovementUseCase
from modules.inventory.application.use_cases.manage_lot import CreateLotUseCase
from modules.inventory.application.commands.inventory_commands import (
    RecordMovement, CreateLot, RegisterSerial,
)
from modules.inventory.application.services.availability_engine import AvailabilityEngine


# ══════════════════════════════════════════════════════════════
# Stock Ledger — a verdade do sistema
# ══════════════════════════════════════════════════════════════
class TestStockLedger:
    @pytest.fixture
    def repo(self):
        return InMemoryInventoryRepository()

    def test_movement_types(self):
        assert MovementType.IN.value == 'in'
        assert MovementType.OUT.value == 'out'
        assert MovementType.RESERVE.value == 'reserve'
        assert MovementType.RELEASE.value == 'release'
        assert MovementType.ADJUSTMENT.value == 'adjustment'
        assert MovementType.PRODUCTION.value == 'production'
        assert MovementType.CONSUMPTION.value == 'consumption'
        assert MovementType.RETURN.value == 'return'
        assert MovementType.TRANSFER.value == 'transfer'

    def test_net_effect_in(self):
        m = StockMovement(item_id='i1', warehouse_id='w1', movement_type=MovementType.IN, quantity=100)
        m.confirm()
        assert m.net_effect == 100

    def test_net_effect_out(self):
        m = StockMovement(item_id='i1', warehouse_id='w1', movement_type=MovementType.OUT, quantity=30)
        m.confirm()
        assert m.net_effect == -30

    def test_net_effect_reserve(self):
        m = StockMovement(item_id='i1', warehouse_id='w1', movement_type=MovementType.RESERVE, quantity=10)
        assert m.net_effect == 0  # reserve não afeta saldo físico

    def test_balance_from_ledger(self, repo):
        repo.save_movement(StockMovement(item_id='i1', warehouse_id='w1', movement_type=MovementType.IN, quantity=100, status=MovementStatus.CONFIRMED))
        repo.save_movement(StockMovement(item_id='i1', warehouse_id='w1', movement_type=MovementType.OUT, quantity=30, status=MovementStatus.CONFIRMED))
        repo.save_movement(StockMovement(item_id='i1', warehouse_id='w1', movement_type=MovementType.IN, quantity=10, status=MovementStatus.CONFIRMED))
        assert repo.compute_balance('i1', 'w1') == 80

    def test_pending_movements_not_counted(self, repo):
        repo.save_movement(StockMovement(item_id='i1', warehouse_id='w1', movement_type=MovementType.IN, quantity=100, status=MovementStatus.PENDING))
        assert repo.compute_balance('i1', 'w1') == 0

    def test_available_from_balance_minus_reservations(self, repo):
        repo.save_movement(StockMovement(item_id='i1', warehouse_id='w1', movement_type=MovementType.IN, quantity=100, status=MovementStatus.CONFIRMED))
        repo.save_reservation(Reservation(item_id='i1', warehouse_id='w1', quantity=30))
        assert repo.compute_available('i1', 'w1') == 70


class TestStockMovement:
    def test_create(self):
        m = StockMovement(item_id='i1', warehouse_id='w1', movement_type=MovementType.IN, quantity=50)
        assert m.status == MovementStatus.PENDING
        assert m.created_at is not None

    def test_confirm(self):
        m = StockMovement(item_id='i1', warehouse_id='w1', movement_type=MovementType.IN, quantity=10)
        m.confirm()
        assert m.status == MovementStatus.CONFIRMED
        assert m.confirmed_at is not None

    def test_cancel(self):
        m = StockMovement(item_id='i1', warehouse_id='w1', movement_type=MovementType.IN, quantity=10)
        m.cancel()
        assert m.status == MovementStatus.CANCELLED


class TestLocation:
    def test_create_rack(self):
        l = Location(warehouse_id='w1', code='A/01/03/02', name='Prateleira A01', type='shelf')
        assert l.level == 4
        assert l.path_parts == ['A', '01', '03', '02']

    def test_path(self):
        l = Location(warehouse_id='w1', code='CD/PRATELEIRA/NIVEL')
        assert l.level == 3


class TestLot:
    def test_create(self):
        l = Lot(item_id='i1', warehouse_id='w1', lot_number='LOT-001')
        assert l.status == LotStatus.ACTIVE

    def test_expired(self):
        l = Lot(item_id='i1', warehouse_id='w1', lot_number='LOT-EXP', expiry_date=date(2020, 1, 1))
        assert l.is_expired is True

    def test_not_expired(self):
        l = Lot(item_id='i1', warehouse_id='w1', lot_number='LOT-OK', expiry_date=date(2099, 12, 31))
        assert l.is_expired is False

    def test_block(self):
        l = Lot(item_id='i1', warehouse_id='w1', lot_number='LOT-BLK')
        l.block()
        assert l.status == LotStatus.BLOCKED


class TestSerialNumber:
    def test_flow(self):
        s = SerialNumber(item_id='i1', warehouse_id='w1', serial='SN001')
        assert s.status == SerialStatus.AVAILABLE
        s.reserve()
        assert s.status == SerialStatus.RESERVED
        s.sell()
        assert s.status == SerialStatus.SOLD
        s.mark_returned()
        assert s.status == SerialStatus.RETURNED

    def test_reserve_twice_fails(self):
        s = SerialNumber(item_id='i1', warehouse_id='w1', serial='SN002')
        s.reserve()
        with pytest.raises(ValueError):
            s.reserve()


class TestReservation:
    def test_expired(self):
        r = Reservation(item_id='i1', warehouse_id='w1', quantity=10,
                        expires_at=datetime.now() - timedelta(hours=1))
        assert r.is_expired is True

    def test_consume(self):
        r = Reservation(item_id='i1', warehouse_id='w1', quantity=10)
        r.consume()
        assert r.status == ReservationStatus.CONSUMED


class TestTransferOrder:
    def test_flow(self):
        t = TransferOrder(from_warehouse_id='w1', to_warehouse_id='w2')
        t.add_item(TransferItem(item_id='i1', quantity=10))
        assert t.status == TransferStatus.DRAFT
        t.send()
        assert t.status == TransferStatus.SENT
        t.mark_in_transit()
        assert t.status == TransferStatus.IN_TRANSIT
        t.receive()
        assert t.status == TransferStatus.RECEIVED
        t.complete()
        assert t.status == TransferStatus.COMPLETED


class TestInventoryCount:
    def test_lines(self):
        c = InventoryCount(warehouse_id='w1')
        c.add_line(CountLine(item_id='i1', expected_quantity=100, actual_quantity=97))
        c.add_line(CountLine(item_id='i2', expected_quantity=50, actual_quantity=50))
        assert c.line_count == 2
        assert c.total_difference == -3

    def test_complete(self):
        c = InventoryCount(warehouse_id='w1')
        c.add_line(CountLine(item_id='i1', expected_quantity=100, actual_quantity=95))
        c.complete()
        assert c.status == CountStatus.COMPLETED
        assert c.completed_at is not None


# ══════════════════════════════════════════════════════════════
# Use Cases
# ══════════════════════════════════════════════════════════════
class TestUseCases:
    @pytest.fixture
    def repo(self):
        return InMemoryInventoryRepository()

    def test_record_movement(self, repo):
        uc = RecordMovementUseCase(repo)
        m = uc.execute(RecordMovement(item_id='i1', warehouse_id='w1', movement_type='in', quantity=100))
        assert m.status == MovementStatus.CONFIRMED
        assert repo.compute_balance('i1', 'w1') == 100

    def test_record_multiple(self, repo):
        uc = RecordMovementUseCase(repo)
        uc.execute(RecordMovement(item_id='i1', warehouse_id='w1', movement_type='in', quantity=100))
        uc.execute(RecordMovement(item_id='i1', warehouse_id='w1', movement_type='out', quantity=30))
        uc.execute(RecordMovement(item_id='i1', warehouse_id='w1', movement_type='in', quantity=20))
        assert repo.compute_balance('i1', 'w1') == 90

    def test_create_lot(self, repo):
        uc = CreateLotUseCase(repo)
        l = uc.execute(CreateLot(item_id='i1', warehouse_id='w1', lot_number='LOT-001'))
        assert repo.find_lot_by_id(l._id).lot_number == 'LOT-001'


# ══════════════════════════════════════════════════════════════
# Availability Engine
# ══════════════════════════════════════════════════════════════
class TestAvailabilityEngine:
    @pytest.fixture
    def repo(self):
        return InMemoryInventoryRepository()

    @pytest.fixture
    def engine(self, repo):
        return AvailabilityEngine(repo)

    def test_balance(self, repo, engine):
        repo.save_movement(StockMovement(item_id='i1', warehouse_id='w1', movement_type=MovementType.IN, quantity=100, status=MovementStatus.CONFIRMED))
        repo.save_movement(StockMovement(item_id='i1', warehouse_id='w1', movement_type=MovementType.OUT, quantity=30, status=MovementStatus.CONFIRMED))
        bal = engine.get_balance('i1', 'w1')
        assert bal['physical'] == 70
        assert bal['reserved'] == 0
        assert bal['available'] == 70

    def test_available_with_reservations(self, repo, engine):
        repo.save_movement(StockMovement(item_id='i1', warehouse_id='w1', movement_type=MovementType.IN, quantity=100, status=MovementStatus.CONFIRMED))
        repo.save_reservation(Reservation(item_id='i1', warehouse_id='w1', quantity=30))
        repo.save_reservation(Reservation(item_id='i1', warehouse_id='w1', quantity=20))
        bal = engine.get_balance('i1', 'w1')
        assert bal['physical'] == 100
        assert bal['reserved'] == 50
        assert bal['available'] == 50

    def test_is_available(self, repo, engine):
        repo.save_movement(StockMovement(item_id='i1', warehouse_id='w1', movement_type=MovementType.IN, quantity=100, status=MovementStatus.CONFIRMED))
        assert engine.is_available('i1', 'w1', 80) is True
        assert engine.is_available('i1', 'w1', 120) is False

    def test_dashboard(self, repo, engine):
        repo.save_movement(StockMovement(item_id='i1', warehouse_id='w1', movement_type=MovementType.IN, quantity=100, status=MovementStatus.CONFIRMED))
        repo.save_movement(StockMovement(item_id='i1', warehouse_id='w1', movement_type=MovementType.OUT, quantity=30, status=MovementStatus.CONFIRMED))
        repo.save_movement(StockMovement(item_id='i2', warehouse_id='w1', movement_type=MovementType.IN, quantity=50, status=MovementStatus.CONFIRMED))
        d = engine.get_dashboard()
        assert d['total_items_in_stock'] == 2


# ══════════════════════════════════════════════════════════════
# Repository
# ══════════════════════════════════════════════════════════════
class TestInventoryRepository:
    @pytest.fixture
    def repo(self):
        return InMemoryInventoryRepository()

    def test_movements_filter(self, repo):
        for i in range(5):
            repo.save_movement(StockMovement(item_id='i1', warehouse_id='w1', movement_type=MovementType.IN, quantity=10, status=MovementStatus.CONFIRMED))
        repo.save_movement(StockMovement(item_id='i2', warehouse_id='w1', movement_type=MovementType.IN, quantity=10, status=MovementStatus.CONFIRMED))
        assert len(repo.find_movements(item_id='i1')) == 5
        assert len(repo.find_movements(item_id='i2')) == 1
        assert len(repo.find_movements()) == 6

    def test_locations(self, repo):
        l1 = Location(warehouse_id='w1', code='A/01', name='Rua A')
        l2 = Location(warehouse_id='w1', code='A/01/01', name='Prateleira 1')
        repo.save_location(l1)
        repo.save_location(l2)
        locs = repo.find_locations_by_warehouse('w1')
        assert len(locs) == 2
        assert repo.find_location_by_code('w1', 'A/01').name == 'Rua A'

    def test_lots(self, repo):
        repo.save_lot(Lot(item_id='i1', warehouse_id='w1', lot_number='LOT-A'))
        repo.save_lot(Lot(item_id='i1', warehouse_id='w1', lot_number='LOT-B'))
        repo.save_lot(Lot(item_id='i2', warehouse_id='w1', lot_number='LOT-C'))
        assert len(repo.find_lots_by_item('i1')) == 2

    def test_serials(self, repo):
        repo.save_serial(SerialNumber(item_id='i1', warehouse_id='w1', serial='SN001'))
        repo.save_serial(SerialNumber(item_id='i1', warehouse_id='w1', serial='SN002', status=SerialStatus.SOLD))
        assert len(repo.find_serials(status='sold')) == 1

    def test_expiring_lots(self, repo):
        repo.save_lot(Lot(item_id='i1', warehouse_id='w1', lot_number='LOT-A', expiry_date=date.today() + timedelta(3)))
        repo.save_lot(Lot(item_id='i1', warehouse_id='w1', lot_number='LOT-B', expiry_date=date.today() + timedelta(20)))
        assert len(repo.find_expiring_lots(5)) == 1

    def test_reservations_filter(self, repo):
        repo.save_reservation(Reservation(item_id='i1', warehouse_id='w1', quantity=10, order_type='sale'))
        repo.save_reservation(Reservation(item_id='i1', warehouse_id='w1', quantity=20, order_type='sale'))
        repo.save_reservation(Reservation(item_id='i2', warehouse_id='w1', quantity=5, order_type='purchase'))
        assert len(repo.find_reservations(item_id='i1')) == 2
        assert len(repo.find_reservations(order_type='sale')) == 2

    def test_expired_reservations(self, repo):
        repo.save_reservation(Reservation(item_id='i1', warehouse_id='w1', quantity=10,
                                          expires_at=datetime.now() - timedelta(days=1)))
        repo.save_reservation(Reservation(item_id='i1', warehouse_id='w1', quantity=10,
                                          expires_at=datetime.now() + timedelta(days=1)))
        assert len(repo.find_expired_reservations()) == 1

    def test_transfers(self, repo):
        t1 = TransferOrder(from_warehouse_id='w1', to_warehouse_id='w2', status=TransferStatus.DRAFT)
        t2 = TransferOrder(from_warehouse_id='w1', to_warehouse_id='w3', status=TransferStatus.COMPLETED)
        repo.save_transfer(t1)
        repo.save_transfer(t2)
        assert len(repo.find_transfers(status='draft')) == 1
        assert len(repo.find_transfers(warehouse_id='w1')) == 2

    def test_counts(self, repo):
        c = InventoryCount(warehouse_id='w1')
        c.add_line(CountLine(item_id='i1', expected_quantity=100, actual_quantity=98))
        repo.save_count(c)
        assert len(repo.find_counts_by_warehouse('w1')) == 1
