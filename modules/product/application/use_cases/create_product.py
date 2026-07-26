from modules.product.domain.entities.product import Product, ProductType
from modules.product.domain.entities.category import Category
from modules.product.domain.value_objects.product_id import ProductId
from modules.product.domain.value_objects.sku import Sku
from modules.product.domain.value_objects.ncm import Ncm
from modules.product.domain.value_objects.ean import Ean
from modules.product.domain.events.product_events import ProductCreated
from modules.product.domain.repositories.product_repository import ProductRepository
from modules.product.application.commands.product_commands import CreateProduct


class CreateProductUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository
        self.events: list = []

    def execute(self, cmd: CreateProduct) -> Product:
        product_id = ProductId.generate()

        sku = Sku(cmd.sku) if cmd.sku else None
        ncm = Ncm(cmd.ncm) if cmd.ncm else None
        ean = Ean(cmd.ean) if cmd.ean else None
        category = Category(name=cmd.category_name) if cmd.category_name else None

        product = Product(
            id=product_id,
            name=cmd.name,
            product_type=cmd.product_type,
            sku=sku,
            ncm=ncm,
            ean=ean,
            unit=cmd.unit,
            cost_price=cmd.cost_price,
            sale_price=cmd.sale_price,
            category=category,
            supplier_id=cmd.supplier_id or None,
            notes=cmd.notes,
            stock=cmd.stock,
            min_stock=cmd.min_stock,
        )

        self.repository.save(product)
        self.events.append(ProductCreated(
            product_id=product_id,
            name=cmd.name,
            product_type=cmd.product_type,
        ))
        return product
