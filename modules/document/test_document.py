import sys
sys.path.insert(0, '/home/palmarante/projetos_cobol/palmarante-loja')

import pytest
from modules.document.infrastructure.postgres.document_repository_postgres import DocumentRepositoryMemory
from modules.document.application.services.document_engine import DocumentEngine
from modules.document.domain.entities.business_document import BusinessDocument, DocumentLine, DocumentParty, DocumentReference
from modules.document.domain.entities.document_definition import DocumentDefinition, DocumentFieldDef, DocumentLineFieldDef, FieldType
from modules.document.domain.entities.document_numbering import DocumentNumbering
from modules.document.domain.value_objects.document_status import DocumentStatus


@pytest.fixture
def repo():
    return DocumentRepositoryMemory()


@pytest.fixture
def engine(repo):
    return DocumentEngine(repo)


@pytest.fixture
def sale_def(repo):
    d = DocumentDefinition(
        name='Pedido de Venda', code='sale_order',
        direction='out', has_lines=True, has_parties=True,
        has_totals=True, has_workflow=False,
        behaviors=['inventory', 'financial'],
        party_types=['customer'],
    )
    return repo.save_definition(d)


@pytest.fixture
def sale_numbering(repo):
    n = DocumentNumbering(document_type='sale_order', pattern='V{year}{month}{seq:06d}', next_number=1)
    return repo.save_numbering(n)


# ── Document Definitions ─────────────────────────────────────

def test_create_definition(engine):
    d = engine.register_definition('Pedido de Venda', 'sale_order', direction='out')
    assert d.name == 'Pedido de Venda'
    assert d.code == 'sale_order'
    assert d.direction == 'out'
    assert d.has_lines is True
    assert d._id != ''


def test_create_definition_duplicate(engine):
    engine.register_definition('Test', 'test_dup')
    with pytest.raises(ValueError, match='already exists'):
        engine.register_definition('Test2', 'test_dup')


def test_find_definition_by_code(repo, sale_def):
    d = repo.find_definition_by_code('sale_order')
    assert d is not None
    assert d.name == 'Pedido de Venda'


def test_find_definition_by_id(repo, sale_def):
    d = repo.find_definition_by_id(sale_def._id)
    assert d is not None
    assert d.code == 'sale_order'


def test_list_definitions(repo, sale_def):
    d2 = repo.save_definition(DocumentDefinition(name='Compra', code='purchase_order'))
    defs = repo.find_all_definitions()
    assert len(defs) == 2


def test_definition_with_fields(repo):
    d = repo.save_definition(DocumentDefinition(
        name='NF-e', code='nfe', direction='out',
        header_fields=[
            DocumentFieldDef(name='Chave Acesso', code='access_key', field_type=FieldType.TEXT, required=True),
            DocumentFieldDef(name='Natureza', code='nature', field_type=FieldType.TEXT),
        ],
        line_fields=[
            DocumentLineFieldDef(name='NCM', code='ncm', required=True),
        ],
        behaviors=['fiscal'],
    ))
    assert len(d.header_fields) == 2
    assert len(d.line_fields) == 1
    assert d.header_fields[0].code == 'access_key'
    assert d.behaviors == ['fiscal']


# ── Document Numbering ───────────────────────────────────────

def test_numbering_default_pattern(engine):
    n = engine.setup_numbering('test_doc')
    assert n.document_type == 'test_doc'
    assert n.pattern == '{year}{month}{seq:06d}'


def test_numbering_generation(engine):
    n = engine.setup_numbering('invoice', pattern='NF{year}{month}{seq:04d}', digits=4, next_number=1)
    num = n.generate_number()
    assert num.startswith('NF')
    import re
    assert re.match(r'NF\d{6}\d{4}', num)  # year(4) + month(2) = 6 digits + 4 seq digits
    assert n.next_number == 1  # hasn't advanced yet
    n.advance()
    assert n.next_number == 2


def test_numbering_custom_pattern(engine):
    n = engine.setup_numbering('sale', pattern='V{series}-{year}{month}{seq:05d}',
                                series='A', next_number=100, digits=5)
    num = n.generate_number()
    assert num.startswith('VA-')
    assert num.endswith('00100')


def test_numbering_advancement(engine):
    n = engine.setup_numbering('prod', next_number=50, digits=3)
    n.advance()
    assert n.next_number == 51
    num = n.generate_number()
    assert num.endswith('051')


def test_find_numbering_by_type(repo, sale_numbering):
    n = repo.find_numbering('sale_order')
    assert n is not None
    assert n.pattern == 'V{year}{month}{seq:06d}'


def test_find_numbering_with_series(repo):
    repo.save_numbering(DocumentNumbering(document_type='sale', series='1'))
    repo.save_numbering(DocumentNumbering(document_type='sale', series='2'))
    n = repo.find_numbering('sale', series='2')
    assert n.series == '2'


# ── BusinessDocument Core ────────────────────────────────────

def test_create_document(engine, sale_def, sale_numbering):
    doc = engine.create_document(
        doc_type='sale_order',
        organization_id='org-001',
        branch_id='branch-001',
        created_by='admin',
    )
    assert doc.document_type == 'sale_order'
    assert doc.status == DocumentStatus.DRAFT
    assert doc.number.startswith('V')
    assert doc.organization_id == 'org-001'
    assert doc.created_by == 'admin'
    assert doc._id != ''
    assert len(doc.history) == 1
    assert doc.history[0].action == 'created'


def test_create_document_with_lines(engine, sale_def, sale_numbering):
    doc = engine.create_document(
        doc_type='sale_order',
        lines=[
            {'item_id': 'item-001', 'item_name': 'Produto A', 'quantity': 2, 'unit_price': 100.0},
            {'item_id': 'item-002', 'item_name': 'Produto B', 'quantity': 1, 'unit_price': 50.0},
        ],
        parties=[{'party_id': 'cust-001', 'party_type': 'customer', 'party_name': 'Cliente A'}],
        created_by='admin',
    )
    assert len(doc.lines) == 2
    assert len(doc.parties) == 1
    assert doc.parties[0].party_id == 'cust-001'
    assert doc.subtotal == 250.0
    assert doc.total == 250.0


def test_document_totals_calculation(engine, sale_def, sale_numbering):
    doc = engine.create_document(
        doc_type='sale_order',
        lines=[
            {'item_id': 'item-001', 'quantity': 2, 'unit_price': 100.0, 'discount_pct': 10, 'tax_value': 20.0},
        ],
        freight=15.0,
        insurance=5.0,
        other_costs=10.0,
    )
    assert doc.subtotal == 200.0
    assert doc.discount_total == 0.0  # discount_value was not set, only pct
    # total = subtotal - discount + freight + insurance + tax + other
    #   = 200 - 0 + 15 + 5 + 20 + 10 = 250
    assert doc.total == 250.0


def test_add_line_to_document(engine, sale_def, sale_numbering):
    doc = engine.create_document(doc_type='sale_order', created_by='admin')
    doc = engine.add_line(doc._id, {'item_id': 'item-001', 'quantity': 3, 'unit_price': 75.0})
    assert len(doc.lines) == 1
    assert doc.lines[0].subtotal == 225.0


def test_remove_line_from_document(engine, sale_def, sale_numbering):
    doc = engine.create_document(
        doc_type='sale_order',
        lines=[
            {'item_id': 'item-001', 'quantity': 1, 'unit_price': 50.0},
            {'item_id': 'item-002', 'quantity': 2, 'unit_price': 30.0},
        ],
    )
    assert len(doc.lines) == 2
    line_id = doc.lines[0]._id
    doc = engine.remove_line(doc._id, line_id)
    assert len(doc.lines) == 1
    assert doc.subtotal == 60.0


def test_change_status(engine, sale_def, sale_numbering):
    doc = engine.create_document(doc_type='sale_order')
    doc = engine.change_status(doc._id, 'approved', comment='Ok', performed_by='admin')
    assert doc.status == DocumentStatus.APPROVED
    assert len(doc.history) == 2
    assert doc.history[1].action == 'status_change'
    assert doc.history[1].from_status == 'draft'
    assert doc.history[1].to_status == 'approved'


def test_add_reference_to_document(engine, sale_def, sale_numbering):
    doc = engine.create_document(doc_type='sale_order')
    doc.add_reference(DocumentReference(
        document_id=doc._id, reference_type='invoice', reference_id='inv-001', reference_number='NF-001'
    ))
    updated = engine._repo.save_document(doc)
    assert len(updated.references) == 1
    assert updated.references[0].reference_id == 'inv-001'


def test_find_document_by_id(engine, sale_def, sale_numbering):
    doc = engine.create_document(doc_type='sale_order')
    found = engine._repo.find_document_by_id(doc._id)
    assert found is not None
    assert found._id == doc._id


def test_list_documents(engine, sale_def, sale_numbering):
    engine.create_document(doc_type='sale_order')
    engine.create_document(doc_type='sale_order')
    docs = engine._repo.find_documents()
    assert len(docs) >= 2


def test_filter_documents_by_type(engine, sale_def, sale_numbering):
    d2 = engine._repo.save_definition(DocumentDefinition(name='Compra', code='purchase_order'))
    n2 = engine._repo.save_numbering(DocumentNumbering(document_type='purchase_order', next_number=1))
    engine.create_document(doc_type='sale_order')
    engine.create_document(doc_type='purchase_order')
    sales = engine._repo.find_documents(document_type='sale_order')
    purchases = engine._repo.find_documents(document_type='purchase_order')
    assert len(sales) >= 1
    assert len(purchases) >= 1


def test_filter_by_status(engine, sale_def, sale_numbering):
    doc = engine.create_document(doc_type='sale_order')
    engine.change_status(doc._id, 'completed')
    docs = engine._repo.find_documents(status='completed')
    assert len(docs) >= 1
    assert docs[0].status == DocumentStatus.COMPLETED


def test_find_by_reference(engine, sale_def, sale_numbering):
    doc = engine.create_document(doc_type='sale_order')
    doc.add_reference(DocumentReference(
        document_id=doc._id, reference_type='order', reference_id='ord-001'
    ))
    engine._repo.save_document(doc)
    found = engine._repo.find_documents_by_reference('order', 'ord-001')
    assert len(found) >= 1
    assert found[0]._id == doc._id


def test_delete_document(engine, sale_def, sale_numbering):
    doc = engine.create_document(doc_type='sale_order')
    doc_id = doc._id
    engine._repo.delete_document(doc_id)
    assert engine._repo.find_document_by_id(doc_id) is None


def test_document_history_trail(engine, sale_def, sale_numbering):
    doc = engine.create_document(doc_type='sale_order')
    doc.change_status(DocumentStatus.APPROVED, performed_by='admin')
    doc.change_status(DocumentStatus.COMPLETED, performed_by='admin')
    assert len(doc.history) >= 3
    actions = [h.action for h in doc.history]
    assert 'created' in actions
    assert actions.count('status_change') >= 2


def test_document_with_multiple_parties(engine, sale_def, sale_numbering):
    doc = engine.create_document(
        doc_type='sale_order',
        parties=[
            {'party_id': 'cust-001', 'party_type': 'customer', 'party_name': 'Cliente'},
            {'party_id': 'car-001', 'party_type': 'carrier', 'party_name': 'Transportadora'},
        ],
    )
    assert len(doc.parties) == 2
    assert doc.parties[0].party_type == 'customer'
    assert doc.parties[1].party_type == 'carrier'


def test_document_definition_not_found(engine):
    with pytest.raises(ValueError, match='not found'):
        engine.create_document(doc_type='non_existent')


def test_numbering_auto_assignment(engine, sale_def, sale_numbering):
    doc1 = engine.create_document(doc_type='sale_order')
    doc2 = engine.create_document(doc_type='sale_order')
    n = engine._repo.find_numbering('sale_order')
    assert n.next_number == 3  # two documents consumed 1 and 2
    assert doc1.number != doc2.number


# ── Dashboard ────────────────────────────────────────────────

def test_dashboard(engine, sale_def, sale_numbering):
    engine.create_document(doc_type='sale_order')
    engine.create_document(doc_type='sale_order')
    dashboard = engine.get_dashboard()
    assert dashboard['total_documents'] >= 2
    assert dashboard['active_definitions'] >= 1
    assert dashboard['by_type'].get('sale_order', 0) >= 2
    assert dashboard['total_value'] >= 0


# ── Line Calculations ────────────────────────────────────────

def test_line_subtotal():
    line = DocumentLine(item_id='item-001', quantity=5, unit_price=20.0)
    assert line.subtotal == 100.0
    assert line.net_total == 100.0


def test_line_with_discount():
    line = DocumentLine(item_id='item-001', quantity=2, unit_price=100.0, discount_value=10.0)
    assert line.subtotal == 200.0
    assert line.net_total == 190.0


def test_document_recalc_totals():
    doc = BusinessDocument(document_type='test')
    doc.add_line(DocumentLine(item_id='item-001', quantity=3, unit_price=50.0, tax_value=15.0, discount_value=5.0))
    doc.add_line(DocumentLine(item_id='item-002', quantity=1, unit_price=100.0))
    assert doc.subtotal == 250.0
    assert doc.discount_total == 5.0
    assert doc.tax_total == 15.0
    assert doc.total == 260.0  # 250 - 5 + 15 = 260


def test_business_document_defaults():
    doc = BusinessDocument(document_type='test')
    assert doc.status == DocumentStatus.DRAFT
    assert doc.header.date is not None
    assert doc.header.currency == 'BRL'
    assert doc.lines == []
    assert doc.parties == []
    assert doc.metadata == {}
    assert doc.direction == 'out'
    assert doc.total == 0.0
