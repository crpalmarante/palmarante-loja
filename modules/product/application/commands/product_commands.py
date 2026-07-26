from dataclasses import dataclass
from modules.product.domain.value_objects.product_id import ProductId
from modules.product.domain.entities.product import ProductType, ProductUnit
from modules.product.domain.value_objects.sku import Sku
from modules.product.domain.value_objects.ncm import Ncm
from modules.product.domain.value_objects.ean import Ean


@dataclass
class CreateProduct:
    name: str
    product_type: ProductType = ProductType.PRODUCT
    sku: str = ''
    ncm: str = ''
    ean: str = ''
    unit: ProductUnit = ProductUnit.UNIT
    cost_price: float = 0.0
    sale_price: float = 0.0
    category_name: str = ''
    supplier_id: str = ''
    notes: str = ''
    stock: float = 0.0
    min_stock: float = 0.0


@dataclass
class UpdateProduct:
    product_id: ProductId
    name: str | None = None
    sku: str | None = None
    ncm: str | None = None
    ean: str | None = None
    unit: ProductUnit | None = None
    cost_price: float | None = None
    sale_price: float | None = None
    category_name: str | None = None
    supplier_id: str | None = None
    notes: str | None = None
    min_stock: float | None = None


@dataclass
class ActivateProduct:
    product_id: ProductId


@dataclass
class DeactivateProduct:
    product_id: ProductId


@dataclass
class ArchiveProduct:
    product_id: ProductId
