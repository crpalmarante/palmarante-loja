from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class PriceHistory:
    cost_price: float
    sale_price: float
    reason: str = ''
    changed_at: datetime = field(default_factory=datetime.now)
