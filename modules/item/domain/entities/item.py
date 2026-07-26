from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from decimal import Decimal

from modules.item.domain.value_objects.item_id import ItemId
from modules.item.domain.value_objects.sku import Sku
from modules.item.domain.value_objects.ncm import Ncm
from modules.item.domain.value_objects.ean import Ean
from modules.item.domain.value_objects.cest import Cest
from modules.item.domain.value_objects.gtin import Gtin
from modules.item.domain.value_objects.weight import Weight
from modules.item.domain.value_objects.dimension import Dimension
from modules.item.domain.value_objects.volume import Volume
from modules.item.domain.entities.barcode import ItemBarcode
from modules.item.domain.entities.variant import ItemVariant
from modules.item.domain.entities.price_history import PriceHistory


class ItemStatus(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    ARCHIVED = 'archived'


class ItemType(str, Enum):
    PRODUCT = 'product'
    SERVICE = 'service'
    KIT = 'kit'
    COMBO = 'combo'
    RAW_MATERIAL = 'raw_material'
    FINISHED = 'finished'
    ASSET = 'asset'
    EXPENSE = 'expense'
    FISCAL_ITEM = 'fiscal_item'


class ItemUnit(str, Enum):
    UNIT = 'unit'
    KG = 'kg'
    G = 'g'
    L = 'l'
    ML = 'ml'
    M = 'm'
    M2 = 'm2'
    M3 = 'm3'
    PC = 'pc'
    CX = 'cx'
    SERVICE = 'sv'
    OTHER = 'other'


@dataclass
class Item:
    id: ItemId
    name: str
    item_type: ItemType = ItemType.PRODUCT
    sku: Sku | None = None
    ncm: Ncm | None = None
    cest: Cest | None = None
    ean: Ean | None = None
    gtin: Gtin | None = None
    unit: ItemUnit = ItemUnit.UNIT
    cost_price: float = 0.0
    sale_price: float = 0.0
    category_id: str | None = None
    supplier_id: str | None = None
    brand: str = ''
    weight: Weight | None = None
    dimension: Dimension | None = None
    volume: Volume | None = None
    barcodes: list[ItemBarcode] = field(default_factory=list)
    variants: list[ItemVariant] = field(default_factory=list)
    price_history: list[PriceHistory] = field(default_factory=list)
    notes: str = ''
    status: ItemStatus = ItemStatus.ACTIVE
    stock: float = 0.0
    min_stock: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def activate(self):
        if self.status == ItemStatus.ARCHIVED:
            raise ValueError('Cannot activate an archived item')
        self.status = ItemStatus.ACTIVE
        self.updated_at = datetime.now()

    def deactivate(self):
        if self.status == ItemStatus.ARCHIVED:
            raise ValueError('Cannot deactivate an archived item')
        self.status = ItemStatus.INACTIVE
        self.updated_at = datetime.now()

    def archive(self):
        self.status = ItemStatus.ARCHIVED
        self.updated_at = datetime.now()

    def update_price(self, cost: float | None = None, sale: float | None = None, reason: str = ''):
        old_cost = self.cost_price
        old_sale = self.sale_price
        if cost is not None:
            self.cost_price = cost
        if sale is not None:
            self.sale_price = sale
        if cost is not None or sale is not None:
            self.price_history.append(PriceHistory(
                cost_price=old_cost if cost is not None else self.cost_price,
                sale_price=old_sale if sale is not None else self.sale_price,
                reason=reason,
            ))
        self.updated_at = datetime.now()

    def adjust_stock(self, quantity: float):
        self.stock += quantity
        self.updated_at = datetime.now()

    def add_barcode(self, barcode: ItemBarcode):
        if barcode.is_main:
            for b in self.barcodes:
                b.is_main = False
        self.barcodes.append(barcode)
        self.updated_at = datetime.now()

    def add_variant(self, variant: ItemVariant):
        self.variants.append(variant)
        self.updated_at = datetime.now()

    @property
    def has_ncm(self) -> bool:
        return self.ncm is not None

    @property
    def has_ean(self) -> bool:
        return self.ean is not None

    @property
    def has_sku(self) -> bool:
        return self.sku is not None

    @property
    def has_cest(self) -> bool:
        return self.cest is not None

    @property
    def main_barcode(self) -> str:
        for b in self.barcodes:
            if b.is_main:
                return b.code
        return str(self.ean) if self.ean else ''
