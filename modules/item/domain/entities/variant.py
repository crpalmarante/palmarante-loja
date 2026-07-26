from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ItemVariant:
    name: str
    sku: str = ''
    sale_price: float = 0.0
    cost_price: float = 0.0
    stock: float = 0.0
    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
