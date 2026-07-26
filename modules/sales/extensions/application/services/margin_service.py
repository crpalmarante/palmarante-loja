class MarginService:
    def __init__(self, repo):
        self._repo = repo
        self._clients = None

    @property
    def clients(self):
        if self._clients is None:
            from modules.sales.core.application.services import clients
            self._clients = clients
        return self._clients

    def analyze_line(self, item_id: str, quantity: float = 1,
                     unit_price: float = 0, discount_value: float = 0,
                     commission_value: float = 0) -> dict:
        try:
            item = self.clients.get_item(item_id)
            cost = item.get('cost_price', 0) if item else 0
        except Exception:
            cost = 0
        total_cost = cost * quantity
        net_revenue = (unit_price * quantity) - discount_value
        margin_value = net_revenue - total_cost - commission_value
        margin_pct = (margin_value / net_revenue * 100) if net_revenue > 0 else 0

        if margin_pct >= 20:
            color = 'green'
            level = 'good'
        elif margin_pct >= 10:
            color = 'yellow'
            level = 'warning'
        else:
            color = 'red'
            level = 'critical'

        return {
            'item_id': item_id,
            'quantity': quantity,
            'unit_price': round(unit_price, 2),
            'unit_cost': round(cost, 2),
            'total_cost': round(total_cost, 2),
            'net_revenue': round(net_revenue, 2),
            'margin_value': round(margin_value, 2),
            'margin_pct': round(margin_pct, 2),
            'color': color,
            'level': level,
        }

    def analyze_order(self, lines: list) -> dict:
        results = [self.analyze_line(**l) for l in lines]
        avg_margin = sum(l['margin_pct'] for l in results) / len(results) if results else 0
        return {
            'lines': results,
            'avg_margin_pct': round(avg_margin, 2),
            'total_cost': sum(l['total_cost'] for l in results),
        }
