from dataclasses import dataclass, field
from datetime import datetime
from modules.product.domain.value_objects.product_id import ProductId
from modules.product.domain.entities.product import ProductType


@dataclass
class ProductCreated:
    product_id: ProductId
    name: str
    product_type: ProductType
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass
class ProductUpdated:
    product_id: ProductId
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass
class ProductActivated:
    product_id: ProductId
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass
class ProductInactivated:
    product_id: ProductId
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass
class ProductArchived:
    product_id: ProductId
    occurred_at: datetime = field(default_factory=datetime.now)
