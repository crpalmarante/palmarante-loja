import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Phone:
    value: str

    def formatted(self) -> str:
        cleaned = re.sub(r'[^0-9]', '', self.value)
        if len(cleaned) == 11:
            return f'({cleaned[:2]}) {cleaned[2:7]}-{cleaned[7:]}'
        if len(cleaned) == 10:
            return f'({cleaned[:2]}) {cleaned[2:6]}-{cleaned[6:]}'
        return self.value

    def __str__(self) -> str:
        return self.formatted()
