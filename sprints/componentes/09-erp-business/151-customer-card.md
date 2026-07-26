# FiscalUI Framework

## Documento 151 — Customer Card

**Nível 9 — ERP Business Components**

**Versão 1.0**

Ficha resumo do cliente com dados cadastrais, contato, classificação fiscal e indicadores.

---

```html
<div class="ui-customer-card">
    <div class="ui-customer-card__header">
        <div class="ui-customer-card__avatar">
            <div class="ui-avatar ui-avatar--lg" data-initials="JS"></div>
        </div>
        <div class="ui-customer-card__info">
            <h3 class="ui-customer-card__name">João Silva</h3>
            <span class="ui-customer-card__doc">CPF: 123.456.789-00</span>
            <span class="ui-customer-card__status ui-customer-card__status--active">Ativo</span>
        </div>
        <div class="ui-customer-card__actions">
            <button class="ui-btn ui-btn--ghost ui-btn--sm" data-action="edit">Editar</button>
            <button class="ui-btn ui-btn--ghost ui-btn--sm" data-action="more">⋮</button>
        </div>
    </div>

    <div class="ui-customer-card__body">
        <div class="ui-customer-card__section">
            <h4>Contato</h4>
            <div class="ui-customer-card__field"><label>Telefone</label><span>(11) 99999-8888</span></div>
            <div class="ui-customer-card__field"><label>Email</label><span>joao@email.com</span></div>
        </div>
        <div class="ui-customer-card__section">
            <h4>Endereço</h4>
            <div class="ui-customer-card__field"><label>CEP</label><span>01001-000</span></div>
            <div class="ui-customer-card__field"><label>Cidade</label><span>São Paulo - SP</span></div>
        </div>
        <div class="ui-customer-card__section">
            <h4>Classificação Fiscal</h4>
            <div class="ui-customer-card__field"><label>Regime</label><span>Simples Nacional</span></div>
            <div class="ui-customer-card__field"><label>ICMS</label><span>Contribuinte</span></div>
            <div class="ui-customer-card__field"><label>Suframa</label><span>Não</span></div>
        </div>
    </div>

    <div class="ui-customer-card__footer">
        <div class="ui-customer-card__metric">
            <span class="ui-customer-card__metric-value">R$ 15.430,00</span>
            <span class="ui-customer-card__metric-label">Total em notas (mês)</span>
        </div>
        <div class="ui-customer-card__metric">
            <span class="ui-customer-card__metric-value">12</span>
            <span class="ui-customer-card__metric-label">Notas emitidas (mês)</span>
        </div>
        <div class="ui-customer-card__metric">
            <span class="ui-customer-card__metric-value">R$ 0,00</span>
            <span class="ui-customer-card__metric-label">Pendências</span>
        </div>
    </div>
</div>
```

```css
.ui-customer-card { background: var(--color-surface); border-radius: var(--radius-lg); border: 1px solid var(--color-border); overflow: hidden; }
.ui-customer-card__header { display: flex; align-items: center; gap: var(--spacing-md); padding: var(--spacing-md); border-bottom: 1px solid var(--color-border); }
.ui-customer-card__info { flex: 1; display: flex; flex-direction: column; gap: 2px; }
.ui-customer-card__name { margin: 0; font-size: var(--font-size-lg); font-weight: var(--font-weight-semibold); }
.ui-customer-card__doc { font-size: var(--font-size-sm); color: var(--color-text-secondary); }
.ui-customer-card__status { display: inline-flex; align-items: center; gap: 4px; font-size: var(--font-size-xs); font-weight: var(--font-weight-medium); padding: 2px 8px; border-radius: var(--radius-full); }
.ui-customer-card__status--active { background: var(--color-success-light); color: var(--color-success); }
.ui-customer-card__status--inactive { background: var(--color-danger-light); color: var(--color-danger); }

.ui-customer-card__body { padding: var(--spacing-md); display: grid; grid-template-columns: 1fr 1fr 1fr; gap: var(--spacing-md); }
.ui-customer-card__section h4 { margin: 0 0 var(--spacing-xs); font-size: var(--font-size-xs); text-transform: uppercase; color: var(--color-text-muted); letter-spacing: 0.5px; }
.ui-customer-card__field { display: flex; justify-content: space-between; padding: 2px 0; font-size: var(--font-size-sm); }
.ui-customer-card__field label { color: var(--color-text-secondary); }
.ui-customer-card__field span { font-weight: var(--font-weight-medium); }

.ui-customer-card__footer { display: flex; background: var(--color-surface-alt); border-top: 1px solid var(--color-border); }
.ui-customer-card__metric { flex: 1; padding: var(--spacing-sm) var(--spacing-md); text-align: center; }
.ui-customer-card__metric + .ui-customer-card__metric { border-left: 1px solid var(--color-border); }
.ui-customer-card__metric-value { display: block; font-size: var(--font-size-lg); font-weight: var(--font-weight-bold); }
.ui-customer-card__metric-label { font-size: var(--font-size-xs); color: var(--color-text-secondary); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
