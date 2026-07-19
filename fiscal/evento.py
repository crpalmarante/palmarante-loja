from datetime import datetime, timezone
from lxml import etree
from fiscal.certificado import CertificadoA1
from fiscal.assinatura import assinar_xml
from fiscal.transmissao import SEFAZ_AMBIENTES
import requests
from requests import Session

SEFAZ_EVENTO = {
    'nfe': {
        2: {
            41: 'https://hom1.sefa.pr.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            35: 'https://hom1.sefaz.sp.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            33: 'https://hom1.sefaz.rj.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            31: 'https://hom1.sefaz.mg.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            43: 'https://hom1.sefaz.rs.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            42: 'https://hom1.sefaz.sc.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            52: 'https://homolog.sefaz.go.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            29: 'https://hml.sefaz.ba.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            26: 'https://hom1.sefaz.pe.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            23: 'https://hml1.sefaz.ce.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            53: 'https://hom1.sefaz.df.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            50: 'https://hom.sefaz.ms.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            51: 'https://hom1.sefaz.mt.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            15: 'https://hom1.sefaz.pa.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
        },
        1: {
            41: 'https://sefa.pr.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            35: 'https://nfe.fazenda.sp.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            33: 'https://sefaz.rj.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            31: 'https://sefaz.mg.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            43: 'https://nfe.sefaz.rs.gov.br/ws/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            42: 'https://sefaz.sc.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            52: 'https://sefaz.go.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            29: 'https://sefaz.ba.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            26: 'https://sefaz.pe.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            23: 'https://sefaz.ce.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            53: 'https://sefaz.df.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            50: 'https://sefaz.ms.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            51: 'https://sefaz.mt.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
            15: 'https://sefaz.pa.gov.br/WS/NfeRecepcaoEvento/NFeRecepcaoEvento.asmx',
        },
    },
    'nfce': {
        2: {
            41: 'https://homologacao.nfce.sefa.pr.gov.br/ws/NfceRecepcaoEventoService',
            35: 'https://homologacao.nfce.fazenda.sp.gov.br/ws/NfceRecepcaoEventoService',
            33: 'https://nfc-homologacao.sefaz.rj.gov.br/ws/NfceRecepcaoEventoService',
            31: 'https://homnfce.sefaz.mg.gov.br/ws/NfceRecepcaoEventoService',
            43: 'https://hom1.nfce.fazenda.rs.gov.br/ws/NfceRecepcaoEventoService',
            42: 'https://nfce-homologacao.sefaz.sc.gov.br/ws/NfceRecepcaoEventoService',
            52: 'https://homolog.sefaz.go.gov.br/ws/NfceRecepcaoEventoService',
            29: 'https://hml.sefaz.ba.gov.br/ws/NfceRecepcaoEventoService',
            26: 'https://homnfce.sefaz.pe.gov.br/ws/NfceRecepcaoEventoService',
            23: 'https://hmlnfce.sefaz.ce.gov.br/ws/NfceRecepcaoEventoService',
            53: 'https://homnfce.sefaz.df.gov.br/ws/NfceRecepcaoEventoService',
            50: 'https://homnfce.sefaz.ms.gov.br/ws/NfceRecepcaoEventoService',
            51: 'https://homnfce.sefaz.mt.gov.br/ws/NfceRecepcaoEventoService',
            15: 'https://homnfce.sefaz.pa.gov.br/ws/NfceRecepcaoEventoService',
        },
        1: {
            41: 'https://nfce.sefa.pr.gov.br/ws/NfceRecepcaoEventoService',
            35: 'https://nfce.fazenda.sp.gov.br/ws/NfceRecepcaoEventoService',
            33: 'https://nfce.sefaz.rj.gov.br/ws/NfceRecepcaoEventoService',
            31: 'https://nfce.sefaz.mg.gov.br/ws/NfceRecepcaoEventoService',
            43: 'https://nfe.fazenda.rs.gov.br/ws/NfceRecepcaoEventoService',
            42: 'https://nfce.sefaz.sc.gov.br/ws/NfceRecepcaoEventoService',
            52: 'https://nfce.sefaz.go.gov.br/ws/NfceRecepcaoEventoService',
            29: 'https://nfce.sefaz.ba.gov.br/ws/NfceRecepcaoEventoService',
            26: 'https://nfce.sefaz.pe.gov.br/ws/NfceRecepcaoEventoService',
            23: 'https://nfce.sefaz.ce.gov.br/ws/NfceRecepcaoEventoService',
            53: 'https://nfce.sefaz.df.gov.br/ws/NfceRecepcaoEventoService',
            50: 'https://nfce.sefaz.ms.gov.br/ws/NfceRecepcaoEventoService',
            51: 'https://nfce.sefaz.mt.gov.br/ws/NfceRecepcaoEventoService',
            15: 'https://nfce.sefaz.pa.gov.br/ws/NfceRecepcaoEventoService',
        },
    },
}

def get_wsdl_evento(modelo='nfce', uf=43, ambiente=2):
    mapa = SEFAZ_EVENTO.get(modelo, {}).get(ambiente, {})
    base = mapa.get(uf)
    if not base:
        raise ValueError(f'EVENTO {modelo.upper()} UF {uf} ambiente {ambiente} nao configurado')
    return base

def montar_xml_cancelamento(chave, protocolo, justificativa, ambiente=2, uf=43):
    nsmap = {None: 'http://www.portalfiscal.inf.br/nfe'}
    evento = etree.Element('{http://www.portalfiscal.inf.br/nfe}evento', nsmap=nsmap)
    evento.set('versao', '1.00')

    infEvento = etree.SubElement(evento, '{http://www.portalfiscal.inf.br/nfe}infEvento')
    infEvento.set('Id', f'ID110111{chave}')

    cOrgao = etree.SubElement(infEvento, 'cOrgao'); cOrgao.text = str(uf)
    tpAmb = etree.SubElement(infEvento, 'tpAmb'); tpAmb.text = str(ambiente)
    CNPJ = etree.SubElement(infEvento, 'CNPJ')
    chave_nfe = etree.SubElement(infEvento, 'chNFe'); chave_nfe.text = chave
    dhEvento = etree.SubElement(infEvento, 'dhEvento')
    dhEvento.text = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S-03:00')
    tpEvento = etree.SubElement(infEvento, 'tpEvento'); tpEvento.text = '110111'
    nSeqEvento = etree.SubElement(infEvento, 'nSeqEvento'); nSeqEvento.text = '1'
    verEvento = etree.SubElement(infEvento, 'verEvento'); verEvento.text = '1.00'

    detEvento = etree.SubElement(infEvento, 'detEvento')
    descEvento = etree.SubElement(detEvento, 'descEvento'); descEvento.text = 'Cancelamento'
    nProt = etree.SubElement(detEvento, 'nProt'); nProt.text = protocolo
    xJust = etree.SubElement(detEvento, 'xJust'); xJust.text = justificativa[:255]

    return etree.tostring(evento, xml_declaration=True, encoding='UTF-8', pretty_print=True).decode()

def transmitir_evento(xml_evento_assinado, chave, modelo='nfce', uf=43, ambiente=2, certificado=None, cert_senha=''):
    if isinstance(certificado, tuple) and len(certificado) == 2 and certificado[0]:
        cert_obj = CertificadoA1(certificado[0], certificado[1])
        cert_obj.carregar()
        certificado = cert_obj
    elif isinstance(certificado, str) and certificado:
        cert_obj = CertificadoA1(certificado, '')
        cert_obj.carregar()
        certificado = cert_obj

    session = Session()
    if certificado and certificado.caminho:
        session.cert = (certificado.caminho, None)
    session.verify = False

    url_recepcao = get_wsdl_evento(modelo, uf, ambiente)
    if not url_recepcao:
        url = SEFAZ_AMBIENTES.get(modelo, {}).get(ambiente, {}).get(uf, '')
        url_recepcao = url.replace('Autorizacao', 'RecepcaoEvento')

    lote = etree.fromstring(xml_evento_assinado.encode())

    soap_env = f'''<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
  <soap:Header>
    <nfeCabecMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/NFeRecepcaoEventoService">
      <versaoDados>1.00</versaoDados>
      <cUF>{uf}</cUF>
    </nfeCabecMsg>
  </soap:Header>
  <soap:Body>
    <nfeRecepcaoEvento xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/NFeRecepcaoEventoService">
      <nfeDadosMsg>{etree.tostring(lote, encoding='UTF-8').decode()}</nfeDadosMsg>
    </nfeRecepcaoEvento>
  </soap:Body>
</soap:Envelope>'''

    headers = {
        'Content-Type': 'application/soap+xml;charset=UTF-8',
        'SOAPAction': 'http://www.portalfiscal.inf.br/nfe/wsdl/NFeRecepcaoEventoService/nfeRecepcaoEvento',
    }

    resp = session.post(url_recepcao, data=soap_env.encode('utf-8'), headers=headers, timeout=120)
    return resp.text

def montar_xml_carta_correcao(chave, sequencia, correcao, ambiente=2, uf=43):
    nsmap = {None: 'http://www.portalfiscal.inf.br/nfe'}
    evento = etree.Element('{http://www.portalfiscal.inf.br/nfe}evento', nsmap=nsmap)
    evento.set('versao', '1.00')

    infEvento = etree.SubElement(evento, '{http://www.portalfiscal.inf.br/nfe}infEvento')
    infEvento.set('Id', f'ID110110{chave}')

    etree.SubElement(infEvento, 'cOrgao').text = str(uf)
    etree.SubElement(infEvento, 'tpAmb').text = str(ambiente)
    etree.SubElement(infEvento, 'CNPJ')
    etree.SubElement(infEvento, 'chNFe').text = chave
    etree.SubElement(infEvento, 'dhEvento').text = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S-03:00')
    etree.SubElement(infEvento, 'tpEvento').text = '110110'
    etree.SubElement(infEvento, 'nSeqEvento').text = str(sequencia)
    etree.SubElement(infEvento, 'verEvento').text = '1.00'

    detEvento = etree.SubElement(infEvento, 'detEvento')
    etree.SubElement(detEvento, 'descEvento').text = 'Carta de Correcao'
    etree.SubElement(detEvento, 'xCorrecao').text = correcao[:1000]
    etree.SubElement(detEvento, 'xCondUso').text = 'A Carta de Correcao e disciplinada pelo paragrafo 1o-A do art. 7o do Convenio S/N, de 15 de dezembro de 1970 e pode ser utilizada para regularizacao de erro ocorrido na emissao de documento fiscal, desde que o erro nao esteja relacionado com: I - as variaveis que determinam o valor do imposto tais como: base de calculo, aliquota, diferenca de preco ou quantidade, valor do imposto; II - a correcao de dados cadastrais que implique mudanca do remetente ou do destinatario; III - a data de emissao ou de saida.'

    return etree.tostring(evento, xml_declaration=True, encoding='UTF-8', pretty_print=True).decode()

def extrair_resultado_evento(resposta_xml):
    try:
        root = etree.fromstring(resposta_xml.encode())
        retEvento = root.find('.//{http://www.portalfiscal.inf.br/nfe}retEvento')
        if retEvento is not None:
            infEvento = retEvento.find('{http://www.portalfiscal.inf.br/nfe}infEvento')
            if infEvento is not None:
                return {
                    'cStat': infEvento.findtext('{http://www.portalfiscal.inf.br/nfe}cStat', ''),
                    'xMotivo': infEvento.findtext('{http://www.portalfiscal.inf.br/nfe}xMotivo', ''),
                    'nProt': infEvento.findtext('{http://www.portalfiscal.inf.br/nfe}nProt', ''),
                }
        return {'cStat': '999', 'xMotivo': 'Evento nao encontrado', 'nProt': ''}
    except Exception as e:
        return {'cStat': '999', 'xMotivo': str(e), 'nProt': ''}
