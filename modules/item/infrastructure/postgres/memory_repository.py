from modules.item.domain.entities.item import Item
from modules.item.domain.value_objects.item_id import ItemId
from modules.item.domain.repositories.item_repository import ItemRepository


class InMemoryItemRepository(ItemRepository):
    def __init__(self):
        self._items: dict[str, Item] = {}

    def save(self, item: Item) -> Item:
        self._items[str(item.id)] = item
        return item

    def find_by_id(self, item_id: ItemId) -> Item | None:
        return self._items.get(str(item_id))

    def find_all(self, query: str = '', status: str = '',
                 item_type: str = '', category: str = '',
                 offset: int = 0, limit: int = 50) -> list[Item]:
        results = list(self._items.values())

        if query:
            q = query.lower()
            results = [i for i in results if q in i.name.lower()
                       or (i.has_sku and q in str(i.sku).lower())
                       or (i.has_ean and q in str(i.ean))]

        if status:
            results = [i for i in results if i.status.value == status]

        if item_type:
            results = [i for i in results if i.item_type.value == item_type]

        if category:
            c = category.lower()
            results = [i for i in results if c in i.category.lower()]

        results.sort(key=lambda i: i.created_at, reverse=True)
        return results[offset:offset + limit]

    def count(self, query: str = '', status: str = '',
              item_type: str = '', category: str = '') -> int:
        return len(self.find_all(query, status, item_type, category))

    def delete(self, item_id: ItemId) -> None:
        self._items.pop(str(item_id), None)
