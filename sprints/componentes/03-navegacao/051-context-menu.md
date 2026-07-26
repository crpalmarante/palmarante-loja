# FiscalUI Framework

## Documento 051 — Context Menu

**Nível 3 — Navegação**

**Versão 1.0**

Menu de contexto exibido ao clique com botão direito. Posicionado no cursor, com submenus e atalhos.

---

```js
class UIContextMenu extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.items = options.items || [];        // mesma estrutura do Menu
        this._target = options.target || null;
        this._open = false;
    }

    init(target) {
        if (target) this._target = target;
        this._menu = document.createElement('nav');
        this._menu.className = 'ui-context-menu';
        this._menu.innerHTML = this.items.map((item, i) => this._renderItem(item, i)).join('');
        this._menu.hidden = true;
        document.body.appendChild(this._menu);

        this._target?.addEventListener('contextmenu', (e) => this.show(e));
        document.addEventListener('click', () => this.hide());
        document.addEventListener('contextmenu', (e) => { if (!this._menu.contains(e.target)) this.hide(); });
        document.addEventListener('keydown', (e) => { if (e.key === 'Escape') this.hide(); });

        this._menu.addEventListener('click', (e) => {
            const item = e.target.closest('.ui-context-menu__item');
            if (!item || item.classList.contains('ui-context-menu__item--disabled') || item.classList.contains('ui-context-menu__item--parent')) return;
            this.hide();
            const index = item.dataset.index;
            const action = this._findAction(index);
            action?.();
            this.emit('contextmenu:select', { index });
        });
    }

    show(e) {
        e.preventDefault();
        this._menu.hidden = false;
        const x = Math.min(e.clientX, window.innerWidth - this._menu.offsetWidth);
        const y = Math.min(e.clientY, window.innerHeight - this._menu.offsetHeight);
        this._menu.style.left = `${x}px`;
        this._menu.style.top = `${y}px`;
        this._open = true;
    }

    hide() { if (this._open) { this._menu.hidden = true; this._open = false; } }

    _renderItem(item, index) {
        if (item.divider) return '<hr class="ui-context-menu__divider">';
        return `
            <div class="ui-context-menu__item ${item.disabled ? 'ui-context-menu__item--disabled' : ''}
                        ${item.children ? 'ui-context-menu__item--parent' : ''}"
                 data-index="${index}">
                ${item.icon ? `<span class="ui-context-menu__icon">${FiscalUI.icons.render(item.icon, { size: 16 })}</span>` : ''}
                <span class="ui-context-menu__label">${item.label}</span>
                ${item.shortcut ? `<kbd class="ui-context-menu__shortcut">${item.shortcut}</kbd>` : ''}
                ${item.children ? `<span class="ui-context-menu__arrow">${FiscalUI.icons.render('chevron-right', { size: 14 })}</span>` : ''}
            </div>
            ${item.children ? `<div class="ui-context-menu__submenu">${item.children.map((c, j) => this._renderItem(c, `${index}-${j}`)).join('')}</div>` : ''}
        `;
    }

    _findAction(index) {
        const parts = String(index).split('-').map(Number);
        let item = this.items[parts[0]];
        for (let i = 1; i < parts.length; i++) item = item?.children?.[parts[i]];
        return item?.action;
    }

    destroy() { this._menu?.remove(); super.destroy(); }
}
```

```css
.ui-context-menu {
    position: fixed;
    z-index: var(--z-popover);
    min-width: 180px;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-lg);
    padding: var(--spacing-xs);
}

.ui-context-menu__item {
    display: flex; align-items: center; gap: var(--spacing-sm);
    padding: var(--spacing-xs) var(--spacing-md);
    border-radius: var(--radius-sm);
    cursor: pointer; font-size: var(--font-size-sm);
    color: var(--color-text); transition: background var(--motion-fast);
    position: relative;
}
.ui-context-menu__item:hover { background: var(--color-surface-hover); }
.ui-context-menu__item--disabled { opacity: 0.4; cursor: not-allowed; }
.ui-context-menu__item--parent { position: relative; }

.ui-context-menu__icon { flex-shrink: 0; color: var(--color-text-secondary); }
.ui-context-menu__label { flex: 1; }
.ui-context-menu__shortcut { font-size: 11px; color: var(--color-text-muted); }
.ui-context-menu__arrow { color: var(--color-text-muted); }
.ui-context-menu__divider { border: none; border-top: 1px solid var(--color-border); margin: var(--spacing-xs) 0; }

.ui-context-menu__submenu { display: none; position: absolute; left: 100%; top: -4px; }
.ui-context-menu__item--parent:hover > .ui-context-menu__submenu { display: block; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
