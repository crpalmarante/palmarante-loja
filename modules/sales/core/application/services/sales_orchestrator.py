"""SalesOrchestrator — facade that delegates each operation to its Use Case.

Each use case encapsulates a single business transaction:
1. Receives a typed Command
2. Validates business rules
3. Calls external platform APIs
4. Updates the SalesOrder aggregate
5. Returns result

Sales Platform never calculates taxes, never moves inventory,
and never generates accounting entries directly — it only
publishes intentions and coordinates the flow.
"""
from modules.sales.core.application.commands.sales_commands import (
    CreateQuotation, ApproveQuotation, ConvertQuotationToOrder,
    CreateSalesOrder, ReserveInventory, ReleaseInventory,
    GenerateShipment, GenerateInvoice, CancelOrder, CloseOrder,
)
from modules.sales.core.application.use_cases.quotation_use_cases import (
    CreateQuotationUseCase, ApproveQuotationUseCase, ConvertQuotationUseCase,
)
from modules.sales.core.application.use_cases.order_use_cases import (
    CreateSalesOrderUseCase, ReserveInventoryUseCase,
    GenerateShipmentUseCase, GenerateInvoiceUseCase,
    CancelSalesOrderUseCase, CloseSalesOrderUseCase,
)
from modules.sales.core.domain.repositories.sales_repository import SalesRepository
from modules.sales.core.domain.entities.opportunity import Opportunity
from modules.sales.core.domain.entities.contract import Contract, ContractLine
from modules.sales.core.domain.entities.return_request import ReturnRequest, ReturnItem
from modules.sales.core.domain.entities.order_template import OrderTemplate, OrderTemplateLine
from modules.sales.core.domain.entities.team import SalesTeamMember
from modules.sales.core.domain.entities.timeline import TimelineEntry, TimelineEventType
from modules.sales.core.domain.entities.note import SalesNote, NoteType
from modules.sales.core.domain.entities.attachment import SalesAttachment
from modules.sales.core.domain.entities.delivery_term import DeliveryTerm, DeliveryTermCode
from modules.sales.extensions.domain.entities.experience import (
    FavoriteItem, PriceHistoryEntry, SalesTag,
    SalesChannel, CustomerClass, ApprovalMatrixRule,
)
from modules.sales.core.application.services import clients


class SalesOrchestrator:
    def __init__(self, repo: SalesRepository):
        self._repo = repo
        self.create_quotation = CreateQuotationUseCase(repo)
        self.approve_quotation = ApproveQuotationUseCase(repo)
        self.convert_quotation = ConvertQuotationUseCase(repo)
        self.create_order = CreateSalesOrderUseCase(repo)
        self.reserve = ReserveInventoryUseCase(repo)
        self.generate_shipment = GenerateShipmentUseCase(repo)
        self.generate_invoice = GenerateInvoiceUseCase(repo)
        self.cancel_order = CancelSalesOrderUseCase(repo)
        self.close_order = CloseSalesOrderUseCase(repo)

    # ── Quotations ────────────────────────────────────────────────
    def execute_create_quotation(self, cmd: CreateQuotation) -> dict:
        return self.create_quotation.execute(cmd)

    def execute_approve_quotation(self, cmd: ApproveQuotation) -> dict:
        return self.approve_quotation.execute(cmd)

    def execute_convert_quotation(self, cmd: ConvertQuotationToOrder):
        return self.convert_quotation.execute(cmd)

    # ── Sales Orders ──────────────────────────────────────────────
    def execute_create_order(self, cmd: CreateSalesOrder):
        return self.create_order.execute(cmd)

    def execute_reserve(self, cmd: ReserveInventory) -> dict:
        return self.reserve.execute(cmd)

    def execute_release(self, cmd: ReleaseInventory) -> dict:
        return self.reserve.execute(
            ReserveInventory(document_id=cmd.document_id, warehouse_id=cmd.warehouse_id)
        )

    def execute_generate_shipment(self, cmd: GenerateShipment):
        return self.generate_shipment.execute(cmd)

    def execute_generate_invoice(self, cmd: GenerateInvoice) -> dict:
        return self.generate_invoice.execute(cmd)

    def execute_cancel_order(self, cmd: CancelOrder):
        return self.cancel_order.execute(cmd)

    def execute_close_order(self, cmd: CloseOrder):
        return self.close_order.execute(cmd)

    # ── Legacy helpers (API convenience wrappers) ─────────────────
    def create_sales_order(self, **kwargs) -> 'SalesOrder':
        return self.create_order.execute(CreateSalesOrder(**kwargs))

    def approve_sales_order(self, document_id: str, **kwargs):
        so = self._repo.find_sales_order_by_document(document_id)
        if so:
            so.approve()
            self._repo.save_sales_order(so)
        clients.change_document_status(document_id, 'approved',
                                        comment='Aprovado',
                                        performed_by=kwargs.get('performed_by', ''))
        return so

    def reserve_for_order(self, document_id: str, warehouse_id: str = ''):
        return self.execute_reserve(ReserveInventory(
            document_id=document_id, warehouse_id=warehouse_id))

    def add_shipment_to_order(self, document_id: str, carrier: str = '',
                               origin_warehouse: str = '', notes: str = '',
                               created_by: str = ''):
        return self.execute_generate_shipment(GenerateShipment(
            document_id=document_id, carrier=carrier,
            origin_warehouse=origin_warehouse, notes=notes,
            created_by=created_by))

    def ship_order(self, document_id: str, tracking: str = '',
                   performed_by: str = ''):
        so = self._repo.find_sales_order_by_document(document_id)
        if so and so.shipments:
            so.shipments[-1].ship(tracking)
            so.status = __import__('modules.sales.core.domain.entities.sales_order',
                                    fromlist=['SalesOrderStatus']).SalesOrderStatus.SHIPPED
            so.updated_at = __import__('datetime').datetime.now()
            self._repo.save_sales_order(so)
        clients.change_document_status(document_id, 'shipped',
                                        comment=f'Shipped {tracking}',
                                        performed_by=performed_by)
        return so

    def invoice_order(self, document_id: str, fiscal: bool = False,
                      created_by: str = ''):
        return self.execute_generate_invoice(GenerateInvoice(
            document_id=document_id, fiscal=fiscal, created_by=created_by))

    def cancel_sales_order(self, document_id: str, performed_by: str = ''):
        return self.execute_cancel_order(CancelOrder(
            document_id=document_id, performed_by=performed_by))

    def add_line_to_order(self, document_id: str, line_data: dict):
        so = self._repo.find_sales_order_by_document(document_id)
        if not so:
            raise ValueError(f'SalesOrder for {document_id} not found')
        from modules.sales.core.domain.entities.sales_order import SalesOrderLine
        line = SalesOrderLine(**line_data)
        so.add_line(line)
        try:
            clients.add_document_line(document_id, line_data)
        except Exception:
            pass
        return self._repo.save_sales_order(so)

    def find_sales_order(self, so_id: str):
        return self._repo.find_sales_order_by_id(so_id)

    def find_sales_order_by_document(self, document_id: str):
        return self._repo.find_sales_order_by_document(document_id)

    # ── Opportunities ────────────────────────────────────────────
    def create_opportunity(self, title: str, customer_id: str,
                           customer_name: str = '', **kwargs) -> Opportunity:
        party = clients.get_party(customer_id)
        cust_name = customer_name or (party.get('name', '') if party else '')
        opp = Opportunity(title=title, customer_id=customer_id,
                          customer_name=cust_name, **kwargs)
        return self._repo.save_opportunity(opp)

    def close_opportunity(self, opp_id: str, result: str,
                          reason: str = '') -> Opportunity:
        opp = self._repo.find_opportunity_by_id(opp_id)
        if not opp:
            raise ValueError(f'Opportunity {opp_id} not found')
        if result == 'won':
            opp.win()
        else:
            opp.lose(reason)
        return self._repo.save_opportunity(opp)

    # ── Returns ──────────────────────────────────────────────────
    def create_return(self, document_id: str, document_number: str = '',
                      customer_id: str = '', items: list = None,
                      reason: str = '', sales_rep: str = '',
                      notes: str = '') -> ReturnRequest:
        rt = ReturnRequest(document_id=document_id,
                           document_number=document_number,
                           customer_id=customer_id, items=items or [],
                           reason=reason, sales_rep=sales_rep, notes=notes)
        return self._repo.save_return(rt)

    # ── Contracts ────────────────────────────────────────────────
    def create_contract(self, customer_id: str, customer_name: str = '',
                        title: str = '', start_date: str = '',
                        end_date: str = '', billing_cycle: str = 'monthly',
                        value: float = 0.0, items: list = None,
                        sales_rep: str = '') -> Contract:
        party = clients.get_party(customer_id)
        cust_name = customer_name or (party.get('name', '') if party else '')
        cont = Contract(customer_id=customer_id, customer_name=cust_name,
                        title=title, start_date=start_date, end_date=end_date,
                        billing_cycle=billing_cycle, value=value,
                        items=[ContractLine(**l) for l in (items or [])],
                        sales_rep=sales_rep)
        cont.activate()
        return self._repo.save_contract(cont)

    # ── Dashboard ────────────────────────────────────────────────
    def get_dashboard(self) -> dict:
        opps = self._repo.find_opportunities()
        pipelines = self._repo.find_all_pipelines()
        orders = self._repo.find_sales_orders()
        total_pipeline = sum(o.expected_value for o in opps if o.status.value in ('new', 'qualified', 'proposal', 'negotiation'))
        won = sum(o.expected_value for o in opps if o.status.value == 'won')
        by_stage = {}
        for o in opps:
            by_stage[o.stage or o.status.value] = by_stage.get(o.stage or o.status.value, 0) + 1
        return {
            'total_opportunities': len(opps),
            'pipeline_value': total_pipeline,
            'won_value': won,
            'won_count': sum(1 for o in opps if o.status.value == 'won'),
            'by_stage': by_stage,
            'pipelines': len(pipelines),
            'total_orders': len(orders),
            'orders_by_status': {s: sum(1 for o in orders if o.status.value == s) for s in set(o.status.value for o in orders)},
        }

    # ── Sales Experience ────────────────────────────────────────
    # Customer Last Orders
    def customer_last_orders(self, customer_id: str, limit: int = 10) -> list:
        return self._repo.find_sales_orders(customer_id=customer_id, limit=limit)

    # Order Duplicate
    def duplicate_order(self, document_id: str, customer_id: str = '',
                        customer_name: str = '', performed_by: str = '') -> 'SalesOrder':
        so = self._repo.find_sales_order_by_document(document_id)
        if not so:
            raise ValueError(f'SalesOrder for {document_id} not found')
        new_so = so.duplicate(customer_id, customer_name)
        new_so.created_by = performed_by
        doc_resp = clients.create_document(
            doc_type='sale_order', direction='out',
            lines=[{'item_id': l.item_id, 'item_name': l.item_name,
                    'quantity': l.quantity, 'unit_price': l.unit_price}
                   for l in so.lines],
            parties=[{'party_id': new_so.customer_id, 'party_type': 'customer',
                      'party_name': new_so.customer_name}],
            notes=f'Duplicado do pedido {so.document_number}',
            created_by=performed_by,
        )
        doc = doc_resp.get('data', doc_resp)
        new_so.document_id = doc.get('id', '')
        new_so.document_number = doc.get('number', '')
        self._add_timeline(new_so.document_id, 'created',
                           f'Pedido duplicado de {so.document_number}', performed_by)
        return self._repo.save_sales_order(new_so)

    # Quick Quote (minimal quotation)
    def quick_quote(self, customer_id: str, item_id: str, quantity: float = 1,
                    unit_price: float = 0, sales_rep: str = '',
                    customer_name: str = '') -> dict:
        party = clients.get_party(customer_id)
        cust_name = customer_name or (party.get('name', '') if party else '')
        if unit_price <= 0:
            from modules.sales.core.application.services.price_engine import PriceEngine
            unit_price = PriceEngine(self._repo).get_item_price(item_id)
        resp = clients.create_document(
            doc_type='quotation', direction='out',
            lines=[{'item_id': item_id, 'quantity': quantity,
                    'unit_price': unit_price}],
            parties=[{'party_id': customer_id, 'party_type': 'customer',
                      'party_name': cust_name}],
            created_by=sales_rep,
        )
        return resp.get('data', resp)

    # Order Templates
    def create_template(self, name: str, **kwargs) -> OrderTemplate:
        tpl = OrderTemplate(name=name, **kwargs)
        return self._repo.save_template(tpl)

    def apply_template(self, template_id: str, customer_id: str = '',
                       customer_name: str = '') -> dict:
        tpl = self._repo.find_template_by_id(template_id)
        if not tpl:
            raise ValueError(f'Template {template_id} not found')
        def _line_dict(l):
            if isinstance(l, dict):
                return l
            return {'item_id': l.item_id, 'item_name': l.item_name,
                    'item_code': l.item_code, 'quantity': l.quantity,
                    'unit': l.unit, 'unit_price': l.unit_price}
        return {
            'customer_id': customer_id or tpl.customer_id,
            'customer_name': customer_name or tpl.customer_name,
            'lines': [_line_dict(l) for l in (tpl.lines or [])],
            'payment_method': tpl.payment_terms,
            'installments': tpl.installments,
            'due_days': tpl.due_days,
            'notes': tpl.notes,
        }

    # Favorites
    def add_favorite(self, customer_id: str, item_id: str,
                     item_name: str = '', item_code: str = '') -> FavoriteItem:
        fav = FavoriteItem(customer_id=customer_id, item_id=item_id,
                           item_name=item_name, item_code=item_code)
        return self._repo.save_favorite(fav)

    def remove_favorite(self, favorite_id: str):
        self._repo.remove_favorite(favorite_id)

    def list_favorites(self, customer_id: str) -> list:
        return self._repo.find_favorites(customer_id)

    # Price History
    def record_price(self, item_id: str, price: float, **kwargs) -> PriceHistoryEntry:
        entry = PriceHistoryEntry(item_id=item_id, price=price, **kwargs)
        return self._repo.save_price_history(entry)

    def price_history(self, item_id: str, limit: int = 20) -> list:
        return self._repo.find_price_history(item_id, limit)

    # Timeline
    def _add_timeline(self, document_id: str, event_type: str,
                      description: str = '', performed_by: str = '',
                      old_value: str = '', new_value: str = ''):
        entry = TimelineEntry(
            document_id=document_id, event_type=event_type,
            description=description, performed_by=performed_by,
            old_value=old_value, new_value=new_value,
        )
        return self._repo.save_timeline_entry(entry)

    def get_timeline(self, document_id: str) -> list:
        return self._repo.find_timeline(document_id)

    # Sales Notes
    def add_note(self, document_id: str, content: str,
                 note_type: str = 'internal', created_by: str = '') -> SalesNote:
        note = SalesNote(document_id=document_id, content=content,
                         note_type=NoteType(note_type), created_by=created_by)
        self._add_timeline(document_id, 'note_added',
                           f'Nota {note_type} adicionada', created_by)
        return self._repo.save_note(note)

    def list_notes(self, document_id: str, note_type: str = '') -> list:
        return self._repo.find_notes(document_id, note_type)

    # Tags
    def create_tag(self, name: str, color: str = '#6b7280') -> SalesTag:
        tag = SalesTag(name=name, color=color)
        return self._repo.save_tag(tag)

    def list_tags(self) -> list:
        return self._repo.find_tags()

    # Team
    def add_team_member(self, rep_id: str, name: str, role: str = 'seller',
                        supervisor_id: str = '', email: str = '') -> SalesTeamMember:
        member = SalesTeamMember(rep_id=rep_id, name=name, role=role,
                                 supervisor_id=supervisor_id, email=email)
        return self._repo.save_team_member(member)

    def list_team(self, role: str = '') -> list:
        return self._repo.find_team_members(role)

    # Approval Matrix
    def add_approval_rule(self, name: str, min_value: float,
                          max_value: float = 0, approver_role: str = 'seller') -> ApprovalMatrixRule:
        rule = ApprovalMatrixRule(name=name, min_value=min_value,
                                  max_value=max_value, approver_role=approver_role)
        return self._repo.save_approval_rule(rule)

    def get_approver_for(self, order_value: float) -> str:
        return self._repo.find_approver_for_value(order_value)

    def list_approval_rules(self) -> list:
        return self._repo.find_approval_rules()
