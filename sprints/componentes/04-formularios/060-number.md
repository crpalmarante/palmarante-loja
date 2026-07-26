# FiscalUI Framework

## Documento 060 — Number

**Nível 4 — Formulários**

**Versão 1.0**

Campo numérico com stepper, min/max, step e formatação de decimais.

---

```js
class UINumber extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || '';
        this.value = options.value ?? '';
        this.min = options.min ?? null;
        this.max = options.max ?? null;
        this.step = options.step ?? 1;
        this.decimals = options.decimals ?? 0;
        this.placeholder = options.placeholder || '';
        this.showStepper = options.showStepper !== false;
        this.prefix = options.prefix || '';
        this.rules = options.rules || [];
    }

    template() {
        return `
            <div class="ui-field">
                ${this.label ? `<label class="ui-field__label">${this.label}</label>` : ''}
                <div class="ui-field__input-wrapper">
                    ${this.prefix ? `<span class="ui-field__prefix">${this.prefix}</span>` : ''}
                    <input class="ui-field__input" type="text" inputmode="decimal"
                           name="${this.name}" placeholder="${this.placeholder}"
                           value="${this.value !== '' ? this._format(this.value) : ''}"
                           autocomplete="off">
                    ${this.showStepper ? `
                    <div class="ui-field__stepper">
                        <button class="ui-field__step-up" aria-label="Aumentar">▲</button>
                        <button class="ui-field__step-down" aria-label="Diminuir">▼</button>
                    </div>` : ''}
                </div>
                <span class="ui-field__error"></span>
            </div>
        `;
    }

    onInit() {
        this._input = this.query('.ui-field__input');

        this._input.addEventListener('input', () => {
            const raw = this._input.value.replace(/[^\d,.-]/g, '');
            this._input.value = raw;
            this.value = this._parse(raw);
            this.emit('field:change', { name: this.name, value: this.value });
        });

        this._input.addEventListener('blur', () => {
            this._input.value = this.value !== '' ? this._format(this.value) : '';
            this.emit('field:blur', { name: this.name });
        });

        this._input.addEventListener('focus', () => {
            this._input.value = this.value !== '' ? String(this._toNumber(this.value)) : '';
            this._input.select();
        });

        this.query('.ui-field__step-up')?.addEventListener('click', () => this._step(this.step));
        this.query('.ui-field__step-down')?.addEventListener('click', () => this._step(-this.step));
    }

    _step(delta) {
        let val = this._toNumber(this.value) || 0;
        val = Math.round((val + delta) / this.step) * this.step;
        if (this.min !== null) val = Math.max(val, this.min);
        if (this.max !== null) val = Math.min(val, this.max);
        this.value = val;
        this._input.value = this._format(val);
        this.emit('field:change', { name: this.name, value: this.value });
    }

    _format(val) {
        const n = this._toNumber(val);
        if (isNaN(n)) return '';
        return n.toFixed(this.decimals).replace('.', ',');
    }

    _parse(str) {
        const normalized = str.replace(/\./g, '').replace(',', '.');
        const n = parseFloat(normalized);
        return isNaN(n) ? '' : n;
    }

    _toNumber(val) {
        if (val === '' || val === null || val === undefined) return NaN;
        if (typeof val === 'number') return val;
        return parseFloat(String(val).replace(',', '.'));
    }

    value() { return this.value; }
    setValue(val) { this.value = val; if (this._input) this._input.value = val !== '' ? this._format(val) : ''; }
    reset() { this.setValue(''); }
}
```

```css
.ui-field__stepper { display: flex; flex-direction: column; border-left: 1px solid var(--color-border); }
.ui-field__step-up, .ui-field__step-down {
    border: none; background: transparent; cursor: pointer;
    font-size: 8px; padding: 1px 8px; color: var(--color-text-muted);
    line-height: 1; flex: 1; transition: background var(--motion-fast);
}
.ui-field__step-up:hover, .ui-field__step-down:hover { background: var(--color-surface-hover); color: var(--color-text); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
