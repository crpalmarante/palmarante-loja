from dataclasses import dataclass

from business_core.domain.party.document import DocumentType
from business_core.shared.value_object import ValueObject


@dataclass(frozen=True)
class PartyDocument(ValueObject):
    type: DocumentType = DocumentType.CPF
    value: str = ""
    is_main: bool = False
