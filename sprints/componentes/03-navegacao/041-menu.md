# FiscalUI Framework

## Documento 041 — Menu

**Nível 3 — Navegação**

**Versão 1.0**

Lista vertical de itens clicáveis. Suporta ícones, atalhos de teclado, submenus e estados ativo/desabilitado.

---

```js
class UIMenu extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.items = options.items || [];
        this.compact = options.compact || false;
        this._activeIndex = -1;
    }

    template() {
        return `<nav class="ui-menu ${this.compact ? 'ui-menu--compact' : ''}" role="menu">
            ${this.items.map((item, i) => this._renderItem(item, i)).join('')}
        </nav>`;
    }

    _renderItem(item, index) {
        return `
            <div class="ui-menu__item ${item.active ? 'ui-menu__item--active' : ''}
                        ${item.disabled ? 'ui-menu__item--disabled' : ''}
                        ${item.children ? 'ui-menu__item--parent' : ''}"
                 role="menuitem" tabindex="${item.disabled ? -1 : 0}" data-index="${index}">
                ${item.icon ? `<span class="ui-menu__icon">${FiscalUI.icons.render(item.icon, { size: 18 })}</span>` : ''}
                <span class="ui-menu__label">${item.label}</span>
                ${item.shortcut ? `<kbd class="ui-menu__shortcut">${item.shortcut}</kbd>` : ''}
                ${item.children ? `<span class="ui-menu__arrow">${FiscalUI.icons.render('chevron-right', { size: 14 })}</span>` : ''}
                ${item.badge ? `<span class="ui-badge ui-badge--${item.badge.variant || 'primary'} ui-badge--sm">${item.badge.text}</span>` : ''}
            </div>
            ${item.children ? `<div class="ui-menu__submenu">${item.children.map((child, j) => this._renderItem(child, `${index}-${j}`)).join('')}</div>` : ''}
        `;
    }

    onInit() {
        this._items = this.queryAll('.ui-menu__item');
        this._items.forEach(el => {
            el.addEventListener('click', () => this._onClick(el));
            el.addEventListener('keydown', (e) => this._onKeydown(e, el));
            if (el.classList.contains('ui-menu__item--parent')) {
                el.addEventListener('mouseenter', () => this._openSubmenu(el));
                el.addEventListener('mouseleave', () => this._closeSubmenu(el));
            }
        });
    }

    _onClick(el) {
        if (el.classList.contains('ui-menu__item--disabled') || el.classList.contains('ui-menu__item--parent')) return;
        this._activate(el);
        this.emit('menu:select', { item: el.dataset.index });
    }

    _activate(el) {
        this._items.forEach(i => i.classList.remove('ui-menu__item--active'));
        el.classList.add('ui-menu__item--active');
        this._activeIndex = parseInt(el.dataset.index);
    }

    _openSubmenu(el) { el.nextElementSibling?.classList.add('ui-menu__submenu--open'); }
    _closeSubmenu(el) { el.nextElementSibling?.classList.remove('ui-menu__submenu--open'); }

    _onKeydown(e, el) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); this._onClick(el); }
        if (e.key === 'ArrowDown') { e.preventDefault(); this._focusNext(1); }
        if (e.key === 'ArrowUp') { e.preventDefault(); this._focusNext(-1); }
    }

    _focusNext(dir) {
        const idx = this._activeIndex + dir;
        if (idx >= 0 && idx < this._items.length) {
            this._items[idx].focus();
            this._activate(this._items[idx]);
        }
    }
}
```

```css
.ui-menu {
    display: flex;
    flex-direction: column;
    gap: 2px;
    padding: var(--spacing-xs);
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    min-width: 200px;
}

.ui-menu--compact .ui-menu__item { padding: var(--spacing-xs) var(--spacing-sm); font-size: var(--font-size-sm); }

.ui-menu__item {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--radius-sm);
    cursor: pointer;
    color: var(--color-text);
    font-size: var(--font-size-md);
    transition: background var(--motion-fast);
    position: relative;
}

.ui-menu__item:hover { background: var(--color-surface-hover); }
.ui-menu__item--active { background: var(--color-primary-surface); color: var(--color-primary); }
.ui-menu__item--disabled { opacity: 0.4; cursor: not-allowed; }
.ui-menu__item--parent { position: relative; }

.ui-menu__icon { flex-shrink: 0; color: var(--color-text-secondary); }
.ui-menu__label { flex: 1; }
.ui-menu__shortcut { font-size: var(--font-size-xs); color: var(--color-text-muted); font-family: inherit; padding: 1px 4px; background: var(--color-surface-hover); border-radius: 2px; }
.ui-menu__arrow { color: var(--color-text-muted); }

.ui-menu__submenu { display: none; position: absolute; left: 100%; top: 0; }
.ui-menu__submenu--open { display: block; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
