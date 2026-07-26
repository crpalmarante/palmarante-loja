from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TimelineEventType(str, Enum):
    CREATED = 'created'
    DISCOUNT_CHANGED = 'discount_changed'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    RESERVED = 'reserved'
    PICKING = 'picking'
    SHIPPED = 'shipped'
    INVOICED = 'invoiced'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    NOTE_ADDED = 'note_added'
    LINE_ADDED = 'line_added'
    LINE_REMOVED = 'line_removed'
    PRICE_CHANGED = 'price_changed'
    STATUS_CHANGED = 'status_changed'


@dataclass
class TimelineEntry:
    document_id: str
    event_type: str
    description: str = ''
    performed_by: str = ''
    old_value: str = ''
    new_value: str = ''
    metadata: dict = None
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = datetime.now()
