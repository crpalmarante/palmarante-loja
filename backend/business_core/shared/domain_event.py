import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class DomainEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = ""
    aggregate_id: str = ""
    aggregate_type: str = ""
    occurred_at: str = ""
    recorded_at: str = ""
    version: int = 1
    correlation_id: str = ""
    causation_id: str = ""
    actor_id: str = ""
    tenant_id: str = ""
    organization_id: str = ""
    payload: Optional[dict] = None
    metadata: Optional[dict] = None
