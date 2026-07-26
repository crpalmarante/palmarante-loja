from modules.item.domain.entities.item import Item, ItemStatus, ItemType
from modules.item.domain.entities.barcode import ItemBarcode, BarcodeType
from modules.item.domain.entities.variant import ItemVariant
from modules.item.domain.entities.price_history import PriceHistory
from modules.item.domain.value_objects.item_id import ItemId


def make_item(**kw):
    d = dict(id=ItemId.generate(), name='Test')
    d.update(kw)
    return Item(**d)


class TestItemLifecycle:
    def test_create(self):
        i = make_item()
        assert i.name == 'Test' and i.status == ItemStatus.ACTIVE

    def test_service_type(self):
        i = make_item(item_type=ItemType.SERVICE)
        assert i.item_type == ItemType.SERVICE

    def test_activate_deactivate(self):
        i = make_item()
        i.deactivate(); assert i.status == ItemStatus.INACTIVE
        i.activate(); assert i.status == ItemStatus.ACTIVE

    def test_archive(self):
        i = make_item()
        i.archive(); assert i.status == ItemStatus.ARCHIVED


class TestItemPrice:
    def test_update_price_records_history(self):
        i = make_item(cost_price=10, sale_price=20)
        i.update_price(cost=15, sale=25, reason='Aumento')
        assert i.cost_price == 15
        assert i.sale_price == 25
        assert len(i.price_history) == 1
        assert i.price_history[0].reason == 'Aumento'


class TestItemBarcodes:
    def test_add_barcode(self):
        i = make_item()
        i.add_barcode(ItemBarcode(code='1234567890123', is_main=True))
        assert len(i.barcodes) == 1
        assert i.main_barcode == '1234567890123'

    def test_add_barcode_sets_main(self):
        i = make_item()
        i.add_barcode(ItemBarcode(code='111', is_main=True))
        i.add_barcode(ItemBarcode(code='222', is_main=True))
        assert i.barcodes[0].is_main is False
        assert i.barcodes[1].is_main is True


class TestItemVariants:
    def test_add_variant(self):
        i = make_item()
        i.add_variant(ItemVariant(name='Pequeno', sku='VAR-001'))
        assert len(i.variants) == 1
        assert i.variants[0].name == 'Pequeno'
