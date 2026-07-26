# FiscalUI Framework

## Documento 134 — Validators

**Nível 8 — Utilities**

**Versão 1.0**

Biblioteca de validação brasileira: CPF, CNPJ, IE, CEP, telefone, e-mail, URLs e validações genéricas.

---

```js
class Validators {
    static cpf(value) {
        const digits = value.replace(/\D/g, '');
        if (digits.length !== 11 || /^(\d)\1{10}$/.test(digits)) return false;

        const calc = (digits, factors) =>
            factors.reduce((acc, f, i) => acc + parseInt(digits[i]) * f, 0) % 11;

        const d1 = calc(digits, [10,9,8,7,6,5,4,3,2]) < 2 ? 0 : 11 - calc(digits, [10,9,8,7,6,5,4,3,2]);
        const d2 = calc(digits, [11,10,9,8,7,6,5,4,3,2]) < 2 ? 0 : 11 - calc(digits, [11,10,9,8,7,6,5,4,3,2]);

        return d1 === parseInt(digits[9]) && d2 === parseInt(digits[10]);
    }

    static cnpj(value) {
        const digits = value.replace(/\D/g, '');
        if (digits.length !== 14 || /^(\d)\1{13}$/.test(digits)) return false;

        const calc = (d, factors) => {
            const sum = factors.reduce((acc, f, i) => acc + parseInt(d[i]) * f, 0);
            const r = sum % 11;
            return r < 2 ? 0 : 11 - r;
        };

        const d1 = calc(digits, [5,4,3,2,9,8,7,6,5,4,3,2]);
        const d2 = calc(digits, [6,5,4,3,2,9,8,7,6,5,4,3,2]);

        return d1 === parseInt(digits[12]) && d2 === parseInt(digits[13]);
    }

    static ie(value, uf) {
        const digits = value.replace(/\D/g, '');
        const rules = {
            SP: () => digits.length >= 12 && digits.length <= 13,
            RJ: () => digits.length === 8,
            MG: () => digits.length === 13,
            RS: () => digits.length === 10,
            PR: () => digits.length === 10,
            SC: () => digits.length === 9,
            // ... demais UFs
        };
        return rules[uf] ? rules[uf]() : false;
    }

    static cep(value) {
        const digits = value.replace(/\D/g, '');
        return digits.length === 8;
    }

    static phone(value) {
        const digits = value.replace(/\D/g, '');
        return digits.length >= 10 && digits.length <= 11;
    }

    static email(value) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
    }

    static url(value) {
        try { new URL(value); return true; } catch { return false; }
    }

    static required(value) {
        if (value === null || value === undefined) return false;
        if (typeof value === 'string') return value.trim().length > 0;
        return true;
    }

    static minLength(value, min) {
        return typeof value === 'string' && value.length >= min;
    }

    static maxLength(value, max) {
        return typeof value === 'string' && value.length <= max;
    }

    static min(value, min) {
        return typeof value === 'number' && value >= min;
    }

    static max(value, max) {
        return typeof value === 'number' && value <= max;
    }

    static pattern(value, regex) {
        return regex.test(value);
    }

    static greaterThan(value, threshold) { return Number(value) > threshold; }
    static lessThan(value, threshold) { return Number(value) < threshold; }
    static between(value, min, max) { return value >= min && value <= max; }
    static integer(value) { return Number.isInteger(Number(value)); }
    static decimal(value) { return !isNaN(value) && String(value).includes('.'); }

    static form(rules, data) {
        const errors = {};
        for (const [field, fieldRules] of Object.entries(rules)) {
            for (const rule of fieldRules) {
                const { validator, message, params } = rule;
                if (!this[validator](data[field], ...(params || []))) {
                    if (!errors[field]) errors[field] = [];
                    errors[field].push(message || `Falha na validação '${validator}'`);
                }
            }
        }
        return { valid: Object.keys(errors).length === 0, errors };
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
