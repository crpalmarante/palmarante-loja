from dataclasses import dataclass

from business_core.shared.value_object import ValueObject


@dataclass(frozen=True)
class PersonName(ValueObject):
    given_name: str = ""
    middle_name: str = ""
    family_name: str = ""
    display_name: str = ""

    @property
    def full_name(self):
        parts = [p for p in [self.given_name, self.middle_name, self.family_name] if p]
        return " ".join(parts) if parts else self.display_name

    def __str__(self):
        return self.display_name or self.full_name


@dataclass(frozen=True)
class CompanyName(ValueObject):
    legal_name: str = ""
    trade_name: str = ""

    def __str__(self):
        return self.trade_name or self.legal_name
