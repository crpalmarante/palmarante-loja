# FiscalUI Framework

## Documento 039 — Spinner

**Nível 2 — Basic Components**

**Versão 1.0**

Indicador circular de carregamento. Usado em botões, containers ou como overlay.

---

```js
class UISpinner extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.size = options.size || 'md';          // sm, md, lg
        this.variant = options.variant || 'primary';
        this.label = options.label || '';
    }

    template() {
        return `
            <div class="ui-spinner ui-spinner--${this.size}" role="status" aria-label="Carregando">
                <svg class="ui-spinner__circle" viewBox="0 0 24 24">
                    <circle class="ui-spinner__track" cx="12" cy="12" r="10" fill="none" stroke-width="3"/>
                    <circle class="ui-spinner__bar ui-spinner__bar--${this.variant}" cx="12" cy="12" r="10" fill="none" stroke-width="3"
                            stroke-dasharray="62.83" stroke-dashoffset="15" stroke-linecap="round"/>
                </svg>
                ${this.label ? `<span class="ui-spinner__label">${this.label}</span>` : ''}
            </div>
        `;
    }
}
```

```css
.ui-spinner {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-xs);
}

.ui-spinner__circle { animation: ui-spin 1s linear infinite; }
.ui-spinner__track { stroke: var(--color-surface-hover); }
.ui-spinner__bar { stroke: var(--color-primary); }

.ui-spinner__bar--primary { stroke: var(--color-primary); }
.ui-spinner__bar--success { stroke: var(--color-success); }
.ui-spinner__bar--warning { stroke: var(--color-warning); }
.ui-spinner__bar--danger  { stroke: var(--color-danger); }

.ui-spinner__label { font-size: var(--font-size-sm); color: var(--color-text-secondary); }

.ui-spinner--sm .ui-spinner__circle { width: 16px; height: 16px; }
.ui-spinner--md .ui-spinner__circle { width: 24px; height: 24px; }
.ui-spinner--lg .ui-spinner__circle { width: 40px; height: 40px; }

@keyframes ui-spin {
    to { transform: rotate(360deg); }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial |
