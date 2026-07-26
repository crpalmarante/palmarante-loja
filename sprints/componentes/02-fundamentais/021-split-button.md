# FiscalUI Framework

## Documento 021 — Split Button

**Nível 2 — Basic Components**

**Versão 1.0**

Botão com ação principal + dropdown de ações secundárias. Útil quando há uma ação padrão e variações possíveis.

---

# 1. Visão Geral

O Split Button combina um botão principal com um menu dropdown acionado por uma seta. A ação principal é executada no clique do botão; a seta revela ações alternativas.

```
┌──────────────────────────────────┐
│  Salvar                     ▼   │
└──────────────────────────────────┘
    ├── Salvar
    ├── Salvar como rascunho
    └── Salvar e notificar
```

---

# 2. API

```js
class UISplitButton extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.label = options.label || '';
        this.variant = options.variant || 'primary';
        this.size = options.size || 'md';
        this.icon = options.icon || null;
        this.disabled = options.disabled || false;
        this.items = options.items || [];         // { label, icon, onClick }
        this.onClick = options.onClick || null;
        this._open = false;
    }

    template() {
        return `
            <div class="ui-split-btn ${this.disabled ? 'ui-split-btn--disabled' : ''}">
                <button class="ui-btn ui-btn--${this.variant} ui-btn--${this.size} ui-split-btn__main"
                        type="button" ${this.disabled ? 'disabled' : ''}>
                    ${this.icon ? FiscalUI.icons.render(this.icon, { size: 18 }) : ''}
                    <span class="ui-btn__label">${this.label}</span>
                </button>
                <button class="ui-btn ui-btn--${this.variant} ui-btn--${this.size} ui-split-btn__toggle"
                        type="button" aria-label="Mais ações" ${this.disabled ? 'disabled' : ''}>
                    ${FiscalUI.icons.render('chevron-down', { size: 16 })}
                </button>
                <div class="ui-split-btn__menu" hidden>
                    ${this.items.map((item, i) => `
                        <button class="ui-split-btn__item" data-index="${i}" type="button">
                            ${item.icon ? FiscalUI.icons.render(item.icon, { size: 16 }) : ''}
                            <span>${item.label}</span>
                        </button>
                    `).join('')}
                </div>
            </div>
        `;
    }

    onInit() {
        this._main = this.query('.ui-split-btn__main');
        this._toggle = this.query('.ui-split-btn__toggle');
        this._menu = this.query('.ui-split-btn__menu');

        this._main.addEventListener('click', (e) => {
            if (this.disabled) return;
            this.emit('split-btn:click', { originalEvent: e });
            this.onClick?.(e);
        });

        this._toggle.addEventListener('click', () => this._toggleMenu());

        this._menu.addEventListener('click', (e) => {
            const item = e.target.closest('.ui-split-btn__item');
            if (!item) return;
            const idx = parseInt(item.dataset.index);
            const action = this.items[idx];
            action?.onClick?.();
            this._closeMenu();
        });

        document.addEventListener('click', (e) => {
            if (this._open && !this.element.contains(e.target)) this._closeMenu();
        });
    }

    _toggleMenu() { this._open ? this._closeMenu() : this._openMenu(); }
    _openMenu() { this._open = true; this._menu.hidden = false; }
    _closeMenu() { this._open = false; this._menu.hidden = true; }
}
```

---

# 3. CSS

```css
.ui-split-btn {
    display: inline-flex;
    position: relative;
}

.ui-split-btn__main {
    border-radius: var(--radius-md) 0 0 var(--radius-md);
}

.ui-split-btn__toggle {
    border-radius: 0 var(--radius-md) var(--radius-md) 0;
    border-left: 1px solid rgba(0,0,0,0.1);
    padding: 0 var(--spacing-sm);
    min-width: auto;
}

.ui-split-btn__menu {
    position: absolute;
    top: 100%;
    right: 0;
    min-width: 200px;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-lg);
    z-index: var(--z-dropdown);
    padding: var(--spacing-xs);
    margin-top: var(--spacing-xs);
}

.ui-split-btn__item {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    width: 100%;
    padding: var(--spacing-sm) var(--spacing-md);
    border: none;
    background: transparent;
    color: var(--color-text);
    cursor: pointer;
    border-radius: var(--radius-sm);
    font-size: var(--font-size-sm);
}

.ui-split-btn__item:hover { background: var(--color-surface-hover); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial |
