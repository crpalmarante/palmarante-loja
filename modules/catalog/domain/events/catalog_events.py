from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CategoryCreated:
    category_id: str
    name: str
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass
class UnitCreated:
    code: str
    name: str
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass
class AttributeCreated:
    attribute_id: str
    name: str
    occurred_at: datetime = field(default_factory=datetime.now)
