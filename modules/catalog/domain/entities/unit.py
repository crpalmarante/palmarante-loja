from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class UnitType(str, Enum):
    UNITS = 'units'
    WEIGHT = 'weight'
    VOLUME = 'volume'
    LENGTH = 'length'
    AREA = 'area'
    TIME = 'time'
    PACKAGE = 'package'
    OTHER = 'other'


@dataclass
class Unit:
    code: str
    name: str
    type: UnitType = UnitType.UNITS
    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
