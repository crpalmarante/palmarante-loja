# FiscalUI Framework

## Documento 109 — Workspace

**Nível 6 — Layouts**

**Versão 1.0**

Workspace multi-abas estilo IDE. Gerencia abas abertas, área de conteúdo central e painéis auxiliares.

---

```js
class WorkspaceLayout extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.tabs = options.tabs || [];
        this._activeTab = options.activeTab || (this.tabs[0]?.id || null);
    }

    template() {
        return `
            <div class="ui-layout-workspace">
                <div class="ui-layout-workspace__tabs">
                    <div class="ui-layout-workspace__tab-list">
                        ${this.tabs.map(tab => `
                            <div class="ui-layout-workspace__tab ${tab.id === this._activeTab ? 'ui-layout-workspace__tab--active' : ''}"
                                 data-tab="${tab.id}">
                                ${tab.icon ? `<span class="ui-layout-workspace__tab-icon">${FiscalUI.icons.render(tab.icon, { size: 14 })}</span>` : ''}
                                <span class="ui-layout-workspace__tab-label">${tab.label}</span>
                                <button class="ui-layout-workspace__tab-close" data-tab="${tab.id}">&times;</button>
                            </div>
                        `).join('')}
                    </div>
                    <div class="ui-layout-workspace__tab-actions">
                        <button class="ui-layout-workspace__new-tab" aria-label="Nova aba">+</button>
                    </div>
                </div>
                <div class="ui-layout-workspace__content">
                    ${this.tabs.map(tab => `
                        <div class="ui-layout-workspace__panel ${tab.id === this._activeTab ? 'ui-layout-workspace__panel--active' : ''}"
                             data-panel="${tab.id}">${tab.content || ''}</div>
                    `).join('')}
                </div>
                <div class="ui-layout-workspace__statusbar">
                    <span class="ui-layout-workspace__status-left"></span>
                    <span class="ui-layout-workspace__status-right"></span>
                </div>
            </div>
        `;
    }

    onInit() {
        this._tabList = this.query('.ui-layout-workspace__tab-list');
        this._content = this.query('.ui-layout-workspace__content');

        this.queryAll('.ui-layout-workspace__tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                if (e.target.closest('.ui-layout-workspace__tab-close')) return;
                this.activate(tab.dataset.tab);
            });
        });

        this.queryAll('.ui-layout-workspace__tab-close').forEach(btn => {
            btn.addEventListener('click', (e) => { e.stopPropagation(); this.closeTab(btn.dataset.tab); });
        });

        this.query('.ui-layout-workspace__new-tab')?.addEventListener('click', () => this.emit('workspace:new-tab'));
    }

    activate(tabId) {
        if (!tabId || this._activeTab === tabId) return;
        this._activeTab = tabId;
        this.queryAll('.ui-layout-workspace__tab').forEach(t => t.classList.toggle('ui-layout-workspace__tab--active', t.dataset.tab === tabId));
        this.queryAll('.ui-layout-workspace__panel').forEach(p => p.classList.toggle('ui-layout-workspace__panel--active', p.dataset.panel === tabId));
        this.emit('workspace:activate', { tab: tabId });
    }

    openTab(tab) {
        this.tabs.push(tab);
        this.render();
        this.activate(tab.id);
    }

    closeTab(tabId) {
        const idx = this.tabs.findIndex(t => t.id === tabId);
        if (idx === -1) return;
        this.tabs.splice(idx, 1);
        if (this._activeTab === tabId) {
            const nextTab = this.tabs[Math.min(idx, this.tabs.length - 1)];
            this._activeTab = nextTab?.id || null;
        }
        this.render();
        if (this._activeTab) this.activate(this._activeTab);
        this.emit('workspace:close', { tab: tabId });
    }

    setStatusLeft(text) { this.query('.ui-layout-workspace__status-left').textContent = text; }
    setStatusRight(text) { this.query('.ui-layout-workspace__status-right').textContent = text; }
}
```

```css
.ui-layout-workspace { display: flex; flex-direction: column; height: 100%; }

.ui-layout-workspace__tabs { display: flex; background: var(--color-surface-hover); border-bottom: 1px solid var(--color-border); flex-shrink: 0; }
.ui-layout-workspace__tab-list { display: flex; flex: 1; overflow-x: auto; }
.ui-layout-workspace__tab { display: flex; align-items: center; gap: var(--spacing-xs); padding: var(--spacing-sm) var(--spacing-md); cursor: pointer; border-right: 1px solid var(--color-border); font-size: var(--font-size-sm); white-space: nowrap; background: var(--color-surface-hover); min-width: 0; }
.ui-layout-workspace__tab--active { background: var(--color-surface); border-bottom: 2px solid var(--color-primary); margin-bottom: -1px; }
.ui-layout-workspace__tab-icon { color: var(--color-text-muted); }
.ui-layout-workspace__tab-label { overflow: hidden; text-overflow: ellipsis; }
.ui-layout-workspace__tab-close { border: none; background: transparent; cursor: pointer; color: var(--color-text-muted); font-size: 14px; line-height: 1; padding: 0 2px; border-radius: 2px; }
.ui-layout-workspace__tab-close:hover { background: var(--color-surface-hover); color: var(--color-text); }
.ui-layout-workspace__new-tab { border: none; background: transparent; cursor: pointer; padding: 0 var(--spacing-md); font-size: 18px; color: var(--color-text-muted); }

.ui-layout-workspace__content { flex: 1; overflow: hidden; position: relative; }
.ui-layout-workspace__panel { display: none; height: 100%; overflow: auto; }
.ui-layout-workspace__panel--active { display: block; }

.ui-layout-workspace__statusbar { display: flex; justify-content: space-between; padding: 2px var(--spacing-md); background: var(--color-primary); color: #fff; font-size: var(--font-size-xs); flex-shrink: 0; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
