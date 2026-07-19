import os
from datetime import datetime

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def exportar_sped_fiscal(periodo_inicio, periodo_fim, cnpj, ie, razao_social):
    linhas = []
    reg_0000 = f'|0000|001|1|{periodo_inicio.replace("-","")}|{periodo_fim.replace("-","")}|{razao_social}|{cnpj}|{ie}|{""}|{""}|{""}|{""}|{""}|'
    linhas.append(reg_0000)

    with open(os.path.join(DIR, 'dados/vendas.json')) as f:
        import json
        vendas = json.load(f).get('vendas', [])

    with open(os.path.join(DIR, 'dados/produtos.json')) as f:
        produtos = json.load(f)
        prod_map = {str(p['id']): p for p in produtos.get('produtos', [])}

    index_c100 = 1
    for venda in vendas:
        data_str = venda.get('data', '')
        if not data_str:
            continue
        if (periodo_inicio <= data_str[:10] <= periodo_fim) or (periodo_inicio <= data_str.replace('/', '-')[:10] <= periodo_fim):
            pass
        else:
            continue

        if venda.get('status') in ('PENDENTE', 'CANCELADO'):
            continue

        cliente = venda.get('cliente', 'Consumidor Final')
        total = float(venda.get('total', 0))
        chave = venda.get('chave', '')

        if venda.get('forma_pg') == 'PENDENTE':
            continue

        cpf_cnpj_cli = ''.join(c for c in cliente if c.isdigit())
        tipo_doc = '55' if len(cpf_cnpj_cli) == 14 else '65'

        linhas.append(f'|C100|{index_c100}|1|{tipo_doc}|{""}|{""}|{data_str[:10]}|{""}|{chave}|{""}|{"1"}|{""}|{""}|{total:.2f}|{"0.00"}|{"0.00"}|{"0.00"}|')
        index_c100 += 1

        n_item = 1
        for item in venda.get('itens', []):
            prod = prod_map.get(str(item.get('prod_id', '')), {})
            cfop = prod.get('cfop', '5102')
            cst = prod.get('cst', '400')
            ncm = prod.get('ncm', '')
            qtd = float(item.get('qtd', 1))
            preco = float(item.get('preco', 0))
            total_item = qtd * preco

            linhas.append(f'|C170|{n_item}|{item.get("codigo","")}|{item.get("nome","")}|{"UN"}|{qtd:.3f}|{preco:.2f}|{total_item:.2f}|{"0.00"}|{"0.00"}|{cfop}|{ncm}|{cst}|{""}|{""}|')
            n_item += 1

    linhas.append(f'|9900|{len(linhas)}|')
    linhas.append('|9999|')

    return '\n'.join(linhas)

def exportar_sped_pis_cofins(periodo_inicio, periodo_fim, cnpj):
    linhas = []
    reg_0000 = f'|0000|050|1|{periodo_inicio.replace("-","")}|{periodo_fim.replace("-","")}|{cnpj}|{""}|{""}|'
    linhas.append(reg_0000)

    with open(os.path.join(DIR, 'dados/vendas.json')) as f:
        import json
        vendas = json.load(f).get('vendas', [])

    for venda in vendas:
        if venda.get('forma_pg') == 'PENDENTE':
            continue
        if venda.get('status') == 'CANCELADO':
            continue

        total = float(venda.get('total', 0))
        chave = venda.get('chave', '')
        cliente = venda.get('cliente', 'CF')
        cpf_cnpj = ''.join(c for c in cliente if c.isdigit())

        linhas.append(f'|C010|{cpf_cnpj}|{""}|')

        n_item = 1
        for item in venda.get('itens', []):
            qtd = float(item.get('qtd', 1))
            preco = float(item.get('preco', 0))
            total_item = qtd * preco
            linhas.append(f'|C100|{n_item}|{chave}|{item.get("nome","")}|{"UN"}|{qtd:.3f}|{preco:.2f}|{total_item:.2f}|{"0.00"}|{"0.00"}|')
            n_item += 1

    linhas.append(f'|9900|{len(linhas)}|')
    linhas.append('|9999|')
    return '\n'.join(linhas)
