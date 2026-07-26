import pytest
from modules.product.domain.entities.product import Product, ProductStatus, ProductType, ProductUnit
from modules.product.domain.entities.category import Category
from modules.product.domain.value_objects.product_id import ProductId
from modules.product.domain.value_objects.sku import Sku
from modules.product.domain.value_objects.ncm import Ncm
from modules.product.domain.value_objects.ean import Ean


def make_product(**kwargs) -> Product:
    defaults = dict(
        id=ProductId.generate(),
        name='Produto Teste',
    )
    defaults.update(kwargs)
    return Product(**defaults)


class TestProductLifecycle:
    def test_create_product(self):
        p = make_product()
        assert p.name == 'Produto Teste'
        assert p.status == ProductStatus.ACTIVE
        assert p.product_type == ProductType.PRODUCT

    def test_create_service(self):
        p = make_product(product_type=ProductType.SERVICE)
        assert p.product_type == ProductType.SERVICE

    def test_activate(self):
        p = make_product()
        p.deactivate()
        assert p.status == ProductStatus.INACTIVE
        p.activate()
        assert p.status == ProductStatus.ACTIVE

    def test_deactivate(self):
        p = make_product()
        p.deactivate()
        assert p.status == ProductStatus.INACTIVE

    def test_archive(self):
        p = make_product()
        p.archive()
        assert p.status == ProductStatus.ARCHIVED

    def test_activate_archived_raises(self):
        p = make_product()
        p.archive()
        with pytest.raises(ValueError, match='Cannot activate an archived product'):
            p.activate()

    def test_deactivate_archived_raises(self):
        p = make_product()
        p.archive()
        with pytest.raises(ValueError, match='Cannot deactivate an archived product'):
            p.deactivate()


class TestProductPrices:
    def test_update_price_cost(self):
        p = make_product(cost_price=10.0, sale_price=20.0)
        p.update_price(cost=15.0)
        assert p.cost_price == 15.0
        assert p.sale_price == 20.0

    def test_update_price_sale(self):
        p = make_product(sale_price=20.0)
        p.update_price(sale=25.0)
        assert p.sale_price == 25.0

    def test_update_price_both(self):
        p = make_product(cost_price=10.0, sale_price=20.0)
        p.update_price(cost=12.0, sale=22.0)
        assert p.cost_price == 12.0
        assert p.sale_price == 22.0


class TestProductStock:
    def test_adjust_stock_positive(self):
        p = make_product(stock=10.0)
        p.adjust_stock(5.0)
        assert p.stock == 15.0

    def test_adjust_stock_negative(self):
        p = make_product(stock=10.0)
        p.adjust_stock(-3.0)
        assert p.stock == 7.0


class TestProductProperties:
    def test_has_sku_true(self):
        p = make_product(sku=Sku('ABC'))
        assert p.has_sku is True

    def test_has_sku_false(self):
        p = make_product()
        assert p.has_sku is False

    def test_has_ncm_true(self):
        p = make_product(ncm=Ncm('84713000'))
        assert p.has_ncm is True

    def test_has_ean_true(self):
        p = make_product(ean=Ean('5901234123457'))
        assert p.has_ean is True


class TestCategory:
    def test_create_category(self):
        c = Category(name='Eletrônicos')
        assert c.name == 'Eletrônicos'
        assert c.active is True

    def test_category_with_parent(self):
        c = Category(name='Celulares', parent_id='cat-eletronicos')
        assert c.parent_id == 'cat-eletronicos'

    def test_category_str(self):
        c = Category(name='Informática')
        assert str(c) == 'Informática'
