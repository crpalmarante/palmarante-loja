from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class StateType(Enum):
    INITIAL = 'initial'
    INTERMEDIATE = 'intermediate'
    FINAL = 'final'
    APPROVAL = 'approval'


@dataclass
class WorkflowState:
    workflow_id: str
    name: str
    code: str
    type: StateType = StateType.INTERMEDIATE
    description: str = ''
    color: str = '#1a73e8'
    sort_order: int = 0
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    @property
    def is_initial(self) -> bool:
        return self.type == StateType.INITIAL

    @property
    def is_final(self) -> bool:
        return self.type == StateType.FINAL

    @property
    def is_approval(self) -> bool:
        return self.type == StateType.APPROVAL
