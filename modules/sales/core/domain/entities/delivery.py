from dataclasses import dataclass, field
from datetime import datetime
from modules.sales.core.domain.value_objects.sales_status import DeliveryStatus


@dataclass
class DeliveryItem:
    item_id: str
    item_name: str = ''
    quantity: float = 0
    picked: float = 0
    shipped: float = 0
    unit: str = 'UN'


@dataclass
class Delivery:
    document_id: str
    document_number: str = ''
    carrier: str = ''
    tracking_code: str = ''
    status: DeliveryStatus = DeliveryStatus.PENDING
    items: list = None
    origin_warehouse: str = ''
    destination: str = ''
    notes: str = ''
    shipped_at: datetime = None
    delivered_at: datetime = None
    created_by: str = ''
    created_at: datetime = None
    updated_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.items is None:
            self.items = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

    def ship(self, tracking: str = ''):
        self.status = DeliveryStatus.SHIPPED
        self.tracking_code = tracking or self.tracking_code
        self.shipped_at = datetime.now()
        self.updated_at = datetime.now()

    def deliver(self):
        self.status = DeliveryStatus.DELIVERED
        self.delivered_at = datetime.now()
        self.updated_at = datetime.now()
