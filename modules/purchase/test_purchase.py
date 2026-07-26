import sys
sys.path.insert(0, '/home/palmarante/projetos_cobol/palmarante-loja')

import pytest
from modules.purchase.core.infrastructure.repositories.memory import PurchaseRepositoryMemory
from modules.purchase.core.application.services.purchase_orchestrator import PurchaseOrchestrator
from modules.purchase.core.domain.entities.purchase_request import PurchaseRequest, PurchaseRequestItem, RequestStatus
from modules.purchase.core.domain.entities.purchase_requisition import PurchaseRequisition, RequisitionStatus
from modules.purchase.core.domain.entities.rfq import RFQ, RFQItem, RFQStatus
from modules.purchase.core.domain.entities.supplier_quotation import SupplierQuotation, QuotationItem, QuotationStatus
from modules.purchase.core.domain.entities.purchase_order import PurchaseOrder, PurchaseOrderLine, PurchaseOrderStatus
from modules.purchase.core.domain.entities.goods_receipt import GoodsReceipt, GoodsReceiptLine
from modules.purchase.core.domain.entities.purchase_return import PurchaseReturn, PurchaseReturnLine
from modules.purchase.core.domain.entities.supplier_agreement import SupplierAgreement, AgreementPriceItem
from modules.purchase.core.domain.entities.approval_matrix import ApprovalMatrixRule, ApprovalScope, ApprovalEngine
from modules.purchase.core.domain.entities.vendor_score import VendorScoreEntry


@pytest.fixture
def repo():
    return PurchaseRepositoryMemory()


@pytest.fixture
def purch(repo):
    return PurchaseOrchestrator(repo)


# ── PURCHASE-001: Purchase Requests ─────────────────────────

def test_create_request(purch):
    items = [PurchaseRequestItem(item_id='i-1', item_code='NB-001',
                                  item_name='Notebook', quantity=5,
                                  estimated_price=5000, estimated_total=25000)]
    pr = purch.create_request('Solicitar Notebooks', 'João', 'TI', items)
    assert pr._id != ''
    assert pr.status == RequestStatus.DRAFT
    assert pr.estimated_total == 25000
    assert pr.department == 'TI'


def test_approve_request(purch):
    pr = purch.create_request('Teste', 'Maria', 'Marketing')
    pr = purch.approve_request(pr._id, 'Supervisor')
    assert pr.status == RequestStatus.APPROVED
    assert pr.approved_by == 'Supervisor'


# ── PURCHASE-002: Purchase Requisitions ─────────────────────

def test_create_requisition(purch):
    pr = purch.create_requisition('Consolidado Compras', 'Compras')
    assert pr._id != ''
    assert pr.status == RequisitionStatus.DRAFT


def test_requisition_consolidates_requests(purch):
    r1 = purch.create_request('TI', 'João', 'TI', items=[
        PurchaseRequestItem(item_id='i-1', item_name='Notebook', quantity=5,
                             estimated_price=5000, estimated_total=25000)])
    r2 = purch.create_request('Marketing', 'Maria', 'Marketing', items=[
        PurchaseRequestItem(item_id='i-1', item_name='Notebook', quantity=2,
                             estimated_price=5000, estimated_total=10000)])
    pr = purch.create_requisition('Consolidado', requests=[r1._id, r2._id])
    assert len(pr.sources) == 2
    assert len(pr.items) == 1
    assert pr.items[0].quantity == 7
    assert pr.estimated_total == 35000


# ── PURCHASE-003: RFQs ─────────────────────────────────────

def test_create_rfq(purch):
    items = [RFQItem(item_id='i-1', item_name='Notebook', quantity=10)]
    rfq = purch.create_rfq('Cotação Notebooks', items=items,
                           invited_suppliers=['s-1', 's-2', 's-3'])
    assert rfq._id != ''
    assert len(rfq.invited_suppliers) == 3
    assert rfq.status == RFQStatus.DRAFT


def test_open_rfq(purch):
    rfq = purch.create_rfq('Teste')
    rfq = purch.open_rfq(rfq._id)
    assert rfq.status == RFQStatus.OPEN


# ── PURCHASE-004: Supplier Quotations ───────────────────────

def test_submit_quotation(purch):
    rfq = purch.create_rfq('Cotação', items=[
        RFQItem(item_id='i-1', item_name='Notebook', quantity=10)])
    purch.open_rfq(rfq._id)
    items = [QuotationItem(item_id='i-1', quantity=10, unit_price=4500)]
    q = purch.submit_quotation(rfq._id, 's-1', 'Fornecedor A',
                                items=items, freight=200,
                                delivery_estimate_days=15)
    assert q._id != ''
    assert q.total == 45000
    assert q.grand_total == 45200


def test_accept_quotation(purch):
    rfq = purch.create_rfq('Teste')
    purch.open_rfq(rfq._id)
    purch.submit_quotation(rfq._id, 's-1', 'Fornecedor',
                           items=[QuotationItem(item_id='i-1', quantity=1, unit_price=100)])
    qs = purch._repo.find_quotations(rfq_id=rfq._id)
    q = purch.accept_quotation(qs[0]._id)
    assert q.status == QuotationStatus.ACCEPTED


# ── PURCHASE-005: Comparison Engine ─────────────────────────

def test_comparison_engine(purch):
    rfq = purch.create_rfq('Comparação', items=[
        RFQItem(item_id='i-1', item_name='Notebook', quantity=10)])
    purch.open_rfq(rfq._id)
    purch.submit_quotation(rfq._id, 's-1', 'Fornecedor A',
                           items=[QuotationItem(item_id='i-1', quantity=10, unit_price=5000)],
                           freight=100, delivery_estimate_days=10)
    purch.submit_quotation(rfq._id, 's-2', 'Fornecedor B',
                           items=[QuotationItem(item_id='i-1', quantity=10, unit_price=4800)],
                           freight=200, delivery_estimate_days=5)
    result = purch.compare_quotations(rfq._id)
    assert len(result['matrix']) == 1
    assert len(result['summary']) == 2
    assert result['best'] is not None
    assert result['best']['supplier_name'] in ('Fornecedor A', 'Fornecedor B')


def test_comparison_best_score(purch):
    rfq = purch.create_rfq('Melhor Preço', items=[
        RFQItem(item_id='i-1', quantity=10)])
    purch.open_rfq(rfq._id)
    purch.submit_quotation(rfq._id, 's-1', 'Caro',
                           items=[QuotationItem(item_id='i-1', quantity=10, unit_price=100)],
                           freight=0, delivery_estimate_days=100)
    purch.submit_quotation(rfq._id, 's-2', 'Barato',
                           items=[QuotationItem(item_id='i-1', quantity=10, unit_price=50)],
                           freight=0, delivery_estimate_days=5)
    result = purch.compare_quotations(rfq._id)
    assert result['best']['supplier_name'] == 'Barato'


# ── PURCHASE-006: Purchase Orders ───────────────────────────

def test_create_po(purch):
    lines = [PurchaseOrderLine(item_id='i-1', quantity=10, unit_price=100, total=1000)]
    po = purch.create_po('doc-001', 's-1', 'Fornecedor', lines)
    assert po._id != ''
    assert po.total == 1000
    assert po.status == PurchaseOrderStatus.DRAFT


def test_po_from_quotation(purch):
    rfq = purch.create_rfq('Cotação PO')
    purch.open_rfq(rfq._id)
    purch.submit_quotation(rfq._id, 's-1', 'Fornecedor PO',
                           items=[QuotationItem(item_id='i-1', quantity=10, unit_price=100)],
                           freight=50, payment_method='boleto', installments=3)
    qs = purch._repo.find_quotations(rfq_id=rfq._id)
    po = purch.create_po_from_quotation(qs[0]._id, 'doc-002')
    assert po is not None
    assert po.supplier_name == 'Fornecedor PO'
    assert po.total == 1050
    assert po.payment_terms.installments == 3


def test_approve_po(purch):
    po = purch.create_po('doc-001', 's-1')
    po = purch.approve_po(po._id, 'Gerente')
    assert po.status == PurchaseOrderStatus.APPROVED


# ── PURCHASE-007: Receiving ─────────────────────────────────

def test_receive_goods(purch):
    lines = [PurchaseOrderLine(item_id='i-1', quantity=10, unit_price=50, total=500)]
    po = purch.create_po('doc-001', 's-1', lines=lines)
    gr = purch.receive_goods(po._id,
                              [{'po_line_id': po.lines[0]._id, 'received_qty': 8}],
                              warehouse_id='WH-1')
    assert gr is not None
    assert gr.status.value == 'draft'
    upd = purch._repo.find_purchase_order_by_id(po._id)
    assert upd.lines[0].received_qty == 8
    assert upd.lines[0].pending_qty == 2


def test_return_create(purch):
    po = purch.create_po('doc-001', 's-1',
                          lines=[PurchaseOrderLine(item_id='i-1', quantity=10, unit_price=100, total=1000)])
    ret = purch.create_return(po._id,
                               lines=[PurchaseReturnLine(item_id='i-1', quantity=2, unit_price=100, total=200, reason='defeito')])
    assert ret is not None
    assert ret.total == 200


# ── PURCHASE-008: Supplier Agreements ───────────────────────

def test_create_agreement(purch):
    items = [AgreementPriceItem(item_id='i-1', item_name='Notebook', price=4500)]
    a = purch.create_agreement('s-1', 'Fornecedor A', 'Acordo Anual',
                                items=items, max_discount_pct=10,
                                valid_from='2026-01-01', valid_to='2026-12-31')
    assert a._id != ''
    assert a.is_valid() is True
    assert a.get_item_price('i-1') == 4500


# ── PURCHASE-009: Approval Matrix ──────────────────────────

def test_approval_rule(purch):
    r = purch.add_approval_rule('purchase_order', 0, 5000, 'supervisor')
    assert r._id != ''
    assert r.description() == '0 a 5000 → supervisor'


def test_approval_engine():
    rules = [
        ApprovalMatrixRule(scope=ApprovalScope.PURCHASE_ORDER, min_value=0, max_value=5000, approver_role='supervisor'),
        ApprovalMatrixRule(scope=ApprovalScope.PURCHASE_ORDER, min_value=5001, max_value=50000, approver_role='manager'),
        ApprovalMatrixRule(scope=ApprovalScope.PURCHASE_ORDER, min_value=50001, max_value=float('inf'), approver_role='director'),
    ]
    engine = ApprovalEngine(rules)
    assert engine.find_approver(3000) == 'supervisor'
    assert engine.find_approver(30000) == 'manager'
    assert engine.find_approver(100000) == 'director'
    assert engine.needs_approval(3000) is True
    assert engine.needs_approval(30000) is True


# ── PURCHASE-010: Vendor Score ──────────────────────────────

def test_vendor_score(purch):
    vs = purch.evaluate_vendor('s-1', 'Fornecedor A', 'po-1',
                                on_time_delivery=True, defect_rate=0.5,
                                price_competitiveness=80, communication_rating=90)
    assert vs._id != ''
    assert vs.criteria.overall_score > 0


def test_vendor_score_calculation():
    vs = VendorScoreEntry(supplier_id='s-1',
                          on_time_delivery=True, defect_rate=0.5,
                          price_competitiveness=80, communication_rating=90)
    score = vs.calculate_score()
    assert vs.criteria.price_score == 80
    assert vs.criteria.quality_score == 95
    assert score > 0


# ── PURCHASE-011: Price History ─────────────────────────────

def test_price_history(repo):
    from modules.purchase.extensions.infrastructure.extended_services import PriceHistoryService
    svc = PriceHistoryService(repo)
    svc.record('i-1', 's-1', 100, 10, 'PO-001')
    svc.record('i-1', 's-2', 90, 10, 'PO-002')
    history = svc.for_item('i-1')
    assert len(history) == 2
    best = svc.best_price('i-1')
    assert best['unit_price'] == 90


# ── PURCHASE-012: Last Purchases ────────────────────────────

def test_last_purchases(repo):
    from modules.purchase.extensions.infrastructure.extended_services import LastPurchasesService
    from modules.purchase.core.domain.entities.purchase_order import PurchaseOrder, PurchaseOrderLine
    svc = LastPurchasesService(repo)
    po = repo.save_purchase_order(PurchaseOrder(
        document_id='d-1', supplier_id='s-1', supplier_name='Fornecedor',
        lines=[PurchaseOrderLine(item_id='i-1', item_name='Produto', quantity=10, unit_price=100, total=1000)],
    ))
    results = svc.for_item('i-1')
    assert len(results) == 1
    assert results[0]['unit_price'] == 100


# ── PURCHASE-013: Split Purchase ───────────────────────────

def test_split_purchase(repo):
    from modules.purchase.extensions.infrastructure.extended_services import SplitPurchaseService
    from modules.purchase.core.domain.entities.purchase_order import PurchaseOrder, PurchaseOrderLine
    svc = SplitPurchaseService(repo)
    po = repo.save_purchase_order(PurchaseOrder(
        document_id='d-1', supplier_id='s-1',
        lines=[PurchaseOrderLine(item_id='i-1', quantity=100, unit_price=10, total=1000)],
    ))
    splits = svc.split_order(po._id, [
        {'supplier_id': 's-1', 'supplier_name': 'A', 'items': [{'line_id': po.lines[0]._id, 'quantity': 60}]},
        {'supplier_id': 's-2', 'supplier_name': 'B', 'items': [{'line_id': po.lines[0]._id, 'quantity': 40}]},
    ])
    assert len(splits) == 2


# ── PURCHASE-015: Purchase Policies ─────────────────────────

def test_purchase_policy(repo):
    from modules.purchase.extensions.infrastructure.extended_services import PurchasePolicyEngine
    eng = PurchasePolicyEngine(repo)
    eng.add_policy('Fornecedor Bloqueado', 'supplier_id', 'equals', 's-bad', 'block')
    results = eng.evaluate({'supplier_id': 's-bad'})
    assert len(results) == 1
    assert results[0]['action'] == 'block'
    results2 = eng.evaluate({'supplier_id': 's-good'})
    assert len(results2) == 0


# ── PURCHASE-016: Validation Engine ─────────────────────────

def test_validation_engine(repo):
    from modules.purchase.extensions.infrastructure.extended_services import ValidationEngine
    eng = ValidationEngine()
    result = eng.validate_po({'supplier_id': '', 'lines': [], 'total': 0})
    assert result['valid'] is False
    assert len(result['errors']) == 2


# ── PURCHASE-019: Dashboard ────────────────────────────────

def test_dashboard(repo):
    from modules.purchase.extensions.infrastructure.extended_services import PurchaseDashboard
    from modules.purchase.core.domain.entities.purchase_order import PurchaseOrder
    repo.save_purchase_order(PurchaseOrder(document_id='d-1', supplier_id='s-1',
                                            supplier_name='Fornecedor A', total=5000))
    repo.save_purchase_order(PurchaseOrder(document_id='d-2', supplier_id='s-2',
                                            supplier_name='Fornecedor B', total=8000))
    dash = PurchaseDashboard(repo)
    data = dash.build()
    assert data['total_orders'] == 2
    assert data['total_value'] == 13000
    assert len(data['top_suppliers']) == 2


# ── Strategic Sourcing ──────────────────────────────────────

def test_homologation(repo):
    from modules.purchase.extensions.infrastructure.extended_services import StrategicSourcing
    src = StrategicSourcing(repo)
    result = src.homologate('s-1', documents=['certidao.pdf'], approved=True)
    assert result['status'] == 'approved'


def test_preferred_supplier(repo):
    from modules.purchase.extensions.infrastructure.extended_services import StrategicSourcing
    src = StrategicSourcing(repo)
    src.set_preferred('s-1', 'i-1', 1)
    src.set_preferred('s-2', 'i-1', 2)
    suppliers = src.get_suppliers_for_item('i-1')
    assert len(suppliers) == 2
    assert suppliers[0]['priority'] == 1  # s-1 is preferred first


def test_supplier_summary(repo):
    from modules.purchase.extensions.infrastructure.extended_services import StrategicSourcing
    src = StrategicSourcing(repo)
    summary = src.supplier_summary('s-1')
    assert summary['supplier_id'] == 's-1'


# ── Full Flow: Request → Requisition → RFQ → Quotation → PO → Receiving ──

def test_full_purchase_flow(purch):
    # 1. Requests
    r1 = purch.create_request('TI Notebooks', 'João', 'TI', items=[
        PurchaseRequestItem(item_id='i-1', item_name='Notebook', quantity=5,
                             estimated_price=5000, estimated_total=25000)])
    r2 = purch.create_request('Marketing Notebooks', 'Maria', 'Marketing', items=[
        PurchaseRequestItem(item_id='i-1', item_name='Notebook', quantity=3,
                             estimated_price=5000, estimated_total=15000)])
    # 2. Approve requests
    purch.approve_request(r1._id, 'Sup TI')
    purch.approve_request(r2._id, 'Sup MKT')
    # 3. Create Requisition consolidating
    req = purch.create_requisition('Consolidado Notebooks', buyer='Compras',
                                    requests=[r1._id, r2._id])
    assert len(req.items) == 1
    assert req.items[0].quantity == 8
    # 4. RFQ
    rfq = purch.create_rfq('Cotação Notebooks', items=[
        RFQItem(item_id='i-1', item_name='Notebook', quantity=8)])
    purch.open_rfq(rfq._id)
    # 5. Quotations from 3 suppliers
    purch.submit_quotation(rfq._id, 's-1', 'Dell', items=[
        QuotationItem(item_id='i-1', quantity=8, unit_price=4800)], freight=0, delivery_estimate_days=15)
    purch.submit_quotation(rfq._id, 's-2', 'Lenovo', items=[
        QuotationItem(item_id='i-1', quantity=8, unit_price=4500)], freight=200, delivery_estimate_days=10)
    purch.submit_quotation(rfq._id, 's-3', 'HP', items=[
        QuotationItem(item_id='i-1', quantity=8, unit_price=4700)], freight=100, delivery_estimate_days=12)
    # 6. Compare
    comp = purch.compare_quotations(rfq._id)
    assert len(comp['summary']) == 3
    best = comp['best']
    # 7. Create PO from best quotation
    best_q = purch._repo.find_quotation_by_id(best['quotation_id'])
    po = purch.create_po_from_quotation(best_q._id, 'doc-purchase-001')
    assert po is not None
    assert po.supplier_id == best_q.supplier_id
    assert po.total == best_q.grand_total
    # 8. Approve PO
    po = purch.approve_po(po._id, 'Diretor')
    assert po.status == PurchaseOrderStatus.APPROVED
    # 9. Send to supplier
    po.send()
    assert po.status == PurchaseOrderStatus.SENT
    # 10. Receive goods
    gr = purch.receive_goods(po._id,
                              [{'po_line_id': po.lines[0]._id, 'received_qty': 8}],
                              warehouse_id='WH-01', received_by='João')
    assert gr is not None
    upd = purch._repo.find_purchase_order_by_id(po._id)
    assert upd.lines[0].received_qty == 8
    # 11. Evaluate vendor
    vs = purch.evaluate_vendor(po.supplier_id, po.supplier_name, po._id,
                                on_time_delivery=True, defect_rate=0,
                                price_competitiveness=85, communication_rating=90)
    assert vs.criteria.overall_score > 0
