from fastapi import APIRouter, HTTPException, Query
from modules.notification.application.services.notification_client import (
    notify_purchase_request_created, notify_purchase_order_created,
    notify_purchase_order_approved, notify_goods_received, notify_rfq_opened,
)

from modules.purchase.core.infrastructure.repositories.memory import PurchaseRepositoryMemory
from modules.purchase.core.application.services.purchase_orchestrator import PurchaseOrchestrator
from modules.purchase.core.domain.entities.purchase_request import PurchaseRequestItem, RequestStatus
from modules.purchase.core.domain.entities.rfq import RFQItem
from modules.purchase.core.domain.entities.supplier_quotation import QuotationItem
from modules.purchase.core.domain.entities.purchase_order import PurchaseOrderLine
from modules.purchase.core.domain.entities.purchase_return import PurchaseReturnLine
from modules.purchase.core.domain.entities.supplier_agreement import AgreementPriceItem
from modules.purchase.core.domain.entities.vendor_score import VendorScoreEntry
from modules.purchase.extensions.infrastructure.extended_services import (
    PriceHistoryService, LastPurchasesService, SplitPurchaseService,
    ScheduledDeliveryService, PurchasePolicyEngine, ValidationEngine,
    PurchaseEventService, PurchaseTimeline, PurchaseDashboard,
    StrategicSourcing,
)

router = APIRouter(prefix='/api/purchase')

repo = PurchaseRepositoryMemory()
purch = PurchaseOrchestrator(repo)

# Extensions
price_hist = PriceHistoryService(repo)
last_purch = LastPurchasesService(repo)
split_svc = SplitPurchaseService(repo)
delivery_sched = ScheduledDeliveryService()
policy_eng = PurchasePolicyEngine(repo)
val_eng = ValidationEngine()
evt_svc = PurchaseEventService()
timeline = PurchaseTimeline(repo)
dashboard = PurchaseDashboard(repo)
sourcing = StrategicSourcing(repo)


# ── PURCHASE-001: Purchase Requests ──────────────────────────

@router.get('/requests')
def list_requests(status: str = Query(''), requestor: str = Query('')):
    results = purch.list_requests(status, requestor)
    return {'data': [{'id': r._id, 'title': r.title, 'number': r.number,
                      'department': r.department, 'requestor': r.requestor,
                      'status': r.status.value, 'urgency': r.urgency,
                      'estimated_total': r.estimated_total,
                      'items': len(r.items)}
                     for r in results]}


@router.post('/requests')
def create_request(body: dict):
    items = [PurchaseRequestItem(**i) for i in body.get('items', [])]
    pr = purch.create_request(
        title=body['title'], requestor=body.get('requestor', ''),
        department=body.get('department', ''),
        urgency=body.get('urgency', 'medium'),
        justification=body.get('justification', ''),
        items=items,
    )
    notify_purchase_request_created(pr.number, pr.requestor,
                                    body.get('approver', 'user-002'), pr._id)
    return {'data': {'id': pr._id, 'number': pr.number}}


@router.post('/requests/{rid}/approve')
def approve_request(rid: str, body: dict = {}):
    pr = purch.approve_request(rid, body.get('by', ''))
    if not pr: raise HTTPException(404, 'Request not found')
    return {'data': {'id': pr._id, 'status': pr.status.value}}


# ── PURCHASE-002: Purchase Requisitions ─────────────────────

@router.get('/requisitions')
def list_requisitions(status: str = Query('')):
    results = purch.list_requisitions(status)
    return {'data': [{'id': r._id, 'title': r.title, 'number': r.number,
                      'status': r.status.value, 'buyer': r.buyer,
                      'sources': len(r.sources), 'items': len(r.items),
                      'estimated_total': r.estimated_total}
                     for r in results]}


@router.post('/requisitions')
def create_requisition(body: dict):
    pr = purch.create_requisition(
        title=body['title'], buyer=body.get('buyer', ''),
        requests=body.get('request_ids', []),
        urgency=body.get('urgency', 'medium'),
        notes=body.get('notes', ''),
    )
    return {'data': {'id': pr._id, 'number': pr.number, 'items': len(pr.items),
                     'estimated_total': pr.estimated_total}}


# ── PURCHASE-003: RFQs ──────────────────────────────────────

@router.get('/rfqs')
def list_rfqs(status: str = Query('')):
    rfqs = purch._repo.find_rfqs(status)
    return {'data': [{'id': r._id, 'title': r.title, 'number': r.number,
                      'status': r.status.value, 'items': len(r.items),
                      'invited': len(r.invited_suppliers),
                      'created_at': r.created_at.isoformat() if hasattr(r.created_at, 'isoformat') else str(r.created_at)}
                     for r in rfqs]}


@router.post('/rfqs')
def create_rfq(body: dict):
    items = [RFQItem(**i) for i in body.get('items', [])]
    rfq = purch.create_rfq(title=body['title'], items=items,
                           requisition_id=body.get('requisition_id', ''),
                           description=body.get('description', ''),
                           invited_suppliers=body.get('invited_suppliers', []),
                           delivery_address=body.get('delivery_address', ''),
                           valid_until=body.get('valid_until', ''),
                           notes=body.get('notes', ''))
    return {'data': {'id': rfq._id, 'number': rfq.number}}


@router.post('/rfqs/{rfq_id}/open')
def open_rfq(rfq_id: str):
    rfq = purch.open_rfq(rfq_id)
    if not rfq: raise HTTPException(404, 'RFQ not found')
    notify_rfq_opened(rfq.number or rfq.title, 'user-001', rfq._id)
    return {'data': {'id': rfq._id, 'status': rfq.status.value}}


# ── PURCHASE-004: Supplier Quotations ────────────────────────

@router.get('/quotations')
def list_quotations(rfq_id: str = Query(''), supplier_id: str = Query('')):
    qs = purch._repo.find_quotations(rfq_id, supplier_id)
    return {'data': [{'id': q._id, 'rfq_id': q.rfq_id,
                      'supplier_name': q.supplier_name,
                      'total': q.total, 'freight': q.freight,
                      'grand_total': q.grand_total,
                      'delivery_days': q.delivery_estimate_days,
                      'status': q.status.value, 'score': q.score}
                     for q in qs]}


@router.post('/rfqs/{rfq_id}/quotations')
def submit_quotation(rfq_id: str, body: dict):
    items = [QuotationItem(**i) for i in body.get('items', [])]
    q = purch.submit_quotation(rfq_id, body['supplier_id'],
                               body.get('supplier_name', ''),
                               items=items,
                               freight=body.get('freight', 0),
                               payment_method=body.get('payment_method', 'boleto'),
                               installments=body.get('installments', 1),
                               delivery_estimate_days=body.get('delivery_estimate_days', 0),
                               valid_until=body.get('valid_until', ''),
                               notes=body.get('notes', ''))
    if not q: raise HTTPException(404, 'RFQ not found')
    return {'data': {'id': q._id, 'grand_total': q.grand_total}}


# ── PURCHASE-005: Comparison Engine ────────────────────────

@router.get('/rfqs/{rfq_id}/comparison')
def compare_quotations(rfq_id: str):
    result = purch.compare_quotations(rfq_id)
    if not result: raise HTTPException(404, 'RFQ not found')
    return {'data': result}


# ── PURCHASE-006: Purchase Orders ────────────────────────────

@router.get('/orders')
def list_orders(supplier_id: str = Query(''), status: str = Query('')):
    orders = purch.list_pos(supplier_id, status)
    return {'data': [{'id': po._id, 'document_number': po.document_number,
                      'supplier_name': po.supplier_name,
                      'total': po.total, 'status': po.status.value,
                      'lines': len(po.lines),
                      'created_at': po.created_at.isoformat() if hasattr(po.created_at, 'isoformat') else str(po.created_at)}
                     for po in orders]}


@router.post('/orders')
def create_order(body: dict):
    lines = [PurchaseOrderLine(**l) for l in body.get('lines', [])]
    po = purch.create_po(body.get('document_id', ''), body['supplier_id'],
                         body.get('supplier_name', ''), lines=lines,
                         expected_delivery=body.get('expected_delivery', ''),
                         delivery_address=body.get('delivery_address', ''),
                         notes=body.get('notes', ''))
    notify_purchase_order_created(po.document_number or po._id,
                                  po.supplier_name, 'user-001', po._id)
    return {'data': {'id': po._id, 'total': po.total, 'status': po.status.value}}


@router.post('/orders/from-quotation/{quotation_id}')
def create_order_from_quotation(quotation_id: str, body: dict = {}):
    po = purch.create_po_from_quotation(quotation_id, body.get('document_id', ''))
    if not po: raise HTTPException(400, 'Could not generate PO from quotation')
    notify_purchase_order_created(po.document_number or po._id,
                                  po.supplier_name, 'user-001', po._id)
    return {'data': {'id': po._id, 'total': po.total, 'status': po.status.value}}


@router.post('/orders/{po_id}/approve')
def approve_order(po_id: str, body: dict = {}):
    po = purch.approve_po(po_id, body.get('by', ''))
    if not po: raise HTTPException(404, 'Order not found')
    notify_purchase_order_approved(po.document_number or po._id,
                                   po.supplier_name, 'user-001', po._id)
    return {'data': {'id': po._id, 'status': po.status.value,
                     'approved_by': po.approved_by}}


# ── PURCHASE-007: Receiving ──────────────────────────────────

@router.post('/orders/{po_id}/receive')
def receive_order(po_id: str, body: dict):
    gr = purch.receive_goods(po_id, body.get('lines', []),
                             body.get('warehouse_id', ''),
                             body.get('received_by', ''),
                             body.get('notes', ''))
    if not gr: raise HTTPException(404, 'Order not found')
    po = purch._repo.find_by_id(po_id)
    supplier_name = po.supplier_name if po else ''
    notify_goods_received(gr.po_number or po_id, supplier_name,
                          body.get('received_by', 'user-001'), po_id)
    return {'data': {'id': gr._id, 'status': gr.status.value, 'lines': len(gr.lines)}}


@router.get('/goods-receipts')
def list_receipts(po_id: str = Query('')):
    receipts = purch._repo.find_goods_receipts(po_id)
    return {'data': [{'id': g._id, 'po_id': g.po_id, 'po_number': g.po_number,
                      'supplier_name': g.supplier_name,
                      'status': g.status.value, 'lines': len(g.lines),
                      'received_at': g.received_at.isoformat() if hasattr(g.received_at, 'isoformat') else str(g.received_at)}
                     for g in receipts]}


@router.post('/returns')
def create_return(body: dict):
    lines = [PurchaseReturnLine(**l) for l in body.get('lines', [])]
    ret = purch.create_return(body['po_id'], lines=lines,
                              reason=body.get('reason', ''),
                              notes=body.get('notes', ''),
                              created_by=body.get('created_by', ''))
    if not ret: raise HTTPException(404, 'PO not found')
    return {'data': {'id': ret._id, 'total': ret.total}}


# ── PURCHASE-008: Supplier Agreements ────────────────────────

@router.get('/agreements')
def list_agreements(supplier_id: str = Query('')):
    agreements = purch.list_agreements(supplier_id)
    return {'data': [{'id': a._id, 'name': a.name, 'number': a.number,
                      'supplier_name': a.supplier_name,
                      'valid_from': a.valid_from, 'valid_to': a.valid_to,
                      'active': a.active, 'items': len(a.items)}
                     for a in agreements]}


@router.post('/agreements')
def create_agreement(body: dict):
    items = [AgreementPriceItem(**i) for i in body.get('items', [])]
    a = purch.create_agreement(body['supplier_id'],
                               body.get('supplier_name', ''),
                               name=body.get('name', ''),
                               items=items,
                               max_discount_pct=body.get('max_discount_pct', 0),
                               payment_method=body.get('payment_method', ''),
                               installments=body.get('installments', 1),
                               due_days=body.get('due_days', 30),
                               valid_from=body.get('valid_from', ''),
                               valid_to=body.get('valid_to', ''),
                               notes=body.get('notes', ''))
    return {'data': {'id': a._id}}


# ── PURCHASE-009: Approval Matrix ───────────────────────────

@router.get('/approval-rules')
def list_approval_rules(scope: str = Query('')):
    rules = purch.list_approval_rules(scope)
    return {'data': [{'id': r._id, 'scope': r.scope.value,
                      'min_value': r.min_value, 'max_value': r.max_value,
                      'approver_role': r.approver_role,
                      'description': r.description(), 'active': r.active}
                     for r in rules]}


@router.post('/approval-rules')
def create_approval_rule(body: dict):
    r = purch.add_approval_rule(
        scope=body.get('scope', 'purchase_order'),
        min_value=body.get('min_value', 0),
        max_value=body.get('max_value', 999999999),
        approver_role=body.get('approver_role', 'supervisor'),
        active=body.get('active', True),
    )
    return {'data': {'id': r._id, 'description': r.description()}}


# ── PURCHASE-010: Vendor Score ──────────────────────────────

@router.post('/vendor-scores')
def create_vendor_score(body: dict):
    vs = purch.evaluate_vendor(
        supplier_id=body['supplier_id'],
        supplier_name=body.get('supplier_name', ''),
        po_id=body.get('po_id', ''),
        on_time_delivery=body.get('on_time_delivery', True),
        defect_rate=body.get('defect_rate', 0),
        price_competitiveness=body.get('price_competitiveness', 50),
        communication_rating=body.get('communication_rating', 50),
        notes=body.get('notes', ''),
    )
    return {'data': {'id': vs._id, 'overall_score': vs.criteria.overall_score}}


@router.get('/vendor-scores')
def list_vendor_scores(supplier_id: str = Query('')):
    scores = purch.vendor_scores(supplier_id)
    return {'data': [{'id': s._id, 'supplier_name': s.supplier_name,
                      'po_number': s.po_number,
                      'overall_score': s.criteria.overall_score,
                      'price': s.criteria.price_score,
                      'delivery': s.criteria.delivery_score,
                      'quality': s.criteria.quality_score,
                      'service': s.criteria.service_score}
                     for s in scores]}


# ── PURCHASE-011: Price History ─────────────────────────────

@router.post('/price-history')
def record_price(body: dict):
    entry = price_hist.record(body['item_id'], body['supplier_id'],
                               body['unit_price'], body.get('quantity', 0),
                               body.get('po_number', ''))
    return {'data': entry}


@router.get('/price-history/{item_id}')
def get_price_history(item_id: str):
    entries = price_hist.for_item(item_id)
    best = price_hist.best_price(item_id)
    return {'data': {'history': entries, 'best_price': best}}


# ── PURCHASE-012: Last Purchases ────────────────────────────

@router.get('/last-purchases/{item_id}')
def get_last_purchases(item_id: str):
    results = last_purch.for_item(item_id)
    return {'data': results}


# ── PURCHASE-013: Split Purchase ────────────────────────────

@router.post('/orders/{po_id}/split')
def split_order(po_id: str, body: dict):
    results = split_svc.split_order(po_id, body.get('splits', []))
    return {'data': results}


# ── PURCHASE-014: Scheduled Delivery ────────────────────────

@router.post('/orders/{po_id}/schedule-delivery')
def schedule_delivery(po_id: str, body: dict):
    schedules = delivery_sched.schedule(po_id, body.get('deliveries', []))
    return {'data': schedules}


# ── PURCHASE-015: Purchase Policies ─────────────────────────

@router.get('/policies')
def list_policies():
    return {'data': policy_eng._policies}


@router.post('/policies')
def create_policy(body: dict):
    p = policy_eng.add_policy(
        name=body['name'],
        condition_field=body.get('condition_field', ''),
        condition_operator=body.get('condition_operator', 'equals'),
        condition_value=body.get('condition_value', ''),
        action=body.get('action', 'block'),
        action_value=body.get('action_value', ''),
        scope=body.get('scope', 'global'),
        priority=body.get('priority', 0),
    )
    return {'data': p}


@router.post('/policies/evaluate')
def evaluate_policies(body: dict):
    results = policy_eng.evaluate(body.get('context', {}))
    return {'data': results}


# ── PURCHASE-016: Validation Engine ─────────────────────────

@router.post('/validate/order')
def validate_order(body: dict):
    result = val_eng.validate_po(body)
    return {'data': result}


# ── PURCHASE-017: Purchase Events ───────────────────────────

@router.post('/events')
def emit_event(body: dict):
    event = evt_svc.emit(body['event_type'], **body.get('data', {}))
    return {'data': event}


@router.get('/events/{document_id}')
def list_events(document_id: str):
    events = evt_svc.list_by_document(document_id)
    return {'data': events}


# ── PURCHASE-018: Timeline ──────────────────────────────────

@router.post('/timeline')
def add_timeline(body: dict):
    entry = timeline.add(body['document_id'], body['title'],
                          body.get('description', ''),
                          body.get('created_by', ''),
                          body.get('entry_type', 'general'))
    return {'data': entry}


@router.get('/timeline/{document_id}')
def get_timeline(document_id: str):
    entries = timeline.for_document(document_id)
    return {'data': entries}


# ── PURCHASE-019: Dashboard ─────────────────────────────────

@router.get('/dashboard')
def get_dashboard():
    data = dashboard.build()
    return {'data': data}


# ── Strategic Sourcing ──────────────────────────────────────

@router.post('/sourcing/homologate')
def homologate_supplier(body: dict):
    result = sourcing.homologate(
        body['supplier_id'],
        documents=body.get('documents', []),
        approved=body.get('approved', False),
        notes=body.get('notes', ''),
    )
    return {'data': result}


@router.post('/sourcing/risk-assessment')
def assess_risk(body: dict):
    result = sourcing.assess_risk(
        body['supplier_id'],
        financial_score=body.get('financial_score', 0),
        delivery_risk=body.get('delivery_risk', 'medium'),
        overall_risk=body.get('overall_risk', 'medium'),
        notes=body.get('notes', ''),
    )
    return {'data': result}


@router.post('/sourcing/preferred')
def set_preferred_supplier(body: dict):
    result = sourcing.set_preferred(
        body['supplier_id'],
        item_id=body.get('item_id', ''),
        priority=body.get('priority', 1),
    )
    return {'data': result}


@router.get('/sourcing/suppliers-for-item/{item_id}')
def suppliers_for_item(item_id: str):
    suppliers = sourcing.get_suppliers_for_item(item_id)
    return {'data': suppliers}


@router.get('/sourcing/supplier-summary/{supplier_id}')
def supplier_summary(supplier_id: str):
    summary = sourcing.supplier_summary(supplier_id)
    return {'data': summary}
