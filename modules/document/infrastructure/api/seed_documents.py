"""Seed document definitions and numbering for testing."""
from modules.document.infrastructure.postgres.document_repository_postgres import DocumentRepositoryMemory
from modules.document.application.services.document_engine import DocumentEngine
from modules.document.domain.entities.document_definition import DocumentDefinition, DocumentFieldDef, DocumentLineFieldDef, FieldType

repo = DocumentRepositoryMemory()
engine = DocumentEngine(repo)


def seed():
    # ── Document Definitions ────────────────────────────────────
    definitions = [
        DocumentDefinition(
            name='Pedido de Venda', code='sale_order',
            direction='out', has_lines=True, has_parties=True,
            has_totals=True, has_workflow=True, workflow_code='sales_approval',
            behaviors=['inventory', 'financial'],
            header_fields=[
                DocumentFieldDef(name='Cond. Pagamento', code='payment_terms', field_type=FieldType.TEXT, sort_order=1),
                DocumentFieldDef(name='Transportadora', code='carrier', field_type=FieldType.TEXT, sort_order=2),
            ],
            line_fields=[
                DocumentLineFieldDef(name='Lote', code='lot', field_type=FieldType.TEXT, sort_order=1),
            ],
            party_types=['customer', 'carrier'],
        ),
        DocumentDefinition(
            name='Pedido de Compra', code='purchase_order',
            direction='in', has_lines=True, has_parties=True,
            has_totals=True, has_workflow=True, workflow_code='purchase_approval',
            behaviors=['inventory', 'financial'],
            party_types=['supplier'],
        ),
        DocumentDefinition(
            name='Orçamento', code='quotation',
            direction='out', has_lines=True, has_parties=True,
            has_totals=True, has_workflow=False,
            behaviors=['financial'],
            party_types=['customer'],
        ),
        DocumentDefinition(
            name='Nota Fiscal', code='invoice',
            direction='out', has_lines=True, has_parties=True,
            has_totals=True, has_workflow=False,
            behaviors=['inventory', 'financial', 'fiscal'],
            party_types=['customer'],
        ),
        DocumentDefinition(
            name='Ordem de Produção', code='production_order',
            direction='internal', has_lines=True, has_parties=False,
            has_totals=True, has_workflow=True, workflow_code='production_flow',
            behaviors=['inventory'],
            party_types=[],
        ),
        DocumentDefinition(
            name='Ordem de Serviço', code='service_order',
            direction='out', has_lines=True, has_parties=True,
            has_totals=True, has_workflow=True, workflow_code='service_flow',
            behaviors=['financial'],
            party_types=['customer', 'technician'],
        ),
    ]

    for d in definitions:
        try:
            existing = repo.find_definition_by_code(d.code)
            if existing:
                print(f'Definition "{d.code}" already exists, skipping')
                continue
            saved = repo.save_definition(d)
            print(f'✓ Definition: {saved.name} ({saved.code})')
        except Exception as e:
            print(f'✗ Error creating definition "{d.code}": {e}')

    # ── Document Numbering ──────────────────────────────────────
    numbering_rules = [
        {'doc_type': 'sale_order', 'pattern': 'V{v}{seq:06d}'},
        {'doc_type': 'purchase_order', 'pattern': 'PC{v}{seq:06d}'},
        {'doc_type': 'quotation', 'pattern': 'ORC{v}{seq:06d}'},
        {'doc_type': 'invoice', 'pattern': 'NF{v}{seq:06d}', 'digits': 9},
        {'doc_type': 'production_order', 'pattern': 'OP{v}{seq:06d}'},
        {'doc_type': 'service_order', 'pattern': 'OS{v}{seq:06d}'},
    ]

    for rule in numbering_rules:
        try:
            existing = repo.find_numbering(rule['doc_type'])
            if existing:
                print(f'Numbering for "{rule["doc_type"]}" already exists, skipping')
                continue
            num = engine.setup_numbering(
                doc_type=rule['doc_type'],
                pattern=rule['pattern'].replace('{v}', '{year}{month}'),
                digits=rule.get('digits', 6),
            )
            print(f'✓ Numbering: {rule["doc_type"]} → {num.generate_number()}')
        except Exception as e:
            print(f'✗ Error creating numbering "{rule["doc_type"]}": {e}')

    # ── Sample Documents ────────────────────────────────────────
    samples = [
        {
            'doc_type': 'sale_order',
            'direction': 'out',
            'header': {'responsible': 'Carlos Silva', 'department': 'Vendas', 'cost_center': 'CC-VENDAS'},
            'lines': [
                {'item_id': 'item-001', 'item_name': 'Notebook Dell', 'quantity': 2, 'unit_price': 4500.00},
                {'item_id': 'item-002', 'item_name': 'Mouse Wireless', 'quantity': 5, 'unit_price': 89.90},
            ],
            'parties': [{'party_id': 'party-cust-001', 'party_type': 'customer', 'party_name': 'Empresa ABC Ltda'}],
            'notes': 'Pedido urgente - entrega em 48h',
        },
        {
            'doc_type': 'purchase_order',
            'direction': 'in',
            'header': {'responsible': 'Ana Oliveira', 'department': 'Compras', 'cost_center': 'CC-COMPRAS'},
            'lines': [
                {'item_id': 'item-003', 'item_name': 'Parafuso M8', 'quantity': 1000, 'unit_price': 0.45},
                {'item_id': 'item-004', 'item_name': 'Porca M8', 'quantity': 1000, 'unit_price': 0.30},
            ],
            'parties': [{'party_id': 'party-sup-001', 'party_type': 'supplier', 'party_name': 'Fornecedora XYZ'}],
            'notes': 'Entregar no almoxarifado central',
        },
        {
            'doc_type': 'quotation',
            'direction': 'out',
            'lines': [
                {'item_id': 'item-005', 'item_name': 'Serviço de Consultoria', 'quantity': 40, 'unit_price': 250.00},
            ],
            'parties': [{'party_id': 'party-cust-002', 'party_type': 'customer', 'party_name': 'Cliente Potencial SA'}],
            'notes': 'Válido por 30 dias',
        },
    ]

    for s in samples:
        try:
            doc = engine.create_document(
                doc_type=s['doc_type'],
                direction=s.get('direction', 'out'),
                header=s.get('header', {}),
                lines=s.get('lines', []),
                parties=s.get('parties', []),
                notes=s.get('notes', ''),
                created_by='seed',
            )
            print(f'✓ Document: {doc.number} ({doc.document_type}) — {doc.status.value}')
        except Exception as e:
            print(f'✗ Error creating document "{s["doc_type"]}": {e}')

    print(f'\nSeeding complete! {len(definitions)} definitions, {len(numbering_rules)} numbering rules, {len(samples)} documents.')

    return repo


if __name__ == '__main__':
    seed()
