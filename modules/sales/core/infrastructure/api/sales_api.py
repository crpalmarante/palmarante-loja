import uvicorn
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from modules.sales.core.infrastructure.postgres.sales_repository_memory import SalesRepositoryMemory
from modules.sales.core.application.services.sales_orchestrator import SalesOrchestrator
from modules.sales.core.domain.entities.price_list import PriceList, PriceListItem
from modules.sales.core.domain.entities.discount_rule import DiscountRule, DiscountType, DiscountScope, DiscountTier
from modules.sales.core.domain.entities.commission import CommissionRule, CommissionType
from modules.sales.core.domain.entities.opportunity import Pipeline, PipelineStage
from modules.sales.core.domain.entities.delivery import Delivery, DeliveryItem
from modules.sales.core.domain.entities.return_request import ReturnRequest, ReturnItem
from modules.sales.extensions.infrastructure.api.extensions_api import router as extensions_router
from modules.sales.core.application.services.clients import search_items, search_parties
from modules.notification.application.services.notification_client import (
    notify_order_created, notify_order_approved, notify_order_cancelled,
    notify_order_shipped, notify_quotation_created, notify_contract_created,
)

app = FastAPI(title='BusinessCore — Sales Platform', version='1.0.0')
app.include_router(extensions_router)
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

repo = SalesRepositoryMemory()
sales = SalesOrchestrator(repo)


def _seed():
    if not repo.find_all_pipelines():
        p = Pipeline(name='Vendas Diretas', stages=[
            'new', 'qualified', 'proposal', 'negotiation', 'won', 'lost',
        ])
        repo.save_pipeline(p)

    if not repo.find_all_price_lists():
        pl = PriceList(name='Tabela Padrão', code='STANDARD')
        pl.set_price('item-001', 4500.0, 4000.0)
        pl.set_price('item-002', 89.90, 75.0)
        pl.set_price('item-003', 0.45, 0.40)
        repo.save_price_list(pl)

    if not repo.find_active_discount_rules():
        repo.save_discount_rule(DiscountRule(
            name='Desconto 5% acima R$ 1.000',
            code='DISC_5P_1K',
            discount_type=DiscountType.PERCENTAGE,
            value=5.0, min_order_value=1000.0, priority=1,
        ))
        repo.save_discount_rule(DiscountRule(
            name='Desconto 10% acima R$ 5.000',
            code='DISC_10P_5K',
            discount_type=DiscountType.PERCENTAGE,
            value=10.0, min_order_value=5000.0, priority=2,
        ))

    if not repo.find_commission_rules():
        repo.save_commission_rule(CommissionRule(
            name='Comissão Padrão 3%',
            code='COMM_3P',
            commission_type=CommissionType.PERCENTAGE,
            rate=3.0,
        ))

    if not repo.find_opportunities():
        sales.create_opportunity(
            title='Venda de Notebooks', customer_id='cust-001',
            customer_name='Empresa ABC Ltda',
            expected_value=9000.0, probability=60,
            sales_rep='Carlos Silva', source='indicação',
        )
        sales.create_opportunity(
            title='Consultoria TI', customer_id='cust-002',
            customer_name='Cliente Potencial SA',
            expected_value=10000.0, probability=30,
            sales_rep='Ana Oliveira', source='site',
        )

    if not repo.find_contracts():
        sales.create_contract(
            customer_id='cust-001', customer_name='Empresa ABC Ltda',
            title='Contrato de Suporte Mensal',
            start_date='2026-01-01', end_date='2026-12-31',
            billing_cycle='monthly', value=12000.0,
            items=[{'item_id': 'srv-001', 'description': 'Suporte Técnico',
                    'quantity': 12, 'unit_price': 1000.0}],
            sales_rep='Carlos Silva',
        )


_seed()


# ── Dashboard ────────────────────────────────────────────────
@app.get('/api/sales/dashboard')
def dashboard():
    return {'data': sales.get_dashboard()}


# ── Opportunities (CRM) ──────────────────────────────────────
@app.get('/api/sales/opportunities')
def list_opportunities(customer_id: str = Query(''), status: str = Query(''),
                       sales_rep: str = Query('')):
    opps = repo.find_opportunities(customer_id, status, sales_rep)
    return {'data': [{'id': o._id, 'title': o.title, 'customer_id': o.customer_id,
                      'customer_name': o.customer_name, 'status': o.status.value,
                      'stage': o.stage, 'expected_value': o.expected_value,
                      'probability': o.probability, 'source': o.source,
                      'sales_rep': o.sales_rep, 'expected_close': o.expected_close,
                      'notes': o.notes,
                      'created_at': o.created_at.isoformat() if o.created_at else ''}
                     for o in opps]}


@app.post('/api/sales/opportunities')
def create_opportunity(body: dict):
    try:
        opp = sales.create_opportunity(
            title=body['title'], customer_id=body['customer_id'],
            customer_name=body.get('customer_name', ''),
            pipeline_id=body.get('pipeline_id', ''),
            expected_value=body.get('expected_value', 0.0),
            probability=body.get('probability', 10),
            notes=body.get('notes', ''), source=body.get('source', ''),
            sales_rep=body.get('sales_rep', ''),
            expected_close=body.get('expected_close', ''),
            items=body.get('items'),
        )
        return {'data': {'id': opp._id, 'title': opp.title, 'status': opp.status.value}}
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.post('/api/sales/opportunities/{opp_id}/close')
def close_opportunity(opp_id: str, body: dict):
    try:
        opp = sales.close_opportunity(opp_id, body.get('result', 'lost'),
                                       body.get('reason', ''))
        return {'data': {'id': opp._id, 'status': opp.status.value}}
    except ValueError as e:
        raise HTTPException(400, str(e))


# ── Pipelines ────────────────────────────────────────────────
@app.get('/api/sales/pipelines')
def list_pipelines():
    pipes = repo.find_all_pipelines()
    return {'data': [{'id': p._id, 'name': p.name, 'stages': p.stages, 'active': p.active}
                     for p in pipes]}


@app.post('/api/sales/pipelines')
def create_pipeline(body: dict):
    p = Pipeline(name=body['name'], stages=body.get('stages', []))
    repo.save_pipeline(p)
    return {'data': {'id': p._id, 'name': p.name}}


# ── Sales Orders (Aggregate) ──────────────────────────────────
def _so_to_dict(so):
    return {
        'id': so._id, 'document_id': so.document_id,
        'document_number': so.document_number, 'document_type': so.document_type,
        'customer_id': so.customer_id, 'customer_name': so.customer_name,
        'sales_rep': {'id': so.sales_rep.rep_id, 'name': so.sales_rep.name,
                      'commission_rate': so.sales_rep.commission_rate}
        if so.sales_rep else None,
        'payment_terms': {'method': so.payment_terms.method.value,
                          'installments': so.payment_terms.installments,
                          'due_days': so.payment_terms.due_days},
        'status': so.status.value,
        'subtotal': so.subtotal, 'discount_total': so.discount_total,
        'tax_total': so.tax_total, 'freight': so.freight,
        'total': so.total,
        'lines': [{'id': l._id, 'item_id': l.item_id, 'item_code': l.item_code,
                   'item_name': l.item_name, 'quantity': l.quantity,
                   'unit': l.unit, 'unit_price': l.unit_price,
                   'discount_pct': l.discount_pct, 'discount_value': l.discount_value,
                   'tax_value': l.tax_value, 'total': l.total}
                  for l in so.lines],
        'shipments': [{'id': s._id, 'carrier': s.carrier, 'tracking_code': s.tracking_code,
                       'status': s.status, 'items': len(s.items)}
                      for s in so.shipments],
        'commissions': [{'rep_id': c.rep_id, 'value': c.value, 'status': c.status}
                        for c in so.commissions],
        'installments': [{'number': i.number, 'due_date': i.due_date,
                          'value': i.value, 'status': i.status.value}
                         for i in so.installments],
        'notes': so.notes, 'opportunity_id': so.opportunity_id,
        'created_by': so.created_by,
        'created_at': so.created_at.isoformat() if so.created_at else '',
        'updated_at': so.updated_at.isoformat() if so.updated_at else '',
    }


@app.get('/api/sales/orders')
def list_orders(customer_id: str = Query(''), status: str = Query('')):
    orders = repo.find_sales_orders(customer_id, status)
    return {'data': [_so_to_dict(o) for o in orders]}


@app.get('/api/sales/orders/{so_id}')
def get_order(so_id: str):
    so = repo.find_sales_order_by_id(so_id)
    if not so:
        raise HTTPException(404, 'SalesOrder not found')
    return {'data': _so_to_dict(so)}


@app.post('/api/sales/orders')
def create_order(body: dict):
    try:
        so = sales.create_sales_order(
            customer_id=body['customer_id'],
            customer_name=body.get('customer_name', ''),
            items=body.get('items', []),
            price_list_id=body.get('price_list_id', ''),
            discount_rule_ids=body.get('discount_rule_ids'),
            sales_rep=body.get('sales_rep', ''),
            notes=body.get('notes', ''),
            opportunity_id=body.get('opportunity_id', ''),
            payment_method=body.get('payment_method', 'pix'),
            installments=body.get('installments', 1),
            due_days=body.get('due_days', 30),
            rep_commission_rate=body.get('rep_commission_rate', 0.0),
        )
        notify_order_created(so.document_number, so.customer_name,
                             so.sales_rep, so._id)
        return {'data': _so_to_dict(so)}
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(502, f'Document API error: {e}')


@app.post('/api/sales/orders/{doc_id}/approve')
def approve_order(doc_id: str, body: dict = None):
    try:
        so = sales.approve_sales_order(doc_id, performed_by=(body or {}).get('performed_by', ''))
        notify_order_approved(so.document_number, so.customer_name,
                              so._id, so.sales_rep)
        return {'data': _so_to_dict(so)}
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(502, str(e))


@app.post('/api/sales/orders/{doc_id}/cancel')
def cancel_order(doc_id: str, body: dict = None):
    try:
        so = sales.cancel_sales_order(doc_id, performed_by=(body or {}).get('performed_by', ''))
        notify_order_cancelled(so.document_number, so.customer_name,
                               so._id, so.sales_rep)
        return {'data': _so_to_dict(so)}
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.post('/api/sales/orders/{doc_id}/reserve')
def reserve_order(doc_id: str, body: dict = None):
    try:
        result = sales.reserve_for_order(doc_id, warehouse_id=(body or {}).get('warehouse_id', ''))
        return {'data': result}
    except Exception as e:
        raise HTTPException(502, str(e))


@app.post('/api/sales/orders/{doc_id}/ship')
def ship_order(doc_id: str, body: dict = None):
    try:
        so = sales.ship_order(doc_id, tracking=(body or {}).get('tracking', ''),
                               performed_by=(body or {}).get('performed_by', ''))
        notify_order_shipped(so.document_number, so.customer_name,
                             so._id, so.sales_rep)
        return {'data': _so_to_dict(so)}
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.post('/api/sales/orders/{doc_id}/invoice')
def invoice_order(doc_id: str, body: dict = None):
    try:
        inv = sales.invoice_order(doc_id, fiscal=(body or {}).get('fiscal', False),
                                   created_by=(body or {}).get('created_by', ''))
        return {'data': inv}
    except Exception as e:
        raise HTTPException(502, str(e))


@app.post('/api/sales/orders/{doc_id}/shipments')
def add_shipment(doc_id: str, body: dict = None):
    try:
        so = sales.add_shipment_to_order(
            doc_id, carrier=body.get('carrier', ''),
            origin_warehouse=body.get('origin_warehouse', ''),
            notes=body.get('notes', ''),
            created_by=body.get('created_by', ''),
        )
        return {'data': _so_to_dict(so)}
    except Exception as e:
        raise HTTPException(502, str(e))


@app.post('/api/sales/orders/{doc_id}/lines')
def add_order_line(doc_id: str, body: dict):
    try:
        so = sales.add_line_to_order(doc_id, body)
        return {'data': _so_to_dict(so)}
    except ValueError as e:
        raise HTTPException(400, str(e))


# ── Contracts ────────────────────────────────────────────────
@app.get('/api/sales/contracts')
def list_contracts(customer_id: str = Query(''), status: str = Query('')):
    contracts = repo.find_contracts(customer_id, status)
    return {'data': [{'id': c._id, 'contract_number': c.contract_number,
                      'title': c.title, 'customer_name': c.customer_name,
                      'status': c.status.value, 'value': c.value,
                      'start_date': c.start_date, 'end_date': c.end_date,
                      'billing_cycle': c.billing_cycle,
                      'created_at': c.created_at.isoformat() if c.created_at else ''}
                     for c in contracts]}


@app.post('/api/sales/contracts')
def create_contract(body: dict):
    try:
        c = sales.create_contract(
            customer_id=body['customer_id'],
            customer_name=body.get('customer_name', ''),
            title=body.get('title', ''),
            start_date=body.get('start_date', ''),
            end_date=body.get('end_date', ''),
            billing_cycle=body.get('billing_cycle', 'monthly'),
            value=body.get('value', 0.0),
            items=body.get('items'),
            sales_rep=body.get('sales_rep', ''),
        )
        notify_contract_created(c.title or c._id, c.customer_name,
                                c.sales_rep or 'user-001', c._id)
        return {'data': {'id': c._id, 'title': c.title, 'status': c.status.value}}
    except ValueError as e:
        raise HTTPException(400, str(e))


# ── Price Lists ──────────────────────────────────────────────
@app.get('/api/sales/price-lists')
def list_price_lists():
    pls = repo.find_all_price_lists()
    return {'data': [{'id': pl._id, 'name': pl.name, 'code': pl.code,
                      'items': len(pl.items), 'active': pl.active}
                     for pl in pls]}


@app.post('/api/sales/price-lists')
def create_price_list(body: dict):
    pl = PriceList(name=body['name'], code=body.get('code', ''))
    for item in body.get('items', []):
        pl.set_price(item.get('item_id', ''), item.get('price', 0), item.get('min_price', 0))
    repo.save_price_list(pl)
    return {'data': {'id': pl._id, 'name': pl.name}}


# ── Discount Rules ───────────────────────────────────────────
@app.get('/api/sales/discount-rules')
def list_discount_rules():
    rules = repo.find_active_discount_rules()
    return {'data': [{'id': r._id, 'name': r.name, 'code': r.code,
                      'type': r.discount_type.value, 'value': r.value,
                      'priority': r.priority, 'min_order_value': r.min_order_value}
                     for r in rules]}


@app.post('/api/sales/discount-rules')
def create_discount_rule(body: dict):
    tiers = [DiscountTier(**t) for t in body.get('tiers', [])]
    r = DiscountRule(
        name=body['name'], code=body.get('code', ''),
        discount_type=DiscountType(body.get('discount_type', 'percentage')),
        scope=DiscountScope(body.get('scope', 'global')),
        value=body.get('value', 0), tiers=tiers,
        item_ids=body.get('item_ids', []),
        customer_ids=body.get('customer_ids', []),
        min_order_value=body.get('min_order_value', 0),
        max_discount_value=body.get('max_discount_value', 0),
        priority=body.get('priority', 0),
    )
    repo.save_discount_rule(r)
    return {'data': {'id': r._id, 'name': r.name}}


# ── Commission Rules ─────────────────────────────────────────
@app.get('/api/sales/commission-rules')
def list_commission_rules():
    rules = repo.find_commission_rules()
    return {'data': [{'id': r._id, 'name': r.name, 'code': r.code,
                      'type': r.commission_type.value, 'rate': r.rate,
                      'active': r.active} for r in rules]}


@app.post('/api/sales/commission-rules')
def create_commission_rule(body: dict):
    r = CommissionRule(
        name=body['name'], code=body.get('code', ''),
        commission_type=CommissionType(body.get('commission_type', 'percentage')),
        rate=body.get('rate', 0), fixed_value=body.get('fixed_value', 0),
        sales_rep_ids=body.get('sales_rep_ids', []),
    )
    repo.save_commission_rule(r)
    return {'data': {'id': r._id, 'name': r.name}}


# ── Returns ──────────────────────────────────────────────────
@app.get('/api/sales/returns')
def list_returns(document_id: str = Query(''), status: str = Query('')):
    returns = repo.find_returns(document_id, status)
    return {'data': [{'id': r._id, 'document_id': r.document_id,
                      'document_number': r.document_number,
                      'status': r.status.value, 'reason': r.reason,
                      'created_at': r.created_at.isoformat() if r.created_at else ''}
                     for r in returns]}


@app.post('/api/sales/returns')
def create_return(body: dict):
    items = [ReturnItem(**l) for l in body.get('items', [])]
    rt = sales.create_return(
        document_id=body['document_id'],
        document_number=body.get('document_number', ''),
        customer_id=body.get('customer_id', ''),
        items=items, reason=body.get('reason', ''),
        sales_rep=body.get('sales_rep', ''),
        notes=body.get('notes', ''),
    )
    return {'data': {'id': rt._id, 'status': rt.status.value}}


# ── Quotations ───────────────────────────────────────────────
@app.post('/api/sales/quotations')
def create_quotation(body: dict):
    try:
        result = sales.execute_create_quotation(
            __import__('modules.sales.core.application.commands.sales_commands',
                       fromlist=['CreateQuotation']).CreateQuotation(
                customer_id=body.get('customer_id', ''),
                customer_name=body.get('customer_name', ''),
                lines=body.get('lines', []),
                notes=body.get('notes', ''),
                sales_rep=body.get('sales_rep', ''),
                opportunity_id=body.get('opportunity_id', ''),
                valid_until=body.get('valid_until', ''),
                payment_terms=body.get('payment_terms', ''),
                price_list_id=body.get('price_list_id', ''),
            )
        )
        doc_id = result.get('document_id', '')
        doc_number = result.get('document_number', '')
        notify_quotation_created(doc_number, body.get('customer_name', ''),
                                 body.get('sales_rep', 'user-001'), doc_id)
        return {'data': result}
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(502, f'Document API error: {e}')


# ── Sales Experience ─────────────────────────────────────────
# Customer Last Orders
@app.get('/api/sales/customers/{customer_id}/last-orders')
def customer_last_orders(customer_id: str, limit: int = Query(10)):
    orders = sales.customer_last_orders(customer_id, limit)
    return {'data': [_so_to_dict(o) for o in orders]}


# Order Duplicate
@app.post('/api/sales/orders/{doc_id}/duplicate')
def duplicate_order(doc_id: str, body: dict = None):
    try:
        so = sales.duplicate_order(
            doc_id,
            customer_id=(body or {}).get('customer_id', ''),
            customer_name=(body or {}).get('customer_name', ''),
            performed_by=(body or {}).get('performed_by', ''),
        )
        return {'data': _so_to_dict(so)}
    except ValueError as e:
        raise HTTPException(400, str(e))


# Quick Quote
@app.post('/api/sales/quick-quote')
def quick_quote(body: dict):
    try:
        result = sales.quick_quote(
            customer_id=body['customer_id'],
            item_id=body['item_id'],
            quantity=body.get('quantity', 1),
            unit_price=body.get('unit_price', 0),
            sales_rep=body.get('sales_rep', ''),
            customer_name=body.get('customer_name', ''),
        )
        return {'data': result}
    except Exception as e:
        raise HTTPException(502, str(e))


# Order Templates
@app.get('/api/sales/templates')
def list_templates(customer_id: str = Query('')):
    tpls = repo.find_templates(customer_id)
    return {'data': [{'id': t._id, 'name': t.name, 'customer_name': t.customer_name,
                      'lines': len(t.lines or []), 'created_at': t.created_at.isoformat() if t.created_at else ''}
                     for t in tpls]}


@app.post('/api/sales/templates')
def create_template(body: dict):
    tpl = sales.create_template(
        name=body['name'],
        customer_id=body.get('customer_id', ''),
        customer_name=body.get('customer_name', ''),
        lines=[__import__('modules.sales.core.domain.entities.order_template',
                         fromlist=['OrderTemplateLine']).OrderTemplateLine(**l)
               for l in body.get('lines', [])],
        payment_terms=body.get('payment_terms', 'pix'),
        installments=body.get('installments', 1),
        due_days=body.get('due_days', 30),
        notes=body.get('notes', ''),
        sales_rep=body.get('sales_rep', ''),
    )
    return {'data': {'id': tpl._id, 'name': tpl.name}}


@app.post('/api/sales/templates/{template_id}/apply')
def apply_template(template_id: str, body: dict = None):
    try:
        result = sales.apply_template(
            template_id,
            customer_id=(body or {}).get('customer_id', ''),
            customer_name=(body or {}).get('customer_name', ''),
        )
        return {'data': result}
    except ValueError as e:
        raise HTTPException(400, str(e))


# Favorites
@app.get('/api/sales/customers/{customer_id}/favorites')
def list_favorites(customer_id: str):
    favs = sales.list_favorites(customer_id)
    return {'data': [{'id': f._id, 'item_id': f.item_id, 'item_name': f.item_name,
                      'item_code': f.item_code}
                     for f in favs]}


@app.post('/api/sales/favorites')
def add_favorite(body: dict):
    fav = sales.add_favorite(
        customer_id=body['customer_id'],
        item_id=body['item_id'],
        item_name=body.get('item_name', ''),
        item_code=body.get('item_code', ''),
    )
    return {'data': {'id': fav._id, 'item_id': fav.item_id}}


@app.delete('/api/sales/favorites/{favorite_id}')
def remove_favorite(favorite_id: str):
    sales.remove_favorite(favorite_id)
    return {'data': {'removed': favorite_id}}


# Price History
@app.post('/api/sales/price-history')
def record_price(body: dict):
    entry = sales.record_price(
        item_id=body['item_id'],
        price=body['price'],
        price_list_id=body.get('price_list_id', ''),
        price_list_name=body.get('price_list_name', ''),
        recorded_by=body.get('recorded_by', ''),
        source=body.get('source', 'manual'),
    )
    return {'data': {'id': entry._id, 'item_id': entry.item_id, 'price': entry.price}}


@app.get('/api/sales/price-history/{item_id}')
def get_price_history(item_id: str, limit: int = Query(20)):
    history = sales.price_history(item_id, limit)
    return {'data': [{'id': e._id, 'price': e.price, 'source': e.source,
                      'recorded_by': e.recorded_by,
                      'created_at': e.created_at.isoformat() if e.created_at else ''}
                     for e in history]}


# Timeline
@app.get('/api/sales/orders/{doc_id}/timeline')
def get_timeline(doc_id: str):
    entries = sales.get_timeline(doc_id)
    return {'data': [{'id': e._id, 'event_type': e.event_type, 'description': e.description,
                      'performed_by': e.performed_by, 'old_value': e.old_value,
                      'new_value': e.new_value,
                      'created_at': e.created_at.isoformat() if e.created_at else ''}
                     for e in entries]}


# Sales Notes
@app.get('/api/sales/orders/{doc_id}/notes')
def list_notes(doc_id: str, note_type: str = Query('')):
    notes = sales.list_notes(doc_id, note_type)
    return {'data': [{'id': n._id, 'note_type': n.note_type.value, 'content': n.content,
                      'created_by': n.created_by,
                      'created_at': n.created_at.isoformat() if n.created_at else ''}
                     for n in notes]}


@app.post('/api/sales/notes')
def add_note(body: dict):
    note = sales.add_note(
        document_id=body['document_id'],
        content=body['content'],
        note_type=body.get('note_type', 'internal'),
        created_by=body.get('created_by', ''),
    )
    return {'data': {'id': note._id, 'note_type': note.note_type.value}}


# Tags
@app.get('/api/sales/tags')
def list_tags():
    tags = sales.list_tags()
    return {'data': [{'id': t._id, 'name': t.name, 'color': t.color} for t in tags]}


@app.post('/api/sales/tags')
def create_tag(body: dict):
    tag = sales.create_tag(name=body['name'], color=body.get('color', '#6b7280'))
    return {'data': {'id': tag._id, 'name': tag.name}}


# Sales Team
@app.get('/api/sales/team')
def list_team(role: str = Query('')):
    members = sales.list_team(role)
    return {'data': [{'id': m._id, 'rep_id': m.rep_id, 'name': m.name,
                      'role': m.role, 'supervisor_id': m.supervisor_id,
                      'active': m.active} for m in members]}


@app.post('/api/sales/team')
def add_team_member(body: dict):
    member = sales.add_team_member(
        rep_id=body['rep_id'],
        name=body['name'],
        role=body.get('role', 'seller'),
        supervisor_id=body.get('supervisor_id', ''),
        email=body.get('email', ''),
    )
    return {'data': {'id': member._id, 'name': member.name, 'role': member.role}}


# Approval Matrix
@app.get('/api/sales/approval-rules')
def list_approval_rules():
    rules = sales.list_approval_rules()
    return {'data': [{'id': r._id, 'name': r.name, 'min_value': r.min_value,
                      'max_value': r.max_value, 'approver_role': r.approver_role,
                      'active': r.active} for r in rules]}


@app.post('/api/sales/approval-rules')
def add_approval_rule(body: dict):
    rule = sales.add_approval_rule(
        name=body['name'],
        min_value=body.get('min_value', 0),
        max_value=body.get('max_value', 0),
        approver_role=body.get('approver_role', 'seller'),
    )
    return {'data': {'id': rule._id, 'name': rule.name}}


@app.get('/api/sales/approver-for/{order_value}')
def get_approver_for(order_value: float):
    role = sales.get_approver_for(order_value)
    return {'data': {'order_value': order_value, 'approver_role': role}}


# ── Smart Search Aggregator ─────────────────────────────────
@app.get('/api/search')
def smart_search(q: str = Query(''), limit: int = Query(5)):
    from modules.sales.extensions.application.services.extended_services import SearchService
    svc = SearchService(repo)
    sales_results = svc.search(q, limit)
    items = search_items(q, limit)
    parties = search_parties(q, limit)
    return {
        'data': {
            'orders': sales_results.get('orders', []),
            'customers': sales_results.get('customers', []),
            'products': sales_results.get('products', []) + [
                {'id': i.get('id') or i.get('item_id'), 'title': i.get('name', ''),
                 'code': i.get('code', '')}
                for i in (items if isinstance(items, list) else [])
            ],
            'quotations': sales_results.get('quotations', []),
            'contracts': sales_results.get('contracts', []),
            'purchase_orders': [],
            'suppliers': [
                {'id': p.get('id'), 'title': p.get('name', ''),
                 'email': p.get('email', ''),
                 'status': p.get('status', '')}
                for p in (parties if isinstance(parties, list) else [])
            ],
        }
    }


if __name__ == '__main__':
    _seed()
    uvicorn.run(app, host='0.0.0.0', port=8008)
