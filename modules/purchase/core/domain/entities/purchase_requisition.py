from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class RequisitionStatus(Enum):
    DRAFT = 'draft'
    PENDING_APPROVAL = 'pending_approval'
    APPROVED = 'approved'
    IN_RFQ = 'in_rfq'
    FULFILLED = 'fulfilled'
    CANCELLED = 'cancelled'


@dataclass
class RequisitionSource:
    request_id: str
    request_number: str = ''
    department: str = ''
    requestor: str = ''
    items: list = None
    _id: str = ''

    def __post_init__(self):
        if self.items is None:
            self.items = []


@dataclass
class PurchaseRequisitionItem:
    item_id: str
    item_code: str = ''
    item_name: str = ''
    quantity: float = 1.0
    unit: str = 'UN'
    estimated_price: float = 0.0
    estimated_total: float = 0.0
    required_date: str = ''
    notes: str = ''
    _id: str = ''


@dataclass
class PurchaseRequisition:
    title: str
    number: str = ''
    description: str = ''
    sources: list = None
    items: list = None
    status: RequisitionStatus = RequisitionStatus.DRAFT
    urgency: str = 'medium'
    buyer: str = ''
    approved_by: str = ''
    notes: str = ''
    created_at: datetime = None
    updated_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.sources is None:
            self.sources = []
        if self.items is None:
            self.items = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

    @property
    def estimated_total(self) -> float:
        return sum(i.estimated_total for i in self.items)

    def consolidate_from_requests(self, requests: list):
        for req in requests:
            req.source_id = req._id
            self.sources.append(RequisitionSource(
                request_id=req._id,
                request_number=req.number,
                department=req.department,
                requestor=req.requestor,
                items=req.items,
            ))
            for ri in req.items:
                existing = next((i for i in self.items if i.item_id == ri.item_id), None)
                if existing:
                    existing.quantity += ri.quantity
                    existing.estimated_total = existing.estimated_price * existing.quantity
                else:
                    self.items.append(PurchaseRequisitionItem(
                        item_id=ri.item_id, item_code=ri.item_code,
                        item_name=ri.item_name, quantity=ri.quantity,
                        unit=ri.unit, estimated_price=ri.estimated_price,
                        estimated_total=ri.estimated_total,
                        required_date=ri.required_date,
                    ))

    def approve(self, by: str = ''):
        self.status = RequisitionStatus.APPROVED
        self.approved_by = by
        self.updated_at = datetime.now()
