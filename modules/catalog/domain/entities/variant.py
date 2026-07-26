from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Variant:
    item_id: str
    sku: str = ''
    name: str = ''
    attribute_values: dict[str, str] = field(default_factory=dict)
    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @property
    def display_name(self) -> str:
        if self.name:
            return self.name
        parts = [f'{k}: {v}' for k, v in self.attribute_values.items()]
        return ' / '.join(parts)
