from abc import ABC, abstractmethod
from modules.product.domain.entities.product import Product
from modules.product.domain.value_objects.product_id import ProductId


class ProductRepository(ABC):

    @abstractmethod
    def save(self, product: Product) -> Product:
        pass

    @abstractmethod
    def find_by_id(self, product_id: ProductId) -> Product | None:
        pass

    @abstractmethod
    def find_all(self, query: str = '', status: str = '',
                 product_type: str = '', category: str = '',
                 offset: int = 0, limit: int = 50) -> list[Product]:
        pass

    @abstractmethod
    def count(self, query: str = '', status: str = '',
              product_type: str = '', category: str = '') -> int:
        pass

    @abstractmethod
    def delete(self, product_id: ProductId) -> None:
        pass
