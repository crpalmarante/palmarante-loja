# FiscalUI Framework

## Documento 056 — Input

**Nível 4 — Formulários**

**Versão 1.0**

Campo de texto base. Suporta label, placeholder, hint, erro, prefixo/sufixo, tamanhos e estados.

---

```js
class UIInput extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || '';
        this.placeholder = options.placeholder || '';
        this.value = options.value || '';
        this.type = options.type || 'text';
        this.hint = options.hint || '';
        this.prefix = options.prefix || '';
        this.suffix = options.suffix || '';
        this.size = options.size || 'md';              // sm, md, lg
        this.disabled = options.disabled || false;
        this.readonly = options.readonly || false;
        this.required = options.required || false;
        this.maxLength = options.maxLength || null;
        this.rules = options.rules || [];
    }

    template() {
        return `
            <div class="ui-field ${this.size ? `ui-field--${this.size}` : ''}">
                ${this.label ? `<label class="ui-field__label">${this.label}${this.required ? '<span class="ui-field__required">*</span>' : ''}</label>` : ''}
                <div class="ui-field__input-wrapper">
                    ${this.prefix ? `<span class="ui-field__prefix">${this.prefix}</span>` : ''}
                    <input class="ui-field__input"
                           type="${this.type}" name="${this.name}"
                           placeholder="${this.placeholder}"
                           value="${this.value}"
                           ${this.disabled ? 'disabled' : ''}
                           ${this.readonly ? 'readonly' : ''}
                           ${this.required ? 'required' : ''}
                           ${this.maxLength ? `maxlength="${this.maxLength}"` : ''}>
                    ${this.suffix ? `<span class="ui-field__suffix">${this.suffix}</span>` : ''}
                </div>
                ${this.hint ? `<span class="ui-field__hint">${this.hint}</span>` : ''}
                <span class="ui-field__error"></span>
            </div>
        `;
    }

    onInit() {
        this._input = this.query('.ui-field__input');
        this._input.addEventListener('input', () => {
            this.value = this._input.value;
            this.emit('field:change', { name: this.name, value: this.value });
        });
        this._input.addEventListener('blur', () => this.emit('field:blur', { name: this.name }));
        this._input.addEventListener('focus', () => this.element.classList.add('ui-field--focused'));
        this._input.addEventListener('blur', () => this.element.classList.remove('ui-field--focused'));
    }

    value() { return this._input?.value || this.value; }
    setValue(val) { this.value = val; if (this._input) this._input.value = val; }
    reset() { this.setValue(''); }
    focus() { this._input?.focus(); }
}
```

```css
.ui-field__input-wrapper {
    display: flex; align-items: center;
    border: 1px solid var(--color-border); border-radius: var(--radius-md);
    background: var(--color-surface); transition: border-color var(--motion-fast), box-shadow var(--motion-fast);
    overflow: hidden;
}
.ui-field--focused .ui-field__input-wrapper { border-color: var(--color-primary); box-shadow: 0 0 0 3px var(--color-primary-surface); }
.ui-field__input { flex: 1; border: none; outline: none; background: transparent; color: var(--color-text); padding: 0 var(--spacing-sm); font-size: var(--font-size-md); }
.ui-field__input:disabled { opacity: 0.5; cursor: not-allowed; }

.ui-field__prefix, .ui-field__suffix {
    padding: 0 var(--spacing-sm); color: var(--color-text-secondary);
    font-size: var(--font-size-sm); background: var(--color-surface-hover);
    height: 100%; display: flex; align-items: center;
}

.ui-field--sm .ui-field__input-wrapper { height: 32px; }
.ui-field--sm .ui-field__input { font-size: var(--font-size-sm); }
.ui-field--md .ui-field__input-wrapper { height: 40px; }
.ui-field--lg .ui-field__input-wrapper { height: 48px; }
.ui-field--lg .ui-field__input { font-size: var(--font-size-lg); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
