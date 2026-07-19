import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.x509 import load_pem_x509_certificate

class CertificadoA1:
    def __init__(self, caminho=None, senha=None):
        self.caminho = caminho
        self.senha = senha
        self.certificado = None
        self.chave_privada = None
        self.valido = False
        self.validade = None
        self.cnpj = ''
        self.nome = None

    def carregar(self):
        if not self.caminho or not os.path.isfile(self.caminho):
            raise FileNotFoundError(f"Certificado nao encontrado: {self.caminho}")
        with open(self.caminho, 'rb') as f:
            pfx_data = f.read()
        try:
            private_key, certificate, _ = pkcs12.load_key_and_certificates(
                pfx_data, self.senha.encode() if self.senha else None
            )
        except Exception:
            raise ValueError("Erro ao ler certificado A1 (PFX/P12). Verifique a senha.")
        if certificate is None:
            raise ValueError("Nenhum certificado encontrado no arquivo.")
        self.certificado = certificate
        self.chave_privada = private_key
        self.validade = certificate.not_valid_after
        self.valido = True
        cn_parts = []
        for attr in certificate.subject:
            if attr.oid._name == 'commonName':
                cn = attr.value or ''
                cn_parts.append(cn)
                if ':' in cn:
                    self.nome, _, cnpj_candidate = cn.partition(':')
                    if cnpj_candidate.isdigit() and len(cnpj_candidate) == 14:
                        self.cnpj = cnpj_candidate
                    else:
                        self.nome = cn
        if not self.nome and cn_parts:
            self.nome = cn_parts[0]
        return self

    def obter_cnpj(self):
        return self.cnpj
