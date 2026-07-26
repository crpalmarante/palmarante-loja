from modules.sales.extensions.domain.entities.credit import CustomerCredit, CreditStatus


class CreditService:
    def __init__(self, repo):
        self._repo = repo

    def get_or_create_credit(self, customer_id: str, customer_name: str = '') -> CustomerCredit:
        credit = self._find_credit(customer_id)
        if not credit:
            credit = CustomerCredit(customer_id=customer_id, customer_name=customer_name)
            credit = self._repo.save_credit(credit)
        return credit

    def set_limit(self, customer_id: str, limit: float, notes: str = '') -> CustomerCredit:
        credit = self.get_or_create_credit(customer_id)
        credit.credit_limit = limit
        credit.notes = notes or credit.notes
        credit.available_balance = limit - credit.used_balance
        return self._repo.save_credit(credit)

    def check_order(self, customer_id: str, order_total: float) -> dict:
        credit = self.get_or_create_credit(customer_id)
        status = credit.check_order(order_total)
        self._repo.save_credit(credit)
        return {
            'customer_id': customer_id,
            'credit_limit': credit.credit_limit,
            'used_balance': credit.used_balance,
            'available': credit.available_balance,
            'needed': order_total,
            'status': status.value,
            'approved': status == CreditStatus.APPROVED,
        }

    def _find_credit(self, customer_id: str):
        return self._repo.find_credit_by_customer(customer_id)
