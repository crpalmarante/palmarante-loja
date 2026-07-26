import sys
sys.path.insert(0, '/home/palmarante/projetos_cobol/palmarante-loja')

import pytest
from unittest.mock import patch, MagicMock
from modules.sales.core.infrastructure.postgres.sales_repository_memory import SalesRepositoryMemory
from modules.sales.core.application.services.sales_orchestrator import SalesOrchestrator
from modules.sales.core.application.services.price_engine import PriceEngine
from modules.sales.core.application.services.discount_engine import DiscountEngine
from modules.sales.core.domain.entities.opportunity import Opportunity, Pipeline
from modules.sales.core.domain.entities.price_list import PriceList, PriceListItem
from modules.sales.core.domain.entities.discount_rule import DiscountRule, DiscountType, DiscountScope, DiscountTier
from modules.sales.core.domain.entities.commission import CommissionRule, CommissionType, CommissionStatement, CommissionLine
from modules.sales.core.domain.entities.contract import Contract, ContractLine
from modules.sales.core.domain.entities.delivery import Delivery, DeliveryItem
from modules.sales.core.domain.entities.return_request import ReturnRequest, ReturnItem
from modules.sales.core.domain.value_objects.sales_status import (
    OpportunityStatus, ContractStatus, DeliveryStatus
)


@pytest.fixture
def repo():
    return SalesRepositoryMemory()


@pytest.fixture
def sales(repo):
    return SalesOrchestrator(repo)


# ── Opportunities ────────────────────────────────────────────

def test_create_opportunity(sales):
    with patch('modules.sales.core.application.services.clients.get_party', return_value={'name': 'Test Corp'}):
        opp = sales.create_opportunity(
            title='Venda Teste', customer_id='cust-001',
            customer_name='Test Corp', expected_value=5000.0,
            probability=60, sales_rep='João',
        )
    assert opp.title == 'Venda Teste'
    assert opp.customer_id == 'cust-001'
    assert opp.status == OpportunityStatus.NEW
    assert opp.expected_value == 5000.0
    assert opp.sales_rep == 'João'
    assert opp._id != ''


def test_win_opportunity(sales):
    with patch('modules.sales.core.application.services.clients.get_party', return_value={'name': 'C'}):
        opp = sales.create_opportunity('Test', 'c-1')
    opp.win()
    assert opp.status == OpportunityStatus.WON
    assert opp.won_at is not None


def test_lose_opportunity(sales):
    with patch('modules.sales.core.application.services.clients.get_party', return_value={'name': 'C'}):
        opp = sales.create_opportunity('Test', 'c-1')
    opp.lose('Preço muito alto')
    assert opp.status == OpportunityStatus.LOST
    assert opp.lost_reason == 'Preço muito alto'


def test_close_opportunity_won(sales):
    with patch('modules.sales.core.application.services.clients.get_party', return_value={'name': 'C'}):
        opp = sales.create_opportunity('Test', 'c-1')
    opp2 = sales.close_opportunity(opp._id, 'won')
    assert opp2.status == OpportunityStatus.WON


def test_close_opportunity_lost(sales):
    with patch('modules.sales.core.application.services.clients.get_party', return_value={'name': 'C'}):
        opp = sales.create_opportunity('Test', 'c-1')
    opp2 = sales.close_opportunity(opp._id, 'lost', 'Budget')
    assert opp2.status == OpportunityStatus.LOST
    assert opp2.lost_reason == 'Budget'


def test_find_opportunities(sales):
    with patch('modules.sales.core.application.services.clients.get_party', return_value={'name': 'C'}):
        sales.create_opportunity('Opp A', 'c-1', sales_rep='João')
        sales.create_opportunity('Opp B', 'c-2', sales_rep='Maria')
    opps = sales._repo.find_opportunities()
    assert len(opps) == 2
    joao = sales._repo.find_opportunities(sales_rep='João')
    assert len(joao) == 1


def test_pipeline_crud(repo):
    p = Pipeline(name='Vendas Diretas', stages=['new', 'qualified', 'won'])
    repo.save_pipeline(p)
    assert p._id != ''
    found = repo.find_pipeline_by_id(p._id)
    assert found.name == 'Vendas Diretas'
    assert len(repo.find_all_pipelines()) == 1


# ── Price Engine ─────────────────────────────────────────────

def test_price_list_with_items(repo):
    pl = PriceList(name='Tabela A', code='A')
    pl.set_price('item-001', 100.0, 90.0)
    pl.set_price('item-002', 50.0)
    repo.save_price_list(pl)
    assert pl.get_price('item-001') == 100.0
    assert pl.get_price('item-003') is None


def test_price_engine_from_list(repo):
    pl = PriceList(name='Std', code='STD')
    pl.set_price('item-x', 250.0)
    repo.save_price_list(pl)
    engine = PriceEngine(repo)
    price = engine.get_item_price('item-x', pl._id)
    assert price == 250.0


def test_price_engine_from_catalog(repo):
    engine = PriceEngine(repo)
    with patch('modules.sales.core.application.services.clients.get_catalog_prices',
               return_value=[{'price': 99.90}]):
        price = engine.get_item_price('item-999')
        assert price == 99.90


def test_price_engine_from_item(repo):
    engine = PriceEngine(repo)
    with patch('modules.sales.core.application.services.clients.get_catalog_prices', return_value=[]):
        with patch('modules.sales.core.application.services.clients.get_item',
                   return_value={'sale_price': 75.0}):
            price = engine.get_item_price('item-999')
            assert price == 75.0


def test_apply_prices_to_lines(repo):
    pl = PriceList(name='Std', code='STD')
    pl.set_price('item-a', 200.0)
    repo.save_price_list(pl)
    engine = PriceEngine(repo)
    lines = engine.apply_to_lines([
        {'item_id': 'item-a', 'quantity': 3},
        {'item_id': 'item-b', 'item_name': 'Manual', 'quantity': 1, 'unit_price': 50.0},
    ], pl._id)
    assert len(lines) == 2
    assert lines[0]['unit_price'] == 200.0
    assert lines[0]['total'] == 600.0
    assert lines[1]['unit_price'] == 50.0


# ── Discount Engine ──────────────────────────────────────────

def test_discount_rule_percentage(repo):
    r = DiscountRule(name='5% off', code='D5', discount_type=DiscountType.PERCENTAGE, value=5.0)
    disc = r.calculate(200.0)
    assert disc == 10.0


def test_discount_rule_fixed(repo):
    r = DiscountRule(name='R$20 off', code='F20', discount_type=DiscountType.FIXED, value=20.0)
    disc = r.calculate(100.0)
    assert disc == 20.0


def test_discount_rule_with_max(repo):
    r = DiscountRule(name='10% max 15', code='D10M15',
                     discount_type=DiscountType.PERCENTAGE, value=10.0,
                     max_discount_value=15.0)
    disc = r.calculate(500.0)  # 10% = 50, capped at 15
    assert disc == 15.0


def test_discount_rule_tiered(repo):
    r = DiscountRule(name='Tiered', code='TIER', discount_type=DiscountType.TIERED,
                     tiers=[
                         DiscountTier(min_quantity=10, min_value=500, discount_pct=5),
                         DiscountTier(min_quantity=50, min_value=2500, discount_pct=10),
                     ])
    disc = r.calculate(100.0, quantity=60, order_total=6000.0)
    assert disc == 10.0  # 100 * 10%


def test_discount_engine_apply(repo):
    repo.save_discount_rule(DiscountRule(
        name='5% acima 100', code='D5',
        discount_type=DiscountType.PERCENTAGE, value=5.0,
        min_order_value=100.0, priority=1,
    ))
    engine = DiscountEngine(repo)
    lines = engine.apply_to_lines([
        {'item_id': 'a', 'unit_price': 100.0, 'quantity': 2},
    ])
    assert lines[0]['discount_value'] == 10.0  # 5% of 200
    assert lines[0]['total'] == 190.0


# ── Commission Engine ────────────────────────────────────────

def test_commission_rule_percentage(repo):
    r = CommissionRule(name='3%', code='C3', commission_type=CommissionType.PERCENTAGE, rate=3.0)
    comm = r.calculate(1000.0)
    assert comm == 30.0


def test_commission_rule_fixed(repo):
    r = CommissionRule(name='R$10', code='C10', commission_type=CommissionType.FIXED, fixed_value=10.0)
    comm = r.calculate(1000.0, quantity=5)
    assert comm == 50.0


def test_calculate_order_commission(repo):
    repo.save_commission_rule(CommissionRule(name='3%', code='C3', rate=3.0))
    engine = __import__('modules.sales.core.application.services.commission_engine',
                        fromlist=['CommissionEngine']).CommissionEngine(repo)
    comm = engine.calculate_order_commission('rep-1', 'doc-1', 'NUM-001', 1000.0)
    assert comm == 30.0


# ── Contracts ────────────────────────────────────────────────

def test_create_contract(sales):
    with patch('modules.sales.core.application.services.clients.get_party', return_value={'name': 'C'}):
        c = sales.create_contract(
            customer_id='c-1', customer_name='C',
            title='Suporte', start_date='2026-01-01', end_date='2026-12-31',
            value=12000.0,
            items=[{'item_id': 'srv-001', 'description': 'Suporte', 'quantity': 12, 'unit_price': 1000.0}],
        )
    assert c.status == ContractStatus.ACTIVE
    assert c.title == 'Suporte'
    assert c.value == 12000.0
    assert len(c.items) == 1


def test_contract_status_lifecycle(repo):
    c = Contract(customer_id='c-1', title='Test')
    assert c.status == ContractStatus.DRAFT
    c.activate()
    assert c.status == ContractStatus.ACTIVE
    c.suspend()
    assert c.status == ContractStatus.SUSPENDED
    c.complete()
    assert c.status == ContractStatus.COMPLETED


# ── Deliveries ───────────────────────────────────────────────

def test_delivery_lifecycle(repo):
    d = Delivery(document_id='doc-1', document_number='V-001')
    assert d.status == DeliveryStatus.PENDING
    d.ship('BR-12345')
    assert d.status == DeliveryStatus.SHIPPED
    assert d.tracking_code == 'BR-12345'
    d.deliver()
    assert d.status == DeliveryStatus.DELIVERED


def test_shipment_on_sales_order(sales, repo):
    from modules.sales.core.domain.entities.sales_order import SalesOrder
    so = SalesOrder(document_id='doc-ship', document_number='V-002')
    repo.save_sales_order(so)
    with patch('modules.sales.core.application.services.clients.get_document',
               return_value={'data': {'number': 'V-002', 'lines': [
                   {'item_id': 'i-1', 'item_name': 'Item A', 'quantity': 2},
               ]}}):
        with patch('modules.sales.core.application.services.clients.change_document_status',
                   return_value={'data': {'status': 'picking'}}):
            so2 = sales.add_shipment_to_order('doc-ship', carrier='Correios', created_by='admin')
    assert so2.document_id == 'doc-ship'
    assert len(so2.shipments) == 1
    assert so2.shipments[0].carrier == 'Correios'
    assert so2.status.value == 'picking'


def test_ship_order(sales, repo):
    from modules.sales.core.domain.entities.sales_order import SalesOrder, SalesShipment
    so = SalesOrder(document_id='doc-ship2', document_number='V-003')
    so.add_shipment(SalesShipment(document_id='doc-ship2'))
    repo.save_sales_order(so)
    with patch('modules.sales.core.application.services.clients.record_movement', return_value={}):
        with patch('modules.sales.core.application.services.clients.change_document_status',
                   return_value={'data': {'status': 'shipped'}}):
            so2 = sales.ship_order('doc-ship2', tracking='BR-999')
    assert so2.status.value == 'shipped'
    assert so2.shipments[0].tracking_code == 'BR-999'


# ── Returns ──────────────────────────────────────────────────

def test_create_return(sales):
    items = [ReturnItem(item_id='i-1', item_name='Produto', quantity=1, reason='Defeito')]
    rt = sales.create_return('doc-1', 'V-001', 'c-1', items=items, reason='Defeito de fabricação')
    assert rt.document_id == 'doc-1'
    assert len(rt.items) == 1
    assert rt.items[0].reason == 'Defeito'


# ── SalesOrder Orchestration (mocked) ────────────────────────

@patch('modules.sales.core.application.services.clients.get_party', return_value={'name': 'Empresa X'})
@patch('modules.sales.core.application.services.clients.create_document')
def test_create_sales_order(mock_doc, mock_party, sales):
    mock_doc.return_value = {'data': {'id': 'doc-1', 'number': 'V202607000001', 'status': 'draft', 'total': 300.0}}
    so = sales.create_sales_order(
        customer_id='c-1', customer_name='Empresa X',
        lines=[{'item_id': 'i-1', 'item_name': 'Produto', 'quantity': 2, 'unit_price': 150.0}],
        sales_rep='João', rep_commission_rate=3.0,
    )
    assert so.document_number == 'V202607000001'
    assert so.status.value == 'draft'
    assert so.customer_name == 'Empresa X'
    assert len(so.lines) == 1
    assert len(so.commissions) == 1
    assert so.commissions[0].value == 9.0  # 3% of 300
    assert len(so.installments) == 1


@patch('modules.sales.core.application.services.clients.change_document_status')
def test_approve_sales_order(mock_status, sales, repo):
    # Need a SalesOrder in the repo first
    from modules.sales.core.domain.entities.sales_order import SalesOrder, SalesOrderStatus
    so = SalesOrder(document_id='doc-1', document_number='V-001')
    so._id = 'so-1'
    repo._sales_orders['so-1'] = so
    mock_status.return_value = {'data': {'status': 'approved'}}
    result = sales.approve_sales_order('doc-1', performed_by='admin')
    assert result.status.value == 'approved'


@patch('modules.sales.core.application.services.clients.get_document')
@patch('modules.sales.core.application.services.clients.reserve_inventory')
@patch('modules.sales.core.application.services.clients.change_document_status')
def test_reserve_for_order(mock_status, mock_reserve, mock_doc, sales):
    mock_doc.return_value = {'data': {'lines': [
        {'item_id': 'i-1', 'quantity': 5},
    ]}}
    mock_reserve.return_value = {'data': {'status': 'active'}}
    result = sales.reserve_for_order('doc-1', 'wh-1')
    assert result['document_id'] == 'doc-1'


@patch('modules.sales.core.application.services.clients.get_document')
@patch('modules.sales.core.application.services.clients.create_document')
@patch('modules.sales.core.application.services.clients.change_document_status')
def test_create_invoice(mock_status, mock_create, mock_doc, sales):
    mock_doc.return_value = {'data': {'number': 'V-001', 'lines': [
        {'item_id': 'i-1', 'item_name': 'P', 'quantity': 1, 'unit_price': 100.0, 'tax_value': 10.0},
    ], 'parties': [{'party_id': 'c-1', 'party_type': 'customer', 'party_name': 'C'}]}}
    mock_create.return_value = {'data': {'id': 'inv-1', 'number': 'NF-001', 'status': 'draft'}}
    inv = sales.invoice_order('doc-1')
    assert inv['number'] == 'NF-001'


# ── Dashboard ────────────────────────────────────────────────

def test_dashboard(sales):
    with patch('modules.sales.core.application.services.clients.get_party', return_value={'name': 'C'}):
        sales.create_opportunity('Opp 1', 'c-1', expected_value=5000)
        sales.create_opportunity('Opp 2', 'c-2', expected_value=3000)
    dash = sales.get_dashboard()
    assert dash['total_opportunities'] >= 2
    assert dash['pipeline_value'] >= 8000


# ── Sales Experience ────────────────────────────────────────────

def test_customer_last_orders(sales, repo):
    from modules.sales.core.domain.entities.sales_order import SalesOrder
    so1 = SalesOrder(document_id='d1', document_number='V-001', customer_id='c-1')
    so2 = SalesOrder(document_id='d2', document_number='V-002', customer_id='c-1')
    so3 = SalesOrder(document_id='d3', document_number='V-003', customer_id='c-2')
    repo.save_sales_order(so1)
    repo.save_sales_order(so2)
    repo.save_sales_order(so3)
    orders = sales.customer_last_orders('c-1')
    assert len(orders) == 2
    assert orders[0].customer_id == 'c-1'


@patch('modules.sales.core.application.services.clients.create_document')
@patch('modules.sales.core.application.services.clients.get_party')
def test_duplicate_order(mock_party, mock_doc, sales, repo):
    from modules.sales.core.domain.entities.sales_order import SalesOrder, SalesOrderLine
    so = SalesOrder(document_id='d-dup', document_number='V-001', customer_id='c-1',
                    customer_name='C1')
    so.add_line(SalesOrderLine(item_id='i-1', item_name='Item', quantity=2, unit_price=50))
    repo.save_sales_order(so)
    mock_party.return_value = {'name': 'C1'}
    mock_doc.return_value = {'data': {'id': 'new-doc', 'number': 'V-002', 'total': 100.0}}
    dup = sales.duplicate_order('d-dup', performed_by='admin')
    assert dup.document_number == 'V-002'
    assert dup.source_order_id != ''
    assert len(dup.lines) == 1


@patch('modules.sales.core.application.services.clients.create_document')
@patch('modules.sales.core.application.services.clients.get_party')
def test_quick_quote(mock_party, mock_doc, sales):
    mock_party.return_value = {'name': 'Q'}
    mock_doc.return_value = {'data': {'id': 'qq-1', 'number': 'Q202607000001'}}
    result = sales.quick_quote(customer_id='c-1', item_id='i-1', quantity=5,
                                unit_price=100.0, sales_rep='João')
    assert result.get('number') == 'Q202607000001'


def test_order_template_crud(sales, repo):
    tpl = sales.create_template(name='Kit Escritório', customer_id='c-1',
                                 lines=[{"item_id": "i-1", "item_name": "Mouse",
                                         "quantity": 1, "unit_price": 50.0}])
    assert tpl._id != ''
    assert tpl.name == 'Kit Escritório'
    found = repo.find_template_by_id(tpl._id)
    assert found.name == 'Kit Escritório'
    result = sales.apply_template(tpl._id, customer_id='c-new', customer_name='New')
    assert result['customer_id'] == 'c-new'


def test_favorites(sales, repo):
    fav = sales.add_favorite(customer_id='c-1', item_id='i-1', item_name='Mouse')
    assert fav._id != ''
    favs = sales.list_favorites('c-1')
    assert len(favs) == 1
    assert favs[0].item_id == 'i-1'
    sales.remove_favorite(fav._id)
    assert len(sales.list_favorites('c-1')) == 0


def test_price_history(sales, repo):
    e1 = sales.record_price(item_id='i-1', price=100.0, recorded_by='admin')
    e2 = sales.record_price(item_id='i-1', price=120.0, recorded_by='admin')
    history = sales.price_history('i-1')
    assert len(history) == 2
    assert history[0].price == 120.0  # newest first


@patch('modules.sales.core.application.services.clients.create_document')
@patch('modules.sales.core.application.services.clients.get_party')
def test_timeline(mock_party, mock_doc, sales):
    mock_party.return_value = {'name': 'C'}
    mock_doc.return_value = {'data': {'id': 'tl-doc', 'number': 'TL-001', 'total': 200.0}}
    so = sales.create_sales_order(customer_id='c-1', lines=[{'item_id': 'i-1', 'quantity': 1, 'unit_price': 100}])
    entries = sales.get_timeline(so.document_id)
    assert isinstance(entries, list)


def test_sales_notes(sales, repo):
    note = sales.add_note(document_id='doc-1', content='Observação interna',
                           note_type='internal', created_by='admin')
    assert note._id != ''
    assert note.note_type.value == 'internal'
    notes = sales.list_notes('doc-1')
    assert len(notes) == 1
    notes_ext = sales.list_notes('doc-1', 'external')
    assert len(notes_ext) == 0


def test_tags(sales, repo):
    tag = sales.create_tag(name='Exportação', color='#ff0000')
    assert tag._id != ''
    tags = sales.list_tags()
    assert len(tags) >= 1
    assert any(t.name == 'Exportação' for t in tags)


def test_team(sales, repo):
    m = sales.add_team_member(rep_id='rep-1', name='João', role='seller',
                               supervisor_id='sup-1')
    assert m._id != ''
    assert m.role == 'seller'
    sellers = sales.list_team('seller')
    assert len(sellers) >= 1
    all_team = sales.list_team()
    assert len(all_team) >= 1


def test_approval_matrix(sales, repo):
    r1 = sales.add_approval_rule(name='Até 5k', min_value=0, max_value=5000,
                                  approver_role='seller')
    r2 = sales.add_approval_rule(name='5k-50k', min_value=5000, max_value=50000,
                                  approver_role='supervisor')
    r3 = sales.add_approval_rule(name='Acima 50k', min_value=50000,
                                  approver_role='director')
    assert sales.get_approver_for(1000) == 'seller'
    assert sales.get_approver_for(10000) == 'supervisor'
    assert sales.get_approver_for(100000) == 'director'
    rules = sales.list_approval_rules()
    assert len(rules) >= 3
