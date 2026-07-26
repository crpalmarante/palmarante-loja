import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Ean:
    value: str

    def __post_init__(self):
        cleaned = re.sub(r'[^0-9]', '', self.value)
        if len(cleaned) not in (8, 13):
            raise ValueError(f'EAN deve ter 8 ou 13 dígitos: {self.value}')

    def formatted(self) -> str:
        return re.sub(r'[^0-9]', '', self.value)

    def __str__(self) -> str:
        return self.formatted()
