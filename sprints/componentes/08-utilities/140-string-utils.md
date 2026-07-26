# FiscalUI Framework

## Documento 140 — String Utils

**Nível 8 — Utilities**

**Versão 1.0**

Utilitários de manipulação de strings: remoção de acentos, normalização, busca fonética, templates.

---

```js
class StringUtils {
    static removeAccents(str) {
        return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    }

    static normalize(str) {
        return StringUtils.removeAccents(str).toLowerCase().trim();
    }

    static compare(a, b) {
        return StringUtils.normalize(a) === StringUtils.normalize(b);
    }

    static contains(haystack, needle) {
        return StringUtils.normalize(haystack).includes(StringUtils.normalize(needle));
    }

    static search(query, items, keys) {
        const q = StringUtils.normalize(query);
        return items.filter(item =>
            keys.some(key => StringUtils.normalize(String(item[key])).includes(q))
        );
    }

    static slugify(str) {
        return StringUtils.removeAccents(str)
            .toLowerCase()
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/^-|-$/g, '');
    }

    static truncate(str, length = 100, suffix = '...') {
        if (str.length <= length) return str;
        return str.slice(0, length).trimEnd() + suffix;
    }

    static pad(str, length, char = ' ') {
        return str.toString().padStart(length, char);
    }

    static padEnd(str, length, char = ' ') {
        return str.toString().padEnd(length, char);
    }

    static template(str, data) {
        return str.replace(/\{\{(\w+)\}\}/g, (_, key) => data[key] !== undefined ? data[key] : `{{${key}}}`);
    }

    static pluralize(count, singular, plural) {
        return count === 1 ? singular : (plural || singular + 's');
    }

    static escapeHtml(str) {
        const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
        return str.replace(/[&<>"']/g, c => map[c]);
    }

    static unescapeHtml(str) {
        const map = { '&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"', '&#39;': "'" };
        return str.replace(/&(?:amp|lt|gt|quot|#39);/g, m => map[m]);
    }

    static reverse(str) { return str.split('').reverse().join(''); }

    static count(str, substring) {
        return (str.match(new RegExp(substring.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g')) || []).length;
    }

    static interpolate(str, ...args) {
        return str.replace(/%[sd]/g, () => args.shift());
    }

    static splitLines(str) { return str.split(/\r?\n/); }

    static indent(str, level = 1, char = '  ') {
        return str.split('\n').map(line => char.repeat(level) + line).join('\n');
    }

    static ellipsis(str, maxLen) {
        return str.length > maxLen ? str.slice(0, maxLen - 1) + '…' : str;
    }

    static soundex(str) {
        const s = StringUtils.removeAccents(str).toUpperCase();
        if (!s) return '';
        const first = s[0];
        const encoded = s.slice(1)
            .replace(/[AEIOUYHW]/g, '')
            .replace(/[BFPV]/g, '1')
            .replace(/[CGJKQSXZ]/g, '2')
            .replace(/[DT]/g, '3')
            .replace(/[L]/g, '4')
            .replace(/[MN]/g, '5')
            .replace(/[R]/g, '6')
            .replace(/(\d)\1+/g, '$1');
        return first + (encoded + '000').slice(0, 3);
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
