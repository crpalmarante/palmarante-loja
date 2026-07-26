from modules.product.domain.events.product_events import ProductActivated, ProductInactivated, ProductArchived
from modules.product.domain.repositories.product_repository import ProductRepository
from modules.product.application.commands.product_commands import ActivateProduct, DeactivateProduct, ArchiveProduct


class ActivateProductUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository
        self.events: list = []

    def activate(self, cmd: ActivateProduct) -> None:
        product = self.repository.find_by_id(cmd.product_id)
        if not product:
            raise ValueError(f'Product not found: {cmd.product_id}')
        product.activate()
        self.repository.save(product)
        self.events.append(ProductActivated(product_id=cmd.product_id))

    def deactivate(self, cmd: DeactivateProduct) -> None:
        product = self.repository.find_by_id(cmd.product_id)
        if not product:
            raise ValueError(f'Product not found: {cmd.product_id}')
        product.deactivate()
        self.repository.save(product)
        self.events.append(ProductInactivated(product_id=cmd.product_id))

    def archive(self, cmd: ArchiveProduct) -> None:
        product = self.repository.find_by_id(cmd.product_id)
        if not product:
            raise ValueError(f'Product not found: {cmd.product_id}')
        product.archive()
        self.repository.save(product)
        self.events.append(ProductArchived(product_id=cmd.product_id))
