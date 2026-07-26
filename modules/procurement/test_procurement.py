import sys
sys.path.insert(0, '/home/palmarante/projetos_cobol/palmarante-loja')

import pytest
from modules.procurement.core.infrastructure.repositories.memory import ProcurementRepositoryMemory
from modules.procurement.core.application.services.procurement_orchestrator import ProcurementOrchestrator
from modules.procurement.core.domain.entities.rfq import RFQ, RFQItem, TechnicalSpec, RFQStatus
from modules.procurement.core.domain.entities.quotation import SupplierQuotation, QuotationItem, QuotationStatus
from modules.procurement.core.domain.entities.award import AwardDecision, AwardItem, AwardMethod


@pytest.fixture
def repo():
    return ProcurementRepositoryMemory()


@pytest.fixture
def proc(repo):
    return ProcurementOrchestrator(repo)


# ── RFQ (PROC-001) ─────────────────────────────────────────

def test_create_rfq(proc):
    items = [RFQItem(item_id='i-1', item_code='NB-001',
                      item_name='Notebook Dell Latitude', quantity=100,
                      expected_price=5000)]
    rfq = proc.create_rfq('Cotação Notebooks', items=items,
                           invited_suppliers=['s-1', 's-2', 's-3'],
                           requires_technical_evaluation=True)
    assert rfq._id != ''
    assert len(rfq.invited_suppliers) == 3
    assert rfq.status == RFQStatus.DRAFT
    assert rfq.requires_technical_evaluation is True


def test_rfq_with_technical_specs(proc):
    item = RFQItem(item_id='i-1', item_name='Notebook', quantity=10)
    item.add_spec('Memória', '16GB', 'GB', True)
    item.add_spec('SSD', '512GB', 'GB', True)
    item.add_spec('Garantia', '36', 'meses')
    rfq = proc.create_rfq('Cotação Técnica', items=[item])
    assert len(rfq.items[0].technical_specs) == 3


def test_open_rfq(proc):
    rfq = proc.create_rfq('Teste')
    rfq = proc.open_rfq(rfq._id)
    assert rfq.status == RFQStatus.OPEN


# ── Supplier Portal (PROC-002) ─────────────────────────────

def test_portal_invitations(proc):
    rfq = proc.create_rfq('Cotação A', invited_suppliers=['s-1', 's-2'])
    proc.open_rfq(rfq._id)
    inv = proc.portal_invitations('s-1')
    assert len(inv) == 1
    assert inv[0]['title'] == 'Cotação A'
    assert inv[0]['has_quoted'] is False


def test_portal_submit_quotation(proc):
    rfq = proc.create_rfq('Cotação Portal', items=[
        RFQItem(item_id='i-1', item_name='Produto', quantity=10)])
    proc.open_rfq(rfq._id)
    q = proc.portal_submit(rfq._id, 's-1', 'Fornecedor ABC',
                            items=[{'item_id': 'i-1', 'quantity': 10,
                                    'unit_price': 4500}],
                            freight=200, delivery_estimate_days=15,
                            warranty_description='12 meses')
    assert q._id != ''
    assert q.grand_total == 45200


# ── Comparison Engine (PROC-003/004) ⭐⭐⭐⭐⭐ ────────────

def test_comparison_engine_basic(proc):
    rfq = proc.create_rfq('Cotação Comparação', items=[
        RFQItem(item_id='i-1', item_name='Notebook', quantity=10)])
    proc.open_rfq(rfq._id)
    proc.submit_quotation(rfq._id, 's-1', 'ABC', items=[
        QuotationItem(item_id='i-1', quantity=10, unit_price=4950)], freight=300,
        delivery_estimate_days=15, warranty_description='12 meses')
    proc.submit_quotation(rfq._id, 's-2', 'XYZ', items=[
        QuotationItem(item_id='i-1', quantity=10, unit_price=4880)], freight=0,
        delivery_estimate_days=30, warranty_description='12 meses')
    proc.submit_quotation(rfq._id, 's-3', 'Delta', items=[
        QuotationItem(item_id='i-1', quantity=10, unit_price=5020)], freight=100,
        delivery_estimate_days=10, warranty_description='24 meses')
    result = proc.compare(rfq._id)
    assert len(result['matrix']) == 1
    assert len(result['matrix'][0]['quotations']) == 3
    assert len(result['summary']) == 3
    assert result['best'] is not None
    assert 'decision_matrix' in result
    assert len(result['decision_matrix']) == 3


def test_comparison_engine_scoring(proc):
    rfq = proc.create_rfq('Score Test', items=[
        RFQItem(item_id='i-1', item_name='Produto', quantity=10)])
    proc.open_rfq(rfq._id)
    proc.submit_quotation(rfq._id, 's-1', 'Barato', items=[
        QuotationItem(item_id='i-1', quantity=10, unit_price=100)], freight=0,
        delivery_estimate_days=5)
    proc.submit_quotation(rfq._id, 's-2', 'Caro', items=[
        QuotationItem(item_id='i-1', quantity=10, unit_price=200)], freight=0,
        delivery_estimate_days=5)
    result = proc.compare(rfq._id)
    best = result['best']
    assert best['supplier_name'] == 'Barato'


def test_comparison_custom_weights(proc):
    rfq = proc.create_rfq('Weights', items=[
        RFQItem(item_id='i-1', item_name='Produto', quantity=10)])
    proc.open_rfq(rfq._id)
    proc.submit_quotation(rfq._id, 's-1', 'A', items=[
        QuotationItem(item_id='i-1', quantity=10, unit_price=100)], freight=0,
        delivery_estimate_days=30)
    proc.submit_quotation(rfq._id, 's-2', 'B', items=[
        QuotationItem(item_id='i-1', quantity=10, unit_price=101)], freight=0,
        delivery_estimate_days=1)
    proc.comparison.set_weights({'price': 10, 'delivery': 60, 'freight': 10,
                                  'quality': 10, 'history': 5, 'warranty': 5})
    result = proc.compare(rfq._id)
    # With delivery weight=60, supplier B (1 day) should be best
    assert result['best']['supplier_id'] == 's-2'


def test_comparison_technical_specs(proc):
    item = RFQItem(item_id='i-1', item_name='Notebook', quantity=10)
    item.add_spec('Memória', '16GB', 'GB', True)
    item.add_spec('SSD', '512GB', 'GB', True)
    rfq = proc.create_rfq('Tech Compare', items=[item])
    proc.open_rfq(rfq._id)
    proc.submit_quotation(rfq._id, 's-1', 'A', items=[
        QuotationItem(item_id='i-1', quantity=10, unit_price=100,
                       technical_response={'Memória': '16GB', 'SSD': '512GB'})])
    result = proc.compare(rfq._id)
    matrix_item = result['matrix'][0]
    assert len(matrix_item['technical_specs']) == 2
    assert matrix_item['technical_specs'][0]['field'] == 'Memória'


# ── Award Engine (PROC-005) ───────────────────────────────

def test_award_single(proc):
    rfq = proc.create_rfq('Award Test', items=[
        RFQItem(item_id='i-1', item_name='Produto', quantity=10)])
    proc.open_rfq(rfq._id)
    q = proc.submit_quotation(rfq._id, 's-1', 'Vencedor', items=[
        QuotationItem(item_id='i-1', quantity=10, unit_price=100)])
    decision = proc.award_single(rfq._id, 's-1', q._id)
    assert decision.method == AwardMethod.SINGLE
    assert len(decision.items) == 1
    rfq = proc.repo.find_rfq_by_id(rfq._id)
    assert rfq.status == RFQStatus.AWARDED


def test_award_per_item(proc):
    rfq = proc.create_rfq('Multi Award', items=[
        RFQItem(item_id='i-1', item_name='Notebook', quantity=10),
        RFQItem(item_id='i-2', item_name='Mouse', quantity=50)])
    proc.open_rfq(rfq._id)
    q1 = proc.submit_quotation(rfq._id, 's-1', 'Fornecedor A', items=[
        QuotationItem(item_id='i-1', quantity=10, unit_price=5000),
        QuotationItem(item_id='i-2', quantity=50, unit_price=50)])
    q2 = proc.submit_quotation(rfq._id, 's-2', 'Fornecedor B', items=[
        QuotationItem(item_id='i-1', quantity=10, unit_price=4800),
        QuotationItem(item_id='i-2', quantity=50, unit_price=55)])
    decision = proc.award_per_item(rfq._id, [
        {'item_id': 'i-1', 'quotation_id': q2._id, 'quantity': 10},  # B melhor para notebook
        {'item_id': 'i-2', 'quotation_id': q1._id, 'quantity': 50},  # A melhor para mouse
    ])
    assert decision.method == AwardMethod.PER_ITEM
    assert len(decision.items) == 2


def test_generate_multiple_pos(proc):
    rfq = proc.create_rfq('Multi PO', items=[
        RFQItem(item_id='i-1', item_name='Item A', quantity=10),
        RFQItem(item_id='i-2', item_name='Item B', quantity=20)])
    proc.open_rfq(rfq._id)
    q1 = proc.submit_quotation(rfq._id, 's-1', 'Fornecedor A', items=[
        QuotationItem(item_id='i-1', quantity=10, unit_price=100)])
    q2 = proc.submit_quotation(rfq._id, 's-2', 'Fornecedor B', items=[
        QuotationItem(item_id='i-2', quantity=20, unit_price=50)])
    decision = proc.award_per_item(rfq._id, [
        {'item_id': 'i-1', 'quotation_id': q1._id, 'quantity': 10},
        {'item_id': 'i-2', 'quotation_id': q2._id, 'quantity': 20},
    ])
    pos = proc.generate_pos(decision._id, 'PO-001')
    assert len(pos) == 2
    assert pos[0].supplier_id in ('s-1', 's-2')
    assert pos[1].supplier_id in ('s-1', 's-2')


# ── Simulation (PROC-008) ─────────────────────────────────

def test_simulation(proc):
    rfq = proc.create_rfq('Sim Test', items=[
        RFQItem(item_id='i-1', quantity=10)])
    proc.open_rfq(rfq._id)
    q = proc.submit_quotation(rfq._id, 's-1', 'Simulado', items=[
        QuotationItem(item_id='i-1', quantity=10, unit_price=100)], freight=50)
    result = proc.simulate(q._id, {'freight': 0})
    assert result['base_total'] == 1050
    assert result['recalculated_total'] == 1000
    assert result['savings'] == 50


def test_simulation_with_freight_change(proc):
    rfq = proc.create_rfq('Freight Sim', items=[
        RFQItem(item_id='i-1', quantity=10)])
    proc.open_rfq(rfq._id)
    q = proc.submit_quotation(rfq._id, 's-1', 'Test', items=[
        QuotationItem(item_id='i-1', quantity=10, unit_price=100)], freight=100)
    result = proc.simulate(q._id, {'freight': 0})
    assert result['recalculated_total'] == 1000
    assert result['savings'] == 100


# ── Negotiation (PROC-009) ─────────────────────────────────

def test_negotiation(proc):
    rfq = proc.create_rfq('Neg Test', items=[
        RFQItem(item_id='i-1', quantity=10)])
    proc.open_rfq(rfq._id)
    q = proc.submit_quotation(rfq._id, 's-1', 'Negociado', items=[
        QuotationItem(item_id='i-1', quantity=10, unit_price=100)])
    cp = proc.make_counter(rfq._id, q._id, 'buyer',
                            items=[{'item_id': 'i-1', 'unit_price': 90, 'quantity': 10}],
                            grand_total=900)
    assert cp is not None
    assert cp.round.value == 'counter'
    history = proc.negotiation_history(q._id)
    assert len(history) == 1


# ── Decision Matrix (PROC-010) ────────────────────────────

def test_decision_matrix(proc):
    rfq = proc.create_rfq('Matrix Test', items=[
        RFQItem(item_id='i-1', quantity=10)])
    proc.open_rfq(rfq._id)
    proc.submit_quotation(rfq._id, 's-1', 'ABC', items=[
        QuotationItem(item_id='i-1', quantity=10, unit_price=100)], freight=0,
        delivery_estimate_days=10)
    proc.submit_quotation(rfq._id, 's-2', 'XYZ', items=[
        QuotationItem(item_id='i-1', quantity=10, unit_price=95)], freight=0,
        delivery_estimate_days=15)
    result = proc.compare(rfq._id)
    dm = result['decision_matrix']
    assert len(dm) == 2
    assert dm[0]['score'] >= dm[1]['score']
    assert 'price' in dm[0]
    assert 'delivery' in dm[0]
    assert 'score_detail' in dm[0]
    assert 'history' in dm[0]


# ── Full Flow: RFQ → Portal → Quotes → Compare → Negotiate → Award → POs ──

def test_full_procurement_flow(proc):
    # 1. Create RFQ with technical specs
    item = RFQItem(item_id='i-1', item_name='Notebook Dell Latitude 5450',
                    quantity=100, expected_price=5000)
    item.add_spec('Memória', '16GB', 'GB', True)
    item.add_spec('SSD', '512GB', 'GB', True)
    rfq = proc.create_rfq('RFQ #001 - Notebooks Corporativos', items=[item],
                           invited_suppliers=['s-1', 's-2', 's-3'],
                           requires_technical_evaluation=True)
    assert rfq._id != ''
    # 2. Open RFQ
    proc.open_rfq(rfq._id)
    # 3. Suppliers submit via Portal
    q1 = proc.portal_submit(rfq._id, 's-1', 'ABC Tecnologia',
                             items=[{'item_id': 'i-1', 'quantity': 100, 'unit_price': 4950,
                                     'technical_response': {'Memória': '16GB', 'SSD': '512GB'}}],
                             freight=300, delivery_estimate_days=15,
                             warranty_description='12 meses', payment_method='boleto')
    q2 = proc.portal_submit(rfq._id, 's-2', 'XYZ Solutions',
                             items=[{'item_id': 'i-1', 'quantity': 100, 'unit_price': 4880,
                                     'technical_response': {'Memória': '16GB', 'SSD': '256GB'}}],
                             freight=0, delivery_estimate_days=30,
                             warranty_description='12 meses', payment_method='pix')
    q3 = proc.portal_submit(rfq._id, 's-3', 'Delta Distribuição',
                             items=[{'item_id': 'i-1', 'quantity': 100, 'unit_price': 5020,
                                     'technical_response': {'Memória': '32GB', 'SSD': '1TB'}}],
                             freight=100, delivery_estimate_days=10,
                             warranty_description='24 meses', payment_method='boleto')
    # 4. Compare
    comp = proc.compare(rfq._id)
    assert len(comp['summary']) == 3
    assert comp['best'] is not None
    assert len(comp['matrix'][0]['technical_specs']) == 2
    # 5. Simulate what-if (500 units)
    sim = proc.simulate(q1._id, {'quantity': 500})
    assert sim['base_total'] == q1.grand_total
    assert sim['recalculated_total'] == q1.grand_total * 5
    # 6. Negotiate with best
    cp = proc.make_counter(rfq._id, comp['best']['quotation_id'], 'buyer',
                            items=[{'item_id': 'i-1', 'unit_price': 4800, 'quantity': 100}],
                            grand_total=480000)
    assert cp is not None
    # 7. Award (per item — only 1 item here)
    decision = proc.award_single(rfq._id, comp['best']['supplier_id'],
                                  comp['best']['quotation_id'], created_by='Compras')
    assert len(decision.items) == 1
    # 8. Generate PO
    pos = proc.generate_pos(decision._id, 'PO-2026')
    assert len(pos) == 1
