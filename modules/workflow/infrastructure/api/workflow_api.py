import uvicorn
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from modules.workflow.infrastructure.postgres.memory_repository import InMemoryWorkflowRepository
from modules.workflow.application.services.workflow_engine import WorkflowEngine
from modules.workflow.domain.entities.workflow import Workflow
from modules.workflow.domain.entities.state import WorkflowState, StateType
from modules.workflow.domain.entities.transition import WorkflowTransition
from modules.workflow.domain.entities.rule import WorkflowRule, RuleType, RuleOperator

app = FastAPI(title='BusinessCore — Workflow Platform', version='1.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

repo = InMemoryWorkflowRepository()
engine = WorkflowEngine(repo)


# ── Workflow Definitions ─────────────────────────────────────
@app.get('/api/workflows/dashboard')
def dashboard():
    return {'data': engine.get_dashboard()}


@app.get('/api/workflows')
def list_workflows(document_type: str = Query('')):
    wfs = repo.find_all_workflows(document_type)
    return {'data': [{'id': w._id, 'name': w.name, 'code': w.code,
                      'document_type': w.document_type, 'status': w.status.value} for w in wfs]}


@app.post('/api/workflows')
def create_workflow(body: dict):
    w = Workflow(name=body['name'], code=body['code'],
                 description=body.get('description', ''),
                 document_type=body.get('document_type', ''))
    repo.save_workflow(w)
    return {'data': {'id': w._id, 'name': w.name, 'code': w.code}}


@app.get('/api/workflows/{wf_id}')
def get_workflow(wf_id: str):
    w = repo.find_workflow_by_id(wf_id)
    if not w:
        raise HTTPException(404, 'Workflow not found')
    states = repo.find_states_by_workflow(wf_id)
    transitions = repo.find_transitions_by_workflow(wf_id)
    return {'data': {
        'id': w._id, 'name': w.name, 'code': w.code,
        'description': w.description, 'document_type': w.document_type,
        'status': w.status.value,
        'states': [{'id': s._id, 'name': s.name, 'code': s.code, 'type': s.type.value} for s in states],
        'transitions': [{'id': t._id, 'name': t.name, 'code': t.code,
                         'from': t.from_state_id, 'to': t.to_state_id,
                         'requires_approval': t.requires_approval} for t in transitions],
    }}


# ── States ───────────────────────────────────────────────────
@app.get('/api/workflows/{wf_id}/states')
def list_states(wf_id: str):
    states = repo.find_states_by_workflow(wf_id)
    return {'data': [{'id': s._id, 'name': s.name, 'code': s.code,
                      'type': s.type.value, 'color': s.color, 'sort_order': s.sort_order} for s in states]}


@app.post('/api/workflows/{wf_id}/states')
def add_state(wf_id: str, body: dict):
    s = WorkflowState(workflow_id=wf_id, name=body['name'], code=body['code'],
                      type=StateType(body.get('type', 'intermediate')),
                      color=body.get('color', '#1a73e8'),
                      description=body.get('description', ''),
                      sort_order=body.get('sort_order', 0))
    repo.save_state(s)
    return {'data': {'id': s._id, 'name': s.name}}


# ── Transitions ──────────────────────────────────────────────
@app.get('/api/workflows/{wf_id}/transitions')
def list_transitions(wf_id: str):
    transitions = repo.find_transitions_by_workflow(wf_id)
    return {'data': [{'id': t._id, 'name': t.name, 'code': t.code,
                      'from': t.from_state_id, 'to': t.to_state_id,
                      'requires_approval': t.requires_approval} for t in transitions]}


@app.post('/api/workflows/{wf_id}/transitions')
def add_transition(wf_id: str, body: dict):
    t = WorkflowTransition(workflow_id=wf_id, name=body['name'], code=body['code'],
                           from_state_id=body['from_state_id'],
                           to_state_id=body['to_state_id'],
                           requires_approval=body.get('requires_approval', False),
                           approval_count=body.get('approval_count', 1),
                           sort_order=body.get('sort_order', 0))
    repo.save_transition(t)
    return {'data': {'id': t._id, 'name': t.name}}


# ── Rules ────────────────────────────────────────────────────
@app.get('/api/workflows/{wf_id}/rules')
def list_rules(wf_id: str):
    rules = repo.find_rules_by_workflow(wf_id)
    return {'data': [{'id': r._id, 'name': r.name, 'type': r.rule_type.value,
                      'transition_id': r.transition_id, 'field': r.field,
                      'operator': r.operator.value, 'value': r.value} for r in rules]}


@app.post('/api/workflows/{wf_id}/rules')
def add_rule(wf_id: str, body: dict):
    r = WorkflowRule(workflow_id=wf_id, name=body['name'],
                     rule_type=RuleType(body.get('rule_type', 'condition')),
                     transition_id=body.get('transition_id', ''),
                     field=body.get('field', ''), operator=RuleOperator(body.get('operator', 'equals')),
                     value=body.get('value', ''), error_message=body.get('error_message', ''),
                     target_role=body.get('target_role', ''))
    repo.save_rule(r)
    return {'data': {'id': r._id, 'name': r.name}}


# ── Workflow Instances ───────────────────────────────────────
@app.get('/api/workflow-instances')
def list_instances(workflow_id: str = Query(''), status: str = Query(''),
                   document_type: str = Query(''), document_id: str = Query('')):
    if document_type and document_id:
        instances = repo.find_instances_by_document(document_type, document_id)
    elif workflow_id:
        instances = repo.find_instances_by_workflow(workflow_id, status)
    else:
        instances = list(repo._instances.values())
    return {'data': [{'id': i._id, 'workflow_id': i.workflow_id,
                      'document_type': i.document_type, 'document_id': i.document_id,
                      'current_state_id': i.current_state_id, 'status': i.status.value,
                      'started_at': i.started_at.isoformat() if i.started_at else ''} for i in instances]}


@app.post('/api/workflow-instances')
def start_instance(body: dict):
    try:
        instance = engine.start(body['workflow_id'], body['document_type'],
                                body['document_id'], body.get('document_data', {}))
        return {'data': {'id': instance._id, 'current_state_id': instance.current_state_id, 'status': instance.status.value}}
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.post('/api/workflow-instances/{inst_id}/transition')
def execute_transition(inst_id: str, body: dict):
    try:
        instance = engine.execute_transition(
            inst_id, transition_code=body.get('transition_code', ''),
            to_state_id=body.get('to_state_id', ''),
            comment=body.get('comment', ''), performed_by=body.get('performed_by', ''))
        return {'data': {'id': instance._id, 'current_state_id': instance.current_state_id, 'status': instance.status.value}}
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.post('/api/workflow-instances/{inst_id}/cancel')
def cancel_instance(inst_id: str, body: dict = None):
    try:
        instance = engine.cancel(inst_id, (body or {}).get('reason', ''))
        return {'data': {'id': instance._id, 'status': instance.status.value}}
    except ValueError as e:
        raise HTTPException(404, str(e))


# ── History ──────────────────────────────────────────────────
@app.get('/api/workflow-instances/{inst_id}/history')
def instance_history(inst_id: str):
    history = repo.find_history_by_instance(inst_id)
    return {'data': [{'id': h._id, 'action': h.action,
                      'from_state': h.from_state_id, 'to_state': h.to_state_id,
                      'comment': h.comment, 'performed_by': h.performed_by,
                      'created_at': h.created_at.isoformat() if h.created_at else ''} for h in history]}


# ── Approvals ────────────────────────────────────────────────
@app.get('/api/approvals')
def list_approvals(role: str = Query(''), instance_id: str = Query('')):
    if instance_id:
        approvals = repo.find_approvals_by_instance(instance_id)
    else:
        approvals = repo.find_pending_approvals(role)
    return {'data': [{'id': a._id, 'instance_id': a.instance_id,
                      'transition_id': a.transition_id,
                      'status': a.status.value, 'role': a.role} for a in approvals]}


@app.post('/api/approvals/{approval_id}/approve')
def approve_approval(approval_id: str, body: dict = None):
    try:
        instance = engine.approve(approval_id, (body or {}).get('user', ''),
                                   (body or {}).get('comment', ''))
        return {'data': {'instance_id': instance._id, 'current_state': instance.current_state_id}}
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.post('/api/approvals/{approval_id}/reject')
def reject_approval(approval_id: str, body: dict = None):
    try:
        approval = engine.reject(approval_id, (body or {}).get('user', ''),
                                  (body or {}).get('comment', ''))
        return {'data': {'approval_id': approval._id, 'status': approval.status.value}}
    except ValueError as e:
        raise HTTPException(400, str(e))


# ── Dashboard ────────────────────────────────────────────────
@app.get('/api/workflows/dashboard')
def dashboard():
    return {'data': engine.get_dashboard()}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8006)
