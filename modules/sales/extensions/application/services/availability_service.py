class AvailabilityService:
    def __init__(self, repo):
        self._repo = repo
        self._clients = None

    @property
    def clients(self):
        if self._clients is None:
            from modules.sales.core.application.services import clients
            self._clients = clients
        return self._clients

    def check_availability(self, item_id: str, warehouse_id: str = '',
                           quantity: float = 1) -> dict:
        try:
            avail = self.clients.get_availability(item_id, warehouse_id)
        except Exception:
            avail = {'data': {'available': 0, 'reserved': 0, 'physical': 0}}
        data = avail.get('data', avail)
        available = data.get('available', 0)
        reserved = data.get('reserved', 0)
        physical = data.get('physical', 0)
        return {
            'item_id': item_id,
            'available': available,
            'reserved': reserved,
            'physical': physical,
            'requested': quantity,
            'can_promise': available >= quantity,
            'estimated_date': self._estimate_date(item_id, available, quantity),
        }

    def check_order_lines(self, lines: list, warehouse_id: str = '') -> list:
        results = []
        for line in lines:
            item_id = line.get('item_id', '')
            qty = line.get('quantity', 1)
            if item_id:
                results.append(self.check_availability(item_id, warehouse_id, qty))
        return results

    def _estimate_date(self, item_id: str, available: float,
                       requested: float) -> str:
        if available >= requested:
            from datetime import datetime, timedelta
            return (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        return ''
