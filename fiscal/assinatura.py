import os
from lxml import etree
from signxml import XMLSigner, methods
from fiscal.certificado import CertificadoA1

def assinar_xml(xml_string, certificado, cert_senha=''):
    if isinstance(certificado, str):
        cfg = CertificadoA1(certificado, cert_senha)
        cfg.carregar()
        if not cfg.valido:
            raise ValueError("Certificado invalido ou expirado")
        certificado = cfg

    xml_doc = etree.fromstring(xml_string.encode())

    ref_uri = xml_doc.get('Id')
    if not ref_uri:
        infNfe = xml_doc.find('.//{*}infNFe')
        if infNfe is not None:
            ref_uri = infNfe.get('Id')
    if not ref_uri:
        raise ValueError("Nao foi possivel determinar Id do XML")

    signer = XMLSigner(
        method=methods.enveloped,
        signature_algorithm='rsa-sha256',
        digest_algorithm='sha256',
        c14n_algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315',
    )

    ref_uri = '#' + ref_uri if not ref_uri.startswith('#') else ref_uri

    signed_xml = signer.sign(
        xml_doc,
        key=certificado.chave_privada,
        cert=[certificado.certificado],
        reference_uri=ref_uri,
    )

    return etree.tostring(signed_xml, xml_declaration=True, encoding='UTF-8', pretty_print=True).decode()
