from abc import ABC, abstractmethod
from modules.catalog.domain.entities.category import Category
from modules.catalog.domain.entities.brand import Brand
from modules.catalog.domain.entities.manufacturer import Manufacturer
from modules.catalog.domain.entities.unit import Unit
from modules.catalog.domain.entities.unit_conversion import UnitConversion
from modules.catalog.domain.entities.attribute import Attribute
from modules.catalog.domain.entities.attribute_value import AttributeValue
from modules.catalog.domain.entities.variant import Variant
from modules.catalog.domain.entities.fiscal_classification import FiscalClassification


class CatalogRepository(ABC):

    @abstractmethod
    def save_category(self, cat: Category) -> Category: pass
    @abstractmethod
    def find_category_by_id(self, cat_id: str) -> Category | None: pass
    @abstractmethod
    def find_all_categories(self, query: str = '', active: bool | None = None) -> list[Category]: pass
    @abstractmethod
    def find_categories_by_parent(self, parent_id: str) -> list[Category]: pass

    @abstractmethod
    def save_brand(self, brand: Brand) -> Brand: pass
    @abstractmethod
    def find_all_brands(self, query: str = '', active: bool | None = None) -> list[Brand]: pass

    @abstractmethod
    def save_manufacturer(self, m: Manufacturer) -> Manufacturer: pass
    @abstractmethod
    def find_all_manufacturers(self, query: str = '') -> list[Manufacturer]: pass

    @abstractmethod
    def save_unit(self, unit: Unit) -> Unit: pass
    @abstractmethod
    def find_all_units(self, active: bool | None = None) -> list[Unit]: pass

    @abstractmethod
    def save_conversion(self, conv: UnitConversion) -> UnitConversion: pass
    @abstractmethod
    def find_conversion(self, from_code: str, to_code: str) -> UnitConversion | None: pass

    @abstractmethod
    def save_attribute(self, attr: Attribute) -> Attribute: pass
    @abstractmethod
    def find_all_attributes(self, active: bool | None = None) -> list[Attribute]: pass

    @abstractmethod
    def save_attribute_value(self, val: AttributeValue) -> AttributeValue: pass
    @abstractmethod
    def find_values_by_attribute(self, attr_id: str) -> list[AttributeValue]: pass

    @abstractmethod
    def save_variant(self, variant: Variant) -> Variant: pass
    @abstractmethod
    def find_variants_by_item(self, item_id: str) -> list[Variant]: pass
