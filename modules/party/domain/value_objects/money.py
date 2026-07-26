from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = 'BRL'

    def __str__(self) -> str:
        return f'{self.currency} {self.amount:.2f}'
