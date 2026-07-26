from datetime import datetime
from modules.product.domain.entities.product import Product
from modules.product.domain.value_objects.product_id import ProductId
from modules.product.domain.repositories.product_repository import ProductRepository


class InMemoryProductRepository(ProductRepository):
    def __init__(self):
        self._products: dict[str, Product] = {}

    def save(self, product: Product) -> Product:
        self._products[str(product.id)] = product
        return product

    def find_by_id(self, product_id: ProductId) -> Product | None:
        return self._products.get(str(product_id))

    def find_all(self, query: str = '', status: str = '',
                 product_type: str = '', category: str = '',
                 offset: int = 0, limit: int = 50) -> list[Product]:
        results = list(self._products.values())

        if query:
            q = query.lower()
            results = [p for p in results if q in p.name.lower()
                       or (p.has_sku and q in str(p.sku).lower())
                       or (p.has_ean and q in str(p.ean))]

        if status:
            results = [p for p in results if p.status.value == status]

        if product_type:
            results = [p for p in results if p.product_type.value == product_type]

        if category:
            c = category.lower()
            results = [p for p in results if p.category and c in p.category.name.lower()]

        results.sort(key=lambda p: p.created_at, reverse=True)
        return results[offset:offset + limit]

    def count(self, query: str = '', status: str = '',
              product_type: str = '', category: str = '') -> int:
        return len(self.find_all(query, status, product_type, category))

    def delete(self, product_id: ProductId) -> None:
        self._products.pop(str(product_id), None)
