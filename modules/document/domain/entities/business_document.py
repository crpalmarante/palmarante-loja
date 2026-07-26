from dataclasses import dataclass, field
from datetime import datetime
from modules.document.domain.value_objects.document_status import DocumentStatus


@dataclass
class DocumentHeader:
    number: str = ''
    date: datetime = None
    currency: str = 'BRL'
    notes: str = ''
    responsible: str = ''
    department: str = ''
    cost_center: str = ''
    custom_fields: dict = None

    def __post_init__(self):
        if self.date is None:
            self.date = datetime.now()
        if self.custom_fields is None:
            self.custom_fields = {}


@dataclass
class DocumentLine:
    item_id: str = ''
    item_code: str = ''
    item_name: str = ''
    quantity: float = 1.0
    unit: str = 'UN'
    unit_price: float = 0.0
    discount_pct: float = 0.0
    discount_value: float = 0.0
    tax_value: float = 0.0
    total: float = 0.0
    notes: str = ''
    custom_fields: dict = None
    sort_order: int = 0
    _id: str = ''

    def __post_init__(self):
        if self.custom_fields is None:
            self.custom_fields = {}

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price

    @property
    def net_total(self) -> float:
        return self.subtotal - self.discount_value


@dataclass
class DocumentParty:
    party_id: str
    party_type: str
    party_name: str = ''
    document_id: str = ''
    _id: str = ''


@dataclass
class DocumentReference:
    document_id: str
    reference_type: str
    reference_id: str
    reference_number: str = ''
    _id: str = ''


@dataclass
class DocumentAttachment:
    document_id: str
    filename: str
    file_path: str = ''
    file_size: int = 0
    mime_type: str = ''
    notes: str = ''
    uploaded_by: str = ''
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class DocumentNote:
    document_id: str
    content: str
    note_type: str = 'general'
    created_by: str = ''
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class DocumentHistory:
    document_id: str
    action: str
    from_status: str = ''
    to_status: str = ''
    comment: str = ''
    performed_by: str = ''
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class BusinessDocument:
    document_type: str
    definition_id: str = ''
    number: str = ''
    header: DocumentHeader = None
    lines: list = None
    parties: list = None
    references: list = None
    attachments: list = None
    notes: list = None
    history: list = None
    status: DocumentStatus = DocumentStatus.DRAFT
    organization_id: str = ''
    branch_id: str = ''
    direction: str = 'out'
    subtotal: float = 0.0
    discount_total: float = 0.0
    freight: float = 0.0
    insurance: float = 0.0
    tax_total: float = 0.0
    other_costs: float = 0.0
    total: float = 0.0
    workflow_instance_id: str = ''
    metadata: dict = None
    created_at: datetime = None
    updated_at: datetime = None
    created_by: str = ''
    _id: str = ''

    def __post_init__(self):
        if self.header is None:
            self.header = DocumentHeader()
        if self.lines is None:
            self.lines = []
        if self.parties is None:
            self.parties = []
        if self.references is None:
            self.references = []
        if self.attachments is None:
            self.attachments = []
        if self.notes is None:
            self.notes = []
        if self.history is None:
            self.history = []
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

    def add_line(self, line: DocumentLine):
        self.lines.append(line)
        self._recalc_totals()

    def add_party(self, party: DocumentParty):
        self.parties.append(party)

    def add_reference(self, ref: DocumentReference):
        self.references.append(ref)

    def add_history(self, action: str, from_status: str = '',
                    to_status: str = '', comment: str = '',
                    performed_by: str = ''):
        h = DocumentHistory(
            document_id=self._id,
            action=action,
            from_status=from_status or self.status.value,
            to_status=to_status,
            comment=comment,
            performed_by=performed_by,
        )
        self.history.append(h)

    def change_status(self, new_status: DocumentStatus, comment: str = '',
                      performed_by: str = ''):
        old = self.status.value
        self.status = new_status
        self.updated_at = datetime.now()
        self.add_history('status_change', from_status=old,
                         to_status=new_status.value, comment=comment,
                         performed_by=performed_by)

    def _recalc_totals(self):
        subtotal = sum(l.subtotal for l in self.lines)
        discount = sum(l.discount_value for l in self.lines)
        tax = sum(l.tax_value for l in self.lines)
        self.subtotal = subtotal
        self.discount_total = discount
        self.tax_total = tax
        self.total = subtotal - discount + self.freight + self.insurance + tax + self.other_costs

    def recalc_totals(self):
        self._recalc_totals()
