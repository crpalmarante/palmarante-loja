# FiscalUI Framework

## Documento 058 — Password

**Nível 4 — Formulários**

**Versão 1.0**

Campo de senha com toggle de visibilidade, medidor de força e sugestão de gerador.

---

```js
class UIPassword extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || '';
        this.placeholder = options.placeholder || '••••••••';
        this.value = options.value || '';
        this.showToggle = options.showToggle !== false;
        this.showStrength = options.showStrength || false;
        this.rules = options.rules || [];
    }

    template() {
        return `
            <div class="ui-field">
                ${this.label ? `<label class="ui-field__label">${this.label}</label>` : ''}
                <div class="ui-field__input-wrapper">
                    <input class="ui-field__input" type="password"
                           name="${this.name}" placeholder="${this.placeholder}" value="${this.value}">
                    ${this.showToggle ? `<button class="ui-field__toggle-vis" type="button" aria-label="Mostrar senha">
                        ${FiscalUI.icons.render('eye', { size: 18 })}</button>` : ''}
                </div>
                ${this.showStrength ? `<div class="ui-password__meter"><div class="ui-password__meter-bar" style="width: 0%"></div></div>` : ''}
                <span class="ui-field__hint">Mín. 8 caracteres, 1 letra, 1 número</span>
                <span class="ui-field__error"></span>
            </div>
        `;
    }

    onInit() {
        this._input = this.query('.ui-field__input');
        this._toggleBtn = this.query('.ui-field__toggle-vis');
        this._meter = this.query('.ui-password__meter-bar');
        this._visible = false;

        this._input.addEventListener('input', () => {
            this.value = this._input.value;
            if (this._meter) this._updateStrength();
            this.emit('field:change', { name: this.name, value: this.value });
        });
        this._input.addEventListener('blur', () => this.emit('field:blur', { name: this.name }));

        this._toggleBtn?.addEventListener('click', () => {
            this._visible = !this._visible;
            this._input.type = this._visible ? 'text' : 'password';
            this._toggleBtn.innerHTML = FiscalUI.icons.render(this._visible ? 'eye-off' : 'eye', { size: 18 });
        });
    }

    _updateStrength() {
        const v = this.value;
        let score = 0;
        if (v.length >= 8) score += 25;
        if (/[a-z]/.test(v)) score += 15;
        if (/[A-Z]/.test(v)) score += 20;
        if (/\d/.test(v)) score += 20;
        if (/[^a-zA-Z0-9]/.test(v)) score += 20;
        this._meter.style.width = `${Math.min(score, 100)}%`;
        this._meter.style.background = score < 40 ? 'var(--color-danger)' : score < 70 ? 'var(--color-warning)' : 'var(--color-success)';
    }

    value() { return this._input?.value || this.value; }
    setValue(val) { this.value = val; if (this._input) this._input.value = val; }
    reset() { this.setValue(''); this._meter ? this._meter.style.width = '0%' : null; }
}
```

```css
.ui-field__toggle-vis {
    border: none; background: transparent; cursor: pointer;
    padding: 0 var(--spacing-sm); color: var(--color-text-muted);
    display: flex; align-items: center;
}
.ui-field__toggle-vis:hover { color: var(--color-text); }

.ui-password__meter { height: 4px; background: var(--color-surface-hover); border-radius: 2px; margin-top: var(--spacing-xs); }
.ui-password__meter-bar { height: 100%; border-radius: 2px; transition: width var(--motion-normal), background var(--motion-normal); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
