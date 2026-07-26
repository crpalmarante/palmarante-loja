from datetime import datetime
from modules.item.domain.entities.item import Item
from modules.item.domain.value_objects.sku import Sku
from modules.item.domain.value_objects.ncm import Ncm
from modules.item.domain.value_objects.ean import Ean
from modules.item.domain.events.item_events import ItemUpdated
from modules.item.domain.repositories.item_repository import ItemRepository
from modules.item.application.commands.item_commands import UpdateItem


class UpdateItemUseCase:
    def __init__(self, repository: ItemRepository):
        self.repository = repository
        self.events: list = []

    def execute(self, cmd: UpdateItem) -> Item:
        item = self.repository.find_by_id(cmd.item_id)
        if not item:
            raise ValueError(f'Item not found: {cmd.item_id}')

        if cmd.name is not None:
            item.name = cmd.name
        if cmd.sku is not None:
            item.sku = Sku(cmd.sku)
        if cmd.ncm is not None:
            item.ncm = Ncm(cmd.ncm) if cmd.ncm else None
        if cmd.ean is not None:
            item.ean = Ean(cmd.ean) if cmd.ean else None
        if cmd.unit is not None:
            item.unit = cmd.unit
        if cmd.cost_price is not None:
            item.cost_price = cmd.cost_price
        if cmd.sale_price is not None:
            item.sale_price = cmd.sale_price
        if cmd.category is not None:
            item.category = cmd.category
        if cmd.supplier_id is not None:
            item.supplier_id = cmd.supplier_id or None
        if cmd.notes is not None:
            item.notes = cmd.notes
        if cmd.min_stock is not None:
            item.min_stock = cmd.min_stock

        item.updated_at = datetime.now()
        self.repository.save(item)
        self.events.append(ItemUpdated(item_id=cmd.item_id))
        return item
