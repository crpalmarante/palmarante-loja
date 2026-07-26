import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class ItemId:
    value: str

    @staticmethod
    def generate() -> 'ItemId':
        return ItemId(str(uuid.uuid4()))

    @staticmethod
    def from_string(value: str) -> 'ItemId':
        return ItemId(value)

    def __str__(self) -> str:
        return self.value
