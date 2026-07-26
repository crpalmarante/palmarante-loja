from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class DeliveryTermCode(str, Enum):
    CIF = 'cif'
    FOB = 'fob'
    STORE_PICKUP = 'store_pickup'
    CARRIER = 'carrier'
    OWN_DELIVERY = 'own_delivery'


@dataclass
class DeliveryTerm:
    name: str
    code: DeliveryTermCode = DeliveryTermCode.FOB
    description: str = ''
    carrier_required: bool = True
    address_required: bool = True
    active: bool = True
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
