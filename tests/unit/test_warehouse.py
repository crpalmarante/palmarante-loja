import pytest
from modules.warehouse.domain.entities.warehouse import Warehouse
from modules.warehouse.domain.entities.stock_item import StockItem
from modules.warehouse.domain.entities.stock_movement import StockMovement, MovementType, MovementStatus
from modules.warehouse.domain.entities.inventory_count import InventoryCount
from modules.warehouse.infrastructure.postgres.memory_repository import InMemoryWarehouseRepository
from modules.warehouse.application.use_cases.create_warehouse import CreateWarehouseUseCase
from modules.warehouse.application.use_cases.adjust_stock import AdjustStockUseCase
from modules.warehouse.application.use_cases.record_movement import RecordMovementUseCase
from modules.warehouse.application.commands.warehouse_commands import CreateWarehouse, AdjustStock, RecordMovement


class TestWarehouse:
    def test_create(self):
        w = Warehouse(name='Armazém Central', code='AC', address='Rua A, 123')
        assert w.name == 'Armazém Central' and w.code == 'AC'

    def test_create_with_empty(self):
        w = Warehouse(name='Filial Sul', code='FS')
        assert w.active is True


class TestStockItem:
    def test_create(self):
        s = StockItem(warehouse_id='w1', item_id='i1', quantity=100, reserved=10, min_stock=20)
        assert s.available == 90

    def test_low_stock(self):
        s = StockItem(warehouse_id='w1', item_id='i1', quantity=15, min_stock=20)
        assert s.quantity <= s.min_stock


class TestStockMovement:
    def test_create_in(self):
        m = StockMovement(item_id='i1', warehouse_id='w1', movement_type=MovementType.IN, quantity=50)
        assert m.status == MovementStatus.PENDING
        assert m.created_at is not None

    def test_confirm(self):
        m = StockMovement(item_id='i1', warehouse_id='w1', movement_type=MovementType.OUT, quantity=10)
        m.confirm()
        assert m.status == MovementStatus.CONFIRMED
        assert m.confirmed_at is not None

    def test_cancel(self):
        m = StockMovement(item_id='i1', warehouse_id='w1', movement_type=MovementType.IN, quantity=5)
        m.cancel()
        assert m.status == MovementStatus.CANCELLED


class TestInventoryCount:
    def test_difference(self):
        c = InventoryCount(warehouse_id='w1', item_id='i1', expected_quantity=100, actual_quantity=95)
        assert c.difference == -5

    def test_exact_match(self):
        c = InventoryCount(warehouse_id='w1', item_id='i1', expected_quantity=50, actual_quantity=50)
        assert c.difference == 0


class TestWarehouseUseCases:
    @pytest.fixture
    def repo(self):
        return InMemoryWarehouseRepository()

    def test_create_warehouse(self, repo):
        uc = CreateWarehouseUseCase(repo)
        wh = uc.execute(CreateWarehouse(name='Matriz', code='MT'))
        assert wh._id
        assert repo.find_warehouse_by_id(wh._id).name == 'Matriz'

    def test_adjust_stock(self, repo):
        uc = AdjustStockUseCase(repo)
        stock = uc.execute(AdjustStock(warehouse_id='w1', item_id='i1', quantity=100))
        assert stock.quantity == 100
        stock2 = uc.execute(AdjustStock(warehouse_id='w1', item_id='i1', quantity=-30))
        assert stock2.quantity == 70

    def test_record_in_movement_updates_stock(self, repo):
        uc = RecordMovementUseCase(repo)
        cmd = RecordMovement(item_id='i1', warehouse_id='w1', movement_type=MovementType.IN, quantity=50)
        uc.execute(cmd)
        stock = repo.find_stock_item('w1', 'i1')
        assert stock.quantity == 50

    def test_record_out_movement(self, repo):
        uc = RecordMovementUseCase(repo)
        uc.execute(RecordMovement(item_id='i1', warehouse_id='w1', movement_type=MovementType.IN, quantity=100))
        uc.execute(RecordMovement(item_id='i1', warehouse_id='w1', movement_type=MovementType.OUT, quantity=30))
        stock = repo.find_stock_item('w1', 'i1')
        assert stock.quantity == 70


class TestWarehouseRepository:
    @pytest.fixture
    def repo(self):
        return InMemoryWarehouseRepository()

    def test_crud(self, repo):
        w = Warehouse(name='Teste', code='TST')
        repo.save_warehouse(w)
        assert len(repo.find_all_warehouses()) == 1
        assert repo.find_all_warehouses(query='teste')
        assert repo.find_warehouse_by_id(w._id).name == 'Teste'

    def test_low_stock_search(self, repo):
        repo.save_stock_item(StockItem(warehouse_id='w1', item_id='i1', quantity=5, min_stock=10))
        repo.save_stock_item(StockItem(warehouse_id='w1', item_id='i2', quantity=50, min_stock=10))
        assert len(repo.find_low_stock()) == 1

    def test_movements(self, repo):
        m1 = StockMovement(item_id='i1', warehouse_id='w1', movement_type=MovementType.IN, quantity=10)
        m2 = StockMovement(item_id='i2', warehouse_id='w1', movement_type=MovementType.OUT, quantity=5)
        repo.save_movement(m1)
        repo.save_movement(m2)
        assert len(repo.find_movements_by_item('i1')) == 1
        assert len(repo.find_movements_by_warehouse('w1')) == 2

    def test_inventory_counts(self, repo):
        c = InventoryCount(warehouse_id='w1', item_id='i1', expected_quantity=100, actual_quantity=98)
        repo.save_inventory_count(c)
        assert len(repo.find_counts_by_warehouse('w1')) == 1

    def test_stock_by_item(self, repo):
        repo.save_stock_item(StockItem(warehouse_id='w1', item_id='i1', quantity=10))
        repo.save_stock_item(StockItem(warehouse_id='w2', item_id='i1', quantity=20))
        items = repo.find_stock_by_item('i1')
        assert len(items) == 2
        assert sum(s.quantity for s in items) == 30
