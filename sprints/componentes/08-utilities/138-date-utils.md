# FiscalUI Framework

## Documento 138 — Date Utils

**Nível 8 — Utilities**

**Versão 1.0**

Utilitários de data sem dependências externas: formatação, cálculo de diferenças, dias úteis, feriados brasileiros.

---

```js
class DateUtils {
    static format(date, pattern = 'dd/MM/yyyy') {
        const d = date instanceof Date ? date : new Date(date);
        const map = {
            dd: String(d.getDate()).padStart(2, '0'),
            MM: String(d.getMonth() + 1).padStart(2, '0'),
            yyyy: d.getFullYear(),
            HH: String(d.getHours()).padStart(2, '0'),
            mm: String(d.getMinutes()).padStart(2, '0'),
            ss: String(d.getSeconds()).padStart(2, '0')
        };
        return pattern.replace(/dd|MM|yyyy|HH|mm|ss/g, m => map[m]);
    }

    static diffDays(a, b) {
        const diff = Math.abs(new Date(a) - new Date(b));
        return Math.floor(diff / (1000 * 60 * 60 * 24));
    }

    static addDays(date, days) {
        const d = new Date(date);
        d.setDate(d.getDate() + days);
        return d;
    }

    static addMonths(date, months) {
        const d = new Date(date);
        d.setMonth(d.getMonth() + months);
        return d;
    }

    static addYears(date, years) {
        const d = new Date(date);
        d.setFullYear(d.getFullYear() + years);
        return d;
    }

    static startOfDay(date) {
        const d = new Date(date);
        d.setHours(0, 0, 0, 0);
        return d;
    }

    static endOfDay(date) {
        const d = new Date(date);
        d.setHours(23, 59, 59, 999);
        return d;
    }

    static startOfMonth(date) {
        const d = new Date(date);
        d.setDate(1);
        return DateUtils.startOfDay(d);
    }

    static endOfMonth(date) {
        const d = new Date(date);
        d.setMonth(d.getMonth() + 1);
        d.setDate(0);
        return DateUtils.endOfDay(d);
    }

    static isWeekend(date) {
        const day = new Date(date).getDay();
        return day === 0 || day === 6;
    }

    static isBusinessDay(date) {
        if (DateUtils.isWeekend(date)) return false;
        const holidays = DateUtils.getBrazilianHolidays(new Date(date).getFullYear());
        const d = DateUtils.format(date, 'yyyy-MM-dd');
        return !holidays.includes(d);
    }

    static getBrazilianHolidays(year) {
        const easter = DateUtils._easter(year);
        const carnival = DateUtils.addDays(easter, -47);
        const corpusChristi = DateUtils.addDays(easter, 60);

        return [
            `${year}-01-01`,         // Confraternização Universal
            `${year}-04-21`,         // Tiradentes
            `${year}-05-01`,         // Dia do Trabalho
            `${year}-09-07`,         // Independência
            `${year}-10-12`,         // Nossa Senhora Aparecida
            `${year}-11-02`,         // Finados
            `${year}-11-15`,         // Proclamação da República
            `${year}-11-20`,         // Consciência Negra
            `${year}-12-25`,         // Natal
            DateUtils.format(easter, 'yyyy-MM-dd'),
            DateUtils.format(carnival, 'yyyy-MM-dd'),
            DateUtils.format(corpusChristi, 'yyyy-MM-dd')
        ];
    }

    static _easter(year) {
        const a = year % 19, b = Math.floor(year / 100), c = year % 100;
        const d = Math.floor(b / 4), e = b % 4, f = Math.floor((b + 8) / 25);
        const g = Math.floor((b - f + 1) / 3), h = (19 * a + b - d - g + 15) % 30;
        const i = Math.floor(c / 4), k = c % 4, l = (32 + 2 * e + 2 * i - h - k) % 7;
        const m = Math.floor((a + 11 * h + 22 * l) / 451);
        const month = Math.floor((h + l - 7 * m + 114) / 31);
        const day = ((h + l - 7 * m + 114) % 31) + 1;
        return new Date(year, month - 1, day);
    }

    static daysBetweenBusiness(a, b) {
        let count = 0;
        let current = new Date(Math.min(a, b));
        const end = new Date(Math.max(a, b));
        while (current <= end) {
            if (DateUtils.isBusinessDay(current)) count++;
            current = DateUtils.addDays(current, 1);
        }
        return count;
    }

    static monthsBetween(a, b) {
        const d1 = new Date(a), d2 = new Date(b);
        return (d2.getFullYear() - d1.getFullYear()) * 12 + (d2.getMonth() - d1.getMonth());
    }

    static age(birthDate) {
        const today = new Date();
        const birth = new Date(birthDate);
        let age = today.getFullYear() - birth.getFullYear();
        const m = today.getMonth() - birth.getMonth();
        if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) age--;
        return age;
    }

    static parse(dateStr, pattern = 'dd/MM/yyyy') {
        const parts = dateStr.split(/[^0-9]/);
        const p = pattern.split(/[^A-Za-z]/);
        const map = {};
        p.forEach((k, i) => map[k] = parseInt(parts[i]));
        return new Date(map['yyyy'], (map['MM'] || 1) - 1, map['dd'] || 1);
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
