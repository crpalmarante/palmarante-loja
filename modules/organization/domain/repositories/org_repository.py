from abc import ABC, abstractmethod
from modules.organization.domain.entities.organization import Organization
from modules.organization.domain.entities.branch import Branch


class OrganizationRepository(ABC):

    @abstractmethod
    def save_organization(self, org: Organization) -> Organization:
        pass

    @abstractmethod
    def find_organization_by_id(self, org_id: str) -> Organization | None:
        pass

    @abstractmethod
    def find_organization_by_party(self, party_id: str) -> Organization | None:
        pass

    @abstractmethod
    def find_all_organizations(self, query: str = '', active: bool | None = None) -> list[Organization]:
        pass

    @abstractmethod
    def save_branch(self, branch: Branch) -> Branch:
        pass

    @abstractmethod
    def find_branches_by_organization(self, org_id: str) -> list[Branch]:
        pass
