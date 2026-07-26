from modules.sales.core.application.commands.sales_commands import (
    CreateSalesOrder, ReserveInventory, ReleaseInventory,
    GenerateShipment, GenerateInvoice, CancelOrder, CloseOrder,
)
from modules.sales.core.application.services import clients
from modules.sales.core.application.services.price_engine import PriceEngine
from modules.sales.core.application.services.discount_engine import DiscountEngine
from modules.sales.core.application.services.commission_engine import CommissionEngine
from modules.sales.core.domain.repositories.sales_repository import SalesRepository
from modules.sales.core.domain.entities.sales_order import (
    SalesOrder, SalesOrderLine, SalesOrderStatus,
    SalesPaymentTerms, PaymentMethod,
    SalesShipment, SalesRepresentative, SalesCommission,
)


class CreateSalesOrderUseCase:
    def __init__(self, repo: SalesRepository):
        self._repo = repo
        self.prices = PriceEngine(repo)
        self.discounts = DiscountEngine(repo)

    def execute(self, cmd: CreateSalesOrder) -> SalesOrder:
        party = clients.get_party(cmd.customer_id)
        cust_name = cmd.customer_name or (party.get('name', '') if party else '')

        lines = self.prices.apply_to_lines(cmd.lines or [], cmd.price_list_id)
        lines = self.discounts.apply_to_lines(lines, cmd.discount_rule_ids)

        parties = [{'party_id': cmd.customer_id, 'party_type': 'customer', 'party_name': cust_name}]
        references = []
        if cmd.opportunity_id:
            references.append({'reference_type': 'opportunity', 'reference_id': cmd.opportunity_id})

        doc_resp = clients.create_document(
            doc_type='sale_order', direction='out',
            lines=lines, parties=parties,
            references=references or None,
            notes=cmd.notes, header={'responsible': cmd.sales_rep},
            created_by=cmd.sales_rep,
        )
        doc = doc_resp.get('data', doc_resp)
        doc_id, doc_number = doc.get('id', ''), doc.get('number', '')

        so_lines = [SalesOrderLine(**{k: l.get(k) for k in
                     ['item_id','item_code','item_name','quantity','unit',
                      'unit_price','discount_pct','discount_value','tax_value','total']
                     if k in l}) for l in lines]

        so = SalesOrder(
            document_id=doc_id, document_number=doc_number,
            customer_id=cmd.customer_id, customer_name=cust_name,
            sales_rep=SalesRepresentative(rep_id=cmd.sales_rep, name=cmd.sales_rep,
                                          commission_rate=cmd.rep_commission_rate)
            if cmd.sales_rep else None,
            payment_terms=SalesPaymentTerms(
                method=PaymentMethod(cmd.payment_method),
                installments=cmd.installments, due_days=cmd.due_days,
            ),
            lines=so_lines,
            subtotal=sum(l.get('unit_price',0)*l.get('quantity',1) for l in lines),
            discount_total=sum(l.get('discount_value',0) for l in lines),
            tax_total=sum(l.get('tax_value',0) for l in lines),
            total=doc.get('total', 0),
            notes=cmd.notes, opportunity_id=cmd.opportunity_id or '',
            expected_delivery=cmd.expected_delivery or '',
            created_by=cmd.sales_rep,
        )

        so.generate_installments()

        if cmd.sales_rep and cmd.rep_commission_rate > 0:
            comm = SalesCommission(rep_id=cmd.sales_rep, rep_name=cmd.sales_rep,
                                    rate=cmd.rep_commission_rate)
            comm.calculate(so.total)
            so.add_commission(comm)

        so = self._repo.save_sales_order(so)

        if cmd.opportunity_id:
            opp = self._repo.find_opportunity_by_id(cmd.opportunity_id)
            if opp:
                opp.win()
                self._repo.save_opportunity(opp)

        return so


class ReserveInventoryUseCase:
    def __init__(self, repo: SalesRepository):
        self._repo = repo

    def execute(self, cmd: ReserveInventory) -> dict:
        doc = clients.get_document(cmd.document_id)
        data = doc.get('data', doc)
        lines = data.get('lines', [])
        warehouse = cmd.warehouse_id or 'default'
        reservations = []
        for line in lines:
            if line.get('item_id'):
                try:
                    r = clients.reserve_inventory(line['item_id'], warehouse,
                                                   line['quantity'],
                                                   order_id=cmd.document_id)
                    reservations.append(r.get('data', r))
                except Exception as e:
                    raise ValueError(f'Reservation failed: {e}')
        so = self._repo.find_sales_order_by_document(cmd.document_id)
        if so:
            so.status = SalesOrderStatus.RESERVED
            self._repo.save_sales_order(so)
        clients.change_document_status(cmd.document_id, 'reserved',
                                        comment='Inventory reserved')
        return {'document_id': cmd.document_id, 'reservations': reservations}


class GenerateShipmentUseCase:
    def __init__(self, repo: SalesRepository):
        self._repo = repo

    def execute(self, cmd: GenerateShipment) -> SalesOrder:
        so = self._repo.find_sales_order_by_document(cmd.document_id)
        if not so:
            raise ValueError(f'SalesOrder for {cmd.document_id} not found')
        doc = clients.get_document(cmd.document_id)
        data = doc.get('data', doc)
        items = [{'item_id': l.get('item_id',''), 'item_name': l.get('item_name',''),
                  'quantity': l.get('quantity',0)} for l in data.get('lines',[]) if l.get('item_id')]
        shipment = SalesShipment(
            document_id=cmd.document_id, document_number=so.document_number,
            carrier=cmd.carrier, origin_warehouse=cmd.origin_warehouse,
            tracking_code=cmd.tracking_code, items=items, notes=cmd.notes,
        )
        so.add_shipment(shipment)
        self._repo.save_sales_order(so)
        clients.change_document_status(cmd.document_id, 'picking',
                                        comment='Shipment generated',
                                        performed_by=cmd.created_by)
        return self._repo.save_sales_order(so)


class GenerateInvoiceUseCase:
    def __init__(self, repo: SalesRepository):
        self._repo = repo

    def execute(self, cmd: GenerateInvoice) -> dict:
        doc = clients.get_document(cmd.document_id)
        data = doc.get('data', doc)
        lines = data.get('lines', [])
        parties = data.get('parties', [])
        doc_type = 'nfe' if cmd.fiscal else 'invoice'
        resp = clients.create_document(
            doc_type=doc_type, direction='out',
            lines=lines, parties=parties,
            references=[{'reference_type': 'sale_order',
                         'reference_id': cmd.document_id,
                         'reference_number': data.get('number','')}],
            created_by=cmd.created_by,
        )
        inv = resp.get('data', resp)
        so = self._repo.find_sales_order_by_document(cmd.document_id)
        if so:
            so.status = SalesOrderStatus.INVOICED
            self._repo.save_sales_order(so)
        clients.change_document_status(cmd.document_id, 'invoiced',
                                        comment=f'Invoice {inv.get("number","")} created',
                                        performed_by=cmd.created_by)
        return inv


class CancelSalesOrderUseCase:
    def __init__(self, repo: SalesRepository):
        self._repo = repo

    def execute(self, cmd: CancelOrder) -> SalesOrder:
        so = self._repo.find_sales_order_by_document(cmd.document_id)
        if not so:
            raise ValueError(f'SalesOrder for {cmd.document_id} not found')
        so.cancel()
        so = self._repo.save_sales_order(so)
        clients.change_document_status(cmd.document_id, 'cancelled',
                                        comment=cmd.reason or 'Cancelado',
                                        performed_by=cmd.performed_by)
        try:
            clients.record_movement('', '', 'adjustment', 0,
                                    reference_type='cancellation',
                                    reference_id=cmd.document_id)
        except Exception:
            pass
        return so


class CloseSalesOrderUseCase:
    def __init__(self, repo: SalesRepository):
        self._repo = repo

    def execute(self, cmd: CloseOrder) -> SalesOrder:
        so = self._repo.find_sales_order_by_document(cmd.document_id)
        if not so:
            raise ValueError(f'SalesOrder for {cmd.document_id} not found')
        so.status = SalesOrderStatus.COMPLETED
        so.updated_at = __import__('datetime').datetime.now()
        so = self._repo.save_sales_order(so)
        clients.change_document_status(cmd.document_id, 'completed',
                                        comment='Pedido concluído',
                                        performed_by=cmd.performed_by)
        return so
