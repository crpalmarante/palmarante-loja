# FiscalUI Framework

## Documento 044 — Toolbar

**Nível 3 — Navegação**

**Versão 1.0**

Barra de ações horizontal, agrupa botões e controles em uma linha compacta. Usada em editores, grids e formulários.

---

```js
class UIToolbar extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.items = options.items || [];    // { type, icon, label, disabled, action, divider }
        this.size = options.size || 'md';    // sm, md
    }

    template() {
        return `
            <div class="ui-toolbar ui-toolbar--${this.size}" role="toolbar">
                ${this.items.map(item => this._renderItem(item)).join('')}
            </div>
        `;
    }

    _renderItem(item) {
        if (item.divider) return '<span class="ui-toolbar__divider"></span>';
        return `
            <button class="ui-toolbar__btn ${item.active ? 'ui-toolbar__btn--active' : ''} ${item.disabled ? 'ui-toolbar__btn--disabled' : ''}"
                    title="${item.label}" ${item.disabled ? 'disabled' : ''} aria-label="${item.label}">
                ${item.icon ? FiscalUI.icons.render(item.icon, { size: this.size === 'sm' ? 16 : 18 }) : ''}
                ${item.label && item.labelOnly ? `<span>${item.label}</span>` : ''}
            </button>
        `;
    }

    onInit() {
        this.queryAll('.ui-toolbar__btn').forEach((btn, i) => {
            const item = this.items[i];
            if (item && !item.disabled) {
                btn.addEventListener('click', () => {
                    this.emit('toolbar:action', { action: item.action, index: i });
                    item.action?.();
                });
            }
        });
    }
}
```

```css
.ui-toolbar {
    display: flex;
    align-items: center;
    gap: 2px;
    padding: var(--spacing-xs);
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
}

.ui-toolbar--sm .ui-toolbar__btn { padding: 4px; }
.ui-toolbar__btn {
    display: flex; align-items: center; justify-content: center;
    padding: var(--spacing-xs);
    border: none; background: transparent; cursor: pointer;
    color: var(--color-text-secondary);
    border-radius: var(--radius-sm);
    transition: background var(--motion-fast), color var(--motion-fast);
}
.ui-toolbar__btn:hover { background: var(--color-surface-hover); color: var(--color-text); }
.ui-toolbar__btn--active { background: var(--color-primary-surface); color: var(--color-primary); }
.ui-toolbar__btn--disabled { opacity: 0.4; cursor: not-allowed; }
.ui-toolbar__divider { width: 1px; height: 20px; background: var(--color-border); margin: 0 var(--spacing-xs); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
