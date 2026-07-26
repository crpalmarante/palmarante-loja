# FiscalUI Framework

## Documento 025 — Badge

**Nível 2 — Basic Components**

**Versão 1.0**

Indicador numérico ou textual pequeno. Notificações, contadores, status.

---

```js
class UIBadge extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.value = options.value || '';
        this.variant = options.variant || 'default';  // default, primary, success, warning, danger
        this.size = options.size || 'md';
        this.dot = options.dot || false;               // modo bolinha
        this.max = options.max || 99;                  // valor máximo exibido
    }

    template() {
        const display = this.dot ? '' : (typeof this.value === 'number' && this.value > this.max ? `${this.max}+` : this.value);
        const cls = `ui-badge ui-badge--${this.variant} ui-badge--${this.size} ${this.dot ? 'ui-badge--dot' : ''}`;
        return `<span class="${cls}">${display}</span>`;
    }
}
```

```css
.ui-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: var(--font-weight-bold);
    white-space: nowrap;
    border-radius: 999px;
}

.ui-badge--dot { width: 8px; height: 8px; padding: 0; border-radius: 50%; }

.ui-badge--sm { min-width: 16px; height: 16px; padding: 0 4px; font-size: 10px; }
.ui-badge--md { min-width: 20px; height: 20px; padding: 0 6px; font-size: 11px; }
.ui-badge--lg { min-width: 24px; height: 24px; padding: 0 8px; font-size: 12px; }

.ui-badge--default { background: var(--color-surface-hover); color: var(--color-text-secondary); }
.ui-badge--primary { background: var(--color-primary); color: var(--color-on-primary); }
.ui-badge--success { background: var(--color-success); color: var(--color-on-success); }
.ui-badge--warning { background: var(--color-warning); color: var(--color-on-warning); }
.ui-badge--danger  { background: var(--color-danger); color: var(--color-on-danger); }
```

```js
// Exemplos
new UIBadge({ value: 3, variant: 'danger' });       // notificações
new UIBadge({ value: 150, max: 99 });                // "99+"
new UIBadge({ dot: true, variant: 'success' });      // online/offline
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial |
