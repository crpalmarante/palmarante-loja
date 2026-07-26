from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class AttributeType(str, Enum):
    TEXT = 'text'
    COLOR = 'color'
    SIZE = 'size'
    NUMERIC = 'numeric'
    BOOLEAN = 'boolean'


@dataclass
class Attribute:
    name: str
    code: str = ''
    type: AttributeType = AttributeType.TEXT
    required: bool = False
    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
