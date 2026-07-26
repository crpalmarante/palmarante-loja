import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Cep:
    value: str

    def __post_init__(self):
        cleaned = re.sub(r'[^0-9]', '', self.value)
        if len(cleaned) != 8:
            raise ValueError(f'CEP deve ter 8 dígitos: {self.value}')

    def formatted(self) -> str:
        cleaned = re.sub(r'[^0-9]', '', self.value)
        return f'{cleaned[:5]}-{cleaned[5:]}'

    def __str__(self) -> str:
        return self.formatted()
