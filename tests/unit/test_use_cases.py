import pytest
from modules.party.domain.entities.party import PartyType
from modules.party.domain.entities.party_role import RoleType
from modules.party.domain.entities.document import DocumentType
from modules.party.domain.entities.address import AddressType
from modules.party.domain.entities.contact import ContactType
from modules.party.domain.value_objects.party_id import PartyId
from modules.party.infrastructure.postgres.memory_repository import InMemoryPartyRepository

from modules.party.application.commands.party_commands import (
    CreateParty, UpdateParty, ActivateParty, DeactivateParty, ArchiveParty,
    AssignRole, RemoveRole,
    AddDocument, RemoveDocument,
    AddAddress, RemoveAddress,
    AddContact, RemoveContact,
)
from modules.party.application.use_cases.create_party import CreatePartyUseCase
from modules.party.application.use_cases.update_party import UpdatePartyUseCase
from modules.party.application.use_cases.activate_party import ActivatePartyUseCase
from modules.party.application.use_cases.assign_role import AssignRoleUseCase
from modules.party.application.use_cases.add_document import AddDocumentUseCase
from modules.party.application.use_cases.add_address import AddAddressUseCase
from modules.party.application.use_cases.add_contact import AddContactUseCase


@pytest.fixture
def repo():
    return InMemoryPartyRepository()


@pytest.fixture
def create_uc(repo):
    return CreatePartyUseCase(repo)


@pytest.fixture
def update_uc(repo):
    return UpdatePartyUseCase(repo)


@pytest.fixture
def activate_uc(repo):
    return ActivatePartyUseCase(repo)


@pytest.fixture
def assign_uc(repo):
    return AssignRoleUseCase(repo)


@pytest.fixture
def doc_uc(repo):
    return AddDocumentUseCase(repo)


@pytest.fixture
def addr_uc(repo):
    return AddAddressUseCase(repo)


@pytest.fixture
def contact_uc(repo):
    return AddContactUseCase(repo)


def create_person(create_uc, **overrides) -> PartyId:
    kwargs = dict(
        party_type=PartyType.PERSON,
        display_name='João Silva',
        given_name='João',
        family_name='Silva',
    )
    kwargs.update(overrides)
    party = create_uc.execute(CreateParty(**kwargs))
    return party.id


class TestCreateParty:
    def test_create_person(self, create_uc):
        party = create_uc.execute(CreateParty(
            party_type=PartyType.PERSON,
            display_name='Maria',
            given_name='Maria',
            family_name='Souza',
        ))
        assert party.display_name == 'Maria'
        assert party.status.value == 'active'
        assert party.person_name.given_name == 'Maria'

    def test_create_company(self, create_uc):
        party = create_uc.execute(CreateParty(
            party_type=PartyType.COMPANY,
            display_name='ABC Ltda',
            legal_name='ABC Ltda',
        ))
        assert party.display_name == 'ABC Ltda'
        assert party.corporate_name.legal_name == 'ABC Ltda'

    def test_create_with_roles(self, create_uc):
        party = create_uc.execute(CreateParty(
            party_type=PartyType.PERSON,
            display_name='Carlos',
            given_name='Carlos',
            family_name='Santos',
            roles=[RoleType.CUSTOMER, RoleType.SUPPLIER],
        ))
        assert party.has_role(RoleType.CUSTOMER) is True
        assert party.has_role(RoleType.SUPPLIER) is True

    def test_create_generates_id(self, create_uc):
        party = create_uc.execute(CreateParty(
            party_type=PartyType.PERSON,
            display_name='Ana',
            given_name='Ana',
            family_name='Costa',
        ))
        assert party.id is not None
        assert len(str(party.id)) > 0

    def test_create_fires_event(self, create_uc):
        create_uc.events.clear()
        party = create_uc.execute(CreateParty(
            party_type=PartyType.PERSON,
            display_name='Pedro',
            given_name='Pedro',
        ))
        assert len(create_uc.events) == 1
        assert str(create_uc.events[0].party_id) == str(party.id)


class TestUpdateParty:
    def test_update_display_name(self, repo, create_uc, update_uc):
        pid = create_person(create_uc)
        update_uc.execute(UpdateParty(party_id=pid, display_name='João Updated'))
        updated = repo.find_by_id(pid)
        assert updated.display_name == 'João Updated'

    def test_update_notes(self, repo, create_uc, update_uc):
        pid = create_person(create_uc)
        update_uc.execute(UpdateParty(party_id=pid, notes='Novas notas'))
        updated = repo.find_by_id(pid)
        assert updated.notes == 'Novas notas'

    def test_update_nonexistent_raises(self, update_uc):
        with pytest.raises(ValueError, match='Party not found'):
            update_uc.execute(UpdateParty(
                party_id=PartyId.generate(),
                display_name='Test',
            ))


class TestActivateParty:
    def test_deactivate(self, repo, create_uc, activate_uc):
        pid = create_person(create_uc)
        activate_uc.deactivate(DeactivateParty(party_id=pid))
        assert repo.find_by_id(pid).status.value == 'inactive'

    def test_reactivate(self, repo, create_uc, activate_uc):
        pid = create_person(create_uc)
        activate_uc.deactivate(DeactivateParty(party_id=pid))
        activate_uc.activate(ActivateParty(party_id=pid))
        assert repo.find_by_id(pid).status.value == 'active'

    def test_archive(self, repo, create_uc, activate_uc):
        pid = create_person(create_uc)
        activate_uc.archive(ArchiveParty(party_id=pid))
        assert repo.find_by_id(pid).status.value == 'archived'

    def test_nonexistent_raises(self, activate_uc):
        with pytest.raises(ValueError, match='Party not found'):
            activate_uc.activate(ActivateParty(party_id=PartyId.generate()))

    def test_fires_events(self, activate_uc, create_uc):
        pid = create_person(create_uc)
        activate_uc.events.clear()
        activate_uc.deactivate(DeactivateParty(party_id=pid))
        assert len(activate_uc.events) == 1
        assert 'Inactivated' in type(activate_uc.events[0]).__name__


class TestAssignRole:
    def test_assign_role(self, repo, create_uc, assign_uc):
        pid = create_person(create_uc)
        assign_uc.execute(AssignRole(party_id=pid, role_type=RoleType.CARRIER))
        party = repo.find_by_id(pid)
        assert party.has_role(RoleType.CARRIER) is True

    def test_remove_role(self, repo, create_uc, assign_uc):
        pid = create_person(create_uc, roles=[RoleType.CUSTOMER])
        assign_uc.remove(RemoveRole(party_id=pid, role_type=RoleType.CUSTOMER))
        party = repo.find_by_id(pid)
        assert party.has_role(RoleType.CUSTOMER) is False

    def test_nonexistent_raises(self, assign_uc):
        with pytest.raises(ValueError, match='Party not found'):
            assign_uc.execute(AssignRole(party_id=PartyId.generate(), role_type=RoleType.CUSTOMER))


class TestAddDocument:
    def test_add_document(self, repo, create_uc, doc_uc):
        pid = create_person(create_uc)
        doc_uc.execute(AddDocument(
            party_id=pid,
            type=DocumentType.CPF,
            value='52998224725',
            is_main=True,
        ))
        party = repo.find_by_id(pid)
        assert len(party.documents) == 1
        assert party.documents[0].value == '52998224725'

    def test_remove_document(self, repo, create_uc, doc_uc):
        pid = create_person(create_uc)
        doc_uc.execute(AddDocument(party_id=pid, type=DocumentType.CPF, value='11111111111'))
        doc_uc.execute(AddDocument(party_id=pid, type=DocumentType.RG, value='123456'))
        party = repo.find_by_id(pid)
        doc_uc.remove(RemoveDocument(party_id=pid, document_index=0))
        party = repo.find_by_id(pid)
        assert len(party.documents) == 1
        assert party.documents[0].type == DocumentType.RG

    def test_nonexistent_raises(self, doc_uc):
        with pytest.raises(ValueError, match='Party not found'):
            doc_uc.execute(AddDocument(
                party_id=PartyId.generate(),
                type=DocumentType.CPF,
                value='11111111111',
            ))


class TestAddAddress:
    def test_add_address(self, repo, create_uc, addr_uc):
        pid = create_person(create_uc)
        addr_uc.execute(AddAddress(
            party_id=pid,
            street='Rua A',
            city='São Paulo',
            state='SP',
            is_main=True,
        ))
        party = repo.find_by_id(pid)
        assert len(party.addresses) == 1
        assert party.addresses[0].street == 'Rua A'

    def test_remove_address(self, repo, create_uc, addr_uc):
        pid = create_person(create_uc)
        addr_uc.execute(AddAddress(party_id=pid, street='Rua A'))
        addr_uc.execute(AddAddress(party_id=pid, street='Rua B'))
        addr_uc.remove(RemoveAddress(party_id=pid, address_index=0))
        party = repo.find_by_id(pid)
        assert len(party.addresses) == 1
        assert party.addresses[0].street == 'Rua B'

    def test_nonexistent_raises(self, addr_uc):
        with pytest.raises(ValueError, match='Party not found'):
            addr_uc.execute(AddAddress(party_id=PartyId.generate(), street='Rua A'))


class TestAddContact:
    def test_add_contact(self, repo, create_uc, contact_uc):
        pid = create_person(create_uc)
        contact_uc.execute(AddContact(
            party_id=pid,
            type=ContactType.EMAIL,
            value='joao@test.com',
            is_main=True,
        ))
        party = repo.find_by_id(pid)
        assert len(party.contacts) == 1
        assert party.contacts[0].value == 'joao@test.com'

    def test_remove_contact(self, repo, create_uc, contact_uc):
        pid = create_person(create_uc)
        contact_uc.execute(AddContact(party_id=pid, type=ContactType.EMAIL, value='a@b.com'))
        contact_uc.execute(AddContact(party_id=pid, type=ContactType.PHONE, value='1199999999'))
        contact_uc.remove(RemoveContact(party_id=pid, contact_index=0))
        party = repo.find_by_id(pid)
        assert len(party.contacts) == 1
        assert party.contacts[0].value == '1199999999'

    def test_nonexistent_raises(self, contact_uc):
        with pytest.raises(ValueError, match='Party not found'):
            contact_uc.execute(AddContact(
                party_id=PartyId.generate(),
                type=ContactType.EMAIL,
                value='a@b.com',
            ))
