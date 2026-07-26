"""HTTP integration clients for other platform APIs."""
import urllib.request
import json


def _fetch(url: str, method: str = 'GET', body: dict = None) -> dict:
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data,
                                 headers={'Content-Type': 'application/json'},
                                 method=method)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise Exception(f'API error {e.code} from {url}: {e.read().decode()}')


# ── Party API (port 8000) ────────────────────────────────────
def get_party(party_id: str) -> dict | None:
    try:
        return _fetch(f'http://localhost:8000/api/parties/{party_id}').get('data')
    except Exception:
        return None


# ── Item API (port 8001) ─────────────────────────────────────
def get_item(item_id: str) -> dict | None:
    try:
        return _fetch(f'http://localhost:8001/api/items/{item_id}').get('data')
    except Exception:
        return None


# ── Catalog API (port 8003) ──────────────────────────────────
def get_catalog_prices(item_id: str) -> list:
    try:
        r = _fetch(f'http://localhost:8003/api/catalog-prices?item_id={item_id}')
        return r.get('data', [])
    except Exception:
        return []


# ── Inventory API (port 8005) ────────────────────────────────
def reserve_inventory(item_id: str, warehouse_id: str, quantity: float,
                      order_id: str = '') -> dict:
    return _fetch('http://localhost:8005/api/inventory/reservations',
                  method='POST', body={
                      'item_id': item_id, 'warehouse_id': warehouse_id,
                      'quantity': quantity, 'order_id': order_id,
                  })


def get_availability(item_id: str, warehouse_id: str = '') -> dict:
    return _fetch(f'http://localhost:8005/api/inventory/available'
                  f'?item_id={item_id}&warehouse_id={warehouse_id}')


def record_movement(item_id: str, warehouse_id: str, movement_type: str,
                    quantity: float, reference_type: str = '',
                    reference_id: str = '', document_number: str = '') -> dict:
    return _fetch('http://localhost:8005/api/inventory/movements',
                  method='POST', body={
                      'item_id': item_id, 'warehouse_id': warehouse_id,
                      'movement_type': movement_type, 'quantity': quantity,
                      'reference_type': reference_type,
                      'reference_id': reference_id,
                      'document_number': document_number,
                  })


# ── Document API (port 8007) ─────────────────────────────────
def create_document(doc_type: str, lines: list = None, parties: list = None,
                    references: list = None, notes: str = '',
                    direction: str = 'out', header: dict = None,
                    created_by: str = '') -> dict:
    return _fetch('http://localhost:8007/api/documents', method='POST', body={
        'document_type': doc_type, 'direction': direction,
        'lines': lines or [], 'parties': parties or [],
        'references': references or [], 'notes': notes,
        'header': header or {}, 'created_by': created_by,
    })


def add_document_line(doc_id: str, line_data: dict) -> dict:
    return _fetch(f'http://localhost:8007/api/documents/{doc_id}/lines',
                  method='POST', body=line_data)


def get_document(doc_id: str) -> dict:
    return _fetch(f'http://localhost:8007/api/documents/{doc_id}')


def change_document_status(doc_id: str, status: str,
                           comment: str = '', performed_by: str = '') -> dict:
    return _fetch(f'http://localhost:8007/api/documents/{doc_id}/status',
                  method='POST', body={
                      'status': status, 'comment': comment,
                      'performed_by': performed_by,
                  })


def get_document_definitions() -> list:
    r = _fetch('http://localhost:8007/api/document-definitions')
    return r.get('data', [])


# ── Search Aggregator ───────────────────────────────────────
def search_items(query: str, limit: int = 5) -> list:
    try:
        r = _fetch(f'http://localhost:8001/api/items?q={query}&limit={limit}')
        return r.get('data', [])
    except Exception:
        return []


def search_parties(query: str, limit: int = 5) -> list:
    try:
        r = _fetch(f'http://localhost:8000/api/parties?q={query}&limit={limit}')
        return r.get('data', [])
    except Exception:
        return []


def search_local_sales(query: str, limit: int = 5) -> dict:
    try:
        r = _fetch(f'http://localhost:8008/api/sales/ext/search?query={query}&limit={limit}')
        return r.get('data', {})
    except Exception:
        return {}


def search_purchase(query: str, limit: int = 5) -> list:
    try:
        r = _fetch(f'http://localhost:8009/api/purchase/orders?q={query}&limit={limit}')
        return r.get('data', [])
    except Exception:
        return []


def search_documents(query: str, limit: int = 5) -> list:
    try:
        r = _fetch(f'http://localhost:8007/api/documents?q={query}&limit={limit}')
        return r.get('data', [])
    except Exception:
        return []


# ── Workflow API (port 8006) ─────────────────────────────────
def start_workflow(workflow_id: str, document_type: str,
                   document_id: str, document_data: dict = None) -> dict:
    return _fetch('http://localhost:8006/api/workflow-instances',
                  method='POST', body={
                      'workflow_id': workflow_id,
                      'document_type': document_type,
                      'document_id': document_id,
                      'document_data': document_data or {},
                  })


def execute_workflow_transition(instance_id: str, transition_code: str,
                                comment: str = '', performed_by: str = '') -> dict:
    return _fetch(f'http://localhost:8006/api/workflow-instances/{instance_id}/transition',
                  method='POST', body={
                      'transition_code': transition_code,
                      'comment': comment, 'performed_by': performed_by,
                  })
