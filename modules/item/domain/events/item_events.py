from dataclasses import dataclass, field
from datetime import datetime
from modules.item.domain.value_objects.item_id import ItemId
from modules.item.domain.entities.item import ItemType


@dataclass
class ItemCreated:
    item_id: ItemId
    name: str
    item_type: ItemType
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass
class ItemUpdated:
    item_id: ItemId
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass
class ItemActivated:
    item_id: ItemId
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass
class ItemInactivated:
    item_id: ItemId
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass
class ItemArchived:
    item_id: ItemId
    occurred_at: datetime = field(default_factory=datetime.now)
