import pytest
from modules.product.domain.value_objects.sku import Sku
from modules.product.domain.value_objects.ncm import Ncm
from modules.product.domain.value_objects.ean import Ean
from modules.product.domain.value_objects.product_id import ProductId


class TestSku:
    def test_valid_sku(self):
        sku = Sku('ABC-123')
        assert str(sku) == 'ABC-123'

    def test_sku_empty_raises(self):
        with pytest.raises(ValueError, match='SKU não pode ser vazio'):
            Sku('')

    def test_sku_whitespace_raises(self):
        with pytest.raises(ValueError, match='SKU não pode ser vazio'):
            Sku('   ')

    def test_sku_too_long_raises(self):
        with pytest.raises(ValueError, match='SKU muito longo'):
            Sku('A' * 51)


class TestNcm:
    def test_valid_ncm(self):
        ncm = Ncm('8471.30.00')
        assert ncm.formatted() == '8471.30.00'

    def test_ncm_only_digits(self):
        ncm = Ncm('84713000')
        assert ncm.formatted() == '8471.30.00'

    def test_ncm_too_short_raises(self):
        with pytest.raises(ValueError, match='NCM deve ter 8 dígitos'):
            Ncm('8471.30.0')

    def test_ncm_empty_raises(self):
        with pytest.raises(ValueError, match='NCM deve ter 8 dígitos'):
            Ncm('')

    def test_ncm_str(self):
        assert str(Ncm('84713000')) == '8471.30.00'


class TestEan:
    def test_valid_ean_13(self):
        ean = Ean('5901234123457')
        assert ean.formatted() == '5901234123457'

    def test_valid_ean_8(self):
        ean = Ean('12345670')
        assert ean.formatted() == '12345670'

    def test_ean_invalid_length_raises(self):
        with pytest.raises(ValueError, match='EAN deve ter 8 ou 13 dígitos'):
            Ean('12345')

    def test_ean_empty_raises(self):
        with pytest.raises(ValueError, match='EAN deve ter 8 ou 13 dígitos'):
            Ean('')

    def test_ean_with_punctuation(self):
        ean = Ean('5901234123457')
        assert str(ean) == '5901234123457'


class TestProductId:
    def test_generate_returns_uuid(self):
        pid = ProductId.generate()
        assert len(str(pid)) == 36

    def test_from_string(self):
        pid = ProductId.from_string('abc-123')
        assert str(pid) == 'abc-123'
