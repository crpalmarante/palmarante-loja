# FiscalUI Framework

## Documento 024 — Link

**Nível 2 — Basic Components**

**Versão 1.0**

Componente de link estilizado. Segue o tema do sistema, diferentemente do link padrão do navegador.

---

```js
class UILink extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.label = options.label || '';
        this.href = options.href || '#';
        this.icon = options.icon || null;
        this.variant = options.variant || 'default';  // default, subtle, muted
        this.size = options.size || 'md';
        this.external = options.external || false;
        this.onClick = options.onClick || null;
    }

    template() {
        const attrs = `href="${this.href}" ${this.external ? 'target="_blank" rel="noopener"' : ''}`;
        return `
            <a class="ui-link ui-link--${this.variant} ui-link--${this.size}"
               ${attrs}>
                ${this.icon ? FiscalUI.icons.render(this.icon, { size: 14 }) : ''}
                ${this.label}
            </a>
        `;
    }

    onInit() {
        this.element.addEventListener('click', (e) => {
            this.emit('link:click', { href: this.href, originalEvent: e });
            this.onClick?.(e);
        });
    }
}
```

```css
.ui-link {
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-xs);
    color: var(--color-primary);
    text-decoration: none;
    cursor: pointer;
    border-radius: var(--radius-sm);
}

.ui-link:hover { text-decoration: underline; color: var(--color-primary-hover); }
.ui-link:focus-visible { outline: 2px solid var(--color-primary); outline-offset: 2px; }

.ui-link--subtle { color: var(--color-text-secondary); }
.ui-link--muted { color: var(--color-text-muted); }

.ui-link--sm { font-size: var(--font-size-sm); }
.ui-link--md { font-size: var(--font-size-md); }
.ui-link--lg { font-size: var(--font-size-lg); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial |
