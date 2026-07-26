from modules.sales.core.application.commands.sales_commands import (
    CreateQuotation, ApproveQuotation, ConvertQuotationToOrder,
)
from modules.sales.core.application.services import clients
from modules.sales.core.application.services.price_engine import PriceEngine
from modules.sales.core.application.services.discount_engine import DiscountEngine
from modules.sales.core.application.services.commission_engine import CommissionEngine
from modules.sales.core.domain.repositories.sales_repository import SalesRepository
from modules.sales.core.domain.entities.sales_order import (
    SalesOrder, SalesOrderLine, SalesOrderStatus,
    SalesPaymentTerms, PaymentMethod,
    SalesRepresentative, SalesCommission,
)


class CreateQuotationUseCase:
    def __init__(self, repo: SalesRepository):
        self._repo = repo
        self.prices = PriceEngine(repo)
        self.discounts = DiscountEngine(repo)

    def execute(self, cmd: CreateQuotation) -> dict:
        party = clients.get_party(cmd.customer_id)
        cust_name = cmd.customer_name or (party.get('name', '') if party else '')
        parties = [{'party_id': cmd.customer_id, 'party_type': 'customer', 'party_name': cust_name}]
        lines = self.prices.apply_to_lines(cmd.lines or [], cmd.price_list_id)
        lines = self.discounts.apply_to_lines(lines)
        resp = clients.create_document(
            doc_type='quotation', direction='out',
            lines=lines, parties=parties,
            notes=cmd.notes, header={'responsible': cmd.sales_rep, 'payment_terms': cmd.payment_terms},
            created_by=cmd.sales_rep,
        )
        return resp.get('data', resp)


class ApproveQuotationUseCase:
    def __init__(self, repo: SalesRepository):
        self._repo = repo

    def execute(self, cmd: ApproveQuotation) -> dict:
        resp = clients.change_document_status(
            cmd.quotation_id, 'approved',
            comment=cmd.comment or 'Aprovado via Sales',
            performed_by=cmd.performed_by,
        )
        return resp.get('data', resp)


class ConvertQuotationUseCase:
    def __init__(self, repo: SalesRepository):
        self._repo = repo
        self.create_order_uc = None

    def execute(self, cmd: ConvertQuotationToOrder) -> SalesOrder:
        doc = clients.get_document(cmd.quotation_document_id)
        data = doc.get('data', doc)
        from modules.sales.core.application.use_cases.order_use_cases import CreateSalesOrderUseCase
        if not self.create_order_uc:
            self.create_order_uc = CreateSalesOrderUseCase(self._repo)
        order_cmd = __import__('modules.sales.core.application.commands.sales_commands',
                                fromlist=['CreateSalesOrder']).CreateSalesOrder(
            customer_id=data.get('parties', [{}])[0].get('party_id', ''),
            customer_name=data.get('parties', [{}])[0].get('party_name', ''),
            lines=[{'item_id': l.get('item_id', ''), 'item_name': l.get('item_name', ''),
                    'quantity': l.get('quantity', 1), 'unit_price': l.get('unit_price', 0)} for l in data.get('lines', [])],
            notes=f'Convertido da cotação {data.get("number", "")}',
            sales_rep=cmd.sales_rep,
            price_list_id=cmd.price_list_id,
        )
        so = self.create_order_uc.execute(order_cmd)
        clients.change_document_status(cmd.quotation_document_id, 'converted',
                                        comment=f'Convertido para pedido {so.document_number}',
                                        performed_by=cmd.sales_rep)
        return so
