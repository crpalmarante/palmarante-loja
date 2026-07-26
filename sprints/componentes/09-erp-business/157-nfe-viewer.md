# FiscalUI Framework

## Documento 157 — NFe Viewer

**Nível 9 — ERP Business Components**

**Versão 1.0**

Visualizador de NF-e com dados completos da nota, tributos, itens, destinatário e protocolo SEFAZ.

---

```html
<div class="ui-nfe-viewer">
    <div class="ui-nfe-viewer__toolbar">
        <div class="ui-nfe-viewer__toolbar-left">
            <h3 class="ui-nfe-viewer__title">NF-e 000.123.456</h3>
            <span class="ui-nfe-viewer__series">Série 1 | Nº 123456</span>
        </div>
        <div class="ui-nfe-viewer__toolbar-right">
            <button class="ui-btn ui-btn--ghost ui-btn--sm" data-action="xml">XML</button>
            <button class="ui-btn ui-btn--ghost ui-btn--sm" data-action="danfe">DANFE</button>
            <button class="ui-btn ui-btn--ghost ui-btn--sm" data-action="print">🖨️</button>
            <button class="ui-btn ui-btn--ghost ui-btn--sm" data-action="cancel">Cancelar</button>
        </div>
    </div>

    <div class="ui-nfe-viewer__status-bar">
        <div class="ui-nfe-viewer__status ui-nfe-viewer__status--authorized">
            <span class="ui-nfe-viewer__status-icon">✅</span>
            <span>Autorizada — 15/07/2026 14:32:05</span>
        </div>
        <div class="ui-nfe-viewer__protocolo">
            <label>Protocolo:</label>
            <span>35260712345678901234567890123456781234567890</span>
        </div>
    </div>

    <div class="ui-nfe-viewer__tabs">
        <button class="ui-nfe-viewer__tab ui-nfe-viewer__tab--active" data-tab="identificacao">Identificação</button>
        <button class="ui-nfe-viewer__tab" data-tab="itens">Itens (5)</button>
        <button class="ui-nfe-viewer__tab" data-tab="fiscal">Fiscal</button>
        <button class="ui-nfe-viewer__tab" data-tab="pagamento">Pagamento</button>
        <button class="ui-nfe-viewer__tab" data-tab="transporte">Transporte</button>
        <button class="ui-nfe-viewer__tab" data-tab="cobranca">Cobrança</button>
    </div>

    <div class="ui-nfe-viewer__content">
        <div class="ui-nfe-viewer__panel ui-nfe-viewer__panel--active" id="tab-identificacao">
            <div class="ui-nfe-viewer__grid">
                <div class="ui-nfe-viewer__section">
                    <h4>Emitente</h4>
                    <div class="ui-nfe-viewer__field"><label>CNPJ</label><span>11.222.333/0001-44</span></div>
                    <div class="ui-nfe-viewer__field"><label>Razão Social</label><span>Empresa Exemplo Ltda</span></div>
                    <div class="ui-nfe-viewer__field"><label>IE</label><span>123.456.789.000</span></div>
                </div>
                <div class="ui-nfe-viewer__section">
                    <h4>Destinatário</h4>
                    <div class="ui-nfe-viewer__field"><label>CPF/CNPJ</label><span>123.456.789-00</span></div>
                    <div class="ui-nfe-viewer__field"><label>Nome</label><span>João Silva</span></div>
                    <div class="ui-nfe-viewer__field"><label>IE</label><span>Isento</span></div>
                </div>
            </div>

            <div class="ui-nfe-viewer__section">
                <h4>Informações da Nota</h4>
                <div class="ui-nfe-viewer__grid-4">
                    <div class="ui-nfe-viewer__field"><label>Natureza</label><span>Venda de mercadoria</span></div>
                    <div class="ui-nfe-viewer__field"><label>CFOP</label><span>5.102</span></div>
                    <div class="ui-nfe-viewer__field"><label>Data Emissão</label><span>15/07/2026</span></div>
                    <div class="ui-nfe-viewer__field"><label>Data Saída</label><span>15/07/2026</span></div>
                    <div class="ui-nfe-viewer__field"><label>Chave Acesso</label><span>3526 0712 3456 7890 1234 5678 9012 3456 7890 1234 5678</span></div>
                    <div class="ui-nfe-viewer__field"><label>Modelo</label><span>55</span></div>
                </div>
            </div>

            <div class="ui-nfe-viewer__totalizer">
                <div class="ui-nfe-viewer__total-item">
                    <span class="ui-nfe-viewer__total-label">Base ICMS</span>
                    <span class="ui-nfe-viewer__total-value">R$ 1.000,00</span>
                </div>
                <div class="ui-nfe-viewer__total-item">
                    <span class="ui-nfe-viewer__total-label">Valor ICMS</span>
                    <span class="ui-nfe-viewer__total-value">R$ 180,00</span>
                </div>
                <div class="ui-nfe-viewer__total-item">
                    <span class="ui-nfe-viewer__total-label">Valor Produtos</span>
                    <span class="ui-nfe-viewer__total-value">R$ 1.000,00</span>
                </div>
                <div class="ui-nfe-viewer__total-item ui-nfe-viewer__total-item--highlight">
                    <span class="ui-nfe-viewer__total-label">Total NF-e</span>
                    <span class="ui-nfe-viewer__total-value">R$ 1.216,50</span>
                </div>
            </div>
        </div>
    </div>
</div>
```

```css
.ui-nfe-viewer { background: var(--color-surface); border-radius: var(--radius-lg); border: 1px solid var(--color-border); font-size: var(--font-size-sm); }
.ui-nfe-viewer__toolbar, .ui-nfe-viewer__status-bar { display: flex; justify-content: space-between; align-items: center; padding: var(--spacing-sm) var(--spacing-md); border-bottom: 1px solid var(--color-border); }
.ui-nfe-viewer__title { margin: 0; font-size: var(--font-size-md); }
.ui-nfe-viewer__series { font-size: var(--font-size-xs); color: var(--color-text-muted); margin-left: var(--spacing-sm); }
.ui-nfe-viewer__status { display: flex; align-items: center; gap: var(--spacing-xs); font-weight: var(--font-weight-medium); }
.ui-nfe-viewer__status--authorized { color: var(--color-success); }
.ui-nfe-viewer__status--cancelled { color: var(--color-danger); }
.ui-nfe-viewer__status--pending { color: var(--color-warning); }
.ui-nfe-viewer__protocolo label { color: var(--color-text-muted); }
.ui-nfe-viewer__protocolo span { font-family: monospace; font-size: var(--font-size-xs); }
.ui-nfe-viewer__tabs { display: flex; border-bottom: 1px solid var(--color-border); overflow-x: auto; }
.ui-nfe-viewer__tab { padding: var(--spacing-sm) var(--spacing-md); border: none; background: transparent; cursor: pointer; white-space: nowrap; font-size: var(--font-size-sm); color: var(--color-text-secondary); border-bottom: 2px solid transparent; }
.ui-nfe-viewer__tab--active { color: var(--color-primary); border-bottom-color: var(--color-primary); font-weight: var(--font-weight-medium); }
.ui-nfe-viewer__content { padding: var(--spacing-md); }
.ui-nfe-viewer__panel { display: none; }
.ui-nfe-viewer__panel--active { display: block; }
.ui-nfe-viewer__grid { display: grid; grid-template-columns: 1fr 1fr; gap: var(--spacing-md); margin-bottom: var(--spacing-md); }
.ui-nfe-viewer__grid-4 { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: var(--spacing-sm); }
.ui-nfe-viewer__section h4 { margin: 0 0 var(--spacing-xs); font-size: var(--font-size-xs); text-transform: uppercase; color: var(--color-text-muted); }
.ui-nfe-viewer__field { display: flex; flex-direction: column; padding: 3px 0; }
.ui-nfe-viewer__field label { font-size: var(--font-size-xs); color: var(--color-text-muted); }
.ui-nfe-viewer__field span { font-weight: var(--font-weight-medium); }
.ui-nfe-viewer__totalizer { display: flex; gap: var(--spacing-sm); margin-top: var(--spacing-md); padding: var(--spacing-sm); background: var(--color-surface-alt); border-radius: var(--radius-md); }
.ui-nfe-viewer__total-item { flex: 1; text-align: center; }
.ui-nfe-viewer__total-label { display: block; font-size: var(--font-size-xs); color: var(--color-text-muted); }
.ui-nfe-viewer__total-value { font-weight: var(--font-weight-semibold); }
.ui-nfe-viewer__total-item--highlight .ui-nfe-viewer__total-value { color: var(--color-primary); font-size: var(--font-size-lg); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
