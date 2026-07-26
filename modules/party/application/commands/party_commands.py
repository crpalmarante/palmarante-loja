from dataclasses import dataclass, field
from modules.party.domain.value_objects.party_id import PartyId
from modules.party.domain.entities.party import PartyType
from modules.party.domain.entities.party_role import RoleType
from modules.party.domain.entities.document import DocumentType
from modules.party.domain.entities.address import AddressType
from modules.party.domain.entities.contact import ContactType


@dataclass
class CreateParty:
    party_type: PartyType
    display_name: str
    given_name: str = ''
    family_name: str = ''
    legal_name: str = ''
    trade_name: str = ''
    roles: list[RoleType] | None = None
    notes: str = ''


@dataclass
class UpdateParty:
    party_id: PartyId
    display_name: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    legal_name: str | None = None
    trade_name: str | None = None
    notes: str | None = None


@dataclass
class ActivateParty:
    party_id: PartyId


@dataclass
class DeactivateParty:
    party_id: PartyId


@dataclass
class ArchiveParty:
    party_id: PartyId


@dataclass
class AssignRole:
    party_id: PartyId
    role_type: RoleType


@dataclass
class RemoveRole:
    party_id: PartyId
    role_type: RoleType


@dataclass
class AddDocument:
    party_id: PartyId
    type: DocumentType
    value: str
    issuer: str = ''
    is_main: bool = False


@dataclass
class RemoveDocument:
    party_id: PartyId
    document_index: int


@dataclass
class AddAddress:
    party_id: PartyId
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


@dataclass
class RemoveAddress:
    party_id: PartyId
    address_index: int


@dataclass
class AddContact:
    party_id: PartyId
    type: ContactType
    value: str
    name: str = ''
    is_main: bool = False


@dataclass
class RemoveContact:
    party_id: PartyId
    contact_index: int
