from dataclasses import dataclass, field
from typing import Optional

from business_core.shared.value_object import ValueObject


class EntityId(ValueObject):
    value: str


@dataclass
class Entity:
    id: str = ""
    _domain_events: list = field(default_factory=list, repr=False)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def _add_event(self, event):
        event.aggregate_id = self.id
        self._domain_events.append(event)

    def clear_events(self):
        events = list(self._domain_events)
        self._domain_events.clear()
        return events
