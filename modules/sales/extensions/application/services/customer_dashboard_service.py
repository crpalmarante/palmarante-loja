class CustomerDashboardService:
    def __init__(self, repo):
        self._repo = repo
        self._clients = None

    @property
    def clients(self):
        if self._clients is None:
            from modules.sales.core.application.services import clients
            self._clients = clients
        return self._clients

    def get_panel(self, customer_id: str) -> dict:
        orders = self._repo.find_sales_orders(customer_id=customer_id)
        opportunities = self._repo.find_opportunities(customer_id=customer_id)
        contracts = self._repo.find_contracts(customer_id=customer_id)

        total_orders = len(orders)
        completed = [o for o in orders if o.status.value == 'completed']
        total_completed = len(completed)
        total_spent = sum(o.total for o in completed)
        avg_ticket = round(total_spent / total_completed, 2) if total_completed > 0 else 0
        last_order = max(completed, key=lambda o: o.created_at) if completed else None
        biggest_order = max(completed, key=lambda o: o.total) if completed else None
        open_orders = [o for o in orders if o.status.value in ('draft', 'approved', 'reserved')]

        from datetime import datetime
        now = datetime.now()
        days_since_last = (
            (now - last_order.created_at).days
            if last_order and last_order.created_at else None
        )

        open_value = sum(o.total for o in open_orders)
        won = [o for o in opportunities if o.status.value == 'won']
        pipeline = sum(o.expected_value for o in opportunities
                       if o.status.value in ('new', 'qualified', 'proposal', 'negotiation'))

        return {
            'customer_id': customer_id,
            'total_orders': total_orders,
            'total_spent': round(total_spent, 2),
            'avg_ticket': avg_ticket,
            'last_order_value': round(last_order.total, 2) if last_order else 0,
            'last_order_date': last_order.created_at.isoformat() if last_order else '',
            'biggest_order_value': round(biggest_order.total, 2) if biggest_order else 0,
            'days_since_last_purchase': days_since_last,
            'open_orders': len(open_orders),
            'open_value': round(open_value, 2),
            'opportunities_pipeline': round(pipeline, 2),
            'opportunities_won': len(won),
            'active_contracts': len([c for c in contracts if c.status.value == 'active']),
        }
