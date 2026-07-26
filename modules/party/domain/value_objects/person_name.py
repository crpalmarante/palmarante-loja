from dataclasses import dataclass


@dataclass(frozen=True)
class PersonName:
    given_name: str
    family_name: str

    def full_name(self) -> str:
        return f'{self.given_name} {self.family_name}'.strip()

    def __str__(self) -> str:
        return self.full_name()
