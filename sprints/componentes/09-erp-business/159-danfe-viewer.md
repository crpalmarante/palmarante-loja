# FiscalUI Framework

## Documento 159 — DANFE Viewer

**Nível 9 — ERP Business Components**

**Versão 1.0**

Visualizador de DANFE (Documento Auxiliar da NF-e) em tela com pré-visualização para impressão.

---

```html
<div class="ui-danfe-viewer">
    <div class="ui-danfe-viewer__toolbar">
        <button class="ui-btn ui-btn--primary ui-btn--sm" data-action="print">🖨️ Imprimir DANFE</button>
        <button class="ui-btn ui-btn--ghost ui-btn--sm" data-action="download-pdf">📄 Salvar PDF</button>
        <button class="ui-btn ui-btn--ghost ui-btn--sm" data-action="zoom-in">🔍+</button>
        <button class="ui-btn ui-btn--ghost ui-btn--sm" data-action="zoom-out">🔍−</button>
        <span class="ui-danfe-viewer__zoom-level">100%</span>
    </div>

    <div class="ui-danfe-viewer__page">
        <div class="ui-danfe-viewer__header">
            <div class="ui-danfe-viewer__header-top">
                <div class="ui-danfe-viewer__emitente">
                    <h4>EMPRESA EXEMPLO LTDA</h4>
                    <p>CNPJ: 11.222.333/0001-44 | IE: 123.456.789.000</p>
                    <p>Rua Exemplo, 123 — Centro — São Paulo/SP — CEP 01001-000</p>
                </div>
                <div class="ui-danfe-viewer__nfe-info">
                    <div class="ui-danfe-viewer__danfe-label">DANFE</div>
                    <div class="ui-danfe-viewer__nfe-chave">
                        <span>Chave: 3526 0712 3456 7890 1234 5678 9012 3456 7890 1234 5678</span>
                    </div>
                </div>
            </div>
            <div class="ui-danfe-viewer__header-barcode">
                <img src="barcode-placeholder.png" alt="Código de Barras">
            </div>
        </div>

        <div class="ui-danfe-viewer__destinatario">
            <h5>DESTINATÁRIO / REMETENTE</h5>
            <div class="ui-danfe-viewer__dest-grid">
                <div><label>Nome</label><span>João Silva</span></div>
                <div><label>CNPJ/CPF</label><span>123.456.789-00</span></div>
                <div><label>Data Emissão</label><span>15/07/2026</span></div>
                <div><label>Data Entrada/Saída</label><span>15/07/2026</span></div>
            </div>
        </div>

        <div class="ui-danfe-viewer__table">
            <table>
                <thead>
                    <tr>
                        <th>Código</th>
                        <th>Descrição</th>
                        <th>NCM</th>
                        <th>Qtd</th>
                        <th>Un</th>
                        <th>Valor Unit</th>
                        <th>Valor Total</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>001</td>
                        <td>Arroz Parboilizado Tipo 1 5kg</td>
                        <td>1006.30.11</td>
                        <td>10</td>
                        <td>UN</td>
                        <td>22,90</td>
                        <td>229,00</td>
                    </tr>
                    <tr>
                        <td>002</td>
                        <td>Feijão Carioca 1kg</td>
                        <td>0713.33.99</td>
                        <td>20</td>
                        <td>UN</td>
                        <td>8,50</td>
                        <td>170,00</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="ui-danfe-viewer__totals">
            <div class="ui-danfe-viewer__total-row">
                <span>Base Cálculo ICMS</span><span>R$ 399,00</span>
                <span>Valor ICMS</span><span>R$ 71,82</span>
            </div>
            <div class="ui-danfe-viewer__total-row">
                <span>Valor Produtos</span><span>R$ 399,00</span>
                <span>Valor Frete</span><span>R$ 0,00</span>
            </div>
            <div class="ui-danfe-viewer__total-row ui-danfe-viewer__total-row--grand">
                <span>VALOR TOTAL DA NOTA</span><span class="ui-danfe-viewer__total-grand">R$ 399,00</span>
            </div>
        </div>

        <div class="ui-danfe-viewer__footer">
            <div class="ui-danfe-viewer__protocolo">
                <strong>Protocolo de Autorização:</strong> 3526071234567890 — 15/07/2026 14:32:05
            </div>
            <div class="ui-danfe-viewer__qrcode">
                <img src="qrcode-placeholder.png" alt="QR Code">
            </div>
        </div>
    </div>
</div>
```

```css
.ui-danfe-viewer { display: flex; flex-direction: column; align-items: center; background: var(--color-bg); padding: var(--spacing-md); }
.ui-danfe-viewer__toolbar { display: flex; align-items: center; gap: var(--spacing-sm); margin-bottom: var(--spacing-md); padding: var(--spacing-sm); background: var(--color-surface); border-radius: var(--radius-md); box-shadow: var(--shadow-sm); }
.ui-danfe-viewer__zoom-level { font-size: var(--font-size-sm); color: var(--color-text-muted); min-width: 40px; text-align: center; }
.ui-danfe-viewer__page { width: 794px; background: white; color: black; padding: 30px; box-shadow: 0 2px 20px rgba(0,0,0,0.15); font-family: 'Courier New', monospace; font-size: 11px; }
.ui-danfe-viewer__header { border-bottom: 2px solid #000; padding-bottom: 10px; margin-bottom: 10px; }
.ui-danfe-viewer__header-top { display: flex; justify-content: space-between; }
.ui-danfe-viewer__emitente h4 { margin: 0; font-size: 14px; font-weight: bold; }
.ui-danfe-viewer__emitente p { margin: 2px 0; font-size: 10px; }
.ui-danfe-viewer__danfe-label { font-size: 24px; font-weight: bold; border: 2px solid #000; padding: 4px 12px; text-align: center; }
.ui-danfe-viewer__nfe-chave { font-size: 9px; margin-top: 4px; }
.ui-danfe-viewer__header-barcode { text-align: center; padding: 8px 0; }
.ui-danfe-viewer__header-barcode img { height: 30px; }

.ui-danfe-viewer__destinatario { margin-bottom: 10px; }
.ui-danfe-viewer__destinatario h5 { background: #e0e0e0; padding: 4px 8px; font-size: 10px; margin: 0 0 4px; }
.ui-danfe-viewer__dest-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2px 20px; }
.ui-danfe-viewer__dest-grid label { color: #666; }
.ui-danfe-viewer__dest-grid span { font-weight: bold; }

.ui-danfe-viewer__table table { width: 100%; border-collapse: collapse; margin: 10px 0; }
.ui-danfe-viewer__table th { background: #e0e0e0; padding: 4px 6px; text-align: left; font-size: 9px; border: 1px solid #999; }
.ui-danfe-viewer__table td { padding: 3px 6px; border: 1px solid #ccc; font-size: 10px; }

.ui-danfe-viewer__totals { border-top: 2px solid #000; margin-top: 10px; padding-top: 10px; }
.ui-danfe-viewer__total-row { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 10px; padding: 2px 0; font-size: 11px; }
.ui-danfe-viewer__total-row--grand { border-top: 2px solid #000; margin-top: 4px; padding-top: 4px; }
.ui-danfe-viewer__total-grand { font-size: 16px; font-weight: bold; }

.ui-danfe-viewer__footer { display: flex; justify-content: space-between; align-items: center; margin-top: 20px; padding-top: 10px; border-top: 1px solid #ccc; }
.ui-danfe-viewer__protocolo { font-size: 9px; }
.ui-danfe-viewer__qrcode img { width: 80px; height: 80px; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
