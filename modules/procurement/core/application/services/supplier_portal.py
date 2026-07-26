class SupplierPortalService:
    def __init__(self, repo):
        self._repo = repo

    def invitations_for_supplier(self, supplier_id: str) -> list:
        rfqs = self._repo.find_rfqs(status='open')
        invited = []
        for rfq in rfqs:
            if supplier_id in rfq.invited_suppliers:
                has_quoted = any(
                    q.supplier_id == supplier_id
                    for q in self._repo.find_quotations(rfq_id=rfq._id)
                )
                invited.append({
                    'rfq_id': rfq._id,
                    'title': rfq.title,
                    'number': rfq.number,
                    'description': rfq.description,
                    'items': [{'item_id': i.item_id, 'item_code': i.item_code,
                               'item_name': i.item_name, 'quantity': i.quantity,
                               'unit': i.unit, 'technical_specs': i.technical_specs}
                              for i in rfq.items],
                    'delivery_address': rfq.delivery_address,
                    'payment_terms': rfq.payment_terms,
                    'valid_until': rfq.valid_until,
                    'has_quoted': has_quoted,
                })
        return invited

    def submit_quotation(self, rfq_id: str, supplier_id: str,
                         supplier_name: str, items: list,
                         **kw):
        from modules.procurement.core.domain.entities.quotation import SupplierQuotation, QuotationItem
        qitems = []
        for i in items:
            qi = QuotationItem(
                item_id=i.get('item_id'), item_code=i.get('item_code', ''),
                quantity=i.get('quantity', 1), unit_price=i.get('unit_price', 0),
                discount_pct=i.get('discount_pct', 0),
                delivery_days=i.get('delivery_days', 0),
                warranty_days=i.get('warranty_days', 0),
                notes=i.get('notes', ''),
            )
            qi.recalc()
            qitems.append(qi)
        q = SupplierQuotation(rfq_id=rfq_id, supplier_id=supplier_id,
                              supplier_name=supplier_name, items=qitems,
                              supplier_email=kw.get('supplier_email', ''),
                              supplier_phone=kw.get('supplier_phone', ''),
                              freight=kw.get('freight', 0),
                              payment_method=kw.get('payment_method', 'boleto'),
                              installments=kw.get('installments', 1),
                              delivery_estimate_days=kw.get('delivery_estimate_days', 0),
                              valid_until=kw.get('valid_until', ''),
                              warranty_description=kw.get('warranty_description', ''),
                              notes=kw.get('notes', ''),
                              terms_acceptance=kw.get('terms_acceptance', ''),
                              )
        q.recalc()
        return self._repo.save_quotation(q)
