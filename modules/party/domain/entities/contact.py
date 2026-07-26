from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ContactType(str, Enum):
    EMAIL = 'email'
    PHONE = 'phone'
    MOBILE = 'mobile'
    WHATSAPP = 'whatsapp'
    WEBSITE = 'website'
    OTHER = 'other'


@dataclass
class Contact:
    type: ContactType
    value: str
    name: str = ''
    is_main: bool = False
    created_at: datetime = field(default_factory=datetime.now)
