from datetime import datetime
from modules.product.domain.entities.product import Product
from modules.product.domain.entities.category import Category
from modules.product.domain.value_objects.sku import Sku
from modules.product.domain.value_objects.ncm import Ncm
from modules.product.domain.value_objects.ean import Ean
from modules.product.domain.events.product_events import ProductUpdated
from modules.product.domain.repositories.product_repository import ProductRepository
from modules.product.application.commands.product_commands import UpdateProduct


class UpdateProductUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository
        self.events: list = []

    def execute(self, cmd: UpdateProduct) -> Product:
        product = self.repository.find_by_id(cmd.product_id)
        if not product:
            raise ValueError(f'Product not found: {cmd.product_id}')

        if cmd.name is not None:
            product.name = cmd.name
        if cmd.sku is not None:
            product.sku = Sku(cmd.sku)
        if cmd.ncm is not None:
            product.ncm = Ncm(cmd.ncm) if cmd.ncm else None
        if cmd.ean is not None:
            product.ean = Ean(cmd.ean) if cmd.ean else None
        if cmd.unit is not None:
            product.unit = cmd.unit
        if cmd.cost_price is not None:
            product.cost_price = cmd.cost_price
        if cmd.sale_price is not None:
            product.sale_price = cmd.sale_price
        if cmd.category_name is not None:
            product.category = Category(name=cmd.category_name) if cmd.category_name else None
        if cmd.supplier_id is not None:
            product.supplier_id = cmd.supplier_id or None
        if cmd.notes is not None:
            product.notes = cmd.notes
        if cmd.min_stock is not None:
            product.min_stock = cmd.min_stock

        product.updated_at = datetime.now()
        self.repository.save(product)
        self.events.append(ProductUpdated(product_id=cmd.product_id))
        return product
