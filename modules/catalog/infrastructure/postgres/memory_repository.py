from modules.catalog.domain.entities.category import Category
from modules.catalog.domain.entities.brand import Brand
from modules.catalog.domain.entities.manufacturer import Manufacturer
from modules.catalog.domain.entities.unit import Unit
from modules.catalog.domain.entities.unit_conversion import UnitConversion
from modules.catalog.domain.entities.attribute import Attribute
from modules.catalog.domain.entities.attribute_value import AttributeValue
from modules.catalog.domain.entities.variant import Variant
from modules.catalog.domain.entities.fiscal_classification import FiscalClassification
from modules.catalog.domain.repositories.catalog_repository import CatalogRepository


def _match(q: str, *fields) -> bool:
    if not q:
        return True
    ql = q.lower()
    return any(ql in (f or '').lower() for f in fields)


class InMemoryCatalogRepository(CatalogRepository):
    def __init__(self):
        self._categories: dict[str, Category] = {}
        self._brands: dict[str, Brand] = {}
        self._manufacturers: dict[str, Manufacturer] = {}
        self._units: dict[str, Unit] = {}
        self._conversions: list[UnitConversion] = []
        self._attributes: dict[str, Attribute] = {}
        self._attr_values: dict[str, AttributeValue] = {}
        self._variants: list[Variant] = []
        self._ids = 0

    def _next_id(self) -> str:
        self._ids += 1
        return str(self._ids)

    def _store(self, store: dict, entity, id_field='_id'):
        eid = getattr(entity, id_field, None) or self._next_id()
        setattr(entity, id_field, eid)
        store[eid] = entity
        return entity

    # Categories
    def save_category(self, cat: Category) -> Category:
        return self._store(self._categories, cat)
    def find_category_by_id(self, cat_id: str) -> Category | None:
        return self._categories.get(cat_id)
    def find_all_categories(self, query: str = '', active: bool | None = None) -> list[Category]:
        return [c for c in self._categories.values()
                if _match(query, c.name, c.code)
                and (active is None or c.active == active)]
    def find_categories_by_parent(self, parent_id: str) -> list[Category]:
        return [c for c in self._categories.values() if c.parent_id == parent_id]

    # Brands
    def save_brand(self, brand: Brand) -> Brand:
        return self._store(self._brands, brand)
    def find_all_brands(self, query: str = '', active: bool | None = None) -> list[Brand]:
        return [b for b in self._brands.values()
                if _match(query, b.name, b.code)
                and (active is None or b.active == active)]

    # Manufacturers
    def save_manufacturer(self, m: Manufacturer) -> Manufacturer:
        return self._store(self._manufacturers, m)
    def find_all_manufacturers(self, query: str = '') -> list[Manufacturer]:
        return [m for m in self._manufacturers.values() if _match(query, m.name, m.cnpj)]

    # Units
    def save_unit(self, unit: Unit) -> Unit:
        self._units[unit.code] = unit
        return unit
    def find_all_units(self, active: bool | None = None) -> list[Unit]:
        return [u for u in self._units.values() if active is None or u.active == active]

    # Conversions
    def save_conversion(self, conv: UnitConversion) -> UnitConversion:
        self._conversions.append(conv)
        return conv
    def find_conversion(self, from_code: str, to_code: str) -> UnitConversion | None:
        for c in self._conversions:
            if c.from_code == from_code and c.to_code == to_code:
                return c
        return None

    # Attributes
    def save_attribute(self, attr: Attribute) -> Attribute:
        return self._store(self._attributes, attr)
    def find_all_attributes(self, active: bool | None = None) -> list[Attribute]:
        return [a for a in self._attributes.values() if active is None or a.active == active]

    # Attribute values
    def save_attribute_value(self, val: AttributeValue) -> AttributeValue:
        return self._store(self._attr_values, val)
    def find_values_by_attribute(self, attr_id: str) -> list[AttributeValue]:
        return [v for v in self._attr_values.values() if v.attribute_id == attr_id]

    # Variants
    def save_variant(self, variant: Variant) -> Variant:
        self._variants.append(variant)
        return variant
    def find_variants_by_item(self, item_id: str) -> list[Variant]:
        return [v for v in self._variants if v.item_id == item_id]
