from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Dimension:
    length: Decimal
    width: Decimal
    height: Decimal
    unit: str = 'cm'

    def __post_init__(self):
        if self.length < 0 or self.width < 0 or self.height < 0:
            raise ValueError('Dimensions cannot be negative')

    def volume(self) -> Decimal:
        return self.length * self.width * self.height

    def __str__(self) -> str:
        return f'{self.length}x{self.width}x{self.height} {self.unit}'
