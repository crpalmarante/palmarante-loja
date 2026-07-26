from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class CalendarEventType(str, Enum):
    ORDER = 'order'
    DELIVERY = 'delivery'
    RENEWAL = 'renewal'
    PROPOSAL = 'proposal'
    FOLLOW_UP = 'follow_up'
    VISIT = 'visit'


@dataclass
class CalendarEvent:
    title: str
    event_type: CalendarEventType = CalendarEventType.FOLLOW_UP
    date: str = ''
    time: str = ''
    customer_id: str = ''
    customer_name: str = ''
    document_id: str = ''
    sales_rep: str = ''
    description: str = ''
    status: str = 'scheduled'
    color: str = '#1a73e8'
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
