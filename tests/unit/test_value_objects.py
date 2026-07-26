import pytest
from decimal import Decimal
from datetime import date, datetime

from modules.party.domain.value_objects.cpf import Cpf
from modules.party.domain.value_objects.cnpj import Cnpj
from modules.party.domain.value_objects.cep import Cep
from modules.party.domain.value_objects.email import Email
from modules.party.domain.value_objects.phone import Phone
from modules.party.domain.value_objects.person_name import PersonName
from modules.party.domain.value_objects.corporate_name import CorporateName
from modules.party.domain.value_objects.party_id import PartyId
from modules.party.domain.value_objects.date_range import DateRange
from modules.party.domain.value_objects.money import Money


class TestCpf:
    def test_valid_cpf(self):
        cpf = Cpf('529.982.247-25')
        assert cpf.formatted() == '529.982.247-25'

    def test_cpf_only_digits(self):
        cpf = Cpf('52998224725')
        assert cpf.formatted() == '529.982.247-25'

    def test_cpf_too_short(self):
        with pytest.raises(ValueError, match='CPF deve ter 11 dígitos'):
            Cpf('123.456.789-0')

    def test_cpf_too_long(self):
        with pytest.raises(ValueError, match='CPF deve ter 11 dígitos'):
            Cpf('123.456.789-00-1')

    def test_cpf_empty(self):
        with pytest.raises(ValueError, match='CPF deve ter 11 dígitos'):
            Cpf('')

    def test_cpf_str(self):
        assert str(Cpf('52998224725')) == '529.982.247-25'


class TestCnpj:
    def test_valid_cnpj(self):
        cnpj = Cnpj('11.444.777/0001-01')
        assert cnpj.formatted() == '11.444.777/0001-01'

    def test_cnpj_only_digits(self):
        cnpj = Cnpj('11444777000101')
        assert cnpj.formatted() == '11.444.777/0001-01'

    def test_cnpj_too_short(self):
        with pytest.raises(ValueError, match='CNPJ deve ter 14 dígitos'):
            Cnpj('11.444.777/0001-0')

    def test_cnpj_too_long(self):
        with pytest.raises(ValueError, match='CNPJ deve ter 14 dígitos'):
            Cnpj('11.444.777/0001-011')

    def test_cnpj_empty(self):
        with pytest.raises(ValueError, match='CNPJ deve ter 14 dígitos'):
            Cnpj('')

    def test_cnpj_str(self):
        assert str(Cnpj('11444777000101')) == '11.444.777/0001-01'


class TestCep:
    def test_valid_cep(self):
        cep = Cep('01310-100')
        assert cep.formatted() == '01310-100'

    def test_cep_only_digits(self):
        cep = Cep('01310100')
        assert cep.formatted() == '01310-100'

    def test_cep_too_short(self):
        with pytest.raises(ValueError, match='CEP deve ter 8 dígitos'):
            Cep('01310-10')

    def test_cep_too_long(self):
        with pytest.raises(ValueError, match='CEP deve ter 8 dígitos'):
            Cep('01310-1000')

    def test_cep_empty(self):
        with pytest.raises(ValueError, match='CEP deve ter 8 dígitos'):
            Cep('')

    def test_cep_str(self):
        assert str(Cep('01310100')) == '01310-100'


class TestEmail:
    def test_valid_email(self):
        email = Email('user@example.com')
        assert str(email) == 'user@example.com'

    def test_email_with_plus(self):
        email = Email('user+tag@example.co.uk')
        assert str(email) == 'user+tag@example.co.uk'

    def test_email_without_at(self):
        with pytest.raises(ValueError, match='Email inválido'):
            Email('userexample.com')

    def test_email_without_domain(self):
        with pytest.raises(ValueError, match='Email inválido'):
            Email('user@')

    def test_email_empty(self):
        with pytest.raises(ValueError, match='Email inválido'):
            Email('')


class TestPhone:
    def test_mobile_formatted(self):
        phone = Phone('11999999999')
        assert phone.formatted() == '(11) 99999-9999'

    def test_landline_formatted(self):
        phone = Phone('1133334444')
        assert phone.formatted() == '(11) 3333-4444'

    def test_phone_with_punctuation(self):
        phone = Phone('(11) 99999-9999')
        assert phone.formatted() == '(11) 99999-9999'

    def test_phone_short_number(self):
        phone = Phone('123')
        assert phone.formatted() == '123'

    def test_phone_str(self):
        phone = Phone('11999999999')
        assert str(phone) == '(11) 99999-9999'


class TestPersonName:
    def test_full_name(self):
        name = PersonName(given_name='João', family_name='Silva')
        assert name.full_name() == 'João Silva'

    def test_full_name_empty_family(self):
        name = PersonName(given_name='João', family_name='')
        assert name.full_name() == 'João'

    def test_str(self):
        name = PersonName(given_name='Maria', family_name='Souza')
        assert str(name) == 'Maria Souza'


class TestCorporateName:
    def test_str_uses_trade_name(self):
        name = CorporateName(legal_name='ABC Ltda', trade_name='ABC')
        assert str(name) == 'ABC'

    def test_str_fallsback_to_legal_name(self):
        name = CorporateName(legal_name='ABC Ltda')
        assert str(name) == 'ABC Ltda'


class TestPartyId:
    def test_generate_returns_uuid(self):
        pid = PartyId.generate()
        assert len(str(pid)) == 36
        assert '-' in str(pid)

    def test_generate_unique(self):
        ids = {PartyId.generate() for _ in range(100)}
        assert len(ids) == 100

    def test_from_string(self):
        pid = PartyId.from_string('custom-id-123')
        assert str(pid) == 'custom-id-123'


class TestDateRange:
    def test_is_active_no_end(self):
        dr = DateRange(start=date(2020, 1, 1))
        assert dr.is_active() is True

    def test_is_active_within_range(self):
        dr = DateRange(start=date(2020, 1, 1), end=date(2030, 12, 31))
        assert dr.is_active() is True

    def test_is_active_expired(self):
        dr = DateRange(start=date(2020, 1, 1), end=date(2020, 12, 31))
        assert dr.is_active() is False

    def test_str_with_end(self):
        dr = DateRange(start=date(2024, 1, 1), end=date(2024, 12, 31))
        assert 'a' in str(dr)
        assert '2024-01-01' in str(dr)

    def test_str_without_end(self):
        dr = DateRange(start=date(2024, 1, 1))
        assert 'desde' in str(dr)


class TestMoney:
    def test_str_format(self):
        m = Money(amount=Decimal('150.50'))
        assert str(m) == 'BRL 150.50'

    def test_str_zero(self):
        m = Money(amount=Decimal('0'))
        assert str(m) == 'BRL 0.00'

    def test_custom_currency(self):
        m = Money(amount=Decimal('100'), currency='USD')
        assert str(m) == 'USD 100.00'
