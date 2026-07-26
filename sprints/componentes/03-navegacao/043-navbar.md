# FiscalUI Framework

## Documento 043 — Navbar

**Nível 3 — Navegação**

**Versão 1.0**

Barra de navegação horizontal superior. Contém logo, links, ações e menu do usuário. Fixa no topo com suporte a scroll.

---

```js
class UINavbar extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.logo = options.logo || '';
        this.title = options.title || '';
        this.links = options.links || [];
        this.actions = options.actions || [];
        this.user = options.user || null;
        this.sticky = options.sticky !== false;
        this.transparent = options.transparent || false;
    }

    template() {
        return `
            <header class="ui-navbar ${this.sticky ? 'ui-navbar--sticky' : ''} ${this.transparent ? 'ui-navbar--transparent' : ''}">
                <div class="ui-navbar__left">
                    <div class="ui-navbar__brand">
                        ${this.logo ? `<img class="ui-navbar__logo" src="${this.logo}" alt="${this.title}">` : ''}
                        <span class="ui-navbar__title">${this.title}</span>
                    </div>
                    <nav class="ui-navbar__links">
                        ${this.links.map(link => `
                            <a class="ui-navbar__link ${link.active ? 'ui-navbar__link--active' : ''}"
                               href="${link.href || '#'}">${link.label}</a>
                        `).join('')}
                    </nav>
                </div>
                <div class="ui-navbar__right">
                    <div class="ui-navbar__actions">
                        ${this.actions.map(action => `
                            <button class="ui-btn ui-btn--ghost ui-btn--icon" aria-label="${action.label}">
                                ${FiscalUI.icons.render(action.icon, { size: 20 })}
                            </button>
                        `).join('')}
                    </div>
                    ${this.user ? `
                    <div class="ui-navbar__user">
                        <img class="ui-avatar ui-avatar--sm" src="${this.user.avatar || ''}" alt="${this.user.name}">
                        <span class="ui-navbar__user-name">${this.user.name}</span>
                    </div>` : ''}
                </div>
            </header>
        `;
    }

    onInit() {
        this.queryAll('.ui-navbar__link').forEach(el => {
            el.addEventListener('click', (e) => {
                if (el.classList.contains('ui-navbar__link--active')) return;
                this.queryAll('.ui-navbar__link').forEach(l => l.classList.remove('ui-navbar__link--active'));
                el.classList.add('ui-navbar__link--active');
                this.emit('navbar:select', { href: el.getAttribute('href'), label: el.textContent });
            });
        });
    }
}
```

```css
.ui-navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 56px;
    padding: 0 var(--spacing-lg);
    background: var(--color-surface);
    border-bottom: 1px solid var(--color-border);
    z-index: var(--z-navbar);
}

.ui-navbar--sticky { position: sticky; top: 0; }
.ui-navbar--transparent { background: transparent; border-bottom-color: transparent; }

.ui-navbar__left, .ui-navbar__right { display: flex; align-items: center; gap: var(--spacing-lg); }
.ui-navbar__brand { display: flex; align-items: center; gap: var(--spacing-sm); }
.ui-navbar__logo { height: 28px; width: 28px; }
.ui-navbar__title { font-weight: var(--font-weight-semibold); font-size: var(--font-size-lg); }

.ui-navbar__links { display: flex; gap: var(--spacing-xs); }
.ui-navbar__link {
    padding: var(--spacing-xs) var(--spacing-md);
    border-radius: var(--radius-sm);
    color: var(--color-text-secondary);
    text-decoration: none;
    font-size: var(--font-size-md);
    transition: background var(--motion-fast), color var(--motion-fast);
}
.ui-navbar__link:hover { background: var(--color-surface-hover); color: var(--color-text); }
.ui-navbar__link--active { color: var(--color-primary); font-weight: var(--font-weight-semibold); }

.ui-navbar__actions { display: flex; align-items: center; gap: var(--spacing-xs); }
.ui-navbar__user { display: flex; align-items: center; gap: var(--spacing-sm); cursor: pointer; }
.ui-navbar__user-name { font-size: var(--font-size-sm); font-weight: var(--font-weight-medium); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
