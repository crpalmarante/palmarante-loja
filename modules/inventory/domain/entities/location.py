from dataclasses import dataclass


@dataclass
class Location:
    warehouse_id: str
    code: str
    name: str = ''
    parent_id: str = ''
    type: str = 'rack'
    active: bool = True
    _id: str = ''

    @property
    def path_parts(self) -> list[str]:
        return [p for p in self.code.split('/') if p]

    @property
    def level(self) -> int:
        return len(self.path_parts)
