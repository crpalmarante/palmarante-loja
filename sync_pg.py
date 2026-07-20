#!/usr/bin/env python3
"""Sincroniza dados do COBOL/JSON para PostgreSQL (consultas e relatorios)"""
import json, os, subprocess, sys
from datetime import datetime

DIR = os.path.dirname(os.path.abspath(__file__))

# Conexao PostgreSQL (local dev: palmarante@localhost:5433/palmarante_rh)
PG_CONFIG = {
    'host': '/tmp',
    'port': 5433,
    'dbname': 'palmarante_rh',
    'user': 'palmarante',
}

try:
    import psycopg2
except ImportError:
    print("psycopg2 nao instalado. Execute: pip3 install --user psycopg2-binary")
    sys.exit(1)

def get_pg():
    return psycopg2.connect(**PG_CONFIG)

def run_cobol(program, acao='listar'):
    try:
        r = subprocess.run(
            [os.path.join(DIR, program)],
            env={**os.environ, 'ACAO': acao},
            capture_output=True, text=True, timeout=10,
            cwd=DIR
        )
        if r.returncode == 0 and r.stdout:
            return json.loads(r.stdout)
    except Exception as e:
        print(f"  [WARN] COBOL {program} erro: {e}")
    return None

def parse_date(s):
    if not s or s.strip() == '':
        return None
    for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d/%m/%y'):
        try:
            return datetime.strptime(s.strip(), fmt).date()
        except ValueError:
            continue
    return None

def parse_money(s):
    if not s:
        return 0
    s = str(s).replace(',', '.').strip()
    try:
        return float(s)
    except ValueError:
        return 0

def sync_funcionarios():
    print("Sincronizando funcionarios...")
    data = run_cobol('gerir_funcionarios')
    if not data or 'funcionarios' not in data:
        print("  Nenhum dado encontrado")
        return 0

    conn = get_pg()
    cur = conn.cursor()
    count = 0
    for f in data['funcionarios']:
        cur.execute("""
            INSERT INTO rh.funcionarios
                (fn_id, nome, usuario, cpf, rg, data_nasc, celular, email,
                 endereco, data_admissao, data_demissao, salario, filial_id,
                 tipo_contrato, pis, ctps, cbo, grau_instrucao,
                 banco, agencia, conta, pix, plano_saude,
                 vale_transporte, vale_refeicao, ativo)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (fn_id) DO UPDATE SET
                nome=EXCLUDED.nome, usuario=EXCLUDED.usuario, cpf=EXCLUDED.cpf,
                celular=EXCLUDED.celular, email=EXCLUDED.email,
                endereco=EXCLUDED.endereco, salario=EXCLUDED.salario,
                ativo=EXCLUDED.ativo, updated_at=NOW()
        """, (
            f.get('id'), f.get('nome'), f.get('usuario'),
            f.get('cpf'), f.get('rg'), parse_date(f.get('data_nasc')),
            f.get('celular'), f.get('email'), f.get('endereco'),
            parse_date(f.get('data_adm')), parse_date(f.get('data_dem')),
            parse_money(f.get('salario')), f.get('filial_id'),
            f.get('tipo_contrato'), f.get('pis'), f.get('ctps'),
            f.get('cbo'), f.get('grau_instrucao'),
            f.get('banco'), f.get('agencia'), f.get('conta'),
            f.get('pix'), f.get('plano_saude'),
            parse_money(f.get('vt_desconto')), parse_money(f.get('vr')),
            True if f.get('ativo', 'S') in ('S', 's', True) else False
        ))
        count += 1
    conn.commit()
    cur.close()
    conn.close()
    print(f"  {count} funcionarios sincronizados")
    return count

def sync_holerites():
    print("Sincronizando holerites...")
    path = os.path.join(DIR, 'dados/holerite_detalhes.json')
    if not os.path.exists(path):
        print("  Nenhum holerite encontrado")
        return 0

    with open(path) as f:
        holerites = json.load(f)

    if not isinstance(holerites, list):
        holerites = [holerites]

    conn = get_pg()
    cur = conn.cursor()
    count = 0
    for h in holerites:
        cur.execute("""
            INSERT INTO rh.holerites
                (funcionario_id, competencia, tipo, salario_base,
                 proventos, descontos, liquido, inss, irrf, fgts,
                 horas_extras, faltas, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            h.get('funcionario_id') or h.get('id'),
            h.get('competencia'), h.get('tipo', 'mensal'),
            parse_money(h.get('salario_base')),
            parse_money(h.get('proventos')),
            parse_money(h.get('descontos')),
            parse_money(h.get('liquido')),
            parse_money(h.get('inss')),
            parse_money(h.get('irrf')),
            parse_money(h.get('fgts')),
            parse_money(h.get('horas_extras')),
            parse_money(h.get('faltas')),
            h.get('status', 'pendente')
        ))
        count += 1
    conn.commit()
    cur.close()
    conn.close()
    print(f"  {count} holerites sincronizados")
    return count

def sync_all():
    antes = datetime.now()
    print(f"Sincronizando COBOL -> PostgreSQL em {antes}")
    print("="*50)

    total = 0
    total += sync_funcionarios()
    total += sync_holerites()

    depois = datetime.now()
    print(f"\nSincronizacao concluida: {total} registros em {(depois-antes).total_seconds():.1f}s")

if __name__ == '__main__':
    sync_all()
