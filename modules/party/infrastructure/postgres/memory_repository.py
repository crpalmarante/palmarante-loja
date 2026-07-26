from modules.party.domain.entities.party import Party
from modules.party.domain.value_objects.party_id import PartyId
from modules.party.domain.repositories.party_repository import PartyRepository


class InMemoryPartyRepository(PartyRepository):
    def __init__(self):
        self._store: dict[str, Party] = {}

    def save(self, party: Party) -> Party:
        self._store[str(party.id)] = party
        return party

    def find_by_id(self, party_id: PartyId) -> Party | None:
        return self._store.get(str(party_id))

    def find_all(self, query: str = '', status: str = '', role: str = '',
                 party_type: str = '', offset: int = 0, limit: int = 50) -> list[Party]:
        result = list(self._store.values())

        if party_type:
            result = [p for p in result if p.party_type.value == party_type]
        if status:
            result = [p for p in result if p.status.value == status]
        if role:
            result = [p for p in result if p.has_role_str(role)]
        if query:
            q = query.lower()
            result = [p for p in result if q in p.display_name.lower() or
                      any(q in d.value.lower() for d in p.documents) or
                      any(q in c.value.lower() for c in p.contacts)]

        result.sort(key=lambda p: p.created_at, reverse=True)
        return result[offset:offset + limit]

    def count(self, query: str = '', status: str = '', role: str = '',
              party_type: str = '') -> int:
        return len(self.find_all(query, status, role, party_type, 0, 999999))

    def delete(self, party_id: PartyId) -> None:
        self._store.pop(str(party_id), None)
