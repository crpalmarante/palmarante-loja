from dataclasses import dataclass
from datetime import datetime


@dataclass
class WorkflowStarted:
    instance_id: str
    workflow_id: str
    document_type: str
    document_id: str
    initial_state: str
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class WorkflowTransitioned:
    instance_id: str
    workflow_id: str
    from_state: str
    to_state: str
    transition: str
    performed_by: str = ''
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class WorkflowCompleted:
    instance_id: str
    workflow_id: str
    document_type: str
    document_id: str
    final_state: str
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class WorkflowCancelled:
    instance_id: str
    workflow_id: str
    reason: str = ''
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class ApprovalRequested:
    approval_id: str
    instance_id: str
    transition_id: str
    role: str = ''
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class ApprovalCompleted:
    approval_id: str
    instance_id: str
    status: str
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
