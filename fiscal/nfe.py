import hashlib
from datetime import datetime, timezone
from lxml import etree

DIR = None

def gerar_chave_acesso(c_uf, ano, mes, cnpj, modelo, serie, numero, tp_emis, c_nf, c_dv):
    chave = f'{c_uf:02d}{ano:02d}{mes:02d}{cnpj:014d}{modelo:02d}{serie:03d}{numero:09d}{tp_emis:01d}{c_nf:08d}'
    dv = calcular_dv(chave)
    chave += str(dv)
    return chave

def calcular_dv(chave):
    pesos = [4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(d) * p for d, p in zip(chave.zfill(43), pesos))
    resto = soma % 11
    return 0 if resto < 2 else 11 - resto

class NFeBuilder:
    def __init__(self, config):
        self.cfg = config

    def montar_xml(self, venda, itens, numero, serie, ambiente=2):
        c_uf = 43
        cnpj_num = int(''.join(c for c in self.cfg.cnpj if c.isdigit()) or '0')
        modelo = 55  # NF-e
        tp_emis = 1
        c_nf = int(hashlib.sha1(str(datetime.now().timestamp()).encode()).hexdigest()[:8], 16)

        dh_emissao = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S-03:00')
        ano = datetime.now().year % 100
        mes = datetime.now().month

        chave = gerar_chave_acesso(c_uf, ano, mes, cnpj_num, modelo, serie, numero, tp_emis, c_nf, 0)

        nsmap = {None: 'http://www.portalfiscal.inf.br/nfe'}

        nfe = etree.Element('{http://www.portalfiscal.inf.br/nfe}nfe', nsmap=nsmap)
        infNFe = etree.SubElement(nfe, '{http://www.portalfiscal.inf.br/nfe}infNFe')
        infNFe.set('Id', f'NFe{chave}')
        infNFe.set('versao', '4.00')

        # ---------- ide ----------
        ide = etree.SubElement(infNFe, '{http://www.portalfiscal.inf.br/nfe}ide')
        c_UF_e = etree.SubElement(ide, 'cUF'); c_UF_e.text = str(c_uf)
        c_NF_e = etree.SubElement(ide, 'cNF'); c_NF_e.text = str(c_nf)
        natOp_e = etree.SubElement(ide, 'natOp'); natOp_e.text = 'VENDA'
        mod_e = etree.SubElement(ide, 'mod'); mod_e.text = '55'
        serie_e = etree.SubElement(ide, 'serie'); serie_e.text = str(serie)
        nNF_e = etree.SubElement(ide, 'nNF'); nNF_e.text = str(numero)
        dhEmi_e = etree.SubElement(ide, 'dhEmi'); dhEmi_e.text = dh_emissao
        dhSaiEnt = etree.SubElement(ide, 'dhSaiEnt'); dhSaiEnt.text = dh_emissao
        tpNF_e = etree.SubElement(ide, 'tpNF'); tpNF_e.text = '1'
        idDest_e = etree.SubElement(ide, 'idDest')
        idDest_e.text = '2'
        cMunFG_e = etree.SubElement(ide, 'cMunFG'); cMunFG_e.text = '4314902'
        tpImp_e = etree.SubElement(ide, 'tpImp'); tpImp_e.text = '1'
        tpEmis_e = etree.SubElement(ide, 'tpEmis'); tpEmis_e.text = str(tp_emis)
        cDV_e = etree.SubElement(ide, 'cDV'); cDV_e.text = str(calcular_dv(chave))
        tpAmb_e = etree.SubElement(ide, 'tpAmb'); tpAmb_e.text = str(ambiente)
        finNFe_e = etree.SubElement(ide, 'finNFe'); finNFe_e.text = '1'
        indFinal_e = etree.SubElement(ide, 'indFinal'); indFinal_e.text = '0'
        indPres_e = etree.SubElement(ide, 'indPres'); indPres_e.text = '0'
        procEmi_e = etree.SubElement(ide, 'procEmi'); procEmi_e.text = '0'
        verProc_e = etree.SubElement(ide, 'verProc'); verProc_e.text = 'Palmarante POS 1.0'

        # ---------- emit ----------
        emit = etree.SubElement(infNFe, '{http://www.portalfiscal.inf.br/nfe}emit')
        CNPJ_e = etree.SubElement(emit, 'CNPJ')
        CNPJ_e.text = ''.join(c for c in self.cfg.cnpj if c.isdigit())
        xNome_e = etree.SubElement(emit, 'xNome'); xNome_e.text = (self.cfg.nome or '')[:60]
        xFant_e = etree.SubElement(emit, 'xFant'); xFant_e.text = (self.cfg.nome or '')[:60]
        enderEmit = etree.SubElement(emit, 'enderEmit')
        xLgr_e = etree.SubElement(enderEmit, 'xLgr'); xLgr_e.text = (self.cfg.endereco or 'RUA')[:60]
        nro_e = etree.SubElement(enderEmit, 'nro'); nro_e.text = 'S/N'
        xBairro_e = etree.SubElement(enderEmit, 'xBairro'); xBairro_e.text = 'CENTRO'
        cMun_e = etree.SubElement(enderEmit, 'cMun'); cMun_e.text = '4314902'
        xMun_e = etree.SubElement(enderEmit, 'xMun'); xMun_e.text = 'PORTO ALEGRE'
        UF_e = etree.SubElement(enderEmit, 'UF'); UF_e.text = 'RS'
        CEP_e = etree.SubElement(enderEmit, 'CEP'); CEP_e.text = '90000000'
        cPais_e = etree.SubElement(enderEmit, 'cPais'); cPais_e.text = '1058'
        xPais_e = etree.SubElement(enderEmit, 'xPais'); xPais_e.text = 'BRASIL'
        fone_e = etree.SubElement(enderEmit, 'fone'); fone_e.text = self.cfg.telefone or ''
        IE_e = etree.SubElement(emit, 'IE'); IE_e.text = self.cfg.inscricao_est or ''
        CRT_e = etree.SubElement(emit, 'CRT'); CRT_e.text = str(self.cfg.crt)

        # ---------- dest ----------
        dest = etree.SubElement(infNFe, '{http://www.portalfiscal.inf.br/nfe}dest')
        cliente = venda.get('cliente', 'Consumidor Final')
        cpf_cnpj = ''.join(c for c in cliente if c.isdigit())
        if len(cpf_cnpj) == 14:
            CNPJ_dest = etree.SubElement(dest, 'CNPJ'); CNPJ_dest.text = cpf_cnpj
            xNome_dest = etree.SubElement(dest, 'xNome')
            xNome_dest.text = (cliente or 'CONSUMIDOR')[:60]
        elif len(cpf_cnpj) == 11:
            CPF_dest = etree.SubElement(dest, 'CPF'); CPF_dest.text = cpf_cnpj
            xNome_dest = etree.SubElement(dest, 'xNome')
            xNome_dest.text = 'CONSUMIDOR'
        else:
            idOut_dest = etree.SubElement(dest, 'idOutros'); idOut_dest.text = cliente[:20] or 'CONSUMIDOR'
            xNome_dest = etree.SubElement(dest, 'xNome')
            xNome_dest.text = (cliente or 'CONSUMIDOR')[:60]
        indIEDest_e = etree.SubElement(dest, 'indIEDest')
        indIEDest_e.text = '9' if len(cpf_cnpj) != 14 else '1'

        # ---------- totals ----------
        total_venda = float(venda.get('total', 0))
        total_desc = sum(
            float(i.get('desconto_valor', 0) or 0) for i in itens
        )
        v_prod = total_venda + total_desc

        # ---------- det ----------
        det_index = 0
        for item in itens:
            det_index += 1
            det = etree.SubElement(infNFe, '{http://www.portalfiscal.inf.br/nfe}det')
            det.set('nItem', str(det_index))

            prod = etree.SubElement(det, '{http://www.portalfiscal.inf.br/nfe}prod')
            cProd_e = etree.SubElement(prod, 'cProd')
            cProd_e.text = str(item.get('produto_id', item.get('id', det_index)))
            cEAN_e = etree.SubElement(prod, 'cEAN'); cEAN_e.text = ''
            xProd_e = etree.SubElement(prod, 'xProd')
            xProd_e.text = (item.get('nome', 'PRODUTO') or 'PRODUTO')[:120]
            NCM_e = etree.SubElement(prod, 'NCM')
            NCM_e.text = (item.get('ncm', '') or '00000000')[:8]
            CFOP_e = etree.SubElement(prod, 'CFOP')
            CFOP_e.text = (item.get('cfop', '5102') or '5102')[:4]
            uCom_e = etree.SubElement(prod, 'uCom'); uCom_e.text = 'UN'
            qCom_e = etree.SubElement(prod, 'qCom')
            qCom_e.text = f'{float(item.get("qtd", 1)):.4f}'
            vUnCom_e = etree.SubElement(prod, 'vUnCom')
            preco_uni = float(item.get('preco_efetivo', item.get('preco', 0)))
            vUnCom_e.text = f'{preco_uni:.10f}'
            vProd_e = etree.SubElement(prod, 'vProd')
            v_item = preco_uni * float(item.get('qtd', 1))
            vProd_e.text = f'{v_item:.2f}'
            cEANTrib_e = etree.SubElement(prod, 'cEANTrib'); cEANTrib_e.text = ''
            uTrib_e = etree.SubElement(prod, 'uTrib'); uTrib_e.text = 'UN'
            qTrib_e = etree.SubElement(prod, 'qTrib')
            qTrib_e.text = f'{float(item.get("qtd", 1)):.4f}'
            vUnTrib_e = etree.SubElement(prod, 'vUnTrib')
            vUnTrib_e.text = f'{preco_uni:.10f}'
            vDesc_e = etree.SubElement(prod, 'vDesc')
            vDesc_e.text = f'{float(item.get("desconto_valor", 0) or 0):.2f}'
            indTot_e = etree.SubElement(prod, 'indTot'); indTot_e.text = '1'

            # ---------- imposto ----------
            imposto = etree.SubElement(det, '{http://www.portalfiscal.inf.br/nfe}imposto')
            vTotTrib_e = etree.SubElement(imposto, 'vTotTrib'); vTotTrib_e.text = '0.00'

            # ICMS
            icms = etree.SubElement(imposto, '{http://www.portalfiscal.inf.br/nfe}ICMS')
            cst = (item.get('cst', '400') or '400').strip()
            if self.cfg.crt == 1 and cst in ('400', '500', '600', '700'):
                icms40 = etree.SubElement(icms, '{http://www.portalfiscal.inf.br/nfe}ICMS40')
                orig = etree.SubElement(icms40, 'orig'); orig.text = '0'
                cst_el = etree.SubElement(icms40, 'CST'); cst_el.text = cst
                vICMSDeson = etree.SubElement(icms40, 'vICMSDeson'); vICMSDeson.text = '0.00'
                motivo = etree.SubElement(icms40, 'motDesICMS')
                motivo.text = '6' if cst == '400' else '1'
            elif cst in ('00', '10', '20', '40', '41', '60'):
                icms00 = etree.SubElement(icms, '{http://www.portalfiscal.inf.br/nfe}ICMS00')
                orig = etree.SubElement(icms00, 'orig'); orig.text = '0'
                cst_el = etree.SubElement(icms00, 'CST'); cst_el.text = cst
                modBC = etree.SubElement(icms00, 'modBC'); modBC.text = '3'
                vBC_e = etree.SubElement(icms00, 'vBC'); vBC_e.text = f'{v_item:.2f}'
                pICMS_e = etree.SubElement(icms00, 'pICMS')
                alq = float(item.get('icms_alq', 0) or 0)
                pICMS_e.text = f'{alq:.2f}'
                vICMS_e = etree.SubElement(icms00, 'vICMS')
                vICMS_e.text = f'{v_item * alq / 100:.2f}'
            else:
                icms_sn = etree.SubElement(icms, '{http://www.portalfiscal.inf.br/nfe}ICMSSN102')
                orig = etree.SubElement(icms_sn, 'orig'); orig.text = '0'
                csosn = etree.SubElement(icms_sn, 'CSOSN'); csosn.text = cst

            # PIS
            pis = etree.SubElement(imposto, '{http://www.portalfiscal.inf.br/nfe}PIS')
            pisOutr = etree.SubElement(pis, '{http://www.portalfiscal.inf.br/nfe}PISOutr')
            cst_pis = etree.SubElement(pisOutr, 'CST'); cst_pis.text = '99'
            etree.SubElement(pisOutr, 'vBC').text = '0.00'
            etree.SubElement(pisOutr, 'pPIS').text = '0.00'
            etree.SubElement(pisOutr, 'vPIS').text = '0.00'

            # COFINS
            cofins = etree.SubElement(imposto, '{http://www.portalfiscal.inf.br/nfe}COFINS')
            cofinsOutr = etree.SubElement(cofins, '{http://www.portalfiscal.inf.br/nfe}COFINSOutr')
            cst_cof = etree.SubElement(cofinsOutr, 'CST'); cst_cof.text = '99'
            etree.SubElement(cofinsOutr, 'vBC').text = '0.00'
            etree.SubElement(cofinsOutr, 'pCOFINS').text = '0.00'
            etree.SubElement(cofinsOutr, 'vCOFINS').text = '0.00'

        # ---------- total ----------
        total = etree.SubElement(infNFe, '{http://www.portalfiscal.inf.br/nfe}total')
        ICMSTot = etree.SubElement(total, '{http://www.portalfiscal.inf.br/nfe}ICMSTot')
        etree.SubElement(ICMSTot, 'vBC').text = f'{v_prod:.2f}'
        etree.SubElement(ICMSTot, 'vICMS').text = '0.00'
        etree.SubElement(ICMSTot, 'vICMSDeson').text = '0.00'
        etree.SubElement(ICMSTot, 'vFCP').text = '0.00'
        etree.SubElement(ICMSTot, 'vBCST').text = '0.00'
        etree.SubElement(ICMSTot, 'vST').text = '0.00'
        etree.SubElement(ICMSTot, 'vProd').text = f'{v_prod:.2f}'
        etree.SubElement(ICMSTot, 'vFrete').text = '0.00'
        etree.SubElement(ICMSTot, 'vSeg').text = '0.00'
        etree.SubElement(ICMSTot, 'vDesc').text = f'{total_desc:.2f}'
        etree.SubElement(ICMSTot, 'vII').text = '0.00'
        etree.SubElement(ICMSTot, 'vIPI').text = '0.00'
        etree.SubElement(ICMSTot, 'vIPIDevol').text = '0.00'
        etree.SubElement(ICMSTot, 'vPIS').text = '0.00'
        etree.SubElement(ICMSTot, 'vCOFINS').text = '0.00'
        etree.SubElement(ICMSTot, 'vOutro').text = '0.00'
        etree.SubElement(ICMSTot, 'vNF').text = f'{total_venda:.2f}'

        # ---------- transp ----------
        transp = etree.SubElement(infNFe, '{http://www.portalfiscal.inf.br/nfe}transp')
        etree.SubElement(transp, 'modFrete').text = '9'

        # ---------- cobranca ----------
        cobr = etree.SubElement(infNFe, '{http://www.portalfiscal.inf.br/nfe}cobr')
        fat = etree.SubElement(cobr, 'fat')
        etree.SubElement(fat, 'nFat').text = str(numero)
        etree.SubElement(fat, 'vOrig').text = f'{total_venda:.2f}'
        etree.SubElement(fat, 'vLiq').text = f'{total_venda:.2f}'

        # ---------- pagamento ----------
        pag = etree.SubElement(infNFe, '{http://www.portalfiscal.inf.br/nfe}pag')
        detPag = etree.SubElement(pag, 'detPag')
        tPag_e = etree.SubElement(detPag, 'tPag')
        tPag_e.text = venda.get('forma_pg', '01')
        etree.SubElement(detPag, 'vPag').text = f'{total_venda:.2f}'

        # ---------- infAdic ----------
        infAdic = etree.SubElement(infNFe, '{http://www.portalfiscal.inf.br/nfe}infAdic')
        etree.SubElement(infAdic, 'infCpl').text = 'NF-e gerada pelo Palmarante POS'

        xml_str = etree.tostring(nfe, xml_declaration=True, encoding='UTF-8', pretty_print=True).decode()
        return xml_str, chave
