from modules.warehouse.domain.entities.warehouse import Warehouse
from modules.warehouse.domain.entities.stock_item import StockItem
from modules.warehouse.domain.entities.stock_movement import StockMovement
from modules.warehouse.domain.entities.inventory_count import InventoryCount
from modules.warehouse.domain.repositories.warehouse_repository import WarehouseRepository


class InMemoryWarehouseRepository(WarehouseRepository):
    def __init__(self):
        self._warehouses: dict[str, Warehouse] = {}
        self._stock: dict[str, StockItem] = {}
        self._movements: list[StockMovement] = []
        self._counts: list[InventoryCount] = []
        self._ids = 0

    def _next_id(self) -> str:
        self._ids += 1
        return str(self._ids)

    def _stock_key(self, wh_id: str, item_id: str) -> str:
        return f'{wh_id}:{item_id}'

    # Warehouses
    def save_warehouse(self, wh: Warehouse) -> Warehouse:
        if not wh._id:
            wh._id = self._next_id()
        self._warehouses[wh._id] = wh
        return wh

    def find_all_warehouses(self, query: str = '', active: bool | None = None) -> list[Warehouse]:
        ql = query.lower() if query else ''
        return [w for w in self._warehouses.values()
                if (not ql or ql in w.name.lower() or ql in w.code.lower())
                and (active is None or w.active == active)]

    def find_warehouse_by_id(self, wh_id: str) -> Warehouse | None:
        return self._warehouses.get(wh_id)

    # Stock
    def save_stock_item(self, stock: StockItem) -> StockItem:
        key = self._stock_key(stock.warehouse_id, stock.item_id)
        if not stock._id:
            stock._id = key
        self._stock[key] = stock
        return stock

    def find_stock_item(self, warehouse_id: str, item_id: str) -> StockItem | None:
        return self._stock.get(self._stock_key(warehouse_id, item_id))

    def find_stock_by_warehouse(self, warehouse_id: str) -> list[StockItem]:
        return [s for s in self._stock.values() if s.warehouse_id == warehouse_id]

    def find_stock_by_item(self, item_id: str) -> list[StockItem]:
        return [s for s in self._stock.values() if s.item_id == item_id]

    def find_low_stock(self) -> list[StockItem]:
        return [s for s in self._stock.values() if s.min_stock > 0 and s.quantity <= s.min_stock]

    # Movements
    def save_movement(self, mov: StockMovement) -> StockMovement:
        if not mov._id:
            mov._id = self._next_id()
        self._movements.append(mov)
        return mov

    def find_movements_by_item(self, item_id: str) -> list[StockMovement]:
        return [m for m in self._movements if m.item_id == item_id]

    def find_movements_by_warehouse(self, warehouse_id: str) -> list[StockMovement]:
        return [m for m in self._movements if m.warehouse_id == warehouse_id]

    # Inventory counts
    def save_inventory_count(self, count: InventoryCount) -> InventoryCount:
        if not count._id:
            count._id = self._next_id()
        self._counts.append(count)
        return count

    def find_counts_by_warehouse(self, warehouse_id: str) -> list[InventoryCount]:
        return [c for c in self._counts if c.warehouse_id == warehouse_id]
