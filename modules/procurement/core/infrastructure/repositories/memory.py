from modules.procurement.core.domain.repositories.procurement_repository import ProcurementRepository


class ProcurementRepositoryMemory(ProcurementRepository):
    _counter = 0

    def __init__(self):
        self._rfqs = {}
        self._quotations = {}
        self._awards = {}
        self._generated_pos = {}
        self._counter_proposals = {}
        self._vendor_scores = {}
        self._purchase_orders = {}
        self._goods_receipts = {}

    def _next_id(self) -> str:
        self.__class__._counter += 1
        return str(self.__class__._counter)

    def save_rfq(self, rfq):
        if not rfq._id: rfq._id = self._next_id()
        self._rfqs[rfq._id] = rfq
        return rfq

    def find_rfq_by_id(self, rid: str):
        return self._rfqs.get(rid)

    def find_rfqs(self, status: str = '') -> list:
        r = list(self._rfqs.values())
        if status: r = [x for x in r if x.status.value == status]
        r.sort(key=lambda x: x.created_at, reverse=True)
        return r

    def save_quotation(self, q):
        if not q._id: q._id = self._next_id()
        self._quotations[q._id] = q
        return q

    def find_quotation_by_id(self, qid: str):
        return self._quotations.get(qid)

    def find_quotations(self, rfq_id: str = '', supplier_id: str = '') -> list:
        r = list(self._quotations.values())
        if rfq_id: r = [x for x in r if x.rfq_id == rfq_id]
        if supplier_id: r = [x for x in r if x.supplier_id == supplier_id]
        return r

    def save_award_decision(self, d):
        if not d._id: d._id = self._next_id()
        self._awards[d._id] = d
        return d

    def find_award_decision(self, aid: str):
        return self._awards.get(aid)

    def find_award_decisions(self, rfq_id: str = '') -> list:
        r = list(self._awards.values())
        if rfq_id: r = [x for x in r if x.rfq_id == rfq_id]
        return r

    def save_generated_po(self, po):
        if not po._id: po._id = self._next_id()
        self._generated_pos[po._id] = po
        return po

    def save_counter_proposal(self, rfq_id: str, cp):
        if not cp._id: cp._id = self._next_id()
        self._counter_proposals[cp._id] = cp
        return cp

    def find_counter_proposals(self, quotation_id: str = '') -> list:
        r = list(self._counter_proposals.values())
        if quotation_id: r = [x for x in r if x.quotation_id == quotation_id]
        return r

    def find_vendor_scores(self, supplier_id: str = '') -> list:
        if supplier_id:
            return [s for s in self._vendor_scores.values() if hasattr(s, 'supplier_id') and s.supplier_id == supplier_id]
        return list(self._vendor_scores.values())

    def save_purchase_order(self, po):
        if not po._id: po._id = self._next_id()
        self._purchase_orders[po._id] = po
        return po

    def find_purchase_orders(self, supplier_id: str = '', status: str = '') -> list:
        r = list(self._purchase_orders.values())
        if supplier_id: r = [x for x in r if x.supplier_id == supplier_id]
        r.sort(key=lambda x: x.created_at if hasattr(x, 'created_at') and x.created_at else 0, reverse=True)
        return r

    def save_goods_receipt(self, gr):
        if not gr._id: gr._id = self._next_id()
        self._goods_receipts[gr._id] = gr
        return gr

    def find_goods_receipts(self, po_id: str = '') -> list:
        r = list(self._goods_receipts.values())
        if po_id: r = [x for x in r if x.po_id == po_id]
        return r
