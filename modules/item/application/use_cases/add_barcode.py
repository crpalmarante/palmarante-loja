from modules.item.domain.entities.barcode import ItemBarcode
from modules.item.domain.repositories.item_repository import ItemRepository
from modules.item.application.commands.item_commands import AddBarcode


class AddBarcodeUseCase:
    def __init__(self, repository: ItemRepository):
        self.repository = repository

    def execute(self, cmd: AddBarcode) -> ItemBarcode:
        item = self.repository.find_by_id(cmd.item_id)
        if not item:
            raise ValueError(f'Item not found: {cmd.item_id}')
        barcode = ItemBarcode(
            code=cmd.code,
            barcode_type=cmd.barcode_type,
            is_main=cmd.is_main,
        )
        item.add_barcode(barcode)
        self.repository.save(item)
        return barcode
