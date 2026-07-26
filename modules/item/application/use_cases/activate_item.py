from modules.item.domain.events.item_events import ItemActivated, ItemInactivated, ItemArchived
from modules.item.domain.repositories.item_repository import ItemRepository
from modules.item.application.commands.item_commands import ActivateItem, DeactivateItem, ArchiveItem


class ActivateItemUseCase:
    def __init__(self, repository: ItemRepository):
        self.repository = repository
        self.events: list = []

    def activate(self, cmd: ActivateItem) -> None:
        item = self.repository.find_by_id(cmd.item_id)
        if not item:
            raise ValueError(f'Item not found: {cmd.item_id}')
        item.activate()
        self.repository.save(item)
        self.events.append(ItemActivated(item_id=cmd.item_id))

    def deactivate(self, cmd: DeactivateItem) -> None:
        item = self.repository.find_by_id(cmd.item_id)
        if not item:
            raise ValueError(f'Item not found: {cmd.item_id}')
        item.deactivate()
        self.repository.save(item)
        self.events.append(ItemInactivated(item_id=cmd.item_id))

    def archive(self, cmd: ArchiveItem) -> None:
        item = self.repository.find_by_id(cmd.item_id)
        if not item:
            raise ValueError(f'Item not found: {cmd.item_id}')
        item.archive()
        self.repository.save(item)
        self.events.append(ItemArchived(item_id=cmd.item_id))
