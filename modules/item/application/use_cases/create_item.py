from modules.item.domain.entities.item import Item
from modules.item.domain.value_objects.item_id import ItemId
from modules.item.domain.value_objects.sku import Sku
from modules.item.domain.value_objects.ncm import Ncm
from modules.item.domain.value_objects.cest import Cest
from modules.item.domain.value_objects.ean import Ean
from modules.item.domain.value_objects.gtin import Gtin
from modules.item.domain.events.item_events import ItemCreated
from modules.item.domain.repositories.item_repository import ItemRepository
from modules.item.application.commands.item_commands import CreateItem


class CreateItemUseCase:
    def __init__(self, repository: ItemRepository):
        self.repository = repository
        self.events: list = []

    def execute(self, cmd: CreateItem) -> Item:
        item_id = ItemId.generate()

        item = Item(
            id=item_id,
            name=cmd.name,
            item_type=cmd.item_type,
            sku=Sku(cmd.sku) if cmd.sku else None,
            ncm=Ncm(cmd.ncm) if cmd.ncm else None,
            cest=Cest(cmd.cest) if cmd.cest else None,
            ean=Ean(cmd.ean) if cmd.ean else None,
            gtin=Gtin(cmd.gtin) if cmd.gtin else None,
            unit=cmd.unit,
            cost_price=cmd.cost_price,
            sale_price=cmd.sale_price,
            category_id=cmd.category_id,
            supplier_id=cmd.supplier_id or None,
            brand=cmd.brand,
            notes=cmd.notes,
            stock=cmd.stock,
            min_stock=cmd.min_stock,
        )

        self.repository.save(item)
        self.events.append(ItemCreated(
            item_id=item_id,
            name=cmd.name,
            item_type=cmd.item_type,
        ))
        return item
