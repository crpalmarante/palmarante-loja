# FiscalUI Framework

## Documento 139 — Money Utils

**Nível 8 — Utilities**

**Versão 1.0**

Utilitários financeiros: arredondamento, rateio, juros, cálculo de tributos.

---

```js
class MoneyUtils {
    static round(value, decimals = 2) {
        const factor = Math.pow(10, decimals);
        return Math.round(value * factor) / factor;
    }

    static truncate(value, decimals = 2) {
        const factor = Math.pow(10, decimals);
        return Math.trunc(value * factor) / factor;
    }

    static ceiling(value, decimals = 2) {
        const factor = Math.pow(10, decimals);
        return Math.ceil(value * factor) / factor;
    }

    static floor(value, decimals = 2) {
        const factor = Math.pow(10, decimals);
        return Math.floor(value * factor) / factor;
    }

    static sum(values) {
        return values.reduce((acc, v) => acc + v, 0);
    }

    static average(values) {
        return values.length ? MoneyUtils.sum(values) / values.length : 0;
    }

    static rate(total, parts) {
        return parts.map(p => ({
            value: p,
            percent: total > 0 ? MoneyUtils.round((p / total) * 100, 4) : 0
        }));
    }

    static split(total, parts) {
        if (parts.length === 0) return [];
        const perPart = MoneyUtils.floor(total / parts.length, 2);
        let remainder = MoneyUtils.round(total - perPart * parts.length, 2);
        return parts.map((_, i) => {
            if (i === parts.length - 1) return perPart + remainder;
            return perPart;
        });
    }

    static percentOf(value, percent) {
        return MoneyUtils.round(value * percent / 100, 2);
    }

    static addPercent(value, percent) {
        return MoneyUtils.round(value * (1 + percent / 100), 2);
    }

    static discountPercent(value, percent) {
        return MoneyUtils.round(value * (1 - percent / 100), 2);
    }

    static simpleInterest(capital, rate, months) {
        return MoneyUtils.round(capital * (1 + (rate / 100) * months), 2);
    }

    static compoundInterest(capital, rate, months) {
        return MoneyUtils.round(capital * Math.pow(1 + rate / 100, months), 2);
    }

    static pmt(rate, nper, pv) {
        const r = rate / 100;
        if (r === 0) return MoneyUtils.round(pv / nper, 2);
        const factor = Math.pow(1 + r, nper);
        return MoneyUtils.round(pv * r * factor / (factor - 1), 2);
    }

    static extend(value) {
        const [int, dec] = value.toFixed(2).split('.');
        const unidades = ['', 'um', 'dois', 'três', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove'];
        const especiais = ['dez', 'onze', 'doze', 'treze', 'quatorze', 'quinze', 'dezesseis', 'dezessete', 'dezoito', 'dezenove'];
        const dezenas = ['', '', 'vinte', 'trinta', 'quarenta', 'cinquenta', 'sessenta', 'setenta', 'oitenta', 'noventa'];
        const centenas = ['', 'cento', 'duzentos', 'trezentos', 'quatrocentos', 'quinhentos', 'seiscentos', 'setecentos', 'oitocentos', 'novecentos'];

        // Implementação simplificada — retorna o valor numérico
        // Versão completa exigiria parser recursivo
        return `${value.toFixed(2)} (${int},${dec})`;
    }

    static format(value) {
        return value.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }

    static diffPercentage(a, b) {
        if (b === 0) return a === 0 ? 0 : 100;
        return MoneyUtils.round(((a - b) / b) * 100, 2);
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
