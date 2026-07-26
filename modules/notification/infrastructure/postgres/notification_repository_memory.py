from datetime import datetime
from modules.notification.domain.entities.notification import (
    Notification, Task, Alert, Approval, Activity, Reminder, Watcher, Mention,
    NotificationPriority, TaskStatus, ApprovalStatus, AlertSeverity,
)


class NotificationRepositoryMemory:
    def __init__(self):
        self._notifications: dict[str, Notification] = {}
        self._tasks: dict[str, Task] = {}
        self._alerts: dict[str, Alert] = {}
        self._approvals: dict[str, Approval] = {}
        self._activities: dict[str, Activity] = {}
        self._reminders: dict[str, Reminder] = {}
        self._watchers: dict[str, Watcher] = {}
        self._mentions: dict[str, Mention] = {}
        self._counter = 0

    def _next_id(self) -> str:
        self._counter += 1
        return f'n{self._counter:04d}'

    # ── Notifications ──────────────────────────────────────
    def save_notification(self, n: Notification) -> Notification:
        if not n._id:
            n._id = self._next_id()
        self._notifications[n._id] = n
        return n

    def find_notification(self, notification_id: str) -> Notification | None:
        return self._notifications.get(notification_id)

    def find_user_notifications(self, user_id: str, limit: int = 50) -> list:
        items = [n for n in self._notifications.values() if n.user_id == user_id]
        items.sort(key=lambda x: x.created_at, reverse=True)
        return items[:limit]

    def find_unread_notifications(self, user_id: str) -> list:
        items = [n for n in self._notifications.values()
                 if n.user_id == user_id and not n.read]
        items.sort(key=lambda x: x.created_at, reverse=True)
        return items

    def count_unread(self, user_id: str) -> int:
        return sum(1 for n in self._notifications.values()
                   if n.user_id == user_id and not n.read)

    def mark_notification_read(self, notification_id: str):
        n = self._notifications.get(notification_id)
        if n:
            n.mark_read()

    def mark_all_user_read(self, user_id: str):
        for n in self._notifications.values():
            if n.user_id == user_id and not n.read:
                n.mark_read()

    def delete_old_notifications(self, before: datetime):
        to_delete = [id for id, n in self._notifications.items()
                     if n.created_at and n.created_at < before]
        for id in to_delete:
            del self._notifications[id]

    # ── Tasks ──────────────────────────────────────────────
    def save_task(self, t: Task) -> Task:
        if not t._id:
            t._id = self._next_id()
        self._tasks[t._id] = t
        return t

    def find_task(self, task_id: str) -> Task | None:
        return self._tasks.get(task_id)

    def find_user_tasks(self, user_id: str, status: TaskStatus = None) -> list:
        items = [t for t in self._tasks.values() if t.assignee_id == user_id]
        if status:
            items = [t for t in items if t.status == status]
        items.sort(key=lambda x: x.created_at, reverse=True)
        return items

    def find_pending_tasks(self, user_id: str) -> list:
        return [t for t in self._tasks.values()
                if t.assignee_id == user_id
                and t.status in (TaskStatus.PENDING, TaskStatus.IN_PROGRESS)]

    def find_overdue_tasks(self) -> list:
        now = datetime.now()
        return [t for t in self._tasks.values()
                if t.status in (TaskStatus.PENDING, TaskStatus.IN_PROGRESS)
                and t.due_date and t.due_date < now]

    # ── Alerts ─────────────────────────────────────────────
    def save_alert(self, a: Alert) -> Alert:
        if not a._id:
            a._id = self._next_id()
        self._alerts[a._id] = a
        return a

    def find_user_alerts(self, user_id: str, include_acknowledged: bool = False) -> list:
        items = [a for a in self._alerts.values() if a.user_id == user_id]
        if not include_acknowledged:
            items = [a for a in items if not a.acknowledged]
        items.sort(key=lambda x: (x.severity.value, x.created_at), reverse=True)
        return items

    def find_active_alerts(self) -> list:
        now = datetime.now()
        return [a for a in self._alerts.values()
                if not a.acknowledged
                and (not a.expires_at or a.expires_at > now)]

    # ── Approvals ──────────────────────────────────────────
    def save_approval(self, a: Approval) -> Approval:
        if not a._id:
            a._id = self._next_id()
        self._approvals[a._id] = a
        return a

    def find_approval(self, approval_id: str) -> Approval | None:
        return self._approvals.get(approval_id)

    def find_user_pending_approvals(self, user_id: str) -> list:
        items = [a for a in self._approvals.values()
                 if user_id in a.approver_ids and a.status == ApprovalStatus.PENDING]
        items.sort(key=lambda x: x.created_at, reverse=True)
        return items

    def find_target_approvals(self, target_type: str, target_id: str) -> list:
        return [a for a in self._approvals.values()
                if a.target_type == target_type and a.target_id == target_id]

    def find_overdue_approvals(self) -> list:
        now = datetime.now()
        return [a for a in self._approvals.values()
                if a.status == ApprovalStatus.PENDING
                and a.deadline and a.deadline < now]

    # ── Activities ─────────────────────────────────────────
    def save_activity(self, a: Activity) -> Activity:
        if not a._id:
            a._id = self._next_id()
        self._activities[a._id] = a
        return a

    def find_entity_activities(self, entity_type: str, entity_id: str, limit: int = 50) -> list:
        items = [a for a in self._activities.values()
                 if a.entity_type == entity_type and a.entity_id == entity_id]
        items.sort(key=lambda x: x.created_at, reverse=True)
        return items[:limit]

    def find_user_activities(self, user_id: str, limit: int = 20) -> list:
        items = [a for a in self._activities.values() if a.user_id == user_id]
        items.sort(key=lambda x: x.created_at, reverse=True)
        return items[:limit]

    def find_recent_activities(self, limit: int = 50) -> list:
        items = sorted(self._activities.values(),
                       key=lambda x: x.created_at, reverse=True)
        return items[:limit]

    # ── Reminders ──────────────────────────────────────────
    def save_reminder(self, r: Reminder) -> Reminder:
        if not r._id:
            r._id = self._next_id()
        self._reminders[r._id] = r
        return r

    def find_user_reminders(self, user_id: str) -> list:
        items = [r for r in self._reminders.values() if r.user_id == user_id]
        items.sort(key=lambda x: x.remind_at)
        return items

    def find_due_reminders(self) -> list:
        now = datetime.now()
        return [r for r in self._reminders.values() if r.should_fire]

    # ── Watchers ───────────────────────────────────────────
    def save_watcher(self, w: Watcher) -> Watcher:
        if not w._id:
            w._id = self._next_id()
        key = (w.user_id, w.entity_type, w.entity_id)
        existing = [x for x in self._watchers.values()
                    if x.user_id == w.user_id
                    and x.entity_type == w.entity_type
                    and x.entity_id == w.entity_id]
        if existing:
            return existing[0]
        self._watchers[w._id] = w
        return w

    def remove_watcher(self, user_id: str, entity_type: str, entity_id: str):
        to_delete = [id for id, w in self._watchers.items()
                     if w.user_id == user_id
                     and w.entity_type == entity_type
                     and w.entity_id == entity_id]
        for id in to_delete:
            del self._watchers[id]

    def find_entity_watchers(self, entity_type: str, entity_id: str) -> list:
        return [w for w in self._watchers.values()
                if w.entity_type == entity_type and w.entity_id == entity_id]

    def is_watching(self, user_id: str, entity_type: str, entity_id: str) -> bool:
        return any(w.user_id == user_id and w.entity_type == entity_type
                   and w.entity_id == entity_id for w in self._watchers.values())

    # ── Mentions ───────────────────────────────────────────
    def save_mention(self, m: Mention) -> Mention:
        if not m._id:
            m._id = self._next_id()
        self._mentions[m._id] = m
        return m

    def find_user_mentions(self, user_id: str, unread_only: bool = True) -> list:
        items = [m for m in self._mentions.values() if m.user_id == user_id]
        if unread_only:
            items = [m for m in items if not m.read]
        items.sort(key=lambda x: x.created_at, reverse=True)
        return items

    def mark_mention_read(self, mention_id: str):
        m = self._mentions.get(mention_id)
        if m:
            m.mark_read()

    # ── Dashboard counters ─────────────────────────────────
    def dashboard(self, user_id: str) -> dict:
        return {
            'unread_notifications': self.count_unread(user_id),
            'pending_tasks': len(self.find_pending_tasks(user_id)),
            'overdue_tasks': len([t for t in self._tasks.values()
                                  if t.assignee_id == user_id and t.overdue]),
            'pending_approvals': len(self.find_user_pending_approvals(user_id)),
            'active_alerts': len(self.find_user_alerts(user_id)),
            'unread_mentions': len(self.find_user_mentions(user_id)),
        }
