from abc import ABC, abstractmethod
from typing import Optional, List

from business_core.domain.party.party import Party


class IPartyRepository(ABC):
    @abstractmethod
    def save(self, party: Party): ...

    @abstractmethod
    def find_by_id(self, party_id: str) -> Optional[Party]: ...

    @abstractmethod
    def find_by_document(self, document_value: str) -> Optional[Party]: ...

    @abstractmethod
    def list(self, status: str = "", role: str = "", query: str = "", offset: int = 0, limit: int = 50) -> List[Party]: ...

    @abstractmethod
    def count(self, status: str = "", role: str = "", query: str = "") -> int: ...

    @abstractmethod
    def delete(self, party_id: str): ...

    @abstractmethod
    def exists_by_document(self, document_value: str) -> bool: ...
