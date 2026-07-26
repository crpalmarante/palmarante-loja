from modules.warehouse.application.commands.warehouse_commands import AdjustStock, RecordMovement
from modules.warehouse.domain.entities.stock_item import StockItem
from modules.warehouse.domain.entities.stock_movement import StockMovement, MovementType, MovementStatus
from modules.warehouse.domain.repositories.warehouse_repository import WarehouseRepository


class AdjustStockUseCase:
    def __init__(self, repo: WarehouseRepository):
        self._repo = repo

    def execute(self, cmd: AdjustStock) -> StockItem:
        stock = self._repo.find_stock_item(cmd.warehouse_id, cmd.item_id)
        if stock:
            stock.quantity += cmd.quantity
        else:
            stock = StockItem(warehouse_id=cmd.warehouse_id, item_id=cmd.item_id, quantity=cmd.quantity)
        self._repo.save_stock_item(stock)

        movement = StockMovement(
            item_id=cmd.item_id,
            warehouse_id=cmd.warehouse_id,
            movement_type=MovementType.ADJUSTMENT if cmd.quantity >= 0 else MovementType.OUT,
            quantity=abs(cmd.quantity),
            notes=cmd.notes,
            status=MovementStatus.CONFIRMED,
        )
        movement.confirm()
        self._repo.save_movement(movement)

        return stock
