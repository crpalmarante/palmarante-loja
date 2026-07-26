from modules.item.domain.events.item_events import ItemUpdated
from modules.item.domain.repositories.item_repository import ItemRepository
from modules.item.application.commands.item_commands import ChangePrice


class ChangePriceUseCase:
    def __init__(self, repository: ItemRepository):
        self.repository = repository
        self.events: list = []

    def execute(self, cmd: ChangePrice) -> None:
        item = self.repository.find_by_id(cmd.item_id)
        if not item:
            raise ValueError(f'Item not found: {cmd.item_id}')
        item.update_price(cost=cmd.cost_price, sale=cmd.sale_price, reason=cmd.reason)
        self.repository.save(item)
        self.events.append(ItemUpdated(item_id=cmd.item_id))
