from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class DocumentType(str, Enum):
    CPF = 'cpf'
    CNPJ = 'cnpj'
    RG = 'rg'
    IE = 'ie'
    IM = 'im'
    PASSPORT = 'passport'
    OTHER = 'other'


@dataclass
class Document:
    type: DocumentType
    value: str
    issuer: str = ''
    is_main: bool = False
    created_at: datetime = field(default_factory=datetime.now)
