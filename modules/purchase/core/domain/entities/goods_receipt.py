from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class GoodsReceiptStatus(Enum):
    DRAFT = 'draft'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'


@dataclass
class GoodsReceiptLine:
    po_line_id: str
    item_id: str = ''
    item_code: str = ''
    item_name: str = ''
    ordered_qty: float = 0.0
    received_qty: float = 0.0
    accepted_qty: float = 0.0
    rejected_qty: float = 0.0
    rejection_reason: str = ''
    notes: str = ''
    _id: str = ''


@dataclass
class GoodsReceipt:
    po_id: str
    po_number: str = ''
    document_id: str = ''
    supplier_id: str = ''
    supplier_name: str = ''
    lines: list = None
    status: GoodsReceiptStatus = GoodsReceiptStatus.DRAFT
    warehouse_id: str = ''
    received_by: str = ''
    document_number: str = ''
    notes: str = ''
    received_at: datetime = None
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.lines is None:
            self.lines = []
        if self.received_at is None:
            self.received_at = datetime.now()
        if self.created_at is None:
            self.created_at = datetime.now()

    def complete(self):
        self.status = GoodsReceiptStatus.COMPLETED
