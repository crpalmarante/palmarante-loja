from modules.inventory.application.commands.inventory_commands import RecordMovement
from modules.inventory.domain.entities.stock_movement import StockMovement
from modules.inventory.domain.value_objects.movement_type import MovementType, MovementStatus
from modules.inventory.domain.repositories.inventory_repository import InventoryRepository


class RecordMovementUseCase:
    def __init__(self, repo: InventoryRepository):
        self._repo = repo

    def execute(self, cmd: RecordMovement) -> StockMovement:
        movement = StockMovement(
            item_id=cmd.item_id,
            warehouse_id=cmd.warehouse_id,
            movement_type=MovementType(cmd.movement_type),
            quantity=cmd.quantity,
            location_id=cmd.location_id,
            lot_id=cmd.lot_id,
            serial_number=cmd.serial_number,
            reference_type=cmd.reference_type,
            reference_id=cmd.reference_id,
            document_number=cmd.document_number,
            unit_cost=cmd.unit_cost,
            notes=cmd.notes,
            created_by=cmd.created_by,
        )
        if cmd.auto_confirm:
            movement.confirm()
        return self._repo.save_movement(movement)
