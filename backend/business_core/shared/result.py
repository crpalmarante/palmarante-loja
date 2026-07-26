from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class UseCaseResult:
    success: bool = True
    data: Any = None
    warnings: list[str] = field(default_factory=list)
    errors: list[dict] = field(default_factory=list)
    events: list = field(default_factory=list)
    status_code: int = 200


class ErrorCategory:
    VALIDATION = "validation"
    BUSINESS_RULE = "business_rule"
    UNAUTHORIZED = "unauthorized"
    CONFLICT = "conflict"
    NOT_FOUND = "not_found"
    TECHNICAL = "technical"


@dataclass
class BusinessError:
    category: str
    code: str
    message: str
    field: Optional[str] = None
