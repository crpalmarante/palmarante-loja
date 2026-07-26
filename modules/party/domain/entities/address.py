from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class AddressType(str, Enum):
    BILLING = 'billing'
    SHIPPING = 'shipping'
    HEADQUARTERS = 'headquarters'
    BRANCH = 'branch'
    OTHER = 'other'


@dataclass
class Address:
    street: str = ''
    number: str = ''
    complement: str = ''
    district: str = ''
    city: str = ''
    state: str = ''
    postal_code: str = ''
    ibge_code: str = ''
    country: str = 'Brasil'
    address_type: AddressType = AddressType.OTHER
    is_main: bool = False
    created_at: datetime = field(default_factory=datetime.now)
