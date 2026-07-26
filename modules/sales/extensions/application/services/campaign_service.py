class CampaignService:
    def __init__(self, repo):
        self._repo = repo

    def find_active(self, customer_id: str = '', customer_class: str = '',
                    order_total: float = 0.0) -> list:
        return [c for c in self._repo.find_campaigns()
                if c.is_valid(customer_id, customer_class, order_total)]

    def apply_best(self, customer_id: str, customer_class: str,
                   order_total: float) -> dict:
        campaigns = self.find_active(customer_id, customer_class, order_total)
        if not campaigns:
            return {'applied': False, 'discount': 0.0, 'campaign': None}
        best = max(campaigns, key=lambda c: c.apply(order_total))
        discount = best.apply(order_total)
        best.used_count += 1
        self._repo.save_campaign(best)
        return {'applied': True, 'discount': discount,
                'campaign': {'id': best._id, 'name': best.name, 'code': best.code}}
