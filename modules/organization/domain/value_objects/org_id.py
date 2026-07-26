import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class OrgId:
    value: str

    @staticmethod
    def generate() -> 'OrgId':
        return OrgId(str(uuid.uuid4()))

    @staticmethod
    def from_string(value: str) -> 'OrgId':
        return OrgId(value)

    def __str__(self) -> str:
        return self.value
