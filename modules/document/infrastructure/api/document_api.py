import uvicorn
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from modules.document.infrastructure.postgres.document_repository_postgres import DocumentRepositoryMemory
from modules.document.application.services.document_engine import DocumentEngine
from modules.document.domain.entities.business_document import BusinessDocument
from modules.document.domain.entities.document_definition import DocumentDefinition, DocumentFieldDef, DocumentLineFieldDef
from modules.document.domain.entities.document_numbering import DocumentNumbering

app = FastAPI(title='BusinessCore — Document Platform', version='1.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

repo = DocumentRepositoryMemory()
engine = DocumentEngine(repo)

# ── Seed sample data at startup ──────────────────────────────
from modules.document.domain.entities.document_definition import DocumentFieldDef, DocumentLineFieldDef, FieldType
from modules.document.domain.entities.document_numbering import DocumentNumbering

def _seed():
    defs = [
        DocumentDefinition(name='Pedido de Venda', code='sale_order', direction='out', behaviors=['inventory', 'financial'], party_types=['customer', 'carrier']),
        DocumentDefinition(name='Pedido de Compra', code='purchase_order', direction='in', behaviors=['inventory', 'financial'], party_types=['supplier']),
        DocumentDefinition(name='Orçamento', code='quotation', direction='out', behaviors=['financial'], party_types=['customer']),
        DocumentDefinition(name='Nota Fiscal', code='invoice', direction='out', behaviors=['inventory', 'financial', 'fiscal'], party_types=['customer']),
        DocumentDefinition(name='Ordem de Produção', code='production_order', direction='internal', behaviors=['inventory'], has_parties=False, party_types=[]),
        DocumentDefinition(name='Ordem de Serviço', code='service_order', direction='out', behaviors=['financial'], party_types=['customer', 'technician']),
    ]
    for d in defs:
        if not repo.find_definition_by_code(d.code):
            repo.save_definition(d)

    rules = [
        ('sale_order', 'V{year}{month}{seq:06d}'),
        ('purchase_order', 'PC{year}{month}{seq:06d}'),
        ('quotation', 'ORC{year}{month}{seq:06d}'),
        ('invoice', 'NF{year}{month}{seq:09d}'),
        ('production_order', 'OP{year}{month}{seq:06d}'),
        ('service_order', 'OS{year}{month}{seq:06d}'),
    ]
    for dt, pat in rules:
        if not repo.find_numbering(dt):
            repo.save_numbering(DocumentNumbering(document_type=dt, pattern=pat))

    if not repo.find_documents():
        for s in [
            {'doc_type': 'sale_order', 'lines': [{'item_name': 'Notebook Dell', 'quantity': 2, 'unit_price': 4500.0}], 'parties': [{'party_id': 'cust-001', 'party_type': 'customer', 'party_name': 'Empresa ABC'}], 'notes': 'Urgente'},
            {'doc_type': 'purchase_order', 'lines': [{'item_name': 'Parafuso M8', 'quantity': 1000, 'unit_price': 0.45}], 'parties': [{'party_id': 'sup-001', 'party_type': 'supplier', 'party_name': 'Fornecedora XYZ'}], 'notes': 'Entregar no almoxarifado'},
            {'doc_type': 'quotation', 'lines': [{'item_name': 'Consultoria', 'quantity': 40, 'unit_price': 250.0}], 'parties': [{'party_id': 'cust-002', 'party_type': 'customer', 'party_name': 'Cliente Potencial SA'}], 'notes': 'Válido 30 dias'},
        ]:
            try:
                engine.create_document(doc_type=s['doc_type'], lines=s.get('lines',[]), parties=s.get('parties',[]), notes=s.get('notes',''), created_by='seed')
            except Exception as e:
                print(f'Seed doc error: {e}')

_seed()

# ── Document Definitions (DDX Engine) ────────────────────────
@app.get('/api/document-definitions')
def list_definitions():
    defs = repo.find_all_definitions()
    return {'data': [{'id': d._id, 'name': d.name, 'code': d.code,
                      'direction': d.direction, 'has_lines': d.has_lines,
                      'has_parties': d.has_parties, 'has_workflow': d.has_workflow,
                      'active': d.active, 'behaviors': d.behaviors,
                      'header_fields': len(d.header_fields), 'line_fields': len(d.line_fields),
                      'created_at': d.created_at.isoformat() if d.created_at else ''} for d in defs]}


@app.post('/api/document-definitions')
def create_definition(body: dict):
    try:
        defn = engine.register_definition(
            name=body['name'], code=body['code'],
            description=body.get('description', ''),
            direction=body.get('direction', 'out'),
            has_lines=body.get('has_lines', True),
            has_parties=body.get('has_parties', True),
            has_totals=body.get('has_totals', True),
            has_workflow=body.get('has_workflow', False),
            workflow_code=body.get('workflow_code', ''),
            header_fields=[DocumentFieldDef(**f) for f in body.get('header_fields', [])],
            line_fields=[DocumentLineFieldDef(**f) for f in body.get('line_fields', [])],
            party_types=body.get('party_types', ['customer', 'supplier']),
            behaviors=body.get('behaviors', []),
        )
        return {'data': {'id': defn._id, 'name': defn.name, 'code': defn.code}}
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.get('/api/document-definitions/{def_id}')
def get_definition(def_id: str):
    d = repo.find_definition_by_id(def_id)
    if not d:
        raise HTTPException(404, 'Definition not found')
    return {'data': {
        'id': d._id, 'name': d.name, 'code': d.code,
        'description': d.description, 'direction': d.direction,
        'has_lines': d.has_lines, 'has_parties': d.has_parties,
        'has_totals': d.has_totals, 'has_workflow': d.has_workflow,
        'workflow_code': d.workflow_code, 'active': d.active,
        'behaviors': d.behaviors,
        'header_fields': [{'name': f.name, 'code': f.code, 'field_type': f.field_type.value if hasattr(f.field_type, 'value') else f.field_type, 'required': f.required, 'default_value': f.default_value, 'sort_order': f.sort_order} for f in d.header_fields],
        'line_fields': [{'name': f.name, 'code': f.code, 'field_type': f.field_type.value if hasattr(f.field_type, 'value') else f.field_type, 'required': f.required, 'sort_order': f.sort_order} for f in d.line_fields],
        'party_types': d.party_types,
        'created_at': d.created_at.isoformat() if d.created_at else '',
    }}


# ── Document Numbering ───────────────────────────────────────
@app.get('/api/document-numbering')
def list_numbering():
    nums = repo.find_all_numbering()
    return {'data': [{'id': n._id, 'document_type': n.document_type,
                      'pattern': n.pattern, 'series': n.series,
                      'next_number': n.next_number} for n in nums]}


@app.post('/api/document-numbering')
def create_numbering(body: dict):
    try:
        num = engine.setup_numbering(
            body['document_type'],
            pattern=body.get('pattern', '{year}{month}{seq:06d}'),
            prefix=body.get('prefix', ''), suffix=body.get('suffix', ''),
            digits=body.get('digits', 6), series=body.get('series', '1'),
            next_number=body.get('next_number', 1))
        return {'data': {'id': num._id, 'document_type': num.document_type,
                         'pattern': num.pattern, 'series': num.series}}
    except ValueError as e:
        raise HTTPException(400, str(e))


# ── Business Documents ───────────────────────────────────────
@app.get('/api/documents/dashboard')
def dashboard():
    return {'data': engine.get_dashboard()}


@app.get('/api/documents')
def list_documents(document_type: str = Query(''), status: str = Query(''),
                   party_id: str = Query(''), query: str = Query(''),
                   limit: int = Query(100)):
    docs = repo.find_documents(document_type, status, party_id, query, limit)
    return {'data': [{'id': d._id, 'document_type': d.document_type,
                      'number': d.number, 'status': d.status.value,
                      'direction': d.direction,
                      'party': d.parties[0].party_name if d.parties else '',
                      'party_type': d.parties[0].party_type if d.parties else '',
                      'lines': len(d.lines),
                      'total': float(d.total),
                      'created_at': d.created_at.isoformat() if d.created_at else '',
                      'created_by': d.created_by} for d in docs]}


@app.post('/api/documents')
def create_document(body: dict):
    try:
        doc = engine.create_document(
            doc_type=body['document_type'],
            number=body.get('number', ''),
            organization_id=body.get('organization_id', ''),
            branch_id=body.get('branch_id', ''),
            direction=body.get('direction', 'out'),
            header=body.get('header', {}),
            lines=body.get('lines', []),
            parties=body.get('parties', []),
            references=body.get('references', []),
            notes=body.get('notes', ''),
            created_by=body.get('created_by', ''),
        )
        return {'data': {'id': doc._id, 'number': doc.number, 'status': doc.status.value}}
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.get('/api/documents/{doc_id}')
def get_document(doc_id: str):
    d = repo.find_document_by_id(doc_id)
    if not d:
        raise HTTPException(404, 'Document not found')
    return {'data': {
        'id': d._id, 'document_type': d.document_type, 'number': d.number,
        'status': d.status.value, 'organization_id': d.organization_id,
        'branch_id': d.branch_id, 'direction': d.direction,
        'subtotal': float(d.subtotal), 'discount_total': float(d.discount_total),
        'freight': float(d.freight), 'insurance': float(d.insurance),
        'tax_total': float(d.tax_total), 'other_costs': float(d.other_costs),
        'total': float(d.total), 'workflow_instance_id': d.workflow_instance_id,
        'header': {
            'number': d.header.number, 'date': d.header.date.isoformat() if d.header.date else '',
            'currency': d.header.currency, 'notes': d.header.notes,
            'responsible': d.header.responsible, 'department': d.header.department,
            'cost_center': d.header.cost_center, 'custom_fields': d.header.custom_fields,
        },
        'lines': [{'id': l._id, 'item_id': l.item_id, 'item_code': l.item_code,
                   'item_name': l.item_name, 'quantity': float(l.quantity),
                   'unit': l.unit, 'unit_price': float(l.unit_price),
                   'discount_pct': float(l.discount_pct), 'discount_value': float(l.discount_value),
                   'tax_value': float(l.tax_value), 'total': float(l.total),
                   'subtotal': float(l.subtotal), 'net_total': float(l.net_total),
                   'notes': l.notes, 'sort_order': l.sort_order} for l in d.lines],
        'parties': [{'id': p._id, 'party_id': p.party_id, 'party_type': p.party_type,
                     'party_name': p.party_name} for p in d.parties],
        'references': [{'id': r._id, 'reference_type': r.reference_type,
                        'reference_id': r.reference_id, 'reference_number': r.reference_number} for r in d.references],
        'history': [{'id': h._id, 'action': h.action, 'from_status': h.from_status,
                     'to_status': h.to_status, 'comment': h.comment,
                     'performed_by': h.performed_by,
                     'created_at': h.created_at.isoformat() if h.created_at else ''} for h in d.history],
        'created_by': d.created_by,
        'created_at': d.created_at.isoformat() if d.created_at else '',
        'updated_at': d.updated_at.isoformat() if d.updated_at else '',
    }}


@app.put('/api/documents/{doc_id}')
def update_document(doc_id: str, body: dict):
    d = repo.find_document_by_id(doc_id)
    if not d:
        raise HTTPException(404, 'Document not found')
    if 'header' in body:
        for k, v in body['header'].items():
            if hasattr(d.header, k):
                setattr(d.header, k, v)
    if 'notes' in body:
        d.header.notes = body['notes']
    if 'direction' in body:
        d.direction = body['direction']
    if 'lines' in body:
        d.lines = []
        for l in body['lines']:
            from modules.document.domain.entities.business_document import DocumentLine
            d.add_line(DocumentLine(**l))
    d.updated_at = __import__('datetime').datetime.now()
    return {'data': {'id': d._id, 'status': d.status.value}}


@app.delete('/api/documents/{doc_id}')
def delete_document(doc_id: str):
    d = repo.find_document_by_id(doc_id)
    if not d:
        raise HTTPException(404, 'Document not found')
    repo.delete_document(doc_id)
    return {'data': {'deleted': doc_id}}


# ── Document Status ──────────────────────────────────────────
@app.post('/api/documents/{doc_id}/status')
def change_status(doc_id: str, body: dict):
    try:
        doc = engine.change_status(doc_id, body['status'],
                                    comment=body.get('comment', ''),
                                    performed_by=body.get('performed_by', ''))
        return {'data': {'id': doc._id, 'status': doc.status.value}}
    except ValueError as e:
        raise HTTPException(400, str(e))


# ── Document Lines ───────────────────────────────────────────
@app.post('/api/documents/{doc_id}/lines')
def add_line(doc_id: str, body: dict):
    try:
        doc = engine.add_line(doc_id, body)
        return {'data': {'id': doc._id, 'lines': len(doc.lines)}}
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.delete('/api/documents/{doc_id}/lines/{line_id}')
def remove_line(doc_id: str, line_id: str):
    try:
        doc = engine.remove_line(doc_id, line_id)
        return {'data': {'id': doc._id, 'lines': len(doc.lines)}}
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.get('/api/documents/reference/{reference_type}/{reference_id}')
def by_reference(reference_type: str, reference_id: str):
    docs = repo.find_documents_by_reference(reference_type, reference_id)
    return {'data': [{'id': d._id, 'document_type': d.document_type,
                      'number': d.number, 'status': d.status.value,
                      'total': float(d.total)} for d in docs]}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8007)
