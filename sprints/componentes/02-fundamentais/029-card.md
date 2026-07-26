# FiscalUI Framework

## Documento 029 — Card

**Nível 2 — Basic Components**

**Versão 1.0**

Container de conteúdo com superfície elevada. Usado para agrupar informações relacionadas em dashboards, listas e formulários.

---

```js
class UICard extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.title = options.title || '';
        this.subtitle = options.subtitle || '';
        this.icon = options.icon || null;
        this.variant = options.variant || 'default';   // default, outlined, flat
        this.padding = options.padding || 'md';
        this.hoverable = options.hoverable || false;
        this.onClick = options.onClick || null;
        this._header = null;
        this._body = null;
        this._footer = null;
    }

    template() {
        return `
            <div class="ui-card ui-card--${this.variant} ui-card--pad-${this.padding}
                        ${this.hoverable ? 'ui-card--hoverable' : ''}
                        ${this.onClick ? 'ui-card--clickable' : ''}"
                 ${this.onClick ? 'role="button" tabindex="0"' : ''}>
                ${this._headerTemplate()}
                <div class="ui-card__body"></div>
                ${this._footer ? '<div class="ui-card__footer"></div>' : ''}
            </div>
        `;
    }

    _headerTemplate() {
        if (!this.title && !this.icon) return '';
        return `
            <div class="ui-card__header">
                ${this.icon ? `<div class="ui-card__icon">${FiscalUI.icons.render(this.icon, { size: 24 })}</div>` : ''}
                <div>
                    <div class="ui-card__title">${this.title}</div>
                    ${this.subtitle ? `<div class="ui-card__subtitle">${this.subtitle}</div>` : ''}
                </div>
            </div>
        `;
    }

    onInit() {
        this._bodyEl = this.query('.ui-card__body');
        if (this.onClick) {
            this.element.addEventListener('click', () => this.onClick());
            this.element.addEventListener('keydown', (e) => { if (e.key === 'Enter') this.onClick(); });
        }
    }

    setBody(html) { if (this._bodyEl) this._bodyEl.innerHTML = html; }
    appendBody(el) { if (this._bodyEl) this._bodyEl.appendChild(el); }
    setFooter(html) { this._footer = html; this.render(); }
}
```

```css
.ui-card {
    background: var(--color-surface);
    border-radius: var(--radius-lg);
    display: flex;
    flex-direction: column;
}

.ui-card--default { box-shadow: var(--shadow-sm); border: 1px solid var(--color-border); }
.ui-card--outlined { border: 1px solid var(--color-border); box-shadow: none; }
.ui-card--flat { border: none; box-shadow: none; background: transparent; }

.ui-card--hoverable:hover { box-shadow: var(--shadow-md); }
.ui-card--clickable { cursor: pointer; }

.ui-card--pad-none { padding: 0; }
.ui-card--pad-sm   { padding: var(--spacing-sm); }
.ui-card--pad-md   { padding: var(--spacing-md); }
.ui-card--pad-lg   { padding: var(--spacing-lg); }

.ui-card__header {
    display: flex;
    align-items: flex-start;
    gap: var(--spacing-md);
    padding-bottom: var(--spacing-md);
    border-bottom: 1px solid var(--color-border);
    margin-bottom: var(--spacing-md);
}

.ui-card__title { font-size: var(--font-size-lg); font-weight: var(--font-weight-semibold); }
.ui-card__subtitle { font-size: var(--font-size-sm); color: var(--color-text-secondary); margin-top: 2px; }
.ui-card__icon { color: var(--color-primary); }

.ui-card__body { flex: 1; }
.ui-card__footer {
    padding-top: var(--spacing-md);
    border-top: 1px solid var(--color-border);
    margin-top: var(--spacing-md);
    display: flex;
    justify-content: flex-end;
    gap: var(--spacing-sm);
}
```

```js
// Exemplos
const card = new UICard({ title: 'Resumo do Mês', subtitle: 'Julho/2026', icon: 'dashboard' });
card.setBody(`<p>Faturamento: R$ 150.000</p><p>NF-e emitidas: 42</p>`);
card.setFooter(`<button class="ui-btn ui-btn--primary">Ver detalhes</button>`);
card.mount('#container');
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial |
