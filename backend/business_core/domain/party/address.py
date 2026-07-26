from dataclasses import dataclass

from business_core.shared.value_object import ValueObject


@dataclass(frozen=True)
class Address(ValueObject):
    street: str = ""
    number: str = ""
    complement: str = ""
    district: str = ""
    city: str = ""
    region: str = ""
    country: str = "Brasil"
    postal_code: str = ""

    def __str__(self):
        parts = [self.street, self.number]
        if self.complement:
            parts.append(self.complement)
        parts.append(self.city)
        parts.append(self.region)
        return ", ".join(p for p in parts if p)
