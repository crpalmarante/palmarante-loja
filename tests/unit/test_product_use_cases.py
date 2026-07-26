import pytest
from modules.product.domain.entities.product import ProductType, ProductUnit
from modules.product.domain.value_objects.product_id import ProductId
from modules.product.infrastructure.postgres.memory_repository import InMemoryProductRepository

from modules.product.application.commands.product_commands import (
    CreateProduct, UpdateProduct, ActivateProduct, DeactivateProduct, ArchiveProduct,
)
from modules.product.application.use_cases.create_product import CreateProductUseCase
from modules.product.application.use_cases.update_product import UpdateProductUseCase
from modules.product.application.use_cases.activate_product import ActivateProductUseCase


@pytest.fixture
def repo():
    return InMemoryProductRepository()


@pytest.fixture
def create_uc(repo):
    return CreateProductUseCase(repo)


@pytest.fixture
def update_uc(repo):
    return UpdateProductUseCase(repo)


@pytest.fixture
def activate_uc(repo):
    return ActivateProductUseCase(repo)


def create_product(create_uc, **overrides) -> ProductId:
    kwargs = dict(
        name='Produto Teste',
        product_type=ProductType.PRODUCT,
        sale_price=100.0,
    )
    kwargs.update(overrides)
    product = create_uc.execute(CreateProduct(**kwargs))
    return product.id


class TestCreateProduct:
    def test_create_basic(self, create_uc):
        p = create_uc.execute(CreateProduct(name='Notebook'))
        assert p.name == 'Notebook'
        assert p.status.value == 'active'

    def test_create_with_sku(self, create_uc):
        p = create_uc.execute(CreateProduct(name='Mouse', sku='MSE-001'))
        assert str(p.sku) == 'MSE-001'

    def test_create_with_ncm(self, create_uc):
        p = create_uc.execute(CreateProduct(name='Teclado', ncm='84713000'))
        assert str(p.ncm) == '8471.30.00'

    def test_create_with_prices(self, create_uc):
        p = create_uc.execute(CreateProduct(name='Monitor', cost_price=500, sale_price=899.90))
        assert p.cost_price == 500
        assert p.sale_price == 899.90

    def test_create_fires_event(self, create_uc):
        create_uc.events.clear()
        p = create_uc.execute(CreateProduct(name='Test'))
        assert len(create_uc.events) == 1
        assert str(create_uc.events[0].product_id) == str(p.id)

    def test_create_service(self, create_uc):
        p = create_uc.execute(CreateProduct(name='Consultoria', product_type=ProductType.SERVICE))
        assert p.product_type == ProductType.SERVICE

    def test_create_with_category(self, create_uc):
        p = create_uc.execute(CreateProduct(name='Celular', category_name='Eletrônicos'))
        assert p.category.name == 'Eletrônicos'


class TestUpdateProduct:
    def test_update_name(self, repo, create_uc, update_uc):
        pid = create_product(create_uc)
        update_uc.execute(UpdateProduct(product_id=pid, name='Notebook Updated'))
        assert repo.find_by_id(pid).name == 'Notebook Updated'

    def test_update_price(self, repo, create_uc, update_uc):
        pid = create_product(create_uc)
        update_uc.execute(UpdateProduct(product_id=pid, sale_price=150.0))
        assert repo.find_by_id(pid).sale_price == 150.0

    def test_update_sku(self, repo, create_uc, update_uc):
        pid = create_product(create_uc)
        update_uc.execute(UpdateProduct(product_id=pid, sku='NEW-SKU'))
        assert str(repo.find_by_id(pid).sku) == 'NEW-SKU'

    def test_update_nonexistent_raises(self, update_uc):
        with pytest.raises(ValueError, match='Product not found'):
            update_uc.execute(UpdateProduct(
                product_id=ProductId.generate(),
                name='Test',
            ))


class TestActivateProduct:
    def test_deactivate(self, repo, create_uc, activate_uc):
        pid = create_product(create_uc)
        activate_uc.deactivate(DeactivateProduct(product_id=pid))
        assert repo.find_by_id(pid).status.value == 'inactive'

    def test_reactivate(self, repo, create_uc, activate_uc):
        pid = create_product(create_uc)
        activate_uc.deactivate(DeactivateProduct(product_id=pid))
        activate_uc.activate(ActivateProduct(product_id=pid))
        assert repo.find_by_id(pid).status.value == 'active'

    def test_archive(self, repo, create_uc, activate_uc):
        pid = create_product(create_uc)
        activate_uc.archive(ArchiveProduct(product_id=pid))
        assert repo.find_by_id(pid).status.value == 'archived'

    def test_nonexistent_raises(self, activate_uc):
        with pytest.raises(ValueError, match='Product not found'):
            activate_uc.activate(ActivateProduct(product_id=ProductId.generate()))

    def test_fires_events(self, repo, create_uc, activate_uc):
        pid = create_product(create_uc)
        activate_uc.events.clear()
        activate_uc.deactivate(DeactivateProduct(product_id=pid))
        assert len(activate_uc.events) == 1
        assert 'Inactivated' in type(activate_uc.events[0]).__name__
