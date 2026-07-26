from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from modules.product.domain.value_objects.product_id import ProductId
from modules.product.domain.value_objects.sku import Sku
from modules.product.domain.value_objects.ncm import Ncm
from modules.product.domain.value_objects.ean import Ean
from modules.product.domain.entities.category import Category


class ProductStatus(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    ARCHIVED = 'archived'


class ProductType(str, Enum):
    PRODUCT = 'product'
    SERVICE = 'service'


class ProductUnit(str, Enum):
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
    OTHER = 'other'


@dataclass
class Product:
    id: ProductId
    name: str
    product_type: ProductType = ProductType.PRODUCT
    sku: Sku | None = None
    ncm: Ncm | None = None
    ean: Ean | None = None
    unit: ProductUnit = ProductUnit.UNIT
    cost_price: float = 0.0
    sale_price: float = 0.0
    category: Category | None = None
    supplier_id: str | None = None
    notes: str = ''
    status: ProductStatus = ProductStatus.ACTIVE
    stock: float = 0.0
    min_stock: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def activate(self):
        if self.status == ProductStatus.ARCHIVED:
            raise ValueError('Cannot activate an archived product')
        self.status = ProductStatus.ACTIVE
        self.updated_at = datetime.now()

    def deactivate(self):
        if self.status == ProductStatus.ARCHIVED:
            raise ValueError('Cannot deactivate an archived product')
        self.status = ProductStatus.INACTIVE
        self.updated_at = datetime.now()

    def archive(self):
        self.status = ProductStatus.ARCHIVED
        self.updated_at = datetime.now()

    def update_price(self, cost: float | None = None, sale: float | None = None):
        if cost is not None:
            self.cost_price = cost
        if sale is not None:
            self.sale_price = sale
        self.updated_at = datetime.now()

    def adjust_stock(self, quantity: float):
        self.stock += quantity
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
