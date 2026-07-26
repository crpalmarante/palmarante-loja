from dataclasses import dataclass
from modules.item.domain.value_objects.item_id import ItemId
from modules.item.domain.entities.item import ItemType, ItemUnit
from modules.item.domain.entities.barcode import BarcodeType


@dataclass
class CreateItem:
    name: str
    item_type: ItemType = ItemType.PRODUCT
    sku: str = ''
    ncm: str = ''
    cest: str = ''
    ean: str = ''
    gtin: str = ''
    unit: ItemUnit = ItemUnit.UNIT
    cost_price: float = 0.0
    sale_price: float = 0.0
    category_id: str | None = None
    supplier_id: str = ''
    brand: str = ''
    notes: str = ''
    stock: float = 0.0
    min_stock: float = 0.0


@dataclass
class UpdateItem:
    item_id: ItemId
    name: str | None = None
    sku: str | None = None
    ncm: str | None = None
    cest: str | None = None
    ean: str | None = None
    gtin: str | None = None
    unit: ItemUnit | None = None
    cost_price: float | None = None
    sale_price: float | None = None
    category_id: str | None = None
    supplier_id: str | None = None
    brand: str | None = None
    notes: str | None = None
    min_stock: float | None = None


@dataclass
class ActivateItem:
    item_id: ItemId


@dataclass
class DeactivateItem:
    item_id: ItemId


@dataclass
class ArchiveItem:
    item_id: ItemId


@dataclass
class ChangePrice:
    item_id: ItemId
    cost_price: float | None = None
    sale_price: float | None = None
    reason: str = ''


@dataclass
class AddBarcode:
    item_id: ItemId
    code: str
    barcode_type: BarcodeType = BarcodeType.EAN13
    is_main: bool = False


@dataclass
class AddVariant:
    item_id: ItemId
    name: str
    sku: str = ''
    sale_price: float = 0.0
    cost_price: float = 0.0
    stock: float = 0.0
