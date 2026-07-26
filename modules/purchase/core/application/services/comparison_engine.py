class ComparisonEngine:
    def __init__(self, repo):
        self._repo = repo

    def compare(self, rfq_id: str) -> dict:
        rfq = self._repo.find_rfq_by_id(rfq_id)
        if not rfq:
            return {}
        quotations = self._repo.find_quotations(rfq_id=rfq_id)
        matrix = []
        for item in rfq.items:
            row = {
                'item_id': item.item_id,
                'item_code': item.item_code,
                'item_name': item.item_name,
                'quantity': item.quantity,
                'expected_price': item.expected_price,
                'quotations': [],
            }
            for q in quotations:
                qi = next((i for i in q.items if i.item_id == item.item_id), None)
                row['quotations'].append({
                    'quotation_id': q._id,
                    'supplier_id': q.supplier_id,
                    'supplier_name': q.supplier_name,
                    'unit_price': qi.unit_price if qi else None,
                    'total': qi.total if qi else None,
                    'discount_pct': qi.discount_pct if qi else None,
                    'delivery_days': qi.delivery_days if qi else None,
                    'warranty_days': qi.warranty_days if qi else None,
                })
            matrix.append(row)

        summary = []
        for q in quotations:
            summary.append({
                'quotation_id': q._id,
                'supplier_id': q.supplier_id,
                'supplier_name': q.supplier_name,
                'total': q.total,
                'freight': q.freight,
                'grand_total': q.grand_total,
                'delivery_days': q.delivery_estimate_days,
                'payment_method': q.payment_method,
                'installments': q.installments,
                'valid_until': q.valid_until,
                'score': self._calculate_score(q),
            })

        summary.sort(key=lambda s: s.get('score', 0), reverse=True)

        return {
            'rfq_id': rfq_id,
            'rfq_title': rfq.title,
            'matrix': matrix,
            'summary': summary,
            'best': summary[0] if summary else None,
        }

    def _calculate_score(self, quotation) -> float:
        score = 100.0
        if quotation.grand_total > 0:
            score -= min(30, quotation.grand_total * 0.001)
        score -= min(20, quotation.delivery_estimate_days * 2)
        score -= min(10, quotation.freight * 0.005)
        return max(0, round(score, 1))
