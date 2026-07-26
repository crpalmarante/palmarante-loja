# FiscalUI Framework

## Documento 064 — CNPJ

**Nível 4 — Formulários**

**Versão 1.0**

Campo de CNPJ com máscara automática (##.###.###/####-##) e validação de dígito verificador.

---

```js
class UICNPJ extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || '';
        this.value = options.value || '';
        this.placeholder = options.placeholder || '00.000.000/0000-00';
        this.rules = options.rules || [{ type: 'cnpj' }];
    }

    template() {
        return `
            <div class="ui-field">
                ${this.label ? `<label class="ui-field__label">${this.label}</label>` : ''}
                <div class="ui-field__input-wrapper">
                    <span class="ui-field__prefix-icon">${FiscalUI.icons.render('building', { size: 16 })}</span>
                    <input class="ui-field__input ui-field__input--cnpj" type="text" inputmode="numeric"
                           name="${this.name}" placeholder="${this.placeholder}"
                           value="${this.value || ''}" maxlength="18" autocomplete="off">
                </div>
                <span class="ui-field__error"></span>
            </div>
        `;
    }

    onInit() {
        this._input = this.query('.ui-field__input');

        this._input.addEventListener('input', () => {
            const raw = this._input.value.replace(/\D/g, '').slice(0, 14);
            this._input.value = this._mask(raw);
            this.value = raw;
            this.emit('field:change', { name: this.name, value: this.value });
        });

        this._input.addEventListener('blur', () => {
            if (this.value.length === 14 && !this._validate(this.value)) {
                this.element.classList.add('ui-field--error');
                this.query('.ui-field__error').textContent = 'CNPJ inválido';
            }
            this.emit('field:blur', { name: this.name });
        });
    }

    _mask(raw) {
        return raw
            .replace(/^(\d{2})(\d)/, '$1.$2')
            .replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3')
            .replace(/^(\d{2})\.(\d{3})\.(\d{3})(\d)/, '$1.$2.$3/$4')
            .replace(/^(\d{2})\.(\d{3})\.(\d{3})\/(\d{4})(\d)/, '$1.$2.$3/$4-$5');
    }

    _validate(cnpj) {
        const d = cnpj.replace(/\D/g, '');
        if (d.length !== 14 || /^(\d)\1{13}$/.test(d)) return false;
        const calc = (factor) => d.slice(0, factor - 1).split('').reduce((s, n, i) => s + parseInt(n) * (i < 4 ? 5 - i + factor - 5 : 13 - i + factor - 5), 0);
        const d1 = calc(13) % 11 < 2 ? 0 : 11 - calc(13) % 11;
        const d2 = calc(14) % 11 < 2 ? 0 : 11 - calc(14) % 11;
        return d1 === parseInt(d[12]) && d2 === parseInt(d[13]);
    }

    value() { return this.value; }
    setValue(val) { this.value = val.replace(/\D/g, ''); if (this._input) this._input.value = this._mask(this.value); }
    reset() { this.setValue(''); }
}
```

```css
.ui-field__input--cnpj { font-family: monospace; letter-spacing: 1px; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
