import pytest
from datetime import datetime, timedelta
from modules.notification.domain.entities.notification import (
    Notification, Task, Alert, Approval, Activity, Reminder, Watcher, Mention,
    NotificationPriority, TaskStatus, ApprovalStatus, AlertSeverity, ActivityType,
)
from modules.notification.infrastructure.postgres.notification_repository_memory import NotificationRepositoryMemory
from modules.notification.application.services.notification_service import (
    NotificationService, TaskService, AlertService, ApprovalService,
    ActivityService, ReminderService, WatcherService, MentionService,
    AutomationService,
)


@pytest.fixture
def repo():
    return NotificationRepositoryMemory()


@pytest.fixture
def notif_svc(repo):
    return NotificationService(repo)


@pytest.fixture
def task_svc(repo):
    return TaskService(repo)


@pytest.fixture
def approval_svc(repo):
    return ApprovalService(repo)


@pytest.fixture
def activity_svc(repo):
    return ActivityService(repo)


@pytest.fixture
def watcher_svc(repo):
    return WatcherService(repo)


@pytest.fixture
def mention_svc(repo):
    return MentionService(repo)


# ── Domain ─────────────────────────────────────────────────
class TestNotificationEntity:
    def test_create(self):
        n = Notification(user_id='user-001', title='Teste', message='Mensagem')
        assert n.user_id == 'user-001'
        assert not n.read
        assert n.priority == NotificationPriority.NORMAL

    def test_mark_read(self):
        n = Notification(user_id='user-001', title='Test', message='Msg')
        n.mark_read()
        assert n.read
        assert n.read_at is not None

    def test_to_dict(self):
        n = Notification(user_id='user-001', title='Test', message='Msg')
        d = n.to_dict()
        assert d['user_id'] == 'user-001'
        assert d['title'] == 'Test'


class TestTaskEntity:
    def test_create(self):
        t = Task(title='Tarefa', assignee_id='user-001')
        assert t.status == TaskStatus.PENDING

    def test_complete(self):
        t = Task(title='Tarefa', assignee_id='user-001')
        t.complete()
        assert t.status == TaskStatus.COMPLETED
        assert t.completed_at is not None

    def test_overdue(self):
        t = Task(title='Tarefa', assignee_id='user-001',
                  due_date=datetime.now() - timedelta(days=1))
        assert t.overdue

    def test_not_overdue_when_completed(self):
        t = Task(title='Tarefa', assignee_id='user-001',
                  due_date=datetime.now() - timedelta(days=1))
        t.complete()
        assert not t.overdue

    def test_to_dict(self):
        t = Task(title='Tarefa', assignee_id='user-001', tags=['urgente'])
        d = t.to_dict()
        assert d['title'] == 'Tarefa'
        assert 'urgente' in d['tags']


class TestApprovalEntity:
    def test_create(self):
        a = Approval(title='Aprovacao', target_type='order', target_id='ord-001',
                      requester_id='user-001', approver_ids=['user-002'])
        assert a.status == ApprovalStatus.PENDING

    def test_approve(self):
        a = Approval(title='Test', target_type='order', target_id='ord-001',
                      requester_id='user-001', approver_ids=['user-002'])
        a.approve('user-002', 'ok')
        assert a.status == ApprovalStatus.APPROVED
        assert a.decided_by == 'user-002'

    def test_reject(self):
        a = Approval(title='Test', target_type='order', target_id='ord-001',
                      requester_id='user-001', approver_ids=['user-002'])
        a.reject('user-002', 'recusado')
        assert a.status == ApprovalStatus.REJECTED
        assert a.rejection_reason == 'recusado'

    def test_overdue(self):
        a = Approval(title='Test', target_type='order', target_id='ord-001',
                      requester_id='user-001', approver_ids=['user-002'],
                      deadline=datetime.now() - timedelta(hours=1))
        assert a.overdue


class TestActivityEntity:
    def test_create(self):
        a = Activity(entity_type='order', entity_id='ord-001',
                      activity_type=ActivityType.CREATED, user_id='user-001',
                      description='Pedido criado')
        assert a.activity_type == ActivityType.CREATED


class TestReminderEntity:
    def test_should_fire(self):
        r = Reminder(user_id='user-001', title='Lembrete',
                      remind_at=datetime.now() - timedelta(minutes=5))
        assert r.should_fire

    def test_should_not_fire_after_fired(self):
        r = Reminder(user_id='user-001', title='Lembrete',
                      remind_at=datetime.now() - timedelta(minutes=5))
        r.fire()
        assert not r.should_fire


# ── Repository ─────────────────────────────────────────────
class TestNotificationRepository:
    def test_save_and_find_notification(self, repo):
        n = Notification(user_id='user-001', title='Test', message='Msg')
        saved = repo.save_notification(n)
        assert saved._id
        found = repo.find_notification(saved._id)
        assert found.title == 'Test'

    def test_count_unread(self, repo):
        repo.save_notification(Notification(user_id='user-001', title='A', message=''))
        repo.save_notification(Notification(user_id='user-001', title='B', message=''))
        n3 = repo.save_notification(Notification(user_id='user-001', title='C', message=''))
        n3.mark_read()
        assert repo.count_unread('user-001') == 2

    def test_mark_all_read(self, repo):
        repo.save_notification(Notification(user_id='user-001', title='A', message=''))
        repo.save_notification(Notification(user_id='user-001', title='B', message=''))
        repo.mark_all_user_read('user-001')
        assert repo.count_unread('user-001') == 0

    def test_find_overdue_tasks(self, repo):
        repo.save_task(Task(title='Atrasada', assignee_id='user-001',
                             due_date=datetime.now() - timedelta(days=1)))
        repo.save_task(Task(title='Futura', assignee_id='user-001',
                             due_date=datetime.now() + timedelta(days=1)))
        assert len(repo.find_overdue_tasks()) == 1

    def test_find_pending_approvals(self, repo):
        repo.save_approval(Approval(title='A', target_type='order', target_id='o1',
                                     requester_id='u1', approver_ids=['u2']))
        repo.save_approval(Approval(title='B', target_type='order', target_id='o2',
                                     requester_id='u1', approver_ids=['u2']))
        assert len(repo.find_user_pending_approvals('u2')) == 2

    def test_watcher(self, repo):
        w = Watcher(user_id='user-001', entity_type='order', entity_id='ord-001')
        repo.save_watcher(w)
        assert repo.is_watching('user-001', 'order', 'ord-001')
        repo.remove_watcher('user-001', 'order', 'ord-001')
        assert not repo.is_watching('user-001', 'order', 'ord-001')

    def test_dashboard(self, repo):
        repo.save_notification(Notification(user_id='user-001', title='N', message=''))
        repo.save_task(Task(title='T', assignee_id='user-001'))
        repo.save_approval(Approval(title='A', target_type='order', target_id='o1',
                                     requester_id='u1', approver_ids=['user-001']))
        dash = repo.dashboard('user-001')
        assert dash['unread_notifications'] == 1
        assert dash['pending_tasks'] == 1
        assert dash['pending_approvals'] == 1


# ── Services ───────────────────────────────────────────────
class TestNotificationService:
    def test_send_and_list(self, notif_svc, repo):
        notif_svc.send_notification('user-001', 'Título', 'Mensagem')
        assert repo.count_unread('user-001') == 1

    def test_mark_read(self, notif_svc, repo):
        n = notif_svc.send_notification('user-001', 'T', 'M')
        notif_svc.mark_read(n._id)
        assert repo.count_unread('user-001') == 0

    def test_mark_all_read(self, notif_svc, repo):
        notif_svc.send_notification('user-001', 'A', '')
        notif_svc.send_notification('user-001', 'B', '')
        notif_svc.mark_all_read('user-001')
        assert repo.count_unread('user-001') == 0


class TestTaskService:
    def test_crud(self, task_svc, repo):
        t = task_svc.create_task('Nova tarefa', 'user-001', priority='high',
                                  due_date='2026-08-01T00:00:00', category='vendas')
        assert t._id
        assert t.priority == NotificationPriority.HIGH
        tasks = task_svc.get_user_tasks('user-001')
        assert len(tasks) == 1
        task_svc.complete_task(t._id)
        assert repo.find_task(t._id).status == TaskStatus.COMPLETED

    def test_start(self, task_svc):
        t = task_svc.create_task('Iniciar', 'user-001')
        task_svc.start_task(t._id)
        assert task_svc._repo.find_task(t._id).status == TaskStatus.IN_PROGRESS


class TestApprovalService:
    def test_approve_flow(self, approval_svc):
        a = approval_svc.create_approval('Aprovar pedido', 'order', 'ord-001',
                                          'user-001', ['user-002', 'user-003'],
                                          deadline='2026-07-27T00:00:00')
        assert a.status == ApprovalStatus.PENDING
        pending = approval_svc.get_user_pending_approvals('user-002')
        assert len(pending) == 1
        approval_svc.approve(a._id, 'user-002', 'Autorizado')
        assert approval_svc._repo.find_approval(a._id).status == ApprovalStatus.APPROVED

    def test_reject(self, approval_svc):
        a = approval_svc.create_approval('Rejeitar', 'order', 'ord-002',
                                          'user-001', ['user-002'])
        approval_svc.reject(a._id, 'user-002', 'Fora do orçamento')
        assert approval_svc._repo.find_approval(a._id).status == ApprovalStatus.REJECTED


class TestActivityService:
    def test_log_and_retrieve(self, activity_svc):
        activity_svc.log('order', 'ord-001', 'created', 'user-001', 'Pedido criado')
        activity_svc.log('order', 'ord-001', 'approved', 'user-002', 'Aprovado')
        items = activity_svc.get_entity_activities('order', 'ord-001')
        assert len(items) == 2

    def test_recent(self, activity_svc):
        activity_svc.log('order', 'ord-001', 'created', 'u1', 'Criado')
        recent = activity_svc.get_recent_activities()
        assert len(recent) == 1


class TestWatcherService:
    def test_watch(self, watcher_svc):
        w = watcher_svc.watch('user-001', 'order', 'ord-001')
        assert w._id
        assert watcher_svc.is_watching('user-001', 'order', 'ord-001')
        assert not watcher_svc.is_watching('user-002', 'order', 'ord-001')

    def test_unwatch(self, watcher_svc):
        watcher_svc.watch('user-001', 'order', 'ord-001')
        watcher_svc.unwatch('user-001', 'order', 'ord-001')
        assert not watcher_svc.is_watching('user-001', 'order', 'ord-001')

    def test_get_watchers(self, watcher_svc):
        watcher_svc.watch('user-001', 'order', 'ord-001')
        watcher_svc.watch('user-002', 'order', 'ord-001')
        watchers = watcher_svc.get_watchers('order', 'ord-001')
        assert len(watchers) == 2


class TestMentionService:
    def test_mention(self, mention_svc):
        m = mention_svc.create_mention('user-002', 'user-001', 'order', 'ord-001', '@user-002 revise')
        assert m._id
        mentions = mention_svc.get_user_mentions('user-002')
        assert len(mentions) == 1
        mention_svc.mark_read(m._id)
        assert mention_svc.get_user_mentions('user-002', unread_only=True) == []


class TestAutomationService:
    def test_process_overdue_tasks(self, repo):
        notif_svc = NotificationService(repo)
        task_svc = TaskService(repo)
        auto = AutomationService(repo, notif_svc, task_svc)
        task_svc.create_task('Tarefa atrasada', 'user-001',
                              due_date=(datetime.now() - timedelta(days=1)).isoformat())
        n = auto.process_overdue_tasks()
        assert len(n) >= 1
        assert repo.count_unread('user-001') >= 1
