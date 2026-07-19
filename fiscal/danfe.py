import os
from datetime import datetime

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def format_preco(v):
    if v is None: v = 0
    return f'{float(v):.2f}'.replace('.', ',')

def format_cnpj(s):
    if not s: return ''
    d = ''.join(c for c in s if c.isdigit())
    if len(d) == 14:
        return f'{d[:2]}.{d[2:5]}.{d[5:8]}/{d[8:12]}-{d[12:]}'
    return d if len(d) == 14 else s

def format_cpf(s):
    d = ''.join(c for c in s if c.isdigit())
    if len(d) == 11:
        return f'{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}'
    return s

def format_ie(s):
    return s or 'ISENTO'

def gerar_qrcode_data(chave, ambiente=2):
    try:
        import qrcode
        from io import BytesIO
        import base64
        uf_map = {43: 'rs'}
        uf = uf_map.get(43, 'rs')
        url = f'https://www.sefaz.{uf}.gov.br/nfce/consulta?p={chave}|2|1|{ambiente}|{"".join(["0"]*14)}|'
        qr = qrcode.make(url, box_size=4, border=1)
        buf = BytesIO()
        qr.save(buf, format='PNG')
        b64 = base64.b64encode(buf.getvalue()).decode()
        return f'data:image/png;base64,{b64}', url
    except ImportError:
        return '', ''

def danfe_nfce_html(nfce_reg, venda, itens, config):
    chave = nfce_reg.get('chave', '')
    chave_fmt = ' '.join(chave[i:i+4] for i in range(0, 44, 4)) if len(chave) == 44 else chave
    total = float(venda.get('total', 0))
    data = nfce_reg.get('data', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    protocolo = nfce_reg.get('protocolo', '')
    qrcode_b64, qrcode_url = gerar_qrcode_data(chave, config.ambiente)

    itens_html = '\n'.join(
        f'''<tr>
            <td style="text-align:center">{i+1:03d}</td>
            <td>{item.get('nome', '')[:25]}</td>
            <td style="text-align:center">{float(item.get('qtd', 1)):.3f}</td>
            <td>UN</td>
            <td style="text-align:right">{format_preco(item.get('preco'))}</td>
            <td style="text-align:right">{format_preco(float(item.get('qtd', 1)) * float(item.get('preco', 0)))}</td>
        </tr>'''
        for i, item in enumerate(itens)
    )

    qrcode_html = ''
    if qrcode_b64:
        qrcode_html = f'''
        <div style="text-align:center;margin:4px 0;">
            <img src="{qrcode_b64}" style="width:80px;height:80px;" alt="QRCode">
            <div style="font-size:6px;word-break:break-all;">{qrcode_url}</div>
        </div>'''

    return f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>DANFE NFC-e</title>
<style>
@page {{ size:80mm auto; margin:0; }}
@media print {{ body {{ font-size:10px; font-family:monospace; width:70mm; padding:3mm; }} }}
body {{ font-family:monospace; font-size:10px; width:70mm; margin:0 auto; padding:3mm; }}
h2 {{ text-align:center; font-size:12px; margin:2px 0; }}
table {{ width:100%; border-collapse:collapse; font-size:9px; }}
td, th {{ padding:1px 2px; }}
hr {{ border:none; border-top:1px dashed #000; margin:4px 0; }}
.center {{ text-align:center; }}
.right {{ text-align:right; }}
.bold {{ font-weight:bold; }}
.chave {{ font-size:9px; text-align:center; word-break:break-all; }}
.header-info {{ font-size:8px; text-align:center; }}
</style></head><body>
<h2>{config.nome or 'LOJA'}</h2>
<div class="header-info">{config.endereco or ''}</div>
<div class="header-info">CNPJ: {format_cnpj(config.cnpj)}  IE: {format_ie(config.inscricao_est)}</div>
<hr>
<div class="center"><strong>DANFE NFC-e - Documento Auxiliar</strong></div>
<div class="center">NFC-e nº {nfce_reg.get('numero', '')}  Série {nfce_reg.get('serie', '')}</div>
<div class="center">Data: {data}</div>
<hr>
<table><thead><tr>
<th style="text-align:center">SEQ</th><th>DESCRICAO</th><th style="text-align:center">QTD</th><th>UN</th><th style="text-align:right">VL UN</th><th style="text-align:right">VL TOTAL</th>
</tr></thead><tbody>
{itens_html}
</tbody></table>
<hr>
<div style="text-align:right;font-weight:bold;font-size:11px;">TOTAL R$ {format_preco(total)}</div>
<hr>
<div class="chave"><strong>Chave de Acesso</strong><br>{chave_fmt}</div>
<div class="center" style="font-size:8px;">Protocolo: {protocolo}</div>
{qrcode_html}
<div class="center" style="font-size:7px;margin-top:4px;">Consulte pela chave em www.nfce.fazenda.rs.gov.br</div>
<hr>
<div class="center">Obrigado pela preferencia!</div>
</body></html>'''

def danfe_nfe_html(nfe_reg, venda, itens, config):
    chave = nfe_reg.get('chave', '')
    chave_fmt = ' '.join(chave[i:i+4] for i in range(0, 44, 4)) if len(chave) == 44 else chave
    total = float(venda.get('total', 0))
    data = nfe_reg.get('data', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    protocolo = nfe_reg.get('protocolo', '')
    cliente = venda.get('cliente', 'Consumidor Final')

    itens_html = '\n'.join(
        f'''<tr>
            <td style="text-align:center">{i+1:03d}</td>
            <td>{item.get('codigo', item.get('produto_id', ''))}</td>
            <td>{item.get('nome', '')[:20]}</td>
            <td>{item.get('ncm', '')}</td>
            <td style="text-align:center">{float(item.get('qtd', 1)):.3f}</td>
            <td style="text-align:center">UN</td>
            <td style="text-align:right">{format_preco(item.get('preco'))}</td>
            <td style="text-align:right">{format_preco(float(item.get('qtd', 1)) * float(item.get('preco', 0)))}</td>
        </tr>'''
        for i, item in enumerate(itens)
    )

    return f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>DANFE NF-e</title>
<style>
@page {{ size:A4; margin:10mm; }}
body {{ font-family:Arial,sans-serif; font-size:12px; margin:0; padding:10mm; }}
h2 {{ text-align:center; font-size:16px; margin:4px 0; }}
table {{ width:100%; border-collapse:collapse; }}
td, th {{ border:1px solid #000; padding:3px 4px; font-size:11px; }}
hr {{ border:none; border-top:2px solid #000; margin:6px 0; }}
.center {{ text-align:center; }}
.right {{ text-align:right; }}
.bold {{ font-weight:bold; }}
</style></head><body>

<div style="text-align:center;border:2px solid #000;padding:8px;margin-bottom:8px;">
<h2>DANFE</h2>
<div>Documento Auxiliar da Nota Fiscal Eletronica</div>
<div><strong>NF-e nº {nfe_reg.get('numero', '')}  Série {nfe_reg.get('serie', '')}</strong></div>
<div>Data: {data}</div>
</div>

<div style="border:1px solid #000;padding:6px;margin-bottom:6px;">
<div class="bold">Emitente:</div>
<div>{config.nome or 'LOJA'}</div>
<div>CNPJ: {format_cnpj(config.cnpj)}  IE: {format_ie(config.inscricao_est)}</div>
<div>{config.endereco or ''}</div>
</div>

<div style="border:1px solid #000;padding:6px;margin-bottom:6px;">
<div class="bold">Destinatario:</div>
<div>{cliente}</div>
<div>CPF/CNPJ: {''.join(c for c in cliente if c.isdigit()) or '---'}</div>
</div>

<table>
<thead><tr>
<th>SEQ</th><th>COD</th><th>DESCRICAO</th><th>NCM</th><th>QTD</th><th>UN</th><th>VL UNIT</th><th>VL TOTAL</th>
</tr></thead><tbody>
{itens_html}
</tbody></table>

<div style="text-align:right;font-size:14px;font-weight:bold;margin:8px 0;">
Total: R$ {format_preco(total)}
</div>

<hr>
<div class="center"><strong>Chave de Acesso</strong><br>{chave_fmt}</div>
<div class="center">Protocolo: {protocolo}</div>
<div style="text-align:center;font-size:9px;margin-top:8px;">
Consulte pela chave em www.nfe.fazenda.gov.br/portal/consultaRecaptcha.aspx
</div>
</body></html>'''

def danfe_to_pdf(html, output_path):
    try:
        from weasyprint import HTML
        HTML(string=html).write_pdf(output_path)
        return True
    except Exception as e:
        return False
