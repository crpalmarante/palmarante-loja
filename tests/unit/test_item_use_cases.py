import pytest
from modules.item.domain.entities.item import ItemType
from modules.item.domain.entities.barcode import BarcodeType
from modules.item.domain.value_objects.item_id import ItemId
from modules.item.infrastructure.postgres.memory_repository import InMemoryItemRepository
from modules.item.application.commands.item_commands import (
    CreateItem, UpdateItem, ActivateItem, DeactivateItem, ArchiveItem,
    ChangePrice, AddBarcode, AddVariant,
)
from modules.item.application.use_cases.create_item import CreateItemUseCase
from modules.item.application.use_cases.update_item import UpdateItemUseCase
from modules.item.application.use_cases.activate_item import ActivateItemUseCase
from modules.item.application.use_cases.change_price import ChangePriceUseCase
from modules.item.application.use_cases.add_barcode import AddBarcodeUseCase
from modules.item.application.use_cases.add_variant import AddVariantUseCase


@pytest.fixture
def repo():
    return InMemoryItemRepository()


@pytest.fixture
def create_uc(repo): return CreateItemUseCase(repo)


@pytest.fixture
def update_uc(repo): return UpdateItemUseCase(repo)


@pytest.fixture
def activate_uc(repo): return ActivateItemUseCase(repo)


@pytest.fixture
def price_uc(repo): return ChangePriceUseCase(repo)


@pytest.fixture
def barcode_uc(repo): return AddBarcodeUseCase(repo)


@pytest.fixture
def variant_uc(repo): return AddVariantUseCase(repo)


class TestCreateItem:
    def test_basic(self, create_uc):
        i = create_uc.execute(CreateItem(name='Notebook'))
        assert i.name == 'Notebook' and i.status.value == 'active'

    def test_with_type(self, create_uc):
        i = create_uc.execute(CreateItem(name='Svc', item_type=ItemType.SERVICE))
        assert i.item_type == ItemType.SERVICE

    def test_with_ncm_cest(self, create_uc):
        i = create_uc.execute(CreateItem(name='X', ncm='84713000', cest='2801000'))
        assert str(i.ncm) == '8471.30.00'

    def test_fires_event(self, create_uc):
        create_uc.events.clear()
        create_uc.execute(CreateItem(name='X'))
        assert len(create_uc.events) == 1


class TestChangePrice:
    def test_change_price(self, repo, create_uc, price_uc):
        pid = create_uc.execute(CreateItem(name='X', cost_price=10, sale_price=20)).id
        price_uc.execute(ChangePrice(item_id=pid, cost_price=15, sale_price=25, reason='Rev'))
        item = repo.find_by_id(pid)
        assert item.cost_price == 15
        assert item.sale_price == 25
        assert len(item.price_history) == 1

    def test_nonexistent_raises(self, price_uc):
        with pytest.raises(ValueError, match='Item not found'):
            price_uc.execute(ChangePrice(item_id=ItemId.generate(), sale_price=100))


class TestAddBarcode:
    def test_add_barcode(self, repo, create_uc, barcode_uc):
        pid = create_uc.execute(CreateItem(name='X')).id
        barcode_uc.execute(AddBarcode(item_id=pid, code='5901234123457', is_main=True))
        item = repo.find_by_id(pid)
        assert len(item.barcodes) == 1
        assert item.main_barcode == '5901234123457'


class TestAddVariant:
    def test_add_variant(self, repo, create_uc, variant_uc):
        pid = create_uc.execute(CreateItem(name='X')).id
        variant_uc.execute(AddVariant(item_id=pid, name='Pequeno', sku='VAR-001'))
        item = repo.find_by_id(pid)
        assert len(item.variants) == 1
        assert item.variants[0].name == 'Pequeno'
