from modules.sales.core.domain.repositories.sales_repository import SalesRepository
from modules.sales.core.domain.entities.discount_rule import DiscountRule


class DiscountEngine:
    def __init__(self, repo: SalesRepository):
        self._repo = repo

    def apply_to_lines(self, lines: list,
                       rule_ids: list = None) -> list:
        rules = self._repo.find_active_discount_rules()
        if rule_ids:
            rules = [r for r in rules if r._id in rule_ids]
        if not rules:
            return lines
        result = []
        for line in lines:
            price = line.get('unit_price', 0)
            quantity = line.get('quantity', 1)
            order_total = sum(l.get('unit_price', 0) * l.get('quantity', 1) for l in lines)
            line_total = price * quantity
            total_discount = 0.0
            for rule in sorted(rules, key=lambda r: r.priority, reverse=True):
                if rule.item_ids and line.get('item_id', '') not in rule.item_ids:
                    continue
                if rule.min_order_value > 0 and order_total < rule.min_order_value:
                    continue
                total_discount += rule.calculate(line_total, quantity, order_total)
            max_disc = price * quantity
            total_discount = min(total_discount, max_disc)
            line['discount_value'] = line.get('discount_value', 0) + total_discount
            line['total'] = (price * quantity) - line['discount_value'] + line.get('tax_value', 0)
            result.append(line)
        return result
