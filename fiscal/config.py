import os
import json

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CRT_MAP = {
    'Simples Nacional': 1,
    'Simples Nacional (Excesso)': 2,
    'Lucro Presumido': 3,
    'ME': 1,
    'EPP': 1,
    'Lucro Real': 3,
}

class FiscalConfig:
    def __init__(self):
        self.nome = ''
        self.cnpj = ''
        self.endereco = ''
        self.telefone = ''
        self.email = ''
        self.inscricao_est = ''
        self.cnpj_status = ''
        self.certificado = ''
        self.cert_senha = ''
        self.tipo_fiscal = ''
        self.cnae_prim_codigo = ''
        self.cnae_prim_desc = ''
        self.cnae_sec_codigos = ''
        self.cnae_sec_desc = ''
        self.crt = 1
        self.chave_pix = ''
        self.cod_municipio = ''
        self.inscricao_mun = ''
        self.uf = 43
        self.ambiente = 2
        self.serie_nfce = 1
        self.serie_nfe = 1
        self.proximo_numero_nfce = 1
        self.proximo_numero_nfe = 1

    def carregar(self):
        try:
            with open(os.path.join(DIR, 'dados/empresa.json')) as f:
                emp = json.load(f)
                for k, v in emp.items():
                    if hasattr(self, k):
                        setattr(self, k, v)
            self.crt = CRT_MAP.get(self.tipo_fiscal, 1)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        try:
            with open(os.path.join(DIR, 'dados/numeracao.json')) as f:
                num = json.load(f)
                self.ambiente = num.get('ambiente', 2)
                self.serie_nfce = num.get('serie_nfce', 1)
                self.serie_nfe = num.get('serie_nfe', 1)
                self.proximo_numero_nfce = num.get('proximo_numero_nfce', 1)
                self.proximo_numero_nfe = num.get('proximo_numero_nfe', 1)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return self

    def to_dict(self):
        return {
            'nome': self.nome,
            'cnpj': self.cnpj,
            'endereco': self.endereco,
            'inscricao_est': self.inscricao_est,
            'tipo_fiscal': self.tipo_fiscal,
            'crt': self.crt,
            'cnae_prim_codigo': self.cnae_prim_codigo,
            'cnae_prim_desc': self.cnae_prim_desc,
            'cnae_sec_codigos': self.cnae_sec_codigos,
            'cnae_sec_desc': self.cnae_sec_desc,
            'certificado': self.certificado,
            'cert_senha': bool(self.cert_senha),
            'cod_municipio': self.cod_municipio,
            'inscricao_mun': self.inscricao_mun,
            'uf': self.uf,
            'ambiente': self.ambiente,
            'serie_nfce': self.serie_nfce,
            'serie_nfe': self.serie_nfe,
            'proximo_numero_nfce': self.proximo_numero_nfce,
            'proximo_numero_nfe': self.proximo_numero_nfe,
        }
