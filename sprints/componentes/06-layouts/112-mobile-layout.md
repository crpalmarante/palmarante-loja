# FiscalUI Framework

## Documento 112 — Mobile Layout

**Nível 6 — Layouts**

**Versão 1.0**

Layout responsivo para dispositivos móveis. Bottom navigation, header compacto, conteúdo scrollável.

---

```js
class MobileLayout extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.title = options.title || '';
        this.content = options.content || '';
        this.tabs = options.tabs || [];
        this._activeTab = options.activeTab || (this.tabs[0]?.id || null);
        this.showBack = options.showBack || false;
    }

    template() {
        return `
            <div class="ui-layout-mobile">
                <header class="ui-layout-mobile__header">
                    ${this.showBack ? `<button class="ui-layout-mobile__back" aria-label="Voltar">${FiscalUI.icons.render('chevron-left', { size: 20 })}</button>` : ''}
                    <h1 class="ui-layout-mobile__title">${this.title}</h1>
                    <div class="ui-layout-mobile__actions"></div>
                </header>
                <main class="ui-layout-mobile__content">
                    ${this.tabs.length ? this.tabs.map(t => `
                        <div class="ui-layout-mobile__page ${t.id === this._activeTab ? 'ui-layout-mobile__page--active' : ''}" data-page="${t.id}">${t.content || ''}</div>
                    `).join('') : this.content}
                </main>
                ${this.tabs.length ? `
                <nav class="ui-layout-mobile__bottom-nav">
                    ${this.tabs.map(t => `
                        <button class="ui-layout-mobile__nav-item ${t.id === this._activeTab ? 'ui-layout-mobile__nav-item--active' : ''}" data-tab="${t.id}">
                            <span class="ui-layout-mobile__nav-icon">${FiscalUI.icons.render(t.icon || 'circle', { size: 20 })}</span>
                            <span class="ui-layout-mobile__nav-label">${t.label}</span>
                        </button>
                    `).join('')}
                </nav>` : ''}
            </div>
        `;
    }

    onInit() {
        this._content = this.query('.ui-layout-mobile__content');
        this._actions = this.query('.ui-layout-mobile__actions');

        this.query('.ui-layout-mobile__back')?.addEventListener('click', () => this.emit('mobile:back'));

        this.queryAll('.ui-layout-mobile__nav-item').forEach(item => {
            item.addEventListener('click', () => {
                this._activeTab = item.dataset.tab;
                this.queryAll('.ui-layout-mobile__nav-item').forEach(n => n.classList.remove('ui-layout-mobile__nav-item--active'));
                item.classList.add('ui-layout-mobile__nav-item--active');
                this.queryAll('.ui-layout-mobile__page').forEach(p => p.classList.toggle('ui-layout-mobile__page--active', p.dataset.page === this._activeTab));
                this.emit('mobile:tab', { tab: this._activeTab });
            });
        });
    }

    setContent(html) { if (this._content) this._content.innerHTML = html; }
    setActions(html) { if (this._actions) this._actions.innerHTML = html; }
    setTitle(title) { this.title = title; this.query('.ui-layout-mobile__title').textContent = title; }
}
```

```css
.ui-layout-mobile { display: flex; flex-direction: column; height: 100vh; max-width: 480px; margin: 0 auto; background: var(--color-surface); }

.ui-layout-mobile__header { display: flex; align-items: center; gap: var(--spacing-sm); padding: var(--spacing-sm) var(--spacing-md); border-bottom: 1px solid var(--color-border); min-height: 48px; }
.ui-layout-mobile__back { border: none; background: transparent; cursor: pointer; color: var(--color-text); padding: 4px; display: flex; }
.ui-layout-mobile__title { flex: 1; font-size: var(--font-size-lg); font-weight: var(--font-weight-semibold); margin: 0; }
.ui-layout-mobile__actions { display: flex; gap: var(--spacing-xs); }

.ui-layout-mobile__content { flex: 1; overflow-y: auto; -webkit-overflow-scrolling: touch; }
.ui-layout-mobile__page { display: none; padding: var(--spacing-md); }
.ui-layout-mobile__page--active { display: block; }

.ui-layout-mobile__bottom-nav { display: flex; border-top: 1px solid var(--color-border); background: var(--color-surface); flex-shrink: 0; }
.ui-layout-mobile__nav-item { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 2px; padding: var(--spacing-xs) 0; border: none; background: transparent; cursor: pointer; color: var(--color-text-muted); font-size: 10px; }
.ui-layout-mobile__nav-item--active { color: var(--color-primary); }
.ui-layout-mobile__nav-icon { display: flex; }
.ui-layout-mobile__nav-label { line-height: 1; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
