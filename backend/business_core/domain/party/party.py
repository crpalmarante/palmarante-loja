from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

from business_core.domain.party.party_role import PartyRole
from business_core.domain.party.party_address import PartyAddress
from business_core.domain.party.party_contact import PartyContact
from business_core.domain.party.party_document import PartyDocument
from business_core.domain.party.document import Document
from business_core.domain.party.person_name import PersonName, CompanyName
from business_core.domain.party.phone_email import Phone, Email
from business_core.shared.aggregate_root import AggregateRoot
from business_core.shared.domain_event import DomainEvent

from uuid import uuid4


class PartyType(Enum):
    PERSON = "person"
    ORGANIZATION = "organization"


class PartyStatus(Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    ARCHIVED = "archived"


@dataclass
class Party(AggregateRoot):
    party_type: PartyType = PartyType.PERSON
    person_name: Optional[PersonName] = None
    company_name: Optional[CompanyName] = None
    status: PartyStatus = PartyStatus.ACTIVE
    documents: list = field(default_factory=list)
    roles: list = field(default_factory=list)
    addresses: list = field(default_factory=list)
    contacts: list = field(default_factory=list)
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid4())
        if not self.created_at:
            self.created_at = datetime.now()
            self.updated_at = self.created_at

    @staticmethod
    def create_person(given_name, family_name, display_name=None):
        name = PersonName(
            given_name=given_name,
            family_name=family_name,
            display_name=display_name or f"{given_name} {family_name}"
        )
        party = Party(party_type=PartyType.PERSON, person_name=name)
        party.apply(DomainEvent(event_type="PartyCreated", payload={
            "party_id": party.id, "party_type": "person", "name": str(name)
        }))
        return party

    @staticmethod
    def create_organization(legal_name, trade_name=None):
        name = CompanyName(
            legal_name=legal_name,
            trade_name=trade_name or legal_name
        )
        party = Party(party_type=PartyType.ORGANIZATION, company_name=name)
        party.apply(DomainEvent(event_type="PartyCreated", payload={
            "party_id": party.id, "party_type": "organization", "name": str(name)
        }))
        return party

    def add_role(self, role: PartyRole):
        if role not in self.roles:
            self.roles.append(role)
            self.apply(DomainEvent(event_type="RoleAssigned", payload={
                "party_id": self.id, "role": role.role_type.value
            }))

    def remove_role(self, role_type):
        self.roles = [r for r in self.roles if r.role_type != role_type]
        self.apply(DomainEvent(event_type="RoleRemoved", payload={
            "party_id": self.id, "role": role_type.value
        }))

    def add_address(self, address: PartyAddress):
        if address.is_main:
            for a in self.addresses:
                object.__setattr__(a, "is_main", False)
        self.addresses.append(address)

    def add_contact(self, contact: PartyContact):
        if contact.is_main:
            for c in self.contacts:
                object.__setattr__(c, "is_main", False)
        self.contacts.append(contact)

    def add_document(self, document: PartyDocument):
        if document.is_main:
            for d in self.documents:
                object.__setattr__(d, "is_main", False)
        self.documents.append(document)

    def get_main_document(self):
        for d in self.documents:
            if d.is_main:
                return d
        return self.documents[0] if self.documents else None

    def get_main_address(self):
        for a in self.addresses:
            if a.is_main:
                return a
        return self.addresses[0] if self.addresses else None

    def get_main_contact(self):
        for c in self.contacts:
            if c.is_main:
                return c
        return self.contacts[0] if self.contacts else None

    def has_role(self, role_type) -> bool:
        return any(r.role_type == role_type and r.status.value == "active" for r in self.roles)

    def suspend(self):
        self.status = PartyStatus.SUSPENDED
        self.updated_at = datetime.now()
        self.apply(DomainEvent(event_type="PartySuspended", payload={"party_id": self.id}))

    def activate(self):
        self.status = PartyStatus.ACTIVE
        self.updated_at = datetime.now()
        self.apply(DomainEvent(event_type="PartyActivated", payload={"party_id": self.id}))

    def archive(self):
        self.status = PartyStatus.ARCHIVED
        self.updated_at = datetime.now()
        self.apply(DomainEvent(event_type="PartyArchived", payload={"party_id": self.id}))

    @property
    def display_name(self):
        if self.party_type == PartyType.PERSON and self.person_name:
            return str(self.person_name)
        if self.party_type == PartyType.ORGANIZATION and self.company_name:
            return str(self.company_name)
        return ""
