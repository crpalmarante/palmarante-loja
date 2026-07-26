import uuid
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class BusinessCommand:
    command_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    command_type: str = ""
    version: int = 1
    correlation_id: str = ""
    causation_id: str = ""
    tenant_id: str = ""
    organization_id: str = ""
    user_id: str = ""
    payload: Optional[dict] = None
    metadata: Optional[dict] = None
