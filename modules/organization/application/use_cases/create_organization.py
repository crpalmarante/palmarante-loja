from modules.organization.domain.entities.organization import Organization
from modules.organization.domain.events.org_events import CompanyCreated
from modules.organization.domain.repositories.org_repository import OrganizationRepository
from modules.organization.application.commands.org_commands import CreateOrganization


class CreateOrganizationUseCase:
    def __init__(self, repository: OrganizationRepository):
        self.repository = repository
        self.events: list = []

    def execute(self, cmd: CreateOrganization) -> Organization:
        org = Organization(
            party_id=cmd.party_id,
            legal_name=cmd.legal_name,
            trade_name=cmd.trade_name,
            cnpj=cmd.cnpj,
            ie=cmd.ie,
            im=cmd.im,
            crt=cmd.crt,
            cnae=cmd.cnae,
            tax_regime=cmd.tax_regime,
        )
        self.repository.save_organization(org)
        self.events.append(CompanyCreated(
            party_id=cmd.party_id,
            legal_name=cmd.legal_name,
        ))
        return org
