from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Brand:
    name: str
    code: str = ''
    description: str = ''
    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
