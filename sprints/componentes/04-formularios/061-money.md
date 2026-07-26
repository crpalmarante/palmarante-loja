# FiscalUI Framework

## Documento 061 — Money

**Nível 4 — Formulários**

**Versão 1.0**

Campo de valor monetário com formatação automática em Real (BRL). Suporta prefixo R$, separador de milhar e decimais fixos.

---

```js
class UIMoney extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || '';
        this.value = options.value ?? '';
        this.placeholder = options.placeholder || '0,00';
        this.decimals = options.decimals ?? 2;
        this.rules = options.rules || [];
    }

    template() {
        return `
            <div class="ui-field">
                ${this.label ? `<label class="ui-field__label">${this.label}</label>` : ''}
                <div class="ui-field__input-wrapper">
                    <span class="ui-field__prefix">R$</span>
                    <input class="ui-field__input ui-field__input--money" type="text" inputmode="decimal"
                           name="${this.name}" placeholder="${this.placeholder}"
                           value="${this.value !== '' ? this._format(this.value) : ''}" autocomplete="off">
                </div>
                <span class="ui-field__error"></span>
            </div>
        `;
    }

    onInit() {
        this._input = this.query('.ui-field__input');

        this._input.addEventListener('input', () => {
            const cursor = this._input.selectionStart;
            const raw = this._input.value.replace(/\D/g, '');
            const formatted = this._formatFromRaw(raw);
            this._input.value = formatted;
            this.value = this._parse(raw);
            this.emit('field:change', { name: this.name, value: this.value });
        });

        this._input.addEventListener('blur', () => {
            if (this.value !== '') this._input.value = this._format(this.value);
            this.emit('field:blur', { name: this.name });
        });

        this._input.addEventListener('focus', () => this._input.select());
    }

    _format(value) {
        const n = typeof value === 'string' ? parseFloat(value) : value;
        if (isNaN(n)) return '';
        return n.toLocaleString('pt-BR', { minimumFractionDigits: this.decimals, maximumFractionDigits: this.decimals });
    }

    _formatFromRaw(raw) {
        const padded = raw.padStart(this.decimals + 1, '0');
        const intPart = padded.slice(0, -this.decimals);
        const decPart = padded.slice(-this.decimals);
        return `${parseInt(intPart, 10).toLocaleString('pt-BR')},${decPart}`;
    }

    _parse(raw) {
        const num = parseInt(raw, 10);
        if (isNaN(num)) return '';
        return num / Math.pow(10, this.decimals);
    }

    value() { return this.value; }
    setValue(val) { this.value = val; if (this._input) this._input.value = val !== '' ? this._format(val) : ''; }
    reset() { this.setValue(''); }
}
```

```css
.ui-field__input--money { text-align: right; font-variant-numeric: tabular-nums; letter-spacing: 0.5px; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
