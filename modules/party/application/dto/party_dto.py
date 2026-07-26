from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any


@dataclass
class DocumentDTO:
    type: str = ''
    value: str = ''
    issuer: str = ''
    is_main: bool = False


@dataclass
class AddressDTO:
    street: str = ''
    number: str = ''
    complement: str = ''
    district: str = ''
    city: str = ''
    state: str = ''
    postal_code: str = ''
    ibge_code: str = ''
    country: str = 'Brasil'
    address_type: str = 'other'
    is_main: bool = False


@dataclass
class ContactDTO:
    type: str = ''
    value: str = ''
    name: str = ''
    is_main: bool = False


@dataclass
class RoleDTO:
    role_type: str = ''
    status: str = 'active'


@dataclass
class PartyDTO:
    id: str = ''
    party_type: str = ''
    display_name: str = ''
    given_name: str = ''
    family_name: str = ''
    legal_name: str = ''
    trade_name: str = ''
    status: str = 'active'
    roles: list[RoleDTO] = field(default_factory=list)
    documents: list[DocumentDTO] = field(default_factory=list)
    addresses: list[AddressDTO] = field(default_factory=list)
    contacts: list[ContactDTO] = field(default_factory=list)
    notes: str = ''
    created_at: str = ''
    updated_at: str = ''

    def to_dict(self) -> dict[str, Any]:
        result = {}
        for k, v in asdict(self).items():
            if isinstance(v, list):
                result[k] = v
            else:
                result[k] = v
        return result
