# FiscalUI Framework

## Documento 019 — Button

**Nível 2 — Basic Components**

**Versão 1.0**

Componente de botão do FiscalUI. Suporta variantes visuais, tamanhos, estados, ícones, loading e grupos. Construído sobre o `UIComponent` e seguindo o sistema de design tokens.

---

# Índice

1. Visão Geral
2. Variantes
3. Tamanhos
4. Estados
5. Ícones
6. Loading
7. Grupos
8. API
9. CSS
10. Eventos
11. Acessibilidade
12. Exemplos

---

# 1. Visão Geral

O Button é o bloco fundamental de interação. Toda ação no sistema começa com um clique.

```js
const btn = new UIButton({
    label: 'Salvar',
    variant: 'primary',
    icon: 'save',
    onClick: () => FiscalUI.emit('document:save')
});
btn.mount('#container');
```

---

# 2. Variantes

```css
.ui-btn--primary     → Ação principal (Salvar, Confirmar, Enviar)
.ui-btn--secondary   → Ação alternativa (Cancelar, Voltar)
.ui-btn--danger      → Ação destrutiva (Excluir, Cancelar)
.ui-btn--ghost       → Leve, sem fundo (ações inline)
.ui-btn--link        → Apenas texto, parece link
.ui-btn--outline     → Com borda, sem fundo
```

---

# 3. Tamanhos

```css
.ui-btn--xs    → 24px height (inline com texto)
.ui-btn--sm    → 32px height (formulários compactos)
.ui-btn--md    → 40px height (padrão)
.ui-btn--lg    → 48px height (telas cheias, CTAs)
```

---

# 4. Estados

```css
.ui-btn:disabled           → cursor: not-allowed, opacity reduzida
.ui-btn--loading           → spinner + label oculto
.ui-btn--active            → pressionado (mousedown)
.ui-btn:focus-visible      → outline de foco (teclado)
```

---

# 5. API

```js
class UIButton extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.label = options.label || '';
        this.variant = options.variant || 'primary';
        this.size = options.size || 'md';
        this.icon = options.icon || null;
        this.iconPosition = options.iconPosition || 'left';
        this.loading = options.loading || false;
        this.disabled = options.disabled || false;
        this.fullWidth = options.fullWidth || false;
        this.type = options.type || 'button';
        this.onClick = options.onClick || null;
    }

    template() {
        const icon = this.icon ? FiscalUI.icons.render(this.icon, { size: this._iconSize() }) : '';
        const iconBefore = this.icon && this.iconPosition === 'left' ? icon : '';
        const iconAfter = this.icon && this.iconPosition === 'right' ? icon : '';

        return `
            <button class="ui-btn ui-btn--${this.variant} ui-btn--${this.size}
                          ${this.fullWidth ? 'ui-btn--full' : ''}
                          ${this.loading ? 'ui-btn--loading' : ''}"
                    type="${this.type}"
                    ${this.disabled ? 'disabled' : ''}>
                ${this.loading ? '<span class="ui-btn__spinner"></span>' : ''}
                ${iconBefore}
                <span class="ui-btn__label">${this.label}</span>
                ${iconAfter}
            </button>
        `;
    }

    onInit() {
        this._el = this.element;
        this._el.addEventListener('click', (e) => this._onClick(e));
    }

    _onClick(e) {
        if (this.disabled || this.loading) return;
        this.emit('button:click', { originalEvent: e });
        if (this.onClick) this.onClick(e);
    }

    setLabel(label) { this.label = label; this.render(); }
    setDisabled(disabled) { this.disabled = disabled; this.render(); }
    setLoading(loading) { this.loading = loading; this.render(); }
    setIcon(icon) { this.icon = icon; this.render(); }

    _iconSize() {
        return { xs: 14, sm: 16, md: 18, lg: 20 }[this.size] || 18;
    }
}
```

---

# 6. CSS

```css
.ui-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: var(--spacing-xs);
    border: none;
    border-radius: var(--radius-md);
    font-family: var(--font-family);
    font-weight: var(--font-weight-medium);
    cursor: pointer;
    white-space: nowrap;
    user-select: none;
    transition: background var(--motion-fast) var(--ease-out),
                box-shadow var(--motion-fast) var(--ease-out),
                opacity var(--motion-fast) var(--ease-out);
}

.ui-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    pointer-events: none;
}

.ui-btn:focus-visible {
    outline: 2px solid var(--color-primary);
    outline-offset: 2px;
}

/* ─── Variantes ─────────────────────────── */

.ui-btn--primary {
    background: var(--color-primary);
    color: var(--color-on-primary);
}
.ui-btn--primary:hover { background: var(--color-primary-hover); }
.ui-btn--primary:active { background: var(--color-primary-active); }

.ui-btn--secondary {
    background: var(--color-secondary);
    color: var(--color-on-secondary);
}
.ui-btn--secondary:hover { background: var(--color-secondary-hover); }

.ui-btn--danger {
    background: var(--color-danger);
    color: var(--color-on-danger);
}
.ui-btn--danger:hover { background: var(--color-danger-hover); }

.ui-btn--ghost {
    background: transparent;
    color: var(--color-text-secondary);
}
.ui-btn--ghost:hover { background: var(--color-surface-hover); }

.ui-btn--outline {
    background: transparent;
    border: 1px solid var(--color-border);
    color: var(--color-text);
}
.ui-btn--outline:hover { background: var(--color-surface-hover); border-color: var(--color-primary); color: var(--color-primary); }

.ui-btn--link {
    background: transparent;
    color: var(--color-primary);
    padding: 0;
    text-decoration: none;
}
.ui-btn--link:hover { text-decoration: underline; }

/* ─── Tamanhos ─────────────────────────── */

.ui-btn--xs { height: 24px; padding: 0 var(--spacing-sm); font-size: var(--font-size-xs); }
.ui-btn--sm { height: 32px; padding: 0 var(--spacing-md); font-size: var(--font-size-sm); }
.ui-btn--md { height: 40px; padding: 0 var(--spacing-lg); font-size: var(--font-size-md); }
.ui-btn--lg { height: 48px; padding: 0 var(--spacing-xl); font-size: var(--font-size-lg); }

/* ─── Full Width ────────────────────────── */

.ui-btn--full { width: 100%; }

/* ─── Loading ─────────────────────────── */

.ui-btn--loading .ui-btn__label { visibility: hidden; }
.ui-btn--loading .ui-btn__spinner { position: absolute; }
```

---

# 7. Eventos

```js
'button:click'   → Botão foi clicado
```

---

# 8. Acessibilidade

```html
<!-- ✅ Correto -->
<button class="ui-btn ui-btn--primary" type="button">Salvar</button>

<!-- ✅ Com ícone sem texto -->
<button class="ui-btn ui-btn--ghost ui-btn--sm" aria-label="Editar">
    <svg>...</svg>
</button>
```

---

# 9. Exemplos

```js
// Botão primário
new UIButton({ label: 'Salvar', variant: 'primary', onClick: save });

// Botão de excluir com confirmação
new UIButton({ label: 'Excluir', variant: 'danger', onClick: () => confirm('Tem certeza?') });

// Botão com ícone
new UIButton({ label: 'Novo', icon: 'plus', variant: 'primary' });

// Botão loading
new UIButton({ label: 'Enviar', loading: true });

// Botão full width
new UIButton({ label: 'Entrar', fullWidth: true, variant: 'primary' });
```

---

# 10. Testes

```js
describe('UIButton', () => {
    it('should render label', () => {
        const btn = new UIButton({ label: 'Salvar' });
        btn.render();
        expect(btn.element.textContent).toContain('Salvar');
    });

    it('should emit click event', () => {
        const spy = jasmine.createSpy();
        const btn = new UIButton({ label: 'OK' });
        btn.render();
        btn.on('button:click', spy);
        btn.element.click();
        expect(spy).toHaveBeenCalled();
    });

    it('should not emit click when disabled', () => {
        const spy = jasmine.createSpy();
        const btn = new UIButton({ label: 'OK', disabled: true });
        btn.render();
        btn.on('button:click', spy);
        btn.element.click();
        expect(spy).not.toHaveBeenCalled();
    });
});
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial |
