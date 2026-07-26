from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class SalesEventType(str, Enum):
    QUOTATION_CREATED = 'quotation_created'
    QUOTATION_APPROVED = 'quotation_approved'
    QUOTATION_CONVERTED = 'quotation_converted'
    ORDER_CREATED = 'order_created'
    ORDER_CONFIRMED = 'order_confirmed'
    ORDER_APPROVED = 'order_approved'
    ORDER_RESERVED = 'order_reserved'
    ORDER_SHIPPED = 'order_shipped'
    ORDER_DELIVERED = 'order_delivered'
    ORDER_INVOICED = 'order_invoiced'
    ORDER_CANCELLED = 'order_cancelled'
    ORDER_COMPLETED = 'order_completed'
    PAYMENT_RECEIVED = 'payment_received'
    CONTRACT_CREATED = 'contract_created'
    CONTRACT_RENEWED = 'contract_renewed'


@dataclass
class SalesEvent:
    event_type: SalesEventType
    document_id: str = ''
    document_number: str = ''
    customer_id: str = ''
    customer_name: str = ''
    total: float = 0.0
    data: dict = None
    created_by: str = ''
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.data is None:
            self.data = {}
        if self.created_at is None:
            self.created_at = datetime.now()
