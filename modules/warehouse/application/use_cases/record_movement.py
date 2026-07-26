from modules.warehouse.application.commands.warehouse_commands import RecordMovement
from modules.warehouse.domain.entities.stock_movement import StockMovement, MovementStatus, MovementType
from modules.warehouse.domain.repositories.warehouse_repository import WarehouseRepository


class RecordMovementUseCase:
    def __init__(self, repo: WarehouseRepository):
        self._repo = repo

    def execute(self, cmd: RecordMovement) -> StockMovement:
        movement = StockMovement(
            item_id=cmd.item_id,
            warehouse_id=cmd.warehouse_id,
            movement_type=cmd.movement_type,
            quantity=cmd.quantity,
            reference_type=cmd.reference_type,
            reference_id=cmd.reference_id,
            notes=cmd.notes,
            target_warehouse_id=cmd.target_warehouse_id,
        )

        if cmd.movement_type in (MovementType.IN, MovementType.OUT, MovementType.ADJUSTMENT):
            movement.confirm()
            stock = self._repo.find_stock_item(cmd.warehouse_id, cmd.item_id)
            if not stock:
                from modules.warehouse.domain.entities.stock_item import StockItem
                stock = StockItem(warehouse_id=cmd.warehouse_id, item_id=cmd.item_id)
            if cmd.movement_type == MovementType.IN:
                stock.quantity += cmd.quantity
            elif cmd.movement_type == MovementType.OUT:
                stock.quantity -= cmd.quantity
            stock.quantity = max(0, stock.quantity)
            self._repo.save_stock_item(stock)

        self._repo.save_movement(movement)
        return movement
