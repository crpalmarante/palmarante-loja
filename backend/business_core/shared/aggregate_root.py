from dataclasses import dataclass, field

from business_core.shared.entity import Entity


@dataclass
class AggregateRoot(Entity):
    version: int = 0

    def apply(self, event):
        self._add_event(event)
        self.when(event)
        self.version += 1

    def when(self, event):
        pass
