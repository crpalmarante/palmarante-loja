import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Sku:
    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError('SKU não pode ser vazio')
        if len(self.value) > 50:
            raise ValueError(f'SKU muito longo: {len(self.value)} caracteres (máx 50)')

    def __str__(self) -> str:
        return self.value
