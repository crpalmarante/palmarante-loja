from dataclasses import dataclass
from datetime import datetime


@dataclass
class SalesTeamMember:
    rep_id: str
    name: str = ''
    role: str = 'seller'
    supervisor_id: str = ''
    email: str = ''
    active: bool = True
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
