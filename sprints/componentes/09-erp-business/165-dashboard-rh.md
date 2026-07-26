# FiscalUI Framework

## Documento 165 — Dashboard RH

**Nível 9 — ERP Business Components**

**Versão 1.0**

Dashboard de RH com quadro de funcionários, ponto, férias, recrutamento e indicadores.

---

```html
<div class="ui-dashboard-rh">
    <div class="ui-dashboard-rh__header">
        <h2>Dashboard RH</h2>
        <div class="ui-dashboard-rh__actions">
            <button class="ui-btn ui-btn--primary ui-btn--sm">+ Novo Funcionário</button>
        </div>
    </div>

    <div class="ui-dashboard-rh__kpi-row">
        <div class="ui-kpi-card">
            <span class="ui-kpi-card__value">48</span>
            <span class="ui-kpi-card__label">Funcionários Ativos</span>
        </div>
        <div class="ui-kpi-card ui-kpi-card--warning">
            <span class="ui-kpi-card__value">5</span>
            <span class="ui-kpi-card__label">Em Férias</span>
        </div>
        <div class="ui-kpi-card ui-kpi-card--danger">
            <span class="ui-kpi-card__value">3</span>
            <span class="ui-kpi-card__label">Afastados</span>
        </div>
        <div class="ui-kpi-card ui-kpi-card--primary">
            <span class="ui-kpi-card__value">4</span>
            <span class="ui-kpi-card__label">Em Recrutamento</span>
        </div>
        <div class="ui-kpi-card ui-kpi-card--success">
            <span class="ui-kpi-card__value">R$ 285.000,00</span>
            <span class="ui-kpi-card__label">Folha (mês)</span>
        </div>
    </div>

    <div class="ui-dashboard-rh__grid-3">
        <div class="ui-dashboard-rh__card">
            <h3>Departamentos</h3>
            <div class="ui-dashboard-rh__departamentos">
                <div class="ui-dashboard-rh__depto">
                    <span>Administrativo</span>
                    <span class="ui-dashboard-rh__depto-count">12</span>
                </div>
                <div class="ui-dashboard-rh__depto">
                    <span>Comercial</span>
                    <span class="ui-dashboard-rh__depto-count">10</span>
                </div>
                <div class="ui-dashboard-rh__depto">
                    <span>Produção</span>
                    <span class="ui-dashboard-rh__depto-count">15</span>
                </div>
                <div class="ui-dashboard-rh__depto">
                    <span>Logística</span>
                    <span class="ui-dashboard-rh__depto-count">6</span>
                </div>
                <div class="ui-dashboard-rh__depto">
                    <span>TI</span>
                    <span class="ui-dashboard-rh__depto-count">5</span>
                </div>
            </div>
        </div>
        <div class="ui-dashboard-rh__card">
            <h3>Aniversariantes do Mês 🎂</h3>
            <div class="ui-dashboard-rh__aniversariantes">
                <div class="ui-dashboard-rh__aniv-item">
                    <div class="ui-avatar ui-avatar--sm" data-initials="MC"></div>
                    <div><strong>Maria Costa</strong><span> — 15/08</span></div>
                </div>
                <div class="ui-dashboard-rh__aniv-item">
                    <div class="ui-avatar ui-avatar--sm" data-initials="PS"></div>
                    <div><strong>Pedro Santos</strong><span> — 22/08</span></div>
                </div>
                <div class="ui-dashboard-rh__aniv-item">
                    <div class="ui-avatar ui-avatar--sm" data-initials="AL"></div>
                    <div><strong>Ana Lima</strong><span> — 28/08</span></div>
                </div>
            </div>
        </div>
        <div class="ui-dashboard-rh__card">
            <h3>Recrutamento</h3>
            <div class="ui-dashboard-rh__vagas">
                <div class="ui-dashboard-rh__vaga">
                    <div class="ui-dashboard-rh__vaga-info">
                        <span class="ui-dashboard-rh__vaga-titulo">Analista Fiscal</span>
                        <span class="ui-dashboard-rh__vaga-status ui-dashboard-rh__vaga-status--aberta">Aberta</span>
                    </div>
                    <span class="ui-dashboard-rh__vaga-candidatos">12 candidatos</span>
                </div>
                <div class="ui-dashboard-rh__vaga">
                    <div class="ui-dashboard-rh__vaga-info">
                        <span class="ui-dashboard-rh__vaga-titulo">Desenvolvedor COBOL</span>
                        <span class="ui-dashboard-rh__vaga-status ui-dashboard-rh__vaga-status--aberta">Aberta</span>
                    </div>
                    <span class="ui-dashboard-rh__vaga-candidatos">5 candidatos</span>
                </div>
                <div class="ui-dashboard-rh__vaga">
                    <div class="ui-dashboard-rh__vaga-info">
                        <span class="ui-dashboard-rh__vaga-titulo">Auxiliar Produção</span>
                        <span class="ui-dashboard-rh__vaga-status ui-dashboard-rh__vaga-status--fechada">Fechada</span>
                    </div>
                    <span class="ui-dashboard-rh__vaga-candidatos">Contratado</span>
                </div>
            </div>
        </div>
    </div>

    <div class="ui-dashboard-rh__card">
        <h3>Férias Programadas — Próximos 30 dias</h3>
        <table class="ui-table ui-table--compact">
            <thead><tr><th>Funcionário</th><th>Departamento</th><th>Início</th><th>Fim</th><th>Dias</th></tr></thead>
            <tbody>
                <tr><td>João Silva</td><td>Administrativo</td><td>01/08</td><td>20/08</td><td>20</td></tr>
                <tr><td>Maria Souza</td><td>Comercial</td><td>05/08</td><td>19/08</td><td>15</td></tr>
                <tr><td>Carlos Lima</td><td>Produção</td><td>10/08</td><td>24/08</td><td>15</td></tr>
            </tbody>
        </table>
    </div>
</div>
```

```css
.ui-dashboard-rh { display: flex; flex-direction: column; gap: var(--spacing-md); }
.ui-dashboard-rh__header { display: flex; justify-content: space-between; align-items: center; }
.ui-dashboard-rh__header h2 { margin: 0; font-size: var(--font-size-xl); }
.ui-dashboard-rh__kpi-row { display: grid; grid-template-columns: repeat(5, 1fr); gap: var(--spacing-sm); }
.ui-dashboard-rh__grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: var(--spacing-md); }
.ui-dashboard-rh__card { background: var(--color-surface); border-radius: var(--radius-lg); border: 1px solid var(--color-border); padding: var(--spacing-md); }
.ui-dashboard-rh__card h3 { margin: 0 0 var(--spacing-sm); font-size: var(--font-size-sm); }
.ui-dashboard-rh__departamentos { display: flex; flex-direction: column; gap: var(--spacing-xs); }
.ui-dashboard-rh__depto { display: flex; justify-content: space-between; padding: var(--spacing-xs) 0; font-size: var(--font-size-sm); border-bottom: 1px solid var(--color-border-alt); }
.ui-dashboard-rh__depto-count { font-weight: var(--font-weight-bold); }
.ui-dashboard-rh__aniversariantes { display: flex; flex-direction: column; gap: var(--spacing-sm); }
.ui-dashboard-rh__aniv-item { display: flex; align-items: center; gap: var(--spacing-sm); font-size: var(--font-size-sm); }
.ui-dashboard-rh__vagas { display: flex; flex-direction: column; gap: var(--spacing-sm); }
.ui-dashboard-rh__vaga { display: flex; flex-direction: column; gap: 2px; padding: var(--spacing-xs) 0; }
.ui-dashboard-rh__vaga-info { display: flex; justify-content: space-between; align-items: center; }
.ui-dashboard-rh__vaga-titulo { font-weight: var(--font-weight-medium); font-size: var(--font-size-sm); }
.ui-dashboard-rh__vaga-candidatos { font-size: var(--font-size-xs); color: var(--color-text-muted); }
.ui-dashboard-rh__vaga-status { font-size: var(--font-size-xs); padding: 1px 6px; border-radius: var(--radius-sm); }
.ui-dashboard-rh__vaga-status--aberta { background: var(--color-success-light); color: var(--color-success); }
.ui-dashboard-rh__vaga-status--fechada { background: var(--color-surface-alt); color: var(--color-text-muted); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
