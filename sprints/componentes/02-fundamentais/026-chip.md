# FiscalUI Framework

## Documento 026 — Chip

**Nível 2 — Basic Components**

**Versão 1.0**

Tag compacta com remoção. Usado para filtros ativos, seleções múltiplas, atributos.

---

```js
class UIChip extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.label = options.label || '';
        this.icon = options.icon || null;
        this.variant = options.variant || 'default';
        this.removable = options.removable || false;
        this.onRemove = options.onRemove || null;
        this.onClick = options.onClick || null;
    }

    template() {
        return `
            <span class="ui-chip ui-chip--${this.variant}">
                ${this.icon ? FiscalUI.icons.render(this.icon, { size: 14 }) : ''}
                <span class="ui-chip__label">${this.label}</span>
                ${this.removable ? `<button class="ui-chip__remove" aria-label="Remover ${this.label}">
                    ${FiscalUI.icons.render('close', { size: 12 })}</button>` : ''}
            </span>
        `;
    }

    onInit() {
        const removeBtn = this.query('.ui-chip__remove');
        removeBtn?.addEventListener('click', (e) => {
            e.stopPropagation();
            this.emit('chip:remove', { label: this.label });
            this.onRemove?.();
            this.destroy();
        });
        this.element.addEventListener('click', () => this.onClick?.());
    }
}
```

```css
.ui-chip {
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-xs);
    padding: 2px var(--spacing-sm);
    border-radius: 999px;
    font-size: var(--font-size-sm);
    border: 1px solid var(--color-border);
    background: var(--color-surface);
    cursor: default;
    user-select: none;
}

.ui-chip--primary { background: var(--color-primary-light); color: var(--color-primary); border-color: var(--color-primary); }
.ui-chip--success { background: var(--color-success-light); color: var(--color-success); }
.ui-chip--warning { background: var(--color-warning-light); color: var(--color-warning); }
.ui-chip--danger  { background: var(--color-danger-light); color: var(--color-danger); }

.ui-chip__remove {
    display: inline-flex;
    border: none;
    background: transparent;
    cursor: pointer;
    padding: 2px;
    border-radius: 50%;
    color: inherit;
    opacity: 0.6;
}
.ui-chip__remove:hover { opacity: 1; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial |
