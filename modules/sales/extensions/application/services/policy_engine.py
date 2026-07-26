class PolicyEngine:
    def __init__(self, repo):
        self._repo = repo

    def evaluate_all(self, context: dict) -> list:
        policies = self._repo.find_policies()
        results = []
        for p in sorted(policies, key=lambda x: x.priority, reverse=True):
            result = p.evaluate(context)
            if result['matched']:
                results.append(result)
        return results

    def evaluate_for_order(self, customer_id: str = '', customer_class: str = '',
                           order_total: float = 0, channel: str = '',
                           payment_method: str = '') -> list:
        context = {
            'customer_id': customer_id,
            'customer_class': customer_class,
            'order_total': str(order_total),
            'channel': channel,
            'payment_method': payment_method,
        }
        return self.evaluate_all(context)

    def check_blockers(self, customer_id: str = '', customer_class: str = '',
                       order_total: float = 0, channel: str = '',
                       payment_method: str = '') -> list:
        results = self.evaluate_for_order(customer_id, customer_class,
                                           order_total, channel, payment_method)
        return [r for r in results if r['action'] in ('block', 'request_approval')]
