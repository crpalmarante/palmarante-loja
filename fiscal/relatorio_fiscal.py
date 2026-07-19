import os
import json
from datetime import datetime, timedelta
from collections import defaultdict

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def carregar_vendas():
    try:
        with open(os.path.join(DIR, 'dados/vendas.json')) as f:
            return json.load(f).get('vendas', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def carregar_produtos():
    try:
        with open(os.path.join(DIR, 'dados/produtos.json')) as f:
            return json.load(f).get('produtos', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def apurar_icms(periodo_inicio, periodo_fim):
    vendas = carregar_vendas()
    produtos = carregar_produtos()
    prod_map = {str(p['id']): p for p in produtos}

    total_icms_debito = 0.0
    total_icms_st = 0.0
    total_receita = 0.0
    total_icms_isento = 0.0
    csosn_counts = defaultdict(lambda: {'qtde': 0, 'valor': 0.0})

    for venda in vendas:
        data_str = venda.get('data', '')[:10]
        if not (periodo_inicio <= data_str <= periodo_fim):
            continue
        if venda.get('status') in ('PENDENTE', 'CANCELADO'):
            continue
        if venda.get('forma_pg') == 'PENDENTE':
            continue

        total_receita += float(venda.get('total', 0))

        for item in venda.get('itens', []):
            prod = prod_map.get(str(item.get('prod_id', '')), {})
            cst = prod.get('cst', '400')
            alq = float(prod.get('icms_alq', 0) or 0)
            qtd = float(item.get('qtd', 1))
            preco = float(item.get('preco', 0))
            total_item = qtd * preco

            csosn_counts[cst]['qtde'] += 1
            csosn_counts[cst]['valor'] += total_item

            if cst in ('000', '010', '020', '400', '500', '510', '520'):
                total_icms_debito += total_item * alq / 100
            elif cst in ('030', '060', '610', '620'):
                total_icms_st += total_item * alq / 100
            elif cst in ('040', '041', '600', '700'):
                total_icms_isento += total_item

    return {
        'periodo': f'{periodo_inicio} a {periodo_fim}',
        'receita_total': round(total_receita, 2),
        'icms_debito': round(total_icms_debito, 2),
        'icms_st': round(total_icms_st, 2),
        'icms_isento': round(total_icms_isento, 2),
        'icms_liquido': round(total_icms_debito - total_icms_st, 2),
        'cst_detalhe': dict(csosn_counts),
        'total_itens': sum(c['qtde'] for c in csosn_counts.values()),
    }

def apurar_pis_cofins(periodo_inicio, periodo_fim, regime='cumulativo'):
    vendas = carregar_vendas()
    total_receita = 0.0

    for venda in vendas:
        data_str = venda.get('data', '')[:10]
        if not (periodo_inicio <= data_str <= periodo_fim):
            continue
        if venda.get('status') in ('PENDENTE', 'CANCELADO'):
            continue
        if venda.get('forma_pg') == 'PENDENTE':
            continue
        total_receita += float(venda.get('total', 0))

    if regime == 'cumulativo':
        alq_pis = 0.65
        alq_cofins = 3.0
    else:
        alq_pis = 1.65
        alq_cofins = 7.6

    return {
        'periodo': f'{periodo_inicio} a {periodo_fim}',
        'regime': regime,
        'receita_total': round(total_receita, 2),
        'pis': round(total_receita * alq_pis / 100, 2),
        'cofins': round(total_receita * alq_cofins / 100, 2),
        'aliquota_pis': alq_pis,
        'aliquota_cofins': alq_cofins,
        'total_impostos': round(total_receita * (alq_pis + alq_cofins) / 100, 2),
    }

def apurar_completo(periodo_inicio, periodo_fim):
    icms = apurar_icms(periodo_inicio, periodo_fim)
    pis_cofins_cumulativo = apurar_pis_cofins(periodo_inicio, periodo_fim, 'cumulativo')
    pis_cofins_nao_cumulativo = apurar_pis_cofins(periodo_inicio, periodo_fim, 'nao-cumulativo')

    return {
        'periodo': f'{periodo_inicio} a {periodo_fim}',
        'icms': icms,
        'pis_cofins_cumulativo': pis_cofins_cumulativo,
        'pis_cofins_nao_cumulativo': pis_cofins_nao_cumulativo,
        'total_impostos': {
            'cumulativo': round(icms['icms_liquido'] + pis_cofins_cumulativo['total_impostos'], 2),
            'nao_cumulativo': round(icms['icms_liquido'] + pis_cofins_nao_cumulativo['total_impostos'], 2),
        },
        'data_apuracao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
