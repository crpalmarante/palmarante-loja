# FiscalUI Framework

## Documento 135 — Formatters

**Nível 8 — Utilities**

**Versão 1.0**

Utilitários de formatação para exibição de dados no padrão brasileiro.

---

```js
class Formatters {
    static currency(value, currency = 'BRL') {
        return new Intl.NumberFormat('pt-BR', { style: 'currency', currency }).format(value);
    }

    static number(value, decimals = 2) {
        return new Intl.NumberFormat('pt-BR', { minimumFractionDigits: decimals, maximumFractionDigits: decimals }).format(value);
    }

    static percent(value, decimals = 2) {
        return new Intl.NumberFormat('pt-BR', { style: 'percent', minimumFractionDigits: decimals, maximumFractionDigits: decimals }).format(value / 100);
    }

    static cpf(value) {
        const d = value.replace(/\D/g, '').slice(0, 11);
        return d.replace(/^(\d{3})(\d{3})(\d{3})(\d{2})$/, '$1.$2.$3-$4');
    }

    static cnpj(value) {
        const d = value.replace(/\D/g, '').slice(0, 14);
        return d.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/, '$1.$2.$3/$4-$5');
    }

    static cep(value) {
        const d = value.replace(/\D/g, '').slice(0, 8);
        return d.replace(/^(\d{5})(\d{3})$/, '$1-$2');
    }

    static phone(value) {
        const d = value.replace(/\D/g, '').slice(0, 11);
        if (d.length <= 10) return d.replace(/^(\d{2})(\d{4})(\d{4})$/, '($1) $2-$3');
        return d.replace(/^(\d{2})(\d{5})(\d{4})$/, '($1) $2-$3');
    }

    static date(value) {
        const d = value instanceof Date ? value : new Date(value);
        return d.toLocaleDateString('pt-BR');
    }

    static time(value) {
        const d = value instanceof Date ? value : new Date(value);
        return d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
    }

    static datetime(value) {
        return `${this.date(value)} ${this.time(value)}`;
    }

    static cnpjShort(value) {
        const d = value.replace(/\D/g, '').slice(0, 14);
        return d.replace(/^(\d{2})\d{3}(\d{4}).*$/, '$1.***.$2/****-**');
    }

    static cpfShort(value) {
        const d = value.replace(/\D/g, '').slice(0, 11);
        return d.replace(/^(\d{3})\d{3}(\d{2})$/, '$1.***.***-$2');
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
