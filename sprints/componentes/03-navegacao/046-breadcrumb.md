# FiscalUI Framework

## Documento 046 — Breadcrumb

**Nível 3 — Navegação**

**Versão 1.0**

Trilha de navegação hierárquica. Mostra o caminho atual e permite navegar para níveis ancestrais.

---

```js
class UIBreadcrumb extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.items = options.items || [];   // { label, href }
        this.icon = options.icon || 'home';
        this.maxItems = options.maxItems || 0;  // 0 = ilimitado, > 0 = colapsa com "..."
    }

    template() {
        const items = this._processItems();
        return `
            <nav class="ui-breadcrumb" aria-label="Breadcrumb">
                <ol class="ui-breadcrumb__list">
                    ${items.map((item, i) => `
                        <li class="ui-breadcrumb__item ${i === items.length - 1 ? 'ui-breadcrumb__item--current' : ''}"
                            ${i === items.length - 1 ? 'aria-current="page"' : ''}>
                            ${i === items.length - 1
                                ? `<span class="ui-breadcrumb__label">${item.label}</span>`
                                : `<a class="ui-breadcrumb__link" href="${item.href || '#'}">${item.label}</a>`
                            }
                            ${i < items.length - 1 ? `<span class="ui-breadcrumb__sep">${FiscalUI.icons.render('chevron-right', { size: 14 })}</span>` : ''}
                        </li>
                    `).join('')}
                </ol>
            </nav>
        `;
    }

    _processItems() {
        if (!this.maxItems || this.items.length <= this.maxItems) return this.items;
        const first = this.items[0];
        const last = this.items.slice(-(this.maxItems - 1));
        return [first, { label: '...', href: null }, ...last];
    }

    onInit() {
        this.queryAll('.ui-breadcrumb__link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                this.emit('breadcrumb:select', { href: link.getAttribute('href'), label: link.textContent });
            });
        });
    }
}
```

```css
.ui-breadcrumb__list {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    list-style: none;
    margin: 0;
    padding: 0;
}

.ui-breadcrumb__item { display: flex; align-items: center; gap: var(--spacing-xs); }

.ui-breadcrumb__link {
    color: var(--color-text-secondary);
    text-decoration: none;
    font-size: var(--font-size-sm);
    transition: color var(--motion-fast);
}
.ui-breadcrumb__link:hover { color: var(--color-text); }

.ui-breadcrumb__item--current .ui-breadcrumb__label {
    color: var(--color-text);
    font-weight: var(--font-weight-semibold);
    font-size: var(--font-size-sm);
}

.ui-breadcrumb__sep { display: flex; color: var(--color-text-muted); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
