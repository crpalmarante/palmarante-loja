from modules.purchase.core.domain.repositories.purchase_repository import PurchaseRepository


class PurchaseRepositoryMemory(PurchaseRepository):
    _counter = 0

    def __init__(self):
        self._requests = {}
        self._requisitions = {}
        self._rfqs = {}
        self._quotations = {}
        self._orders = {}
        self._receipts = {}
        self._returns = {}
        self._agreements = {}
        self._approval_rules = {}
        self._vendor_scores = {}

    def _next_id(self) -> str:
        self.__class__._counter += 1
        return str(self.__class__._counter)

    # Purchase Requests
    def save_purchase_request(self, pr):
        if not pr._id:
            pr._id = self._next_id()
        self._requests[pr._id] = pr
        return pr

    def find_purchase_request_by_id(self, prid: str):
        return self._requests.get(prid)

    def find_purchase_requests(self, status: str = '', requestor: str = '') -> list:
        r = list(self._requests.values())
        if status: r = [x for x in r if x.status.value == status]
        if requestor: r = [x for x in r if x.requestor == requestor]
        r.sort(key=lambda x: x.created_at, reverse=True)
        return r

    # Purchase Requisitions
    def save_purchase_requisition(self, pr):
        if not pr._id:
            pr._id = self._next_id()
        self._requisitions[pr._id] = pr
        return pr

    def find_purchase_requisition_by_id(self, prid: str):
        return self._requisitions.get(prid)

    def find_purchase_requisitions(self, status: str = '') -> list:
        r = list(self._requisitions.values())
        if status: r = [x for x in r if x.status.value == status]
        r.sort(key=lambda x: x.created_at, reverse=True)
        return r

    # RFQs
    def save_rfq(self, rfq):
        if not rfq._id:
            rfq._id = self._next_id()
        self._rfqs[rfq._id] = rfq
        return rfq

    def find_rfq_by_id(self, rid: str):
        return self._rfqs.get(rid)

    def find_rfqs(self, status: str = '') -> list:
        r = list(self._rfqs.values())
        if status: r = [x for x in r if x.status.value == status]
        r.sort(key=lambda x: x.created_at, reverse=True)
        return r

    # Quotations
    def save_quotation(self, q):
        if not q._id:
            q._id = self._next_id()
        self._quotations[q._id] = q
        return q

    def find_quotation_by_id(self, qid: str):
        return self._quotations.get(qid)

    def find_quotations(self, rfq_id: str = '', supplier_id: str = '') -> list:
        r = list(self._quotations.values())
        if rfq_id: r = [x for x in r if x.rfq_id == rfq_id]
        if supplier_id: r = [x for x in r if x.supplier_id == supplier_id]
        return r

    # Purchase Orders
    def save_purchase_order(self, po):
        if not po._id:
            po._id = self._next_id()
        self._orders[po._id] = po
        return po

    def find_purchase_order_by_id(self, po_id: str):
        return self._orders.get(po_id)

    def find_purchase_order_by_document(self, document_id: str):
        for po in self._orders.values():
            if po.document_id == document_id:
                return po
        return None

    def find_purchase_orders(self, supplier_id: str = '', status: str = '') -> list:
        r = list(self._orders.values())
        if supplier_id: r = [x for x in r if x.supplier_id == supplier_id]
        if status: r = [x for x in r if x.status.value == status]
        r.sort(key=lambda x: x.created_at, reverse=True)
        return r

    # Goods Receipts
    def save_goods_receipt(self, gr):
        if not gr._id:
            gr._id = self._next_id()
        self._receipts[gr._id] = gr
        return gr

    def find_goods_receipts(self, po_id: str = '') -> list:
        r = list(self._receipts.values())
        if po_id: r = [x for x in r if x.po_id == po_id]
        return r

    # Purchase Returns
    def save_purchase_return(self, pr):
        if not pr._id:
            pr._id = self._next_id()
        self._returns[pr._id] = pr
        return pr

    def find_purchase_returns(self, po_id: str = '') -> list:
        r = list(self._returns.values())
        if po_id: r = [x for x in r if x.po_id == po_id]
        return r

    # Supplier Agreements
    def save_supplier_agreement(self, a):
        if not a._id:
            a._id = self._next_id()
        self._agreements[a._id] = a
        return a

    def find_supplier_agreements(self, supplier_id: str = '') -> list:
        r = list(self._agreements.values())
        if supplier_id: r = [x for x in r if x.supplier_id == supplier_id]
        return r

    def find_supplier_agreement_by_id(self, aid: str):
        return self._agreements.get(aid)

    # Approval Rules
    def save_approval_rule(self, r):
        if not r._id:
            r._id = self._next_id()
        self._approval_rules[r._id] = r
        return r

    def find_approval_rules(self, scope: str = '') -> list:
        r = list(self._approval_rules.values())
        if scope: r = [x for x in r if x.scope.value == scope]
        return r

    # Vendor Scores
    def save_vendor_score(self, vs):
        if not vs._id:
            vs._id = self._next_id()
        self._vendor_scores[vs._id] = vs
        return vs

    def find_vendor_scores(self, supplier_id: str = '') -> list:
        r = list(self._vendor_scores.values())
        if supplier_id: r = [x for x in r if x.supplier_id == supplier_id]
        return r
