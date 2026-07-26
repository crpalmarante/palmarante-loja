from dataclasses import dataclass
from enum import Enum

from business_core.domain.party.address import Address
from business_core.shared.value_object import ValueObject


class AddressType(Enum):
    MAIN = "main"
    BILLING = "billing"
    SHIPPING = "shipping"
    HEADQUARTERS = "headquarters"
    BRANCH = "branch"
    OTHER = "other"


@dataclass(frozen=True)
class PartyAddress(ValueObject):
    address: Address = None
    type: AddressType = AddressType.MAIN
    is_main: bool = False
