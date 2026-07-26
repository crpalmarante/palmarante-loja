import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Cpf:
    value: str

    def __post_init__(self):
        cleaned = re.sub(r'[^0-9]', '', self.value)
        if len(cleaned) != 11:
            raise ValueError(f'CPF deve ter 11 dígitos: {self.value}')

    def formatted(self) -> str:
        cleaned = re.sub(r'[^0-9]', '', self.value)
        return f'{cleaned[:3]}.{cleaned[3:6]}.{cleaned[6:9]}-{cleaned[9:]}'

    def __str__(self) -> str:
        return self.formatted()
