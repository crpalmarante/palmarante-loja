from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Branch:
    organization_id: str
    party_id: str
    code: str = ''
    name: str = ''
    cnpj: str = ''
    ie: str = ''
    phone: str = ''
    email: str = ''
    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def deactivate(self):
        self.active = False
        self.updated_at = datetime.now()

    def activate(self):
        self.active = True
        self.updated_at = datetime.now()
