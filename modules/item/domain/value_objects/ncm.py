import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Ncm:
    value: str

    def __post_init__(self):
        cleaned = re.sub(r'[^0-9]', '', self.value)
        if len(cleaned) != 8:
            raise ValueError(f'NCM deve ter 8 dígitos: {self.value}')

    def formatted(self) -> str:
        cleaned = re.sub(r'[^0-9]', '', self.value)
        return f'{cleaned[:4]}.{cleaned[4:6]}.{cleaned[6:]}'

    def __str__(self) -> str:
        return self.formatted()
