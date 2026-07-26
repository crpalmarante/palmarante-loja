# FiscalUI Framework

## Documento 020 — Icon Button

**Nível 2 — Basic Components**

**Versão 1.0**

Botão composto apenas por ícone. Usado para ações compactas em toolbars, tabelas, cards e inputs.

---

# 1. Visão Geral

O Icon Button é um botão que exibe apenas um ícone (sem label). Leva menos espaço e é usado em contextos onde a ação é evidente pelo ícone (lixeira = excluir, lápis = editar).

---

# 2. Variantes

```css
.ui-icon-btn              → ghost (padrão, sem fundo)
.ui-icon-btn--solid       → fundo sólido (primary, danger)
.ui-icon-btn--outline     → com borda
```

---

# 3. Tamanhos

```css
.ui-icon-btn--xs  → 24px
.ui-icon-btn--sm  → 32px
.ui-icon-btn--md  → 40px (padrão)
.ui-icon-btn--lg  → 48px
```

---

# 4. API

```js
class UIIconButton extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.icon = options.icon || 'close';
        this.variant = options.variant || 'ghost';
        this.size = options.size || 'md';
        this.label = options.label || '';   // aria-label
        this.disabled = options.disabled || false;
        this.onClick = options.onClick || null;
    }

    template() {
        return `
            <button class="ui-icon-btn ui-icon-btn--${this.variant} ui-icon-btn--${this.size}
                          ${this.disabled ? 'ui-icon-btn--disabled' : ''}"
                    type="button"
                    aria-label="${this.label}"
                    ${this.disabled ? 'disabled' : ''}>
                ${FiscalUI.icons.render(this.icon, { size: this._iconSize() })}
            </button>
        `;
    }

    _iconSize() {
        return { xs: 14, sm: 16, md: 20, lg: 24 }[this.size] || 20;
    }

    onInit() {
        this.element.addEventListener('click', (e) => {
            if (this.disabled) return;
            this.emit('icon-button:click', { originalEvent: e });
            this.onClick?.(e);
        });
    }
}
```

---

# 5. CSS

```css
.ui-icon-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border: none;
    border-radius: var(--radius-md);
    background: transparent;
    color: var(--color-text-secondary);
    cursor: pointer;
    transition: all var(--motion-fast) var(--ease-out);
}

.ui-icon-btn:hover { background: var(--color-surface-hover); color: var(--color-text); }
.ui-icon-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.ui-icon-btn:focus-visible { outline: 2px solid var(--color-primary); outline-offset: 2px; }

.ui-icon-btn--solid { background: var(--color-primary); color: var(--color-on-primary); }
.ui-icon-btn--solid:hover { background: var(--color-primary-hover); }
.ui-icon-btn--outline { border: 1px solid var(--color-border); }
.ui-icon-btn--outline:hover { border-color: var(--color-primary); color: var(--color-primary); }

.ui-icon-btn--xs { width: 24px; height: 24px; }
.ui-icon-btn--sm { width: 32px; height: 32px; }
.ui-icon-btn--md { width: 40px; height: 40px; }
.ui-icon-btn--lg { width: 48px; height: 48px; }
```

---

# 6. Acessibilidade

```html
<!-- ✅ Sempre ter aria-label -->
<button class="ui-icon-btn" aria-label="Editar">...</button>
<button class="ui-icon-btn" aria-label="Excluir">...</button>

<!-- Ou tooltip visível -->
<span class="ui-tooltip" data-tooltip="Editar">
    <button class="ui-icon-btn" aria-label="Editar">...</button>
</span>
```

---

# 7. Exemplos

```js
// Editar (tabela)
new UIIconButton({ icon: 'edit', label: 'Editar', onClick: () => editRow(id) });

// Excluir (tabela)
new UIIconButton({ icon: 'trash', label: 'Excluir', variant: 'danger', onClick: () => deleteRow(id) });

// Fechar (modal)
new UIIconButton({ icon: 'close', label: 'Fechar', onClick: () => modal.close() });
```

---

# 8. Testes

```js
describe('UIIconButton', () => {
    it('should render icon', () => {
        const btn = new UIIconButton({ icon: 'edit', label: 'Editar' });
        btn.render();
        expect(btn.element.querySelector('svg')).toBeTruthy();
    });

    it('should have aria-label', () => {
        const btn = new UIIconButton({ icon: 'close', label: 'Fechar' });
        btn.render();
        expect(btn.element.getAttribute('aria-label')).toBe('Fechar');
    });
});
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial |
