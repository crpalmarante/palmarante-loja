from dataclasses import dataclass


@dataclass(frozen=True)
class AddressData:
    street: str = ''
    number: str = ''
    complement: str = ''
    district: str = ''
    city: str = ''
    state: str = ''
    postal_code: str = ''
    ibge_code: str = ''
    country: str = 'Brasil'

    def __str__(self) -> str:
        parts = [f'{self.street}, {self.number}' if self.street else '']
        if self.complement:
            parts.append(self.complement)
        parts.append(self.district)
        parts.append(f'{self.city}/{self.state}' if self.city else '')
        return ' - '.join(p for p in parts if p)
