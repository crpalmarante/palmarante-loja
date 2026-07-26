from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class FiscalClassification:
    ncm: str = ''
    cest: str = ''
    origin: int = 0
    gtin: str = ''
    description: str = ''
    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
