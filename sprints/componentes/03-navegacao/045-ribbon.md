# FiscalUI Framework

## Documento 045 — Ribbon

**Nível 3 — Navegação**

**Versão 1.0**

Barra de abas estilizada como faixa horizontal, similar ao Ribbon do Microsoft Office. Agrupa comandos em categorias com abas.

---

```js
class UIRibbon extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.tabs = options.tabs || [];     // { id, label, groups: [{ label, items: [{ icon, label, action }] }] }
        this._activeTab = options.activeTab || (this.tabs[0]?.id || null);
    }

    template() {
        return `
            <div class="ui-ribbon">
                <div class="ui-ribbon__tabs">
                    ${this.tabs.map(tab => `
                        <button class="ui-ribbon__tab ${tab.id === this._activeTab ? 'ui-ribbon__tab--active' : ''}"
                                data-tab="${tab.id}">${tab.label}</button>
                    `).join('')}
                </div>
                <div class="ui-ribbon__content">
                    ${this.tabs.map(tab => `
                        <div class="ui-ribbon__panel ${tab.id === this._activeTab ? 'ui-ribbon__panel--active' : ''}" data-panel="${tab.id}">
                            ${tab.groups.map(group => `
                                <div class="ui-ribbon__group">
                                    ${group.label ? `<span class="ui-ribbon__group-label">${group.label}</span>` : ''}
                                    <div class="ui-ribbon__items">
                                        ${group.items.map(item => `
                                            <button class="ui-ribbon__item" title="${item.label}">
                                                ${FiscalUI.icons.render(item.icon, { size: 20 })}
                                                <span>${item.label}</span>
                                            </button>
                                        `).join('')}
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    onInit() {
        this.queryAll('.ui-ribbon__tab').forEach(tab => {
            tab.addEventListener('click', () => this._activate(tab.dataset.tab));
        });
        this.queryAll('.ui-ribbon__item').forEach(item => {
            item.addEventListener('click', () => this.emit('ribbon:action', { label: item.textContent.trim() }));
        });
    }

    _activate(tabId) {
        this._activeTab = tabId;
        this.queryAll('.ui-ribbon__tab').forEach(t => t.classList.toggle('ui-ribbon__tab--active', t.dataset.tab === tabId));
        this.queryAll('.ui-ribbon__panel').forEach(p => p.classList.toggle('ui-ribbon__panel--active', p.dataset.panel === tabId));
        this.emit('ribbon:tab', { tab: tabId });
    }
}
```

```css
.ui-ribbon {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    overflow: hidden;
}

.ui-ribbon__tabs {
    display: flex;
    background: var(--color-surface-hover);
    border-bottom: 1px solid var(--color-border);
    padding: 0 var(--spacing-sm);
}

.ui-ribbon__tab {
    padding: var(--spacing-xs) var(--spacing-md);
    border: none; background: transparent; cursor: pointer;
    font-size: var(--font-size-sm);
    color: var(--color-text-secondary);
    border-bottom: 2px solid transparent;
    margin-bottom: -1px;
    transition: color var(--motion-fast), border-color var(--motion-fast);
}
.ui-ribbon__tab:hover { color: var(--color-text); }
.ui-ribbon__tab--active { color: var(--color-primary); border-bottom-color: var(--color-primary); }

.ui-ribbon__panel { display: none; padding: var(--spacing-sm); gap: var(--spacing-sm); }
.ui-ribbon__panel--active { display: flex; }

.ui-ribbon__group { display: flex; flex-direction: column; align-items: center; gap: var(--spacing-xs); padding: 0 var(--spacing-sm); border-right: 1px solid var(--color-border); }
.ui-ribbon__group:last-child { border-right: none; }
.ui-ribbon__group-label { font-size: var(--font-size-xs); color: var(--color-text-muted); }
.ui-ribbon__items { display: flex; gap: 2px; }

.ui-ribbon__item {
    display: flex; flex-direction: column; align-items: center; gap: 2px;
    padding: var(--spacing-xs); border: none; background: transparent; cursor: pointer;
    border-radius: var(--radius-sm); color: var(--color-text-secondary);
    font-size: 10px; transition: background var(--motion-fast);
}
.ui-ribbon__item:hover { background: var(--color-surface-hover); color: var(--color-text); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
