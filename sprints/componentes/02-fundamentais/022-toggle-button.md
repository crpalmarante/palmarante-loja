# FiscalUI Framework

## Documento 022 — Toggle Button

**Nível 2 — Basic Components**

**Versão 1.0**

Botão que mantém estado ligado/desligado. Usado em toolbars, filtros e grupos de opções.

---

# 1. Visão Geral

Toggle Button é um botão que alterna entre dois estados: ativo e inativo. Diferente do checkbox, ele é visual e imediatamente perceptível como botão.

```js
const toggle = new UIToggleButton({
    label: 'Negrito',
    icon: 'bold',
    pressed: false,
    onChange: (pressed) => console.log(pressed ? 'Ativado' : 'Desativado')
});
```

---

# 2. API

```js
class UIToggleButton extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.label = options.label || '';
        this.icon = options.icon || null;
        this.pressed = options.pressed || false;
        this.disabled = options.disabled || false;
        this.size = options.size || 'md';
        this.onChange = options.onChange || null;
    }

    template() {
        return `
            <button class="ui-toggle-btn ui-toggle-btn--${this.size}
                          ${this.pressed ? 'ui-toggle-btn--active' : ''}
                          ${this.disabled ? 'ui-toggle-btn--disabled' : ''}"
                    type="button"
                    role="button"
                    aria-pressed="${this.pressed}"
                    ${this.disabled ? 'disabled' : ''}>
                ${this.icon ? FiscalUI.icons.render(this.icon, { size: 16 }) : ''}
                <span class="ui-toggle-btn__label">${this.label}</span>
            </button>
        `;
    }

    onInit() {
        this.element.addEventListener('click', () => {
            if (this.disabled) return;
            this.pressed = !this.pressed;
            this.element.setAttribute('aria-pressed', this.pressed);
            this.element.classList.toggle('ui-toggle-btn--active', this.pressed);
            this.emit('toggle-btn:change', { pressed: this.pressed });
            this.onChange?.(this.pressed);
        });
    }

    setPressed(pressed) { this.pressed = pressed; this.render(); }
}
```

---

# 3. CSS

```css
.ui-toggle-btn {
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-xs);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    background: var(--color-surface);
    color: var(--color-text-secondary);
    cursor: pointer;
    transition: all var(--motion-fast) var(--ease-out);
}

.ui-toggle-btn:hover { background: var(--color-surface-hover); }
.ui-toggle-btn--active { background: var(--color-primary); color: var(--color-on-primary); border-color: var(--color-primary); }
.ui-toggle-btn--disabled { opacity: 0.5; cursor: not-allowed; }

.ui-toggle-btn--sm { height: 32px; padding: 0 var(--spacing-md); font-size: var(--font-size-sm); }
.ui-toggle-btn--md { height: 40px; padding: 0 var(--spacing-lg); }
```

---

# 4. Toolbar com Toggle Buttons

```html
<div class="ui-toolbar" role="toolbar" aria-label="Formatação de texto">
    <button class="ui-toggle-btn" aria-pressed="false">Negrito</button>
    <button class="ui-toggle-btn" aria-pressed="false">Itálico</button>
    <button class="ui-toggle-btn" aria-pressed="false">Sublinhado</button>
</div>
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial |
