import uvicorn
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from modules.notification.infrastructure.postgres.notification_repository_memory import NotificationRepositoryMemory
from modules.notification.application.services.notification_service import (
    NotificationService, TaskService, AlertService, ApprovalService,
    ActivityService, ReminderService, WatcherService, MentionService,
    AutomationService,
)

app = FastAPI(title='BusinessCore — Notification & Task Platform', version='1.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

repo = NotificationRepositoryMemory()
notif_svc = NotificationService(repo)
task_svc = TaskService(repo)
alert_svc = AlertService(repo)
approval_svc = ApprovalService(repo)
activity_svc = ActivityService(repo)
reminder_svc = ReminderService(repo)
watcher_svc = WatcherService(repo)
mention_svc = MentionService(repo)
auto_svc = AutomationService(repo, notif_svc, task_svc)


# ── Dashboard ──────────────────────────────────────────────
@app.get('/api/notifications/dashboard')
def dashboard(user_id: str = 'user-001'):
    return {'data': repo.dashboard(user_id)}


# ── Notifications ──────────────────────────────────────────
@app.get('/api/notifications')
def list_notifications(user_id: str = 'user-001', unread_only: bool = False, limit: int = 50):
    if unread_only:
        items = repo.find_unread_notifications(user_id)[:limit]
    else:
        items = repo.find_user_notifications(user_id, limit)
    return {'data': [n.to_dict() for n in items]}


@app.get('/api/notifications/unread-count')
def unread_count(user_id: str = 'user-001'):
    return {'data': {'count': repo.count_unread(user_id)}}


@app.post('/api/notifications')
def create_notification(body: dict):
    n = notif_svc.send_notification(
        user_id=body['user_id'], title=body['title'], message=body.get('message', ''),
        priority=body.get('priority', 'normal'), channel=body.get('channel', 'inbox'),
        entity_type=body.get('entity_type', ''), entity_id=body.get('entity_id', ''),
        action_url=body.get('action_url', ''), icon=body.get('icon', ''),
        category=body.get('category', ''),
    )
    return {'data': n.to_dict()}


@app.post('/api/notifications/{notification_id}/read')
def mark_notification_read(notification_id: str):
    notif_svc.mark_read(notification_id)
    return {'data': {'ok': True}}


@app.post('/api/notifications/read-all')
def mark_all_read(user_id: str = 'user-001'):
    notif_svc.mark_all_read(user_id)
    return {'data': {'ok': True}}


# ── Tasks ──────────────────────────────────────────────────
@app.get('/api/tasks')
def list_tasks(user_id: str = 'user-001', status: str = ''):
    return {'data': [t.to_dict() for t in task_svc.get_user_tasks(user_id, status)]}


@app.post('/api/tasks')
def create_task(body: dict):
    t = task_svc.create_task(
        title=body['title'], assignee_id=body.get('assignee_id', body['user_id']),
        priority=body.get('priority', 'normal'), description=body.get('description', ''),
        due_date=body.get('due_date', ''), entity_type=body.get('entity_type', ''),
        entity_id=body.get('entity_id', ''), created_by=body.get('user_id', ''),
        category=body.get('category', ''), tags=body.get('tags'),
    )
    return {'data': t.to_dict()}


@app.get('/api/tasks/pending')
def pending_tasks(user_id: str = 'user-001'):
    return {'data': [t.to_dict() for t in task_svc.get_pending_tasks(user_id)]}


@app.get('/api/tasks/overdue')
def overdue_tasks():
    return {'data': [t.to_dict() for t in task_svc.get_overdue_tasks()]}


@app.post('/api/tasks/{task_id}/complete')
def complete_task(task_id: str):
    task_svc.complete_task(task_id)
    return {'data': {'ok': True}}


@app.post('/api/tasks/{task_id}/cancel')
def cancel_task(task_id: str):
    task_svc.cancel_task(task_id)
    return {'data': {'ok': True}}


@app.post('/api/tasks/{task_id}/start')
def start_task(task_id: str):
    task_svc.start_task(task_id)
    return {'data': {'ok': True}}


# ── Alerts ─────────────────────────────────────────────────
@app.get('/api/alerts')
def list_alerts(user_id: str = 'user-001'):
    return {'data': [a.to_dict() for a in alert_svc.get_user_alerts(user_id)]}


@app.post('/api/alerts')
def create_alert(body: dict):
    a = alert_svc.create_alert(
        user_id=body['user_id'], title=body['title'], message=body.get('message', ''),
        severity=body.get('severity', 'info'), entity_type=body.get('entity_type', ''),
        entity_id=body.get('entity_id', ''), action_url=body.get('action_url', ''),
        expires_at=body.get('expires_at', ''),
    )
    return {'data': a.to_dict()}


@app.post('/api/alerts/{alert_id}/acknowledge')
def acknowledge_alert(alert_id: str):
    alert_svc.acknowledge(alert_id)
    return {'data': {'ok': True}}


@app.get('/api/alerts/active')
def active_alerts():
    return {'data': [a.to_dict() for a in alert_svc.get_active_alerts()]}


# ── Approvals ──────────────────────────────────────────────
@app.get('/api/approvals/pending')
def pending_approvals(user_id: str = 'user-001'):
    return {'data': [a.to_dict() for a in approval_svc.get_user_pending_approvals(user_id)]}


@app.post('/api/approvals')
def create_approval(body: dict):
    a = approval_svc.create_approval(
        title=body['title'], target_type=body['target_type'], target_id=body['target_id'],
        requester_id=body['requester_id'], approver_ids=body['approver_ids'],
        priority=body.get('priority', 'normal'), deadline=body.get('deadline', ''),
        escalation_minutes=body.get('escalation_minutes', 0),
    )
    return {'data': a.to_dict()}


@app.post('/api/approvals/{approval_id}/approve')
def approve(approval_id: str, body: dict):
    a = approval_svc.approve(approval_id, body.get('user_id', ''), body.get('reason', ''))
    if not a:
        raise HTTPException(404, 'Approval not found')
    return {'data': a.to_dict()}


@app.post('/api/approvals/{approval_id}/reject')
def reject(approval_id: str, body: dict):
    a = approval_svc.reject(approval_id, body.get('user_id', ''), body.get('reason', ''))
    if not a:
        raise HTTPException(404, 'Approval not found')
    return {'data': a.to_dict()}


# ── Activities ─────────────────────────────────────────────
@app.get('/api/activities')
def list_activities(entity_type: str = '', entity_id: str = '', limit: int = 50):
    if entity_type and entity_id:
        return {'data': [a.to_dict() for a in activity_svc.get_entity_activities(entity_type, entity_id, limit)]}
    return {'data': [a.to_dict() for a in activity_svc.get_recent_activities(limit)]}


@app.post('/api/activities')
def create_activity(body: dict):
    a = activity_svc.log(
        entity_type=body['entity_type'], entity_id=body['entity_id'],
        activity_type=body['activity_type'], user_id=body['user_id'],
        description=body['description'], metadata=body.get('metadata'),
    )
    return {'data': a.to_dict()}


@app.get('/api/activities/recent')
def recent_activities(limit: int = 20):
    return {'data': [a.to_dict() for a in activity_svc.get_recent_activities(limit)]}


# ── Reminders ──────────────────────────────────────────────
@app.get('/api/reminders')
def list_reminders(user_id: str = 'user-001'):
    return {'data': [r.to_dict() for r in reminder_svc._repo.find_user_reminders(user_id)]}


@app.post('/api/reminders')
def create_reminder(body: dict):
    r = reminder_svc.create_reminder(
        user_id=body['user_id'], title=body['title'], remind_at=body['remind_at'],
        message=body.get('message', ''), entity_type=body.get('entity_type', ''),
        entity_id=body.get('entity_id', ''), recurring=body.get('recurring', ''),
    )
    return {'data': r.to_dict()}


# ── Watchers ───────────────────────────────────────────────
@app.post('/api/watchers')
def add_watcher(body: dict):
    w = watcher_svc.watch(body['user_id'], body['entity_type'], body['entity_id'])
    return {'data': w.to_dict()}


@app.delete('/api/watchers')
def remove_watcher(user_id: str, entity_type: str, entity_id: str):
    watcher_svc.unwatch(user_id, entity_type, entity_id)
    return {'data': {'ok': True}}


@app.get('/api/watchers')
def list_watchers(entity_type: str, entity_id: str):
    return {'data': [w.to_dict() for w in watcher_svc.get_watchers(entity_type, entity_id)]}


@app.get('/api/watchers/check')
def check_watching(user_id: str, entity_type: str, entity_id: str):
    return {'data': {'watching': watcher_svc.is_watching(user_id, entity_type, entity_id)}}


# ── Mentions ───────────────────────────────────────────────
@app.get('/api/mentions')
def list_mentions(user_id: str = 'user-001', unread_only: bool = True):
    return {'data': [m.to_dict() for m in mention_svc.get_user_mentions(user_id, unread_only)]}


@app.post('/api/mentions')
def create_mention(body: dict):
    m = mention_svc.create_mention(
        user_id=body['user_id'], mentioned_by=body['mentioned_by'],
        entity_type=body['entity_type'], entity_id=body['entity_id'],
        context=body.get('context', ''),
    )
    return {'data': m.to_dict()}


@app.post('/api/mentions/{mention_id}/read')
def mark_mention_read(mention_id: str):
    mention_svc.mark_read(mention_id)
    return {'data': {'ok': True}}


# ── Automation ─────────────────────────────────────────────
@app.post('/api/automation/check-overdue')
def check_overdue():
    notifications = auto_svc.process_overdue_tasks()
    escalated = auto_svc.process_overdue_approvals()
    reminders = auto_svc.process_due_reminders()
    return {'data': {
        'overdue_task_notifications': len(notifications),
        'overdue_approval_escalations': len(escalated),
        'reminders_fired': len(reminders),
    }}


# ── Seed ───────────────────────────────────────────────────
def _seed():
    if not repo._notifications:
        notif_svc.send_notification('user-001', 'Bem-vindo ao sistema',
                                     'Sua conta foi criada com sucesso.', icon='🎉')
        notif_svc.send_notification('user-001', 'Pedido #2026-0001 aprovado',
                                     'O pedido de João da Silva foi aprovado.',
                                     entity_type='order', entity_id='ord-001', icon='📋')
        notif_svc.send_notification('user-002', 'Requisição de compra pendente',
                                     'A requisição REQ-001 aguarda sua aprovação.',
                                     priority='high', entity_type='requisition',
                                     entity_id='req-001', icon='⚠️')
        notif_svc.send_notification('user-001', 'Estoque baixo: Notebook Dell',
                                     'Restam apenas 2 unidades em estoque.',
                                     priority='high', category='inventory', icon='📦')

        task_svc.create_task('Revisar orçamento Q-001', 'user-001',
                              priority='high', due_date='2026-08-01T00:00:00',
                              entity_type='quotation', entity_id='q-001',
                              category='vendas')
        task_svc.create_task('Aprovar requisição REQ-001', 'user-002',
                              priority='high', due_date='2026-07-28T00:00:00',
                              entity_type='requisition', entity_id='req-001',
                              category='compras')
        task_svc.create_task('Atualizar contrato CT-001', 'user-001',
                              due_date='2026-08-15T00:00:00',
                              entity_type='contract', entity_id='ct-001',
                              category='contratos')

        approval_svc.create_approval('Pedido #2026-0002', 'order', 'ord-002',
                                      'user-001', ['user-002', 'user-003'],
                                      deadline='2026-07-27T00:00:00')
        approval_svc.create_approval('Requisição REQ-002', 'requisition', 'req-002',
                                      'user-002', ['user-001'],
                                      deadline='2026-07-29T00:00:00')

        activity_svc.log('order', 'ord-001', 'created', 'user-001',
                          'Pedido #2026-0001 criado')
        activity_svc.log('order', 'ord-001', 'approved', 'user-002',
                          'Pedido #2026-0001 aprovado')
        activity_svc.log('order', 'ord-001', 'status_change', 'system',
                          'Status alterado de pending para approved')

        alert_svc.create_alert('user-001', 'Certificado A1 expira em 15 dias',
                                'Renove o certificado digital da empresa matriz.',
                                severity='critical', entity_type='certificate',
                                entity_id='cert-001')
        alert_svc.create_alert('user-001', 'NF-e 000487 rejeitada',
                                'Erro de destinatário na NF-e 000487.',
                                severity='warning', entity_type='invoice',
                                entity_id='inv-001')

        reminder_svc.create_reminder('user-001', 'Reunião com fornecedor',
                                      '2026-07-26T14:00:00',
                                      message='Reunião com Dell para negociação de preços.',
                                      entity_type='supplier', entity_id='sup-001')


if __name__ == '__main__':
    _seed()
    uvicorn.run(app, host='0.0.0.0', port=8010)
