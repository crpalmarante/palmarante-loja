from abc import ABC, abstractmethod
from modules.item.domain.entities.item import Item
from modules.item.domain.value_objects.item_id import ItemId


class ItemRepository(ABC):

    @abstractmethod
    def save(self, item: Item) -> Item:
        pass

    @abstractmethod
    def find_by_id(self, item_id: ItemId) -> Item | None:
        pass

    @abstractmethod
    def find_all(self, query: str = '', status: str = '',
                 item_type: str = '', category: str = '',
                 offset: int = 0, limit: int = 50) -> list[Item]:
        pass

    @abstractmethod
    def count(self, query: str = '', status: str = '',
              item_type: str = '', category: str = '') -> int:
        pass

    @abstractmethod
    def delete(self, item_id: ItemId) -> None:
        pass
