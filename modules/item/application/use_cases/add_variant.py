from modules.item.domain.entities.variant import ItemVariant
from modules.item.domain.repositories.item_repository import ItemRepository
from modules.item.application.commands.item_commands import AddVariant


class AddVariantUseCase:
    def __init__(self, repository: ItemRepository):
        self.repository = repository

    def execute(self, cmd: AddVariant) -> ItemVariant:
        item = self.repository.find_by_id(cmd.item_id)
        if not item:
            raise ValueError(f'Item not found: {cmd.item_id}')
        variant = ItemVariant(
            name=cmd.name,
            sku=cmd.sku,
            sale_price=cmd.sale_price,
            cost_price=cmd.cost_price,
            stock=cmd.stock,
        )
        item.add_variant(variant)
        self.repository.save(item)
        return variant
