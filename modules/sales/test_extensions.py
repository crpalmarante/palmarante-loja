import sys
sys.path.insert(0, '/home/palmarante/projetos_cobol/palmarante-loja')

import pytest
from unittest.mock import patch, MagicMock
from modules.sales.core.infrastructure.postgres.sales_repository_memory import SalesRepositoryMemory
from modules.sales.extensions.domain.entities.credit import CustomerCredit, CreditStatus
from modules.sales.extensions.domain.entities.bundle import SalesBundle, BundleItem
from modules.sales.extensions.domain.entities.campaign import Campaign, CampaignType, CampaignTarget
from modules.sales.extensions.domain.entities.policy import SalesPolicy, PolicyAction, PolicyScope
from modules.sales.extensions.domain.entities.rule import SalesRule, RuleCondition, RuleAction
from modules.sales.extensions.application.services.credit_service import CreditService
from modules.sales.extensions.application.services.availability_service import AvailabilityService
from modules.sales.extensions.application.services.recommendation_service import RecommendationService
from modules.sales.extensions.application.services.campaign_service import CampaignService
from modules.sales.extensions.application.services.price_simulation_service import PriceSimulationService
from modules.sales.extensions.application.services.margin_service import MarginService
from modules.sales.extensions.application.services.customer_dashboard_service import CustomerDashboardService
from modules.sales.extensions.application.services.policy_engine import PolicyEngine
from modules.sales.extensions.application.services.rules_engine import RulesEngine


@pytest.fixture
def repo():
    return SalesRepositoryMemory()


# ── Sales-001: Customer Credit ────────────────────────────────

def test_credit_check_approved(repo):
    svc = CreditService(repo)
    credit = svc.get_or_create_credit('c-1', 'Cliente A')
    svc.set_limit('c-1', 10000.0)
    result = svc.check_order('c-1', 5000.0)
    assert result['approved'] is True
    assert result['status'] == 'approved'
    assert result['available'] == 10000.0


def test_credit_check_rejected(repo):
    svc = CreditService(repo)
    svc.set_limit('c-2', 3000.0)
    result = svc.check_order('c-2', 5000.0)
    assert result['approved'] is False
    assert result['status'] == 'limit_exceeded'


def test_credit_no_limit(repo):
    svc = CreditService(repo)
    result = svc.check_order('c-3', 5000.0)
    assert result['approved'] is False
    assert result['status'] == 'pending'


# ── Sales-002: Availability (ATP) ─────────────────────────────

@patch('modules.sales.core.application.services.clients.get_availability')
def test_availability_check(mock_get, repo):
    mock_get.return_value = {'data': {'available': 50, 'reserved': 10, 'physical': 60}}
    svc = AvailabilityService(repo)
    result = svc.check_availability('item-001', '', 5)
    assert result['can_promise'] is True
    assert result['available'] == 50
    assert result['estimated_date'] != ''


@patch('modules.sales.core.application.services.clients.get_availability')
def test_availability_unavailable(mock_get, repo):
    mock_get.return_value = {'data': {'available': 0, 'reserved': 5, 'physical': 5}}
    svc = AvailabilityService(repo)
    result = svc.check_availability('item-001', '', 10)
    assert result['can_promise'] is False
    assert result['estimated_date'] == ''


# ── Sales-003: Similar Products ───────────────────────────────

def test_similar_products(repo):
    svc = RecommendationService(repo)
    items = svc.find_similar('item-001')
    assert isinstance(items, list)


# ── Sales-004: Bundles / Kits ─────────────────────────────────

def test_bundle_crud(repo):
    svc = RecommendationService(repo)
    items = [BundleItem(item_id='i-1', item_name='Mouse', quantity=1),
             BundleItem(item_id='i-2', item_name='Teclado', quantity=1)]
    b = SalesBundle(name='Kit Escritório', code='KIT-001', items=items,
                    bundle_price=150.0, savings_pct=15)
    repo.save_bundle(b)
    assert b._id != ''
    bundles = svc.find_bundles()
    assert len(bundles) == 1
    assert bundles[0].name == 'Kit Escritório'
    found = svc.find_bundles('i-1')
    assert len(found) == 1


# ── Sales-005/006: Cross/Up Selling ────────────────────────────

def test_cross_sell(repo):
    svc = RecommendationService(repo)
    items = svc.find_cross_sell('item-001')
    assert isinstance(items, list)


def test_up_sell(repo):
    svc = RecommendationService(repo)
    items = svc.find_up_sell('item-001')
    assert isinstance(items, list)


# ── Sales-007: Campaigns ──────────────────────────────────────

def test_campaign_crud(repo):
    c = Campaign(name='Natal 10%', code='NATAL2026',
                 campaign_type=CampaignType.PERCENTAGE,
                 target=CampaignTarget.CUSTOMER_CLASS,
                 value=10.0, min_order_value=100.0,
                 customer_classes=['gold', 'diamond'])
    repo.save_campaign(c)
    assert c._id != ''
    assert c.is_valid(customer_class='gold', order_total=200.0)
    assert not c.is_valid(customer_class='bronze', order_total=200.0)
    discount = c.apply(1000.0)
    assert discount == 100.0


def test_campaign_service(repo):
    c = Campaign(name='Black Friday', code='BF', value=15.0,
                 campaign_type=CampaignType.PERCENTAGE)
    repo.save_campaign(c)
    svc = CampaignService(repo)
    result = svc.apply_best('c-1', '', 1000.0)
    assert result['applied'] is True
    assert result['discount'] == 150.0


# ── Sales-008: Price Simulation ───────────────────────────────

@patch('modules.sales.core.application.services.clients.get_item')
def test_simulate_line(mock_item, repo):
    mock_item.return_value = {'cost_price': 80.0}
    svc = PriceSimulationService(repo)
    result = svc.simulate(item_id='i-1', quantity=10, unit_price=100.0,
                           discount_pct=10, freight=20.0, commission_rate=3.0)
    assert result['subtotal'] == 1000.0
    assert result['discount_value'] == 100.0
    assert result['freight'] == 20.0
    assert result['total'] == 920.0
    assert result['margin_pct'] > 0


def test_simulate_order(repo):
    svc = PriceSimulationService(repo)
    result = svc.simulate_order(
        [{'item_id': 'i-1', 'quantity': 2, 'unit_price': 100.0}],
        freight=15.0,
    )
    assert result['totals']['subtotal'] == 200.0
    assert result['totals']['freight'] == 15.0


# ── Sales-009: Margin Analysis ────────────────────────────────

@patch('modules.sales.core.application.services.clients.get_item')
def test_margin_analysis(mock_item, repo):
    mock_item.return_value = {'cost_price': 50.0}

    svc = MarginService(repo)
    result = svc.analyze_line(item_id='i-1', quantity=10, unit_price=100.0)
    assert result['total_cost'] == 500.0
    assert result['net_revenue'] == 1000.0
    assert result['margin_pct'] == 50.0
    assert result['color'] == 'green'
    assert result['level'] == 'good'

    result2 = svc.analyze_line(item_id='i-1', quantity=10, unit_price=55.0)
    assert result2['color'] == 'red'
    assert result2['level'] == 'critical'


def test_margin_order(repo):
    svc = MarginService(repo)
    with patch('modules.sales.core.application.services.clients.get_item',
               return_value={'cost_price': 30.0}):
        result = svc.analyze_order([
            {'item_id': 'i-1', 'quantity': 5, 'unit_price': 100.0},
        ])
    assert result['total_cost'] == 150.0


# ── Sales-010: Customer Dashboard ─────────────────────────────

def test_customer_dashboard(repo):
    from modules.sales.core.domain.entities.sales_order import SalesOrder, SalesOrderStatus
    so = SalesOrder(document_id='d-1', document_number='V-001',
                    customer_id='c-1', status=SalesOrderStatus.COMPLETED, total=5000.0)
    so.created_at = __import__('datetime').datetime(2026, 1, 15)
    repo.save_sales_order(so)
    svc = CustomerDashboardService(repo)
    panel = svc.get_panel('c-1')
    assert panel['total_orders'] >= 1
    assert panel['total_spent'] == 5000.0


# ── Sales Policy Engine ───────────────────────────────────────

def test_policy_engine(repo):
    p = SalesPolicy(name='Inadimplente', code='BLOCK_DEBT',
                    scope=PolicyScope.GLOBAL, action=PolicyAction.BLOCK,
                    condition_field='payment_method',
                    condition_value='credit',
                    condition_operator='equals')
    repo.save_policy(p)
    engine = PolicyEngine(repo)
    blockers = engine.check_blockers(payment_method='credit')
    assert len(blockers) == 1
    assert blockers[0]['action'] == 'block'
    ok = engine.check_blockers(payment_method='pix')
    assert len(ok) == 0


def test_policy_margin_block(repo):
    p = SalesPolicy(name='Margem Mínima', code='MARGIN_10',
                    action=PolicyAction.REQUEST_APPROVAL,
                    condition_field='order_total',
                    condition_operator='less_than',
                    condition_value='100')
    repo.save_policy(p)
    engine = PolicyEngine(repo)
    result = engine.evaluate_for_order(order_total=50)
    assert len(result) == 1
    result2 = engine.evaluate_for_order(order_total=200)
    assert len(result2) == 0


# ── Sales Rules Engine ────────────────────────────────────────

def test_rules_engine(repo):
    r = SalesRule(name='Governo', code='GOV',
                  condition_field='customer_type',
                  condition_operator='equals',
                  condition_value='government',
                  action_field=RuleAction.APPLY_PRICE_LIST,
                  action_value='TABELA_GOV')
    repo.save_rule(r)
    engine = RulesEngine(repo)
    results = engine.evaluate_for_order(customer_type='government')
    assert len(results) == 1
    assert results[0]['action_value'] == 'TABELA_GOV'
    results2 = engine.evaluate_for_order(customer_type='private')
    assert len(results2) == 0


def test_rules_volume_discount(repo):
    r = SalesRule(name='Desconto Volume', code='VOLUME',
                  condition_field='quantity',
                  condition_operator='greater_than',
                  condition_value='100',
                  action_field=RuleAction.APPLY_DISCOUNT,
                  action_value='10')
    repo.save_rule(r)
    engine = RulesEngine(repo)
    results = engine.evaluate_for_order(quantity=200)
    assert len(results) == 1
    results2 = engine.evaluate_for_order(quantity=50)
    assert len(results2) == 0


# ── Sales-011: Customer Agreements ─────────────────────────────

def test_create_agreement(repo):
    from modules.sales.extensions.application.services.extended_services import AgreementService
    svc = AgreementService(repo)
    a = svc.create('c-1', 'Acordo Ouro', price_list_id='PL-1', max_discount_pct=15.0,
                   payment_method='boleto', due_days=45)
    assert a._id != ''
    assert a.customer_id == 'c-1'
    assert a.price_list_id == 'PL-1'


def test_find_active_agreement(repo):
    from modules.sales.extensions.application.services.extended_services import AgreementService
    from modules.sales.extensions.domain.entities.agreement import CustomerAgreement
    from datetime import datetime, timedelta
    svc = AgreementService(repo)
    ag = CustomerAgreement(customer_id='c-2', name='Acordo Ativo',
                           valid_from=(datetime.now() - timedelta(days=10)).isoformat(),
                           valid_to=(datetime.now() + timedelta(days=30)).isoformat(),
                           price_list_id='PL-2')
    repo.save_agreement(ag)
    found = svc.find_active('c-2')
    assert found is not None
    assert found.price_list_id == 'PL-2'


def test_apply_agreement_to_order(repo):
    from modules.sales.extensions.application.services.extended_services import AgreementService
    from datetime import datetime, timedelta
    svc = AgreementService(repo)
    ag = repo.save_agreement(type('obj', (), {
        'customer_id': 'c-3', 'price_list_id': 'PL-3',
        'payment_method': 'credit', 'installments': 3,
        'due_days': 60, 'delivery_term': 'express',
        'sales_rep': 'rep-1',
        'is_valid': lambda self: True,
        'apply_to_order': lambda self, o: {**o, 'price_list_id': 'PL-3',
                                            'payment_method': 'credit',
                                            'installments': 3, 'due_days': 60,
                                            'delivery_term': 'express',
                                            'sales_rep': 'rep-1'},
        '_id': 'agr_test', 'name': '',
        'valid_from': '', 'valid_to': '',
        'notes': '', 'active': True,
    })())
    # direct test of service apply_to_order
    result = svc.apply_to_order('c-4', {'total': 100})
    assert result == {'total': 100}


# ── Sales-012: Sales Calendar ──────────────────────────────────

def test_calendar_crud(repo):
    from modules.sales.extensions.application.services.extended_services import CalendarService
    svc = CalendarService(repo)
    ev = svc.add_event('Reunião Cliente', '2026-08-15',
                        event_type='visit', customer_id='c-1',
                        customer_name='Cliente A', sales_rep='rep-1')
    assert ev._id != ''
    assert ev.title == 'Reunião Cliente'
    events = svc.list_events()
    assert len(events) == 1


def test_calendar_filter_by_rep(repo):
    from modules.sales.extensions.application.services.extended_services import CalendarService
    svc = CalendarService(repo)
    svc.add_event('Evento A', '2026-08-01', sales_rep='rep-1')
    svc.add_event('Evento B', '2026-08-02', sales_rep='rep-2')
    evts = svc.list_events(sales_rep='rep-1')
    assert len(evts) == 1
    assert evts[0].title == 'Evento A'


def test_calendar_from_order(repo):
    from modules.sales.extensions.application.services.extended_services import CalendarService
    svc = CalendarService(repo)
    ev = svc.generate_from_order('doc-1', 'c-1', 'Cliente', '2026-08-20', 'rep-1')
    assert ev.title == 'Entrega Pedido'
    assert ev.document_id == 'doc-1'


# ── Sales-013: Order Split Engine ──────────────────────────────

def test_split_by_warehouse(repo):
    from modules.sales.extensions.application.services.extended_services import OrderSplitService
    svc = OrderSplitService(repo)
    result = svc.split_by_warehouse('doc-1', {'WH-1': ['line-1', 'line-2'], 'WH-2': ['line-3']})
    assert len(result) == 2
    assert result[0]['warehouse_id'] == 'WH-1'
    assert result[0]['original_document_id'] == 'doc-1'


@patch('modules.sales.core.application.services.clients.get_availability')
def test_split_by_availability(mock_get, repo):
    mock_get.return_value = {'data': {'available': 100}}
    from modules.sales.extensions.application.services.extended_services import OrderSplitService
    svc = OrderSplitService(repo)
    result = svc.split_by_availability('doc-1', [
        {'item_id': 'i-1', 'quantity': 5},
        {'item_id': 'i-2', 'quantity': 200},
    ])
    assert len(result['available']) == 1
    assert len(result['unavailable']) == 1


# ── Sales-014: Delivery Scheduling ─────────────────────────────

def test_delivery_schedule(repo):
    from modules.sales.extensions.application.services.extended_services import DeliverySchedulingService
    svc = DeliverySchedulingService(repo)
    result = svc.schedule('doc-1', delivery_type='express',
                          scheduled_date='2026-08-20', address='Rua A, 123')
    assert result['document_id'] == 'doc-1'
    assert result['delivery_type'] == 'express'
    assert result['status'] == 'scheduled'


def test_delivery_estimate(repo):
    from modules.sales.extensions.application.services.extended_services import DeliverySchedulingService
    svc = DeliverySchedulingService(repo)
    result = svc.estimate('12345-678')
    assert result['today'] == 'same_day'
    assert result['estimated_days'] == 1


# ── Sales-015: Customer Preferences ────────────────────────────

def test_customer_preferences(repo):
    from modules.sales.extensions.application.services.extended_services import CustomerPreferencesService
    svc = CustomerPreferencesService(repo)
    result = svc.set('c-1', language='pt-BR', carrier='Correios',
                     delivery_time='morning', contacts=['email@test.com'])
    assert result['language'] == 'pt-BR'
    read = svc.get('c-1')
    assert read['language'] == 'pt-BR'
    assert read['carrier'] == 'Correios'


def test_customer_preferences_default(repo):
    from modules.sales.extensions.application.services.extended_services import CustomerPreferencesService
    svc = CustomerPreferencesService(repo)
    result = svc.get('c-unknown')
    assert result['customer_id'] == 'c-unknown'


# ── Sales-016: Sales KPI Engine ────────────────────────────────

def test_kpi_empty(repo):
    from modules.sales.extensions.application.services.extended_services import KpiEngine
    svc = KpiEngine(repo)
    result = svc.calculate(30)
    assert result['total_orders'] == 0
    assert result['avg_ticket'] == 0


def test_kpi_with_data(repo):
    from modules.sales.extensions.application.services.extended_services import KpiEngine
    from modules.sales.core.domain.entities.sales_order import SalesOrder, SalesOrderStatus
    from datetime import datetime, timedelta
    so = SalesOrder(document_id='d-1', document_number='V-001',
                    customer_id='c-1', customer_name='C1',
                    status=SalesOrderStatus.COMPLETED, total=5000.0,
                    lines=[])
    so.created_at = datetime.now() - timedelta(days=5)
    repo.save_sales_order(so)
    svc = KpiEngine(repo)
    result = svc.calculate(30)
    assert result['total_orders'] >= 1
    assert result['total_revenue'] == 5000.0


# ── Sales-018: Validation Engine ───────────────────────────────

@patch('modules.sales.core.application.services.clients.get_party')
@patch('modules.sales.core.application.services.clients.get_item')
def test_validation_order_valid(mock_item, mock_party, repo):
    mock_party.return_value = {'id': 'c-1', 'name': 'Cliente', 'active': True}
    mock_item.return_value = {'id': 'i-1', 'name': 'Produto', 'active': True}
    from modules.sales.extensions.application.services.extended_services import ValidationEngine
    svc = ValidationEngine(repo)
    result = svc.validate_order(customer_id='c-1', items=[
        {'item_id': 'i-1', 'quantity': 2, 'unit_price': 100.0},
    ], order_total=200.0)
    assert result['valid'] is True
    assert len(result['errors']) == 0


@patch('modules.sales.core.application.services.clients.get_party')
def test_validation_order_invalid_customer(mock_party, repo):
    mock_party.return_value = {}
    from modules.sales.extensions.application.services.extended_services import ValidationEngine
    svc = ValidationEngine(repo)
    result = svc.validate_order(customer_id='c-unknown')
    assert result['valid'] is False or result['can_proceed'] is False


def test_validation_warnings(repo):
    from modules.sales.extensions.application.services.extended_services import ValidationEngine
    svc = ValidationEngine(repo)
    result = svc.validate_order(items=[{'item_id': 'i-1', 'quantity': 1, 'unit_price': 0}],
                                order_total=0, discount_total=1000)
    assert len(result['warnings']) >= 1


# ── Sales-019: Audit Trail ─────────────────────────────────────

def test_audit_record(repo):
    from modules.sales.extensions.application.services.extended_services import AuditService
    svc = AuditService(repo)
    entry = svc.record('SalesOrder', 'ord-1', 'status',
                       'draft', 'confirmed', 'user-1')
    assert entry._id != ''
    assert entry.entity_type == 'SalesOrder'
    assert entry.old_value == 'draft'


def test_audit_history(repo):
    from modules.sales.extensions.application.services.extended_services import AuditService
    svc = AuditService(repo)
    svc.record('SalesOrder', 'ord-1', 'total', '100', '200', 'user-1', document_id='doc-1')
    svc.record('SalesOrder', 'ord-1', 'status', 'draft', 'confirmed', 'user-1', document_id='doc-1')
    history = svc.history(document_id='doc-1')
    assert len(history) == 2
    hist_entity = svc.history(entity_type='SalesOrder')
    assert len(hist_entity) == 2


# ── Sales-020: Sales Events ────────────────────────────────────

def test_event_emit(repo):
    from modules.sales.extensions.application.services.extended_services import EventService
    from modules.sales.extensions.domain.entities.events import SalesEventType
    svc = EventService(repo)
    event = svc.emit(SalesEventType.ORDER_CONFIRMED,
                     document_id='doc-1', document_number='V-001',
                     customer_id='c-1', customer_name='Cliente',
                     total=5000.0, created_by='user-1')
    assert event._id != ''
    assert event.event_type == SalesEventType.ORDER_CONFIRMED


def test_event_list_by_document(repo):
    from modules.sales.extensions.application.services.extended_services import EventService
    from modules.sales.extensions.domain.entities.events import SalesEventType
    svc = EventService(repo)
    svc.emit(SalesEventType.ORDER_CREATED, document_id='doc-1', customer_id='c-1')
    svc.emit(SalesEventType.ORDER_CONFIRMED, document_id='doc-1', customer_id='c-1')
    events = svc.list_by_document('doc-1')
    assert len(events) == 2
    assert events[0].event_type == SalesEventType.ORDER_CREATED


# ── Sales-021: Business Rules Hooks ────────────────────────────

def test_hook_register(repo):
    from modules.sales.extensions.application.services.extended_services import HookManager
    mgr = HookManager()
    mgr.register('before_confirm_order', lambda ctx: {'blocked': False})
    result = mgr.run_before('confirm_order', {'order_id': 'ord-1'})
    assert result['hook_point'] == 'before_confirm_order'
    assert len(result['results']) == 1


def test_hook_multiple(repo):
    from modules.sales.extensions.application.services.extended_services import HookManager
    mgr = HookManager()
    mgr.register('after_add_line', lambda ctx: {'valid': True})
    mgr.register('after_add_line', lambda ctx: {'priced': True})
    result = mgr.run_after('add_line', {'line': {'item_id': 'i-1'}})
    assert len(result['results']) == 2


# ── Sales-024: Search Engine ───────────────────────────────────

def test_search_orders(repo):
    from modules.sales.extensions.application.services.extended_services import SearchService
    from modules.sales.core.domain.entities.sales_order import SalesOrder, SalesOrderStatus
    so = SalesOrder(document_id='d-1', document_number='V-001',
                    customer_id='c-1', customer_name='Cliente ABC',
                    status=SalesOrderStatus.COMPLETED, total=1000.0,
                    lines=[])
    repo.save_sales_order(so)
    svc = SearchService(repo)
    results = svc.search('ABC')
    assert len(results['orders']) >= 1
    assert results['orders'][0]['title'] == 'V-001 - Cliente ABC'


def test_search_empty(repo):
    from modules.sales.extensions.application.services.extended_services import SearchService
    svc = SearchService(repo)
    results = svc.search('ZZZNOTFOUND')
    assert len(results['orders']) == 0
    assert len(results['customers']) == 0
    assert len(results['products']) == 0


# ── Sales Intelligence ─────────────────────────────────────────

def test_intelligence_inactive_customers(repo):
    from modules.sales.extensions.application.services.extended_services import SalesIntelligence
    from modules.sales.core.domain.entities.sales_order import SalesOrder, SalesOrderStatus
    from datetime import datetime, timedelta
    so = SalesOrder(document_id='d-1', document_number='V-001',
                    customer_id='c-1', customer_name='C1',
                    status=SalesOrderStatus.COMPLETED, total=100)
    so.created_at = datetime.now() - timedelta(days=200)
    repo.save_sales_order(so)
    svc = SalesIntelligence(repo)
    inativos = svc.inactive_customers(90)
    assert len(inativos) >= 1


def test_intelligence_top_products(repo):
    from modules.sales.extensions.application.services.extended_services import SalesIntelligence
    from modules.sales.core.domain.entities.sales_order import SalesOrder, SalesOrderStatus
    from modules.sales.core.domain.entities.sales_order import SalesOrderLine
    so = SalesOrder(document_id='d-1', document_number='V-001',
                    customer_id='c-1', customer_name='C1',
                    status=SalesOrderStatus.COMPLETED, total=1000,
                    lines=[SalesOrderLine(item_id='i-1', item_name='Produto A',
                                          item_code='P-001', quantity=10,
                                          unit_price=100, total=1000)])
    repo.save_sales_order(so)
    svc = SalesIntelligence(repo)
    top = svc.top_products(5)
    assert len(top) >= 1
    assert top[0]['item_name'] == 'Produto A'


def test_intelligence_forecast(repo):
    from modules.sales.extensions.application.services.extended_services import SalesIntelligence
    from modules.sales.core.domain.entities.sales_order import SalesOrder, SalesOrderStatus
    from datetime import datetime, timedelta
    so = SalesOrder(document_id='d-1', document_number='V-001',
                    customer_id='c-1', customer_name='C1',
                    status=SalesOrderStatus.COMPLETED, total=6000.0)
    so.created_at = datetime.now() - timedelta(days=30)
    repo.save_sales_order(so)
    svc = SalesIntelligence(repo)
    forecast = svc.sales_forecast(3)
    assert forecast['forecast'] > 0


def test_intelligence_executive_panel(repo):
    from modules.sales.extensions.application.services.extended_services import SalesIntelligence
    from modules.sales.core.domain.entities.sales_order import SalesOrder, SalesOrderStatus
    so = SalesOrder(document_id='d-1', document_number='V-001',
                    customer_id='c-1', customer_name='C1',
                    status=SalesOrderStatus.COMPLETED, total=5000.0)
    repo.save_sales_order(so)
    svc = SalesIntelligence(repo)
    panel = svc.executive_panel()
    assert 'kpi' in panel
    assert 'top_products' in panel
    assert 'forecast' in panel
    assert 'alerts' in panel
