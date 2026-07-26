from dataclasses import dataclass


@dataclass
class Warehouse:
    name: str
    code: str
    description: str = ''
    address: str = ''
    responsible: str = ''
    active: bool = True
    _id: str = ''
