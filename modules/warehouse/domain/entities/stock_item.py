from dataclasses import dataclass


@dataclass
class StockItem:
    warehouse_id: str
    item_id: str
    quantity: float = 0.0
    reserved: float = 0.0
    min_stock: float = 0.0
    max_stock: float = 0.0
    location: str = ''
    _id: str = ''

    @property
    def available(self) -> float:
        return self.quantity - self.reserved
