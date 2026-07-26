# FiscalUI Framework

## Documento 136 — Mask Engine

**Nível 8 — Utilities**

**Versão 1.0**

Motor de máscaras de entrada para inputs. Suporta CPF, CNPJ, CEP, telefone, RG, IE, data, hora, dinheiro.

---

```js
class MaskEngine {
    constructor() {
        this._masks = new Map();
        this._registerDefaults();
    }

    _registerDefaults() {
        this.register('cpf', '999.999.999-99');
        this.register('cnpj', '99.999.999/9999-99');
        this.register('cep', '99999-999');
        this.register('phone', '(99) 99999-9999');
        this.register('phone_fixed', '(99) 9999-9999');
        this.register('date', '99/99/9999');
        this.register('time', '99:99');
        this.register('datetime', '99/99/9999 99:99');
        this.register('credit_card', '9999 9999 9999 9999');
        this.register('ie', '999.999.999.999');
        this.register('rg', '99.999.999-9');
    }

    register(name, pattern) {
        this._masks.set(name, pattern);
    }

    apply(value, maskOrName) {
        const mask = this._masks.has(maskOrName) ? this._masks.get(maskOrName) : maskOrName;
        if (!mask) return value;

        const digits = value.replace(/\D/g, '');
        let result = '';
        let d = 0;

        for (let i = 0; i < mask.length && d < digits.length; i++) {
            if (mask[i] === '9') {
                result += digits[d++];
            } else {
                result += mask[i];
            }
        }
        return result;
    }

    unapply(value) {
        return value.replace(/\D/g, '');
    }

    bind(input, maskOrName, options = {}) {
        const handler = (e) => {
            const masked = this.apply(e.target.value, maskOrName);
            if (e.target.value !== masked) {
                e.target.value = masked;
                e.target.dispatchEvent(new Event('input', { bubbles: true }));
            }
        };
        input.addEventListener('input', handler);
        return () => input.removeEventListener('input', handler);
    }

    money(value, options = {}) {
        const locale = options.locale || 'pt-BR';
        const currency = options.currency || 'BRL';
        const raw = value.replace(/\D/g, '');
        const num = parseInt(raw) / 100;
        if (isNaN(num)) return '';
        return new Intl.NumberFormat(locale, { style: 'currency', currency, minimumFractionDigits: 2 }).format(num);
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
