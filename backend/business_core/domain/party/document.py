from dataclasses import dataclass
from enum import Enum

from business_core.shared.value_object import ValueObject


class DocumentType(Enum):
    CPF = "cpf"
    CNPJ = "cnpj"
    RG = "rg"
    IE = "ie"  # Inscrição Estadual
    IM = "im"  # Inscrição Municipal
    PASSPORT = "passport"
    OTHER = "other"


@dataclass(frozen=True)
class Document(ValueObject):
    type: DocumentType = DocumentType.CPF
    value: str = ""

    def __str__(self):
        return self.value
