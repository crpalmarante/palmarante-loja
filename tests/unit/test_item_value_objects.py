import pytest
from decimal import Decimal
from modules.item.domain.value_objects.sku import Sku
from modules.item.domain.value_objects.ncm import Ncm
from modules.item.domain.value_objects.cest import Cest
from modules.item.domain.value_objects.ean import Ean
from modules.item.domain.value_objects.gtin import Gtin
from modules.item.domain.value_objects.item_id import ItemId
from modules.item.domain.value_objects.weight import Weight
from modules.item.domain.value_objects.dimension import Dimension
from modules.item.domain.value_objects.volume import Volume


class TestSku:
    def test_valid(self):
        assert str(Sku('ABC-123')) == 'ABC-123'
    def test_empty_raises(self):
        with pytest.raises(ValueError): Sku('')


class TestNcm:
    def test_valid(self):
        assert Ncm('8471.30.00').formatted() == '8471.30.00'
    def test_short_raises(self):
        with pytest.raises(ValueError): Ncm('123')


class TestCest:
    def test_valid(self):
        assert Cest('28.010.00').formatted() == '28.010.00'
    def test_only_digits(self):
        assert Cest('2801000').formatted() == '28.010.00'
    def test_short_raises(self):
        with pytest.raises(ValueError, match='CEST deve ter 7 dígitos'): Cest('123')


class TestEan:
    def test_valid_13(self):
        assert Ean('5901234123457').formatted() == '5901234123457'
    def test_valid_8(self):
        assert Ean('12345670').formatted() == '12345670'


class TestGtin:
    def test_valid_8(self): assert Gtin('12345670').formatted() == '12345670'
    def test_valid_13(self): assert Gtin('5901234123457').formatted() == '5901234123457'
    def test_valid_14(self): assert Gtin('59012341234570').formatted() == '59012341234570'
    def test_invalid_raises(self):
        with pytest.raises(ValueError, match='GTIN deve ter'): Gtin('123')


class TestWeight:
    def test_positive(self):
        w = Weight(Decimal('1.5'))
        assert str(w) == '1.500 kg'
    def test_negative_raises(self):
        with pytest.raises(ValueError): Weight(Decimal('-1'))
    def test_to_grams(self):
        assert Weight(Decimal('2'), 'kg').in_grams() == Decimal('2000')
        assert Weight(Decimal('500'), 'g').in_grams() == Decimal('500')


class TestDimension:
    def test_valid(self):
        d = Dimension(Decimal('30'), Decimal('20'), Decimal('10'))
        assert d.volume() == Decimal('6000')
    def test_negative_raises(self):
        with pytest.raises(ValueError): Dimension(Decimal('-1'), Decimal('1'), Decimal('1'))


class TestVolume:
    def test_valid(self):
        v = Volume(Decimal('0.5'))
        assert str(v) == '0.500 m3'
    def test_to_liters(self):
        assert Volume(Decimal('1'), 'm3').in_liters() == Decimal('1000')
        assert Volume(Decimal('500'), 'l').in_liters() == Decimal('500')
