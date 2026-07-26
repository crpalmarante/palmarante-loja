# FiscalUI Framework

## Documento 030 — Panel

**Nível 2 — Basic Components**

**Versão 1.0**

Container colapsável com header, body e footer. Usado para sidebars, painéis de configuração e seções expandíveis.

---

```js
class UIPanel extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.title = options.title || '';
        this.collapsible = options.collapsible || false;
        this.collapsed = options.collapsed || false;
        this.variant = options.variant || 'default';
        this._bodyEl = null;
    }

    template() {
        return `
            <div class="ui-panel ui-panel--${this.variant} ${this.collapsed ? 'ui-panel--collapsed' : ''}">
                <div class="ui-panel__header">
                    <span class="ui-panel__title">${this.title}</span>
                    ${this.collapsible ? `<button class="ui-panel__toggle" aria-label="Expandir/Recolher">
                        ${FiscalUI.icons.render('chevron-down', { size: 16 })}</button>` : ''}
                </div>
                <div class="ui-panel__body" ${this.collapsed ? 'hidden' : ''}></div>
                <div class="ui-panel__footer" hidden></div>
            </div>
        `;
    }

    onInit() {
        this._bodyEl = this.query('.ui-panel__body');
        this._footerEl = this.query('.ui-panel__footer');
        this.query('.ui-panel__toggle')?.addEventListener('click', () => this.toggle());
    }

    setBody(html) { if (this._bodyEl) this._bodyEl.innerHTML = html; }
    appendBody(el) { if (this._bodyEl) this._bodyEl.appendChild(el); }
    setFooter(html) { if (this._footerEl) { this._footerEl.innerHTML = html; this._footerEl.hidden = false; } }

    toggle() {
        this.collapsed = !this.collapsed;
        this.element.classList.toggle('ui-panel--collapsed', this.collapsed);
        if (this._bodyEl) this._bodyEl.hidden = this.collapsed;
        this.emit('panel:toggle', { collapsed: this.collapsed });
    }

    open() { if (this.collapsed) this.toggle(); }
    close() { if (!this.collapsed) this.toggle(); }
}
```

```css
.ui-panel {
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    background: var(--color-surface);
}

.ui-panel__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-md);
    border-bottom: 1px solid var(--color-border);
}

.ui-panel__title { font-size: var(--font-size-md); font-weight: var(--font-weight-semibold); }

.ui-panel__toggle {
    border: none; background: transparent; cursor: pointer;
    color: var(--color-text-secondary);
    transition: transform var(--motion-fast);
}

.ui-panel--collapsed .ui-panel__toggle { transform: rotate(-90deg); }
.ui-panel--collapsed .ui-panel__header { border-bottom: none; }

.ui-panel__body { padding: var(--spacing-md); }
.ui-panel__footer {
    padding: var(--spacing-md);
    border-top: 1px solid var(--color-border);
    display: flex;
    justify-content: flex-end;
    gap: var(--spacing-sm);
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial |
