WEIGHT_DEFAULTS = {
    'price': 35,
    'delivery': 20,
    'freight': 15,
    'quality': 15,
    'history': 10,
    'warranty': 5,
}


class ComparisonEngine:
    def __init__(self, repo):
        self._repo = repo
        self._weights = dict(WEIGHT_DEFAULTS)

    def set_weights(self, weights: dict):
        self._weights.update(weights)

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
                'description': item.description,
                'quantity': item.quantity,
                'unit': item.unit,
                'expected_price': item.expected_price,
                'technical_specs': [{'field': s.field, 'value': s.value, 'unit': s.unit,
                                     'is_differentiator': s.is_differentiator}
                                    for s in (item.technical_specs or [])],
                'quotations': [],
                'best_offer': None,
            }
            best_price = float('inf')
            for q in quotations:
                qi = next((i for i in q.items if i.item_id == item.item_id), None)
                if not qi:
                    continue
                row['quotations'].append({
                    'quotation_id': q._id,
                    'supplier_id': q.supplier_id,
                    'supplier_name': q.supplier_name,
                    'unit_price': qi.unit_price,
                    'subtotal': qi.subtotal,
                    'discount_pct': qi.discount_pct,
                    'total': qi.total,
                    'delivery_days': qi.delivery_days,
                    'warranty_days': qi.warranty_days,
                    'technical_response': qi.technical_response or {},
                    'freight': q.freight,
                    'payment_method': q.payment_method,
                    'installments': q.installments,
                    'grand_total_share': self._prorate(qi.total, q.total, q.grand_total),
                    'score': 0,
                })
                if qi.unit_price < best_price:
                    best_price = qi.unit_price
                    row['best_offer'] = {
                        'supplier_name': q.supplier_name,
                        'unit_price': best_price,
                    }
            matrix.append(row)

        summary = []
        for q in quotations:
            supplier_history = self._get_supplier_history(q.supplier_id)
            s = {
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
                'warranty': q.warranty_description,
                'score': self._calculate_score(q),
                'score_detail': self._score_detail(q),
                'history': supplier_history,
            }
            summary.append(s)

        summary.sort(key=lambda s: s.get('score', 0), reverse=True)

        return {
            'rfq_id': rfq_id,
            'rfq_title': rfq.title,
            'requires_technical': rfq.requires_technical_evaluation,
            'weights': self._weights,
            'matrix': matrix,
            'summary': summary,
            'best': summary[0] if summary else None,
            'decision_matrix': self._build_decision_matrix(summary),
        }

    def _calculate_score(self, q) -> float:
        score = 0.0
        w = self._weights
        if q.grand_total > 0:
            price_score = max(0, 100 - (q.grand_total * 0.001))
            score += price_score * w['price'] / 100
        delivery_score = max(0, 100 - q.delivery_estimate_days * 2)
        score += delivery_score * w['delivery'] / 100
        freight_score = max(0, 100 - q.freight * 0.2)
        score += freight_score * w['freight'] / 100
        if w['warranty'] > 0:
            warranty_score = min(100, q.warranty_description.count('mês') * 20 or 50)
            score += warranty_score * w['warranty'] / 100
        if w['history'] > 0:
            history = self._get_supplier_history(q.supplier_id)
            avg_score = history.get('avg_score', 50) or 50
            score += avg_score * w['history'] / 100
        return round(score, 1)

    def _score_detail(self, q) -> dict:
        w = self._weights
        price_score = max(0, 100 - (q.grand_total * 0.001)) if q.grand_total > 0 else 0
        delivery_score = max(0, 100 - q.delivery_estimate_days * 2)
        freight_score = max(0, 100 - q.freight * 0.2)
        warranty_score = min(100, q.warranty_description.count('mês') * 20 or 50)
        history = self._get_supplier_history(q.supplier_id)
        return {
            'price': round(price_score * w['price'] / 100, 1),
            'delivery': round(delivery_score * w['delivery'] / 100, 1),
            'freight': round(freight_score * w['freight'] / 100, 1),
            'warranty': round(warranty_score * w['warranty'] / 100, 1),
            'history_score': round((history.get('avg_score', 50) or 50) * w['history'] / 100, 1),
        }

    def _build_decision_matrix(self, summary: list) -> list:
        matrix = []
        for s in summary:
            row = {
                'supplier_name': s['supplier_name'],
                'supplier_id': s['supplier_id'],
                'price': f"R$ {s['grand_total']:,.2f}",
                'delivery': f"{s['delivery_days']} dias",
                'freight': f"R$ {s['freight']:,.2f}",
                'warranty': s.get('warranty', '-'),
                'payment': f"{s['installments']}x {s['payment_method']}",
                'score': s['score'],
                'score_detail': s['score_detail'],
                'history': {
                    'rating': s['history'].get('avg_score', 0),
                    'on_time': s['history'].get('on_time_pct', 0),
                    'quality': s['history'].get('quality_pct', 0),
                },
            }
            matrix.append(row)
        matrix.sort(key=lambda r: r['score'], reverse=True)
        return matrix

    def _prorate(self, item_total: float, quotation_total: float, grand_total: float) -> float:
        if quotation_total <= 0:
            return 0
        return round(item_total / quotation_total * grand_total, 2) if item_total else 0

    def _get_supplier_history(self, supplier_id: str) -> dict:
        scores = self._repo.find_vendor_scores(supplier_id)
        if not scores:
            return {'avg_score': 0, 'total_evaluations': 0,
                    'on_time_pct': 0, 'quality_pct': 0, 'defect_rate': 0}
        avg = sum(s.criteria.overall_score for s in scores) / len(scores)
        on_time = sum(1 for s in scores if getattr(s, 'on_time_delivery', True))
        return {
            'avg_score': round(avg, 1),
            'total_evaluations': len(scores),
            'on_time_pct': round(on_time / len(scores) * 100, 1),
            'quality_pct': round(avg, 1),
            'defect_rate': round(sum(getattr(s, 'defect_rate', 0) for s in scores) / len(scores), 1),
        }
