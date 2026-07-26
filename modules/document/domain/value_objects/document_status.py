from enum import Enum


class DocumentStatus(Enum):
    DRAFT = 'draft'
    OPEN = 'open'
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    ARCHIVED = 'archived'


class DocumentType(Enum):
    SALE_ORDER = 'sale_order'
    PURCHASE_ORDER = 'purchase_order'
    QUOTATION = 'quotation'
    INVOICE = 'invoice'
    NFE = 'nfe'
    PRODUCTION_ORDER = 'production_order'
    TRANSFER = 'transfer'
    ADJUSTMENT = 'adjustment'
    PAYMENT = 'payment'
    JOURNAL_ENTRY = 'journal_entry'
    SERVICE_ORDER = 'service_order'
    CONTRACT = 'contract'
    BUDGET = 'budget'
    EXPENSE = 'expense'
    RECEIPT = 'receipt'
    OTHER = 'other'


class DocumentDirection(Enum):
    IN = 'in'
    OUT = 'out'
    INTERNAL = 'internal'
