from dataclasses import dataclass
from datetime import datetime
from modules.document.domain.value_objects.document_status import DocumentStatus


@dataclass
class DocumentCreated:
    document_id: str
    document_type: str
    number: str
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class DocumentStatusChanged:
    document_id: str
    document_type: str
    from_status: str
    to_status: str
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class DocumentLineAdded:
    document_id: str
    item_id: str
    quantity: float
    total: float
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class DocumentReferenced:
    document_id: str
    reference_type: str
    reference_id: str
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class DocumentCompleted:
    document_id: str
    document_type: str
    total: float
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class DocumentCancelled:
    document_id: str
    document_type: str
    reason: str = ''
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
