from dataclasses import dataclass
from datetime import datetime


@dataclass
class SalesAttachment:
    document_id: str
    filename: str = ''
    original_name: str = ''
    mime_type: str = 'application/octet-stream'
    size_bytes: int = 0
    category: str = 'general'
    uploaded_by: str = ''
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
