class RulesEngine:
    def __init__(self, repo):
        self._repo = repo

    def evaluate_all(self, context: dict) -> list:
        rules = self._repo.find_rules()
        results = []
        for r in sorted(rules, key=lambda x: x.priority, reverse=True):
            result = r.evaluate(context)
            if result['matched']:
                results.append(result)
        return results

    def evaluate_for_order(self, customer_type: str = '', quantity: float = 0,
                           total: float = 0, channel: str = '',
                           item_category: str = '',
                           payment_method: str = '') -> list:
        context = {
            'customer_type': customer_type,
            'quantity': str(quantity),
            'total': str(total),
            'channel': channel,
            'item_category': item_category,
            'payment_method': payment_method,
        }
        return self.evaluate_all(context)
