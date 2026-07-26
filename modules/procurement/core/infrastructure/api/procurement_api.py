from fastapi import APIRouter, HTTPException, Query
from modules.notification.application.services.notification_client import (
    notify_purchase_order_created, notify_rfq_opened,
)

from modules.procurement.core.infrastructure.repositories.memory import ProcurementRepositoryMemory
from modules.procurement.core.application.services.procurement_orchestrator import ProcurementOrchestrator
from modules.procurement.core.domain.entities.rfq import RFQItem
from modules.procurement.core.domain.entities.quotation import QuotationItem

router = APIRouter(prefix='/api/procurement')

repo = ProcurementRepositoryMemory()
proc = ProcurementOrchestrator(repo)


# ── RFQ (PROC-001) ────────────────────────────────────────────

@router.get('/rfqs')
def list_rfqs(status: str = Query('')):
    rfqs = proc.list_rfqs(status)
    return {'data': [{'id': r._id, 'title': r.title, 'number': r.number,
                      'status': r.status.value, 'items': len(r.items),
                      'quotations': len(proc.repo.find_quotations(rfq_id=r._id)),
                      'requires_technical': r.requires_technical_evaluation,
                      'created_at': r.created_at.isoformat() if hasattr(r.created_at, 'isoformat') else str(r.created_at)}
                     for r in rfqs]}


@router.post('/rfqs')
def create_rfq(body: dict):
    items = [RFQItem(**i) for i in body.get('items', [])]
    rfq = proc.create_rfq(
        title=body['title'], items=items,
        description=body.get('description', ''),
        invited_suppliers=body.get('invited_suppliers', []),
        delivery_address=body.get('delivery_address', ''),
        payment_terms=body.get('payment_terms', ''),
        valid_until=body.get('valid_until', ''),
        requires_technical_evaluation=body.get('requires_technical_evaluation', False),
        notes=body.get('notes', ''),
    )
    from modules.notification.application.services.notification_client import send_notification
    send_notification('user-001', f'RFQ {rfq.number or rfq.title} criada',
                      f'Cotação {rfq.title} foi criada com {len(rfq.items)} itens.',
                      entity_type='rfq', entity_id=rfq._id, icon='📢')
    return {'data': {'id': rfq._id}}


@router.get('/rfqs/{rfq_id}')
def get_rfq(rfq_id: str):
    rfq = proc.repo.find_rfq_by_id(rfq_id)
    if not rfq: raise HTTPException(404, 'RFQ not found')
    return {'data': {
        'id': rfq._id, 'title': rfq.title, 'number': rfq.number,
        'description': rfq.description, 'status': rfq.status.value,
        'requires_technical': rfq.requires_technical_evaluation,
        'items': [{'item_id': i.item_id, 'item_code': i.item_code,
                   'item_name': i.item_name, 'quantity': i.quantity,
                   'expected_price': i.expected_price,
                   'required_date': i.required_date,
                   'technical_specs': [{'field': s.field, 'value': s.value, 'unit': s.unit}
                                       for s in (i.technical_specs or [])]}
                  for i in rfq.items],
        'invited_suppliers': rfq.invited_suppliers,
        'delivery_address': rfq.delivery_address,
        'valid_until': rfq.valid_until,
        'created_at': rfq.created_at.isoformat() if hasattr(rfq.created_at, 'isoformat') else str(rfq.created_at),
    }}


@router.post('/rfqs/{rfq_id}/open')
def open_rfq(rfq_id: str):
    rfq = proc.open_rfq(rfq_id)
    if not rfq: raise HTTPException(404, 'RFQ not found')
    notify_rfq_opened(rfq.number or rfq.title, 'user-001', rfq._id)
    return {'data': {'id': rfq._id, 'status': rfq.status.value}}


# ── Supplier Portal (PROC-002) ────────────────────────────────

@router.get('/portal/invitations/{supplier_id}')
def portal_invitations(supplier_id: str):
    invitations = proc.portal_invitations(supplier_id)
    return {'data': invitations}


@router.post('/portal/quotations')
def portal_submit_quotation(body: dict):
    q = proc.portal_submit(
        rfq_id=body['rfq_id'],
        supplier_id=body['supplier_id'],
        supplier_name=body.get('supplier_name', ''),
        items=body.get('items', []),
        supplier_email=body.get('supplier_email', ''),
        supplier_phone=body.get('supplier_phone', ''),
        freight=body.get('freight', 0),
        payment_method=body.get('payment_method', 'boleto'),
        installments=body.get('installments', 1),
        delivery_estimate_days=body.get('delivery_estimate_days', 0),
        valid_until=body.get('valid_until', ''),
        warranty_description=body.get('warranty_description', ''),
        terms_acceptance=body.get('terms_acceptance', ''),
        notes=body.get('notes', ''),
    )
    if not q: raise HTTPException(404, 'RFQ not found')
    return {'data': {'id': q._id, 'grand_total': q.grand_total}}


# ── Quotations ────────────────────────────────────────────────

@router.get('/quotations')
def list_quotations(rfq_id: str = Query(''), supplier_id: str = Query('')):
    qs = proc.repo.find_quotations(rfq_id, supplier_id)
    return {'data': [{'id': q._id, 'rfq_id': q.rfq_id,
                      'supplier_name': q.supplier_name,
                      'items': len(q.items),
                      'total': q.total, 'freight': q.freight,
                      'grand_total': q.grand_total,
                      'delivery_days': q.delivery_estimate_days,
                      'payment_method': q.payment_method,
                      'status': q.status.value, 'score': q.score}
                     for q in qs]}


# ── Quote Comparison (PROC-003/004) ⭐⭐⭐⭐⭐ ─────────────

@router.get('/rfqs/{rfq_id}/comparison')
def compare_quotations(rfq_id: str):
    result = proc.compare(rfq_id)
    if not result: raise HTTPException(404, 'RFQ not found')
    return {'data': result}


@router.post('/rfqs/{rfq_id}/comparison/weights')
def set_comparison_weights(rfq_id: str, body: dict):
    proc.comparison.set_weights(body.get('weights', {}))
    result = proc.compare(rfq_id)
    return {'data': result}


# ── Simulation (PROC-008) ────────────────────────────────────

@router.post('/simulate/{quotation_id}')
def simulate_quotation(quotation_id: str, body: dict):
    result = proc.simulate(quotation_id, body)
    return {'data': result}


# ── Negotiation (PROC-009) ───────────────────────────────────

@router.post('/negotiate/counter')
def make_counter(body: dict):
    cp = proc.make_counter(
        rfq_id=body['rfq_id'],
        quotation_id=body['quotation_id'],
        proposed_by=body.get('proposed_by', 'buyer'),
        supplier_id=body.get('supplier_id', ''),
        items=body.get('items', []),
        total=body.get('total', 0),
        freight=body.get('freight', 0),
        grand_total=body.get('grand_total', 0),
        delivery_days=body.get('delivery_days', 0),
        payment_method=body.get('payment_method', ''),
        installments=body.get('installments', 0),
        notes=body.get('notes', ''),
    )
    if not cp: raise HTTPException(404, 'Quotation not found')
    return {'data': {'id': cp._id, 'round': cp.round.value}}


@router.get('/negotiate/history/{quotation_id}')
def negotiation_history(quotation_id: str):
    history = proc.negotiation_history(quotation_id)
    return {'data': [{'id': h._id, 'round': h.round.value,
                      'proposed_by': h.proposed_by,
                      'grand_total': h.grand_total,
                      'delivery_days': h.delivery_days,
                      'created_at': h.created_at.isoformat() if hasattr(h.created_at, 'isoformat') else str(h.created_at)}
                     for h in history]}


# ── Award Decision (PROC-005) ────────────────────────────────

@router.post('/rfqs/{rfq_id}/award/single')
def award_single(rfq_id: str, body: dict):
    d = proc.award_single(rfq_id, body['supplier_id'],
                          body['quotation_id'],
                          created_by=body.get('created_by', ''),
                          notes=body.get('notes', ''))
    if not d: raise HTTPException(404, 'RFQ or Quotation not found')
    return {'data': {'id': d._id, 'method': d.method.value, 'items': len(d.items)}}


@router.post('/rfqs/{rfq_id}/award/per-item')
def award_per_item(rfq_id: str, body: dict):
    d = proc.award_per_item(rfq_id, body.get('selections', []),
                            created_by=body.get('created_by', ''),
                            notes=body.get('notes', ''))
    if not d: raise HTTPException(404, 'RFQ not found')
    return {'data': {'id': d._id, 'method': d.method.value, 'items': len(d.items)}}


@router.post('/award/{award_id}/generate-pos')
def generate_pos_from_award(award_id: str, body: dict = {}):
    pos = proc.generate_pos(award_id, body.get('document_base', 'PO'))
    for p in pos:
        notify_purchase_order_created(
            getattr(p, 'document_number', '') or p._id,
            p.supplier_name, 'user-001', p._id)
    return {'data': [{'po_id': p._id, 'document_id': p.document_id,
                      'supplier_name': p.supplier_name, 'total': p.total,
                      'items': len(p.items)}
                     for p in pos]}


# ─── Decision Matrix (PROC-010) ─────────────────────────────

@router.get('/rfqs/{rfq_id}/decision-matrix')
def decision_matrix(rfq_id: str):
    result = proc.compare(rfq_id)
    if not result: raise HTTPException(404, 'RFQ not found')
    return {'data': {
        'rfq_id': rfq_id,
        'rfq_title': result.get('rfq_title', ''),
        'weights': result.get('weights', {}),
        'matrix': result.get('decision_matrix', []),
        'best': result.get('best', {}),
    }}


# ── Purchase Orders (operational) ───────────────────────────

@router.get('/orders')
def list_orders(supplier_id: str = Query(''), status: str = Query('')):
    pos = proc.list_pos(supplier_id, status)
    return {'data': [{'id': po._id, 'document_id': getattr(po, 'document_id', ''),
                      'document_number': getattr(po, 'document_number', ''),
                      'supplier_name': getattr(po, 'supplier_name', ''),
                      'total': getattr(po, 'total', 0),
                      'status': getattr(po, 'status', getattr(po, 'status', '')),
                      'items': len(getattr(po, 'items', [])),
                      'created_at': po.created_at.isoformat() if hasattr(po, 'created_at') and po.created_at else ''}
                     for po in pos]}


@router.get('/goods-receipts')
def list_receipts(po_id: str = Query('')):
    receipts = proc.list_receipts(po_id)
    return {'data': [{'id': g._id, 'po_id': g.po_id,
                      'supplier_name': g.supplier_name,
                      'status': g.status.value if hasattr(g.status, 'value') else g.status,
                      'lines': len(g.lines)}
                     for g in receipts]}
