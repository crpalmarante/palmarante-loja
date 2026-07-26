from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from modules.party.domain.value_objects.party_id import PartyId
from modules.party.domain.value_objects.person_name import PersonName
from modules.party.domain.value_objects.corporate_name import CorporateName
from modules.party.domain.entities.party_role import PartyRole, RoleType, RoleStatus
from modules.party.domain.entities.document import Document, DocumentType
from modules.party.domain.entities.address import Address
from modules.party.domain.entities.contact import Contact


class PartyType(str, Enum):
    PERSON = 'person'
    COMPANY = 'company'


class PartyStatus(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    ARCHIVED = 'archived'


@dataclass
class Party:
    id: PartyId
    party_type: PartyType
    display_name: str
    person_name: PersonName | None = None
    corporate_name: CorporateName | None = None
    status: PartyStatus = PartyStatus.ACTIVE
    roles: list[PartyRole] = field(default_factory=list)
    documents: list[Document] = field(default_factory=list)
    addresses: list[Address] = field(default_factory=list)
    contacts: list[Contact] = field(default_factory=list)
    notes: str = ''
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def activate(self):
        if self.status == PartyStatus.ARCHIVED:
            raise ValueError('Cannot activate an archived party')
        self.status = PartyStatus.ACTIVE
        self.updated_at = datetime.now()

    def deactivate(self):
        if self.status == PartyStatus.ARCHIVED:
            raise ValueError('Cannot deactivate an archived party')
        self.status = PartyStatus.INACTIVE
        self.updated_at = datetime.now()

    def archive(self):
        self.status = PartyStatus.ARCHIVED
        self.updated_at = datetime.now()

    def has_role(self, role_type: RoleType) -> bool:
        return any(r.role_type == role_type and r.status == RoleStatus.ACTIVE for r in self.roles)

    def has_role_str(self, role_type_str: str) -> bool:
        return any(r.role_type.value == role_type_str and r.status == RoleStatus.ACTIVE for r in self.roles)

    def assign_role(self, role_type: RoleType):
        existing = next((r for r in self.roles if r.role_type == role_type), None)
        if existing:
            existing.activate()
        else:
            self.roles.append(PartyRole(role_type=role_type))
        self.updated_at = datetime.now()

    def remove_role(self, role_type: RoleType):
        existing = next((r for r in self.roles if r.role_type == role_type), None)
        if existing:
            existing.deactivate()
        self.updated_at = datetime.now()

    def add_document(self, doc: Document):
        if doc.is_main:
            for d in self.documents:
                d.is_main = False
        self.documents.append(doc)
        self.updated_at = datetime.now()

    def remove_document(self, document_index: int):
        if 0 <= document_index < len(self.documents):
            del self.documents[document_index]
            self.updated_at = datetime.now()

    def add_address(self, addr: Address):
        if addr.is_main:
            for a in self.addresses:
                a.is_main = False
        self.addresses.append(addr)
        self.updated_at = datetime.now()

    def remove_address(self, address_index: int):
        if 0 <= address_index < len(self.addresses):
            del self.addresses[address_index]
            self.updated_at = datetime.now()

    def add_contact(self, contact: Contact):
        if contact.is_main:
            for c in self.contacts:
                c.is_main = False
        self.contacts.append(contact)
        self.updated_at = datetime.now()

    def remove_contact(self, contact_index: int):
        if 0 <= contact_index < len(self.contacts):
            del self.contacts[contact_index]
            self.updated_at = datetime.now()

    def add_contact_from_dict(self, data: dict):
        from modules.party.domain.entities.contact import Contact, ContactType
        c = Contact(
            type=ContactType(data.get('type', 'other')),
            value=data.get('value', ''),
            name=data.get('name', ''),
            is_main=data.get('is_main', False),
        )
        if c.is_main:
            for existing in self.contacts:
                existing.is_main = False
        self.contacts.append(c)
        self.updated_at = datetime.now()

    @property
    def main_document(self) -> Document | None:
        for d in self.documents:
            if d.is_main:
                return d
        return self.documents[0] if self.documents else None

    @property
    def main_address(self) -> Address | None:
        for a in self.addresses:
            if a.is_main:
                return a
        return self.addresses[0] if self.addresses else None

    @property
    def main_contact(self) -> Contact | None:
        for c in self.contacts:
            if c.is_main:
                return c
        return self.contacts[0] if self.contacts else None
