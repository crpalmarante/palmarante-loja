# FiscalUI Framework

## Documento 105 — Dashboard Layout

**Nível 6 — Layouts**

**Versão 1.0**

Layout completo de dashboard com sidebar, navbar, área de conteúdo e toolbar de ações.

---

```js
class DashboardLayout extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.title = options.title || 'Dashboard';
        this.sidebar = options.sidebar || '';
        this.navbar = options.navbar || '';
        this.content = options.content || '';
        this.footer = options.footer || '';
    }

    template() {
        return `
            <div class="ui-layout-dash">
                <div class="ui-layout-dash__sidebar">${this.sidebar}</div>
                <div class="ui-layout-dash__main">
                    <div class="ui-layout-dash__navbar">${this.navbar}</div>
                    <div class="ui-layout-dash__toolbar">
                        <h2 class="ui-layout-dash__title">${this.title}</h2>
                        <div class="ui-layout-dash__actions"></div>
                    </div>
                    <main class="ui-layout-dash__content">${this.content}</main>
                    ${this.footer ? `<footer class="ui-layout-dash__footer">${this.footer}</footer>` : ''}
                </div>
            </div>
        `;
    }

    onInit() {
        this._content = this.query('.ui-layout-dash__content');
        this._actions = this.query('.ui-layout-dash__actions');
    }

    setContent(html) { if (this._content) this._content.innerHTML = html; }
    setActions(html) { if (this._actions) this._actions.innerHTML = html; }
    setTitle(title) { this.title = title; this.query('.ui-layout-dash__title').textContent = title; }
}
```

```css
.ui-layout-dash { display: flex; height: 100vh; overflow: hidden; }
.ui-layout-dash__sidebar { width: 260px; flex-shrink: 0; border-right: 1px solid var(--color-border); overflow-y: auto; }
.ui-layout-dash__main { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
.ui-layout-dash__navbar { flex-shrink: 0; }
.ui-layout-dash__toolbar { display: flex; align-items: center; justify-content: space-between; padding: var(--spacing-md) var(--spacing-lg); border-bottom: 1px solid var(--color-border); }
.ui-layout-dash__title { font-size: var(--font-size-xl); margin: 0; font-weight: var(--font-weight-semibold); }
.ui-layout-dash__actions { display: flex; gap: var(--spacing-sm); }
.ui-layout-dash__content { flex: 1; overflow-y: auto; padding: var(--spacing-lg); }
.ui-layout-dash__footer { padding: var(--spacing-md) var(--spacing-lg); border-top: 1px solid var(--color-border); font-size: var(--font-size-xs); color: var(--color-text-muted); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
