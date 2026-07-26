from modules.procurement.core.domain.entities.negotiation import CounterProposal, NegotiationItem, NegotiationRound


class NegotiationEngine:
    def __init__(self, repo):
        self._repo = repo

    def make_counter(self, rfq_id: str, quotation_id: str, proposed_by: str,
                     supplier_id: str = '', items: list = None, **kw) -> CounterProposal | None:
        q = self._repo.find_quotation_by_id(quotation_id)
        if not q: return None
        nitems = [NegotiationItem(**i) if isinstance(i, dict) else i for i in (items or [])]
        proposal = CounterProposal(
            proposed_by=proposed_by, supplier_id=supplier_id or q.supplier_id,
            quotation_id=quotation_id, items=nitems,
            round=NegotiationRound.COUNTER if proposed_by == 'buyer' else NegotiationRound.INITIAL,
            **kw,
        )
        self._repo.save_counter_proposal(rfq_id, proposal)
        q.mark_countered()
        return proposal

    def negotiation_history(self, quotation_id: str) -> list:
        return self._repo.find_counter_proposals(quotation_id)

    def accept_counter(self, quotation_id: str, counter_id: str) -> dict:
        q = self._repo.find_quotation_by_id(quotation_id)
        if not q: return {}
        q.accept()
        updated_items = []
        counter = None
        for cp in self._repo.find_counter_proposals(quotation_id):
            if cp._id == counter_id:
                counter = cp
                break
        if counter:
            q.total = counter.total or q.total
            q.freight = counter.freight or q.freight
            q.grand_total = counter.grand_total or q.grand_total
            q.delivery_estimate_days = counter.delivery_days or q.delivery_estimate_days
            for ni in counter.items:
                existing = next((i for i in q.items if i.item_id == ni.item_id), None)
                if existing:
                    existing.unit_price = ni.unit_price or existing.unit_price
                    existing.discount_pct = ni.discount_pct or existing.discount_pct
                    existing.recalc()
            q.recalc()
        return {'quotation_id': quotation_id, 'status': q.status.value,
                'grand_total': q.grand_total, 'delivery_days': q.delivery_estimate_days}


class SimulationEngine:
    def simulate(self, quotation, changes: dict) -> dict:
        base_total = quotation.grand_total
        new_qty = changes.get('quantity')
        new_freight = changes.get('freight')
        split_deliveries = changes.get('split_deliveries')
        results = {'base_total': base_total}

        if new_qty:
            ratio = new_qty / sum(i.quantity for i in quotation.items)
            results['recalculated_total'] = round(base_total * ratio, 2)
            results['scenario'] = f'Quantidade ajustada para {new_qty}'

        if new_freight is not None:
            adj = results.get('recalculated_total', base_total) - quotation.freight + new_freight
            results['recalculated_total'] = round(adj, 2)
            results['scenario'] = (results.get('scenario', '') +
                                   f', frete ajustado para R$ {new_freight}')

        if split_deliveries:
            results['split_schedule'] = [
                {'parcel': i + 1, 'quantity': pct / 100 * new_qty if new_qty else 0,
                 'date': date}
                for i, (pct, date) in enumerate(split_deliveries)
            ]

        results['savings'] = round(base_total - results.get('recalculated_total', base_total), 2)
        return results
