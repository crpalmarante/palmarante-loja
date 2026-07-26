from dataclasses import dataclass
from enum import Enum

from business_core.shared.value_object import ValueObject


class PhoneType(Enum):
    MOBILE = "mobile"
    LANDLINE = "landline"
    FAX = "fax"
    WHATSAPP = "whatsapp"


@dataclass(frozen=True)
class Phone(ValueObject):
    number: str = ""
    type: PhoneType = PhoneType.MOBILE

    def __str__(self):
        return self.number


@dataclass(frozen=True)
class Email(ValueObject):
    address: str = ""

    def __str__(self):
        return self.address
