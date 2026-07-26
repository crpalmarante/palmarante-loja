# FiscalUI Framework

## Documento 047 — Tabs

**Nível 3 — Navegação**

**Versão 1.0**

Navegação por abas. Suporta variantes underline, pills e cards. Pode ser scrollável ou com overflow dropdown.

---

```js
class UITabs extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.tabs = options.tabs || [];          // { id, label, icon, badge, disabled }
        this.variant = options.variant || 'underline'; // underline, pills, cards
        this._activeTab = options.activeTab || (this.tabs[0]?.id || null);
    }

    template() {
        return `
            <div class="ui-tabs ui-tabs--${this.variant}">
                <div class="ui-tabs__bar" role="tablist">
                    ${this.tabs.map(tab => `
                        <button class="ui-tabs__tab ${tab.id === this._activeTab ? 'ui-tabs__tab--active' : ''}
                                    ${tab.disabled ? 'ui-tabs__tab--disabled' : ''}"
                                role="tab" data-tab="${tab.id}" ${tab.disabled ? 'disabled' : ''}
                                aria-selected="${tab.id === this._activeTab}">
                            ${tab.icon ? `<span class="ui-tabs__tab-icon">${FiscalUI.icons.render(tab.icon, { size: 16 })}</span>` : ''}
                            <span>${tab.label}</span>
                            ${tab.badge ? `<span class="ui-badge ui-badge--sm ui-badge--${tab.badge.variant || 'primary'}">${tab.badge.text}</span>` : ''}
                        </button>
                    `).join('')}
                </div>
                <div class="ui-tabs__panels">
                    ${this.tabs.map(tab => `
                        <div class="ui-tabs__panel ${tab.id === this._activeTab ? 'ui-tabs__panel--active' : ''}"
                             role="tabpanel" data-panel="${tab.id}"></div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    onInit() {
        this.queryAll('.ui-tabs__tab').forEach(tab => {
            tab.addEventListener('click', () => this.activate(tab.dataset.tab));
        });
    }

    activate(tabId) {
        if (this._activeTab === tabId) return;
        this._activeTab = tabId;
        this.queryAll('.ui-tabs__tab').forEach(t => {
            const active = t.dataset.tab === tabId;
            t.classList.toggle('ui-tabs__tab--active', active);
            t.setAttribute('aria-selected', active);
        });
        this.queryAll('.ui-tabs__panel').forEach(p => p.classList.toggle('ui-tabs__panel--active', p.dataset.panel === tabId));
        this.emit('tabs:change', { tab: tabId });
    }

    getPanel(tabId) { return this.query(`.ui-tabs__panel[data-panel="${tabId}"]`); }
}
```

```css
.ui-tabs__bar {
    display: flex;
    gap: 0;
    border-bottom: 1px solid var(--color-border);
}

.ui-tabs__tab {
    display: flex; align-items: center; gap: var(--spacing-xs);
    padding: var(--spacing-sm) var(--spacing-md);
    border: none; background: transparent; cursor: pointer;
    font-size: var(--font-size-md); color: var(--color-text-secondary);
    white-space: nowrap;
    transition: color var(--motion-fast), border-color var(--motion-fast), background var(--motion-fast);
}
.ui-tabs__tab:hover { color: var(--color-text); }
.ui-tabs__tab--disabled { opacity: 0.4; cursor: not-allowed; }

.ui-tabs--underline .ui-tabs__tab {
    border-bottom: 2px solid transparent;
    margin-bottom: -1px;
}
.ui-tabs--underline .ui-tabs__tab--active { color: var(--color-primary); border-bottom-color: var(--color-primary); }

.ui-tabs--pills .ui-tabs__bar { gap: var(--spacing-xs); border-bottom: none; }
.ui-tabs--pills .ui-tabs__tab { border-radius: var(--radius-md); }
.ui-tabs--pills .ui-tabs__tab--active { background: var(--color-primary); color: #fff; }

.ui-tabs--cards .ui-tabs__bar { gap: 0; }
.ui-tabs--cards .ui-tabs__tab { border: 1px solid transparent; border-bottom-color: var(--color-border); border-radius: var(--radius-md) var(--radius-md) 0 0; }
.ui-tabs--cards .ui-tabs__tab--active { border-color: var(--color-border); border-bottom-color: var(--color-surface); background: var(--color-surface); }

.ui-tabs__panel { display: none; padding: var(--spacing-md); }
.ui-tabs__panel--active { display: block; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
