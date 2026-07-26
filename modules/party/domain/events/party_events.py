from dataclasses import dataclass, field
from datetime import datetime
from modules.party.domain.value_objects.party_id import PartyId
from modules.party.domain.entities.party import PartyType
from modules.party.domain.entities.address import Address
from modules.party.domain.entities.document import Document
from modules.party.domain.entities.contact import Contact


@dataclass
class PartyCreated:
    party_id: PartyId
    party_type: PartyType
    display_name: str
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass
class PartyUpdated:
    party_id: PartyId
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass
class PartyActivated:
    party_id: PartyId
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass
class PartyInactivated:
    party_id: PartyId
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass
class PartyArchived:
    party_id: PartyId
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass
class AddressAdded:
    party_id: PartyId
    address: Address
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass
class DocumentAdded:
    party_id: PartyId
    document: Document
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass
class ContactAdded:
    party_id: PartyId
    contact: Contact
    occurred_at: datetime = field(default_factory=datetime.now)
