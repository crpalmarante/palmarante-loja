from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class NoteType(str, Enum):
    INTERNAL = 'internal'
    EXTERNAL = 'external'
    DELIVERY = 'delivery'
    FISCAL = 'fiscal'


@dataclass
class SalesNote:
    document_id: str
    note_type: NoteType = NoteType.INTERNAL
    content: str = ''
    created_by: str = ''
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
