from modules.purchase.core.domain.entities.purchase_request import PurchaseRequest, PurchaseRequestItem, RequestStatus
from modules.purchase.core.domain.entities.purchase_requisition import PurchaseRequisition, PurchaseRequisitionItem, RequisitionStatus
from modules.purchase.core.domain.entities.rfq import RFQ, RFQItem, RFQStatus
from modules.purchase.core.domain.entities.supplier_quotation import SupplierQuotation, QuotationItem, QuotationStatus
from modules.purchase.core.domain.entities.purchase_order import PurchaseOrder, PurchaseOrderLine, PurchaseOrderStatus, PurchasePaymentTerms
from modules.purchase.core.domain.entities.goods_receipt import GoodsReceipt, GoodsReceiptLine, GoodsReceiptStatus
from modules.purchase.core.domain.entities.purchase_return import PurchaseReturn, PurchaseReturnLine, ReturnStatus
from modules.purchase.core.domain.entities.supplier_agreement import SupplierAgreement, AgreementPriceItem
from modules.purchase.core.domain.entities.approval_matrix import ApprovalMatrixRule, ApprovalScope, ApprovalEngine
from modules.purchase.core.domain.entities.vendor_score import VendorScoreEntry, VendorScoreCriteria
from modules.purchase.core.domain.repositories.purchase_repository import PurchaseRepository
from modules.purchase.core.application.services.comparison_engine import ComparisonEngine


class PurchaseOrchestrator:
    def __init__(self, repo: PurchaseRepository):
        self._repo = repo
        self._comparison = ComparisonEngine(repo)
        self._approval = ApprovalEngine()

    @property
    def comparison(self):
        return self._comparison

    @property
    def approval(self):
        return self._approval

    # ── Purchase Requests (PURCHASE-001) ──────────────────────

    def create_request(self, title: str, requestor: str = '',
                       department: str = '', items: list = None, **kw) -> PurchaseRequest:
        pr = PurchaseRequest(title=title, requestor=requestor,
                             department=department, items=items or [], **kw)
        return self._repo.save_purchase_request(pr)

    def list_requests(self, status: str = '', requestor: str = '') -> list:
        return self._repo.find_purchase_requests(status, requestor)

    def approve_request(self, prid: str, by: str = ''):
        pr = self._repo.find_purchase_request_by_id(prid)
        if pr: pr.approve(by)
        return pr

    # ── Purchase Requisitions (PURCHASE-002) ──────────────────

    def create_requisition(self, title: str, buyer: str = '',
                           requests: list = None, **kw) -> PurchaseRequisition:
        pr = PurchaseRequisition(title=title, buyer=buyer, **kw)
        if requests:
            reqs = [self._repo.find_purchase_request_by_id(r) for r in requests if r]
            pr.consolidate_from_requests([r for r in reqs if r])
        return self._repo.save_purchase_requisition(pr)

    def list_requisitions(self, status: str = '') -> list:
        return self._repo.find_purchase_requisitions(status)

    def approve_requisition(self, prid: str, by: str = ''):
        pr = self._repo.find_purchase_requisition_by_id(prid)
        if pr:
            val = pr.estimated_total
            role = self._approval.find_approver(val, ApprovalScope.REQUISITION)
            pr.approve(by or role)
        return pr

    # ── RFQ (PURCHASE-003) ────────────────────────────────────

    def create_rfq(self, title: str, items: list = None, **kw) -> RFQ:
        rfq = RFQ(title=title, items=items or [], **kw)
        return self._repo.save_rfq(rfq)

    def open_rfq(self, rfq_id: str):
        rfq = self._repo.find_rfq_by_id(rfq_id)
        if rfq: rfq.open()
        return rfq

    # ── Supplier Quotations (PURCHASE-004) ──────────────────────

    def submit_quotation(self, rfq_id: str, supplier_id: str,
                         supplier_name: str = '', items: list = None,
                         **kw) -> SupplierQuotation | None:
        rfq = self._repo.find_rfq_by_id(rfq_id)
        if not rfq: return None
        qitems = [QuotationItem(**i) if isinstance(i, dict) else i for i in (items or [])]
        for qi in qitems:
            qi.recalc()
        q = SupplierQuotation(rfq_id=rfq_id, supplier_id=supplier_id,
                              supplier_name=supplier_name, items=qitems, **kw)
        q.recalc()
        return self._repo.save_quotation(q)

    def accept_quotation(self, qid: str):
        q = self._repo.find_quotation_by_id(qid)
        if q: q.accept()
        return q

    # ── Comparison Engine (PURCHASE-005) ──────────────────────

    def compare_quotations(self, rfq_id: str) -> dict:
        return self._comparison.compare(rfq_id)

    # ── Purchase Orders (PURCHASE-006) ────────────────────────

    def create_po(self, document_id: str, supplier_id: str, supplier_name: str = '',
                  lines: list = None, **kw) -> PurchaseOrder:
        po = PurchaseOrder(document_id=document_id, supplier_id=supplier_id,
                           supplier_name=supplier_name, lines=lines or [], **kw)
        po.recalc()
        return self._repo.save_purchase_order(po)

    def create_po_from_quotation(self, quotation_id: str, document_id: str = '') -> PurchaseOrder | None:
        q = self._repo.find_quotation_by_id(quotation_id)
        if not q: return None
        lines = []
        for qi in q.items:
            lines.append(PurchaseOrderLine(
                item_id=qi.item_id, item_code=qi.item_code,
                item_name=qi.item_name, quantity=qi.quantity,
                unit_price=qi.unit_price, discount_pct=qi.discount_pct,
                discount_value=qi.discount_value, total=qi.total,
            ))
        po = PurchaseOrder(
            document_id=document_id or '',
            document_type='purchase_order',
            supplier_id=q.supplier_id, supplier_name=q.supplier_name,
            quotation_id=q._id, rfq_id=q.rfq_id,
            lines=lines, freight=q.freight,
            payment_terms=PurchasePaymentTerms(
                method=q.payment_method, installments=q.installments,
                due_days=q.due_days,
            ),
        )
        po.recalc()
        return self._repo.save_purchase_order(po)

    def list_pos(self, supplier_id: str = '', status: str = '') -> list:
        return self._repo.find_purchase_orders(supplier_id, status)

    def approve_po(self, po_id: str, by: str = ''):
        po = self._repo.find_purchase_order_by_id(po_id)
        if po:
            val = po.total
            role = self._approval.find_approver(val, ApprovalScope.PURCHASE_ORDER)
            po.approve(by or role)
        return po

    # ── Goods Receipt (PURCHASE-007) ──────────────────────────

    def receive_goods(self, po_id: str, lines_data: list = None,
                      warehouse_id: str = '', received_by: str = '',
                      notes: str = '') -> GoodsReceipt | None:
        po = self._repo.find_purchase_order_by_id(po_id)
        if not po: return None
        gr_lines = []
        for ld in (lines_data or []):
            line_id = ld.get('po_line_id', '')
            received = ld.get('received_qty', 0)
            accepted = ld.get('accepted_qty', received)
            rejected = ld.get('rejected_qty', 0)
            po.receive_line(line_id, received)
            gr_lines.append(GoodsReceiptLine(
                po_line_id=line_id,
                item_id=ld.get('item_id', ''),
                received_qty=received, accepted_qty=accepted,
                rejected_qty=rejected,
                rejection_reason=ld.get('rejection_reason', ''),
            ))
        gr = GoodsReceipt(po_id=po_id, po_number=po.document_number,
                          supplier_id=po.supplier_id,
                          supplier_name=po.supplier_name,
                          lines=gr_lines, warehouse_id=warehouse_id,
                          received_by=received_by, notes=notes)
        return self._repo.save_goods_receipt(gr)

    # ── Purchase Returns ───────────────────────────────────────

    def create_return(self, po_id: str, lines: list = None, **kw) -> PurchaseReturn | None:
        po = self._repo.find_purchase_order_by_id(po_id)
        if not po: return None
        rlines = [PurchaseReturnLine(**l) if isinstance(l, dict) else l for l in (lines or [])]
        ret = PurchaseReturn(po_id=po_id, po_number=po.document_number,
                             supplier_id=po.supplier_id,
                             supplier_name=po.supplier_name,
                             lines=rlines, **kw)
        return self._repo.save_purchase_return(ret)

    # ── Supplier Agreements (PURCHASE-008) ────────────────────

    def create_agreement(self, supplier_id: str, supplier_name: str = '',
                         name: str = '', items: list = None, **kw):
        a = SupplierAgreement(supplier_id=supplier_id,
                              supplier_name=supplier_name,
                              name=name, items=items or [], **kw)
        return self._repo.save_supplier_agreement(a)

    def list_agreements(self, supplier_id: str = '') -> list:
        return self._repo.find_supplier_agreements(supplier_id)

    # ── Approval Matrix (PURCHASE-009) ────────────────────────

    def add_approval_rule(self, scope: str, min_value: float,
                          max_value: float, approver_role: str, **kw):
        r = ApprovalMatrixRule(
            scope=ApprovalScope(scope),
            min_value=min_value, max_value=max_value,
            approver_role=approver_role, **kw)
        self._repo.save_approval_rule(r)
        self._reload_approval()
        return r

    def list_approval_rules(self, scope: str = '') -> list:
        return self._repo.find_approval_rules(scope)

    def _reload_approval(self):
        rules = self._repo.find_approval_rules()
        self._approval.set_rules(rules)

    # ── Vendor Score (PURCHASE-010) ───────────────────────────

    def evaluate_vendor(self, supplier_id: str, supplier_name: str = '',
                        po_id: str = '', **kw) -> VendorScoreEntry:
        vs = VendorScoreEntry(supplier_id=supplier_id, po_id=po_id, **kw)
        if supplier_name:
            vs.supplier_name = supplier_name
        vs.calculate_score()
        return self._repo.save_vendor_score(vs)

    def vendor_scores(self, supplier_id: str = '') -> list:
        return self._repo.find_vendor_scores(supplier_id)
