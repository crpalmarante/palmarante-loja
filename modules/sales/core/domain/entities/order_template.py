from dataclasses import dataclass
from datetime import datetime


@dataclass
class OrderTemplateLine:
    item_id: str
    item_name: str = ''
    item_code: str = ''
    quantity: float = 1
    unit: str = 'UN'
    unit_price: float = 0.0


@dataclass
class OrderTemplate:
    name: str
    customer_id: str = ''
    customer_name: str = ''
    lines: list = None
    payment_terms: str = 'pix'
    installments: int = 1
    due_days: int = 30
    notes: str = ''
    sales_rep: str = ''
    tags: list = None
    created_at: datetime = None
    updated_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.lines is None:
            self.lines = []
        if self.tags is None:
            self.tags = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
