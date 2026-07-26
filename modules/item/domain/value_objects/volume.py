from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Volume:
    value: Decimal
    unit: str = 'm3'

    def __post_init__(self):
        if self.value < 0:
            raise ValueError(f'Volume cannot be negative: {self.value}')

    def in_liters(self) -> Decimal:
        if self.unit == 'm3':
            return self.value * Decimal('1000')
        if self.unit == 'l':
            return self.value
        return self.value

    def __str__(self) -> str:
        return f'{self.value:.3f} {self.unit}'
