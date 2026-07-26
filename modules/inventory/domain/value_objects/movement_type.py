from enum import Enum


class MovementType(Enum):
    IN = 'in'
    OUT = 'out'
    TRANSFER = 'transfer'
    RESERVE = 'reserve'
    RELEASE = 'release'
    ADJUSTMENT = 'adjustment'
    PRODUCTION = 'production'
    CONSUMPTION = 'consumption'
    RETURN = 'return'


class MovementStatus(Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
