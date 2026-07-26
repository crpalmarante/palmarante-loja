# FiscalUI Framework

## Documento 113 — Tablet Layout

**Nível 6 — Layouts**

**Versão 1.0**

Layout adaptado para tablets com sidebar recolhível e touch-friendly targets.

---

```js
class TabletLayout extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.title = options.title || '';
        this.sidebar = options.sidebar || '';
        this.content = options.content || '';
        this._sidebarOpen = true;
    }

    template() {
        return `
            <div class="ui-layout-tablet ${this._sidebarOpen ? '' : 'ui-layout-tablet--sidebar-closed'}">
                <div class="ui-layout-tablet__sidebar">
                    <div class="ui-layout-tablet__sidebar-header">
                        <button class="ui-layout-tablet__menu-btn" aria-label="Menu">${FiscalUI.icons.render('menu', { size: 24 })}</button>
                        <h2 class="ui-layout-tablet__sidebar-title">${this.title}</h2>
                    </div>
                    <div class="ui-layout-tablet__sidebar-body">${this.sidebar}</div>
                </div>
                <div class="ui-layout-tablet__main">
                    <header class="ui-layout-tablet__topbar">
                        <button class="ui-layout-tablet__toggle-sidebar" aria-label="Alternar sidebar">${FiscalUI.icons.render('sidebar', { size: 20 })}</button>
                        <h1 class="ui-layout-tablet__title">${this.title}</h1>
                        <div class="ui-layout-tablet__actions"></div>
                    </header>
                    <main class="ui-layout-tablet__content">${this.content}</main>
                </div>
            </div>
        `;
    }

    onInit() {
        this._sidebar = this.query('.ui-layout-tablet__sidebar');
        this._content = this.query('.ui-layout-tablet__content');
        this._actions = this.query('.ui-layout-tablet__actions');

        this.query('.ui-layout-tablet__toggle-sidebar')?.addEventListener('click', () => this.toggleSidebar());
        this.query('.ui-layout-tablet__menu-btn')?.addEventListener('click', () => this.toggleSidebar());
    }

    toggleSidebar() {
        this._sidebarOpen = !this._sidebarOpen;
        this.element.classList.toggle('ui-layout-tablet--sidebar-closed', !this._sidebarOpen);
        this.emit('tablet:sidebar-toggle', { open: this._sidebarOpen });
    }

    setContent(html) { if (this._content) this._content.innerHTML = html; }
    setActions(html) { if (this._actions) this._actions.innerHTML = html; }
    setTitle(title) { this.title = title; this.queryAll('.ui-layout-tablet__title, .ui-layout-tablet__sidebar-title').forEach(el => el.textContent = title); }
}
```

```css
.ui-layout-tablet { display: flex; height: 100vh; }

.ui-layout-tablet__sidebar { width: 240px; flex-shrink: 0; border-right: 1px solid var(--color-border); display: flex; flex-direction: column; transition: width var(--motion-normal), transform var(--motion-normal); }
.ui-layout-tablet--sidebar-closed .ui-layout-tablet__sidebar { width: 0; overflow: hidden; border-right: none; }

.ui-layout-tablet__sidebar-header { display: flex; align-items: center; gap: var(--spacing-sm); padding: var(--spacing-md); border-bottom: 1px solid var(--color-border); min-height: 56px; }
.ui-layout-tablet__menu-btn { border: none; background: transparent; cursor: pointer; color: var(--color-text); padding: 4px; display: flex; }
.ui-layout-tablet__sidebar-title { font-size: var(--font-size-md); margin: 0; }
.ui-layout-tablet__sidebar-body { flex: 1; overflow-y: auto; padding: var(--spacing-xs); }

.ui-layout-tablet__main { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
.ui-layout-tablet__topbar { display: flex; align-items: center; gap: var(--spacing-sm); padding: var(--spacing-sm) var(--spacing-md); border-bottom: 1px solid var(--color-border); min-height: 56px; }
.ui-layout-tablet__toggle-sidebar { border: none; background: transparent; cursor: pointer; color: var(--color-text-secondary); padding: 8px; border-radius: var(--radius-sm); display: flex; }
.ui-layout-tablet__toggle-sidebar:hover { background: var(--color-surface-hover); }
.ui-layout-tablet__title { flex: 1; font-size: var(--font-size-lg); margin: 0; font-weight: var(--font-weight-semibold); }
.ui-layout-tablet__actions { display: flex; gap: var(--spacing-sm); }

.ui-layout-tablet__content { flex: 1; overflow-y: auto; padding: var(--spacing-lg); -webkit-overflow-scrolling: touch; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
