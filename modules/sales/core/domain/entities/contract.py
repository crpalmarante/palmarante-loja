from dataclasses import dataclass, field
from datetime import datetime
from modules.sales.core.domain.value_objects.sales_status import ContractStatus


@dataclass
class ContractLine:
    item_id: str
    description: str = ''
    quantity: float = 1
    unit_price: float = 0.0
    total: float = 0.0


@dataclass
class Contract:
    customer_id: str
    customer_name: str = ''
    contract_number: str = ''
    title: str = ''
    description: str = ''
    status: ContractStatus = ContractStatus.DRAFT
    start_date: str = ''
    end_date: str = ''
    billing_cycle: str = 'monthly'
    value: float = 0.0
    items: list = None
    renewal_type: str = 'automatic'
    notes: str = ''
    sales_rep: str = ''
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

    def activate(self):
        self.status = ContractStatus.ACTIVE
        self.updated_at = datetime.now()

    def suspend(self):
        self.status = ContractStatus.SUSPENDED
        self.updated_at = datetime.now()

    def complete(self):
        self.status = ContractStatus.COMPLETED
        self.updated_at = datetime.now()
