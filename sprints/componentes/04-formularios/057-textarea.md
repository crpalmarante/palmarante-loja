# FiscalUI Framework

## Documento 057 — TextArea

**Nível 4 — Formulários**

**Versão 1.0**

Campo de texto multilinha. Suporta redimensionamento vertical, contador de caracteres e auto-resize.

---

```js
class UITextArea extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || '';
        this.placeholder = options.placeholder || '';
        this.value = options.value || '';
        this.rows = options.rows || 4;
        this.maxLength = options.maxLength || null;
        this.autoResize = options.autoResize || false;
        this.hint = options.hint || '';
        this.disabled = options.disabled || false;
        this.rules = options.rules || [];
    }

    template() {
        return `
            <div class="ui-field">
                ${this.label ? `<label class="ui-field__label">${this.label}</label>` : ''}
                <textarea class="ui-field__textarea"
                          name="${this.name}" rows="${this.rows}"
                          placeholder="${this.placeholder}"
                          ${this.disabled ? 'disabled' : ''}
                          ${this.maxLength ? `maxlength="${this.maxLength}"` : ''}>${this.value}</textarea>
                ${this.hint ? `<span class="ui-field__hint">${this.hint}</span>` : ''}
                <div class="ui-field__footer">
                    <span class="ui-field__error"></span>
                    ${this.maxLength ? `<span class="ui-field__counter">${this.value.length}/${this.maxLength}</span>` : ''}
                </div>
            </div>
        `;
    }

    onInit() {
        this._textarea = this.query('.ui-field__textarea');
        this._counter = this.query('.ui-field__counter');

        this._textarea.addEventListener('input', () => {
            this.value = this._textarea.value;
            if (this._counter) this._counter.textContent = `${this.value.length}/${this.maxLength}`;
            if (this.autoResize) this._resize();
            this.emit('field:change', { name: this.name, value: this.value });
        });
        this._textarea.addEventListener('blur', () => this.emit('field:blur', { name: this.name }));
        if (this.autoResize) this._resize();
    }

    _resize() {
        this._textarea.style.height = 'auto';
        this._textarea.style.height = `${this._textarea.scrollHeight}px`;
    }

    value() { return this._textarea?.value || this.value; }
    setValue(val) { this.value = val; if (this._textarea) { this._textarea.value = val; if (this.autoResize) this._resize(); } }
    reset() { this.setValue(''); }
}
```

```css
.ui-field__textarea {
    width: 100%; padding: var(--spacing-sm);
    border: 1px solid var(--color-border); border-radius: var(--radius-md);
    background: var(--color-surface); color: var(--color-text);
    font-size: var(--font-size-md); font-family: inherit;
    resize: vertical; transition: border-color var(--motion-fast), box-shadow var(--motion-fast);
    outline: none;
}
.ui-field__textarea:focus { border-color: var(--color-primary); box-shadow: 0 0 0 3px var(--color-primary-surface); }
.ui-field__textarea:disabled { opacity: 0.5; cursor: not-allowed; }
.ui-field__footer { display: flex; justify-content: space-between; align-items: flex-start; }
.ui-field__counter { font-size: var(--font-size-xs); color: var(--color-text-muted); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
