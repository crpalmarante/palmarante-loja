from datetime import datetime, timezone
from lxml import etree

class NfseBuilder:
    def __init__(self, config):
        self.cfg = config

    def montar_xml(self, venda, itens, numero_rps, serie_rps='S'):
        dt = datetime.now(timezone.utc)
        data_emissao = dt.strftime('%Y-%m-%dT%H:%M:%S')

        # Padrao ABRASF 2.04
        nsmap = {None: 'http://www.abrasf.org.br/nfse.xsd'}

        nfse = etree.Element('{http://www.abrasf.org.br/nfse.xsd}GerarNfseEnvio', nsmap=nsmap)

        rps = etree.SubElement(nfse, 'Rps')
        inf_rps = etree.SubElement(rps, 'InfRps')
        inf_rps.set('Id', f'RPS{numero_rps}')

        # Identificacao RPS
        ident = etree.SubElement(inf_rps, 'IdentificacaoRps')
        etree.SubElement(ident, 'Numero').text = str(numero_rps)
        etree.SubElement(ident, 'Serie').text = serie_rps
        etree.SubElement(ident, 'Tipo').text = '1'

        etree.SubElement(inf_rps, 'DataEmissao').text = data_emissao
        etree.SubElement(inf_rps, 'NaturezaOperacao').text = '1'
        etree.SubElement(inf_rps, 'RegimeEspecialTributacao').text = '6'
        etree.SubElement(inf_rps, 'OptanteSimplesNacional').text = '1'
        etree.SubElement(inf_rps, 'IncentivadorCultural').text = '2'
        etree.SubElement(inf_rps, 'Status').text = '1'

        # Servico
        servico = etree.SubElement(inf_rps, 'Servico')
        valores = etree.SubElement(servico, 'Valores')
        total_venda = float(venda.get('total', 0))
        total_itens = sum(float(i.get('qtd', 1)) * float(i.get('preco', 0)) for i in itens)

        # find the first service item's ISS aliquot
        iss_alq = 0
        for item in itens:
            alq = float(item.get('iss_alq', 0) or 0)
            if alq > 0:
                iss_alq = alq
                break

        v_iss = total_venda * iss_alq / 100 if iss_alq > 0 else 0

        etree.SubElement(valores, 'ValorServicos').text = f'{total_venda:.2f}'
        etree.SubElement(valores, 'ValorDeducoes').text = '0.00'
        etree.SubElement(valores, 'ValorPis').text = '0.00'
        etree.SubElement(valores, 'ValorCofins').text = '0.00'
        etree.SubElement(valores, 'ValorInss').text = '0.00'
        etree.SubElement(valores, 'ValorIr').text = '0.00'
        etree.SubElement(valores, 'ValorCsll').text = '0.00'
        etree.SubElement(valores, 'IssRetido').text = '2'
        etree.SubElement(valores, 'ValorIss').text = f'{v_iss:.2f}'
        etree.SubElement(valores, 'ValorIssRetido').text = '0.00'
        etree.SubElement(valores, 'OutrasRetencoes').text = '0.00'
        etree.SubElement(valores, 'BaseCalculo').text = f'{total_venda:.2f}'
        etree.SubElement(valores, 'Aliquota').text = f'{iss_alq:.4f}'
        etree.SubElement(valores, 'ValorLiquidoNfse').text = f'{total_venda - v_iss:.2f}'
        etree.SubElement(valores, 'DescontoIncondicionado').text = '0.00'
        etree.SubElement(valores, 'DescontoCondicionado').text = '0.00'

        # get service item code
        cod_serv = ''
        for item in itens:
            cs = item.get('cod_serv_mun', '') or ''
            if cs:
                cod_serv = cs
                break
        if not cod_serv:
            cod_serv = item.get('cod_serv_mun', '0000') if itens else '0000'

        etree.SubElement(servico, 'ItemListaServico').text = cod_serv
        etree.SubElement(servico, 'CodigoCnae').text = (self.cfg.cnae_prim_codigo or '0000000')[:7]
        etree.SubElement(servico, 'CodigoTributacaoMunicipio').text = cod_serv
        etree.SubElement(servico, 'Discriminacao').text = ' '.join(
            f"{item.get('qtd', 1)}x {item.get('nome', '')}" for item in itens
        )[:2000]
        cod_mun = self.cfg.cod_municipio or '4314902'
        etree.SubElement(servico, 'CodigoMunicipio').text = cod_mun

        # Prestador
        prestador = etree.SubElement(inf_rps, 'Prestador')
        cnpj_emit = ''.join(c for c in self.cfg.cnpj if c.isdigit())
        etree.SubElement(prestador, 'CpfCnpj')
        etree.SubElement(prestador, 'InscricaoMunicipal').text = self.cfg.inscricao_mun or ''
        etree.SubElement(prestador, 'CodigoMunicipio').text = cod_mun
        # CpfCnpj needs proper structure
        cnpj_elem = prestador.find('CpfCnpj')
        if len(cnpj_emit) == 14:
            etree.SubElement(cnpj_elem, 'Cnpj').text = cnpj_emit
        else:
            etree.SubElement(cnpj_elem, 'Cpf').text = cnpj_emit

        # Tomador
        tomador = etree.SubElement(inf_rps, 'Tomador')
        cliente = venda.get('cliente', 'Consumidor Final')
        cpf_cnpj = ''.join(c for c in cliente if c.isdigit())
        ident_tom = etree.SubElement(tomador, 'IdentificacaoTomador')
        cpf_cnpj_tom = etree.SubElement(ident_tom, 'CpfCnpj')
        if len(cpf_cnpj) == 14:
            etree.SubElement(cpf_cnpj_tom, 'Cnpj').text = cpf_cnpj
        elif len(cpf_cnpj) == 11:
            etree.SubElement(cpf_cnpj_tom, 'Cpf').text = cpf_cnpj
        razao = etree.SubElement(tomador, 'RazaoSocial')
        razao.text = (cliente or 'Consumidor')[:115]

        # Endereco do tomador
        end_tom = etree.SubElement(tomador, 'Endereco')
        etree.SubElement(end_tom, 'Endereco').text = self.cfg.endereco or ''
        etree.SubElement(end_tom, 'Bairro').text = 'CENTRO'
        etree.SubElement(end_tom, 'CodigoMunicipio').text = cod_mun
        etree.SubElement(end_tom, 'Uf').text = 'RS'
        etree.SubElement(end_tom, 'Cep').text = '90000000'

        # Contato do tomador
        contato = etree.SubElement(tomador, 'Contato')
        etree.SubElement(contato, 'Telefone').text = self.cfg.telefone or ''
        etree.SubElement(contato, 'Email').text = self.cfg.email or ''

        xml_str = etree.tostring(nfse, xml_declaration=True, encoding='UTF-8', pretty_print=True).decode()
        return xml_str
