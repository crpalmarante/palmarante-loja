from dataclasses import dataclass, field


@dataclass
class CreateDocument:
    document_type: str
    definition_id: str = ''
    number: str = ''
    organization_id: str = ''
    branch_id: str = ''
    direction: str = 'out'
    header: dict = None
    lines: list = None
    parties: list = None
    references: list = None
    notes: str = ''
    created_by: str = ''


@dataclass
class UpdateDocumentHeader:
    document_id: str
    header: dict = None


@dataclass
class AddDocumentLine:
    document_id: str
    item_id: str = ''
    item_code: str = ''
    item_name: str = ''
    quantity: float = 1.0
    unit: str = 'UN'
    unit_price: float = 0.0
    discount_pct: float = 0.0
    tax_value: float = 0.0
    notes: str = ''


@dataclass
class RemoveDocumentLine:
    document_id: str
    line_id: str


@dataclass
class ChangeDocumentStatus:
    document_id: str
    status: str
    comment: str = ''
    performed_by: str = ''


@dataclass
class CreateDefinition:
    name: str
    code: str
    description: str = ''
    direction: str = 'out'
    has_lines: bool = True
    has_parties: bool = True
    has_totals: bool = True
    has_workflow: bool = False
    workflow_code: str = ''
    header_fields: list = None
    line_fields: list = None
    party_types: list = None
    behaviors: list = None


@dataclass
class SetupNumbering:
    document_type: str
    pattern: str = '{year}{month}{seq:06d}'
    prefix: str = ''
    suffix: str = ''
    digits: int = 6
    series: str = '1'
    next_number: int = 1
