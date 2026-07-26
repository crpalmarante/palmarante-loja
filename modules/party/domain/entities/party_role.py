from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class RoleType(str, Enum):
    CUSTOMER = 'customer'
    SUPPLIER = 'supplier'
    EMPLOYEE = 'employee'
    CARRIER = 'carrier'
    BANK = 'bank'
    VENDOR = 'vendor'
    PROSPECT = 'prospect'


class RoleStatus(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


@dataclass
class PartyRole:
    role_type: RoleType
    status: RoleStatus = RoleStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.now)

    def activate(self):
        self.status = RoleStatus.ACTIVE

    def deactivate(self):
        self.status = RoleStatus.INACTIVE
