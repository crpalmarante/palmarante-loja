"""Integration tests against the live Sales API (port 8008)."""
import sys
sys.path.insert(0, '/home/palmarante/projetos_cobol/palmarante-loja')

import pytest
import requests

API = 'http://localhost:8008/api'
DOC_API = 'http://localhost:8007/api'


@pytest.fixture(autouse=True)
def wait_for_apis():
    try:
        requests.get(f'{API}/sales/dashboard', timeout=2)
    except requests.ConnectionError:
        pytest.skip('Sales API not running on port 8008')


# ── Dashboard ────────────────────────────────────────────────

def test_dashboard():
    r = requests.get(f'{API}/sales/dashboard')
    assert r.status_code == 200
    data = r.json()['data']
    assert data['total_opportunities'] >= 0
    assert 'pipeline_value' in data
    assert 'pipelines' in data


# ── Opportunities ────────────────────────────────────────────

def test_list_opportunities():
    r = requests.get(f'{API}/sales/opportunities')
    assert r.status_code == 200
    assert 'data' in r.json()


def test_create_opportunity():
    r = requests.post(f'{API}/sales/opportunities', json={
        'title': 'API Test Opportunity',
        'customer_id': 'cust-api-test',
        'customer_name': 'API Test Corp',
        'expected_value': 15000.0,
        'probability': 70,
        'source': 'integration-test',
        'sales_rep': 'Bot',
    })
    assert r.status_code == 200
    data = r.json()['data']
    assert data['status'] == 'new'
    assert data['id'] != ''
    return data['id']


def test_close_opportunity_won():
    r = requests.post(f'{API}/sales/opportunities', json={
        'title': 'Close Test', 'customer_id': 'c-close',
    })
    opp_id = r.json()['data']['id']
    r2 = requests.post(f'{API}/sales/opportunities/{opp_id}/close', json={
        'result': 'won',
    })
    assert r2.status_code == 200
    assert r2.json()['data']['status'] == 'won'


def test_close_opportunity_lost():
    r = requests.post(f'{API}/sales/opportunities', json={
        'title': 'Lost Test', 'customer_id': 'c-lost',
    })
    opp_id = r.json()['data']['id']
    r2 = requests.post(f'{API}/sales/opportunities/{opp_id}/close', json={
        'result': 'lost', 'reason': 'Price',
    })
    assert r2.status_code == 200
    assert r2.json()['data']['status'] == 'lost'


# ── Pipelines ────────────────────────────────────────────────

def test_list_pipelines():
    r = requests.get(f'{API}/sales/pipelines')
    assert r.status_code == 200
    assert len(r.json()['data']) >= 1


# ── Price Lists ──────────────────────────────────────────────

def test_list_price_lists():
    r = requests.get(f'{API}/sales/price-lists')
    assert r.status_code == 200
    data = r.json()['data']
    assert len(data) >= 1


def test_create_price_list():
    r = requests.post(f'{API}/sales/price-lists', json={
        'name': 'Test Prices',
        'code': 'TEST',
        'items': [{'item_id': 'item-x', 'price': 199.90}],
    })
    assert r.status_code == 200
    assert r.json()['data']['id'] != ''


# ── Discount Rules ───────────────────────────────────────────

def test_list_discount_rules():
    r = requests.get(f'{API}/sales/discount-rules')
    assert r.status_code == 200
    assert len(r.json()['data']) >= 2


def test_create_discount_rule():
    r = requests.post(f'{API}/sales/discount-rules', json={
        'name': 'Test 15% off',
        'code': 'TEST_15',
        'discount_type': 'percentage',
        'value': 15.0,
        'min_order_value': 500.0,
        'priority': 5,
    })
    assert r.status_code == 200
    assert r.json()['data']['id'] != ''


# ── Commission Rules ─────────────────────────────────────────

def test_list_commission_rules():
    r = requests.get(f'{API}/sales/commission-rules')
    assert r.status_code == 200
    data = r.json()['data']
    assert len(data) >= 1


def test_create_commission_rule():
    r = requests.post(f'{API}/sales/commission-rules', json={
        'name': 'Test 5%',
        'code': 'COMM_5',
        'commission_type': 'percentage',
        'rate': 5.0,
    })
    assert r.status_code == 200


# ── Contracts ────────────────────────────────────────────────

def test_list_contracts():
    r = requests.get(f'{API}/sales/contracts')
    assert r.status_code == 200
    data = r.json()['data']
    assert len(data) >= 1  # seeded


def test_create_contract():
    r = requests.post(f'{API}/sales/contracts', json={
        'customer_id': 'cust-003',
        'customer_name': 'Contract Client',
        'title': 'Annual Support',
        'start_date': '2026-01-01',
        'end_date': '2026-12-31',
        'billing_cycle': 'monthly',
        'value': 24000.0,
        'sales_rep': 'João',
    })
    assert r.status_code == 200
    data = r.json()['data']
    assert data['status'] == 'active'


# ── Sales Orders ─────────────────────────────────────────────

def test_list_orders():
    r = requests.get(f'{API}/sales/orders')
    assert r.status_code == 200
    assert 'data' in r.json()


def test_create_order():
    r = requests.post(f'{API}/sales/orders', json={
        'customer_id': 'cust-ord-test',
        'customer_name': 'Order Client',
        'items': [{'item_id': 'item-001', 'item_name': 'Produto Teste',
                   'quantity': 3, 'unit_price': 100.0}],
        'sales_rep': 'Bot',
        'notes': 'Pedido de teste via API',
        'rep_commission_rate': 3.0,
        'payment_method': 'pix',
        'installments': 3,
    })
    assert r.status_code == 200
    data = r.json()['data']
    assert data['status'] == 'draft'
    assert data['payment_terms']['installments'] == 3
    assert len(data['commissions']) == 1
    return data['id']


# ── Returns ──────────────────────────────────────────────────

def test_create_return():
    r = requests.post(f'{API}/sales/returns', json={
        'document_id': 'doc-ret-001',
        'document_number': 'V-001',
        'customer_id': 'c-ret',
        'items': [{'item_id': 'i-1', 'item_name': 'Defeituoso', 'quantity': 1, 'reason': 'Defeito'}],
        'reason': 'Produto com defeito',
    })
    assert r.status_code == 200
    data = r.json()['data']
    assert data['status'] == 'requested'


def test_list_returns():
    r = requests.get(f'{API}/sales/returns')
    assert r.status_code == 200
    assert len(r.json()['data']) >= 1
