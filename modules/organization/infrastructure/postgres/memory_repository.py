from modules.organization.domain.entities.organization import Organization
from modules.organization.domain.entities.branch import Branch
from modules.organization.domain.repositories.org_repository import OrganizationRepository


class InMemoryOrganizationRepository(OrganizationRepository):
    def __init__(self):
        self._orgs: dict[str, Organization] = {}
        self._branches: list[Branch] = []

    def save_organization(self, org: Organization) -> Organization:
        self._orgs[org.party_id] = org
        return org

    def find_organization_by_id(self, org_id: str) -> Organization | None:
        return self._orgs.get(org_id)

    def find_organization_by_party(self, party_id: str) -> Organization | None:
        return self._orgs.get(party_id)

    def find_all_organizations(self, query: str = '', active: bool | None = None) -> list[Organization]:
        results = list(self._orgs.values())
        if query:
            q = query.lower()
            results = [o for o in results if q in o.legal_name.lower() or q in o.trade_name.lower()]
        if active is not None:
            results = [o for o in results if o.active == active]
        return results

    def save_branch(self, branch: Branch) -> Branch:
        self._branches.append(branch)
        return branch

    def find_branches_by_organization(self, org_id: str) -> list[Branch]:
        return [b for b in self._branches if b.organization_id == org_id]
