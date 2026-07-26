# FiscalUI Framework

## Documento 162 — Dashboard Comercial

**Nível 9 — ERP Business Components**

**Versão 1.0**

Dashboard comercial com vendas, ticket médio, desempenho por vendedor, top produtos.

---

```html
<div class="ui-dashboard-comercial">
    <div class="ui-dashboard-comercial__header">
        <h2>Dashboard Comercial</h2>
        <div class="ui-dashboard-comercial__actions">
            <button class="ui-btn ui-btn--primary ui-btn--sm">Exportar Relatório</button>
        </div>
    </div>

    <div class="ui-dashboard-comercial__kpi-row">
        <div class="ui-kpi-card ui-kpi-card--primary">
            <span class="ui-kpi-card__value">R$ 89.450,00</span>
            <span class="ui-kpi-card__label">Vendas (mês)</span>
            <span class="ui-kpi-card__change ui-kpi-card__change--up">+15% vs. meta</span>
        </div>
        <div class="ui-kpi-card">
            <span class="ui-kpi-card__value">847</span>
            <span class="ui-kpi-card__label">Pedidos (mês)</span>
        </div>
        <div class="ui-kpi-card">
            <span class="ui-kpi-card__value">R$ 105,60</span>
            <span class="ui-kpi-card__label">Ticket Médio</span>
            <span class="ui-kpi-card__change ui-kpi-card__change--up">+3,2%</span>
        </div>
        <div class="ui-kpi-card ui-kpi-card--success">
            <span class="ui-kpi-card__value">92%</span>
            <span class="ui-kpi-card__label">Conversão</span>
        </div>
    </div>

    <div class="ui-dashboard-comercial__grid">
        <div class="ui-dashboard-comercial__card">
            <h3>Vendas por Período</h3>
            <div class="ui-chart-bar" style="height:200px">
                <!-- Bar chart -->
            </div>
        </div>
        <div class="ui-dashboard-comercial__card">
            <h3>Desempenho por Vendedor</h3>
            <table class="ui-table ui-table--compact">
                <thead><tr><th>Vendedor</th><th>Vendas</th><th>Meta</th><th>%</th></tr></thead>
                <tbody>
                    <tr><td>Ana Costa</td><td>R$ 28.500,00</td><td>R$ 25.000,00</td><td><span class="ui-badge ui-badge--success">114%</span></td></tr>
                    <tr><td>Pedro Santos</td><td>R$ 22.300,00</td><td>R$ 25.000,00</td><td><span class="ui-badge ui-badge--warning">89%</span></td></tr>
                    <tr><td>Lucas Oliveira</td><td>R$ 19.800,00</td><td>R$ 20.000,00</td><td><span class="ui-badge ui-badge--info">99%</span></td></tr>
                    <tr><td>Maria Fernandes</td><td>R$ 18.850,00</td><td>R$ 20.000,00</td><td><span class="ui-badge ui-badge--warning">94%</span></td></tr>
                </tbody>
            </table>
        </div>
    </div>

    <div class="ui-dashboard-comercial__grid-3">
        <div class="ui-dashboard-comercial__card">
            <h3>Top Produtos</h3>
            <div class="ui-dashboard-comercial__ranking">
                <div class="ui-dashboard-comercial__rank-item">1. Arroz 5kg — 342 un</div>
                <div class="ui-dashboard-comercial__rank-item">2. Feijão 1kg — 280 un</div>
                <div class="ui-dashboard-comercial__rank-item">3. Óleo Soja — 195 un</div>
                <div class="ui-dashboard-comercial__rank-item">4. Açúcar 2kg — 167 un</div>
                <div class="ui-dashboard-comercial__rank-item">5. Café 500g — 143 un</div>
            </div>
        </div>
        <div class="ui-dashboard-comercial__card">
            <h3>Vendas por Categoria</h3>
            <div class="ui-chart-pie" style="height:200px">
                <!-- Pie chart -->
            </div>
        </div>
        <div class="ui-dashboard-comercial__card">
            <h3>Metas</h3>
            <div class="ui-dashboard-comercial__metas">
                <div class="ui-dashboard-comercial__meta-item">
                    <div class="ui-dashboard-comercial__meta-header">
                        <span>Vendas</span><span>89%</span>
                    </div>
                    <div class="ui-progress-bar"><div class="ui-progress-bar__fill" style="width:89%"></div></div>
                </div>
                <div class="ui-dashboard-comercial__meta-item">
                    <div class="ui-dashboard-comercial__meta-header">
                        <span>Novos Clientes</span><span>120%</span>
                    </div>
                    <div class="ui-progress-bar"><div class="ui-progress-bar__fill ui-progress-bar__fill--success" style="width:100%"></div></div>
                </div>
                <div class="ui-dashboard-comercial__meta-item">
                    <div class="ui-dashboard-comercial__meta-header">
                        <span>Ticket Médio</span><span>72%</span>
                    </div>
                    <div class="ui-progress-bar"><div class="ui-progress-bar__fill ui-progress-bar__fill--warning" style="width:72%"></div></div>
                </div>
            </div>
        </div>
    </div>
</div>
```

```css
.ui-dashboard-comercial { display: flex; flex-direction: column; gap: var(--spacing-md); }
.ui-dashboard-comercial__header { display: flex; justify-content: space-between; align-items: center; }
.ui-dashboard-comercial__header h2 { margin: 0; font-size: var(--font-size-xl); }
.ui-dashboard-comercial__kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--spacing-sm); }
.ui-dashboard-comercial__grid { display: grid; grid-template-columns: 1fr 1fr; gap: var(--spacing-md); }
.ui-dashboard-comercial__grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: var(--spacing-md); }
.ui-dashboard-comercial__card { background: var(--color-surface); border-radius: var(--radius-lg); border: 1px solid var(--color-border); padding: var(--spacing-md); }
.ui-dashboard-comercial__card h3 { margin: 0 0 var(--spacing-sm); font-size: var(--font-size-sm); }
.ui-dashboard-comercial__ranking { display: flex; flex-direction: column; gap: var(--spacing-xs); }
.ui-dashboard-comercial__rank-item { padding: var(--spacing-xs) var(--spacing-sm); background: var(--color-surface-alt); border-radius: var(--radius-sm); font-size: var(--font-size-sm); }
.ui-dashboard-comercial__metas { display: flex; flex-direction: column; gap: var(--spacing-md); }
.ui-dashboard-comercial__meta-header { display: flex; justify-content: space-between; font-size: var(--font-size-sm); margin-bottom: 4px; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
