import os
import json
import subprocess
from lxml import etree
from datetime import datetime
import re

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NS = {
    'nfe': 'http://www.portalfiscal.inf.br/nfe',
}

def extrair_texto(elemento, caminho, default=''):
    if elemento is None:
        return default
    encontrado = elemento.find(caminho, NS)
    if encontrado is not None and encontrado.text:
        return encontrado.text.strip()
    return default

def parse_nfe_xml(xml_string):
    root = etree.fromstring(xml_string.encode())
    nfe = root.find('.//nfe:NFe', NS)
    if nfe is None:
        nfe = root
    infNFe = nfe.find('.//nfe:infNFe', NS)
    if infNFe is None:
        raise ValueError('XML invalido: infNFe nao encontrado')

    ide = infNFe.find('nfe:ide', NS)
    emit = infNFe.find('nfe:emit', NS)
    dest = infNFe.find('nfe:dest', NS)
    dets = infNFe.findall('nfe:det', NS)
    total = infNFe.find('.//nfe:ICMSTot', NS)

    cnpj_emit = extrair_texto(emit, 'nfe:CNPJ')
    nome_emit = extrair_texto(emit, 'nfe:xNome')
    ie_emit = extrair_texto(emit, 'nfe:IE')

    data_emissao_str = extrair_texto(ide, 'nfe:dhEmi')
    data_emissao = data_emissao_str[:10] if data_emissao_str else ''

    chave = extrair_texto(ide, 'nfe:cNF', '')
    n_nf = extrair_texto(ide, 'nfe:nNF')
    serie = extrair_texto(ide, 'nfe:serie')
    natureza = extrair_texto(ide, 'nfe:natOp')

    # Get full chave from ID attribute
    chave_completa = ''
    infNFe_id = infNFe.get('Id', '')
    if infNFe_id.startswith('NFe'):
        chave_completa = infNFe_id[3:]

    itens = []
    for det in dets:
        prod = det.find('nfe:prod', NS)
        imposto = det.find('nfe:imposto', NS)
        n_item = det.get('nItem', '')

        nome = extrair_texto(prod, 'nfe:xProd')
        ncm = extrair_texto(prod, 'nfe:NCM')
        cfop = extrair_texto(prod, 'nfe:CFOP')
        ucom = extrair_texto(prod, 'nfe:uCom')
        qcom = extrair_texto(prod, 'nfe:qCom')
        vuncom = extrair_texto(prod, 'nfe:vUnCom')
        vprod = extrair_texto(prod, 'nfe:vProd')
        cest_str = extrair_texto(prod, 'nfe:CEST')
        codigo_prod = extrair_texto(prod, 'nfe:cProd')
        ean = extrair_texto(prod, 'nfe:cEAN')

        icms_info = {}
        if imposto is not None:
            for icms_tag in ['ICMS00', 'ICMS10', 'ICMS20', 'ICMS30', 'ICMS40', 'ICMS51', 'ICMS60', 'ICMS70', 'ICMS90', 'ICMSSN101', 'ICMSSN102', 'ICMSSN201', 'ICMSSN202', 'ICMSSN500', 'ICMSSN900']:
                icms_node = imposto.find(f'nfe:{icms_tag}', NS)
                if icms_node is not None:
                    icms_info['cst'] = extrair_texto(icms_node, 'nfe:CST')
                    icms_info['csosn'] = extrair_texto(icms_node, 'nfe:CSOSN')
                    icms_info['orig'] = extrair_texto(icms_node, 'nfe:orig')
                    icms_info['pICMS'] = extrair_texto(icms_node, 'nfe:pICMS')
                    icms_info['vICMS'] = extrair_texto(icms_node, 'nfe:vICMS')
                    break

        itens.append({
            'n_item': n_item,
            'codigo': codigo_prod,
            'nome': nome,
            'ncm': ncm,
            'cfop': cfop,
            'cest': cest_str,
            'ean': ean,
            'unidade': ucom,
            'quantidade': qcom,
            'vl_unitario': vuncom,
            'vl_total': vprod,
            'icms_cst': icms_info.get('cst', ''),
            'icms_csosn': icms_info.get('csosn', ''),
            'icms_aliquota': icms_info.get('pICMS', ''),
            'icms_valor': icms_info.get('vICMS', ''),
        })

    vBC = extrair_texto(total, 'nfe:vBC')
    vICMS = extrair_texto(total, 'nfe:vICMS')
    vProd = extrair_texto(total, 'nfe:vProd')
    vNF = extrair_texto(total, 'nfe:vNF')
    vST = extrair_texto(total, 'nfe:vST')

    resultado = {
        'chave': chave_completa,
        'numero': n_nf,
        'serie': serie,
        'data_emissao': data_emissao,
        'natureza': natureza,
        'fornecedor': {
            'cnpj': cnpj_emit,
            'nome': nome_emit,
            'ie': ie_emit,
        },
        'total': {
            'vBC': vBC,
            'vICMS': vICMS,
            'vProd': vProd,
            'vNF': vNF,
            'vST': vST,
        },
        'itens': itens,
        'xml': xml_string,
    }
    return resultado

def importar_nfe_entrada(xml_string, data_path):
    parsed = parse_nfe_xml(xml_string)

    path = os.path.join(data_path, 'nfe_entrada.json')
    try:
        with open(path) as f:
            dados = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = {'nfe_entradas': []}

    chave = parsed.get('chave', '')
    for existente in dados.get('nfe_entradas', []):
        if existente.get('chave') == chave:
            return parsed, False

    registro = {
        'chave': chave,
        'numero': parsed.get('numero', ''),
        'serie': parsed.get('serie', ''),
        'data_emissao': parsed.get('data_emissao', ''),
        'data_importacao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'fornecedor': parsed.get('fornecedor', {}),
        'total': parsed.get('total', {}),
        'itens': parsed.get('itens', []),
        'produtos_adicionados': [],
    }

    dados['nfe_entradas'].append(registro)
    with open(path, 'w') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    return parsed, True

def importar_e_adicionar_produtos(xml_string, data_path):
    parsed, is_new = importar_nfe_entrada(xml_string, data_path)
    if not is_new:
        return parsed, False, []

    produtos_path = os.path.join(DIR, 'dados/produtos.json')
    try:
        with open(produtos_path) as f:
            prods = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        prods = {'produtos': []}

    existentes = {p.get('nome', '').strip().lower(): p for p in prods.get('produtos', [])}
    ids_adicionados = []
    ultimo_id = max([p.get('id', 0) for p in prods.get('produtos', [])], default=0)

    for item in parsed.get('itens', []):
        nome = item.get('nome', '').strip()
        if not nome:
            continue
        key = nome.lower()
        if key in existentes:
            ids_adicionados.append(existentes[key].get('id'))
            continue

        ultimo_id += 1
        preco_custo = float(item.get('vl_unitario', 0))
        preco_venda = preco_custo * 1.3

        novo_prod = {
            'id': ultimo_id,
            'nome': nome,
            'codigo': item.get('codigo',str(ultimo_id)),
            'preco': round(preco_venda, 2),
            'preco_custo': preco_custo,
            'stock': float(item.get('quantidade', 0)),
            'ncm': item.get('ncm', ''),
            'cest': item.get('cest', ''),
            'cfop': item.get('cfop', '5102'),
            'cst': item.get('icms_cst', item.get('icms_csosn', '400')),
            'icms_alq': item.get('icms_aliquota', 0),
            'unidade': item.get('unidade', 'UN'),
            'codigo_barras': item.get('ean', ''),
        }
        prods['produtos'].append(novo_prod)
        ids_adicionados.append(ultimo_id)

    with open(produtos_path, 'w') as f:
        json.dump(prods, f, ensure_ascii=False, indent=2)

    parsed['produtos_adicionados'] = ids_adicionados
    return parsed, True, ids_adicionados
