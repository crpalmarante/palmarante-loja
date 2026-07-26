from datetime import datetime
from modules.notification.domain.entities.notification import (
    Notification, Task, Alert, Approval, Activity, Reminder, Watcher, Mention,
    NotificationPriority, NotificationChannel, TaskStatus, ApprovalStatus,
    AlertSeverity, ActivityType,
)


class NotificationService:
    def __init__(self, repo):
        self._repo = repo

    def send_notification(self, user_id: str, title: str, message: str,
                          priority: str = 'normal', channel: str = 'inbox',
                          entity_type: str = '', entity_id: str = '',
                          action_url: str = '', icon: str = '', category: str = '') -> Notification:
        n = Notification(
            user_id=user_id, title=title, message=message,
            priority=NotificationPriority(priority),
            channel=NotificationChannel(channel) if channel else NotificationChannel.INBOX,
            entity_type=entity_type, entity_id=entity_id,
            action_url=action_url, icon=icon, category=category,
        )
        return self._repo.save_notification(n)

    def mark_read(self, notification_id: str):
        self._repo.mark_notification_read(notification_id)

    def mark_all_read(self, user_id: str):
        self._repo.mark_all_user_read(user_id)

    def get_unread_count(self, user_id: str) -> int:
        return self._repo.count_unread(user_id)

    def get_user_notifications(self, user_id: str, limit: int = 50) -> list:
        return self._repo.find_user_notifications(user_id, limit)


class TaskService:
    def __init__(self, repo):
        self._repo = repo

    def create_task(self, title: str, assignee_id: str,
                    priority: str = 'normal', description: str = '',
                    due_date: str = '', entity_type: str = '', entity_id: str = '',
                    created_by: str = '', category: str = '', tags: list = None) -> Task:
        t = Task(
            title=title, assignee_id=assignee_id,
            priority=NotificationPriority(priority),
            description=description,
            due_date=datetime.fromisoformat(due_date) if due_date else None,
            entity_type=entity_type, entity_id=entity_id,
            created_by=created_by, category=category, tags=tags or [],
        )
        return self._repo.save_task(t)

    def complete_task(self, task_id: str):
        t = self._repo.find_task(task_id)
        if t and t.status != TaskStatus.COMPLETED:
            t.complete()
            self._repo.save_task(t)

    def cancel_task(self, task_id: str):
        t = self._repo.find_task(task_id)
        if t:
            t.cancel()
            self._repo.save_task(t)

    def start_task(self, task_id: str):
        t = self._repo.find_task(task_id)
        if t and t.status == TaskStatus.PENDING:
            t.start()
            self._repo.save_task(t)

    def get_user_tasks(self, user_id: str, status: str = '') -> list:
        s = TaskStatus(status) if status else None
        return self._repo.find_user_tasks(user_id, s)

    def get_pending_tasks(self, user_id: str) -> list:
        return self._repo.find_pending_tasks(user_id)

    def get_overdue_tasks(self) -> list:
        return self._repo.find_overdue_tasks()


class AlertService:
    def __init__(self, repo):
        self._repo = repo

    def create_alert(self, user_id: str, title: str, message: str,
                     severity: str = 'info', entity_type: str = '', entity_id: str = '',
                     action_url: str = '', expires_at: str = '') -> Alert:
        a = Alert(
            user_id=user_id, title=title, message=message,
            severity=AlertSeverity(severity),
            entity_type=entity_type, entity_id=entity_id,
            action_url=action_url,
            expires_at=datetime.fromisoformat(expires_at) if expires_at else None,
        )
        return self._repo.save_alert(a)

    def acknowledge(self, alert_id: str):
        a = self._repo.find_user_alerts('', True)
        for al in self._repo._alerts.values():
            if al._id == alert_id:
                al.acknowledge()
                break

    def get_user_alerts(self, user_id: str) -> list:
        return self._repo.find_user_alerts(user_id)

    def get_active_alerts(self) -> list:
        return self._repo.find_active_alerts()


class ApprovalService:
    def __init__(self, repo):
        self._repo = repo

    def create_approval(self, title: str, target_type: str, target_id: str,
                        requester_id: str, approver_ids: list,
                        priority: str = 'normal', deadline: str = '',
                        escalation_minutes: int = 0) -> Approval:
        a = Approval(
            title=title, target_type=target_type, target_id=target_id,
            requester_id=requester_id, approver_ids=approver_ids,
            priority=NotificationPriority(priority),
            deadline=datetime.fromisoformat(deadline) if deadline else None,
            escalation_minutes=escalation_minutes,
        )
        return self._repo.save_approval(a)

    def approve(self, approval_id: str, user_id: str, reason: str = ''):
        a = self._repo.find_approval(approval_id)
        if a and a.status == ApprovalStatus.PENDING:
            a.approve(user_id, reason)
            self._repo.save_approval(a)
        return a

    def reject(self, approval_id: str, user_id: str, reason: str = ''):
        a = self._repo.find_approval(approval_id)
        if a and a.status == ApprovalStatus.PENDING:
            a.reject(user_id, reason)
            self._repo.save_approval(a)
        return a

    def get_user_pending_approvals(self, user_id: str) -> list:
        return self._repo.find_user_pending_approvals(user_id)

    def get_target_approvals(self, target_type: str, target_id: str) -> list:
        return self._repo.find_target_approvals(target_type, target_id)


class ActivityService:
    def __init__(self, repo):
        self._repo = repo

    def log(self, entity_type: str, entity_id: str, activity_type: str,
            user_id: str, description: str, metadata: dict = None) -> Activity:
        a = Activity(
            entity_type=entity_type, entity_id=entity_id,
            activity_type=ActivityType(activity_type),
            user_id=user_id, description=description, metadata=metadata or {},
        )
        return self._repo.save_activity(a)

    def get_entity_activities(self, entity_type: str, entity_id: str, limit: int = 50) -> list:
        return self._repo.find_entity_activities(entity_type, entity_id, limit)

    def get_recent_activities(self, limit: int = 50) -> list:
        return self._repo.find_recent_activities(limit)


class ReminderService:
    def __init__(self, repo):
        self._repo = repo

    def create_reminder(self, user_id: str, title: str, remind_at: str,
                        message: str = '', entity_type: str = '', entity_id: str = '',
                        recurring: str = '') -> Reminder:
        r = Reminder(
            user_id=user_id, title=title,
            remind_at=datetime.fromisoformat(remind_at),
            message=message, entity_type=entity_type, entity_id=entity_id,
            recurring=recurring,
        )
        return self._repo.save_reminder(r)

    def get_due_reminders(self) -> list:
        due = self._repo.find_due_reminders()
        for r in due:
            r.fire()
        return due


class WatcherService:
    def __init__(self, repo):
        self._repo = repo

    def watch(self, user_id: str, entity_type: str, entity_id: str) -> Watcher:
        return self._repo.save_watcher(Watcher(
            user_id=user_id, entity_type=entity_type, entity_id=entity_id))
    def unwatch(self, user_id: str, entity_type: str, entity_id: str):
        self._repo.remove_watcher(user_id, entity_type, entity_id)
    def get_watchers(self, entity_type: str, entity_id: str) -> list:
        return self._repo.find_entity_watchers(entity_type, entity_id)
    def is_watching(self, user_id: str, entity_type: str, entity_id: str) -> bool:
        return self._repo.is_watching(user_id, entity_type, entity_id)


class MentionService:
    def __init__(self, repo):
        self._repo = repo

    def create_mention(self, user_id: str, mentioned_by: str,
                       entity_type: str, entity_id: str, context: str = '') -> Mention:
        m = Mention(
            user_id=user_id, mentioned_by=mentioned_by,
            entity_type=entity_type, entity_id=entity_id, context=context,
        )
        return self._repo.save_mention(m)

    def get_user_mentions(self, user_id: str, unread_only: bool = True) -> list:
        return self._repo.find_user_mentions(user_id, unread_only)
    def mark_read(self, mention_id: str):
        self._repo.mark_mention_read(mention_id)


class AutomationService:
    def __init__(self, repo, notif_svc=None, task_svc=None):
        self._repo = repo
        self._notif_svc = notif_svc or NotificationService(repo)
        self._task_svc = task_svc or TaskService(repo)

    def process_overdue_tasks(self) -> list:
        overdue = self._repo.find_overdue_tasks()
        created = []
        for t in overdue:
            n = self._notif_svc.send_notification(
                user_id=t.assignee_id,
                title=f'Tarefa atrasada: {t.title}',
                message=f'A tarefa "{t.title}" venceu em {t.due_date.strftime("%d/%m/%Y")}.',
                priority='high', entity_type='task', entity_id=t._id,
                icon='⚠️',
            )
            created.append(n)
        return created

    def process_overdue_approvals(self) -> list:
        overdue = self._repo.find_overdue_approvals()
        escalated = []
        for a in overdue:
            for approver_id in a.approver_ids:
                n = self._notif_svc.send_notification(
                    user_id=approver_id,
                    title=f'Aprovação urgente: {a.title}',
                    message=f'A aprovação "{a.title}" está pendente além do prazo.',
                    priority='urgent', entity_type='approval', entity_id=a._id,
                    icon='🔴',
                )
                escalated.append(n)
        return escalated

    def process_due_reminders(self) -> list:
        from modules.notification.application.services.notification_service import ReminderService
        rsvc = ReminderService(self._repo)
        due = rsvc.get_due_reminders()
        created = []
        for r in due:
            n = self._notif_svc.send_notification(
                user_id=r.user_id, title=r.title, message=r.message or r.title,
                entity_type=r.entity_type, entity_id=r.entity_id, icon='⏰',
            )
            created.append(n)
        return created
