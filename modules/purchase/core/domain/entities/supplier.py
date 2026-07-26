from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class SupplierStatus(Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    BLOCKED = 'blocked'
    PENDING = 'pending'


@dataclass
class SupplierContact:
    name: str = ''
    email: str = ''
    phone: str = ''
    role: str = ''
    is_main: bool = False


@dataclass
class SupplierCategory:
    code: str
    name: str = ''
    description: str = ''


@dataclass
class Supplier:
    name: str
    document: str = ''
    document_type: str = 'cnpj'
    email: str = ''
    phone: str = ''
    website: str = ''

    address_street: str = ''
    address_number: str = ''
    address_complement: str = ''
    address_neighborhood: str = ''
    address_city: str = ''
    address_state: str = ''
    address_zip: str = ''
    address_country: str = 'BR'

    contacts: list = None
    categories: list = None
    payment_methods: list = None

    status: SupplierStatus = SupplierStatus.PENDING
    rating: float = 0.0
    delivery_avg_days: int = 0
    notes: str = ''

    created_at: datetime = None
    updated_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.contacts is None:
            self.contacts = []
        if self.categories is None:
            self.categories = []
        if self.payment_methods is None:
            self.payment_methods = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

    def block(self):
        self.status = SupplierStatus.BLOCKED
        self.updated_at = datetime.now()

    def activate(self):
        self.status = SupplierStatus.ACTIVE
        self.updated_at = datetime.now()
