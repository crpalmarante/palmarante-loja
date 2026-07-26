from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class AssignmentType(Enum):
    ROLE = 'role'
    USER = 'user'
    MANAGER = 'manager'
    GROUP = 'group'


@dataclass
class WorkflowAssignment:
    workflow_id: str
    transition_id: str
    assignment_type: AssignmentType
    value: str
    active: bool = True
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
