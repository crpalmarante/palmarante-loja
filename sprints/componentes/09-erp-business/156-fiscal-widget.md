# FiscalUI Framework

## Documento 156 — Fiscal Widget

**Nível 9 — ERP Business Components**

**Versão 1.0**

Widget fiscal com classificação tributária, alíquotas, NCM, CST e regime.

---

```html
<div class="ui-fiscal-widget">
    <div class="ui-fiscal-widget__header">
        <h3 class="ui-fiscal-widget__title">Classificação Fiscal</h3>
        <div class="ui-fiscal-widget__period">
            <span>Vigência: Jul/2026</span>
        </div>
    </div>

    <div class="ui-fiscal-widget__body">
        <div class="ui-fiscal-widget__section">
            <h4>Tributação</h4>
            <div class="ui-fiscal-widget__row">
                <div class="ui-fiscal-widget__field">
                    <label>Regime</label>
                    <span class="ui-tag ui-tag--success">Simples Nacional</span>
                </div>
                <div class="ui-fiscal-widget__field">
                    <label>CRT</label>
                    <span>1</span>
                </div>
                <div class="ui-fiscal-widget__field">
                    <label>Alíquota ICMS</label>
                    <span>18,00%</span>
                </div>
            </div>
        </div>

        <div class="ui-fiscal-widget__section">
            <h4>Códigos Fiscais</h4>
            <div class="ui-fiscal-widget__codes">
                <div class="ui-fiscal-widget__code-item">
                    <span class="ui-fiscal-widget__code-label">NCM</span>
                    <span class="ui-fiscal-widget__code-value">1006.30.11</span>
                    <button class="ui-btn ui-btn--ghost ui-btn--xs" data-action="ncm-detail">🔍</button>
                </div>
                <div class="ui-fiscal-widget__code-item">
                    <span class="ui-fiscal-widget__code-label">CST ICMS</span>
                    <span class="ui-fiscal-widget__code-value">00</span>
                    <span class="ui-fiscal-widget__code-desc">Tributada integralmente</span>
                </div>
                <div class="ui-fiscal-widget__code-item">
                    <span class="ui-fiscal-widget__code-label">CST PIS</span>
                    <span class="ui-fiscal-widget__code-value">01</span>
                    <span class="ui-fiscal-widget__code-desc">Operação Tributável</span>
                </div>
                <div class="ui-fiscal-widget__code-item">
                    <span class="ui-fiscal-widget__code-label">CST COFINS</span>
                    <span class="ui-fiscal-widget__code-value">01</span>
                    <span class="ui-fiscal-widget__code-desc">Operação Tributável</span>
                </div>
                <div class="ui-fiscal-widget__code-item">
                    <span class="ui-fiscal-widget__code-label">CFOP</span>
                    <span class="ui-fiscal-widget__code-value">5.102</span>
                    <span class="ui-fiscal-widget__code-desc">Venda merc. adquirida</span>
                </div>
            </div>
        </div>

        <div class="ui-fiscal-widget__section">
            <h4>Cálculo Tributário</h4>
            <div class="ui-fiscal-widget__calc">
                <div class="ui-fiscal-widget__calc-row">
                    <span>Base de Cálculo ICMS</span>
                    <span>R$ 1.000,00</span>
                </div>
                <div class="ui-fiscal-widget__calc-row">
                    <span>Valor ICMS</span>
                    <span class="ui-fiscal-widget__calc-value">R$ 180,00</span>
                </div>
                <div class="ui-fiscal-widget__calc-row">
                    <span>Valor PIS</span>
                    <span class="ui-fiscal-widget__calc-value">R$ 6,50</span>
                </div>
                <div class="ui-fiscal-widget__calc-row">
                    <span>Valor COFINS</span>
                    <span class="ui-fiscal-widget__calc-value">R$ 30,00</span>
                </div>
                <div class="ui-fiscal-widget__calc-row ui-fiscal-widget__calc-row--total">
                    <span>Carga Tributária Total</span>
                    <span class="ui-fiscal-widget__calc-total">R$ 216,50 (21,65%)</span>
                </div>
            </div>
        </div>
    </div>
</div>
```

```css
.ui-fiscal-widget { background: var(--color-surface); border-radius: var(--radius-lg); border: 1px solid var(--color-border); }
.ui-fiscal-widget__header { display: flex; justify-content: space-between; align-items: center; padding: var(--spacing-md); border-bottom: 1px solid var(--color-border); }
.ui-fiscal-widget__title { margin: 0; font-size: var(--font-size-md); font-weight: var(--font-weight-semibold); }
.ui-fiscal-widget__period { font-size: var(--font-size-xs); color: var(--color-text-muted); }
.ui-fiscal-widget__body { padding: var(--spacing-md); display: flex; flex-direction: column; gap: var(--spacing-md); }
.ui-fiscal-widget__section h4 { margin: 0 0 var(--spacing-sm); font-size: var(--font-size-xs); text-transform: uppercase; color: var(--color-text-muted); letter-spacing: 0.5px; }
.ui-fiscal-widget__row { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: var(--spacing-sm); }
.ui-fiscal-widget__field label { display: block; font-size: var(--font-size-xs); color: var(--color-text-muted); margin-bottom: 2px; }
.ui-fiscal-widget__field span { font-size: var(--font-size-sm); font-weight: var(--font-weight-medium); }
.ui-fiscal-widget__codes { display: flex; flex-direction: column; gap: 4px; }
.ui-fiscal-widget__code-item { display: flex; align-items: center; gap: var(--spacing-sm); padding: var(--spacing-xs) var(--spacing-sm); background: var(--color-surface-alt); border-radius: var(--radius-sm); font-size: var(--font-size-sm); }
.ui-fiscal-widget__code-label { color: var(--color-text-muted); min-width: 80px; }
.ui-fiscal-widget__code-value { font-weight: var(--font-weight-semibold); min-width: 40px; }
.ui-fiscal-widget__code-desc { color: var(--color-text-secondary); font-size: var(--font-size-xs); }
.ui-fiscal-widget__calc { display: flex; flex-direction: column; gap: 4px; }
.ui-fiscal-widget__calc-row { display: flex; justify-content: space-between; padding: 4px 0; font-size: var(--font-size-sm); }
.ui-fiscal-widget__calc-row--total { border-top: 2px solid var(--color-border); margin-top: 4px; padding-top: 8px; }
.ui-fiscal-widget__calc-total { font-weight: var(--font-weight-bold); color: var(--color-primary); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
