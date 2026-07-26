from modules.procurement.core.domain.entities.rfq import RFQ, RFQItem, RFQStatus
from modules.procurement.core.domain.entities.quotation import SupplierQuotation, QuotationItem, QuotationStatus
from modules.procurement.core.domain.repositories.procurement_repository import ProcurementRepository
from modules.procurement.core.application.services.comparison_engine import ComparisonEngine
from modules.procurement.core.application.services.award_engine import AwardEngine
from modules.procurement.core.application.services.negotiation_engine import NegotiationEngine, SimulationEngine
from modules.procurement.core.application.services.supplier_portal import SupplierPortalService


class ProcurementOrchestrator:
    def __init__(self, repo: ProcurementRepository):
        self._repo = repo
        self._comparison = ComparisonEngine(repo)
        self._award = AwardEngine(repo)
        self._negotiation = NegotiationEngine(repo)
        self._simulation = SimulationEngine()
        self._portal = SupplierPortalService(repo)

    @property
    def comparison(self): return self._comparison
    @property
    def award(self): return self._award
    @property
    def negotiation(self): return self._negotiation
    @property
    def simulation(self): return self._simulation
    @property
    def portal(self): return self._portal
    @property
    def repo(self): return self._repo

    # ── RFQ ──────────────────────────────────────────────────

    def create_rfq(self, title: str, items: list = None, **kw) -> RFQ:
        rfq = RFQ(title=title, items=items or [], **kw)
        return self._repo.save_rfq(rfq)

    def open_rfq(self, rfq_id: str):
        rfq = self._repo.find_rfq_by_id(rfq_id)
        if rfq: rfq.open()
        return rfq

    def list_rfqs(self, status: str = '') -> list:
        return self._repo.find_rfqs(status)

    # ── Quotations ──────────────────────────────────────────

    def submit_quotation(self, rfq_id: str, supplier_id: str,
                         supplier_name: str = '', items: list = None, **kw):
        rfq = self._repo.find_rfq_by_id(rfq_id)
        if not rfq: return None
        qitems = [QuotationItem(**i) if isinstance(i, dict) else i for i in (items or [])]
        for qi in qitems: qi.recalc()
        q = SupplierQuotation(rfq_id=rfq_id, supplier_id=supplier_id,
                              supplier_name=supplier_name, items=qitems, **kw)
        q.recalc()
        return self._repo.save_quotation(q)

    def accept_quotation(self, qid: str):
        q = self._repo.find_quotation_by_id(qid)
        if q: q.accept()
        return q

    # ── Comparison ───────────────────────────────────────────

    def compare(self, rfq_id: str) -> dict:
        return self._comparison.compare(rfq_id)

    # ── Award ────────────────────────────────────────────────

    def award_single(self, rfq_id: str, supplier_id: str,
                     quotation_id: str, **kw):
        decision = self._award.award_single(rfq_id, supplier_id, quotation_id, **kw)
        rfq = self._repo.find_rfq_by_id(rfq_id)
        if rfq: rfq.status = RFQStatus.AWARDED
        return decision

    def award_per_item(self, rfq_id: str, selections: list, **kw):
        decision = self._award.award_per_item(rfq_id, selections, **kw)
        rfq = self._repo.find_rfq_by_id(rfq_id)
        if rfq: rfq.status = RFQStatus.AWARDED
        return decision

    def generate_pos(self, award_id: str, document_base: str = '') -> list:
        pos = self._award.generate_pos(award_id, document_base)
        for po in pos:
            self._repo.save_generated_po(po)
        return pos

    # ── Negotiation ──────────────────────────────────────────

    def make_counter(self, rfq_id: str, quotation_id: str,
                     proposed_by: str, **kw):
        return self._negotiation.make_counter(rfq_id, quotation_id, proposed_by, **kw)

    def negotiation_history(self, quotation_id: str) -> list:
        return self._negotiation.negotiation_history(quotation_id)

    # ── Simulation ───────────────────────────────────────────

    def simulate(self, quotation_id: str, changes: dict) -> dict:
        q = self._repo.find_quotation_by_id(quotation_id)
        if not q: return {}
        return self._simulation.simulate(q, changes)

    # ── Supplier Portal ─────────────────────────────────────

    def portal_invitations(self, supplier_id: str) -> list:
        return self._portal.invitations_for_supplier(supplier_id)

    def portal_submit(self, rfq_id: str, supplier_id: str,
                      supplier_name: str, items: list, **kw):
        return self._portal.submit_quotation(rfq_id, supplier_id,
                                              supplier_name, items, **kw)

    # ── Operational PO ──────────────────────────────────────

    def list_pos(self, supplier_id: str = '', status: str = '') -> list:
        return self._repo.find_purchase_orders(supplier_id, status)

    def list_receipts(self, po_id: str = '') -> list:
        return self._repo.find_goods_receipts(po_id)
