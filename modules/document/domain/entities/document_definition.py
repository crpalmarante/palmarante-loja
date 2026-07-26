from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class FieldType(Enum):
    TEXT = 'text'
    NUMBER = 'number'
    DATE = 'date'
    BOOLEAN = 'boolean'
    SELECT = 'select'
    PARTY = 'party'
    ITEM = 'item'
    MONEY = 'money'
    PERCENT = 'percent'


class BehaviorType(Enum):
    INVENTORY = 'inventory'
    FINANCIAL = 'financial'
    FISCAL = 'fiscal'
    WORKFLOW = 'workflow'
    ACCOUNTING = 'accounting'


@dataclass
class DocumentFieldDef:
    name: str
    code: str
    field_type: FieldType = FieldType.TEXT
    required: bool = False
    options: str = ''
    default_value: str = ''
    sort_order: int = 0


@dataclass
class DocumentLineFieldDef:
    name: str
    code: str
    field_type: FieldType = FieldType.TEXT
    required: bool = False
    sort_order: int = 0


@dataclass
class DocumentDefinition:
    name: str
    code: str
    description: str = ''
    direction: str = 'out'
    has_lines: bool = True
    has_parties: bool = True
    has_totals: bool = True
    has_workflow: bool = False
    workflow_code: str = ''
    behaviors: list = None
    header_fields: list = None
    line_fields: list = None
    party_types: list = None
    active: bool = True
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.behaviors is None:
            self.behaviors = []
        if self.header_fields is None:
            self.header_fields = []
        if self.line_fields is None:
            self.line_fields = []
        if self.party_types is None:
            self.party_types = ['customer', 'supplier']
        if self.created_at is None:
            self.created_at = datetime.now()
