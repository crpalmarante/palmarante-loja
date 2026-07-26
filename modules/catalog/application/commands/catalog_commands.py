from dataclasses import dataclass
from modules.catalog.domain.entities.attribute import AttributeType
from modules.catalog.domain.entities.unit import UnitType


@dataclass
class CreateCategory:
    name: str
    parent_id: str | None = None
    code: str = ''
    description: str = ''


@dataclass
class CreateBrand:
    name: str
    code: str = ''
    description: str = ''


@dataclass
class CreateManufacturer:
    name: str
    cnpj: str = ''
    code: str = ''


@dataclass
class CreateUnit:
    code: str
    name: str
    type: UnitType = UnitType.UNITS


@dataclass
class CreateUnitConversion:
    from_code: str
    to_code: str
    factor: float


@dataclass
class CreateAttribute:
    name: str
    code: str = ''
    type: AttributeType = AttributeType.TEXT
    required: bool = False


@dataclass
class CreateAttributeValue:
    attribute_id: str
    value: str
    code: str = ''
    sort_order: int = 0


@dataclass
class CreateVariant:
    item_id: str
    sku: str = ''
    name: str = ''
    attribute_values: dict | None = None
