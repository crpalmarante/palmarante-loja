# FiscalUI Framework

## Documento 161 — Dashboard Financeiro

**Nível 9 — ERP Business Components**

**Versão 1.0**

Dashboard financeiro com fluxo de caixa, contas a pagar/receber, DRE simplificado.

---

```html
<div class="ui-dashboard-financeiro">
    <div class="ui-dashboard-financeiro__header">
        <h2>Dashboard Financeiro</h2>
        <div class="ui-dashboard-financeiro__date-range">
            <button class="ui-btn ui-btn--ghost ui-btn--sm ui-btn--active">Hoje</button>
            <button class="ui-btn ui-btn--ghost ui-btn--sm">7 dias</button>
            <button class="ui-btn ui-btn--ghost ui-btn--sm">30 dias</button>
            <button class="ui-btn ui-btn--ghost ui-btn--sm">Este mês</button>
        </div>
    </div>

    <div class="ui-dashboard-financeiro__kpi-row">
        <div class="ui-kpi-card ui-kpi-card--success">
            <span class="ui-kpi-card__value">R$ 45.230,00</span>
            <span class="ui-kpi-card__label">Receitas (mês)</span>
        </div>
        <div class="ui-kpi-card ui-kpi-card--danger">
            <span class="ui-kpi-card__value">R$ 32.100,00</span>
            <span class="ui-kpi-card__label">Despesas (mês)</span>
        </div>
        <div class="ui-kpi-card ui-kpi-card--primary">
            <span class="ui-kpi-card__value">R$ 13.130,00</span>
            <span class="ui-kpi-card__label">Saldo</span>
            <span class="ui-kpi-card__change ui-kpi-card__change--up">+29% vs. mês anterior</span>
        </div>
        <div class="ui-kpi-card">
            <span class="ui-kpi-card__value">R$ 8.500,00</span>
            <span class="ui-kpi-card__label">A Receber (30d)</span>
        </div>
        <div class="ui-kpi-card ui-kpi-card--warning">
            <span class="ui-kpi-card__value">R$ 3.200,00</span>
            <span class="ui-kpi-card__label">A Pagar (30d)</span>
        </div>
    </div>

    <div class="ui-dashboard-financeiro__grid">
        <div class="ui-dashboard-financeiro__card">
            <h3>Fluxo de Caixa</h3>
            <div class="ui-dashboard-financeiro__chart">
                <div class="ui-chart-area" style="height:200px">
                    <!-- Area chart by Chart Engine -->
                </div>
            </div>
        </div>
        <div class="ui-dashboard-financeiro__card">
            <h3>Distribuição de Despesas</h3>
            <div class="ui-dashboard-financeiro__chart">
                <div class="ui-chart-donut" style="height:200px">
                    <!-- Donut chart by Chart Engine -->
                </div>
            </div>
        </div>
    </div>

    <div class="ui-dashboard-financeiro__card">
        <h3>DRE Simplificado — Julho/2026</h3>
        <table class="ui-table ui-table--compact">
            <thead><tr><th>Conta</th><th>Valor</th><th>%</th></tr></thead>
            <tbody>
                <tr><td>Receita Bruta</td><td>R$ 45.230,00</td><td>100%</td></tr>
                <tr><td>(-) Impostos</td><td>R$ 9.046,00</td><td>20%</td></tr>
                <tr><td>(-) CMV</td><td>R$ 18.092,00</td><td>40%</td></tr>
                <tr class="ui-table__row-highlight"><td><strong>Lucro Bruto</strong></td><td><strong>R$ 18.092,00</strong></td><td><strong>40%</strong></td></tr>
                <tr><td>(-) Despesas Operacionais</td><td>R$ 4.962,00</td><td>11%</td></tr>
                <tr class="ui-table__row-highlight"><td><strong>Lucro Líquido</strong></td><td><strong>R$ 13.130,00</strong></td><td><strong>29%</strong></td></tr>
            </tbody>
        </table>
    </div>
</div>
```

```css
.ui-dashboard-financeiro { display: flex; flex-direction: column; gap: var(--spacing-md); }
.ui-dashboard-financeiro__header { display: flex; justify-content: space-between; align-items: center; }
.ui-dashboard-financeiro__header h2 { margin: 0; font-size: var(--font-size-xl); }
.ui-dashboard-financeiro__date-range { display: flex; gap: 4px; }
.ui-dashboard-financeiro__kpi-row { display: grid; grid-template-columns: repeat(5, 1fr); gap: var(--spacing-sm); }
.ui-dashboard-financeiro__grid { display: grid; grid-template-columns: 1fr 1fr; gap: var(--spacing-md); }
.ui-dashboard-financeiro__card { background: var(--color-surface); border-radius: var(--radius-lg); border: 1px solid var(--color-border); padding: var(--spacing-md); }
.ui-dashboard-financeiro__card h3 { margin: 0 0 var(--spacing-sm); font-size: var(--font-size-sm); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
