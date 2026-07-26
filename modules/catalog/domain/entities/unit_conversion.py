from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal


@dataclass
class UnitConversion:
    from_code: str
    to_code: str
    factor: Decimal
    created_at: datetime = field(default_factory=datetime.now)

    def convert(self, value: Decimal) -> Decimal:
        return value * self.factor
