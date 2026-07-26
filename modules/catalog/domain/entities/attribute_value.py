from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AttributeValue:
    attribute_id: str
    value: str
    code: str = ''
    sort_order: int = 0
    created_at: datetime = field(default_factory=datetime.now)
