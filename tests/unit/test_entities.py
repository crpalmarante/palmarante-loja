import pytest
from datetime import datetime

from modules.party.domain.entities.party import Party, PartyType, PartyStatus
from modules.party.domain.entities.party_role import PartyRole, RoleType, RoleStatus
from modules.party.domain.entities.document import Document, DocumentType
from modules.party.domain.entities.address import Address, AddressType
from modules.party.domain.entities.contact import Contact, ContactType
from modules.party.domain.value_objects.party_id import PartyId
from modules.party.domain.value_objects.person_name import PersonName
from modules.party.domain.value_objects.corporate_name import CorporateName


def make_person(**kwargs) -> Party:
    defaults = dict(
        id=PartyId.generate(),
        party_type=PartyType.PERSON,
        display_name='João Silva',
        person_name=PersonName(given_name='João', family_name='Silva'),
    )
    defaults.update(kwargs)
    return Party(**defaults)


def make_company(**kwargs) -> Party:
    defaults = dict(
        id=PartyId.generate(),
        party_type=PartyType.COMPANY,
        display_name='ABC Ltda',
        corporate_name=CorporateName(legal_name='ABC Ltda', trade_name='ABC'),
    )
    defaults.update(kwargs)
    return Party(**defaults)


class TestPartyLifecycle:
    def test_create_person(self):
        p = make_person()
        assert p.party_type == PartyType.PERSON
        assert p.status == PartyStatus.ACTIVE
        assert p.display_name == 'João Silva'
        assert str(p.person_name) == 'João Silva'

    def test_create_company(self):
        p = make_company()
        assert p.party_type == PartyType.COMPANY
        assert p.display_name == 'ABC Ltda'
        assert str(p.corporate_name) == 'ABC'

    def test_activate(self):
        p = make_person()
        p.deactivate()
        assert p.status == PartyStatus.INACTIVE
        p.activate()
        assert p.status == PartyStatus.ACTIVE

    def test_deactivate(self):
        p = make_person()
        p.deactivate()
        assert p.status == PartyStatus.INACTIVE

    def test_archive(self):
        p = make_person()
        p.archive()
        assert p.status == PartyStatus.ARCHIVED

    def test_activate_archived_raises(self):
        p = make_person()
        p.archive()
        with pytest.raises(ValueError, match='Cannot activate an archived party'):
            p.activate()

    def test_deactivate_archived_raises(self):
        p = make_person()
        p.archive()
        with pytest.raises(ValueError, match='Cannot deactivate an archived party'):
            p.deactivate()


class TestPartyRoles:
    def test_assign_role(self):
        p = make_person()
        p.assign_role(RoleType.CUSTOMER)
        assert p.has_role(RoleType.CUSTOMER) is True

    def test_multiple_roles(self):
        p = make_person()
        p.assign_role(RoleType.CUSTOMER)
        p.assign_role(RoleType.SUPPLIER)
        assert p.has_role(RoleType.CUSTOMER) is True
        assert p.has_role(RoleType.SUPPLIER) is True

    def test_remove_role(self):
        p = make_person()
        p.assign_role(RoleType.CUSTOMER)
        p.remove_role(RoleType.CUSTOMER)
        assert p.has_role(RoleType.CUSTOMER) is False

    def test_assign_same_role_twice(self):
        p = make_person()
        p.assign_role(RoleType.CUSTOMER)
        p.assign_role(RoleType.CUSTOMER)
        active = [r for r in p.roles if r.status == RoleStatus.ACTIVE]
        assert len(active) == 1

    def test_has_role_str(self):
        p = make_person()
        p.assign_role(RoleType.CUSTOMER)
        assert p.has_role_str('customer') is True
        assert p.has_role_str('supplier') is False


class TestPartyDocuments:
    def test_add_document(self):
        p = make_person()
        doc = Document(type=DocumentType.CPF, value='52998224725', is_main=True)
        p.add_document(doc)
        assert len(p.documents) == 1
        assert p.documents[0].value == '52998224725'

    def test_main_document(self):
        p = make_person()
        p.add_document(Document(type=DocumentType.CPF, value='11111111111'))
        p.add_document(Document(type=DocumentType.RG, value='123456', is_main=True))
        assert p.main_document.type == DocumentType.RG

    def test_add_document_sets_main(self):
        p = make_person()
        p.add_document(Document(type=DocumentType.CPF, value='11111111111', is_main=True))
        p.add_document(Document(type=DocumentType.RG, value='123456', is_main=True))
        assert p.documents[0].is_main is False
        assert p.documents[1].is_main is True

    def test_remove_document(self):
        p = make_person()
        p.add_document(Document(type=DocumentType.CPF, value='11111111111'))
        p.add_document(Document(type=DocumentType.RG, value='123456'))
        p.remove_document(0)
        assert len(p.documents) == 1
        assert p.documents[0].type == DocumentType.RG

    def test_remove_document_invalid_index(self):
        p = make_person()
        p.add_document(Document(type=DocumentType.CPF, value='11111111111'))
        p.remove_document(99)
        assert len(p.documents) == 1


class TestPartyAddresses:
    def test_add_address(self):
        p = make_person()
        addr = Address(street='Rua A', city='São Paulo', state='SP', is_main=True)
        p.add_address(addr)
        assert len(p.addresses) == 1

    def test_main_address(self):
        p = make_person()
        p.add_address(Address(street='Rua A', city='SP'))
        p.add_address(Address(street='Rua B', city='RJ', is_main=True))
        assert p.main_address.street == 'Rua B'

    def test_remove_address(self):
        p = make_person()
        p.add_address(Address(street='Rua A'))
        p.add_address(Address(street='Rua B'))
        p.remove_address(0)
        assert len(p.addresses) == 1
        assert p.addresses[0].street == 'Rua B'

    def test_remove_address_invalid_index(self):
        p = make_person()
        p.add_address(Address(street='Rua A'))
        p.remove_address(99)
        assert len(p.addresses) == 1


class TestPartyContacts:
    def test_add_contact(self):
        p = make_person()
        contact = Contact(type=ContactType.EMAIL, value='joao@test.com', is_main=True)
        p.add_contact(contact)
        assert len(p.contacts) == 1

    def test_main_contact(self):
        p = make_person()
        p.add_contact(Contact(type=ContactType.EMAIL, value='a@b.com'))
        p.add_contact(Contact(type=ContactType.PHONE, value='1199999999', is_main=True))
        assert p.main_contact.value == '1199999999'

    def test_remove_contact(self):
        p = make_person()
        p.add_contact(Contact(type=ContactType.EMAIL, value='a@b.com'))
        p.add_contact(Contact(type=ContactType.PHONE, value='1199999999'))
        p.remove_contact(0)
        assert len(p.contacts) == 1
        assert p.contacts[0].value == '1199999999'

    def test_remove_contact_invalid_index(self):
        p = make_person()
        p.add_contact(Contact(type=ContactType.EMAIL, value='a@b.com'))
        p.remove_contact(99)
        assert len(p.contacts) == 1
