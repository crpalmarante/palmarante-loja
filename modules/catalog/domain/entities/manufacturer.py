from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Manufacturer:
    name: str
    cnpj: str = ''
    code: str = ''
    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
