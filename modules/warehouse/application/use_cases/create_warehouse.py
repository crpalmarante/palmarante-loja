from modules.warehouse.application.commands.warehouse_commands import CreateWarehouse
from modules.warehouse.domain.entities.warehouse import Warehouse
from modules.warehouse.domain.repositories.warehouse_repository import WarehouseRepository


class CreateWarehouseUseCase:
    def __init__(self, repo: WarehouseRepository):
        self._repo = repo

    def execute(self, cmd: CreateWarehouse) -> Warehouse:
        wh = Warehouse(name=cmd.name, code=cmd.code, description=cmd.description,
                       address=cmd.address, responsible=cmd.responsible)
        return self._repo.save_warehouse(wh)
