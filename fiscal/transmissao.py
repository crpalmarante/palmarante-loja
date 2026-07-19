import requests
from lxml import etree
from requests import Session

SEFAZ_AMBIENTES = {
    'nfce': {
        2: {
            12: 'https://homnfce.sefaz.ac.gov.br/ws/NfceAutorizacaoService',
            27: 'https://hf.nfce.sefaz.al.gov.br/ws/NfceAutorizacaoService',
            13: 'https://homnfce.sefaz.am.gov.br/ws/NfceAutorizacaoService',
            16: 'https://hml.nfce.fazenda.ap.gov.br/ws/NfceAutorizacaoService',
            29: 'https://hml.sefaz.ba.gov.br/ws/NfceAutorizacaoService',
            23: 'https://hmlnfce.sefaz.ce.gov.br/ws/NfceAutorizacaoService',
            53: 'https://homnfce.sefaz.df.gov.br/ws/NfceAutorizacaoService',
            32: 'https://homologacao.sefaz.es.gov.br/ws/NfceAutorizacaoService',
            52: 'https://homolog.sefaz.go.gov.br/ws/NfceAutorizacaoService',
            21: 'https://hmlnfce.sefaz.ma.gov.br/ws/NfceAutorizacaoService',
            31: 'https://homnfce.sefaz.mg.gov.br/ws/NfceAutorizacaoService',
            50: 'https://homnfce.sefaz.ms.gov.br/ws/NfceAutorizacaoService',
            51: 'https://homnfce.sefaz.mt.gov.br/ws/NfceAutorizacaoService',
            15: 'https://homnfce.sefaz.pa.gov.br/ws/NfceAutorizacaoService',
            25: 'https://hom.nfce.sefaz.pb.gov.br/ws/NfceAutorizacaoService',
            26: 'https://homnfce.sefaz.pe.gov.br/ws/NfceAutorizacaoService',
            22: 'https://homnfce.sefaz.pi.gov.br/ws/NfceAutorizacaoService',
            41: 'https://homologacao.nfce.sefa.pr.gov.br/ws/NfceAutorizacaoService',
            33: 'https://nfc-homologacao.sefaz.rj.gov.br/ws/NfceAutorizacaoService',
            24: 'https://hom.nfce.sefaz.rn.gov.br/ws/NfceAutorizacaoService',
            11: 'https://homnfce.sefaz.ro.gov.br/ws/NfceAutorizacaoService',
            14: 'https://nfce-homologacao.sefaz.rr.gov.br/ws/NfceAutorizacaoService',
            43: 'https://hom1.nfce.fazenda.rs.gov.br/ws/NfceAutorizacaoService',
            42: 'https://nfce-homologacao.sefaz.sc.gov.br/ws/NfceAutorizacaoService',
            28: 'https://hml.nfce.sefaz.se.gov.br/ws/NfceAutorizacaoService',
            35: 'https://homologacao.nfce.fazenda.sp.gov.br/ws/NfceAutorizacaoService',
            17: 'https://homolog.sefaz.to.gov.br/ws/NfceAutorizacaoService',
        },
        1: {
            12: 'https://nfce.sefaz.ac.gov.br/ws/NfceAutorizacaoService',
            27: 'https://nfce.sefaz.al.gov.br/ws/NfceAutorizacaoService',
            13: 'https://nfce.sefaz.am.gov.br/ws/NfceAutorizacaoService',
            16: 'https://nfce.fazenda.ap.gov.br/ws/NfceAutorizacaoService',
            29: 'https://nfce.sefaz.ba.gov.br/ws/NfceAutorizacaoService',
            23: 'https://nfce.sefaz.ce.gov.br/ws/NfceAutorizacaoService',
            53: 'https://nfce.sefaz.df.gov.br/ws/NfceAutorizacaoService',
            32: 'https://nfce.sefaz.es.gov.br/ws/NfceAutorizacaoService',
            52: 'https://nfce.sefaz.go.gov.br/ws/NfceAutorizacaoService',
            21: 'https://nfce.sefaz.ma.gov.br/ws/NfceAutorizacaoService',
            31: 'https://nfce.sefaz.mg.gov.br/ws/NfceAutorizacaoService',
            50: 'https://nfce.sefaz.ms.gov.br/ws/NfceAutorizacaoService',
            51: 'https://nfce.sefaz.mt.gov.br/ws/NfceAutorizacaoService',
            15: 'https://nfce.sefaz.pa.gov.br/ws/NfceAutorizacaoService',
            25: 'https://nfce.sefaz.pb.gov.br/ws/NfceAutorizacaoService',
            26: 'https://nfce.sefaz.pe.gov.br/ws/NfceAutorizacaoService',
            22: 'https://nfce.sefaz.pi.gov.br/ws/NfceAutorizacaoService',
            41: 'https://nfce.sefa.pr.gov.br/ws/NfceAutorizacaoService',
            33: 'https://nfce.sefaz.rj.gov.br/ws/NfceAutorizacaoService',
            24: 'https://nfce.sefaz.rn.gov.br/ws/NfceAutorizacaoService',
            11: 'https://nfce.sefaz.ro.gov.br/ws/NfceAutorizacaoService',
            14: 'https://nfce.sefaz.rr.gov.br/ws/NfceAutorizacaoService',
            43: 'https://nfe.fazenda.rs.gov.br/ws/NfceAutorizacaoService',
            42: 'https://nfce.sefaz.sc.gov.br/ws/NfceAutorizacaoService',
            28: 'https://nfce.sefaz.se.gov.br/ws/NfceAutorizacaoService',
            35: 'https://nfce.fazenda.sp.gov.br/ws/NfceAutorizacaoService',
            17: 'https://nfce.sefaz.to.gov.br/ws/NfceAutorizacaoService',
        },
    },
    'nfe': {
        2: {
            12: 'https://hom1.sefaz.ac.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            27: 'https://hom.sefaz.al.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            13: 'https://hom1.sefaz.am.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            29: 'https://hom.sefaz.ba.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            23: 'https://hom1.sefaz.ce.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            53: 'https://hom1.sefaz.df.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            32: 'https://homologacao.sefaz.es.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            52: 'https://homolog.sefaz.go.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            21: 'https://hom.sefaz.ma.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            31: 'https://hom1.sefaz.mg.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            50: 'https://hom.sefaz.ms.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            51: 'https://hom1.sefaz.mt.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            25: 'https://hom.sefaz.pb.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            26: 'https://hom1.sefaz.pe.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            22: 'https://hom.sefaz.pi.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            41: 'https://hom1.sefa.pr.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            33: 'https://hom1.sefaz.rj.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            24: 'https://hom.sefaz.rn.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            11: 'https://hom.sefaz.ro.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            14: 'https://hom.sefaz.rr.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            43: 'https://hom1.sefaz.rs.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            42: 'https://hom1.sefaz.sc.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            28: 'https://hom.sefaz.se.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            35: 'https://hom1.sefaz.sp.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            17: 'https://hom.sefaz.to.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
        },
        1: {
            12: 'https://sefaz.ac.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            27: 'https://sefaz.al.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            13: 'https://sefaz.am.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            29: 'https://sefaz.ba.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            23: 'https://sefaz.ce.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            53: 'https://sefaz.df.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            32: 'https://sefaz.es.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            52: 'https://sefaz.go.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            21: 'https://sefaz.ma.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            31: 'https://sefaz.mg.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            50: 'https://sefaz.ms.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            51: 'https://sefaz.mt.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            25: 'https://sefaz.pb.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            26: 'https://sefaz.pe.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            22: 'https://sefaz.pi.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            41: 'https://sefa.pr.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            33: 'https://sefaz.rj.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            24: 'https://sefaz.rn.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            11: 'https://sefaz.ro.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            43: 'https://nfe.sefaz.rs.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            42: 'https://sefaz.sc.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            28: 'https://sefaz.se.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            35: 'https://nfe.fazenda.sp.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
            17: 'https://sefaz.to.gov.br/WS/NfeAutorizacao/NFeAutorizacao.asmx',
        },
    },
}

def get_wsdl(modelo='nfce', uf=43, ambiente=2):
    mapa = SEFAZ_AMBIENTES.get(modelo, {}).get(ambiente, {})
    base = mapa.get(uf)
    if not base:
        raise ValueError(f'{modelo.upper()} UF {uf} ambiente {ambiente} nao configurado')
    return base

def transmitir_lote(xml_assinado, modelo='nfce', uf=43, ambiente=2, certificado=None, cert_senha=''):
    from fiscal.certificado import CertificadoA1
    if isinstance(certificado, str) and certificado:
        cert = CertificadoA1(certificado, cert_senha)
        cert.carregar()
        if not cert.valido:
            raise ValueError('Certificado invalido')
        certificado = cert

    session = Session()
    if certificado and certificado.caminho:
        session.cert = (certificado.caminho, None)
    session.verify = False

    wsdl_url = get_wsdl(modelo, uf, ambiente)

    from lxml import etree as letree
    xml_doc = letree.fromstring(xml_assinado.encode())

    corpo = etree.tostring(xml_doc, encoding='UTF-8').decode()

    soap_env = f'''<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
               xmlns:xsd="http://www.w3.org/2001/XMLSchema"
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <soap:Header>
    <nfeCabecMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/NfeAutorizacaoService">
      <versaoDados>4.00</versaoDados>
      <cUF>{uf}</cUF>
    </nfeCabecMsg>
  </soap:Header>
  <soap:Body>
    <nfeAutorizacaoLote xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/NfeAutorizacaoService">
      <nfeDadosMsg>{corpo}</nfeDadosMsg>
    </nfeAutorizacaoLote>
  </soap:Body>
</soap:Envelope>'''

    headers = {
        'Content-Type': 'application/soap+xml;charset=UTF-8',
        'SOAPAction': 'http://www.portalfiscal.inf.br/nfe/wsdl/NfeAutorizacaoService/nfeAutorizacaoLote',
    }

    resp = session.post(wsdl_url, data=soap_env.encode('utf-8'), headers=headers, timeout=120)
    return resp.text

def extrair_protocolo(resposta_xml):
    try:
        root = etree.fromstring(resposta_xml.encode())
        ns = {'ns': 'http://www.portalfiscal.inf.br/nfe'}
        prot_nfe = root.find('.//{http://www.portalfiscal.inf.br/nfe}protNFe')
        if prot_nfe is not None:
            infProt = prot_nfe.find('{http://www.portalfiscal.inf.br/nfe}infProt')
            if infProt is not None:
                tpAmb = infProt.findtext('{http://www.portalfiscal.inf.br/nfe}tpAmb', '')
                nProt = infProt.findtext('{http://www.portalfiscal.inf.br/nfe}nProt', '')
                digVal = infProt.findtext('{http://www.portalfiscal.inf.br/nfe}digVal', '')
                cStat = infProt.findtext('{http://www.portalfiscal.inf.br/nfe}cStat', '')
                xMotivo = infProt.findtext('{http://www.portalfiscal.inf.br/nfe}xMotivo', '')
                return {
                    'tpAmb': tpAmb,
                    'nProt': nProt,
                    'digVal': digVal,
                    'cStat': cStat,
                    'xMotivo': xMotivo,
                }
        return {'cStat': '999', 'xMotivo': 'Protocolo nao encontrado'}
    except Exception as e:
        return {'cStat': '999', 'xMotivo': str(e)}
