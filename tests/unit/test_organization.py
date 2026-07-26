import pytest
from modules.organization.domain.entities.organization import Organization, TaxRegime, CRT
from modules.organization.domain.entities.branch import Branch
from modules.organization.infrastructure.postgres.memory_repository import InMemoryOrganizationRepository
from modules.organization.application.use_cases.create_organization import CreateOrganizationUseCase
from modules.organization.application.commands.org_commands import (
    CreateOrganization, CreateBranch,
)


class TestOrganizationEntity:
    def test_create_org(self):
        o = Organization(party_id='p1', legal_name='ABC Ltda')
        assert o.legal_name == 'ABC Ltda'
        assert o.active is True
        assert o.tax_regime == TaxRegime.LUCRO_PRESUMIDO

    def test_org_with_all_fields(self):
        o = Organization(
            party_id='p1', legal_name='ABC Ltda', trade_name='ABC',
            cnpj='11444777000101', ie='123456789', crt=CRT.SN1,
            cnae='6202300', tax_regime=TaxRegime.SIMPLES_NACIONAL,
        )
        assert o.trade_name == 'ABC'
        assert o.crt == CRT.SN1
        assert o.tax_regime == TaxRegime.SIMPLES_NACIONAL

    def test_deactivate(self):
        o = Organization(party_id='p1', legal_name='Test')
        o.deactivate()
        assert o.active is False

    def test_activate(self):
        o = Organization(party_id='p1', legal_name='Test')
        o.deactivate()
        o.activate()
        assert o.active is True


class TestBranchEntity:
    def test_create_branch(self):
        b = Branch(organization_id='o1', party_id='p2', name='Filial Centro')
        assert b.name == 'Filial Centro'
        assert b.active is True

    def test_branch_deactivate(self):
        b = Branch(organization_id='o1', party_id='p2')
        b.deactivate()
        assert b.active is False


class TestCreateOrganizationUseCase:
    @pytest.fixture
    def repo(self):
        return InMemoryOrganizationRepository()

    @pytest.fixture
    def uc(self, repo):
        return CreateOrganizationUseCase(repo)

    def test_create_org(self, uc, repo):
        org = uc.execute(CreateOrganization(
            party_id='p1', legal_name='ABC Ltda', trade_name='ABC',
            cnpj='11444777000101',
        ))
        assert org.legal_name == 'ABC Ltda'
        assert org.trade_name == 'ABC'
        assert repo.find_organization_by_party('p1') is not None

    def test_create_fires_event(self, uc):
        uc.events.clear()
        uc.execute(CreateOrganization(party_id='p1', legal_name='Test'))
        assert len(uc.events) == 1
        assert uc.events[0].legal_name == 'Test'

    def test_find_all(self, repo, uc):
        uc.execute(CreateOrganization(party_id='p1', legal_name='Alpha'))
        uc.execute(CreateOrganization(party_id='p2', legal_name='Beta'))
        assert len(repo.find_all_organizations()) == 2

    def test_find_all_query(self, repo, uc):
        uc.execute(CreateOrganization(party_id='p1', legal_name='Alpha Ltda'))
        uc.execute(CreateOrganization(party_id='p2', legal_name='Beta SA'))
        results = repo.find_all_organizations(query='alpha')
        assert len(results) == 1
        assert results[0].legal_name == 'Alpha Ltda'

    def test_find_all_active_filter(self, repo, uc):
        uc.execute(CreateOrganization(party_id='p1', legal_name='Alpha'))
        o2 = uc.execute(CreateOrganization(party_id='p2', legal_name='Beta'))
        o2.deactivate()
        repo.save_organization(o2)
        results = repo.find_all_organizations(active=True)
        assert len(results) == 1


class TestBranchRepository:
    @pytest.fixture
    def repo(self):
        return InMemoryOrganizationRepository()

    def test_save_and_find_branches(self, repo):
        repo.save_branch(Branch(organization_id='o1', party_id='p2', name='Filial A'))
        repo.save_branch(Branch(organization_id='o1', party_id='p3', name='Filial B'))
        repo.save_branch(Branch(organization_id='o2', party_id='p4', name='Outra'))
        branches = repo.find_branches_by_organization('o1')
        assert len(branches) == 2
