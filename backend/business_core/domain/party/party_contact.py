from dataclasses import dataclass
from enum import Enum

from business_core.domain.party.phone_email import Email, Phone
from business_core.shared.value_object import ValueObject


class ContactType(Enum):
    COMMERCIAL = "commercial"
    FINANCIAL = "financial"
    TECHNICAL = "technical"
    ADMINISTRATIVE = "administrative"
    OTHER = "other"


@dataclass(frozen=True)
class PartyContact(ValueObject):
    name: str = ""
    phone: Phone = None
    email: Email = None
    role: str = ""
    type: ContactType = ContactType.COMMERCIAL
    is_main: bool = False
