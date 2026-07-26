from dataclasses import dataclass
from datetime import date
from enum import Enum

from business_core.shared.value_object import ValueObject


class PartyRoleType(Enum):
    CUSTOMER = "customer"
    SUPPLIER = "supplier"
    EMPLOYEE = "employee"
    CARRIER = "carrier"
    SALES_REP = "sales_rep"
    ACCOUNTANT = "accountant"
    CONTACT = "contact"
    PARTNER = "partner"
    MANUFACTURER = "manufacturer"
    TAXPAYER = "taxpayer"
    BANK = "bank"
    OTHER = "other"


class RoleStatus(Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INACTIVE = "inactive"


@dataclass(frozen=True)
class PartyRole(ValueObject):
    role_type: PartyRoleType = PartyRoleType.CUSTOMER
    status: RoleStatus = RoleStatus.ACTIVE
    start_date: date = None
    end_date: date = None
