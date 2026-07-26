from fastapi import APIRouter, HTTPException, Query

from modules.sales.core.infrastructure.postgres.sales_repository_memory import SalesRepositoryMemory
from modules.sales.core.application.services.sales_orchestrator import SalesOrchestrator
from modules.sales.extensions.application.services.credit_service import CreditService
from modules.sales.extensions.application.services.availability_service import AvailabilityService
from modules.sales.extensions.application.services.recommendation_service import RecommendationService
from modules.sales.extensions.application.services.campaign_service import CampaignService
from modules.sales.extensions.application.services.price_simulation_service import PriceSimulationService
from modules.sales.extensions.application.services.margin_service import MarginService
from modules.sales.extensions.application.services.customer_dashboard_service import CustomerDashboardService
from modules.sales.extensions.application.services.policy_engine import PolicyEngine
from modules.sales.extensions.application.services.rules_engine import RulesEngine
from modules.sales.extensions.application.services.extended_services import (
    AgreementService, CalendarService, OrderSplitService,
    DeliverySchedulingService, CustomerPreferencesService,
    KpiEngine, ValidationEngine, AuditService, EventService,
    HookManager, SearchService, SalesIntelligence,
)
from modules.sales.extensions.domain.entities.bundle import SalesBundle, BundleItem
from modules.sales.extensions.domain.entities.campaign import Campaign, CampaignType, CampaignTarget
from modules.sales.extensions.domain.entities.policy import SalesPolicy, PolicyAction, PolicyScope
from modules.sales.extensions.domain.entities.rule import SalesRule, RuleCondition, RuleAction
from modules.sales.extensions.domain.entities.events import SalesEventType
from modules.sales.extensions.domain.entities.calendar import CalendarEventType

router = APIRouter(prefix='/api/sales')

repo = SalesRepositoryMemory()
sales = SalesOrchestrator(repo)
credit_svc = CreditService(repo)
avail_svc = AvailabilityService(repo)
rec_svc = RecommendationService(repo)
camp_svc = CampaignService(repo)
price_sim = PriceSimulationService(repo)
margin_svc = MarginService(repo)
cust_dash = CustomerDashboardService(repo)
policy_eng = PolicyEngine(repo)
rules_eng = RulesEngine(repo)
agr_svc = AgreementService(repo)
cal_svc = CalendarService(repo)
split_svc = OrderSplitService(repo)
delivery_sched = DeliverySchedulingService(repo)
pref_svc = CustomerPreferencesService(repo)
kpi_eng = KpiEngine(repo)
val_eng = ValidationEngine(repo)
audit_svc = AuditService(repo)
evt_svc = EventService(repo)
hook_mgr = HookManager()
search_svc = SearchService(repo)
intel_svc = SalesIntelligence(repo)


# ── Sales-001: Customer Credit ────────────────────────────────
@router.get('/ext/credit/{customer_id}')
def get_credit(customer_id: str):
    credit = credit_svc.get_or_create_credit(customer_id)
    if not credit:
        raise HTTPException(404, 'Credit not found')
    return {'data': {'id': credit._id, 'customer_id': credit.customer_id,
                     'credit_limit': credit.credit_limit,
                     'used_balance': credit.used_balance,
                     'available': credit.available_balance,
                     'status': credit.status.value}}


@router.post('/ext/credit/{customer_id}/limit')
def set_credit_limit(customer_id: str, body: dict):
    credit = credit_svc.set_limit(customer_id, body['limit'], body.get('notes', ''))
    return {'data': {'id': credit._id, 'credit_limit': credit.credit_limit}}


@router.post('/ext/credit/check-order')
def check_credit(body: dict):
    result = credit_svc.check_order(body['customer_id'], body['order_total'])
    return {'data': result}


# ── Sales-002: Availability (ATP) ─────────────────────────────
@router.get('/ext/availability/{item_id}')
def check_availability(item_id: str, warehouse_id: str = Query(''), quantity: float = Query(1)):
    result = avail_svc.check_availability(item_id, warehouse_id, quantity)
    return {'data': result}


@router.post('/ext/availability/check-lines')
def check_lines(body: dict):
    results = avail_svc.check_order_lines(body.get('lines', []), body.get('warehouse_id', ''))
    return {'data': results}


# ── Sales-003: Similar Products ───────────────────────────────
@router.get('/ext/similar/{item_id}')
def similar_products(item_id: str, limit: int = Query(3)):
    items = rec_svc.find_similar(item_id, limit)
    return {'data': items}


# ── Sales-004: Bundles / Kits ─────────────────────────────────
@router.get('/ext/bundles')
def list_bundles(item_id: str = Query('')):
    bundles = rec_svc.find_bundles(item_id)
    return {'data': [{'id': b._id, 'name': b.name, 'code': b.code,
                      'items': len(b.items or []), 'bundle_price': b.bundle_price,
                      'savings_pct': b.savings_pct, 'active': b.active}
                     for b in bundles]}


@router.post('/ext/bundles')
def create_bundle(body: dict):
    items = [BundleItem(**l) for l in body.get('items', [])]
    b = SalesBundle(name=body['name'], code=body.get('code', ''),
                    description=body.get('description', ''),
                    items=items, bundle_price=body.get('bundle_price', 0),
                    savings_pct=body.get('savings_pct', 0))
    repo.save_bundle(b)
    return {'data': {'id': b._id, 'name': b.name}}


# ── Sales-005/006: Cross/Up Selling ────────────────────────────
@router.get('/ext/cross-sell/{item_id}')
def cross_sell(item_id: str, limit: int = Query(3)):
    items = rec_svc.find_cross_sell(item_id, limit)
    return {'data': items}


@router.get('/ext/up-sell/{item_id}')
def up_sell(item_id: str, limit: int = Query(3)):
    items = rec_svc.find_up_sell(item_id, limit)
    return {'data': items}


# ── Sales-007: Campaigns ──────────────────────────────────────
@router.get('/ext/campaigns')
def list_campaigns():
    camps = repo.find_campaigns()
    return {'data': [{'id': c._id, 'name': c.name, 'code': c.code,
                      'type': c.campaign_type.value, 'value': c.value,
                      'active': c.active} for c in camps]}


@router.post('/ext/campaigns')
def create_campaign(body: dict):
    c = Campaign(
        name=body['name'], code=body.get('code', ''),
        campaign_type=CampaignType(body.get('campaign_type', 'percentage')),
        target=CampaignTarget(body.get('target', 'all')),
        value=body.get('value', 0),
        min_order_value=body.get('min_order_value', 0),
        customer_classes=body.get('customer_classes', []),
        valid_from=body.get('valid_from', ''),
        valid_to=body.get('valid_to', ''),
    )
    repo.save_campaign(c)
    return {'data': {'id': c._id, 'name': c.name}}


@router.post('/ext/campaigns/apply-best')
def apply_best_campaign(body: dict):
    result = camp_svc.apply_best(
        body.get('customer_id', ''),
        body.get('customer_class', ''),
        body.get('order_total', 0),
    )
    return {'data': result}


# ── Sales-008: Price Simulation ───────────────────────────────
@router.post('/ext/simulate/line')
def simulate_line(body: dict):
    result = price_sim.simulate(**{k: v for k, v in body.items()})
    return {'data': result}


@router.post('/ext/simulate/order')
def simulate_order(body: dict):
    result = price_sim.simulate_order(
        body.get('lines', []), body.get('freight', 0),
        body.get('commission_rate', 0), body.get('price_list_id', ''),
    )
    return {'data': result}


# ── Sales-009: Margin Analysis ────────────────────────────────
@router.post('/ext/margin/line')
def analyze_margin_line(body: dict):
    result = margin_svc.analyze_line(**{k: v for k, v in body.items()})
    return {'data': result}


@router.post('/ext/margin/order')
def analyze_margin_order(body: dict):
    result = margin_svc.analyze_order(body.get('lines', []))
    return {'data': result}


# ── Sales-010: Customer Dashboard ─────────────────────────────
@router.get('/ext/customer-dashboard/{customer_id}')
def customer_dashboard(customer_id: str):
    panel = cust_dash.get_panel(customer_id)
    return {'data': panel}


# ── Sales Policy Engine ───────────────────────────────────────
@router.get('/ext/policies')
def list_policies():
    policies = repo.find_policies()
    return {'data': [{'id': p._id, 'name': p.name, 'code': p.code,
                      'action': p.action.value, 'active': p.active}
                     for p in policies]}


@router.post('/ext/policies')
def create_policy(body: dict):
    p = SalesPolicy(
        name=body['name'], code=body.get('code', ''),
        description=body.get('description', ''),
        scope=PolicyScope(body.get('scope', 'global')),
        action=PolicyAction(body.get('action', 'warn')),
        condition_field=body.get('condition_field', ''),
        condition_operator=body.get('condition_operator', 'equals'),
        condition_value=body.get('condition_value', ''),
        action_value=body.get('action_value', ''),
        priority=body.get('priority', 0),
    )
    repo.save_policy(p)
    return {'data': {'id': p._id, 'name': p.name}}


@router.post('/ext/policies/evaluate')
def evaluate_policies(body: dict):
    results = policy_eng.evaluate_for_order(
        customer_id=body.get('customer_id', ''),
        customer_class=body.get('customer_class', ''),
        order_total=body.get('order_total', 0),
        channel=body.get('channel', ''),
        payment_method=body.get('payment_method', ''),
    )
    return {'data': results}


@router.post('/ext/policies/blockers')
def check_blockers(body: dict):
    blockers = policy_eng.check_blockers(
        customer_id=body.get('customer_id', ''),
        customer_class=body.get('customer_class', ''),
        order_total=body.get('order_total', 0),
        channel=body.get('channel', ''),
        payment_method=body.get('payment_method', ''),
    )
    return {'data': blockers}


# ── Sales Rules Engine ───────────────────────────────────────
@router.get('/ext/rules')
def list_rules():
    rules = repo.find_rules()
    return {'data': [{'id': r._id, 'name': r.name, 'code': r.code,
                      'condition_field': r.condition_field,
                      'action_field': r.action_field.value if hasattr(r.action_field, 'value') else r.action_field,
                      'action_value': r.action_value, 'active': r.active}
                     for r in rules]}


@router.post('/ext/rules')
def create_rule(body: dict):
    r = SalesRule(
        name=body['name'], code=body.get('code', ''),
        description=body.get('description', ''),
        condition_field=body.get('condition_field', ''),
        condition_operator=body.get('condition_operator', 'equals'),
        condition_value=body.get('condition_value', ''),
        action_field=RuleAction(body.get('action_field', 'apply_discount')),
        action_value=body.get('action_value', ''),
        priority=body.get('priority', 0),
    )
    repo.save_rule(r)
    return {'data': {'id': r._id, 'name': r.name}}


@router.post('/ext/rules/evaluate')
def evaluate_rules(body: dict):
    results = rules_eng.evaluate_for_order(
        customer_type=body.get('customer_type', ''),
        quantity=body.get('quantity', 0),
        total=body.get('total', 0),
        channel=body.get('channel', ''),
        item_category=body.get('item_category', ''),
        payment_method=body.get('payment_method', ''),
    )
    return {'data': results}


# ── Sales-011: Customer Agreements ──────────────────────────
@router.get('/ext/agreements/{customer_id}')
def list_agreements(customer_id: str):
    agreements = agr_svc.find_by_customer(customer_id)
    return {'data': [{'id': a._id, 'name': a.name,
                      'price_list_id': a.price_list_id,
                      'max_discount_pct': a.max_discount_pct,
                      'valid_from': a.valid_from, 'valid_to': a.valid_to,
                      'active': a.active, 'notes': a.notes}
                     for a in agreements]}


@router.post('/ext/agreements')
def create_agreement(body: dict):
    a = agr_svc.create(
        customer_id=body['customer_id'], name=body.get('name', ''),
        price_list_id=body.get('price_list_id', ''),
        max_discount_pct=body.get('max_discount_pct', 0),
        payment_method=body.get('payment_method', ''),
        installments=body.get('installments', 1),
        due_days=body.get('due_days', 30),
        delivery_term=body.get('delivery_term', ''),
        sales_rep=body.get('sales_rep', ''),
        valid_from=body.get('valid_from', ''),
        valid_to=body.get('valid_to', ''),
        notes=body.get('notes', ''),
    )
    return {'data': {'id': a._id}}


@router.post('/ext/agreements/apply-to-order')
def apply_agreement(body: dict):
    result = agr_svc.apply_to_order(body['customer_id'], body.get('order_data', {}))
    return {'data': result}


# ── Sales-012: Sales Calendar ───────────────────────────────
@router.get('/ext/calendar')
def list_calendar(date_from: str = Query(''), date_to: str = Query(''),
                  sales_rep: str = Query('')):
    events = cal_svc.list_events(date_from, date_to, sales_rep)
    return {'data': [{'id': e._id, 'title': e.title, 'date': e.date,
                      'time': e.time, 'event_type': e.event_type.value,
                      'customer_id': e.customer_id, 'customer_name': e.customer_name,
                      'document_id': e.document_id, 'status': e.status,
                      'color': e.color, 'description': e.description}
                     for e in events]}


@router.post('/ext/calendar')
def create_calendar_event(body: dict):
    ev = cal_svc.add_event(
        title=body['title'], date=body['date'],
        event_type=CalendarEventType(body.get('event_type', 'follow_up')),
        customer_id=body.get('customer_id', ''),
        customer_name=body.get('customer_name', ''),
        document_id=body.get('document_id', ''),
        sales_rep=body.get('sales_rep', ''),
        description=body.get('description', ''),
    )
    return {'data': {'id': ev._id}}


@router.post('/ext/calendar/from-order')
def calendar_from_order(body: dict):
    ev = cal_svc.generate_from_order(
        document_id=body['document_id'],
        customer_id=body['customer_id'],
        customer_name=body.get('customer_name', ''),
        expected_delivery=body['expected_delivery'],
        sales_rep=body.get('sales_rep', ''),
    )
    return {'data': {'id': ev._id}}


# ── Sales-013: Order Split Engine ──────────────────────────
@router.post('/ext/split/by-warehouse')
def split_by_warehouse(body: dict):
    result = split_svc.split_by_warehouse(body['document_id'], body.get('warehouse_map', {}))
    return {'data': result}


@router.post('/ext/split/by-availability')
def split_by_availability(body: dict):
    result = split_svc.split_by_availability(body['document_id'], body.get('lines', []))
    return {'data': result}


# ── Sales-014: Delivery Scheduling ─────────────────────────
@router.post('/ext/delivery-schedule')
def schedule_delivery(body: dict):
    result = delivery_sched.schedule(
        document_id=body['document_id'],
        delivery_type=body.get('delivery_type', 'standard'),
        scheduled_date=body.get('scheduled_date', ''),
        address=body.get('address', ''),
        notes=body.get('notes', ''),
        created_by=body.get('created_by', ''),
    )
    return {'data': result}


@router.get('/ext/delivery-estimate')
def estimate_delivery(customer_zip: str = Query('')):
    result = delivery_sched.estimate(customer_zip)
    return {'data': result}


# ── Sales-015: Customer Preferences ────────────────────────
@router.get('/ext/preferences/{customer_id}')
def get_preferences(customer_id: str):
    prefs = pref_svc.get(customer_id)
    return {'data': prefs}


@router.post('/ext/preferences/{customer_id}')
def set_preferences(customer_id: str, body: dict):
    prefs = pref_svc.set(customer_id=customer_id, **body)
    return {'data': prefs}


# ── Sales-016: Sales KPI Engine ────────────────────────────
@router.get('/ext/kpi')
def get_kpi(days: int = Query(30)):
    result = kpi_eng.calculate(days)
    return {'data': result}


# ── Sales-017: Document Templates ──────────────────────────
@router.get('/ext/doc-templates')
def list_doc_templates():
    return {'data': []}


@router.post('/ext/doc-templates')
def create_doc_template(body: dict):
    from datetime import datetime
    tpl = {
        '_id': f'dtpl_{datetime.now().timestamp()}',
        'name': body.get('name', ''),
        'context': body.get('context', ''),
        'header_fields': body.get('header_fields', []),
        'line_behaviors': body.get('line_behaviors', []),
        'payment_rules': body.get('payment_rules', []),
        'created_at': datetime.now().isoformat(),
    }
    return {'data': tpl}


# ── Sales-018: Validation Engine ───────────────────────────
@router.post('/ext/validate/order')
def validate_order(body: dict):
    result = val_eng.validate_order(**{k: v for k, v in body.items()})
    return {'data': result}


# ── Sales-019: Audit Trail ─────────────────────────────────
@router.post('/ext/audit')
def record_audit(body: dict):
    entry = audit_svc.record(
        entity_type=body['entity_type'], entity_id=body['entity_id'],
        field_name=body.get('field_name', ''),
        old_value=body.get('old_value', ''),
        new_value=body.get('new_value', ''),
        changed_by=body.get('changed_by', ''),
        change_type=body.get('change_type', 'update'),
        document_id=body.get('document_id', ''),
    )
    return {'data': {'id': entry._id}}


@router.get('/ext/audit/history')
def audit_history(entity_type: str = Query(''), entity_id: str = Query(''),
                  document_id: str = Query(''), limit: int = Query(100)):
    entries = audit_svc.history(entity_type, entity_id, document_id, limit)
    return {'data': [{'id': e._id, 'entity_type': e.entity_type,
                      'entity_id': e.entity_id, 'field_name': e.field_name,
                      'old_value': e.old_value, 'new_value': e.new_value,
                      'changed_by': e.changed_by, 'change_type': e.change_type,
                      'created_at': e.created_at.isoformat() if hasattr(e.created_at, 'isoformat') else str(e.created_at)}
                     for e in entries]}


# ── Sales-020: Sales Events ────────────────────────────────
@router.post('/ext/events')
def emit_event(body: dict):
    event = evt_svc.emit(
        SalesEventType(body['event_type']),
        document_id=body.get('document_id', ''),
        document_number=body.get('document_number', ''),
        customer_id=body.get('customer_id', ''),
        customer_name=body.get('customer_name', ''),
        total=body.get('total', 0),
        data=body.get('data', {}),
        created_by=body.get('created_by', ''),
    )
    return {'data': {'id': event._id, 'event_type': event.event_type.value}}


@router.get('/ext/events/{document_id}')
def list_events(document_id: str):
    events = evt_svc.list_by_document(document_id)
    return {'data': [{'id': e._id, 'event_type': e.event_type.value,
                      'document_number': e.document_number,
                      'customer_name': e.customer_name,
                      'created_at': e.created_at.isoformat() if hasattr(e.created_at, 'isoformat') else str(e.created_at)}
                     for e in events]}


# ── Sales-021: Business Rules Hooks ────────────────────────
@router.post('/ext/hooks/register')
def register_hook(body: dict):
    hook_mgr.register(body['hook_point'], lambda ctx: body.get('result', {}))
    return {'data': {'hook_point': body['hook_point'], 'registered': True}}


@router.post('/ext/hooks/run')
def run_hook(body: dict):
    mode = body.get('mode', 'before')
    if mode == 'before':
        result = hook_mgr.run_before(body['hook_point'], body.get('context', {}))
    else:
        result = hook_mgr.run_after(body['hook_point'], body.get('context', {}))
    return {'data': result}


# ── Sales-022: Extensibility Points (declarative) ──────────
_extension_points = {}


@router.get('/ext/extension-points')
def list_extension_points():
    return {'data': {k: list(v.keys()) for k, v in _extension_points.items()}}


@router.post('/ext/extension-points')
def register_extension(body: dict):
    point = body['point']
    name = body['name']
    if point not in _extension_points:
        _extension_points[point] = {}
    _extension_points[point][name] = {
        'handler': body.get('handler', ''),
        'config': body.get('config', {}),
        'active': body.get('active', True),
    }
    return {'data': {'point': point, 'name': name}}


@router.get('/ext/extension-points/{point}')
def get_extension_point(point: str):
    exts = _extension_points.get(point, {})
    return {'data': {k: v for k, v in exts.items()}}


# ── Sales-023: Business Timeline (consolidated) ────────────
@router.get('/ext/business-timeline/{document_id}')
def business_timeline(document_id: str):
    tl = repo.find_timeline(document_id)
    events = evt_svc.list_by_document(document_id)
    audit = audit_svc.history(document_id=document_id)
    combined = []
    for e in tl:
        combined.append({
            'type': 'timeline', 'id': e._id,
            'title': e.title, 'description': e.description,
            'created_at': e.created_at.isoformat() if hasattr(e.created_at, 'isoformat') else str(e.created_at),
            'created_by': e.created_by,
        })
    for e in events:
        combined.append({
            'type': 'event', 'id': e._id,
            'title': e.event_type.value, 'description': e.event_type.value,
            'created_at': e.created_at.isoformat() if hasattr(e.created_at, 'isoformat') else str(e.created_at),
            'created_by': e.created_by,
        })
    for e in audit:
        combined.append({
            'type': 'audit', 'id': e._id,
            'title': f'{e.field_name}: {e.old_value} \u2192 {e.new_value}',
            'description': f'{e.entity_type} #{e.entity_id}',
            'created_at': e.created_at.isoformat() if hasattr(e.created_at, 'isoformat') else str(e.created_at),
            'changed_by': e.changed_by,
        })
    combined.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    return {'data': combined}


# ── Sales-024: Search Engine ───────────────────────────────
@router.get('/ext/search')
def global_search(query: str = Query(''), limit: int = Query(10)):
    results = search_svc.search(query, limit)
    return {'data': results}


# ── Sales-025: Favorite Actions ────────────────────────────
_favorite_actions = {}


@router.get('/ext/favorite-actions')
def list_favorite_actions(user: str = Query('')):
    if not user:
        return {'data': list(_favorite_actions.values())}
    return {'data': [v for v in _favorite_actions.values() if v.get('user') == user]}


@router.post('/ext/favorite-actions')
def add_favorite_action(body: dict):
    from datetime import datetime
    fa = {
        '_id': f'favact_{datetime.now().timestamp()}',
        'user': body.get('user', ''),
        'label': body.get('label', ''),
        'action': body.get('action', ''),
        'params': body.get('params', {}),
        'icon': body.get('icon', ''),
        'created_at': datetime.now().isoformat(),
    }
    _favorite_actions[fa['_id']] = fa
    return {'data': fa}


@router.delete('/ext/favorite-actions/{action_id}')
def remove_favorite_action(action_id: str):
    _favorite_actions.pop(action_id, None)
    return {'data': {'removed': True}}


# ── Sales Intelligence ─────────────────────────────────────
@router.get('/ext/intelligence/inactive-customers')
def inactive_customers(days: int = Query(90)):
    result = intel_svc.inactive_customers(days)
    return {'data': result}


@router.get('/ext/intelligence/top-products')
def top_products(limit: int = Query(10)):
    result = intel_svc.top_products(limit)
    return {'data': result}


@router.get('/ext/intelligence/forecast')
def sales_forecast(months: int = Query(3)):
    result = intel_svc.sales_forecast(months)
    return {'data': result}


@router.get('/ext/intelligence/executive-panel')
def executive_panel():
    result = intel_svc.executive_panel()
    return {'data': result}
