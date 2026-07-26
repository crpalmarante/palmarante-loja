# FiscalUI Framework

## Documento 042 — Sidebar

**Nível 3 — Navegação**

**Versão 1.0**

Painel lateral persistente com logo, menu de navegação e footer. Pode ser recolhido (ícones apenas) ou expandido.

---

```js
class UISidebar extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.collapsed = options.collapsed || false;
        this.logo = options.logo || '';
        this.title = options.title || '';
        this.menuItems = options.menuItems || [];
        this.footerItems = options.footerItems || [];
        this.width = options.width || 260;
        this.collapsedWidth = options.collapsedWidth || 60;
    }

    template() {
        return `
            <aside class="ui-sidebar ${this.collapsed ? 'ui-sidebar--collapsed' : ''}"
                   style="--sidebar-width: ${this.width}px; --sidebar-collapsed-width: ${this.collapsedWidth}px">
                <div class="ui-sidebar__header">
                    <div class="ui-sidebar__brand">
                        ${this.logo ? `<img class="ui-sidebar__logo" src="${this.logo}" alt="${this.title}">` : ''}
                        <span class="ui-sidebar__title">${this.title}</span>
                    </div>
                    <button class="ui-sidebar__toggle" aria-label="Alternar sidebar">
                        ${FiscalUI.icons.render('chevron-left', { size: 16 })}
                    </button>
                </div>
                <nav class="ui-sidebar__nav">
                    ${this.menuItems.map(item => this._renderItem(item)).join('')}
                </nav>
                <div class="ui-sidebar__footer">
                    ${this.footerItems.map(item => this._renderItem(item)).join('')}
                </div>
            </aside>
        `;
    }

    _renderItem(item) {
        return `
            <a class="ui-sidebar__item ${item.active ? 'ui-sidebar__item--active' : ''} ${item.disabled ? 'ui-sidebar__item--disabled' : ''}"
               href="${item.href || '#'}" role="menuitem" ${item.disabled ? 'aria-disabled="true"' : ''}>
                <span class="ui-sidebar__item-icon">${FiscalUI.icons.render(item.icon, { size: 20 })}</span>
                <span class="ui-sidebar__item-label">${item.label}</span>
                ${item.badge ? `<span class="ui-badge ui-badge--sm ui-badge--${item.badge.variant || 'primary'}">${item.badge.text}</span>` : ''}
            </a>
        `;
    }

    onInit() {
        this._toggleBtn = this.query('.ui-sidebar__toggle');
        this._toggleBtn.addEventListener('click', () => this.toggle());

        this._items = this.queryAll('.ui-sidebar__item');
        this._items.forEach(el => {
            el.addEventListener('click', (e) => {
                if (el.classList.contains('ui-sidebar__item--disabled')) { e.preventDefault(); return; }
                this._activate(el);
                this.emit('sidebar:select', { href: el.getAttribute('href'), label: el.querySelector('.ui-sidebar__item-label')?.textContent });
            });
        });
    }

    toggle() {
        this.collapsed = !this.collapsed;
        this.element.classList.toggle('ui-sidebar--collapsed', this.collapsed);
        this.emit('sidebar:toggle', { collapsed: this.collapsed });
    }

    _activate(el) {
        this._items.forEach(i => i.classList.remove('ui-sidebar__item--active'));
        el.classList.add('ui-sidebar__item--active');
    }

    expand() { if (this.collapsed) this.toggle(); }
    collapse() { if (!this.collapsed) this.toggle(); }
}
```

```css
.ui-sidebar {
    display: flex;
    flex-direction: column;
    width: var(--sidebar-width);
    height: 100vh;
    background: var(--color-surface);
    border-right: 1px solid var(--color-border);
    transition: width var(--motion-normal) var(--ease-out);
    overflow: hidden;
}

.ui-sidebar--collapsed { width: var(--sidebar-collapsed-width); }

.ui-sidebar__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-md);
    border-bottom: 1px solid var(--color-border);
    min-height: 56px;
}

.ui-sidebar__brand { display: flex; align-items: center; gap: var(--spacing-sm); overflow: hidden; }
.ui-sidebar__logo { height: 28px; width: 28px; flex-shrink: 0; }
.ui-sidebar__title { font-weight: var(--font-weight-semibold); white-space: nowrap; }

.ui-sidebar__toggle {
    border: none; background: transparent; cursor: pointer; color: var(--color-text-secondary);
    flex-shrink: 0; transition: transform var(--motion-fast);
}
.ui-sidebar--collapsed .ui-sidebar__toggle { transform: rotate(180deg); }

.ui-sidebar__nav { flex: 1; overflow-y: auto; padding: var(--spacing-xs); display: flex; flex-direction: column; gap: 2px; }
.ui-sidebar__footer { border-top: 1px solid var(--color-border); padding: var(--spacing-xs); }

.ui-sidebar__item {
    display: flex; align-items: center; gap: var(--spacing-sm);
    padding: var(--spacing-sm) var(--spacing-md); border-radius: var(--radius-sm);
    color: var(--color-text); text-decoration: none; font-size: var(--font-size-md);
    transition: background var(--motion-fast); white-space: nowrap;
}
.ui-sidebar__item:hover { background: var(--color-surface-hover); }
.ui-sidebar__item--active { background: var(--color-primary-surface); color: var(--color-primary); }
.ui-sidebar__item--disabled { opacity: 0.4; pointer-events: none; }

.ui-sidebar__item-icon { flex-shrink: 0; }
.ui-sidebar__item-label { flex: 1; }
.ui-sidebar--collapsed .ui-sidebar__item-label,
.ui-sidebar--collapsed .ui-sidebar__title,
.ui-sidebar--collapsed .ui-badge { display: none; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
