from dataclasses import dataclass, field


@dataclass
class CreateQuotation:
    customer_id: str
    customer_name: str = ''
    lines: list = None
    notes: str = ''
    sales_rep: str = ''
    opportunity_id: str = ''
    valid_until: str = ''
    payment_terms: str = ''
    price_list_id: str = ''


@dataclass
class ApproveQuotation:
    quotation_id: str
    performed_by: str = ''
    comment: str = ''


@dataclass
class ConvertQuotationToOrder:
    quotation_document_id: str
    sales_rep: str = ''
    price_list_id: str = ''


@dataclass
class CreateSalesOrder:
    customer_id: str
    customer_name: str = ''
    lines: list = None
    notes: str = ''
    sales_rep: str = ''
    opportunity_id: str = ''
    price_list_id: str = ''
    discount_rule_ids: list = None
    payment_method: str = 'pix'
    installments: int = 1
    due_days: int = 30
    rep_commission_rate: float = 0.0
    expected_delivery: str = ''


@dataclass
class ReserveInventory:
    document_id: str
    warehouse_id: str = ''


@dataclass
class ReleaseInventory:
    document_id: str
    warehouse_id: str = ''


@dataclass
class GenerateShipment:
    document_id: str
    carrier: str = ''
    origin_warehouse: str = ''
    tracking_code: str = ''
    notes: str = ''
    created_by: str = ''


@dataclass
class GenerateInvoice:
    document_id: str
    fiscal: bool = False
    created_by: str = ''


@dataclass
class CancelOrder:
    document_id: str
    reason: str = ''
    performed_by: str = ''


@dataclass
class CloseOrder:
    document_id: str
    performed_by: str = ''
