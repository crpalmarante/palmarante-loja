# FiscalUI Framework

## Documento 164 — Dashboard Produção

**Nível 9 — ERP Business Components**

**Versão 1.0**

Dashboard de produção com ordens de produção, eficiência, OEE, status de máquinas.

---

```html
<div class="ui-dashboard-producao">
    <div class="ui-dashboard-producao__header">
        <h2>Dashboard Produção</h2>
        <div class="ui-dashboard-producao__period">
            <span class="ui-dashboard-producao__turno">Turno: A (06:00-14:00)</span>
        </div>
    </div>

    <div class="ui-dashboard-producao__kpi-row">
        <div class="ui-kpi-card ui-kpi-card--primary">
            <span class="ui-kpi-card__value">12</span>
            <span class="ui-kpi-card__label">OPs em Andamento</span>
        </div>
        <div class="ui-kpi-card ui-kpi-card--success">
            <span class="ui-kpi-card__value">87,5%</span>
            <span class="ui-kpi-card__label">Eficiência</span>
        </div>
        <div class="ui-kpi-card">
            <span class="ui-kpi-card__value">72%</span>
            <span class="ui-kpi-card__label">OEE</span>
        </div>
        <div class="ui-kpi-card ui-kpi-card--warning">
            <span class="ui-kpi-card__value">4.320 un</span>
            <span class="ui-kpi-card__label">Produzido (turno)</span>
        </div>
        <div class="ui-kpi-card ui-kpi-card--danger">
            <span class="ui-kpi-card__value">23 min</span>
            <span class="ui-kpi-card__label">Parada (turno)</span>
        </div>
    </div>

    <div class="ui-dashboard-producao__grid">
        <div class="ui-dashboard-producao__card">
            <h3>Ordens de Produção</h3>
            <table class="ui-table ui-table--compact">
                <thead><tr><th>OP</th><th>Produto</th><th>Qtd</th><th>Previsto</th><th>Status</th></tr></thead>
                <tbody>
                    <tr><td>OP-2026-0451</td><td>Arroz 5kg</td><td>500</td><td>15:30</td><td><span class="ui-badge ui-badge--success">Em Produção</span></td></tr>
                    <tr><td>OP-2026-0452</td><td>Feijão 1kg</td><td>300</td><td>17:00</td><td><span class="ui-badge ui-badge--warning">Aguardando</span></td></tr>
                    <tr><td>OP-2026-0453</td><td>Óleo 900ml</td><td>200</td><td>18:30</td><td><span class="ui-badge ui-badge--info">Programada</span></td></tr>
                    <tr><td>OP-2026-0449</td><td>Açúcar 2kg</td><td>400</td><td>—</td><td><span class="ui-badge ui-badge--danger">Atrasada</span></td></tr>
                </tbody>
            </table>
        </div>
        <div class="ui-dashboard-producao__card">
            <h3>Status das Máquinas</h3>
            <div class="ui-dashboard-producao__maquinas">
                <div class="ui-dashboard-producao__maquina">
                    <div class="ui-dashboard-producao__maquina-header">
                        <span class="ui-dashboard-producao__maquina-nome">Linha 1 — Empacotadeira</span>
                        <span class="ui-badge ui-badge--success">Operando</span>
                    </div>
                    <div class="ui-dashboard-producao__maquina-metricas">
                        <span>Rendimento: 95%</span>
                        <span>Velocidade: 120 un/min</span>
                    </div>
                </div>
                <div class="ui-dashboard-producao__maquina">
                    <div class="ui-dashboard-producao__maquina-header">
                        <span class="ui-dashboard-producao__maquina-nome">Linha 2 — Seladora</span>
                        <span class="ui-badge ui-badge--warning">Setup</span>
                    </div>
                    <div class="ui-dashboard-producao__maquina-metricas">
                        <span>Previsão: 15 min</span>
                    </div>
                </div>
                <div class="ui-dashboard-producao__maquina">
                    <div class="ui-dashboard-producao__maquina-header">
                        <span class="ui-dashboard-producao__maquina-nome">Linha 3 — Etiquetadeira</span>
                        <span class="ui-badge ui-badge--danger">Parada</span>
                    </div>
                    <div class="ui-dashboard-producao__maquina-metricas">
                        <span>Motivo: Manutenção</span>
                        <span>Previsão: 14:30</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="ui-dashboard-producao__card">
        <h3>Produção vs. Meta (Hoje)</h3>
        <div class="ui-chart-line" style="height:200px">
            <!-- Line chart by Chart Engine -->
        </div>
    </div>
</div>
```

```css
.ui-dashboard-producao { display: flex; flex-direction: column; gap: var(--spacing-md); }
.ui-dashboard-producao__header { display: flex; justify-content: space-between; align-items: center; }
.ui-dashboard-producao__header h2 { margin: 0; font-size: var(--font-size-xl); }
.ui-dashboard-producao__turno { font-size: var(--font-size-sm); color: var(--color-text-secondary); background: var(--color-surface-alt); padding: var(--spacing-xs) var(--spacing-sm); border-radius: var(--radius-sm); }
.ui-dashboard-producao__kpi-row { display: grid; grid-template-columns: repeat(5, 1fr); gap: var(--spacing-sm); }
.ui-dashboard-producao__grid { display: grid; grid-template-columns: 1fr 1fr; gap: var(--spacing-md); }
.ui-dashboard-producao__card { background: var(--color-surface); border-radius: var(--radius-lg); border: 1px solid var(--color-border); padding: var(--spacing-md); }
.ui-dashboard-producao__card h3 { margin: 0 0 var(--spacing-sm); font-size: var(--font-size-sm); }
.ui-dashboard-producao__maquinas { display: flex; flex-direction: column; gap: var(--spacing-sm); }
.ui-dashboard-producao__maquina { padding: var(--spacing-sm); background: var(--color-surface-alt); border-radius: var(--radius-sm); }
.ui-dashboard-producao__maquina-header { display: flex; justify-content: space-between; align-items: center; }
.ui-dashboard-producao__maquina-nome { font-weight: var(--font-weight-semibold); font-size: var(--font-size-sm); }
.ui-dashboard-producao__maquina-metricas { display: flex; gap: var(--spacing-md); margin-top: 4px; font-size: var(--font-size-xs); color: var(--color-text-secondary); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
