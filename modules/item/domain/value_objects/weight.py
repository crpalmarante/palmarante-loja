from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Weight:
    value: Decimal
    unit: str = 'kg'

    def __post_init__(self):
        if self.value < 0:
            raise ValueError(f'Weight cannot be negative: {self.value}')

    def in_grams(self) -> Decimal:
        if self.unit == 'kg':
            return self.value * Decimal('1000')
        if self.unit == 'g':
            return self.value
        if self.unit == 'lb':
            return self.value * Decimal('453.592')
        return self.value

    def __str__(self) -> str:
        return f'{self.value:.3f} {self.unit}'
