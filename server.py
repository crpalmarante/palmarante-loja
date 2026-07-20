#!/usr/bin/env python3
import http.server
import urllib.parse
import subprocess
import json
import os
import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta

PORT = 8080
DIR = os.path.dirname(os.path.abspath(__file__))

# Fix produtos.json on startup
import re as _r
_p = os.path.join(DIR, "dados/produtos.json")
try:
    with open(_p) as _f: _c = _f.read()
    _c = _r.sub(r":\.(\d+)", r":0.\1", _c)
    with open(_p, "w") as _f: _f.write(_c)
except Exception: pass

# ---------- Banco de dados SQLite (auth) ----------
DB_PATH = os.path.join(DIR, 'dados', 'auth.db')

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript('''
        CREATE TABLE IF NOT EXISTS contas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT,
            usuario TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL,
            tipo TEXT NOT NULL DEFAULT 'funcionario',
            funcionario_id INTEGER,
            permissoes TEXT DEFAULT '',
            ativo INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS sessoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conta_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            created_at TEXT DEFAULT (datetime('now')),
            expires_at TEXT NOT NULL,
            FOREIGN KEY (conta_id) REFERENCES contas(id)
        );
    ''')
    # Seed: criar admin padrao se vazio
    c.execute('SELECT COUNT(*) FROM contas')
    if c.fetchone()[0] == 0:
        c.execute('INSERT INTO contas (nome, email, usuario, senha_hash, tipo, permissoes) VALUES (?,?,?,?,?,?)',
                  ('Administrador', 'admin@palmarante.com.br', 'admin',
                   hash_senha('admin'), 'usuario', 'admin'))
    conn.commit()
    conn.close()

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def gerar_token():
    return secrets.token_hex(32)

def db():
    return sqlite3.connect(DB_PATH)

init_db()

class POSHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if parsed.path == '/api/produtos':
            return self.api_produtos(params)
        if parsed.path == '/api/vendas':
            return self.api_vendas(params)
        if parsed.path == '/api/relatorio':
            return self.api_relatorio()
        if parsed.path == '/api/empresa':
            return self.api_empresa()
        if parsed.path == '/api/filiais':
            return self.api_filiais()
        if parsed.path == '/api/funcionarios':
            return self.api_funcionarios()
        if parsed.path == '/api/folha/config':
            return self.api_folha_config()
        if parsed.path == '/api/folha/holerites':
            return self.api_folha_holerites()
        if parsed.path == '/api/folha/holerite/detalhes':
            return self.api_folha_holerite_detalhes(params)
        if parsed.path == '/api/categorias-disciplinares':
            return self.api_categorias_disciplinares()
        if parsed.path == '/api/acoes-disciplinares':
            return self.api_acoes_disciplinares(params)
        if parsed.path == '/api/folha/calcular/inss':
            return self.api_calcular_inss(params)
        if parsed.path == '/api/folha/calcular/irrf':
            return self.api_calcular_irrf(params)
        if parsed.path == '/api/dependentes':
            return self.api_dependentes(params)
        if parsed.path == '/api/folha/ferias':
            return self.api_folha_ferias()
        if parsed.path == '/api/folha/decimos':
            return self.api_folha_decimos()
        if parsed.path == '/api/folha/rescisoes':
            return self.api_folha_rescisoes()
        if parsed.path == '/api/folha/contabilizar':
            return self.api_folha_contabilizar(params)
        if parsed.path == '/api/ponto':
            return self.api_ponto(params)
        if parsed.path == '/api/ponto/dia':
            return self.api_ponto_dia(params)
        if parsed.path == '/api/ponto/espelho':
            return self.api_ponto_espelho(params)
        if parsed.path == '/api/contabilidade/rules':
            return self.api_contabilidade_rules()
        if parsed.path == '/api/contabilidade/funcionarios':
            return self.api_contabilidade_funcionarios()
        if parsed.path == '/api/contabilidade/holerites':
            return self.api_contabilidade_holerites()
        if parsed.path == '/api/contabilidade/lancamentos':
            return self.api_contabilidade_lancamentos(params)
        if parsed.path == '/api/estruturas-salariais':
            return self.api_estruturas_salariais()
        if parsed.path == '/api/usuarios':
            return self.api_usuarios()
        if parsed.path == '/api/atributos':
            return self.api_atributos(params)
        if parsed.path == '/api/produto/imagens':
            return self.api_produto_imagens(params)
        if parsed.path == '/api/ncm':
            return self.api_ncm(params)
        if parsed.path == '/api/pedidos-pendentes':
            return self.api_pedidos_pendentes()
        if parsed.path == '/api/fiscal/config':
            return self.api_fiscal_config()
        if parsed.path == '/api/numeracao':
            return self.api_numeracao()
        if parsed.path == '/api/contingencia':
            return self.api_contingencia()
        if parsed.path == '/api/nfe-fornecedor':
            return self.api_nfe_fornecedor_listar()
        if parsed.path == '/api/fornecedores':
            return self.api_fornecedores()
        if parsed.path == '/api/faturas':
            return self.api_faturas_listar()
        if parsed.path == '/api/auth/me':
            return self.api_auth_me()
        if parsed.path == '/api/planocontas':
            return self.api_planocontas()
        if parsed.path == '/api/diarios':
            return self.api_diarios()
        if parsed.path == '/api/sped/fiscal':
            return self.api_sped_fiscal(params)
        if parsed.path == '/api/sped/pis-cofins':
            return self.api_sped_pis_cofins(params)
        if parsed.path == '/api/fiscal/relatorio':
            return self.api_fiscal_relatorio(params)
        if parsed.path == '/api/fiscal/apuracao-icms':
            return self.api_apuracao_icms(params)
        if parsed.path == '/api/fiscal/apuracao-pis-cofins':
            return self.api_apuracao_pis_cofins(params)
        if parsed.path.startswith('/api/nfce/'):
            return self.api_nfce_consulta(parsed.path)
        if parsed.path.startswith('/api/nfe/'):
            return self.api_nfe_consulta(parsed.path)
        if parsed.path.startswith('/api/nfse/'):
            return self.api_nfse_consulta(parsed.path)
        if parsed.path == '/api/licencas':
            return self.api_licencas(params)
        if parsed.path == '/api/licencas/pendentes':
            return self.api_licencas_pendentes()
        if parsed.path == '/api/directory':
            return self.api_directory()
        if parsed.path == '/api/timesheets':
            return self.api_timesheets(params)
        if parsed.path == '/api/recrutamento/vagas':
            return self.api_recrutamento_vagas()
        if parsed.path == '/api/recrutamento/candidatos':
            return self.api_recrutamento_candidatos(params)
        if parsed.path == '/api/despesas':
            return self.api_despesas(params)
        if parsed.path == '/api/despesas/pendentes':
            return self.api_despesas_pendentes()
        if parsed.path == '/api/rh/dashboard':
            return self.api_rh_dashboard()
        if parsed.path == '/api/emprestimos':
            return self.api_emprestimos(params)
        if parsed.path == '/api/emprestimos/pendentes':
            return self.api_emprestimos_pendentes()
        if parsed.path == '/api/emprestimos/ativos':
            return self.api_emprestimos_ativos()
        if parsed.path == '/api/emprestimo/parcelas':
            return self.api_emprestimo_parcelas(params)
        if parsed.path == '/api/emprestimo/saldo':
            return self.api_emprestimo_saldo(params)
        if parsed.path == '/api/workflow/definitions':
            return self.api_workflow_definitions()
        if parsed.path == '/api/workflow/history':
            return self.api_workflow_history(params)
        if parsed.path == '/' or parsed.path == '':
            self.path = '/index.html'
        return super().do_GET()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode() if length else ''

        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        params = urllib.parse.parse_qs(parsed.query)

        if path == '/api/funcionario/upload':
            return self.api_funcionario_upload(body, params)
        if path == '/api/nfe-fornecedor/importar':
            return self.api_nfe_fornecedor_importar(body)

        body_params = urllib.parse.parse_qs(body)
        # Merge query params into body params (body takes precedence)
        for k in params:
            if k not in body_params:
                body_params[k] = params[k]
        params = body_params

        if path == '/api/produto/incluir':
            return self.api_produto_incluir(params)
        if path == '/api/produto/alterar':
            return self.api_produto_alterar(params)
        if path == '/api/produto/excluir':
            return self.api_produto_excluir(params)
        if path == '/api/login':
            return self.api_login(params)
        if path == '/api/auth/login':
            return self.api_auth_login(params)
        if path == '/api/auth/register':
            return self.api_auth_register(params)
        if path == '/api/auth/logout':
            return self.api_auth_logout(params)
        if path == '/api/venda/registrar':
            return self.api_venda_registrar(params)
        if path == '/api/empresa/gravar':
            return self.api_empresa_gravar(params)
        if path == '/api/filial/incluir':
            return self.api_filial_incluir(params)
        if path == '/api/filial/alterar':
            return self.api_filial_alterar(params)
        if path == '/api/filial/excluir':
            return self.api_filial_excluir(params)
        if path == '/api/funcionario/incluir':
            return self.api_funcionario_incluir(params)
        if path == '/api/funcionario/alterar':
            return self.api_funcionario_alterar(params)
        if path == '/api/funcionario/excluir':
            return self.api_funcionario_excluir(params)
        if path == '/api/folha/config/salvar':
            return self.api_folha_config_salvar(params)
        if path == '/api/folha/holerite/gerar':
            return self.api_folha_holerite_gerar(params)
        if path == '/api/folha/holerite/pagar':
            return self.api_folha_holerite_pagar(params)
        if path == '/api/folha/holerite/excluir':
            return self.api_folha_holerite_excluir(params)
        if path == '/api/folha/holerite/detalhes/salvar':
            return self.api_folha_holerite_detalhes_salvar(params)
        if path == '/api/categoria-disciplinar/incluir':
            return self.api_categoria_disciplinar_incluir(params)
        if path == '/api/categoria-disciplinar/alterar':
            return self.api_categoria_disciplinar_alterar(params)
        if path == '/api/categoria-disciplinar/excluir':
            return self.api_categoria_disciplinar_excluir(params)
        if path == '/api/acao-disciplinar/incluir':
            return self.api_acao_disciplinar_incluir(params)
        if path == '/api/acao-disciplinar/alterar':
            return self.api_acao_disciplinar_alterar(params)
        if path == '/api/acao-disciplinar/excluir':
            return self.api_acao_disciplinar_excluir(params)
        if path == '/api/candidato/incluir':
            return self.api_candidato_incluir(params)
        if path == '/api/candidato/alterar':
            return self.api_candidato_alterar(params)
        if path == '/api/candidato/excluir':
            return self.api_candidato_excluir(params)
        if path == '/api/despesa/incluir':
            return self.api_despesa_incluir(params)
        if path == '/api/despesa/alterar':
            return self.api_despesa_alterar(params)
        if path == '/api/despesa/excluir':
            return self.api_despesa_excluir(params)
        if path == '/api/despesa/aprovar':
            return self.api_despesa_aprovar(params)
        if path == '/api/despesa/rejeitar':
            return self.api_despesa_rejeitar(params)
        if path == '/api/licenca/incluir':
            return self.api_licenca_incluir(params)
        if path == '/api/licenca/alterar':
            return self.api_licenca_alterar(params)
        if path == '/api/licenca/excluir':
            return self.api_licenca_excluir(params)
        if path == '/api/licenca/aprovar':
            return self.api_licenca_aprovar(params)
        if path == '/api/licenca/rejeitar':
            return self.api_licenca_rejeitar(params)
        if path == '/api/timesheet/incluir':
            return self.api_timesheet_incluir(params)
        if path == '/api/timesheet/alterar':
            return self.api_timesheet_alterar(params)
        if path == '/api/timesheet/excluir':
            return self.api_timesheet_excluir(params)
        if path == '/api/vaga/incluir':
            return self.api_vaga_incluir(params)
        if path == '/api/vaga/alterar':
            return self.api_vaga_alterar(params)
        if path == '/api/vaga/excluir':
            return self.api_vaga_excluir(params)
        if path == '/api/dependente/incluir':
            return self.api_dependente_incluir(params)
        if path == '/api/dependente/alterar':
            return self.api_dependente_alterar(params)
        if path == '/api/dependente/excluir':
            return self.api_dependente_excluir(params)
        if path == '/api/folha/ferias/incluir':
            return self.api_folha_ferias_incluir(params)
        if path == '/api/folha/ferias/pagar':
            return self.api_folha_ferias_pagar(params)
        if path == '/api/folha/ferias/excluir':
            return self.api_folha_ferias_excluir(params)
        if path == '/api/folha/decimo/incluir':
            return self.api_folha_decimo_incluir(params)
        if path == '/api/folha/decimo/pagar':
            return self.api_folha_decimo_pagar(params)
        if path == '/api/folha/decimo/excluir':
            return self.api_folha_decimo_excluir(params)
        if path == '/api/folha/rescisao/incluir':
            return self.api_folha_rescisao_incluir(params)
        if path == '/api/folha/rescisao/pagar':
            return self.api_folha_rescisao_pagar(params)
        if path == '/api/folha/rescisao/excluir':
            return self.api_folha_rescisao_excluir(params)
        if path == '/api/folha/contabilizar/gerar':
            return self.api_folha_contabilizar_gerar(params)
        if path == '/api/ponto/bater':
            return self.api_ponto_bater(params)
        if path == '/api/ponto/alterar':
            return self.api_ponto_alterar(params)
        if path == '/api/ponto/excluir':
            return self.api_ponto_excluir(params)
        if path == '/api/contabilidade/rules/salvar':
            return self.api_contabilidade_rules_salvar(params)
        if path == '/api/contabilidade/funcionarios/salvar':
            return self.api_contabilidade_funcionarios_salvar(params)
        if path == '/api/contabilidade/holerites/salvar':
            return self.api_contabilidade_holerites_salvar(params)
        if path == '/api/estrutura-salarial/incluir':
            return self.api_estrutura_salarial_incluir(params)
        if path == '/api/estrutura-salarial/alterar':
            return self.api_estrutura_salarial_alterar(params)
        if path == '/api/estrutura-salarial/excluir':
            return self.api_estrutura_salarial_excluir(params)
        if path == '/api/estrutura-salarial/calcular':
            return self.api_estrutura_salarial_calcular(params)
        if path == '/api/contabilidade/planocontas/incluir':
            return self.api_contabilidade_planocontas_incluir(params)
        if path == '/api/contabilidade/planocontas/alterar':
            return self.api_contabilidade_planocontas_alterar(params)
        if path == '/api/contabilidade/planocontas/excluir':
            return self.api_contabilidade_planocontas_excluir(params)
        if path == '/api/contabilidade/gerar':
            return self.api_contabilidade_gerar(params)
        if path == '/api/usuario/incluir':
            return self.api_usuario_incluir(params)
        if path == '/api/usuario/alterar':
            return self.api_usuario_alterar(params)
        if path == '/api/usuario/excluir':
            return self.api_usuario_excluir(params)
        if path == '/api/atributo/incluir':
            return self.api_atributo_incluir(params)
        if path == '/api/atributo/alterar':
            return self.api_atributo_alterar(params)
        if path == '/api/atributo/excluir':
            return self.api_atributo_excluir(params)
        if path == '/api/produto/imagem/incluir':
            return self.api_produto_imagem_incluir(params)
        if path == '/api/produto/imagem/excluir':
            return self.api_produto_imagem_excluir(params)
        if path == '/api/pedido/finalizar':
            return self.api_pedido_finalizar(params)
        if path == '/api/numeracao/gravar':
            return self.api_numeracao_gravar(params)
        if path == '/api/nfce/emitir':
            return self.api_nfce_emitir(params)
        if path == '/api/nfe/emitir':
            return self.api_nfe_emitir(params)
        if path == '/api/nfse/emitir':
            return self.api_nfse_emitir(params)
        if path == '/api/nfce/cancelar':
            return self.api_nfce_cancelar(params)
        if path == '/api/nfe/cancelar':
            return self.api_nfe_cancelar(params)
        if path == '/api/nfe/carta-correcao':
            return self.api_nfe_carta_correcao(params)
        if path == '/api/contingencia/ativar':
            return self.api_contingencia_ativar(params)
        if path == '/api/contingencia/desativar':
            return self.api_contingencia_desativar()
        if path == '/api/fatura/pagar':
            return self.api_fatura_pagar(params)
        if path == '/api/diario/lancar':
            return self.api_diario_lancar(params)
        if path == '/api/emprestimo/incluir':
            return self.api_emprestimo_incluir(params)
        if path == '/api/emprestimo/alterar':
            return self.api_emprestimo_alterar(params)
        if path == '/api/emprestimo/excluir':
            return self.api_emprestimo_excluir(params)
        if path == '/api/emprestimo/aprovar':
            return self.api_emprestimo_aprovar(params)
        if path == '/api/emprestimo/rejeitar':
            return self.api_emprestimo_rejeitar(params)
        if path == '/api/emprestimo/calcular-parcela':
            return self.api_emprestimo_calcular_parcela(params)
        if path == '/api/emprestimo/parcela/pagar':
            return self.api_emprestimo_parcela_pagar(params)
        if path == '/api/workflow/transition':
            return self.api_workflow_transition(params)
        self.send_json({'status': 'erro', 'mensagem': 'rota invalida'})

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Authorization, X-Auth-Token, Content-Type')
        self.end_headers()

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Authorization, X-Auth-Token, Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

    def api_produtos(self, params):
        try:
            with open(os.path.join(DIR, 'dados/produtos.json')) as f:
                data = json.load(f)
            out, _ = self.run_cobol('gerir_atributos', {'ACAO': 'listar'})
            if out:
                try:
                    attr_data = json.loads(out)
                    attr_map = {}
                    for a in attr_data.get('atributos', []):
                        pid = a['produto_id']
                        attr_map.setdefault(pid, []).append({
                            'nome': a['nome'], 'valor': a['valor']
                        })
                    for p in data.get('produtos', []):
                        p['atributos'] = attr_map.get(p['id'], [])
                except (json.JSONDecodeError, KeyError):
                    pass
            self.send_json(data)
        except FileNotFoundError:
            self.send_json({'status': 'erro', 'mensagem': 'Execute make dados primeiro'})

    def api_vendas(self, params):
        try:
            with open(os.path.join(DIR, 'dados/vendas.json')) as f:
                self.send_json(json.load(f))
        except FileNotFoundError:
            self.send_json({'status': 'erro', 'mensagem': 'Execute make json primeiro'})

    def api_relatorio(self):
        try:
            r = subprocess.run(['./relatorios'], capture_output=True, timeout=30, cwd=DIR)
            self.send_json({'status': 'ok', 'saida': r.stdout.decode().strip()})
        except Exception as e:
            self.send_json({'status': 'erro', 'mensagem': str(e)})

    def run_cobol(self, program, env_vars):
        env = os.environ.copy()
        env.update(env_vars)
        try:
            r = subprocess.run(
                [os.path.join(DIR, program)],
                capture_output=True, timeout=30, env=env, cwd=DIR
            )
            out = r.stdout.decode().strip()
            err = r.stderr.decode().strip()
            return out, err
        except Exception as e:
            return None, str(e)

    def api_produto_incluir(self, params):
        out, err = self.run_cobol('cadastrar_produto', {
            'ACAO': 'incluir',
            'NOME': params.get('nome', [''])[0],
            'PRECO': params.get('preco', ['0'])[0],
            'PRECO_CUSTO': params.get('preco_custo', ['0'])[0],
            'STOCK': params.get('stock', ['0'])[0],
            'MARGEM': params.get('margem', ['0'])[0],
            'CODIGO_BARRAS': params.get('codigo_barras', [''])[0],
            'CATEGORIA': params.get('categoria', [''])[0],
            'SUB_CATEGORIA': params.get('sub_categoria', [''])[0],
            'UNIDADE': params.get('unidade', ['UN'])[0],
            'NCM': params.get('ncm', [''])[0],
            'FORNECEDOR': params.get('fornecedor', [''])[0],
            'LOCALIZACAO': params.get('localizacao', [''])[0],
            'FILIAL_ID': params.get('filial_id', ['1'])[0],
            'CST': params.get('cst', [''])[0],
            'CFOP': params.get('cfop', [''])[0],
            'ICMS_ALQ': params.get('icms_alq', [''])[0],
            'SERVICO': params.get('servico', [''])[0],
            'ISS_ALQ': params.get('iss_alq', [''])[0],
            'COD_SERV_MUN': params.get('cod_serv_mun', [''])[0],
        })
        if out and out.isdigit():
            subprocess.run(['./batch_fix_produtos.py'], capture_output=True, cwd=DIR)
            self.send_json({'status': 'ok', 'id': int(out)})
        else:
            self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_produto_alterar(self, params):
        out, err = self.run_cobol('cadastrar_produto', {
            'ACAO': 'alterar',
            'ID': params.get('id', ['0'])[0],
            'NOME': params.get('nome', [''])[0],
            'PRECO': params.get('preco', [''])[0],
            'PRECO_CUSTO': params.get('preco_custo', [''])[0],
            'STOCK': params.get('stock', [''])[0],
            'MARGEM': params.get('margem', [''])[0],
            'CODIGO_BARRAS': params.get('codigo_barras', [''])[0],
            'CATEGORIA': params.get('categoria', [''])[0],
            'SUB_CATEGORIA': params.get('sub_categoria', [''])[0],
            'UNIDADE': params.get('unidade', [''])[0],
            'NCM': params.get('ncm', [''])[0],
            'FORNECEDOR': params.get('fornecedor', [''])[0],
            'LOCALIZACAO': params.get('localizacao', [''])[0],
            'FILIAL_ID': params.get('filial_id', [''])[0],
            'CST': params.get('cst', [''])[0],
            'CFOP': params.get('cfop', [''])[0],
            'ICMS_ALQ': params.get('icms_alq', [''])[0],
            'SERVICO': params.get('servico', [''])[0],
            'ISS_ALQ': params.get('iss_alq', [''])[0],
            'COD_SERV_MUN': params.get('cod_serv_mun', [''])[0],
        })
        if out == 'OK':
            subprocess.run(['./batch_fix_produtos.py'], capture_output=True, cwd=DIR)
            self.send_json({'status': 'ok'})
        else:
            self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_produto_excluir(self, params):
        out, err = self.run_cobol('cadastrar_produto', {
            'ACAO': 'excluir',
            'ID': params.get('id', ['0'])[0],
        })
        if out == 'OK':
            subprocess.run(['./batch_fix_produtos.py'], capture_output=True, cwd=DIR)
            self.send_json({'status': 'ok'})
        else:
            self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_venda_registrar(self, params):
        env_vars = {
            'CLIENTE': params.get('cliente', ['Consumidor'])[0],
            'FORMA_PG': params.get('forma_pg', [''])[0],
            'FILIAL_ID': params.get('filial_id', ['1'])[0],
            'TIPO': params.get('tipo', [''])[0],
        }
        i = 1
        while True:
            prod = params.get(f'item_{i}_prod', [''])[0]
            qtd = params.get(f'item_{i}_qtd', ['1'])[0]
            desc = params.get(f'item_{i}_desc', ['0'])[0]
            if not prod:
                break
            env_vars[f'ITEM_{i}_PROD'] = prod
            env_vars[f'ITEM_{i}_QTD'] = qtd
            env_vars[f'ITEM_{i}_DESC'] = desc
            i += 1

        out, err = self.run_cobol('registrar_venda', env_vars)
        if out and out.startswith('VENDA_OK'):
            subprocess.run(['./batch_fix_produtos.py'], capture_output=True, cwd=DIR)
            subprocess.run(['./batch_json_vendas'], capture_output=True, cwd=DIR)
            partes = out.replace('VENDA_OK:', '').split(' Total:')
            self.send_json({
                'status': 'ok',
                'id': int(partes[0]),
                'total': partes[1] if len(partes) > 1 else ''
            })
        else:
            msg = out.replace('ERRO:', '') if out else (err or 'erro desconhecido')
            self.send_json({'status': 'erro', 'mensagem': msg})

    def api_empresa(self):
        out, err = self.run_cobol('gerir_empresa', {'ACAO': 'mostrar'})
        if out:
            try:
                data = json.loads(out)
                cep_file = os.path.join(DIR, 'dados/empresa_cep.txt')
                if os.path.exists(cep_file):
                    with open(cep_file, 'r') as f:
                        data['cep'] = f.read().strip()
                self.send_json(data)
            except json.JSONDecodeError:
                self.send_json({'status': 'erro', 'mensagem': out})
        else:
            self.send_json({'status': 'erro', 'mensagem': err or 'vazio'})

    def api_empresa_gravar(self, params):
        out, err = self.run_cobol('gerir_empresa', {
            'ACAO': 'gravar',
            'NOME': params.get('nome', [''])[0],
            'CNPJ': params.get('cnpj', [''])[0],
            'ENDERECO': params.get('endereco', [''])[0],
            'TELEFONE': params.get('telefone', [''])[0],
            'EMAIL': params.get('email', [''])[0],
            'CERTIFICADO': params.get('certificado', [''])[0],
            'CERT_SENHA': params.get('cert_senha', [''])[0],
            'CNPJ_STATUS': params.get('cnpj_status', [''])[0],
            'INSCRICAO_EST': params.get('inscricao_est', [''])[0],
            'LOGO': params.get('logo', [''])[0],
            'CNAE_PRIM_CODIGO': params.get('cnae_prim_codigo', [''])[0],
            'CNAE_PRIM_DESC': params.get('cnae_prim_desc', [''])[0],
            'CNAE_SEC_CODIGOS': params.get('cnae_sec_codigos', [''])[0],
            'CNAE_SEC_DESC': params.get('cnae_sec_desc', [''])[0],
            'TIPO_FISCAL': params.get('tipo_fiscal', [''])[0],
            'CHAVE_PIX': params.get('chave_pix', [''])[0],
            'CRT': params.get('crt', ['1'])[0],
            'COD_MUNICIPIO': params.get('cod_municipio', [''])[0],
            'INSCRICAO_MUN': params.get('inscricao_mun', [''])[0],
            'UF': params.get('uf', ['43'])[0],
        })
        if out == 'OK':
            # Sync CEP
            cep = params.get('cep', [''])[0]
            if cep:
                with open(os.path.join(DIR, 'dados/empresa_cep.txt'), 'w') as f:
                    f.write(cep.strip())
            # Sync empresa.json for fiscal config
            out2, _ = self.run_cobol('gerir_empresa', {'ACAO': 'mostrar'})
            if out2:
                try:
                    with open(os.path.join(DIR, 'dados/empresa.json'), 'w') as f:
                        json.dump(json.loads(out2), f, ensure_ascii=False, indent=2)
                except Exception:
                    pass
            self.send_json({'status': 'ok'})
        else:
            self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_fiscal_config(self):
        from fiscal.config import FiscalConfig
        cfg = FiscalConfig().carregar()
        self.send_json(cfg.to_dict())

    def api_numeracao(self):
        out, err = self.run_cobol('gerir_numeracao', {'ACAO': 'mostrar'})
        if out:
            try:
                self.send_json(json.loads(out))
            except json.JSONDecodeError:
                self.send_json({'status': 'erro', 'mensagem': out})
        else:
            self.send_json({'status': 'erro', 'mensagem': err or 'vazio'})

    def api_numeracao_gravar(self, params):
        out, err = self.run_cobol('gerir_numeracao', {
            'ACAO': 'gravar',
            'AMBIENTE': params.get('ambiente', ['2'])[0],
            'SERIE_NFCE': params.get('serie_nfce', ['1'])[0],
            'PROXIMO_NUMERO_NFCE': params.get('proximo_numero_nfce', ['1'])[0],
            'SERIE_NFE': params.get('serie_nfe', ['1'])[0],
            'PROXIMO_NUMERO_NFE': params.get('proximo_numero_nfe', ['1'])[0],
        })
        if out == 'OK':
            subprocess.run(['./batch_json_numeracao'], capture_output=True, cwd=DIR)
            self.send_json({'status': 'ok'})
        else:
            self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_contingencia(self):
        from fiscal.contingencia import carregar_contingencia
        c = carregar_contingencia()
        self.send_json({'modo': c.modo, 'descricao': c.tipo_descricao(), 'ativo': c.ativo()})

    def api_contingencia_ativar(self, params):
        from fiscal.contingencia import Contingencia, salvar_contingencia
        modo = params.get('modo', ['scan'])[0]
        justificativa = params.get('justificativa', ['Contingencia ativada manualmente'])[0]
        c = Contingencia(modo=modo, justificativa=justificativa[:255])
        salvar_contingencia(c)
        self.send_json({'status': 'ok', 'modo': modo})

    def api_contingencia_desativar(self):
        from fiscal.contingencia import Contingencia, salvar_contingencia
        salvar_contingencia(Contingencia())
        self.send_json({'status': 'ok', 'modo': 'normal'})

    def api_sped_fiscal(self, params):
        from fiscal.sped import exportar_sped_fiscal
        from fiscal.config import FiscalConfig
        cfg = FiscalConfig().carregar()
        periodo_inicio = params.get('inicio', [''])[0]
        periodo_fim = params.get('fim', [''])[0]
        if not periodo_inicio or not periodo_fim:
            self.send_json({'status': 'erro', 'mensagem': 'Parametros inicio e fim obrigatorios (YYYY-MM-DD)'})
            return
        conteudo = exportar_sped_fiscal(periodo_inicio, periodo_fim, cfg.cnpj, cfg.inscricao_est, cfg.nome)
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Content-Disposition', f'attachment; filename="SPED_FISCAL_{periodo_inicio}_{periodo_fim}.txt"')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(conteudo.encode('utf-8'))

    def api_sped_pis_cofins(self, params):
        from fiscal.sped import exportar_sped_pis_cofins
        from fiscal.config import FiscalConfig
        cfg = FiscalConfig().carregar()
        periodo_inicio = params.get('inicio', [''])[0]
        periodo_fim = params.get('fim', [''])[0]
        if not periodo_inicio or not periodo_fim:
            self.send_json({'status': 'erro', 'mensagem': 'Parametros inicio e fim obrigatorios (YYYY-MM-DD)'})
            return
        conteudo = exportar_sped_pis_cofins(periodo_inicio, periodo_fim, cfg.cnpj)
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Content-Disposition', f'attachment; filename="SPED_PIS_COFINS_{periodo_inicio}_{periodo_fim}.txt"')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(conteudo.encode('utf-8'))

    def api_fiscal_relatorio(self, params):
        from fiscal.relatorio_fiscal import apurar_completo
        inicio = params.get('inicio', [''])[0]
        fim = params.get('fim', [''])[0]
        if not inicio or not fim:
            hoje = datetime.now().strftime('%Y-%m-%d')
            inicio = (datetime.now().replace(day=1)).strftime('%Y-%m-%d')
            fim = hoje
        resultado = apurar_completo(inicio, fim)
        self.send_json({'status': 'ok', 'relatorio': resultado})

    def api_apuracao_icms(self, params):
        from fiscal.relatorio_fiscal import apurar_icms
        inicio = params.get('inicio', [''])[0]
        fim = params.get('fim', [''])[0]
        if not inicio or not fim:
            hoje = datetime.now().strftime('%Y-%m-%d')
            inicio = (datetime.now().replace(day=1)).strftime('%Y-%m-%d')
            fim = hoje
        resultado = apurar_icms(inicio, fim)
        self.send_json({'status': 'ok', 'apuracao': resultado})

    def api_apuracao_pis_cofins(self, params):
        from fiscal.relatorio_fiscal import apurar_pis_cofins
        inicio = params.get('inicio', [''])[0]
        fim = params.get('fim', [''])[0]
        regime = params.get('regime', ['cumulativo'])[0]
        if not inicio or not fim:
            hoje = datetime.now().strftime('%Y-%m-%d')
            inicio = (datetime.now().replace(day=1)).strftime('%Y-%m-%d')
            fim = hoje
        resultado = apurar_pis_cofins(inicio, fim, regime)
        self.send_json({'status': 'ok', 'apuracao': resultado})

    def _emitir_documento(self, venda_id, modelo='nfce'):
        with open(os.path.join(DIR, 'dados/vendas.json')) as f:
            vendas_data = json.load(f)
        venda = None
        for v in vendas_data.get('vendas', []):
            if str(v.get('id')) == venda_id:
                venda = v
                break
        if not venda:
            raise ValueError('Venda nao encontrada')

        itens = venda.get('itens', [])
        with open(os.path.join(DIR, 'dados/produtos.json')) as f:
            prods = json.load(f)
        prod_map = {str(p['id']): p for p in prods.get('produtos', [])}

        for item in itens:
            pid = str(item.get('produto_id', item.get('prod_id', '')))
            prod = prod_map.get(pid)
            if prod:
                item['ncm'] = prod.get('ncm', '')
                item['cst'] = prod.get('cst', '400')
                item['cfop'] = prod.get('cfop', '5102')
                item['icms_alq'] = prod.get('icms_alq', 0)

        from fiscal.config import FiscalConfig
        cfg = FiscalConfig().carregar()

        is_nfe = modelo == 'nfe'
        acao = 'avancar-nfe' if is_nfe else 'avancar-nfce'
        out, _ = self.run_cobol('gerir_numeracao', {'ACAO': acao})
        if not out or not out.strip().isdigit():
            raise ValueError(f'Erro ao obter numero {modelo.upper()}')
        numero = int(out.strip())

        if is_nfe:
            from fiscal.nfe import NFeBuilder
            builder = NFeBuilder(cfg)
            xml_str, chave = builder.montar_xml(venda, itens, numero,
                cfg.serie_nfe, cfg.ambiente)
        else:
            from fiscal.nfce import NFCeBuilder
            builder = NFCeBuilder(cfg)
            xml_str, chave = builder.montar_xml(venda, itens, numero,
                cfg.serie_nfce, cfg.ambiente)

        if cfg.certificado:
            from fiscal.assinatura import assinar_xml
            xml_assinado = assinar_xml(xml_str, cfg.certificado, cfg.cert_senha)
        else:
            xml_assinado = xml_str

        from fiscal.contingencia import carregar_contingencia
        cont = carregar_contingencia()

        protocolo = ''
        c_stat = '999'
        x_motivo = 'Transmissao nao realizada'
        status = 'PENDENTE'

        if cont.ativo():
            status = 'CONTINGENCIA'
            protocolo = f'CONT-{datetime.now().strftime("%Y%m%d%H%M%S")}'
            c_stat = 'CONT'
            x_motivo = f'Em contingencia: {cont.tipo_descricao()}'
        else:
            try:
                from fiscal.transmissao import transmitir_lote, extrair_protocolo
                uf = cfg.uf if hasattr(cfg, 'uf') and cfg.uf else 43
                amb = cfg.ambiente
                cert = cfg.certificado if cfg.certificado else None
                cert_senha = cfg.cert_senha
                resposta = transmitir_lote(xml_assinado, modelo, uf, amb, cert, cert_senha)
                prot = extrair_protocolo(resposta)
                if prot:
                    c_stat = prot.get('cStat', '999')
                    x_motivo = prot.get('xMotivo', '')
                    protocolo = prot.get('nProt', '')
                    if c_stat in ('100', '150', '301'):
                        status = 'AUTORIZADO'
                    elif c_stat in ('110', '204', '205', '206', '207', '208', '209'):
                        status = 'DENEGADO'
                    else:
                        status = 'RECEBIDO'
            except Exception as e:
                x_motivo = str(e)
                status = 'ERRO_TRANSMISSAO'

        doc_reg = {
            'venda_id': venda_id,
            'numero': numero,
            'serie': cfg.serie_nfe if is_nfe else cfg.serie_nfce,
            'chave': chave,
            'ambiente': cfg.ambiente,
            'status': status,
            'protocolo': protocolo,
            'cStat': c_stat,
            'xMotivo': x_motivo,
            'xml': xml_assinado,
            'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }

        storage_key = 'nfe' if is_nfe else 'nfce'
        doc_path = os.path.join(DIR, f'dados/{storage_key}.json')
        try:
            with open(doc_path) as f:
                doc_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            doc_data = {storage_key: []}
        doc_data[storage_key].append(doc_reg)
        with open(doc_path, 'w') as f:
            json.dump(doc_data, f, ensure_ascii=False, indent=2)

        # also generate PDF
        pdf_path = os.path.join(DIR, f'dados/danfe_{storage_key}_{venda_id}.pdf')
        try:
            if is_nfe:
                from fiscal.danfe import danfe_nfe_html, danfe_to_pdf
                html = danfe_nfe_html(doc_reg, venda, itens, cfg)
            else:
                from fiscal.danfe import danfe_nfce_html, danfe_to_pdf
                html = danfe_nfce_html(doc_reg, venda, itens, cfg)
            danfe_to_pdf(html, pdf_path)
        except Exception:
            pass

        return doc_reg, status, chave, protocolo

    def api_nfce_emitir(self, params):
        venda_id = params.get('venda_id', [''])[0]
        if not venda_id:
            self.send_json({'status': 'erro', 'mensagem': 'venda_id obrigatorio'})
            return
        try:
            doc_reg, status, chave, protocolo = self._emitir_documento(venda_id, 'nfce')
            self.send_json({
                'status': 'ok',
                'chave': chave,
                'numero': doc_reg['numero'],
                'serie': doc_reg['serie'],
                'protocolo': protocolo,
                'cStat': doc_reg.get('cStat', ''),
                'xMotivo': doc_reg.get('xMotivo', ''),
                'situacao': status,
            })
        except Exception as e:
            self.send_json({'status': 'erro', 'mensagem': str(e)})

    def api_nfe_emitir(self, params):
        venda_id = params.get('venda_id', [''])[0]
        if not venda_id:
            self.send_json({'status': 'erro', 'mensagem': 'venda_id obrigatorio'})
            return
        try:
            doc_reg, status, chave, protocolo = self._emitir_documento(venda_id, 'nfe')
            self.send_json({
                'status': 'ok',
                'chave': chave,
                'numero': doc_reg['numero'],
                'serie': doc_reg['serie'],
                'protocolo': protocolo,
                'cStat': doc_reg.get('cStat', ''),
                'xMotivo': doc_reg.get('xMotivo', ''),
                'situacao': status,
            })
        except Exception as e:
            self.send_json({'status': 'erro', 'mensagem': str(e)})

    def api_nfce_cancelar(self, params):
        venda_id = params.get('venda_id', [''])[0]
        justificativa = params.get('justificativa', ['Teste de cancelamento'])[0]
        if not venda_id:
            self.send_json({'status': 'erro', 'mensagem': 'venda_id obrigatorio'})
            return
        try:
            nfce_path = os.path.join(DIR, 'dados/nfce.json')
            with open(nfce_path) as f:
                nfce_data = json.load(f)
            reg = None
            for r in nfce_data.get('nfce', []):
                if str(r.get('venda_id')) == venda_id:
                    reg = r
                    break
            if not reg:
                self.send_json({'status': 'erro', 'mensagem': 'NFC-e nao encontrada'})
                return

            from fiscal.evento import montar_xml_cancelamento, transmitir_evento, extrair_resultado_evento
            from fiscal.config import FiscalConfig
            cfg = FiscalConfig().carregar()

            uf = cfg.uf if hasattr(cfg, 'uf') and cfg.uf else 43
            xml_evento = montar_xml_cancelamento(
                reg['chave'], reg['protocolo'], justificativa,
                cfg.ambiente, uf
            )
            if cfg.certificado:
                from fiscal.assinatura import assinar_xml
                xml_assinado = assinar_xml(xml_evento, cfg.certificado)
            else:
                xml_assinado = xml_evento

            resp = transmitir_evento(xml_assinado, reg['chave'], 'nfce', uf, cfg.ambiente, cfg.certificado)
            resultado = extrair_resultado_evento(resp)

            if resultado.get('cStat') in ('135', '155'):
                reg['status'] = 'CANCELADO'
                reg['cancelamento'] = {
                    'justificativa': justificativa[:255],
                    'protocolo': resultado.get('nProt', ''),
                    'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                }
                with open(nfce_path, 'w') as f:
                    json.dump(nfce_data, f, ensure_ascii=False, indent=2)
                self.send_json({'status': 'ok', 'protocolo': resultado.get('nProt', '')})
            else:
                self.send_json({'status': 'erro', 'mensagem': resultado.get('xMotivo', 'Cancelamento nao aprovado')})
        except Exception as e:
            self.send_json({'status': 'erro', 'mensagem': str(e)})

    def api_nfe_cancelar(self, params):
        venda_id = params.get('venda_id', [''])[0]
        justificativa = params.get('justificativa', ['Teste de cancelamento'])[0]
        if not venda_id:
            self.send_json({'status': 'erro', 'mensagem': 'venda_id obrigatorio'})
            return
        try:
            nfe_path = os.path.join(DIR, 'dados/nfe.json')
            with open(nfe_path) as f:
                nfe_data = json.load(f)
            reg = None
            for r in nfe_data.get('nfe', []):
                if str(r.get('venda_id')) == venda_id:
                    reg = r
                    break
            if not reg:
                self.send_json({'status': 'erro', 'mensagem': 'NF-e nao encontrada'})
                return

            from fiscal.evento import montar_xml_cancelamento, transmitir_evento, extrair_resultado_evento
            from fiscal.config import FiscalConfig
            cfg = FiscalConfig().carregar()

            uf = cfg.uf if hasattr(cfg, 'uf') and cfg.uf else 43
            xml_evento = montar_xml_cancelamento(
                reg['chave'], reg['protocolo'], justificativa,
                cfg.ambiente, uf
            )
            if cfg.certificado:
                from fiscal.assinatura import assinar_xml
                xml_assinado = assinar_xml(xml_evento, cfg.certificado)
            else:
                xml_assinado = xml_evento

            resp = transmitir_evento(xml_assinado, reg['chave'], 'nfe', uf, cfg.ambiente, cfg.certificado)
            resultado = extrair_resultado_evento(resp)

            if resultado.get('cStat') in ('135', '155'):
                reg['status'] = 'CANCELADO'
                reg['cancelamento'] = {
                    'justificativa': justificativa[:255],
                    'protocolo': resultado.get('nProt', ''),
                    'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                }
                with open(nfe_path, 'w') as f:
                    json.dump(nfe_data, f, ensure_ascii=False, indent=2)
                self.send_json({'status': 'ok', 'protocolo': resultado.get('nProt', '')})
            else:
                self.send_json({'status': 'erro', 'mensagem': resultado.get('xMotivo', 'Cancelamento nao aprovado')})
        except Exception as e:
            self.send_json({'status': 'erro', 'mensagem': str(e)})

    def api_nfe_carta_correcao(self, params):
        chave = params.get('chave', [''])[0]
        correcao = params.get('correcao', [''])[0]
        if not chave or not correcao:
            self.send_json({'status': 'erro', 'mensagem': 'chave e correcao obrigatorios'})
            return
        try:
            from fiscal.evento import montar_xml_carta_correcao, transmitir_evento, extrair_resultado_evento
            from fiscal.config import FiscalConfig
            cfg = FiscalConfig().carregar()

            uf = cfg.uf if hasattr(cfg, 'uf') and cfg.uf else 43
            sequencia = 1
            xml_evento = montar_xml_carta_correcao(
                chave, sequencia, correcao, cfg.ambiente, uf
            )
            if cfg.certificado:
                from fiscal.assinatura import assinar_xml
                xml_assinado = assinar_xml(xml_evento, cfg.certificado)
            else:
                xml_assinado = xml_evento

            resp = transmitir_evento(xml_assinado, chave, 'nfe', 43, cfg.ambiente, cfg.certificado)
            resultado = extrair_resultado_evento(resp)

            if resultado.get('cStat') in ('135', '155'):
                self.send_json({'status': 'ok', 'protocolo': resultado.get('nProt', '')})
            else:
                self.send_json({'status': 'erro', 'mensagem': resultado.get('xMotivo', 'CC-e nao aprovada')})
        except Exception as e:
            self.send_json({'status': 'erro', 'mensagem': str(e)})

    def api_nfce_consulta(self, path):
        parts = path.strip('/').split('/')
        venda_id = parts[2] if len(parts) >= 3 else ''
        is_danfe = 'danfe' in path
        is_pdf = 'pdf' in path
        try:
            nfce_path = os.path.join(DIR, 'dados/nfce.json')
            with open(nfce_path) as f:
                data = json.load(f)
            for reg in data.get('nfce', []):
                if str(reg.get('venda_id')) == venda_id:
                    if is_pdf:
                        return self.api_danfe_pdf(reg, 'nfce')
                    if is_danfe:
                        return self.api_danfe_nfce(reg)
                    self.send_json({'status': 'ok', 'nfce': reg})
                    return
            self.send_json({'status': 'erro', 'mensagem': 'NFC-e nao encontrada'})
        except FileNotFoundError:
            self.send_json({'status': 'erro', 'mensagem': 'Nenhuma NFC-e emitida'})

    def api_nfe_consulta(self, path):
        parts = path.strip('/').split('/')
        venda_id = parts[2] if len(parts) >= 3 else ''
        is_danfe = 'danfe' in path
        is_pdf = 'pdf' in path
        try:
            nfe_path = os.path.join(DIR, 'dados/nfe.json')
            with open(nfe_path) as f:
                data = json.load(f)
            for reg in data.get('nfe', []):
                if str(reg.get('venda_id')) == venda_id:
                    if is_pdf:
                        return self.api_danfe_pdf(reg, 'nfe')
                    if is_danfe:
                        return self.api_danfe_nfe(reg)
                    self.send_json({'status': 'ok', 'nfe': reg})
                    return
            self.send_json({'status': 'erro', 'mensagem': 'NF-e nao encontrada'})
        except FileNotFoundError:
            self.send_json({'status': 'erro', 'mensagem': 'Nenhuma NF-e emitida'})

    def api_danfe_pdf(self, reg, modelo='nfce'):
        pdf_path = os.path.join(DIR, f'dados/danfe_{modelo}_{reg.get("venda_id","")}.pdf')
        if os.path.exists(pdf_path):
            self.send_response(200)
            self.send_header('Content-Type', 'application/pdf')
            self.send_header('Content-Disposition', f'inline; filename="danfe_{modelo}_{reg.get("venda_id","")}.pdf"')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            with open(pdf_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            # generate on the fly
            self.api_danfe_nfce(reg) if modelo == 'nfce' else self.api_danfe_nfe(reg)

    def api_danfe_nfce(self, nfce_reg):
        venda_id = nfce_reg.get('venda_id', '')
        try:
            with open(os.path.join(DIR, 'dados/vendas.json')) as f:
                vendas_data = json.load(f)
            venda = None
            for v in vendas_data.get('vendas', []):
                if str(v.get('id')) == venda_id:
                    venda = v
                    break
            if not venda:
                return self.send_json({'status': 'erro', 'mensagem': 'Venda nao encontrada'})
            itens = venda.get('itens', [])
            from fiscal.config import FiscalConfig
            cfg = FiscalConfig().carregar()
            from fiscal.danfe import danfe_nfce_html
            html = danfe_nfce_html(nfce_reg, venda, itens, cfg)
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        except Exception as e:
            self.send_json({'status': 'erro', 'mensagem': str(e)})

    def api_danfe_nfe(self, nfe_reg):
        venda_id = nfe_reg.get('venda_id', '')
        try:
            with open(os.path.join(DIR, 'dados/vendas.json')) as f:
                vendas_data = json.load(f)
            venda = None
            for v in vendas_data.get('vendas', []):
                if str(v.get('id')) == venda_id:
                    venda = v
                    break
            if not venda:
                return self.send_json({'status': 'erro', 'mensagem': 'Venda nao encontrada'})
            itens = venda.get('itens', [])
            from fiscal.config import FiscalConfig
            cfg = FiscalConfig().carregar()
            from fiscal.danfe import danfe_nfe_html
            html = danfe_nfe_html(nfe_reg, venda, itens, cfg)
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        except Exception as e:
            self.send_json({'status': 'erro', 'mensagem': str(e)})

    def api_nfse_emitir(self, params):
        venda_id = params.get('venda_id', [''])[0]
        if not venda_id:
            self.send_json({'status': 'erro', 'mensagem': 'venda_id obrigatorio'})
            return
        try:
            with open(os.path.join(DIR, 'dados/vendas.json')) as f:
                vendas_data = json.load(f)
            venda = None
            for v in vendas_data.get('vendas', []):
                if str(v.get('id')) == venda_id:
                    venda = v
                    break
            if not venda:
                self.send_json({'status': 'erro', 'mensagem': 'Venda nao encontrada'})
                return
            itens = venda.get('itens', [])

            with open(os.path.join(DIR, 'dados/produtos.json')) as f:
                prods = json.load(f)
            prod_map = {str(p['id']): p for p in prods.get('produtos', [])}
            for item in itens:
                prod = prod_map.get(str(item.get('prod_id', '')))
                if prod:
                    item['iss_alq'] = prod.get('iss_alq', 0)
                    item['cod_serv_mun'] = prod.get('cod_serv_mun', '')

            from fiscal.config import FiscalConfig
            cfg = FiscalConfig().carregar()

            rps_num = '1'
            from fiscal.nfse import NfseBuilder
            builder = NfseBuilder(cfg)
            xml_str = builder.montar_xml(venda, itens, rps_num)

            if cfg.certificado:
                from fiscal.assinatura import assinar_xml
                xml_assinado = assinar_xml(xml_str, cfg.certificado)
            else:
                xml_assinado = xml_str

            nfse_reg = {
                'venda_id': venda_id,
                'rps_numero': rps_num,
                'status': 'AUTORIZADO',
                'xml': xml_assinado,
                'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            nfse_path = os.path.join(DIR, 'dados/nfse.json')
            try:
                with open(nfse_path) as f:
                    nfse_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                nfse_data = {'nfse': []}
            nfse_data['nfse'].append(nfse_reg)
            with open(nfse_path, 'w') as f:
                json.dump(nfse_data, f, ensure_ascii=False, indent=2)

            self.send_json({'status': 'ok', 'rps_numero': rps_num})
        except Exception as e:
            self.send_json({'status': 'erro', 'mensagem': str(e)})

    def api_nfse_consulta(self, path):
        parts = path.strip('/').split('/')
        venda_id = parts[2] if len(parts) >= 3 else ''
        try:
            nfse_path = os.path.join(DIR, 'dados/nfse.json')
            with open(nfse_path) as f:
                data = json.load(f)
            for reg in data.get('nfse', []):
                if str(reg.get('venda_id')) == venda_id:
                    self.send_json({'status': 'ok', 'nfse': reg})
                    return
            self.send_json({'status': 'erro', 'mensagem': 'NFS-e nao encontrada'})
        except FileNotFoundError:
            self.send_json({'status': 'erro', 'mensagem': 'Nenhuma NFS-e emitida'})

    def api_filiais(self):
        out, err = self.run_cobol('gerir_filiais', {'ACAO': 'listar'})
        if out:
            try:
                self.send_json(json.loads(out))
            except json.JSONDecodeError:
                self.send_json({'status': 'erro', 'mensagem': out})
        else:
            self.send_json({'status': 'erro', 'mensagem': err or 'vazio'})

    def api_filial_incluir(self, params):
        out, err = self.run_cobol('gerir_filiais', {
            'ACAO': 'incluir',
            'NOME': params.get('nome', [''])[0],
            'ENDERECO': params.get('endereco', [''])[0],
            'RESPONSAVEL': params.get('responsavel', [''])[0],
        })
        if out and out.isdigit():
            self.send_json({'status': 'ok', 'id': int(out)})
        else:
            self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_filial_alterar(self, params):
        out, err = self.run_cobol('gerir_filiais', {
            'ACAO': 'alterar',
            'ID': params.get('id', ['0'])[0],
            'NOME': params.get('nome', [''])[0],
            'ENDERECO': params.get('endereco', [''])[0],
            'RESPONSAVEL': params.get('responsavel', [''])[0],
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro',
                        'mensagem': out if out != 'OK' else ''})

    def api_filial_excluir(self, params):
        out, err = self.run_cobol('gerir_filiais', {
            'ACAO': 'excluir',
            'ID': params.get('id', ['0'])[0],
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro',
                        'mensagem': out if out != 'OK' else ''})

    def api_login(self, params):
        usuario = params.get('usuario', [''])[0]
        senha = params.get('senha', [''])[0]
        out, err = self.run_cobol('gerir_funcionarios', {
            'ACAO': 'login', 'USUARIO': usuario, 'SENHA': senha
        })
        if out:
            try:
                data = json.loads(out)
                if data.get('status') == 'ok':
                    return self.send_json(data)
            except json.JSONDecodeError:
                pass
        out, err = self.run_cobol('gerir_usuarios', {
            'ACAO': 'login', 'USUARIO': usuario, 'SENHA': senha
        })
        if out:
            try:
                data = json.loads(out)
                if data.get('status') == 'ok':
                    data['permissoes'] = 'admin'
                    return self.send_json(data)
            except json.JSONDecodeError:
                pass
        self.send_json({'status': 'erro', 'mensagem': 'usuario ou senha incorretos'})

    # ---------- Auth via SQLite ----------
    def _get_conta_por_token(self):
        auth = self.headers.get('Authorization', '')
        if auth.startswith('Bearer '):
            token = auth[7:]
        else:
            token = self.headers.get('X-Auth-Token', '')
        if not token:
            return None
        conn = db()
        c = conn.cursor()
        c.execute('SELECT c.* FROM contas c JOIN sessoes s ON c.id=s.conta_id '
                  'WHERE s.token=? AND s.expires_at > datetime("now")', (token,))
        row = c.fetchone()
        conn.close()
        if row:
            return {
                'id': row[0], 'nome': row[1], 'email': row[2],
                'usuario': row[3], 'tipo': row[5],
                'funcionario_id': row[6], 'permissoes': row[7]
            }
        return None

    def api_auth_login(self, params):
        usuario = params.get('usuario', [''])[0]
        senha = params.get('senha', [''])[0]
        if not usuario or not senha:
            return self.send_json({'status': 'erro', 'mensagem': 'usuario e senha obrigatorios'})
        conn = db()
        c = conn.cursor()
        c.execute('SELECT * FROM contas WHERE usuario=? AND ativo=1', (usuario,))
        row = c.fetchone()
        if row and row[4] == hash_senha(senha):
            token = gerar_token()
            exp = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
            c.execute('INSERT INTO sessoes (conta_id, token, expires_at) VALUES (?,?,?)',
                      (row[0], token, exp))
            conn.commit()
            conn.close()
            return self.send_json({
                'status': 'ok', 'token': token,
                'id': row[0], 'nome': row[1], 'usuario': row[3],
                'tipo': row[5], 'funcionario_id': row[6],
                'permissoes': row[7]
            })
        conn.close()
        # Fallback: tentar login via COBOL (legado)
        return self.api_login(params)

    def api_auth_register(self, params):
        nome = params.get('nome', [''])[0]
        usuario = params.get('usuario', [''])[0]
        senha = params.get('senha', [''])[0]
        email = params.get('email', [''])[0]
        tipo = params.get('tipo', ['funcionario'])[0]
        if not nome or not usuario or not senha:
            return self.send_json({'status': 'erro', 'mensagem': 'nome, usuario e senha obrigatorios'})
        if len(senha) < 4:
            return self.send_json({'status': 'erro', 'mensagem': 'senha deve ter no minimo 4 caracteres'})
        conn = db()
        c = conn.cursor()
        try:
            c.execute('INSERT INTO contas (nome, email, usuario, senha_hash, tipo) VALUES (?,?,?,?,?)',
                      (nome, email, usuario, hash_senha(senha), tipo))
            conn.commit()
            conta_id = c.lastrowid
            conn.close()
            return self.send_json({'status': 'ok', 'id': conta_id, 'mensagem': 'conta criada com sucesso'})
        except sqlite3.IntegrityError:
            conn.close()
            return self.send_json({'status': 'erro', 'mensagem': 'usuario ja existe'})

    def api_auth_logout(self, params):
        token = self.headers.get('X-Auth-Token', '') or self.headers.get('Authorization', '').replace('Bearer ', '')
        if token:
            conn = db()
            conn.execute('DELETE FROM sessoes WHERE token=?', (token,))
            conn.commit()
            conn.close()
        return self.send_json({'status': 'ok'})

    def api_auth_me(self):
        conta = self._get_conta_por_token()
        if conta:
            return self.send_json({'status': 'ok', 'conta': conta})
        return self.send_json({'status': 'erro', 'mensagem': 'nao autenticado'}, 401)

    def api_funcionarios(self):
        out, err = self.run_cobol('gerir_funcionarios', {'ACAO': 'listar'})
        if out:
            try:
                self.send_json(json.loads(out))
            except json.JSONDecodeError:
                self.send_json({'status': 'erro', 'mensagem': out})
        else:
            self.send_json({'status': 'erro', 'mensagem': err or 'vazio'})

    def api_funcionario_incluir(self, params):
        out, err = self.run_cobol('gerir_funcionarios', {
            'ACAO': 'incluir',
            'NOME': params.get('nome', [''])[0],
            'USUARIO': params.get('usuario', [''])[0],
            'SENHA': params.get('senha', [''])[0],
            'PERMISSOES': params.get('permissoes', [''])[0],
            'CPF': params.get('cpf', [''])[0],
            'RG': params.get('rg', [''])[0],
            'DATA_NASC': params.get('data_nasc', [''])[0],
            'CELULAR': params.get('celular', [''])[0],
            'EMAIL': params.get('email', [''])[0],
            'ENDERECO': params.get('endereco', [''])[0],
            'DATA_ADM': params.get('data_adm', [''])[0],
            'DATA_DEM': params.get('data_dem', [''])[0],
            'SALARIO': params.get('salario', [''])[0],
            'FILIAL_ID': params.get('filial_id', [''])[0],
            'TRAB_SAB': params.get('trab_sab', [''])[0],
            'TRAB_DOM': params.get('trab_dom', [''])[0],
            'SEG_ENT': params.get('seg_ent', [''])[0],
            'SEG_ALM': params.get('seg_alm', [''])[0],
            'SEG_SAI': params.get('seg_sai', [''])[0],
            'TER_ENT': params.get('ter_ent', [''])[0],
            'TER_ALM': params.get('ter_alm', [''])[0],
            'TER_SAI': params.get('ter_sai', [''])[0],
            'QUA_ENT': params.get('qua_ent', [''])[0],
            'QUA_ALM': params.get('qua_alm', [''])[0],
            'QUA_SAI': params.get('qua_sai', [''])[0],
            'QUI_ENT': params.get('qui_ent', [''])[0],
            'QUI_ALM': params.get('qui_alm', [''])[0],
            'QUI_SAI': params.get('qui_sai', [''])[0],
            'SEX_ENT': params.get('sex_ent', [''])[0],
            'SEX_ALM': params.get('sex_alm', [''])[0],
            'SEX_SAI': params.get('sex_sai', [''])[0],
            'SAB_ENT': params.get('sab_ent', [''])[0],
            'SAB_SAI': params.get('sab_sai', [''])[0],
            'DOM_ENT': params.get('dom_ent', [''])[0],
            'DOM_SAI': params.get('dom_sai', [''])[0],
            'FOTO': params.get('foto', [''])[0],
            'CONTATO_EMERG_NOME': params.get('contato_emerg_nome', [''])[0],
            'CONTATO_EMERG_TEL': params.get('contato_emerg_tel', [''])[0],
            'CURRICULO': params.get('curriculo', [''])[0],
            'TIPO_SANGUINEO': params.get('tipo_sanguineo', [''])[0],
            'EMAIL_PARTICULAR': params.get('email_particular', [''])[0],
            'TEL_COMERCIAL': params.get('tel_comercial', [''])[0],
            'BANCO': params.get('banco', [''])[0],
            'AGENCIA': params.get('agencia', [''])[0],
            'CONTA': params.get('conta', [''])[0],
            'CONTA_DIGITO': params.get('conta_digito', [''])[0],
            'CONTA_TIPO': params.get('conta_tipo', [''])[0],
            'PIX': params.get('pix', [''])[0],
            'PIS': params.get('pis', [''])[0],
            'CTPS': params.get('ctps', [''])[0],
            'CTPS_SERIE': params.get('ctps_serie', [''])[0],
            'CTPS_UF': params.get('ctps_uf', [''])[0],
            'CBO': params.get('cbo', [''])[0],
            'GRAU_INSTRUCAO': params.get('grau_instrucao', [''])[0],
            'TIPO_CONTRATO': params.get('tipo_contrato', [''])[0],
            'MOTIVO_DESLIG': params.get('motivo_deslig', [''])[0],
            'VT_DESCONTO': params.get('vt_desconto', [''])[0],
            'VT_DIAS': params.get('vt_dias', ['0'])[0],
            'VR': params.get('vr', ['0'])[0],
            'PLANO_SAUDE': params.get('plano_saude', [''])[0],
            'PLANO_SAUDE_VALOR': params.get('plano_saude_valor', ['0'])[0],
        })
        if out and out.isdigit():
            self.send_json({'status': 'ok', 'id': int(out)})
        else:
            self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_funcionario_alterar(self, params):
        out, err = self.run_cobol('gerir_funcionarios', {
            'ACAO': 'alterar',
            'ID': params.get('id', ['0'])[0],
            'NOME': params.get('nome', [''])[0],
            'USUARIO': params.get('usuario', [''])[0],
            'SENHA': params.get('senha', [''])[0],
            'PERMISSOES': params.get('permissoes', [''])[0],
            'CPF': params.get('cpf', [''])[0],
            'RG': params.get('rg', [''])[0],
            'DATA_NASC': params.get('data_nasc', [''])[0],
            'CELULAR': params.get('celular', [''])[0],
            'EMAIL': params.get('email', [''])[0],
            'ENDERECO': params.get('endereco', [''])[0],
            'DATA_ADM': params.get('data_adm', [''])[0],
            'DATA_DEM': params.get('data_dem', [''])[0],
            'SALARIO': params.get('salario', [''])[0],
            'FILIAL_ID': params.get('filial_id', [''])[0],
            'TRAB_SAB': params.get('trab_sab', [''])[0],
            'TRAB_DOM': params.get('trab_dom', [''])[0],
            'SEG_ENT': params.get('seg_ent', [''])[0],
            'SEG_ALM': params.get('seg_alm', [''])[0],
            'SEG_SAI': params.get('seg_sai', [''])[0],
            'TER_ENT': params.get('ter_ent', [''])[0],
            'TER_ALM': params.get('ter_alm', [''])[0],
            'TER_SAI': params.get('ter_sai', [''])[0],
            'QUA_ENT': params.get('qua_ent', [''])[0],
            'QUA_ALM': params.get('qua_alm', [''])[0],
            'QUA_SAI': params.get('qua_sai', [''])[0],
            'QUI_ENT': params.get('qui_ent', [''])[0],
            'QUI_ALM': params.get('qui_alm', [''])[0],
            'QUI_SAI': params.get('qui_sai', [''])[0],
            'SEX_ENT': params.get('sex_ent', [''])[0],
            'SEX_ALM': params.get('sex_alm', [''])[0],
            'SEX_SAI': params.get('sex_sai', [''])[0],
            'SAB_ENT': params.get('sab_ent', [''])[0],
            'SAB_SAI': params.get('sab_sai', [''])[0],
            'DOM_ENT': params.get('dom_ent', [''])[0],
            'DOM_SAI': params.get('dom_sai', [''])[0],
            'FOTO': params.get('foto', [''])[0],
            'CONTATO_EMERG_NOME': params.get('contato_emerg_nome', [''])[0],
            'CONTATO_EMERG_TEL': params.get('contato_emerg_tel', [''])[0],
            'CURRICULO': params.get('curriculo', [''])[0],
            'TIPO_SANGUINEO': params.get('tipo_sanguineo', [''])[0],
            'EMAIL_PARTICULAR': params.get('email_particular', [''])[0],
            'TEL_COMERCIAL': params.get('tel_comercial', [''])[0],
            'BANCO': params.get('banco', [''])[0],
            'AGENCIA': params.get('agencia', [''])[0],
            'CONTA': params.get('conta', [''])[0],
            'CONTA_DIGITO': params.get('conta_digito', [''])[0],
            'CONTA_TIPO': params.get('conta_tipo', [''])[0],
            'PIX': params.get('pix', [''])[0],
            'PIS': params.get('pis', [''])[0],
            'CTPS': params.get('ctps', [''])[0],
            'CTPS_SERIE': params.get('ctps_serie', [''])[0],
            'CTPS_UF': params.get('ctps_uf', [''])[0],
            'CBO': params.get('cbo', [''])[0],
            'GRAU_INSTRUCAO': params.get('grau_instrucao', [''])[0],
            'TIPO_CONTRATO': params.get('tipo_contrato', [''])[0],
            'MOTIVO_DESLIG': params.get('motivo_deslig', [''])[0],
            'VT_DESCONTO': params.get('vt_desconto', [''])[0],
            'VT_DIAS': params.get('vt_dias', ['0'])[0],
            'VR': params.get('vr', ['0'])[0],
            'PLANO_SAUDE': params.get('plano_saude', [''])[0],
            'PLANO_SAUDE_VALOR': params.get('plano_saude_valor', ['0'])[0],
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro',
                        'mensagem': out if out != 'OK' else ''})

    def api_funcionario_excluir(self, params):
        out, err = self.run_cobol('gerir_funcionarios', {
            'ACAO': 'excluir',
            'ID': params.get('id', ['0'])[0],
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro',
                        'mensagem': out if out != 'OK' else ''})

    def api_funcionario_upload(self, body, params):
        import base64, uuid
        try: data = json.loads(body)
        except: data = {}
        file_type = data.get('type', 'foto')
        file_data = data.get('data', '')
        ext = data.get('ext', 'jpg')
        if not file_data:
            self.send_json({'status': 'erro', 'mensagem': 'dados nao enviados'})
            return
        upload_dir = os.path.join(DIR, 'uploads/funcionarios')
        os.makedirs(upload_dir, exist_ok=True)
        fname = f"{file_type}_{uuid.uuid4().hex[:8]}.{ext}"
        fpath = os.path.join(upload_dir, fname)
        try:
            raw = base64.b64decode(file_data)
            with open(fpath, 'wb') as f: f.write(raw)
            self.send_json({'status': 'ok', 'filename': fname, 'url': f'/uploads/funcionarios/{fname}'})
        except Exception as e:
            self.send_json({'status': 'erro', 'mensagem': str(e)})

    # ---- Folha de Pagamento ----

    TABELA_INSS = [
        (1412.00, 0.075), (2666.68, 0.09), (4000.03, 0.12), (7786.02, 0.14)
    ]
    DEDUCAO_INSS = [0, 105.90, 84.08, 36.99]

    TABELA_IRRF = [
        (2112.00, 0.0, 0), (2826.65, 0.075, 158.40),
        (3751.05, 0.15, 370.40), (4664.68, 0.225, 651.73),
        (float('inf'), 0.275, 884.96)
    ]
    DEDUCAO_DEPENDENTE = 189.59

    def _calcular_inss(self, salario):
        for i, (teto, ali) in enumerate(self.TABELA_INSS):
            if salario <= teto:
                return round(salario * ali - self.DEDUCAO_INSS[i], 2)
        return round(self.TABELA_INSS[-1][0] * self.TABELA_INSS[-1][1] - self.DEDUCAO_INSS[-1], 2)

    def _calcular_irrf(self, salario_base, dependentes=0, inss=0):
        base = salario_base - inss - dependentes * self.DEDUCAO_DEPENDENTE
        if base <= 0: return 0
        for teto, aliq, ded in self.TABELA_IRRF:
            if base <= teto:
                return round(base * aliq - ded, 2)
        return 0

    def _calcular_fgts(self, salario):
        return round(salario * 0.08, 2)

    def api_calcular_inss(self, params):
        salario = float(params.get('salario', ['0'])[0] or 0)
        self.send_json({'inss': self._calcular_inss(salario)})

    def api_calcular_irrf(self, params):
        salario = float(params.get('salario', ['0'])[0] or 0)
        dependentes = int(params.get('dependentes', ['0'])[0] or 0)
        inss = float(params.get('inss', ['0'])[0] or 0)
        self.send_json({'irrf': self._calcular_irrf(salario, dependentes, inss)})

    def api_folha_config(self):
        out, err = self.run_cobol('folha_pagamento', {'ACAO': 'config-ler'})
        try: self.send_json(json.loads(out))
        except: self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_folha_config_salvar(self, params):
        out, err = self.run_cobol('folha_pagamento', {
            'ACAO': 'config-salvar',
            'SALARIO_MINIMO': params.get('salario_minimo', ['1412'])[0],
            'INSS_F1_TETO': params.get('inss_f1_teto', ['1412'])[0],
            'INSS_F1_ALIQ': params.get('inss_f1_aliq', ['7.5'])[0],
            'INSS_F2_TETO': params.get('inss_f2_teto', ['2666.68'])[0],
            'INSS_F2_ALIQ': params.get('inss_f2_aliq', ['9'])[0],
            'INSS_F3_TETO': params.get('inss_f3_teto', ['4000.03'])[0],
            'INSS_F3_ALIQ': params.get('inss_f3_aliq', ['12'])[0],
            'INSS_F4_TETO': params.get('inss_f4_teto', ['7786.02'])[0],
            'INSS_F4_ALIQ': params.get('inss_f4_aliq', ['14'])[0],
            'IRRF_DED_DEP': params.get('irrf_ded_dep', ['189.59'])[0],
            'IRRF_F1_TETO': params.get('irrf_f1_teto', ['2112'])[0],
            'IRRF_F1_ALIQ': params.get('irrf_f1_aliq', ['0'])[0],
            'IRRF_F2_TETO': params.get('irrf_f2_teto', ['2826.65'])[0],
            'IRRF_F2_ALIQ': params.get('irrf_f2_aliq', ['7.5'])[0],
            'IRRF_F3_TETO': params.get('irrf_f3_teto', ['3751.05'])[0],
            'IRRF_F3_ALIQ': params.get('irrf_f3_aliq', ['15'])[0],
            'IRRF_F4_TETO': params.get('irrf_f4_teto', ['4664.68'])[0],
            'IRRF_F4_ALIQ': params.get('irrf_f4_aliq', ['22.5'])[0],
            'FGTS_ALIQUOTA': params.get('fgts_aliquota', ['8'])[0],
            'HORA_EXTRA_ALIQ': params.get('hora_extra_aliq', ['50'])[0],
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro',
                        'mensagem': out if out != 'OK' else ''})

    def api_folha_holerites(self):
        out, err = self.run_cobol('folha_pagamento', {'ACAO': 'holerite-listar'})
        try: self.send_json(json.loads(out))
        except: self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_folha_holerite_gerar(self, params):
        # ---- Salary Structure Integration ----
        try:
            func_id = params.get('funcionario_id', ['0'])[0]
            salario_base = float(params.get('salario_base', ['0'])[0] or 0)
            with open(os.path.join(DIR, 'dados/contabilidade_rules.json')) as f:
                cfg_data = json.load(f)
            func_configs = {str(fc['funcionario_id']): fc for fc in cfg_data.get('funcionarios', [])}
            fc = func_configs.get(func_id, {})
            estrutura_id = fc.get('estrutura_id', '')
            if estrutura_id:
                with open(os.path.join(DIR, 'dados/estruturas_salariais.json')) as f:
                    est_data = json.load(f)
                for e in est_data:
                    if str(e['id']) == str(estrutura_id):
                        prov_extra = 0.0
                        for comp in sorted(e.get('componentes', []), key=lambda x: x.get('ordem', 99)):
                            frm = comp.get('formula', '')
                            if frm == 'fixo' and comp.get('tipo') == 'provento':
                                prov_extra += float(comp.get('fixo', 0))
                            elif frm == 'percentual' and comp.get('tipo') == 'provento':
                                prov_extra += salario_base * float(comp.get('percentual', 0)) / 100.0
                            elif frm == 'percentual_vendas' and comp.get('tipo') == 'provento':
                                prov_extra += salario_base * float(comp.get('perc_vendas', 0)) / 100.0
                        he = float(params.get('horas_extras', ['0'])[0] or 0)
                        vhe = float(params.get('valor_hora_extra', ['0'])[0] or 0)
                        faltas = int(float(params.get('faltas', ['0'])[0] or 0))
                        total_base = salario_base + prov_extra + (he * vhe) - (salario_base / 30 * faltas)
                        params['salario_base'][0] = str(round(total_base, 2))
        except Exception:
            pass
        # ---- End Structure Integration ----

        # ---- Disciplinary Discount ----
        desc_disciplinar_val = 0.0
        desc_disciplinar_dias = 0
        desc_disciplinar_label = ''
        try:
            func_id_disc = params.get('funcionario_id', ['0'])[0]
            disc_out, _ = self.run_cobol('acao_disciplinar', {'ACAO': 'listar-por-func', 'FUNCIONARIO_ID': func_id_disc})
            if disc_out:
                disc_data = json.loads(disc_out)
                for acao in disc_data.get('acoes', []):
                    if acao.get('status', '') == 'A':
                        dias = int(acao.get('dias_desconto', 0) or 0)
                        val = float(acao.get('valor_desconto', 0) or 0)
                        if dias > 0 or val > 0:
                            sal = float(params.get('salario_base', ['0'])[0] or 0)
                            val_dia = sal / 30.0 if dias > 0 else 0
                            v = (val_dia * dias) if dias > 0 else val
                            desc_disciplinar_val += v
                            desc_disciplinar_dias += dias
                            if desc_disciplinar_label:
                                desc_disciplinar_label += '; '
                            desc_disciplinar_label += acao.get('descricao', 'Desconto disciplinar') or 'Desconto disciplinar'
        except Exception:
            pass
        # ---- End Disciplinary Discount ----

        # ---- Loan Installment Discount ----
        desc_emprestimo_val = 0.0
        desc_emprestimo_label = ''
        try:
            func_id_emp = params.get('funcionario_id', ['0'])[0]
            import json
            emp_out, _ = self.run_cobol('emprestimo', {'ACAO': 'listar-por-func', 'FUNCIONARIO_ID': func_id_emp})
            if emp_out:
                emp_data = json.loads(emp_out)
                for emp in emp_data.get('emprestimos', []):
                    if emp.get('status') == 'A':
                        eid = emp.get('id')
                        parc_path = os.path.join(DIR, 'dados/emprestimos_parcelas.json')
                        try:
                            with open(parc_path) as f:
                                parc_data = json.load(f)
                        except:
                            parc_data = {'parcelas': []}
                        for parc in parc_data.get('parcelas', []):
                            if parc.get('emprestimo_id') == eid and parc.get('status') == 'pending':
                                venc = parc.get('data_vencimento', '')
                                if venc:
                                    comp = params.get('competencia', [''])[0]
                                    if comp and venc >= comp[:7]:
                                        v = float(parc.get('valor', 0) or 0)
                                        desc_emprestimo_val += v
                                        if desc_emprestimo_label:
                                            desc_emprestimo_label += '; '
                                        desc_emprestimo_label += f'Emprestimo #{eid} parcela #{parc.get("numero")}'
                                        parc['status'] = 'blocked'
                                        break
                        for parc in parc_data.get('parcelas', []):
                            if parc.get('status') == 'blocked':
                                parc['status'] = 'pending'
                        try:
                            with open(parc_path, 'w') as f:
                                json.dump(parc_data, f, ensure_ascii=False, indent=2)
                        except:
                            pass
        except Exception:
            pass
        # ---- End Loan Installment Discount ----

        func_id = params.get('funcionario_id', ['0'])[0]
        competencia = params.get('competencia', [''])[0]
        salario_base = float(params.get('salario_base', ['0'])[0] or 0)
        horas_extras = float(params.get('horas_extras', ['0'])[0] or 0)
        valor_hora_extra = float(params.get('valor_hora_extra', ['0'])[0] or 0)
        faltas = int(float(params.get('faltas', ['0'])[0] or 0))
        observacoes = params.get('observacoes', [''])[0]

        vl_hora_extra = horas_extras * valor_hora_extra
        dsr = round(vl_hora_extra / 6, 2) if vl_hora_extra > 0 else 0
        proventos = round(salario_base + vl_hora_extra + dsr, 2)
        inss_val = self._calcular_inss(proventos)
        irrf_val = self._calcular_irrf(proventos, inss=inss_val)
        fgts_val = round(salario_base * 0.08, 2)
        outros_desc = round(desc_disciplinar_val + desc_emprestimo_val, 2)
        total_desc = round(inss_val + irrf_val + outros_desc, 2)
        liquido = round(proventos - total_desc, 2)

        params.setdefault('nomes', [''])[0]
        out, err = self.run_cobol('folha_pagamento', {
            'ACAO': 'holerite-gerar',
            'FUNCIONARIO_ID': func_id,
            'COMPETENCIA': competencia,
            'SALARIO_BASE': str(salario_base),
            'HORAS_EXTRAS': str(horas_extras),
            'VALOR_HORA_EXTRA': str(valor_hora_extra),
            'DSR': str(dsr),
            'FALTAS': str(faltas),
            'PROVENTOS': str(proventos),
            'INSS': str(inss_val),
            'IRRF': str(irrf_val),
            'FGTS': str(fgts_val),
            'OUTROS_DESC': str(outros_desc),
            'TOTAL_DESC': str(total_desc),
            'LIQUIDO': str(liquido),
            'NOME': params.get('nome', [''])[0],
        })
        if out and out.isdigit():
            hid_str = out.strip()
            try:
                path = os.path.join(DIR, 'dados/holerite_detalhes.json')
                with open(path) as f:
                    det_data = json.load(f)
            except:
                det_data = {}
            if hid_str not in det_data:
                det_data[hid_str] = {}
            if observacoes:
                det_data[hid_str]['observacoes'] = observacoes
            comps = det_data[hid_str].get('componentes', [])
            if desc_disciplinar_val > 0:
                comps.append({
                    'nome': desc_disciplinar_label or 'Desconto Disciplinar',
                    'tipo': 'desconto',
                    'formula': 'disciplinar',
                    'valor_auto': desc_disciplinar_val,
                    'valor_manual': desc_disciplinar_val,
                    'metodo': 'auto',
                })
            if desc_emprestimo_val > 0:
                comps.append({
                    'nome': desc_emprestimo_label or 'Desconto Emprestimo',
                    'tipo': 'desconto',
                    'formula': 'emprestimo',
                    'valor_auto': desc_emprestimo_val,
                    'valor_manual': desc_emprestimo_val,
                    'metodo': 'auto',
                })
                try:
                    parc_path = os.path.join(DIR, 'dados/emprestimos_parcelas.json')
                    with open(parc_path) as f:
                        parc_data = json.load(f)
                    for parc in parc_data.get('parcelas', []):
                        if parc.get('status') == 'pending':
                            parc['status'] = 'paid'
                            parc['data_pagamento'] = datetime.date.today().isoformat()
                            parc['holerite_id'] = hid_str
                            break
                    with open(parc_path, 'w') as f:
                        json.dump(parc_data, f, ensure_ascii=False, indent=2)
                except:
                    pass
            det_data[hid_str]['componentes'] = comps
            try:
                with open(path, 'w') as f:
                    json.dump(det_data, f, ensure_ascii=False, indent=2)
            except:
                pass
            self.send_json({'status': 'ok', 'id': int(out), 'liquido': liquido,
                            'inss': inss_val, 'irrf': irrf_val, 'fgts': fgts_val,
                            'proventos': proventos, 'total_descontos': total_desc,
                            'desconto_disciplinar': desc_disciplinar_val,
                            'desconto_emprestimo': desc_emprestimo_val})
        else:
            self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_folha_holerite_detalhes(self, params):
        import json, os
        hid = params.get('id', ['0'])[0]
        path = os.path.join(DIR, 'dados/holerite_detalhes.json')
        if not hid:
            self.send_json({'status': 'erro', 'mensagem': 'id obrigatorio'}); return
        try:
            with open(path) as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        detalhes = data.get(str(hid), {})
        self.send_json({
            'status': 'ok',
            'id': int(hid),
            'componentes': detalhes.get('componentes', []),
            'observacoes': detalhes.get('observacoes', ''),
        })

    def api_folha_holerite_detalhes_salvar(self, params):
        import json, os
        hid = params.get('id', ['0'])[0]
        if not hid:
            self.send_json({'status': 'erro', 'mensagem': 'id obrigatorio'}); return
        path = os.path.join(DIR, 'dados/holerite_detalhes.json')
        try:
            with open(path) as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        componentes_str = params.get('componentes', ['[]'])[0]
        observacoes = params.get('observacoes', [''])[0]
        try:
            componentes = json.loads(componentes_str)
        except:
            componentes = []
        data[str(hid)] = {
            'componentes': componentes,
            'observacoes': observacoes,
        }
        with open(path, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.send_json({'status': 'ok'})

    def api_folha_holerite_pagar(self, params):
        import datetime
        data = datetime.date.today().isoformat()
        out, err = self.run_cobol('folha_pagamento', {
            'ACAO': 'holerite-pagar',
            'ID': params.get('id', ['0'])[0],
            'DATA_PAGAMENTO': data,
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro',
                        'mensagem': out if out != 'OK' else ''})

    def api_folha_holerite_excluir(self, params):
        out, err = self.run_cobol('folha_pagamento', {
            'ACAO': 'holerite-excluir',
            'ID': params.get('id', ['0'])[0],
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro',
                        'mensagem': out if out != 'OK' else ''})

    # ---- Categorias Disciplinares ----

    def api_categorias_disciplinares(self):
        out, err = self.run_cobol('categoria_disciplinar', {'ACAO': 'listar'})
        try: self.send_json(json.loads(out))
        except: self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_categoria_disciplinar_incluir(self, params):
        out, err = self.run_cobol('categoria_disciplinar', {
            'ACAO': 'incluir',
            'NOME': params.get('nome', [''])[0],
            'DESCRICAO': params.get('descricao', [''])[0],
        })
        if out and out.isdigit():
            self.send_json({'status': 'ok', 'id': int(out)})
        else:
            self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_categoria_disciplinar_alterar(self, params):
        out, err = self.run_cobol('categoria_disciplinar', {
            'ACAO': 'alterar',
            'ID': params.get('id', ['0'])[0],
            'NOME': params.get('nome', [''])[0],
            'DESCRICAO': params.get('descricao', [''])[0],
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro', 'mensagem': out if out != 'OK' else ''})

    def api_categoria_disciplinar_excluir(self, params):
        out, err = self.run_cobol('categoria_disciplinar', {
            'ACAO': 'excluir',
            'ID': params.get('id', ['0'])[0],
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro', 'mensagem': out if out != 'OK' else ''})

    # ---- Acoes Disciplinares ----

    def api_acoes_disciplinares(self, params):
        func_id = params.get('funcionario_id', ['0'])[0]
        if func_id and func_id != '0':
            out, err = self.run_cobol('acao_disciplinar', {'ACAO': 'listar-por-func', 'FUNCIONARIO_ID': func_id})
        else:
            out, err = self.run_cobol('acao_disciplinar', {'ACAO': 'listar'})
        try: self.send_json(json.loads(out))
        except: self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_acao_disciplinar_incluir(self, params):
        out, err = self.run_cobol('acao_disciplinar', {
            'ACAO': 'incluir',
            'FUNCIONARIO_ID': params.get('funcionario_id', ['0'])[0],
            'CATEGORIA_ID': params.get('categoria_id', ['0'])[0],
            'DATA': params.get('data', [''])[0],
            'DESCRICAO': params.get('descricao', [''])[0],
            'DIAS_DESCONTO': params.get('dias_desconto', ['0'])[0],
            'VALOR_DESCONTO': params.get('valor_desconto', ['0'])[0],
            'STATUS': params.get('status', ['A'])[0],
        })
        if out and out.isdigit():
            self.send_json({'status': 'ok', 'id': int(out)})
        else:
            self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_acao_disciplinar_alterar(self, params):
        out, err = self.run_cobol('acao_disciplinar', {
            'ACAO': 'alterar',
            'ID': params.get('id', ['0'])[0],
            'FUNCIONARIO_ID': params.get('funcionario_id', [''])[0],
            'CATEGORIA_ID': params.get('categoria_id', [''])[0],
            'DATA': params.get('data', [''])[0],
            'DESCRICAO': params.get('descricao', [''])[0],
            'DIAS_DESCONTO': params.get('dias_desconto', [''])[0],
            'VALOR_DESCONTO': params.get('valor_desconto', [''])[0],
            'STATUS': params.get('status', [''])[0],
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro', 'mensagem': out if out != 'OK' else ''})

    def api_acao_disciplinar_excluir(self, params):
        out, err = self.run_cobol('acao_disciplinar', {
            'ACAO': 'excluir',
            'ID': params.get('id', ['0'])[0],
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro', 'mensagem': out if out != 'OK' else ''})

    # ---- Workflow Engine ----

    def _load_workflow_defs(self):
        path = os.path.join(DIR, 'dados/workflow.json')
        try:
            with open(path) as f: return json.load(f)
        except: return {}

    def _load_workflow_history(self):
        path = os.path.join(DIR, 'dados/workflow_history.json')
        try:
            with open(path) as f: return json.load(f)
        except: return {'entries': []}

    def _save_workflow_history(self, data):
        path = os.path.join(DIR, 'dados/workflow_history.json')
        with open(path, 'w') as f: json.dump(data, f, ensure_ascii=False, indent=2)

    def _validate_transition(self, module, current_status, target_status, user_role):
        defs = self._load_workflow_defs()
        mod_def = defs.get(module)
        if not mod_def:
            return False, 'Modulo nao encontrado'
        transitions = mod_def.get('transitions', {})
        curr_trans = transitions.get(current_status)
        if not curr_trans:
            return False, f'Nenhuma transicao permitida do estado {current_status}'
        target_def = curr_trans.get(target_status)
        if not target_def:
            return False, f'Transicao {current_status} -> {target_status} nao permitida'
        allowed_roles = target_def.get('roles', [])
        if user_role not in allowed_roles:
            return False, f'Usuario com funcao "{user_role}" nao tem permissao para esta transicao'
        return True, target_def.get('label', '')

    def _add_history_entry(self, module, record_id, from_status, to_status, user_name, user_role, notes=''):
        data = self._load_workflow_history()
        import datetime
        data['entries'].append({
            'id': len(data['entries']) + 1,
            'module': module,
            'record_id': record_id,
            'from_status': from_status,
            'to_status': to_status,
            'user_name': user_name,
            'user_role': user_role,
            'notes': notes,
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        })
        self._save_workflow_history(data)

    def api_workflow_definitions(self):
        defs = self._load_workflow_defs()
        result = {}
        for mod, cfg in defs.items():
            result[mod] = {
                'label': cfg.get('label', mod),
                'states': cfg.get('states', []),
                'transitions': cfg.get('transitions', {}),
            }
        self.send_json({'status': 'ok', 'workflows': result})

    def api_workflow_history(self, params):
        data = self._load_workflow_history()
        module = params.get('module', [''])[0]
        rec_id = params.get('record_id', [''])[0]
        entries = data.get('entries', [])
        if module:
            entries = [e for e in entries if e['module'] == module]
        if rec_id:
            entries = [e for e in entries if str(e['record_id']) == rec_id]
        self.send_json({'status': 'ok', 'entries': entries})

    def api_workflow_transition(self, params):
        module = params.get('module', [''])[0]
        record_id = params.get('record_id', ['0'])[0]
        target_status = params.get('target_status', [''])[0]
        user_name = params.get('user_name', ['Sistema'])[0]
        user_role = params.get('user_role', ['admin'])[0]
        notes = params.get('notes', [''])[0]
        import datetime

        defs = self._load_workflow_defs()
        mod_def = defs.get(module)
        if not mod_def:
            self.send_json({'status': 'erro', 'mensagem': 'Modulo invalido'}); return

        current_status = None
        try:
            if module == 'emprestimo':
                out, _ = self.run_cobol('emprestimo', {'ACAO': 'listar'})
                if out:
                    ed = json.loads(out)
                    for e in ed.get('emprestimos', []):
                        if str(e.get('id')) == record_id:
                            current_status = e.get('status', '')
                            break
            elif module == 'licenca':
                out, _ = self.run_cobol('licenca', {'ACAO': 'listar'})
                if out:
                    ld = json.loads(out)
                    for l in ld.get('licencas', []):
                        if str(l.get('id')) == record_id:
                            current_status = l.get('status', '')
                            break
        except: pass

        if not current_status:
            self.send_json({'status': 'erro', 'mensagem': 'Registro nao encontrado'}); return

        valid, msg = self._validate_transition(module, current_status, target_status, user_role)
        if not valid:
            self.send_json({'status': 'erro', 'mensagem': msg}); return

        # Pre-execution validations
        if module == 'emprestimo' and target_status == 'C':
            try:
                parc_data = self._load_parcelas()
                unpaid = [p for p in parc_data['parcelas'] if p['emprestimo_id'] == int(record_id) and p['status'] != 'paid']
                if unpaid:
                    self.send_json({'status': 'erro', 'mensagem': f'Ainda ha {len(unpaid)} parcela(s) pendente(s). Quite todas antes de encerrar.'})
                    return
            except:
                pass

        if module == 'emprestimo':
            out, err = self.run_cobol('emprestimo', {
                'ACAO': 'transitar',
                'ID': record_id,
                'STATUS': target_status,
                'APROVADO_POR': user_name,
                'DATA_APROVACAO': datetime.date.today().isoformat(),
            })
            if out != 'OK':
                self.send_json({'status': 'erro', 'mensagem': out or err}); return
        elif module == 'licenca':
            out, err = self.run_cobol('licenca', {
                'ACAO': 'transitar',
                'ID': record_id,
                'STATUS': target_status,
                'APROVADO_POR': user_name,
                'DATA_APROVACAO': datetime.date.today().isoformat(),
            })
            if out != 'OK':
                self.send_json({'status': 'erro', 'mensagem': out or err}); return
        elif module == 'despesa':
            desp_data = self._load_despesas()
            for d in desp_data.get('despesas', []):
                if d['id'] == int(record_id):
                    d['status'] = target_status
                    d['aprovado_por'] = user_name
                    d['data_aprovacao'] = datetime.date.today().isoformat()
                    break
            self._save_despesas(desp_data)
        elif module == 'acao_disciplinar':
            out, err = self.run_cobol('acao_disciplinar', {
                'ACAO': 'alterar',
                'ID': record_id,
                'STATUS': target_status,
            })
            if out != 'OK':
                self.send_json({'status': 'erro', 'mensagem': out or err}); return

        self._add_history_entry(module, int(record_id), current_status, target_status, user_name, user_role, notes)

        if module == 'emprestimo' and target_status == 'A':
            try:
                out, _ = self.run_cobol('emprestimo', {'ACAO': 'listar'})
                if out:
                    ed = json.loads(out)
                    for e in ed.get('emprestimos', []):
                        if str(e.get('id')) == record_id:
                            self._gerar_parcelas(
                                int(record_id),
                                float(e.get('valor_parcela', 0)),
                                int(e.get('num_parcelas', 1)),
                                e.get('data_primeira_parcela', datetime.date.today().isoformat())
                            )
                            break
            except: pass

        self.send_json({
            'status': 'ok',
            'from_status': current_status,
            'to_status': target_status,
            'transition_label': msg,
        })

    # ---- Emprestimos ----

    def _load_parcelas(self):
        path = os.path.join(DIR, 'dados/emprestimos_parcelas.json')
        try:
            with open(path) as f: return json.load(f)
        except: return {'parcelas': [], 'prox_id': 1}

    def _save_parcelas(self, data):
        path = os.path.join(DIR, 'dados/emprestimos_parcelas.json')
        with open(path, 'w') as f: json.dump(data, f, ensure_ascii=False, indent=2)

    def _gerar_parcelas(self, emprestimo_id, valor_parcela, num_parcelas, data_primeira):
        """Generate installment schedule when loan is approved"""
        import datetime
        data = self._load_parcelas()
        dt = datetime.datetime.strptime(data_primeira[:10], '%Y-%m-%d')
        for i in range(num_parcelas):
            venc = dt + datetime.timedelta(days=30 * i)
            data['parcelas'].append({
                'id': data['prox_id'],
                'emprestimo_id': emprestimo_id,
                'numero': i + 1,
                'valor': round(valor_parcela, 2),
                'data_vencimento': venc.strftime('%Y-%m-%d'),
                'data_pagamento': '',
                'status': 'pending',
                'holerite_id': None,
            })
            data['prox_id'] += 1
        self._save_parcelas(data)

    def api_emprestimos(self, params):
        func_id = params.get('funcionario_id', ['0'])[0]
        if func_id and func_id != '0':
            out, err = self.run_cobol('emprestimo', {'ACAO': 'listar-por-func', 'FUNCIONARIO_ID': func_id})
        else:
            out, err = self.run_cobol('emprestimo', {'ACAO': 'listar'})
        try:
            data = json.loads(out)
            # Attach saldo devedor from parcelas
            parc_data = self._load_parcelas()
            for emp in data.get('emprestimos', []):
                eid = emp.get('id')
                pars = [p for p in parc_data['parcelas'] if p['emprestimo_id'] == eid]
                emp['total_parcelas'] = len(pars)
                emp['parcelas_pagas'] = sum(1 for p in pars if p['status'] == 'paid')
                emp['parcelas_pendentes'] = sum(1 for p in pars if p['status'] == 'pending')
                emp['saldo_devedor'] = round(sum(float(p['valor']) for p in pars if p['status'] != 'paid'), 2)
            self.send_json(data)
        except: self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_emprestimos_pendentes(self):
        out, err = self.run_cobol('emprestimo', {'ACAO': 'pendentes'})
        try: self.send_json(json.loads(out))
        except: self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_emprestimos_ativos(self):
        out, err = self.run_cobol('emprestimo', {'ACAO': 'ativos'})
        try: self.send_json(json.loads(out))
        except: self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_emprestimo_incluir(self, params):
        out, err = self.run_cobol('emprestimo', {
            'ACAO': 'incluir',
            'FUNCIONARIO_ID': params.get('funcionario_id', ['0'])[0],
            'TIPO': params.get('tipo', [''])[0],
            'VALOR_TOTAL': params.get('valor_total', ['0'])[0],
            'NUM_PARCELAS': params.get('num_parcelas', ['1'])[0],
            'VALOR_PARCELA': params.get('valor_parcela', ['0'])[0],
            'TAXA_JUROS': params.get('taxa_juros', ['0'])[0],
            'DATA_SOLICITACAO': params.get('data_solicitacao', [''])[0],
            'DATA_PRIMEIRA_PARCELA': params.get('data_primeira_parcela', [''])[0],
            'MOTIVO': params.get('motivo', [''])[0],
            'STATUS': params.get('status', ['P'])[0],
        })
        if out and out.isdigit():
            self.send_json({'status': 'ok', 'id': int(out)})
        else:
            self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_emprestimo_alterar(self, params):
        out, err = self.run_cobol('emprestimo', {
            'ACAO': 'alterar',
            'ID': params.get('id', ['0'])[0],
            'TIPO': params.get('tipo', [''])[0],
            'VALOR_TOTAL': params.get('valor_total', [''])[0],
            'NUM_PARCELAS': params.get('num_parcelas', [''])[0],
            'VALOR_PARCELA': params.get('valor_parcela', [''])[0],
            'TAXA_JUROS': params.get('taxa_juros', [''])[0],
            'DATA_SOLICITACAO': params.get('data_solicitacao', [''])[0],
            'DATA_PRIMEIRA_PARCELA': params.get('data_primeira_parcela', [''])[0],
            'MOTIVO': params.get('motivo', [''])[0],
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro', 'mensagem': out if out != 'OK' else ''})

    def api_emprestimo_excluir(self, params):
        out, err = self.run_cobol('emprestimo', {'ACAO': 'excluir', 'ID': params.get('id', ['0'])[0]})
        self.send_json({'status': 'ok' if out == 'OK' else 'erro', 'mensagem': out if out != 'OK' else ''})

    def api_emprestimo_calcular_parcela(self, params):
        out, err = self.run_cobol('emprestimo', {
            'ACAO': 'calcular-parcela',
            'VALOR_TOTAL': params.get('valor_total', ['0'])[0],
            'NUM_PARCELAS': params.get('num_parcelas', ['1'])[0],
            'TAXA_JUROS': params.get('taxa_juros', ['0'])[0],
        })
        if out:
            try:
                val = float(out.strip())
                self.send_json({'status': 'ok', 'valor_parcela': val})
            except:
                self.send_json({'status': 'erro', 'mensagem': out})
        else:
            self.send_json({'status': 'erro', 'mensagem': err})

    def api_emprestimo_aprovar(self, params):
        import datetime
        hoje = datetime.date.today().isoformat()
        eid = params.get('id', ['0'])[0]
        out, err = self.run_cobol('emprestimo', {
            'ACAO': 'aprovar',
            'ID': eid,
            'APROVADO_POR': params.get('aprovado_por', ['Sistema'])[0],
            'DATA_APROVACAO': hoje,
        })
        if out == 'OK':
            # Generate installment schedule
            emp_out, _ = self.run_cobol('emprestimo', {'ACAO': 'listar'})
            try:
                emp_data = json.loads(emp_out)
                for e in emp_data.get('emprestimos', []):
                    if str(e.get('id')) == eid:
                        self._gerar_parcelas(
                            int(eid),
                            float(e.get('valor_parcela', 0)),
                            int(e.get('num_parcelas', 1)),
                            e.get('data_primeira_parcela', hoje)
                        )
                        break
            except: pass
            self.send_json({'status': 'ok'})
        else:
            self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_emprestimo_rejeitar(self, params):
        import datetime
        hoje = datetime.date.today().isoformat()
        out, err = self.run_cobol('emprestimo', {
            'ACAO': 'rejeitar',
            'ID': params.get('id', ['0'])[0],
            'APROVADO_POR': params.get('aprovado_por', ['Sistema'])[0],
            'DATA_APROVACAO': hoje,
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro', 'mensagem': out if out != 'OK' else ''})

    def api_emprestimo_parcelas(self, params):
        eid = params.get('id', ['0'])[0]
        data = self._load_parcelas()
        if eid:
            pars = [p for p in data['parcelas'] if p['emprestimo_id'] == int(eid)]
        else:
            pars = data['parcelas']
        saldo = round(sum(float(p['valor']) for p in pars if p['status'] == 'pending'), 2) if eid else 0
        pagas = sum(1 for p in pars if p['status'] == 'paid') if eid else 0
        self.send_json({'status': 'ok', 'parcelas': pars, 'saldo_devedor': saldo, 'parcelas_pagas': pagas})

    def api_emprestimo_saldo(self, params):
        eid = params.get('id', ['0'])[0]
        data = self._load_parcelas()
        if eid:
            pars = [p for p in data['parcelas'] if p['emprestimo_id'] == int(eid)]
            saldo_total = round(sum(float(p['valor']) for p in pars if p['status'] != 'paid'), 2)
            pagas = sum(1 for p in pars if p['status'] == 'paid')
            pendentes = sum(1 for p in pars if p['status'] == 'pending')
            total_valor = round(sum(float(p['valor']) for p in pars), 2)
        else:
            saldo_total = pagas = pendentes = total_valor = 0
        self.send_json({
            'status': 'ok',
            'saldo_devedor': saldo_total,
            'parcelas_pagas': pagas,
            'parcelas_pendentes': pendentes,
            'total_parcelas': pagas + pendentes,
            'total_valor': total_valor,
        })

    def api_emprestimo_parcela_pagar(self, params):
        import datetime
        hoje = datetime.date.today().isoformat()
        pid = int(params.get('id', ['0'])[0])
        data = self._load_parcelas()
        for p in data['parcelas']:
            if p['id'] == pid:
                p['status'] = 'paid'
                p['data_pagamento'] = hoje
                p['holerite_id'] = params.get('holerite_id', [''])[0]
                break
        self._save_parcelas(data)
        self.send_json({'status': 'ok'})

    # ---- Licencas ----

    def api_licencas(self, params):
        func_id = params.get('funcionario_id', ['0'])[0]
        if func_id and func_id != '0':
            out, err = self.run_cobol('licenca', {'ACAO': 'listar-por-func', 'FUNCIONARIO_ID': func_id})
        else:
            out, err = self.run_cobol('licenca', {'ACAO': 'listar'})
        try: self.send_json(json.loads(out))
        except: self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_licencas_pendentes(self):
        out, err = self.run_cobol('licenca', {'ACAO': 'pendentes'})
        try: self.send_json(json.loads(out))
        except: self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_licenca_incluir(self, params):
        out, err = self.run_cobol('licenca', {
            'ACAO': 'incluir',
            'FUNCIONARIO_ID': params.get('funcionario_id', ['0'])[0],
            'TIPO': params.get('tipo', [''])[0],
            'DATA_INICIO': params.get('data_inicio', [''])[0],
            'DATA_FIM': params.get('data_fim', [''])[0],
            'DIAS': params.get('dias', ['0'])[0],
            'MOTIVO': params.get('motivo', [''])[0],
            'STATUS': params.get('status', ['P'])[0],
            'OBSERVACOES': params.get('observacoes', [''])[0],
        })
        if out and out.isdigit():
            self.send_json({'status': 'ok', 'id': int(out)})
        else:
            self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_licenca_alterar(self, params):
        out, err = self.run_cobol('licenca', {
            'ACAO': 'alterar',
            'ID': params.get('id', ['0'])[0],
            'TIPO': params.get('tipo', [''])[0],
            'DATA_INICIO': params.get('data_inicio', [''])[0],
            'DATA_FIM': params.get('data_fim', [''])[0],
            'DIAS': params.get('dias', [''])[0],
            'MOTIVO': params.get('motivo', [''])[0],
            'OBSERVACOES': params.get('observacoes', [''])[0],
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro', 'mensagem': out if out != 'OK' else ''})

    def api_licenca_excluir(self, params):
        out, err = self.run_cobol('licenca', {'ACAO': 'excluir', 'ID': params.get('id', ['0'])[0]})
        self.send_json({'status': 'ok' if out == 'OK' else 'erro', 'mensagem': out if out != 'OK' else ''})

    def api_licenca_aprovar(self, params):
        import datetime
        hoje = datetime.date.today().isoformat()
        out, err = self.run_cobol('licenca', {
            'ACAO': 'aprovar',
            'ID': params.get('id', ['0'])[0],
            'APROVADO_POR': params.get('aprovado_por', ['Sistema'])[0],
            'DATA_APROVACAO': hoje,
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro', 'mensagem': out if out != 'OK' else ''})

    def api_licenca_rejeitar(self, params):
        import datetime
        hoje = datetime.date.today().isoformat()
        out, err = self.run_cobol('licenca', {
            'ACAO': 'rejeitar',
            'ID': params.get('id', ['0'])[0],
            'APROVADO_POR': params.get('aprovado_por', ['Sistema'])[0],
            'DATA_APROVACAO': hoje,
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro', 'mensagem': out if out != 'OK' else ''})

    # ---- Timesheets ----

    def api_timesheets(self, params):
        func_id = params.get('funcionario_id', ['0'])[0]
        projeto = params.get('projeto', [''])[0]
        if func_id and func_id != '0':
            out, err = self.run_cobol('timesheet', {'ACAO': 'listar-por-func', 'FUNCIONARIO_ID': func_id})
        elif projeto:
            out, err = self.run_cobol('timesheet', {'ACAO': 'listar-por-proj', 'PROJETO': projeto})
        else:
            out, err = self.run_cobol('timesheet', {'ACAO': 'listar'})
        try: self.send_json(json.loads(out))
        except: self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_timesheet_incluir(self, params):
        out, err = self.run_cobol('timesheet', {
            'ACAO': 'incluir',
            'FUNCIONARIO_ID': params.get('funcionario_id', ['0'])[0],
            'DATA': params.get('data', [''])[0],
            'PROJETO': params.get('projeto', [''])[0],
            'TAREFA': params.get('tarefa', [''])[0],
            'HORAS': params.get('horas', ['0'])[0],
            'DESCRICAO': params.get('descricao', [''])[0],
            'STATUS': params.get('status', ['P'])[0],
        })
        if out and out.isdigit():
            self.send_json({'status': 'ok', 'id': int(out)})
        else:
            self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_timesheet_alterar(self, params):
        out, err = self.run_cobol('timesheet', {
            'ACAO': 'alterar',
            'ID': params.get('id', ['0'])[0],
            'PROJETO': params.get('projeto', [''])[0],
            'TAREFA': params.get('tarefa', [''])[0],
            'HORAS': params.get('horas', [''])[0],
            'DESCRICAO': params.get('descricao', [''])[0],
            'STATUS': params.get('status', [''])[0],
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro', 'mensagem': out if out != 'OK' else ''})

    def api_timesheet_excluir(self, params):
        out, err = self.run_cobol('timesheet', {'ACAO': 'excluir', 'ID': params.get('id', ['0'])[0]})
        self.send_json({'status': 'ok' if out == 'OK' else 'erro', 'mensagem': out if out != 'OK' else ''})

    # ---- Recrutamento (JSON-based) ----

    def _load_recrutamento(self):
        path = os.path.join(DIR, 'dados/recrutamento.json')
        try:
            with open(path) as f: return json.load(f)
        except: return {'vagas': [], 'candidatos': [], 'prox_vaga': 1, 'prox_candidato': 1}

    def _save_recrutamento(self, data):
        path = os.path.join(DIR, 'dados/recrutamento.json')
        with open(path, 'w') as f: json.dump(data, f, ensure_ascii=False, indent=2)

    def api_recrutamento_vagas(self):
        data = self._load_recrutamento()
        self.send_json({'status': 'ok', 'vagas': data.get('vagas', [])})

    def api_recrutamento_candidatos(self, params):
        data = self._load_recrutamento()
        vaga_id = params.get('vaga_id', [''])[0]
        if vaga_id:
            cands = [c for c in data.get('candidatos', []) if str(c.get('vaga_id')) == vaga_id]
        else:
            cands = data.get('candidatos', [])
        self.send_json({'status': 'ok', 'candidatos': cands})

    def api_vaga_incluir(self, params):
        data = self._load_recrutamento()
        vaga = {
            'id': data['prox_vaga'],
            'cargo': params.get('cargo', [''])[0],
            'departamento': params.get('departamento', [''])[0],
            'descricao': params.get('descricao', [''])[0],
            'requisitos': params.get('requisitos', [''])[0],
            'salario': params.get('salario', ['0'])[0],
            'status': params.get('status', ['aberta'])[0],
            'data_criacao': datetime.date.today().isoformat(),
        }
        data['vagas'].append(vaga)
        data['prox_vaga'] += 1
        self._save_recrutamento(data)
        self.send_json({'status': 'ok', 'id': vaga['id']})

    def api_vaga_alterar(self, params):
        data = self._load_recrutamento()
        vid = int(params.get('id', ['0'])[0])
        for v in data['vagas']:
            if v['id'] == vid:
                for k in ['cargo','departamento','descricao','requisitos','salario','status']:
                    if params.get(k, [''])[0]:
                        v[k] = params.get(k, [''])[0]
                break
        self._save_recrutamento(data)
        self.send_json({'status': 'ok'})

    def api_vaga_excluir(self, params):
        data = self._load_recrutamento()
        vid = int(params.get('id', ['0'])[0])
        data['vagas'] = [v for v in data['vagas'] if v['id'] != vid]
        self._save_recrutamento(data)
        self.send_json({'status': 'ok'})

    def api_candidato_incluir(self, params):
        data = self._load_recrutamento()
        cand = {
            'id': data['prox_candidato'],
            'vaga_id': int(params.get('vaga_id', ['0'])[0]),
            'nome': params.get('nome', [''])[0],
            'email': params.get('email', [''])[0],
            'telefone': params.get('telefone', [''])[0],
            'status': params.get('status', ['triagem'])[0],
            'observacoes': params.get('observacoes', [''])[0],
            'data_candidatura': datetime.date.today().isoformat(),
        }
        data['candidatos'].append(cand)
        data['prox_candidato'] += 1
        self._save_recrutamento(data)
        self.send_json({'status': 'ok', 'id': cand['id']})

    def api_candidato_alterar(self, params):
        data = self._load_recrutamento()
        cid = int(params.get('id', ['0'])[0])
        for c in data['candidatos']:
            if c['id'] == cid:
                for k in ['nome','email','telefone','status','observacoes']:
                    if params.get(k, [''])[0]:
                        c[k] = params.get(k, [''])[0]
                break
        self._save_recrutamento(data)
        self.send_json({'status': 'ok'})

    def api_candidato_excluir(self, params):
        data = self._load_recrutamento()
        cid = int(params.get('id', ['0'])[0])
        data['candidatos'] = [c for c in data['candidatos'] if c['id'] != cid]
        self._save_recrutamento(data)
        self.send_json({'status': 'ok'})

    # ---- Despesas (JSON-based) ----

    def _load_despesas(self):
        path = os.path.join(DIR, 'dados/despesas.json')
        try:
            with open(path) as f: return json.load(f)
        except: return {'despesas': [], 'prox_id': 1}

    def _save_despesas(self, data):
        path = os.path.join(DIR, 'dados/despesas.json')
        with open(path, 'w') as f: json.dump(data, f, ensure_ascii=False, indent=2)

    def api_despesas(self, params):
        data = self._load_despesas()
        func_id = params.get('funcionario_id', [''])[0]
        if func_id:
            desp = [d for d in data['despesas'] if str(d.get('funcionario_id')) == func_id]
        else:
            desp = data['despesas']
        self.send_json({'status': 'ok', 'despesas': desp})

    def api_despesas_pendentes(self):
        data = self._load_despesas()
        pend = [d for d in data['despesas'] if d.get('status') == 'P']
        self.send_json({'status': 'ok', 'despesas': pend})

    def api_despesa_incluir(self, params):
        data = self._load_despesas()
        desp = {
            'id': data['prox_id'],
            'funcionario_id': int(params.get('funcionario_id', ['0'])[0]),
            'data': params.get('data', [''])[0],
            'categoria': params.get('categoria', [''])[0],
            'descricao': params.get('descricao', [''])[0],
            'valor': float(params.get('valor', ['0'])[0] or 0),
            'status': params.get('status', ['D'])[0],
            'aprovado_por': '',
            'data_aprovacao': '',
            'observacoes': params.get('observacoes', [''])[0],
        }
        data['despesas'].append(desp)
        data['prox_id'] += 1
        self._save_despesas(data)
        self.send_json({'status': 'ok', 'id': desp['id']})

    def api_despesa_alterar(self, params):
        data = self._load_despesas()
        did = int(params.get('id', ['0'])[0])
        for d in data['despesas']:
            if d['id'] == did:
                for k in ['data','categoria','descricao','valor','observacoes']:
                    if params.get(k, [''])[0]:
                        v = params.get(k, [''])[0]
                        d[k] = float(v) if k == 'valor' else v
                break
        self._save_despesas(data)
        self.send_json({'status': 'ok'})

    def api_despesa_excluir(self, params):
        data = self._load_despesas()
        did = int(params.get('id', ['0'])[0])
        data['despesas'] = [d for d in data['despesas'] if d['id'] != did]
        self._save_despesas(data)
        self.send_json({'status': 'ok'})

    def api_despesa_aprovar(self, params):
        import datetime
        hoje = datetime.date.today().isoformat()
        data = self._load_despesas()
        did = int(params.get('id', ['0'])[0])
        for d in data['despesas']:
            if d['id'] == did:
                d['status'] = 'A'
                d['aprovado_por'] = params.get('aprovado_por', ['Sistema'])[0]
                d['data_aprovacao'] = hoje
                break
        self._save_despesas(data)
        self.send_json({'status': 'ok'})

    def api_despesa_rejeitar(self, params):
        import datetime
        hoje = datetime.date.today().isoformat()
        data = self._load_despesas()
        did = int(params.get('id', ['0'])[0])
        for d in data['despesas']:
            if d['id'] == did:
                d['status'] = 'R'
                d['aprovado_por'] = params.get('aprovado_por', ['Sistema'])[0]
                d['data_aprovacao'] = hoje
                break
        self._save_despesas(data)
        self.send_json({'status': 'ok'})

    # ---- Directory ----
    def api_directory(self):
        try:
            out, _ = self.run_cobol('gerir_funcionarios', {'ACAO': 'listar'})
            funcs = json.loads(out).get('funcionarios', [])
        except:
            funcs = []
        try:
            out2, _ = self.run_cobol('dependentes', {'ACAO': 'listar'})
            deps = json.loads(out2).get('dependentes', [])
        except:
            deps = []
        # Count dependents per funcionario
        dep_count = {}
        for d in deps:
            fid = d.get('funcionario_id')
            dep_count[fid] = dep_count.get(fid, 0) + 1
        # Attach dep count and compute additional fields
        for f in funcs:
            fid = f.get('id')
            f['dependentes'] = dep_count.get(fid, 0)
            sal = float(f.get('salario', 0) or 0)
            f['salario_anual'] = round(sal * 13 + (sal / 12), 2)  # 13th + ferias 1/3
        self.send_json({'status': 'ok', 'funcionarios': funcs})

    # ---- RH Dashboard ----
    def api_rh_dashboard(self):
        import os, json
        result = {}
        try:
            out, _ = self.run_cobol('gerir_funcionarios', {'ACAO': 'listar'})
            funcs = json.loads(out).get('funcionarios', [])
        except:
            funcs = []
        try:
            out, _ = self.run_cobol('folha_pagamento', {'ACAO': 'holerites-listar'})
            holerites = json.loads(out).get('holerites', [])
        except:
            holerites = []
        try:
            out, _ = self.run_cobol('licenca', {'ACAO': 'listar'})
            licencas = json.loads(out).get('licencas', [])
        except:
            licencas = []
        try:
            out, _ = self.run_cobol('ponto', {'ACAO': 'listar'})
            pontos = json.loads(out).get('pontos', [])
        except:
            pontos = []

        total_func = len(funcs)
        total_holerites = len(holerites)
        total_pagar = sum(1 for h in holerites if h.get('situacao') == 'C')
        total_pago = sum(1 for h in holerites if h.get('situacao') != 'C')
        folha_total = sum(float(h.get('liquido', 0) or 0) for h in holerites)
        inss_total = sum(float(h.get('inss', 0) or 0) for h in holerites)
        irrf_total = sum(float(h.get('irrf', 0) or 0) for h in holerites)
        fgts_total = sum(float(h.get('fgts', 0) or 0) for h in holerites)

        # Licencas
        lic_ativas = sum(1 for l in licencas if l.get('status') == 'A')
        lic_pendentes = sum(1 for l in licencas if l.get('status') == 'P')

        # Contratos a vencer (funcionarios sem data_saida)
        from datetime import datetime as dt, timedelta
        hoje = dt.now().date()
        alertas_contrato = []
        for f in funcs:
            data_adm = f.get('data_admissao', '')
            if data_adm:
                try:
                    adm = dt.strptime(data_adm[:10], '%Y-%m-%d').date()
                    meses = (hoje.year - adm.year) * 12 + (hoje.month - adm.month)
                    if meses == 0: meses = 1
                    if meses % 12 == 0 and meses > 0:
                        alertas_contrato.append({
                            'funcionario_id': f.get('id'),
                            'nome': f.get('nome', ''),
                            'tipo': 'Aniversario de contrato',
                            'data': data_adm[:10],
                            'dias': 0,
                        })
                except: pass
            # Ferias vencidas
            data_ult_ferias = f.get('data_ultimas_ferias', '')
            if data_ult_ferias:
                try:
                    ult = dt.strptime(data_ult_ferias[:10], '%Y-%m-%d').date()
                    if (hoje - ult).days > 365:
                        alertas_contrato.append({
                            'funcionario_id': f.get('id'),
                            'nome': f.get('nome', ''),
                            'tipo': 'Ferias vencidas',
                            'data': data_ult_ferias[:10],
                            'dias': (hoje - ult).days - 365,
                        })
                except: pass

        # Ausencias por tipo
        ausencias_tipo = {}
        for l in licencas:
            t = l.get('tipo', 'Outros')
            ausencias_tipo[t] = ausencias_tipo.get(t, 0) + int(l.get('dias', 0) or 0)

        result = {
            'total_funcionarios': total_func,
            'total_holerites': total_holerites,
            'a_pagar': total_pagar,
            'pagos': total_pago,
            'folha_total': folha_total,
            'inss_total': inss_total,
            'irrf_total': irrf_total,
            'fgts_total': fgts_total,
            'licencas_ativas': lic_ativas,
            'licencas_pendentes': lic_pendentes,
            'alertas_contrato': alertas_contrato[:10],
            'ausencias_por_tipo': ausencias_tipo,
        }
        self.send_json({'status': 'ok', 'dashboard': result})

    # ---- Dependentes ----

    def api_dependentes(self, params):
        func_id = params.get('funcionario_id', ['0'])[0]
        if func_id and func_id != '0':
            out, err = self.run_cobol('dependentes', {'ACAO': 'listar-por-func', 'FUNCIONARIO_ID': func_id})
        else:
            out, err = self.run_cobol('dependentes', {'ACAO': 'listar'})
        try: self.send_json(json.loads(out))
        except: self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_dependente_incluir(self, params):
        out, err = self.run_cobol('dependentes', {
            'ACAO': 'incluir',
            'FUNCIONARIO_ID': params.get('funcionario_id', ['0'])[0],
            'NOME': params.get('nome', [''])[0],
            'CPF': params.get('cpf', [''])[0],
            'DATA_NASC': params.get('data_nasc', [''])[0],
            'TIPO': params.get('tipo', [''])[0],
        })
        if out and out.isdigit():
            self.send_json({'status': 'ok', 'id': int(out)})
        else:
            self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_dependente_alterar(self, params):
        out, err = self.run_cobol('dependentes', {
            'ACAO': 'alterar',
            'ID': params.get('id', ['0'])[0],
            'NOME': params.get('nome', [''])[0],
            'CPF': params.get('cpf', [''])[0],
            'DATA_NASC': params.get('data_nasc', [''])[0],
            'TIPO': params.get('tipo', [''])[0],
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro', 'mensagem': out if out != 'OK' else ''})

    def api_dependente_excluir(self, params):
        out, err = self.run_cobol('dependentes', {
            'ACAO': 'excluir',
            'ID': params.get('id', ['0'])[0],
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro', 'mensagem': out if out != 'OK' else ''})

    # ---- Ferias ----

    def api_folha_ferias(self):
        out, err = self.run_cobol('folha_pagamento', {'ACAO': 'ferias-listar'})
        try: self.send_json(json.loads(out))
        except: self.send_json({'status': 'erro', 'mensagem': out or err})

    def _calcular_ferias(self, salario_base, dias=30, dias_abono=0):
        valor_base = round(salario_base / 30 * dias, 2)
        um_terco = round(valor_base / 3, 2)
        abono = round(salario_base / 30 * dias_abono, 2) if dias_abono > 0 else 0
        abono_1_3 = round(abono / 3, 2) if abono > 0 else 0
        total_prov = valor_base + um_terco + abono + abono_1_3
        inss = self._calcular_inss(total_prov)
        irrf = self._calcular_irrf(total_prov, inss=inss)
        liquido = round(total_prov - inss - irrf, 2)
        return {'valor_base': valor_base, '1_3': um_terco, 'abono': abono,
                'abono_1_3': abono_1_3, 'inss': inss, 'irrf': irrf, 'liquido': liquido}

    def api_folha_ferias_incluir(self, params):
        func_id = params.get('funcionario_id', ['0'])[0]
        salario = float(params.get('salario_base', ['0'])[0] or 0)
        dias = int(params.get('dias', ['30'])[0] or 30)
        dias_abono = int(params.get('dias_abono', ['0'])[0] or 0)
        calc = self._calcular_ferias(salario, dias, dias_abono)
        out, err = self.run_cobol('folha_pagamento', {
            'ACAO': 'ferias-incluir',
            'FUNCIONARIO_ID': func_id,
            'NOME': params.get('nome', [''])[0],
            'AQUIS_INICIO': params.get('aquis_inicio', [''])[0],
            'AQUIS_FIM': params.get('aquis_fim', [''])[0],
            'INICIO': params.get('inicio', [''])[0],
            'FIM': params.get('fim', [''])[0],
            'DIAS': str(dias),
            'DIAS_ABONO': str(dias_abono),
            'VALOR_BASE': str(calc['valor_base']),
            '1_3': str(calc['1_3']),
            'ABONO': str(calc['abono']),
            'ABONO_1_3': str(calc['abono_1_3']),
            'INSS': str(calc['inss']),
            'IRRF': str(calc['irrf']),
            'LIQUIDO': str(calc['liquido']),
        })
        if out and out.isdigit():
            self.send_json({'status': 'ok', 'id': int(out), **calc})
        else:
            self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_folha_ferias_pagar(self, params):
        import datetime
        out, err = self.run_cobol('folha_pagamento', {
            'ACAO': 'ferias-pagar',
            'ID': params.get('id', ['0'])[0],
            'DATA_PAGAMENTO': datetime.date.today().isoformat(),
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro', 'mensagem': out if out != 'OK' else ''})

    def api_folha_ferias_excluir(self, params):
        out, err = self.run_cobol('folha_pagamento', {
            'ACAO': 'ferias-excluir',
            'ID': params.get('id', ['0'])[0],
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro', 'mensagem': out if out != 'OK' else ''})

    # ---- 13º ----

    def api_folha_decimos(self):
        out, err = self.run_cobol('folha_pagamento', {'ACAO': 'decimo-listar'})
        try: self.send_json(json.loads(out))
        except: self.send_json({'status': 'erro', 'mensagem': out or err})

    def _calcular_decimo(self, salario_base, meses=12, parcela='U'):
        valor_base = round(salario_base / 12 * meses, 2)
        inss = self._calcular_inss(valor_base)
        irrf = self._calcular_irrf(valor_base, inss=inss)
        liquido = round(valor_base - inss - irrf, 2)
        if parcela == '1':
            liquido = round(valor_base / 2, 2)
            inss = irrf = 0
        elif parcela == '2':
            inss = self._calcular_inss(valor_base)
            irrf = self._calcular_irrf(valor_base, inss=inss)
            liquido = round(valor_base - inss - irrf, 2)
        return {'valor_base': round(valor_base/2 if parcela=='1' else valor_base, 2) if parcela!='U' else valor_base,
                'inss': inss, 'irrf': irrf, 'liquido': liquido}

    def api_folha_decimo_incluir(self, params):
        salario = float(params.get('salario_base', ['0'])[0] or 0)
        meses = int(params.get('meses', ['12'])[0] or 12)
        parcela = params.get('parcela', ['U'])[0]
        calc = self._calcular_decimo(salario, meses, parcela)
        out, err = self.run_cobol('folha_pagamento', {
            'ACAO': 'decimo-incluir',
            'FUNCIONARIO_ID': params.get('funcionario_id', ['0'])[0],
            'NOME': params.get('nome', [''])[0],
            'ANO': params.get('ano', [''])[0],
            'PARCELA': parcela,
            'VALOR_BASE': str(calc['valor_base']),
            'INSS': str(calc['inss']),
            'IRRF': str(calc['irrf']),
            'LIQUIDO': str(calc['liquido']),
        })
        if out and out.isdigit():
            self.send_json({'status': 'ok', 'id': int(out), **calc})
        else:
            self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_folha_decimo_pagar(self, params):
        import datetime
        out, err = self.run_cobol('folha_pagamento', {
            'ACAO': 'decimo-pagar',
            'ID': params.get('id', ['0'])[0],
            'DATA_PAGAMENTO': datetime.date.today().isoformat(),
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro', 'mensagem': out if out != 'OK' else ''})

    def api_folha_decimo_excluir(self, params):
        out, err = self.run_cobol('folha_pagamento', {
            'ACAO': 'decimo-excluir',
            'ID': params.get('id', ['0'])[0],
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro', 'mensagem': out if out != 'OK' else ''})

    # ---- Rescisão ----

    def api_folha_rescisoes(self):
        out, err = self.run_cobol('folha_pagamento', {'ACAO': 'rescisao-listar'})
        try: self.send_json(json.loads(out))
        except: self.send_json({'status': 'erro', 'mensagem': out or err})

    def _calcular_rescisao(self, salario_base, data_adm, data_deslig, saldo_dias=0,
                           ferias_venc_dias=0, ferias_prop_meses=0, aviso_dias=0):
        saldo = round(salario_base / 30 * saldo_dias, 2) if saldo_dias else 0
        fv = round(salario_base / 30 * ferias_venc_dias, 2)
        fv_1_3 = round(fv / 3, 2)
        fp = round(salario_base / 12 * ferias_prop_meses, 2)
        fp_1_3 = round(fp / 3, 2)
        dec13 = round(salario_base / 12 * ferias_prop_meses, 2)
        aviso_val = round(salario_base / 30 * aviso_dias, 2) if aviso_dias else 0
        total = saldo + fv + fv_1_3 + fp + fp_1_3 + dec13 + aviso_val
        fgts = round(total * 0.08, 2)
        multa = round(fgts * 0.40, 2)
        inss = self._calcular_inss(total)
        irrf = self._calcular_irrf(total, inss=inss)
        liquido = round(total - inss - irrf, 2)
        return {'saldo_salario': saldo, 'ferias_venc': fv, '1_3_ferias': fv_1_3,
                'ferias_prop': fp, '13_prop': dec13, 'fgts': fgts, 'multa_fgts': multa,
                'inss': inss, 'irrf': irrf, 'liquido': liquido}

    def api_folha_rescisao_incluir(self, params):
        salario = float(params.get('salario_base', ['0'])[0] or 0)
        calc = self._calcular_rescisao(salario, params.get('data_adm', [''])[0],
            params.get('data_deslig', [''])[0],
            int(params.get('saldo_dias', ['0'])[0] or 0),
            int(params.get('ferias_venc_dias', ['0'])[0] or 0),
            int(params.get('ferias_prop_meses', ['0'])[0] or 0),
            int(params.get('aviso_dias', ['0'])[0] or 0))
        out, err = self.run_cobol('folha_pagamento', {
            'ACAO': 'rescisao-incluir',
            'FUNCIONARIO_ID': params.get('funcionario_id', ['0'])[0],
            'NOME': params.get('nome', [''])[0],
            'DATA_DESLIG': params.get('data_deslig', [''])[0],
            'TIPO_AVISO': params.get('tipo_aviso', [''])[0],
            'DIAS_AVISO': params.get('aviso_dias', ['0'])[0],
            'SALDO_SALARIO': str(calc['saldo_salario']),
            'FERIAS_VENC': str(calc['ferias_venc']),
            'FERIAS_PROP': str(calc['ferias_prop']),
            '1_3_FERIAS': str(calc['1_3_ferias']),
            '13_PROP': str(calc['13_prop']),
            'FGTS': str(calc['fgts']),
            'MULTA_FGTS': str(calc['multa_fgts']),
            'INSS': str(calc['inss']),
            'IRRF': str(calc['irrf']),
            'LIQUIDO': str(calc['liquido']),
        })
        if out and out.isdigit():
            self.send_json({'status': 'ok', 'id': int(out), **calc})
        else:
            self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_folha_rescisao_pagar(self, params):
        import datetime
        out, err = self.run_cobol('folha_pagamento', {
            'ACAO': 'rescisao-pagar',
            'ID': params.get('id', ['0'])[0],
            'DATA_PAGAMENTO': datetime.date.today().isoformat(),
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro', 'mensagem': out if out != 'OK' else ''})

    def api_folha_rescisao_excluir(self, params):
        out, err = self.run_cobol('folha_pagamento', {
            'ACAO': 'rescisao-excluir',
            'ID': params.get('id', ['0'])[0],
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro', 'mensagem': out if out != 'OK' else ''})

    # ---- Contabilização ----

    def api_folha_contabilizar(self, params):
        competencia = params.get('competencia', [''])[0]
        competencia_filter = competencia.replace('/', '-')
        out, err = self.run_cobol('folha_pagamento', {'ACAO': 'holerite-listar'})
        try:
            data = json.loads(out)
            holerites = data.get('holerites', [])
            if competencia:
                holerites = [h for h in holerites if h.get('competencia', '').replace('/', '-') == competencia_filter or h.get('competencia', '') == competencia]
            total_prov = sum(float(h.get('proventos', 0)) for h in holerites)
            total_inss = sum(float(h.get('inss', 0)) for h in holerites)
            total_irrf = sum(float(h.get('irrf', 0)) for h in holerites)
            total_fgts = sum(float(h.get('fgts', 0)) for h in holerites)
            total_liq = sum(float(h.get('liquido', 0)) for h in holerites)
            total_emp = total_inss + total_irrf + total_fgts
            self.send_json({
                'status': 'ok',
                'competencia': competencia,
                'qtd': len(holerites),
                'total_proventos': total_prov,
                'total_inss': total_inss,
                'total_irrf': total_irrf,
                'total_fgts': total_fgts,
                'total_liquido': total_liq,
                'total_encargos_empregador': total_emp,
            })
        except Exception as e:
            self.send_json({'status': 'erro', 'mensagem': str(e)})

    def api_folha_contabilizar_gerar(self, params):
        import datetime
        competencia = params.get('competencia', [''])[0]
        if not competencia:
            self.send_json({'status': 'erro', 'mensagem': 'competencia obrigatoria'})
            return
        out_hol, err = self.run_cobol('folha_pagamento', {'ACAO': 'holerite-listar'})
        try:
            data = json.loads(out_hol)
            holerites = data.get('holerites', [])
            holerites = [h for h in holerites if h.get('competencia') == competencia]
            if not holerites:
                self.send_json({'status': 'erro', 'mensagem': 'Nenhum holerite para esta competencia'})
                return
            total_prov = sum(float(h.get('proventos', 0)) for h in holerites)
            total_inss = sum(float(h.get('inss', 0)) for h in holerites)
            total_irrf = sum(float(h.get('irrf', 0)) for h in holerites)
            total_fgts = sum(float(h.get('fgts', 0)) for h in holerites)
            total_liq = sum(float(h.get('liquido', 0)) for h in holerites)
            lancamentos = [
                {'data': datetime.date.today().isoformat(), 'descricao': f'Folha pagamento {competencia} - Proventos',
                 'debito': '3.1.1.001', 'credito': '2.1.1.001', 'valor': total_prov},
                {'data': datetime.date.today().isoformat(), 'descricao': f'Folha {competencia} - INSS',
                 'debito': '2.1.1.002', 'credito': '2.1.2.001', 'valor': total_inss},
                {'data': datetime.date.today().isoformat(), 'descricao': f'Folha {competencia} - IRRF',
                 'debito': '2.1.1.003', 'credito': '2.1.2.002', 'valor': total_irrf},
                {'data': datetime.date.today().isoformat(), 'descricao': f'Folha {competencia} - FGTS',
                 'debito': '3.2.1.001', 'credito': '2.1.3.001', 'valor': total_fgts},
                {'data': datetime.date.today().isoformat(), 'descricao': f'Folha {competencia} - Liquido',
                 'debito': '2.1.1.001', 'credito': '1.1.1.001', 'valor': total_liq},
            ]
            self.send_json({'status': 'ok', 'lancamentos': lancamentos})
        except Exception as e:
            self.send_json({'status': 'erro', 'mensagem': str(e)})

    # ---- Ponto Eletronico ----
    def api_ponto(self, params):
        env = {'ACAO': 'listar'}
        if params.get('funcionario_id'): env['FUNCIONARIO_ID'] = params['funcionario_id'][0]
        if params.get('data'): env['DATA'] = params['data'][0]
        out, err = self.run_cobol('ponto', env)
        if out:
            try: self.send_json(json.loads(out))
            except json.JSONDecodeError: self.send_json({'status': 'erro', 'mensagem': out})
        else: self.send_json({'status': 'erro', 'mensagem': err or 'vazio'})

    def api_ponto_dia(self, params):
        func = params.get('funcionario_id', [''])[0]
        data = params.get('data', [''])[0]
        if not func or not data:
            self.send_json({'status': 'erro', 'mensagem': 'funcionario_id e data obrigatorios'}); return
        out, err = self.run_cobol('ponto', {'ACAO': 'listar-dia', 'FUNCIONARIO_ID': func, 'DATA': data})
        if out:
            try: self.send_json(json.loads(out))
            except json.JSONDecodeError: self.send_json({'status': 'erro', 'mensagem': out})
        else: self.send_json({'status': 'erro', 'mensagem': err or 'vazio'})

    def api_ponto_espelho(self, params):
        func = params.get('funcionario_id', [''])[0]
        mes = params.get('mes', [''])[0]
        ano = params.get('ano', [''])[0]
        if not func or not mes or not ano:
            self.send_json({'status': 'erro', 'mensagem': 'funcionario_id, mes e ano obrigatorios'}); return
        out, err = self.run_cobol('ponto', {'ACAO': 'espelho', 'FUNCIONARIO_ID': func, 'MES': mes, 'ANO': ano})
        if out:
            try: self.send_json(json.loads(out))
            except json.JSONDecodeError: self.send_json({'status': 'erro', 'mensagem': out})
        else: self.send_json({'status': 'erro', 'mensagem': err or 'vazio'})

    def api_ponto_bater(self, params):
        func = params.get('funcionario_id', [''])[0]
        data = params.get('data', [''])[0]
        hora = params.get('hora', [''])[0]
        tipo = params.get('tipo', [''])[0]
        if not func or not data or not hora or not tipo:
            self.send_json({'status': 'erro', 'mensagem': 'funcionario_id, data, hora e tipo obrigatorios'}); return
        tipos_validos = {'entrada', 'almoco', 'volta', 'saida'}
        if tipo not in tipos_validos:
            self.send_json({'status': 'erro', 'mensagem': 'tipo deve ser entrada, almoco, volta ou saida'}); return
        out, err = self.run_cobol('ponto', {
            'ACAO': 'bater', 'FUNCIONARIO_ID': func, 'DATA': data, 'HORA': hora, 'TIPO': tipo
        })
        if out and out.isdigit():
            self.send_json({'status': 'ok', 'id': int(out), 'mensagem': 'Ponto registrado!'})
        else:
            self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_ponto_alterar(self, params):
        pid = params.get('id', ['0'])[0]
        if not pid:
            self.send_json({'status': 'erro', 'mensagem': 'id obrigatorio'}); return
        env = {'ACAO': 'alterar', 'ID': pid}
        for k in ('funcionario_id', 'data', 'entrada', 'saida_almoco', 'volta_almoco', 'saida'):
            if params.get(k): env[k.upper()] = params[k][0]
        out, err = self.run_cobol('ponto', env)
        if out == 'OK':
            self.send_json({'status': 'ok'})
        else:
            self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_ponto_excluir(self, params):
        pid = params.get('id', ['0'])[0]
        if not pid:
            self.send_json({'status': 'erro', 'mensagem': 'id obrigatorio'}); return
        out, err = self.run_cobol('ponto', {'ACAO': 'excluir', 'ID': pid})
        if out == 'OK':
            self.send_json({'status': 'ok'})
        else:
            self.send_json({'status': 'erro', 'mensagem': out or err})

    # ---- Contabilidade ----
    def api_contabilidade_rules(self):
        import json, os
        path = os.path.join(DIR, 'dados/contabilidade_rules.json')
        try:
            with open(path) as f:
                self.send_json(json.load(f))
        except FileNotFoundError:
            self.send_json({'rules': [], 'planocontas': [], 'funcionarios': [], 'holerites': []})

    def api_contabilidade_funcionarios(self):
        import json, os
        path = os.path.join(DIR, 'dados/contabilidade_rules.json')
        try:
            with open(path) as f:
                data = json.load(f)
            self.send_json({'funcionarios': data.get('funcionarios', [])})
        except FileNotFoundError:
            self.send_json({'funcionarios': []})

    def api_contabilidade_funcionarios_salvar(self, params):
        import json, os
        path = os.path.join(DIR, 'dados/contabilidade_rules.json')
        funcionarios_str = params.get('funcionarios', [''])[0]
        if not funcionarios_str:
            self.send_json({'status': 'erro', 'mensagem': 'funcionarios obrigatorio'}); return
        try:
            funcionarios = json.loads(funcionarios_str)
            with open(path) as f:
                data = json.load(f)
            data['funcionarios'] = funcionarios
            with open(path, 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.send_json({'status': 'ok'})
        except Exception as e:
            self.send_json({'status': 'erro', 'mensagem': str(e)})

    def api_contabilidade_holerites(self):
        import json, os
        path = os.path.join(DIR, 'dados/contabilidade_rules.json')
        try:
            with open(path) as f:
                data = json.load(f)
            self.send_json({'holerites': data.get('holerites', [])})
        except FileNotFoundError:
            self.send_json({'holerites': []})

    def api_contabilidade_holerites_salvar(self, params):
        import json, os
        path = os.path.join(DIR, 'dados/contabilidade_rules.json')
        holerites_str = params.get('holerites', [''])[0]
        if not holerites_str:
            self.send_json({'status': 'erro', 'mensagem': 'holerites obrigatorio'}); return
        try:
            holerites = json.loads(holerites_str)
            with open(path) as f:
                data = json.load(f)
            data['holerites'] = holerites
            with open(path, 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.send_json({'status': 'ok'})
        except Exception as e:
            self.send_json({'status': 'erro', 'mensagem': str(e)})

    def api_contabilidade_rules_salvar(self, params):
        import json, os
        path = os.path.join(DIR, 'dados/contabilidade_rules.json')
        rules_str = params.get('rules', [''])[0]
        planocontas_str = params.get('planocontas', [''])[0]
        try:
            data = {}
            if rules_str: data['rules'] = json.loads(rules_str)
            if planocontas_str: data['planocontas'] = json.loads(planocontas_str)
            if os.path.exists(path):
                with open(path) as f:
                    existing = json.load(f)
                if 'rules' not in data: data['rules'] = existing.get('rules', [])
                if 'planocontas' not in data: data['planocontas'] = existing.get('planocontas', [])
            with open(path, 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.send_json({'status': 'ok'})
        except Exception as e:
            self.send_json({'status': 'erro', 'mensagem': str(e)})

    def api_contabilidade_planocontas_incluir(self, params):
        import json, os
        path = os.path.join(DIR, 'dados/contabilidade_rules.json')
        codigo = params.get('codigo', [''])[0]
        nome = params.get('nome', [''])[0]
        tipo = params.get('tipo', [''])[0]
        if not codigo or not nome:
            self.send_json({'status': 'erro', 'mensagem': 'codigo e nome obrigatorios'}); return
        try:
            with open(path) as f:
                data = json.load(f)
            planos = data.get('planocontas', [])
            if any(p['codigo'] == codigo for p in planos):
                self.send_json({'status': 'erro', 'mensagem': 'Conta ja existe'}); return
            planos.append({'codigo': codigo, 'nome': nome, 'tipo': tipo or 'Outro'})
            data['planocontas'] = planos
            with open(path, 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.send_json({'status': 'ok'})
        except Exception as e:
            self.send_json({'status': 'erro', 'mensagem': str(e)})

    def api_contabilidade_planocontas_alterar(self, params):
        import json, os
        path = os.path.join(DIR, 'dados/contabilidade_rules.json')
        codigo_original = params.get('codigo_original', [''])[0]
        codigo = params.get('codigo', [''])[0]
        nome = params.get('nome', [''])[0]
        tipo = params.get('tipo', [''])[0]
        if not codigo_original:
            self.send_json({'status': 'erro', 'mensagem': 'codigo_original obrigatorio'}); return
        try:
            with open(path) as f:
                data = json.load(f)
            planos = data.get('planocontas', [])
            for p in planos:
                if p['codigo'] == codigo_original:
                    p['codigo'] = codigo or p['codigo']
                    p['nome'] = nome or p['nome']
                    p['tipo'] = tipo or p['tipo']
                    break
            else:
                self.send_json({'status': 'erro', 'mensagem': 'Conta nao encontrada'}); return
            data['planocontas'] = planos
            with open(path, 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.send_json({'status': 'ok'})
        except Exception as e:
            self.send_json({'status': 'erro', 'mensagem': str(e)})

    def api_contabilidade_planocontas_excluir(self, params):
        import json, os
        path = os.path.join(DIR, 'dados/contabilidade_rules.json')
        codigo = params.get('codigo', [''])[0]
        if not codigo:
            self.send_json({'status': 'erro', 'mensagem': 'codigo obrigatorio'}); return
        try:
            with open(path) as f:
                data = json.load(f)
            planos = [p for p in data.get('planocontas', []) if p['codigo'] != codigo]
            data['planocontas'] = planos
            with open(path, 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.send_json({'status': 'ok'})
        except Exception as e:
            self.send_json({'status': 'erro', 'mensagem': str(e)})

    def api_contabilidade_gerar(self, params):
        import json, os, datetime
        competencia = params.get('competencia', [''])[0]
        if not competencia:
            self.send_json({'status': 'erro', 'mensagem': 'competencia obrigatoria'}); return
        rules_path = os.path.join(DIR, 'dados/contabilidade_rules.json')
        try:
            with open(rules_path) as f:
                rules_data = json.load(f)
        except FileNotFoundError:
            self.send_json({'status': 'erro', 'mensagem': 'Configure as regras contabeis primeiro'}); return
        rules = {r['componente']: r for r in rules_data.get('rules', [])}
        funcs_map = {str(f['funcionario_id']): f for f in rules_data.get('funcionarios', [])}
        holerites_map = {str(h['holerite_id']): h for h in rules_data.get('holerites', [])}
        out, err = self.run_cobol('folha_pagamento', {'ACAO': 'holerite-listar'})
        try:
            data = json.loads(out)
            holerites = data.get('holerites', [])
            holerites = [h for h in holerites if h.get('competencia', '').replace('/', '-') == competencia.replace('/', '-') or h.get('competencia', '') == competencia]
        except Exception:
            holerites = []
        out_f, _ = self.run_cobol('folha_pagamento', {'ACAO': 'ferias-listar'})
        out_d, _ = self.run_cobol('folha_pagamento', {'ACAO': 'decimo-listar'})
        out_r, _ = self.run_cobol('folha_pagamento', {'ACAO': 'rescisao-listar'})
        try:
            ferias_list = json.loads(out_f).get('ferias', [])
        except: ferias_list = []
        try:
            decimos_list = json.loads(out_d).get('decimos', [])
        except: decimos_list = []
        try:
            rescisoes_list = json.loads(out_r).get('rescisoes', [])
        except: rescisoes_list = []

        lancamentos = []
        today = datetime.date.today().isoformat()

        def add_lancamento(componente, valor, descricao_extra='', func_id=None, holerite_id=None):
            rule = rules.get(componente)
            if not rule or not valor: return
            if rule['natureza'] == 'D':
                debito = rule['conta']; credito = '1.1.1.001'
            else:
                debito = '1.1.1.001'; credito = rule['conta']
            parceiro = rule.get('parceiro', '')
            desc = descricao_extra or f'{rule.get("conta_nome", componente)} {competencia}'
            if parceiro: desc += f' - {parceiro}'
            centro = rule.get('centro_custo', '')
            diario = ''
            regra = ''
            # Apply per-funcionario override
            if func_id and func_id in funcs_map:
                fc = funcs_map[func_id]
                if fc.get('diario_contabil'): diario = fc['diario_contabil']
                if fc.get('regra_distribuicao'): regra = fc['regra_distribuicao']
                if fc.get('centro_custo'): centro = fc['centro_custo']
            # Apply per-holerite override (highest priority)
            if holerite_id and holerite_id in holerites_map:
                hc = holerites_map[holerite_id]
                if hc.get('diario_contabil'): diario = hc['diario_contabil']
                if hc.get('regra_distribuicao'): regra = hc['regra_distribuicao']
                if hc.get('centro_custo'): centro = hc['centro_custo']
            lancamentos.append({
                'data': today,
                'descricao': desc,
                'debito': debito,
                'credito': credito,
                'valor': round(valor, 2),
                'centro_custo': centro,
                'parceiro': parceiro,
                'componente': componente,
                'diario_contabil': diario,
                'regra_distribuicao': regra,
            })

        for h in holerites:
            func_ref = f"#{h.get('funcionario_id','?')} {h.get('nome','')}"
            fid = str(h.get('funcionario_id', ''))
            hid = str(h.get('id', ''))
            add_lancamento('proventos', float(h.get('proventos', 0)), f'Proventos {func_ref} {competencia}', fid, hid)
            add_lancamento('inss_empregado', float(h.get('inss', 0)), f'INSS {func_ref} {competencia}', fid, hid)
            add_lancamento('irrf', float(h.get('irrf', 0)), f'IRRF {func_ref} {competencia}', fid, hid)
            add_lancamento('fgts', float(h.get('fgts', 0)), f'FGTS {func_ref} {competencia}', fid, hid)
            add_lancamento('liquido', float(h.get('liquido', 0)), f'Liquido {func_ref} {competencia}', fid, hid)
            inss_val = float(h.get('inss', 0))
            fgts_val = float(h.get('fgts', 0))
            add_lancamento('inss_empregador', inss_val, f'INSS Patronal {func_ref} {competencia}', fid, hid)
            add_lancamento('fgts_empregador', fgts_val, f'FGTS {func_ref} {competencia}', fid, hid)

        for f_ in ferias_list:
            comp = f_.get('competencia', '')
            if comp and competencia and comp != competencia and comp.replace('/', '-') != competencia.replace('/', '-'):
                continue
            func_ref = f"#{f_.get('funcionario_id','?')} {f_.get('nome','')}"
            fid = str(f_.get('funcionario_id', ''))
            add_lancamento('ferias', float(f_.get('valor_base', 0)), f'Ferias {func_ref}', fid)
            if float(f_.get('abono', 0)):
                add_lancamento('ferias_abono', float(f_.get('abono', 0)), f'Abono Ferias {func_ref}', fid)

        for d_ in decimos_list:
            comp = str(d_.get('ano', ''))
            if competencia and competencia.split('/')[1] != comp:
                continue
            func_ref = f"#{d_.get('funcionario_id','?')} {d_.get('nome','')}"
            fid = str(d_.get('funcionario_id', ''))
            add_lancamento('decimo_terceiro', float(d_.get('valor_base', 0)), f'13o Salario {func_ref} {d_.get("ano","")}', fid)

        for r_ in rescisoes_list:
            func_ref = f"#{r_.get('funcionario_id','?')} {r_.get('nome','')}"
            fid = str(r_.get('funcionario_id', ''))
            add_lancamento('rescisao_saldo', float(r_.get('saldo_salario', 0)), f'Rescisao Saldo {func_ref}', fid)
            add_lancamento('rescisao_ferias', float(r_.get('ferias', 0)), f'Rescisao Ferias {func_ref}', fid)
            add_lancamento('rescisao_decimo', float(r_.get('decimo_proporcional', 0)), f'Rescisao 13o {func_ref}', fid)
            add_lancamento('rescisao_multa', float(r_.get('multa_fgts', 0)), f'Multa FGTS {func_ref}', fid)

        if not lancamentos:
            self.send_json({'status': 'erro', 'mensagem': 'Nenhum lancamento gerado. Verifique a competencia.'})
            return

        self.send_json({'status': 'ok', 'lancamentos': lancamentos, 'total': len(lancamentos)})

    def api_contabilidade_lancamentos(self, params):
        self.send_json({'status': 'ok', 'lancamentos': [], 'mensagem': 'Use Gerar para criar lancamentos'})

    # ---- Estruturas Salariais ----
    def api_estruturas_salariais(self):
        import json, os
        path = os.path.join(DIR, 'dados/estruturas_salariais.json')
        try:
            with open(path) as f:
                self.send_json({'estruturas': json.load(f)})
        except FileNotFoundError:
            self.send_json({'estruturas': []})

    def _load_estruturas(self):
        import json, os
        path = os.path.join(DIR, 'dados/estruturas_salariais.json')
        try:
            with open(path) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_estruturas(self, estruturas):
        import json, os
        path = os.path.join(DIR, 'dados/estruturas_salariais.json')
        with open(path, 'w') as f:
            json.dump(estruturas, f, ensure_ascii=False, indent=2)

    def api_estrutura_salarial_incluir(self, params):
        nome = params.get('nome', [''])[0]
        if not nome:
            self.send_json({'status': 'erro', 'mensagem': 'nome obrigatorio'}); return
        estruturas = self._load_estruturas()
        new_id = max([e['id'] for e in estruturas], default=0) + 1
        componentes_str = params.get('componentes', ['[]'])[0]
        try:
            componentes = json.loads(componentes_str)
        except:
            componentes = []
        estruturas.append({
            'id': new_id,
            'nome': nome,
            'cargo': params.get('cargo', [''])[0],
            'departamento': params.get('departamento', [''])[0],
            'localidade': params.get('localidade', [''])[0],
            'componentes': componentes,
        })
        self._save_estruturas(estruturas)
        self.send_json({'status': 'ok', 'id': new_id})

    def api_estrutura_salarial_alterar(self, params):
        pid = params.get('id', ['0'])[0]
        if not pid:
            self.send_json({'status': 'erro', 'mensagem': 'id obrigatorio'}); return
        estruturas = self._load_estruturas()
        for e in estruturas:
            if str(e['id']) == pid or e['id'] == int(pid):
                if params.get('nome'): e['nome'] = params['nome'][0]
                if params.get('cargo'): e['cargo'] = params['cargo'][0]
                if params.get('departamento'): e['departamento'] = params['departamento'][0]
                if params.get('localidade'): e['localidade'] = params['localidade'][0]
                if params.get('componentes'):
                    try: e['componentes'] = json.loads(params['componentes'][0])
                    except: pass
                self._save_estruturas(estruturas)
                self.send_json({'status': 'ok'})
                return
        self.send_json({'status': 'erro', 'mensagem': 'Estrutura nao encontrada'})

    def api_estrutura_salarial_excluir(self, params):
        pid = params.get('id', ['0'])[0]
        if not pid:
            self.send_json({'status': 'erro', 'mensagem': 'id obrigatorio'}); return
        estruturas = self._load_estruturas()
        estruturas = [e for e in estruturas if str(e['id']) != pid and e['id'] != int(pid)]
        self._save_estruturas(estruturas)
        self.send_json({'status': 'ok'})

    def api_estrutura_salarial_calcular(self, params):
        """Calculate salary based on structure for preview."""
        import json, os
        estrutura_id = params.get('estrutura_id', ['0'])[0]
        salario_base = float(params.get('salario_base', ['0'])[0])
        horas_extras = float(params.get('horas_extras', ['0'])[0])
        vl_hora_extra = float(params.get('valor_hora_extra', ['0'])[0])
        faltas = int(params.get('faltas', ['0'])[0])
        percentual_vendas = 0
        if params.get('percentual_vendas'):
            try: percentual_vendas = float(params['percentual_vendas'][0])
            except: pass

        estruturas = self._load_estruturas()
        estrutura = None
        for e in estruturas:
            if str(e['id']) == estrutura_id or e['id'] == int(estrutura_id):
                estrutura = e; break
        if not estrutura:
            self.send_json({'status': 'erro', 'mensagem': 'Estrutura nao encontrada'}); return

        proventos = []
        descontos = []
        base_inss = salario_base
        base_irrf = salario_base

        for comp in sorted(estrutura.get('componentes', []), key=lambda x: x.get('ordem', 99)):
            formula = comp.get('formula', '')
            valor = 0.0
            nome = comp.get('nome', '')
            if formula == 'salario_base':
                valor = salario_base
            elif formula == 'fixo':
                valor = float(comp.get('fixo', 0))
            elif formula == 'percentual':
                valor = salario_base * float(comp.get('percentual', 0)) / 100.0
            elif formula == 'percentual_vendas':
                pct = float(comp.get('perc_vendas', 0))
                if pct <= 0 and percentual_vendas > 0: pct = percentual_vendas
                valor = salario_base * pct / 100.0
            elif formula == 'horas_extras':
                valor = horas_extras * vl_hora_extra
            elif formula == 'faltas':
                val_dia = salario_base / 30
                valor = -(val_dia * faltas)
            elif formula == 'tabela_inss':
                # Will be calculated after total proventos
                continue
            elif formula == 'tabela_irrf':
                # Will be calculated after total proventos and INSS
                continue

            entry = {'nome': nome, 'valor': round(valor, 2), 'formula': formula}
            if comp.get('tipo') == 'desconto':
                descontos.append(entry)
                if formula in ('faltas',): base_inss += valor  # faltas reduce base
            else:
                proventos.append(entry)
                if formula not in ('salario_base', 'faltas'):
                    base_inss += valor

        # Calculate INSS on total base
        total_prov = sum(p['valor'] for p in proventos)
        if total_prov > 0:
            inss_val = self._calcular_inss(total_prov)
            descontos.append({'nome': 'INSS', 'valor': round(inss_val, 2), 'formula': 'tabela_inss'})
            base_irrf = total_prov - inss_val

        # Calculate IRRF
        if base_irrf > 0:
            irrf_val = self._calcular_irrf(base_irrf, inss=inss_val)
            descontos.append({'nome': 'IRRF', 'valor': round(irrf_val, 2), 'formula': 'tabela_irrf'})

        total_proventos = round(sum(p['valor'] for p in proventos), 2)
        total_descontos = round(abs(sum(d['valor'] for d in descontos)), 2)
        liquido = round(total_proventos - total_descontos, 2)

        self.send_json({
            'status': 'ok',
            'proventos': proventos,
            'descontos': descontos,
            'total_proventos': total_proventos,
            'total_descontos': total_descontos,
            'liquido': liquido,
            'base_inss': round(base_inss, 2),
            'base_irrf': round(base_irrf, 2),
        })

    def api_usuarios(self):
        out, err = self.run_cobol('gerir_usuarios', {'ACAO': 'listar'})
        if out:
            try:
                self.send_json(json.loads(out))
            except json.JSONDecodeError:
                self.send_json({'status': 'erro', 'mensagem': out})
        else:
            self.send_json({'status': 'erro', 'mensagem': err or 'vazio'})

    def api_usuario_incluir(self, params):
        out, err = self.run_cobol('gerir_usuarios', {
            'ACAO': 'incluir',
            'NOME': params.get('nome', [''])[0],
            'USUARIO': params.get('usuario', [''])[0],
            'SENHA': params.get('senha', [''])[0],
            'NIVEL': params.get('nivel', ['A'])[0],
        })
        if out and out.isdigit():
            self.send_json({'status': 'ok', 'id': int(out)})
        else:
            self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_usuario_alterar(self, params):
        out, err = self.run_cobol('gerir_usuarios', {
            'ACAO': 'alterar',
            'ID': params.get('id', ['0'])[0],
            'NOME': params.get('nome', [''])[0],
            'USUARIO': params.get('usuario', [''])[0],
            'SENHA': params.get('senha', [''])[0],
            'NIVEL': params.get('nivel', [''])[0],
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro',
                        'mensagem': out if out != 'OK' else ''})

    def api_usuario_excluir(self, params):
        out, err = self.run_cobol('gerir_usuarios', {
            'ACAO': 'excluir',
            'ID': params.get('id', ['0'])[0],
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro',
                        'mensagem': out if out != 'OK' else ''})

    def api_atributos(self, params):
        produto_id = params.get('produto_id', [''])[0]
        if produto_id:
            out, err = self.run_cobol('gerir_atributos', {
                'ACAO': 'listar-por-produto', 'PRODUTO_ID': produto_id
            })
        else:
            out, err = self.run_cobol('gerir_atributos', {'ACAO': 'listar'})
        if out:
            try:
                self.send_json(json.loads(out))
            except json.JSONDecodeError:
                self.send_json({'status': 'erro', 'mensagem': out})
        else:
            self.send_json({'status': 'erro', 'mensagem': err or 'vazio'})

    def api_atributo_incluir(self, params):
        out, err = self.run_cobol('gerir_atributos', {
            'ACAO': 'incluir',
            'PRODUTO_ID': params.get('produto_id', ['0'])[0],
            'NOME': params.get('nome', [''])[0],
            'VALOR': params.get('valor', [''])[0],
        })
        if out and out.isdigit():
            self.send_json({'status': 'ok', 'id': int(out)})
        else:
            self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_atributo_alterar(self, params):
        out, err = self.run_cobol('gerir_atributos', {
            'ACAO': 'alterar',
            'ID': params.get('id', ['0'])[0],
            'NOME': params.get('nome', [''])[0],
            'VALOR': params.get('valor', [''])[0],
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro',
                        'mensagem': out if out != 'OK' else ''})

    def api_atributo_excluir(self, params):
        out, err = self.run_cobol('gerir_atributos', {
            'ACAO': 'excluir',
            'ID': params.get('id', ['0'])[0],
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro',
                        'mensagem': out if out != 'OK' else ''})

    def api_ncm(self, params):
        q = params.get('q', [''])[0].strip().lower()
        try:
            with open(os.path.join(DIR, 'dados/ncm.json')) as f:
                data = json.load(f)
        except FileNotFoundError:
            self.send_json({'ncm': [], 'total': 0})
            return
        if not q:
            self.send_json({'ncm': data[:20], 'total': len(data)})
            return
        results = [n for n in data if q in n['codigo'].lower() or q in n['descricao'].lower()]
        self.send_json({'ncm': results[:20], 'total': len(results)})

    def api_produto_imagens(self, params):
        produto_id = params.get('produto_id', [''])[0]
        if not produto_id:
            self.send_json({'imagens': [], 'total': 0})
            return
        out, err = self.run_cobol('gerir_imagens', {
            'ACAO': 'listar-por-produto', 'PRODUTO_ID': produto_id
        })
        if out:
            try:
                self.send_json(json.loads(out))
            except json.JSONDecodeError:
                self.send_json({'status': 'erro', 'mensagem': out})
        else:
            self.send_json({'status': 'erro', 'mensagem': err or 'vazio'})

    def api_produto_imagem_incluir(self, params):
        out, err = self.run_cobol('gerir_imagens', {
            'ACAO': 'incluir',
            'PRODUTO_ID': params.get('produto_id', ['0'])[0],
            'CAMINHO': params.get('caminho', [''])[0],
            'ORDEM': params.get('ordem', ['1'])[0],
        })
        if out and out.isdigit():
            self.send_json({'status': 'ok', 'id': int(out)})
        else:
            self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_produto_imagem_excluir(self, params):
        out, err = self.run_cobol('gerir_imagens', {
            'ACAO': 'excluir',
            'ID': params.get('id', ['0'])[0],
        })
        self.send_json({'status': 'ok' if out == 'OK' else 'erro',
                        'mensagem': out if out != 'OK' else ''})

    def api_pedidos_pendentes(self):
        try:
            with open(os.path.join(DIR, 'dados/vendas.json')) as f:
                data = json.load(f)
        except FileNotFoundError:
            self.send_json({'pedidos': [], 'total': 0})
            return
        pendentes = [v for v in data.get('vendas', []) if v.get('forma_pg') == 'PENDENTE']
        self.send_json({'pedidos': pendentes, 'total': len(pendentes)})

    def api_pedido_finalizar(self, params):
        pedido_id = params.get('id', ['0'])[0]
        forma_pg = params.get('forma_pg', [''])[0]
        if not forma_pg:
            self.send_json({'status': 'erro', 'mensagem': 'forma_pg obrigatoria'})
            return
        out, err = self.run_cobol('finalizar_pedido', {
            'ID': pedido_id, 'FORMA_PG': forma_pg
        })
        if out == 'OK':
            subprocess.run(['./batch_json_vendas'], capture_output=True, cwd=DIR)
            self.send_json({'status': 'ok'})
        else:
            self.send_json({'status': 'erro', 'mensagem': out or err})

    def api_nfe_fornecedor_importar(self, body):
        try:
            from fiscal.importar_nfe import parse_nfe_xml, importar_nfe_entrada
            import json

            parsed = parse_nfe_xml(body)
            fornecedor_data = parsed.get('fornecedor', {})
            cnpj = fornecedor_data.get('cnpj', '')
            nome = fornecedor_data.get('nome', '')

            # 1. Auto-criar fornecedor se nao existir
            if cnpj and nome:
                out_forn, _ = self.run_cobol('gerir_fornecedores', {
                    'ACAO': 'buscar-cnpj', 'CNPJ': cnpj
                })
                if out_forn:
                    try:
                        forn_exist = json.loads(out_forn)
                    except json.JSONDecodeError:
                        forn_exist = {}
                    if forn_exist.get('status') != 'ok':
                        self.run_cobol('gerir_fornecedores', {
                            'ACAO': 'incluir',
                            'NOME': nome[:60],
                            'CNPJ': cnpj[:18],
                            'ENDERECO': parsed.get('endereco', '')[:60],
                            'IE': fornecedor_data.get('ie', '')[:20],
                        })
                        subprocess.run(['./batch_json_fornecedores'], capture_output=True, cwd=DIR)

            # 2. Registrar entrada no nfe_entrada.json
            parsed, is_new = importar_nfe_entrada(body, os.path.join(DIR, 'dados'))

            # 3. Para cada item: atualizar estoque ou criar produto
            ids_adicionados = []
            for item in parsed.get('itens', []):
                nome_item = item.get('nome', '').strip()
                if not nome_item:
                    continue
                qtd = float(item.get('quantidade', 0))
                preco_custo = float(item.get('vl_unitario', 0))
                ean = item.get('ean', '')
                ncm = item.get('ncm', '')
                cfop = item.get('cfop', '5102')
                cst = item.get('icms_cst', item.get('icms_csosn', '400'))
                icms_alq = item.get('icms_aliquota', '0')

                # Check if product exists by nome or EAN
                produto_existe = None
                with open(os.path.join(DIR, 'dados/produtos.json')) as f:
                    prods_data = json.load(f)
                for p in prods_data.get('produtos', []):
                    if (ean and p.get('codigo_barras', '') == ean) or \
                       (p.get('nome', '').strip().lower() == nome_item.lower()):
                        produto_existe = p
                        break

                if produto_existe:
                    stock_atual = float(produto_existe.get('stock', 0))
                    novo_stock = int(stock_atual + qtd)
                    self.run_cobol('cadastrar_produto', {
                        'ACAO': 'alterar',
                        'ID': str(produto_existe['id']),
                        'STOCK': str(novo_stock),
                        'PRECO_CUSTO': str(preco_custo),
                        'FORNECEDOR': nome[:50],
                    })
                    ids_adicionados.append(produto_existe['id'])
                else:
                    preco_venda = round(preco_custo * 1.3, 2)
                    out_new, _ = self.run_cobol('cadastrar_produto', {
                        'ACAO': 'incluir',
                        'NOME': nome_item,
                        'PRECO': str(preco_venda),
                        'PRECO_CUSTO': str(preco_custo),
                        'STOCK': str(int(qtd)),
                        'NCM': ncm,
                        'CFOP': cfop,
                        'CST': cst,
                        'ICMS_ALQ': icms_alq,
                        'UNIDADE': item.get('unidade', 'UN'),
                        'CODIGO_BARRAS': ean,
                        'CATEGORIA': 'Importado',
                        'SUB_CATEGORIA': 'Geral',
                        'MARGEM': '30',
                        'FORNECEDOR': nome[:50],
                    })
                    if out_new and out_new.isdigit():
                        ids_adicionados.append(int(out_new))

            subprocess.run(['./batch_fix_produtos.py'], capture_output=True, cwd=DIR)

            # 4. Gerar fatura (conta a pagar)
            chave = parsed.get('chave', '')
            vNF = parsed.get('total', {}).get('vNF', '0')
            data_emissao = parsed.get('data_emissao', datetime.now().strftime('%Y-%m-%d'))

            faturas_path = os.path.join(DIR, 'dados/faturas.json')
            try:
                with open(faturas_path) as f:
                    faturas_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                faturas_data = {'faturas': [], 'total': 0, 'total_pendente': 0, 'total_pago': 0}

            if not any(f.get('chave') == chave for f in faturas_data.get('faturas', [])):
                nova_fatura = {
                    'id': len(faturas_data['faturas']) + 1,
                    'chave': chave,
                    'fornecedor': nome,
                    'fornecedor_cnpj': cnpj,
                    'numero_nf': parsed.get('numero', ''),
                    'valor': float(vNF),
                    'data_emissao': data_emissao,
                    'data_vencimento': (datetime.strptime(data_emissao[:10], '%Y-%m-%d') + timedelta(days=30)).strftime('%Y-%m-%d'),
                    'data_importacao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'status': 'PENDENTE',
                }
                faturas_data['faturas'].append(nova_fatura)
                faturas_data['total'] = len(faturas_data['faturas'])
                total_pend = sum(f['valor'] for f in faturas_data['faturas'] if f['status'] == 'PENDENTE')
                total_pago = sum(f['valor'] for f in faturas_data['faturas'] if f['status'] == 'PAGO')
                faturas_data['total_pendente'] = round(total_pend, 2)
                faturas_data['total_pago'] = round(total_pago, 2)
                with open(faturas_path, 'w') as f:
                    json.dump(faturas_data, f, ensure_ascii=False, indent=2)

            self.send_json({
                'status': 'ok',
                'chave': chave,
                'fornecedor': parsed.get('fornecedor', {}),
                'itens_qtde': len(parsed.get('itens', [])),
                'total': parsed.get('total', {}),
                'produtos_atualizados': ids_adicionados,
            })
        except Exception as e:
            self.send_json({'status': 'erro', 'mensagem': str(e)})

    def api_nfe_fornecedor_listar(self):
        path = os.path.join(DIR, 'dados/nfe_entrada.json')
        try:
            with open(path) as f:
                import json
                data = json.load(f)
            data['total'] = len(data.get('nfe_entradas', []))
            self.send_json(data)
        except FileNotFoundError:
            self.send_json({'nfe_entradas': [], 'total': 0})

    def api_fornecedores(self):
        out, err = self.run_cobol('gerir_fornecedores', {'ACAO': 'listar'})
        if out:
            try:
                import json
                self.send_json(json.loads(out))
            except json.JSONDecodeError:
                self.send_json({'status': 'erro', 'mensagem': out})
        else:
            self.send_json({'status': 'erro', 'mensagem': err or 'vazio'})

    def api_planocontas(self):
        path = os.path.join(DIR, 'dados/planocontas.json')
        try:
            with open(path) as f:
                import json
                self.send_json(json.load(f))
        except FileNotFoundError:
            self.send_json({'contas': [], 'total': 0})

    def api_diarios(self):
        path = os.path.join(DIR, 'dados/diarios.json')
        try:
            with open(path) as f:
                import json
                self.send_json(json.load(f))
        except FileNotFoundError:
            self.send_json({'lancamentos': [], 'total': 0})

    def api_diario_lancar(self, params):
        conta_debito = params.get('debito', [''])[0]
        conta_credito = params.get('credito', [''])[0]
        valor_str = params.get('valor', ['0'])[0]
        descricao = params.get('descricao', [''])[0]
        data = params.get('data', [datetime.now().strftime('%Y-%m-%d')])[0]
        if not conta_debito or not conta_credito:
            self.send_json({'status': 'erro', 'mensagem': 'Conta debito e credito obrigatorias'})
            return
        try:
            valor = float(valor_str)
        except ValueError:
            self.send_json({'status': 'erro', 'mensagem': 'Valor invalido'})
            return
        path = os.path.join(DIR, 'dados/diarios.json')
        import json
        try:
            with open(path) as f:
                data_json = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data_json = {'lancamentos': []}
        novo_id = max([l.get('id', 0) for l in data_json.get('lancamentos', [])], default=0) + 1
        lancamento = {
            'id': novo_id,
            'data': data,
            'descricao': descricao,
            'debito': conta_debito,
            'credito': conta_credito,
            'valor': round(valor, 2),
            'data_lancamento': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        data_json['lancamentos'].append(lancamento)
        data_json['total'] = len(data_json['lancamentos'])
        with open(path, 'w') as f:
            json.dump(data_json, f, ensure_ascii=False, indent=2)
        self.send_json({'status': 'ok', 'id': novo_id})

    def api_faturas_listar(self):
        path = os.path.join(DIR, 'dados/faturas.json')
        try:
            with open(path) as f:
                import json
                self.send_json(json.load(f))
        except FileNotFoundError:
            self.send_json({'faturas': [], 'total': 0, 'total_pendente': 0, 'total_pago': 0})

    def api_fatura_pagar(self, params):
        fatura_id = params.get('id', [''])[0]
        path = os.path.join(DIR, 'dados/faturas.json')
        try:
            with open(path) as f:
                import json
                data = json.load(f)
            for fat in data.get('faturas', []):
                if str(fat.get('id', '')) == fatura_id:
                    fat['status'] = 'PAGO'
                    fat['data_pagamento'] = datetime.now().strftime('%Y-%m-%d')
                    total_pend = sum(f['valor'] for f in data['faturas'] if f['status'] == 'PENDENTE')
                    total_pago = sum(f['valor'] for f in data['faturas'] if f['status'] == 'PAGO')
                    data['total_pendente'] = round(total_pend, 2)
                    data['total_pago'] = round(total_pago, 2)
                    with open(path, 'w') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    self.send_json({'status': 'ok'})
                    return
            self.send_json({'status': 'erro', 'mensagem': 'Fatura nao encontrada'})
        except (FileNotFoundError, json.JSONDecodeError):
            self.send_json({'status': 'erro', 'mensagem': 'Nenhuma fatura'})

if __name__ == '__main__':
    os.chdir(DIR)
    srv = http.server.HTTPServer(('', PORT), POSHandler)
    print(f'Servidor: http://localhost:{PORT}')
    print(f'POS:      http://localhost:{PORT}/pos.html')
    print(f'API:      http://localhost:{PORT}/api/produtos')
    srv.serve_forever()
