from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AuditEntry:
    entity_type: str
    entity_id: str
    field_name: str
    old_value: str = ''
    new_value: str = ''
    changed_by: str = ''
    change_type: str = 'update'
    document_id: str = ''
    metadata: dict = None
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = datetime.now()
