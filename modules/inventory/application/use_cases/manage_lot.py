from datetime import date
from modules.inventory.application.commands.inventory_commands import CreateLot
from modules.inventory.domain.entities.lot import Lot
from modules.inventory.domain.repositories.inventory_repository import InventoryRepository


class CreateLotUseCase:
    def __init__(self, repo: InventoryRepository):
        self._repo = repo

    def execute(self, cmd: CreateLot) -> Lot:
        lot = Lot(
            item_id=cmd.item_id,
            warehouse_id=cmd.warehouse_id,
            lot_number=cmd.lot_number,
            supplier_lot=cmd.supplier_lot,
            manufacturing_date=date.fromisoformat(cmd.manufacturing_date) if cmd.manufacturing_date else None,
            expiry_date=date.fromisoformat(cmd.expiry_date) if cmd.expiry_date else None,
            origin=cmd.origin,
            notes=cmd.notes,
        )
        return self._repo.save_lot(lot)
