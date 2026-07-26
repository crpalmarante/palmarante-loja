from modules.sales.core.domain.repositories.sales_repository import SalesRepository
from modules.sales.core.application.services import clients as api


class PriceEngine:
    def __init__(self, repo: SalesRepository):
        self._repo = repo

    def get_item_price(self, item_id: str, price_list_id: str = '') -> float:
        if price_list_id:
            pl = self._repo.find_price_list_by_id(price_list_id)
            if pl:
                price = pl.get_price(item_id)
                if price is not None:
                    return price
        prices = api.get_catalog_prices(item_id)
        if prices:
            return prices[0].get('price', 0)
        item = api.get_item(item_id)
        if item:
            return item.get('sale_price', item.get('cost_price', 0))
        return 0.0

    def apply_to_lines(self, lines: list,
                       price_list_id: str = '') -> list:
        result = []
        for line in lines:
            item_id = line.get('item_id', '')
            item_name = line.get('item_name', '')
            if not item_id and not item_name:
                result.append(line)
                continue
            if not item_id and item_name:
                result.append(line)
                continue
            price = line.get('unit_price', 0)
            if not price:
                price = self.get_item_price(item_id, price_list_id)
            quantity = line.get('quantity', 1)
            discount_pct = line.get('discount_pct', 0)
            tax_value = line.get('tax_value', 0)
            subtotal = quantity * price
            discount_value = subtotal * discount_pct / 100 if discount_pct else line.get('discount_value', 0)
            total = subtotal - discount_value + tax_value
            result.append({
                'item_id': item_id,
                'item_name': line.get('item_name', ''),
                'item_code': line.get('item_code', ''),
                'quantity': quantity,
                'unit': line.get('unit', 'UN'),
                'unit_price': price,
                'discount_pct': discount_pct,
                'discount_value': discount_value,
                'tax_value': tax_value,
                'total': total,
            })
        return result
