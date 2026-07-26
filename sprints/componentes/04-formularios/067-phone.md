# FiscalUI Framework

## Documento 067 — Phone

**Nível 4 — Formulários**

**Versão 1.0**

Campo de telefone com máscara para fixo ((##) ####-####) e celular ((##) #####-####).

---

```js
class UIPhone extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || 'Telefone';
        this.value = options.value || '';
        this.placeholder = options.placeholder || '(00) 00000-0000';
        this.rules = options.rules || [];
    }

    template() {
        return `
            <div class="ui-field">
                ${this.label ? `<label class="ui-field__label">${this.label}</label>` : ''}
                <div class="ui-field__input-wrapper">
                    <span class="ui-field__prefix-icon">${FiscalUI.icons.render('phone', { size: 16 })}</span>
                    <input class="ui-field__input ui-field__input--phone" type="tel"
                           name="${this.name}" placeholder="${this.placeholder}"
                           value="${this.value || ''}" maxlength="15" autocomplete="tel">
                </div>
                <span class="ui-field__error"></span>
            </div>
        `;
    }

    onInit() {
        this._input = this.query('.ui-field__input');

        this._input.addEventListener('input', () => {
            const raw = this._input.value.replace(/\D/g, '').slice(0, 11);
            this._input.value = this._mask(raw);
            this.value = raw;
            this.emit('field:change', { name: this.name, value: this.value });
        });

        this._input.addEventListener('blur', () => this.emit('field:blur', { name: this.name }));
    }

    _mask(raw) {
        if (raw.length <= 10) {
            return raw.replace(/^(\d{2})(\d)/, '($1) $2')
                      .replace(/^(\d{2}) (\d{4})(\d)/, '($1) $2-$3');
        }
        return raw.replace(/^(\d{2})(\d)/, '($1) $2')
                  .replace(/^(\d{2}) (\d{5})(\d)/, '($1) $2-$3');
    }

    value() { return this.value; }
    setValue(val) { this.value = val.replace(/\D/g, ''); if (this._input) this._input.value = this._mask(this.value); }
    reset() { this.setValue(''); }
}
```

```css
.ui-field__input--phone { font-family: monospace; letter-spacing: 0.5px; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
