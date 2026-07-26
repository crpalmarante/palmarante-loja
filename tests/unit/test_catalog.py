import pytest
from decimal import Decimal
from modules.catalog.domain.entities.category import Category
from modules.catalog.domain.entities.brand import Brand
from modules.catalog.domain.entities.manufacturer import Manufacturer
from modules.catalog.domain.entities.unit import Unit, UnitType
from modules.catalog.domain.entities.unit_conversion import UnitConversion
from modules.catalog.domain.entities.attribute import Attribute, AttributeType
from modules.catalog.domain.entities.attribute_value import AttributeValue
from modules.catalog.domain.entities.variant import Variant
from modules.catalog.infrastructure.postgres.memory_repository import InMemoryCatalogRepository


class TestCategory:
    def test_create(self):
        c = Category(name='Eletrônicos')
        assert c.name == 'Eletrônicos'
    def test_subcategory(self):
        c = Category(name='Celulares', parent_id='cat-eletro')
        assert c.parent_id == 'cat-eletro'
    def test_path(self):
        c = Category(name='Celulares', parent_id='Eletrônicos')
        assert c.path == ['Eletrônicos', 'Celulares']


class TestBrand:
    def test_create(self):
        b = Brand(name='Dell', code='DELL')
        assert b.name == 'Dell' and b.code == 'DELL'


class TestManufacturer:
    def test_create(self):
        m = Manufacturer(name='Foxconn', cnpj='11444777000101')
        assert m.name == 'Foxconn'


class TestUnit:
    def test_create(self):
        u = Unit(code='KG', name='Quilograma', type=UnitType.WEIGHT)
        assert u.code == 'KG' and u.type == UnitType.WEIGHT


class TestUnitConversion:
    def test_convert(self):
        c = UnitConversion(from_code='KG', to_code='G', factor=Decimal('1000'))
        assert c.convert(Decimal('2.5')) == Decimal('2500')
    def test_reverse(self):
        c = UnitConversion(from_code='CX', to_code='UN', factor=Decimal('12'))
        assert c.convert(Decimal('3')) == Decimal('36')


class TestAttribute:
    def test_create(self):
        a = Attribute(name='Cor', type=AttributeType.COLOR)
        assert a.name == 'Cor'


class TestAttributeValue:
    def test_create(self):
        v = AttributeValue(attribute_id='a1', value='Azul')
        assert v.value == 'Azul' and v.attribute_id == 'a1'


class TestVariant:
    def test_create(self):
        v = Variant(item_id='i1', sku='CAM-AZ-P', attribute_values={'Cor': 'Azul', 'Tamanho': 'P'})
        assert v.display_name == 'Cor: Azul / Tamanho: P'
    def test_display_name_uses_name(self):
        v = Variant(item_id='i1', name='Camiseta Azul P')
        assert v.display_name == 'Camiseta Azul P'


class TestCatalogRepository:
    @pytest.fixture
    def repo(self):
        return InMemoryCatalogRepository()

    def test_categories(self, repo):
        c = Category(name='Eletrônicos')
        repo.save_category(c)
        assert repo.find_all_categories() != []
        assert repo.find_category_by_id(c._id).name == 'Eletrônicos'

    def test_brands(self, repo):
        repo.save_brand(Brand(name='Dell'))
        assert len(repo.find_all_brands()) == 1
        assert len(repo.find_all_brands(query='dell')) == 1

    def test_units(self, repo):
        repo.save_unit(Unit(code='KG', name='Quilo'))
        assert repo.find_all_units() != []
        assert repo.find_all_units()[0].code == 'KG'

    def test_conversions(self, repo):
        repo.save_conversion(UnitConversion(from_code='KG', to_code='G', factor=Decimal('1000')))
        c = repo.find_conversion('KG', 'G')
        assert c is not None and c.convert(Decimal('1')) == Decimal('1000')

    def test_attributes(self, repo):
        a = Attribute(name='Cor')
        repo.save_attribute(a)
        repo.save_attribute_value(AttributeValue(attribute_id=a._id, value='Azul'))
        repo.save_attribute_value(AttributeValue(attribute_id=a._id, value='Preto'))
        assert len(repo.find_values_by_attribute(a._id)) == 2

    def test_variants(self, repo):
        repo.save_variant(Variant(item_id='i1', sku='CAM-AZ'))
        repo.save_variant(Variant(item_id='i1', sku='CAM-PT'))
        assert len(repo.find_variants_by_item('i1')) == 2
