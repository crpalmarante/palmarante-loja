import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class ProductId:
    value: str

    @staticmethod
    def generate() -> 'ProductId':
        return ProductId(str(uuid.uuid4()))

    @staticmethod
    def from_string(value: str) -> 'ProductId':
        return ProductId(value)

    def __str__(self) -> str:
        return self.value
