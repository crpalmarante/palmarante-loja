# FiscalUI Framework

## Documento 160 — Dashboard Fiscal

**Nível 9 — ERP Business Components**

**Versão 1.0**

Dashboard com indicadores fiscais: notas emitidas, tributos, pendências SEFAZ, apuração.

---

```html
<div class="ui-dashboard-fiscal">
    <div class="ui-dashboard-fiscal__header">
        <h2 class="ui-dashboard-fiscal__title">Dashboard Fiscal</h2>
        <div class="ui-dashboard-fiscal__period">
            <select class="ui-field__select">
                <option>Julho/2026</option>
                <option>Junho/2026</option>
                <option>Maio/2026</option>
            </select>
        </div>
    </div>

    <div class="ui-dashboard-fiscal__kpi-row">
        <div class="ui-kpi-card ui-kpi-card--primary">
            <span class="ui-kpi-card__value">1.234</span>
            <span class="ui-kpi-card__label">NF-e Emitidas</span>
            <span class="ui-kpi-card__change ui-kpi-card__change--up">+12% vs. mês anterior</span>
        </div>
        <div class="ui-kpi-card ui-kpi-card--success">
            <span class="ui-kpi-card__value">98,5%</span>
            <span class="ui-kpi-card__label">Taxa Autorização</span>
            <span class="ui-kpi-card__change ui-kpi-card__change--up">+0,3% vs. mês anterior</span>
        </div>
        <div class="ui-kpi-card ui-kpi-card--danger">
            <span class="ui-kpi-card__value">3</span>
            <span class="ui-kpi-card__label">Notas Rejeitadas</span>
            <span class="ui-kpi-card__change ui-kpi-card__change--down">-5 vs. mês anterior</span>
        </div>
        <div class="ui-kpi-card ui-kpi-card--info">
            <span class="ui-kpi-card__value">R$ 1,2M</span>
            <span class="ui-kpi-card__label">Base ICMS</span>
            <span class="ui-kpi-card__change ui-kpi-card__change--up">+8% vs. mês anterior</span>
        </div>
    </div>

    <div class="ui-dashboard-fiscal__grid">
        <div class="ui-dashboard-fiscal__chart-card">
            <h3>Notas por Dia</h3>
            <div class="ui-dashboard-fiscal__chart-placeholder">
                <div class="ui-chart-bar" style="height:150px">
                    <!-- Chart bars rendered by Chart Engine -->
                </div>
            </div>
        </div>
        <div class="ui-dashboard-fiscal__chart-card">
            <h3>Tributos Apurados</h3>
            <div class="ui-dashboard-fiscal__chart-placeholder">
                <div class="ui-chart-pie" style="height:150px">
                    <!-- Pie chart rendered by Chart Engine -->
                </div>
            </div>
        </div>
    </div>

    <div class="ui-dashboard-fiscal__table-section">
        <h3>Últimas Notas</h3>
        <table class="ui-table ui-table--compact">
            <thead>
                <tr><th>NFe</th><th>Cliente</th><th>Valor</th><th>Status</th><th>Data</th></tr>
            </thead>
            <tbody>
                <tr><td>000.123.456</td><td>João Silva</td><td>R$ 1.216,50</td><td><span class="ui-badge ui-badge--success">Autorizada</span></td><td>15/07</td></tr>
                <tr><td>000.123.457</td><td>Maria Souza</td><td>R$ 3.450,00</td><td><span class="ui-badge ui-badge--warning">Denegada</span></td><td>15/07</td></tr>
                <tr><td>000.123.458</td><td>Carlos Lima</td><td>R$ 890,00</td><td><span class="ui-badge ui-badge--success">Autorizada</span></td><td>14/07</td></tr>
            </tbody>
        </table>
    </div>
</div>
```

```css
.ui-dashboard-fiscal { display: flex; flex-direction: column; gap: var(--spacing-md); }
.ui-dashboard-fiscal__header { display: flex; justify-content: space-between; align-items: center; }
.ui-dashboard-fiscal__title { margin: 0; font-size: var(--font-size-xl); }
.ui-dashboard-fiscal__kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--spacing-sm); }
.ui-dashboard-fiscal__grid { display: grid; grid-template-columns: 1fr 1fr; gap: var(--spacing-md); }
.ui-dashboard-fiscal__chart-card { background: var(--color-surface); border-radius: var(--radius-lg); border: 1px solid var(--color-border); padding: var(--spacing-md); }
.ui-dashboard-fiscal__chart-card h3 { margin: 0 0 var(--spacing-sm); font-size: var(--font-size-sm); }
.ui-dashboard-fiscal__chart-placeholder { display: flex; align-items: flex-end; justify-content: center; min-height: 150px; }
.ui-dashboard-fiscal__table-section { background: var(--color-surface); border-radius: var(--radius-lg); border: 1px solid var(--color-border); padding: var(--spacing-md); }
.ui-dashboard-fiscal__table-section h3 { margin: 0 0 var(--spacing-sm); font-size: var(--font-size-sm); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
