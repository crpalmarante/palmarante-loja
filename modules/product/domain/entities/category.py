from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Category:
    name: str
    parent_id: str | None = None
    description: str = ''
    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return self.name
