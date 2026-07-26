import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Cnpj:
    value: str

    def __post_init__(self):
        cleaned = re.sub(r'[^0-9]', '', self.value)
        if len(cleaned) != 14:
            raise ValueError(f'CNPJ deve ter 14 dígitos: {self.value}')

    def formatted(self) -> str:
        cleaned = re.sub(r'[^0-9]', '', self.value)
        return f'{cleaned[:2]}.{cleaned[2:5]}.{cleaned[5:8]}/{cleaned[8:12]}-{cleaned[12:]}'

    def __str__(self) -> str:
        return self.formatted()
