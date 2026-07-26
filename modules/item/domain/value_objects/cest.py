import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Cest:
    value: str

    def __post_init__(self):
        cleaned = re.sub(r'[^0-9]', '', self.value)
        if len(cleaned) != 7:
            raise ValueError(f'CEST deve ter 7 dígitos: {self.value}')

    def formatted(self) -> str:
        cleaned = re.sub(r'[^0-9]', '', self.value)
        return f'{cleaned[:2]}.{cleaned[2:5]}.{cleaned[5:]}'

    def __str__(self) -> str:
        return self.formatted()
