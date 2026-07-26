from enum import Enum


class OpportunityStatus(Enum):
    NEW = 'new'
    QUALIFIED = 'qualified'
    PROPOSAL = 'proposal'
    NEGOTIATION = 'negotiation'
    WON = 'won'
    LOST = 'lost'
    CANCELLED = 'cancelled'


class SalesOrderStatus(Enum):
    DRAFT = 'draft'
    PENDING_APPROVAL = 'pending_approval'
    APPROVED = 'approved'
    RESERVED = 'reserved'
    PICKING = 'picking'
    SHIPPED = 'shipped'
    INVOICED = 'invoiced'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'


class DeliveryStatus(Enum):
    PENDING = 'pending'
    PICKING = 'picking'
    PACKED = 'packed'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    PARTIAL = 'partial'


class ContractStatus(Enum):
    DRAFT = 'draft'
    ACTIVE = 'active'
    SUSPENDED = 'suspended'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
