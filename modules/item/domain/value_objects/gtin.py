import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Gtin:
    value: str

    def __post_init__(self):
        cleaned = re.sub(r'[^0-9]', '', self.value)
        if len(cleaned) not in (8, 12, 13, 14):
            raise ValueError(f'GTIN deve ter 8, 12, 13 ou 14 dígitos: {self.value}')

    def formatted(self) -> str:
        return re.sub(r'[^0-9]', '', self.value)

    def __str__(self) -> str:
        return self.formatted()
