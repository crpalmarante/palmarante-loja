import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class PartyId:
    value: str

    @staticmethod
    def generate() -> 'PartyId':
        return PartyId(str(uuid.uuid4()))

    @staticmethod
    def from_string(value: str) -> 'PartyId':
        return PartyId(value)

    def __str__(self) -> str:
        return self.value
