from modules.sales.core.domain.repositories.sales_repository import SalesRepository
from modules.sales.core.domain.entities.commission import CommissionStatement, CommissionLine


class CommissionEngine:
    def __init__(self, repo: SalesRepository):
        self._repo = repo

    def calculate_order_commission(self, sales_rep_id: str,
                                   document_id: str, document_number: str,
                                   total: float, lines: list = None) -> float:
        rules = self._repo.find_commission_rules(sales_rep_id)
        if not rules:
            return 0.0
        total_commission = 0.0
        for rule in rules:
            if rule.item_ids and lines:
                for line in lines:
                    if line.get('item_id', '') in rule.item_ids:
                        line_total = (line.get('quantity', 1) * line.get('unit_price', 0)
                                      - line.get('discount_value', 0))
                        total_commission += rule.calculate(line_total, line.get('quantity', 1))
            else:
                total_commission += rule.calculate(total)
        return total_commission

    def generate_statement(self, sales_rep_id: str, sales_rep_name: str,
                           period: str, documents: list) -> CommissionStatement:
        lines = []
        total = 0.0
        for doc in documents:
            comm = self.calculate_order_commission(
                sales_rep_id, doc.get('document_id', ''),
                doc.get('document_number', ''),
                doc.get('total', 0), doc.get('lines'),
            )
            if comm > 0:
                lines.append(CommissionLine(
                    document_id=doc.get('document_id', ''),
                    document_number=doc.get('document_number', ''),
                    base_amount=doc.get('total', 0),
                    rate=0,
                    commission_value=comm,
                ))
                total += comm
        stmt = CommissionStatement(
            sales_rep_id=sales_rep_id, sales_rep_name=sales_rep_name,
            period=period, document_ids=[d.get('document_id', '') for d in documents],
            lines=lines, total_commission=total,
        )
        return self._repo.save_statement(stmt)
