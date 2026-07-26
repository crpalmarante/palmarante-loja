# FiscalUI Framework

## Documento 163 — Dashboard Estoque

**Nível 9 — ERP Business Components**

**Versão 1.0**

Dashboard de estoque com nível atual, produtos críticos, movimentações e giro.

---

```html
<div class="ui-dashboard-estoque">
    <div class="ui-dashboard-estoque__header">
        <h2>Dashboard Estoque</h2>
        <div class="ui-dashboard-estoque__actions">
            <button class="ui-btn ui-btn--ghost ui-btn--sm">🔍 Inventário</button>
            <button class="ui-btn ui-btn--ghost ui-btn--sm">📦 Transferências</button>
        </div>
    </div>

    <div class="ui-dashboard-estoque__kpi-row">
        <div class="ui-kpi-card">
            <span class="ui-kpi-card__value">12.847</span>
            <span class="ui-kpi-card__label">Itens em Estoque</span>
        </div>
        <div class="ui-kpi-card ui-kpi-card--danger">
            <span class="ui-kpi-card__value">23</span>
            <span class="ui-kpi-card__label">Estoque Crítico</span>
        </div>
        <div class="ui-kpi-card ui-kpi-card--warning">
            <span class="ui-kpi-card__value">47</span>
            <span class="ui-kpi-card__label">Estoque Mínimo</span>
        </div>
        <div class="ui-kpi-card">
            <span class="ui-kpi-card__value">R$ 342.500,00</span>
            <span class="ui-kpi-card__label">Valor em Estoque</span>
        </div>
        <div class="ui-kpi-card ui-kpi-card--primary">
            <span class="ui-kpi-card__value">4,2</span>
            <span class="ui-kpi-card__label">Giro (vezes/ano)</span>
        </div>
    </div>

    <div class="ui-dashboard-estoque__grid">
        <div class="ui-dashboard-estoque__card">
            <h3>Produtos com Estoque Crítico ⚠️</h3>
            <table class="ui-table ui-table--compact">
                <thead><tr><th>Produto</th><th>Atual</th><th>Mínimo</th><th>Status</th></tr></thead>
                <tbody>
                    <tr><td>Arroz 5kg</td><td>12</td><td>50</td><td><span class="ui-badge ui-badge--danger">Crítico</span></td></tr>
                    <tr><td>Feijão 1kg</td><td>8</td><td>40</td><td><span class="ui-badge ui-badge--danger">Crítico</span></td></tr>
                    <tr><td>Óleo Soja 900ml</td><td>15</td><td>30</td><td><span class="ui-badge ui-badge--warning">Mínimo</span></td></tr>
                    <tr><td>Açúcar 2kg</td><td>22</td><td>35</td><td><span class="ui-badge ui-badge--warning">Mínimo</span></td></tr>
                </tbody>
            </table>
        </div>
        <div class="ui-dashboard-estoque__card">
            <h3>Movimentações (últimos 7 dias)</h3>
            <div class="ui-dashboard-estoque__movimentos">
                <div class="ui-dashboard-estoque__movimento">
                    <div class="ui-dashboard-estoque__mov-info">
                        <span class="ui-dashboard-estoque__mov-produto">Arroz 5kg</span>
                        <span class="ui-dashboard-estoque__mov-tipo ui-dashboard-estoque__mov-tipo--entrada">Entrada</span>
                    </div>
                    <span class="ui-dashboard-estoque__mov-qtd">+200</span>
                </div>
                <div class="ui-dashboard-estoque__movimento">
                    <div class="ui-dashboard-estoque__mov-info">
                        <span class="ui-dashboard-estoque__mov-produto">Feijão 1kg</span>
                        <span class="ui-dashboard-estoque__mov-tipo ui-dashboard-estoque__mov-tipo--saida">Saída</span>
                    </div>
                    <span class="ui-dashboard-estoque__mov-qtd">-85</span>
                </div>
                <div class="ui-dashboard-estoque__movimento">
                    <div class="ui-dashboard-estoque__mov-info">
                        <span class="ui-dashboard-estoque__mov-produto">Café 500g</span>
                        <span class="ui-dashboard-estoque__mov-tipo ui-dashboard-estoque__mov-tipo--ajuste">Ajuste</span>
                    </div>
                    <span class="ui-dashboard-estoque__mov-qtd">-3</span>
                </div>
            </div>
        </div>
    </div>
</div>
```

```css
.ui-dashboard-estoque { display: flex; flex-direction: column; gap: var(--spacing-md); }
.ui-dashboard-estoque__header { display: flex; justify-content: space-between; align-items: center; }
.ui-dashboard-estoque__header h2 { margin: 0; font-size: var(--font-size-xl); }
.ui-dashboard-estoque__kpi-row { display: grid; grid-template-columns: repeat(5, 1fr); gap: var(--spacing-sm); }
.ui-dashboard-estoque__grid { display: grid; grid-template-columns: 1fr 1fr; gap: var(--spacing-md); }
.ui-dashboard-estoque__card { background: var(--color-surface); border-radius: var(--radius-lg); border: 1px solid var(--color-border); padding: var(--spacing-md); }
.ui-dashboard-estoque__card h3 { margin: 0 0 var(--spacing-sm); font-size: var(--font-size-sm); }
.ui-dashboard-estoque__movimentos { display: flex; flex-direction: column; gap: var(--spacing-xs); }
.ui-dashboard-estoque__movimento { display: flex; justify-content: space-between; align-items: center; padding: var(--spacing-xs) var(--spacing-sm); background: var(--color-surface-alt); border-radius: var(--radius-sm); }
.ui-dashboard-estoque__mov-info { display: flex; align-items: center; gap: var(--spacing-sm); }
.ui-dashboard-estoque__mov-produto { font-weight: var(--font-weight-medium); font-size: var(--font-size-sm); }
.ui-dashboard-estoque__mov-tipo { font-size: var(--font-size-xs); padding: 1px 6px; border-radius: var(--radius-sm); }
.ui-dashboard-estoque__mov-tipo--entrada { background: var(--color-success-light); color: var(--color-success); }
.ui-dashboard-estoque__mov-tipo--saida { background: var(--color-danger-light); color: var(--color-danger); }
.ui-dashboard-estoque__mov-tipo--ajuste { background: var(--color-warning-light); color: var(--color-warning); }
.ui-dashboard-estoque__mov-qtd { font-weight: var(--font-weight-bold); font-size: var(--font-size-sm); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
