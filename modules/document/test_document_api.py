"""Integration tests against the live Document API (port 8007)."""
import sys
sys.path.insert(0, '/home/palmarante/projetos_cobol/palmarante-loja')

import pytest
import requests

API = 'http://localhost:8007/api'


@pytest.fixture(autouse=True)
def wait_for_api():
    try:
        requests.get(f'{API}/documents/dashboard', timeout=2)
    except requests.ConnectionError:
        pytest.skip('API not running on port 8007')


# ── Definitions ──────────────────────────────────────────────

def test_list_definitions():
    r = requests.get(f'{API}/document-definitions')
    assert r.status_code == 200
    data = r.json()['data']
    assert len(data) >= 6
    codes = [d['code'] for d in data]
    assert 'sale_order' in codes
    assert 'purchase_order' in codes


def test_get_definition():
    r = requests.get(f'{API}/document-definitions')
    def_id = r.json()['data'][0]['id']
    r2 = requests.get(f'{API}/document-definitions/{def_id}')
    assert r2.status_code == 200
    data = r2.json()['data']
    assert data['id'] == def_id
    assert 'code' in data


def test_create_definition():
    r = requests.post(f'{API}/document-definitions', json={
        'name': 'Test API Definition',
        'code': 'test_api_def',
        'direction': 'out',
        'has_lines': True,
        'has_parties': False,
        'has_totals': True,
        'behaviors': ['inventory'],
    })
    assert r.status_code == 200
    data = r.json()['data']
    assert data['code'] == 'test_api_def'


# ── Numbering ────────────────────────────────────────────────

def test_list_numbering():
    r = requests.get(f'{API}/document-numbering')
    assert r.status_code == 200
    data = r.json()['data']
    assert len(data) >= 6


def test_create_numbering():
    r = requests.post(f'{API}/document-numbering', json={
        'document_type': 'test_num',
        'pattern': 'T{year}{month}{seq:04d}',
        'digits': 4,
        'next_number': 1,
    })
    assert r.status_code == 200
    data = r.json()['data']
    assert data['document_type'] == 'test_num'


# ── Documents CRUD ──────────────────────────────────────────

def test_create_document():
    r = requests.post(f'{API}/documents', json={
        'document_type': 'sale_order',
        'direction': 'out',
        'header': {'responsible': 'Test User', 'department': 'QA'},
        'lines': [
            {'item_name': 'Item Teste', 'quantity': 5, 'unit_price': 100.0},
        ],
        'parties': [{'party_id': 'cust-test', 'party_type': 'customer', 'party_name': 'Test Corp'}],
        'notes': 'Documento de teste',
        'created_by': 'pytest',
    })
    assert r.status_code == 200
    data = r.json()['data']
    assert data['status'] == 'draft'
    assert data['number'].startswith('V')
    return data['id']


def test_list_documents():
    r = requests.get(f'{API}/documents')
    assert r.status_code == 200
    data = r.json()['data']
    assert len(data) >= 4  # 3 seed + at least 1 created in test_create_document


def test_get_document():
    # create a doc first
    r = requests.post(f'{API}/documents', json={
        'document_type': 'sale_order',
        'lines': [{'item_name': 'Get Test', 'quantity': 1, 'unit_price': 500.0}],
        'parties': [{'party_id': 'p-1', 'party_type': 'customer', 'party_name': 'P'}],
    })
    doc_id = r.json()['data']['id']
    r2 = requests.get(f'{API}/documents/{doc_id}')
    assert r2.status_code == 200
    data = r2.json()['data']
    assert data['id'] == doc_id
    assert data['document_type'] == 'sale_order'
    assert len(data['lines']) == 1
    assert len(data['parties']) == 1


def test_update_document():
    r = requests.post(f'{API}/documents', json={
        'document_type': 'sale_order',
        'lines': [{'item_name': 'Update Test', 'quantity': 1, 'unit_price': 250.0}],
    })
    doc_id = r.json()['data']['id']
    r2 = requests.put(f'{API}/documents/{doc_id}', json={
        'header': {'responsible': 'Updated'},
        'notes': 'Updated notes',
        'direction': 'internal',
    })
    assert r2.status_code == 200
    r3 = requests.get(f'{API}/documents/{doc_id}')
    data = r3.json()['data']
    assert data['header']['responsible'] == 'Updated'
    assert data['header']['notes'] == 'Updated notes'


def test_change_status():
    r = requests.post(f'{API}/documents', json={
        'document_type': 'sale_order',
        'lines': [{'item_name': 'Status Test', 'quantity': 1, 'unit_price': 100.0}],
    })
    doc_id = r.json()['data']['id']
    r2 = requests.post(f'{API}/documents/{doc_id}/status', json={
        'status': 'approved',
        'comment': 'Aprovado em teste',
        'performed_by': 'pytest',
    })
    assert r2.status_code == 200
    assert r2.json()['data']['status'] == 'approved'
    r3 = requests.get(f'{API}/documents/{doc_id}')
    data = r3.json()['data']
    assert data['status'] == 'approved'
    # verify history has the status change
    assert len(data['history']) >= 2
    history_actions = [h['action'] for h in data['history']]
    assert 'created' in history_actions
    assert 'status_change' in history_actions


def test_add_line_via_api():
    r = requests.post(f'{API}/documents', json={
        'document_type': 'sale_order',
        'lines': [{'item_name': 'Original', 'quantity': 1, 'unit_price': 50.0}],
    })
    doc_id = r.json()['data']['id']
    r2 = requests.post(f'{API}/documents/{doc_id}/lines', json={
        'item_name': 'Added Later', 'quantity': 3, 'unit_price': 75.0,
    })
    assert r2.status_code == 200
    assert r2.json()['data']['lines'] == 2
    r3 = requests.get(f'{API}/documents/{doc_id}')
    assert len(r3.json()['data']['lines']) == 2


def test_delete_line():
    r = requests.post(f'{API}/documents', json={
        'document_type': 'sale_order',
        'lines': [
            {'item_name': 'Line 1', 'quantity': 1, 'unit_price': 10.0},
            {'item_name': 'Line 2', 'quantity': 2, 'unit_price': 20.0},
        ],
    })
    doc_id = r.json()['data']['id']
    r2 = requests.get(f'{API}/documents/{doc_id}')
    line_id = r2.json()['data']['lines'][0]['id']
    r3 = requests.delete(f'{API}/documents/{doc_id}/lines/{line_id}')
    assert r3.status_code == 200
    assert r3.json()['data']['lines'] == 1


def test_delete_document():
    r = requests.post(f'{API}/documents', json={
        'document_type': 'sale_order',
        'lines': [{'item_name': 'Delete Me', 'quantity': 1, 'unit_price': 1.0}],
    })
    doc_id = r.json()['data']['id']
    r2 = requests.delete(f'{API}/documents/{doc_id}')
    assert r2.status_code == 200
    r3 = requests.get(f'{API}/documents/{doc_id}')
    assert r3.status_code == 404


def test_find_by_reference():
    r = requests.post(f'{API}/documents', json={
        'document_type': 'sale_order',
        'lines': [{'item_name': 'Ref Test', 'quantity': 1, 'unit_price': 100.0}],
        'references': [{'reference_type': 'contract', 'reference_id': 'ref-001', 'reference_number': 'CT-001'}],
    })
    assert r.status_code == 200
    r2 = requests.get(f'{API}/documents/reference/contract/ref-001')
    assert r2.status_code == 200
    data = r2.json()['data']
    assert len(data) >= 1
    assert data[0]['document_type'] == 'sale_order'


# ── Dashboard ────────────────────────────────────────────────

def test_dashboard():
    r = requests.get(f'{API}/documents/dashboard')
    assert r.status_code == 200
    data = r.json()['data']
    assert data['total_documents'] >= 4
    assert data['active_definitions'] >= 6
    assert 'by_type' in data
    assert 'by_status' in data
