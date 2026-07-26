class PriceSimulationService:
    def __init__(self, repo):
        self._repo = repo
        self._clients = None

    @property
    def clients(self):
        if self._clients is None:
            from modules.sales.core.application.services import clients
            self._clients = clients
        return self._clients

    def simulate(self, item_id: str, quantity: float = 1, unit_price: float = 0,
                 discount_pct: float = 0, freight: float = 0,
                 commission_rate: float = 0, price_list_id: str = '') -> dict:
        if unit_price <= 0:
            from modules.sales.core.application.services.price_engine import PriceEngine
            unit_price = PriceEngine(self._repo).get_item_price(item_id, price_list_id)
        subtotal = unit_price * quantity
        discount_value = subtotal * discount_pct / 100 if discount_pct > 0 else 0
        net_total = subtotal - discount_value
        commission_value = net_total * commission_rate / 100 if commission_rate > 0 else 0
        total = net_total + freight

        cost_price = 0.0
        try:
            item = self.clients.get_item(item_id)
            cost_price = item.get('cost_price', 0) if item else 0
        except Exception:
            pass

        margin_value = net_total - (cost_price * quantity + commission_value + freight)
        margin_pct = (margin_value / net_total * 100) if net_total > 0 else 0

        return {
            'item_id': item_id,
            'quantity': quantity,
            'unit_price': round(unit_price, 2),
            'subtotal': round(subtotal, 2),
            'discount_pct': discount_pct,
            'discount_value': round(discount_value, 2),
            'freight': round(freight, 2),
            'commission_value': round(commission_value, 2),
            'total': round(total, 2),
            'cost_price': round(cost_price, 2),
            'margin_value': round(margin_value, 2),
            'margin_pct': round(margin_pct, 2),
            'price_list_id': price_list_id,
        }

    def simulate_order(self, lines: list, freight: float = 0,
                       commission_rate: float = 0,
                       price_list_id: str = '') -> dict:
        line_results = [self.simulate(**l, price_list_id=price_list_id)
                        for l in lines]
        totals = {
            'subtotal': sum(l['subtotal'] for l in line_results),
            'discount': sum(l['discount_value'] for l in line_results),
            'freight': freight,
            'commission': sum(l['commission_value'] for l in line_results),
            'total': sum(l['total'] for l in line_results) + freight,
            'cost': sum(l['cost_price'] * l['quantity'] for l in line_results),
            'margin_value': sum(l['margin_value'] for l in line_results),
        }
        totals['margin_pct'] = round(
            totals['margin_value'] / totals['subtotal'] * 100, 2
        ) if totals['subtotal'] > 0 else 0
        return {'lines': line_results, 'totals': totals}
