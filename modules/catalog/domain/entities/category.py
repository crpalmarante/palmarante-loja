from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Category:
    name: str
    parent_id: str | None = None
    code: str = ''
    description: str = ''
    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @property
    def path(self) -> list[str]:
        parts = []
        if self.parent_id:
            parts.append(self.parent_id)
        parts.append(self.name)
        return parts
