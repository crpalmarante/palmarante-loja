from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional


class NotificationPriority(Enum):
    LOW = 'low'
    NORMAL = 'normal'
    HIGH = 'high'
    URGENT = 'urgent'


class NotificationChannel(Enum):
    INBOX = 'inbox'
    EMAIL = 'email'
    PUSH = 'push'
    SMS = 'sms'


class TaskStatus(Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'


class ApprovalStatus(Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    CANCELLED = 'cancelled'


class AlertSeverity(Enum):
    INFO = 'info'
    WARNING = 'warning'
    CRITICAL = 'critical'


class ActivityType(Enum):
    CREATED = 'created'
    UPDATED = 'updated'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    CANCELLED = 'cancelled'
    COMMENTED = 'commented'
    SHIPPED = 'shipped'
    RECEIVED = 'received'
    INVOICED = 'invoiced'
    PAID = 'paid'
    STATUS_CHANGE = 'status_change'


@dataclass
class Notification:
    user_id: str
    title: str
    message: str
    priority: NotificationPriority = NotificationPriority.NORMAL
    channel: NotificationChannel = NotificationChannel.INBOX
    read: bool = False
    entity_type: str = ''
    entity_id: str = ''
    action_url: str = ''
    icon: str = ''
    category: str = ''
    created_at: datetime = None
    read_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def mark_read(self):
        self.read = True
        self.read_at = datetime.now()

    def to_dict(self) -> dict:
        return {
            'id': self._id,
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'priority': self.priority.value,
            'channel': self.channel.value,
            'read': self.read,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'action_url': self.action_url,
            'icon': self.icon,
            'category': self.category,
            'created_at': self.created_at.isoformat() if self.created_at else '',
            'read_at': self.read_at.isoformat() if self.read_at else '',
        }


@dataclass
class Task:
    title: str
    assignee_id: str
    status: TaskStatus = TaskStatus.PENDING
    priority: NotificationPriority = NotificationPriority.NORMAL
    description: str = ''
    due_date: datetime = None
    completed_at: datetime = None
    entity_type: str = ''
    entity_id: str = ''
    created_by: str = ''
    category: str = ''
    tags: list = None
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.tags is None:
            self.tags = []

    def complete(self):
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()

    def cancel(self):
        self.status = TaskStatus.CANCELLED

    def start(self):
        self.status = TaskStatus.IN_PROGRESS

    @property
    def overdue(self) -> bool:
        if self.due_date and self.status not in (TaskStatus.COMPLETED, TaskStatus.CANCELLED):
            return datetime.now() > self.due_date
        return False

    def to_dict(self) -> dict:
        return {
            'id': self._id,
            'title': self.title,
            'assignee_id': self.assignee_id,
            'status': self.status.value,
            'priority': self.priority.value,
            'description': self.description,
            'due_date': self.due_date.isoformat() if self.due_date else '',
            'completed_at': self.completed_at.isoformat() if self.completed_at else '',
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'created_by': self.created_by,
            'category': self.category,
            'tags': self.tags,
            'created_at': self.created_at.isoformat() if self.created_at else '',
            'overdue': self.overdue,
        }


@dataclass
class Alert:
    user_id: str
    title: str
    message: str
    severity: AlertSeverity = AlertSeverity.INFO
    acknowledged: bool = False
    entity_type: str = ''
    entity_id: str = ''
    action_url: str = ''
    expires_at: datetime = None
    created_at: datetime = None
    acknowledged_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def acknowledge(self):
        self.acknowledged = True
        self.acknowledged_at = datetime.now()

    def to_dict(self) -> dict:
        return {
            'id': self._id,
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'severity': self.severity.value,
            'acknowledged': self.acknowledged,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'action_url': self.action_url,
            'expires_at': self.expires_at.isoformat() if self.expires_at else '',
            'created_at': self.created_at.isoformat() if self.created_at else '',
            'acknowledged_at': self.acknowledged_at.isoformat() if self.acknowledged_at else '',
        }


@dataclass
class Approval:
    title: str
    target_type: str
    target_id: str
    requester_id: str
    approver_ids: list
    status: ApprovalStatus = ApprovalStatus.PENDING
    priority: NotificationPriority = NotificationPriority.NORMAL
    reason: str = ''
    rejection_reason: str = ''
    decided_by: str = ''
    decided_at: datetime = None
    deadline: datetime = None
    escalation_minutes: int = 0
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def approve(self, user_id: str, reason: str = ''):
        self.status = ApprovalStatus.APPROVED
        self.decided_by = user_id
        self.decided_at = datetime.now()
        self.reason = reason

    def reject(self, user_id: str, reason: str = ''):
        self.status = ApprovalStatus.REJECTED
        self.decided_by = user_id
        self.decided_at = datetime.now()
        self.rejection_reason = reason

    def cancel(self):
        self.status = ApprovalStatus.CANCELLED

    @property
    def overdue(self) -> bool:
        if self.deadline and self.status == ApprovalStatus.PENDING:
            return datetime.now() > self.deadline
        return False

    def to_dict(self) -> dict:
        return {
            'id': self._id,
            'title': self.title,
            'target_type': self.target_type,
            'target_id': self.target_id,
            'requester_id': self.requester_id,
            'approver_ids': self.approver_ids,
            'status': self.status.value,
            'priority': self.priority.value,
            'reason': self.reason,
            'rejection_reason': self.rejection_reason,
            'decided_by': self.decided_by,
            'decided_at': self.decided_at.isoformat() if self.decided_at else '',
            'deadline': self.deadline.isoformat() if self.deadline else '',
            'created_at': self.created_at.isoformat() if self.created_at else '',
            'overdue': self.overdue,
        }


@dataclass
class Activity:
    entity_type: str
    entity_id: str
    activity_type: ActivityType
    user_id: str
    description: str
    metadata: dict = None
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.metadata is None:
            self.metadata = {}

    def to_dict(self) -> dict:
        return {
            'id': self._id,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'activity_type': self.activity_type.value,
            'user_id': self.user_id,
            'description': self.description,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat() if self.created_at else '',
        }


@dataclass
class Reminder:
    user_id: str
    title: str
    remind_at: datetime
    message: str = ''
    entity_type: str = ''
    entity_id: str = ''
    recurring: str = ''
    fired: bool = False
    created_at: datetime = None
    fired_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def fire(self):
        self.fired = True
        self.fired_at = datetime.now()

    @property
    def should_fire(self) -> bool:
        return not self.fired and datetime.now() >= self.remind_at

    def to_dict(self) -> dict:
        return {
            'id': self._id,
            'user_id': self.user_id,
            'title': self.title,
            'remind_at': self.remind_at.isoformat() if self.remind_at else '',
            'message': self.message,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'recurring': self.recurring,
            'fired': self.fired,
            'created_at': self.created_at.isoformat() if self.created_at else '',
        }


@dataclass
class Watcher:
    user_id: str
    entity_type: str
    entity_id: str
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def to_dict(self) -> dict:
        return {
            'id': self._id,
            'user_id': self.user_id,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'created_at': self.created_at.isoformat() if self.created_at else '',
        }


@dataclass
class Mention:
    user_id: str
    mentioned_by: str
    entity_type: str
    entity_id: str
    context: str = ''
    read: bool = False
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def mark_read(self):
        self.read = True

    def to_dict(self) -> dict:
        return {
            'id': self._id,
            'user_id': self.user_id,
            'mentioned_by': self.mentioned_by,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'context': self.context,
            'read': self.read,
            'created_at': self.created_at.isoformat() if self.created_at else '',
        }
