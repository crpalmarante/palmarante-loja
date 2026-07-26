from modules.procurement.core.domain.entities.award import AwardDecision, AwardItem, AwardMethod, GeneratedPO


class AwardEngine:
    def __init__(self, repo):
        self._repo = repo

    def award_single(self, rfq_id: str, supplier_id: str, quotation_id: str,
                     created_by: str = '', notes: str = '') -> AwardDecision:
        rfq = self._repo.find_rfq_by_id(rfq_id)
        if not rfq: return None
        q = self._repo.find_quotation_by_id(quotation_id)
        if not q: return None
        items = []
        for qi in q.items:
            items.append(AwardItem(
                item_id=qi.item_id, quantity=qi.quantity,
                supplier_id=supplier_id, supplier_name=q.supplier_name,
                quotation_id=quotation_id, unit_price=qi.unit_price,
                total=qi.total, delivery_days=qi.delivery_days,
            ))
        decision = AwardDecision(rfq_id=rfq_id, method=AwardMethod.SINGLE,
                                 items=items, created_by=created_by, notes=notes)
        self._repo.save_award_decision(decision)
        rfq.status = self._repo.find_rfq_by_id(rfq_id).status
        return decision

    def award_per_item(self, rfq_id: str, selections: dict,
                       created_by: str = '', notes: str = '') -> AwardDecision:
        rfq = self._repo.find_rfq_by_id(rfq_id)
        if not rfq: return None
        items = []
        for selection in selections:
            q = self._repo.find_quotation_by_id(selection.get('quotation_id'))
            if not q: continue
            qi = next((i for i in q.items if i.item_id == selection.get('item_id')), None)
            if not qi: continue
            items.append(AwardItem(
                item_id=qi.item_id, item_name=qi.item_name,
                quantity=selection.get('quantity', qi.quantity),
                supplier_id=q.supplier_id, supplier_name=q.supplier_name,
                quotation_id=selection['quotation_id'],
                unit_price=qi.unit_price, total=qi.total,
                delivery_days=selection.get('delivery_days', qi.delivery_days),
            ))
        decision = AwardDecision(rfq_id=rfq_id, method=AwardMethod.PER_ITEM,
                                 items=items, created_by=created_by, notes=notes)
        self._repo.save_award_decision(decision)
        return decision

    def generate_pos(self, award_id: str, document_base: str = '') -> list:
        decision = self._repo.find_award_decision(award_id)
        if not decision: return []

        grouped = {}
        for item in decision.items:
            key = item.supplier_id
            if key not in grouped:
                grouped[key] = {'supplier_id': item.supplier_id,
                                'supplier_name': item.supplier_name, 'items': [],
                                'total': 0}
            grouped[key]['items'].append(item)
            grouped[key]['total'] += item.total

        pos = []
        for idx, (sid, data) in enumerate(grouped.items()):
            po = GeneratedPO(
                document_id=f'{document_base or "PO"}-{award_id}-{idx+1}',
                supplier_id=data['supplier_id'],
                supplier_name=data['supplier_name'],
                total=data['total'],
                items=[{'item_id': i.item_id, 'item_name': i.item_name,
                        'quantity': i.quantity, 'unit_price': i.unit_price,
                        'total': i.total, 'delivery_days': i.delivery_days}
                       for i in data['items']],
            )
            self._repo.save_generated_po(po)
            pos.append(po)
        return pos
