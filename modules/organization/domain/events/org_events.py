from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CompanyCreated:
    party_id: str
    legal_name: str
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass
class CompanyUpdated:
    party_id: str
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass
class CompanyActivated:
    party_id: str
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass
class CompanyInactivated:
    party_id: str
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass
class BranchCreated:
    company_id: str
    name: str
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass
class EstablishmentCreated:
    company_id: str
    cnpj: str
    occurred_at: datetime = field(default_factory=datetime.now)
