from abc import ABC, abstractmethod
from modules.party.domain.entities.party import Party
from modules.party.domain.value_objects.party_id import PartyId


class PartyRepository(ABC):

    @abstractmethod
    def save(self, party: Party) -> Party:
        pass

    @abstractmethod
    def find_by_id(self, party_id: PartyId) -> Party | None:
        pass

    @abstractmethod
    def find_all(self, query: str = '', status: str = '', role: str = '',
                 party_type: str = '', offset: int = 0, limit: int = 50) -> list[Party]:
        pass

    @abstractmethod
    def count(self, query: str = '', status: str = '', role: str = '',
              party_type: str = '') -> int:
        pass

    @abstractmethod
    def delete(self, party_id: PartyId) -> None:
        pass
