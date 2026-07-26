# FiscalUI Framework

## Documento 147 — UUID

**Nível 8 — Utilities**

**Versão 1.0**

Gerador de UUID v4 (RFC 4122) e IDs sequenciais, curtos e customizados.

---

```js
class UUID {
    static v4() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
            const r = Math.random() * 16 | 0;
            return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
        });
    }

    static v4Upper() {
        return UUID.v4().toUpperCase();
    }

    static v4Compact() {
        return UUID.v4().replace(/-/g, '');
    }

    static short(length = 8) {
        const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
        let result = '';
        for (let i = 0; i < length; i++) {
            result += chars[Math.floor(Math.random() * chars.length)];
        }
        return result;
    }

    static shortUpper(length = 8) {
        return UUID.short(length).toUpperCase();
    }

    static sequential(prefix = '') {
        return `${prefix}${Date.now()}${Math.random().toString(36).slice(2, 6)}`;
    }

    static numeric() {
        return parseInt(Math.random().toString().slice(2, 12), 10);
    }

    static timestamp() {
        return `${Date.now()}-${Math.random().toString(36).slice(2, 6)}`;
    }

    static isValid(uuid) {
        return /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(uuid);
    }

    static nibble() {
        return Math.random().toString(16).slice(2, 10);
    }

    static crypto() {
        if (!window.crypto?.randomUUID) {
            return UUID.v4();
        }
        return window.crypto.randomUUID();
    }

    static generateId(prefix = 'ui') {
        return `${prefix}-${UUID.short(6)}`;
    }

    static snowflake(workerId = 1) {
        const epoch = 1700000000000n;
        const now = BigInt(Date.now()) - epoch;
        const seq = BigInt(Math.floor(Math.random() * 4096));
        return Number(now << 12n | BigInt(workerId) << 10n | seq);
    }

    static ulid() {
        const chars = '0123456789ABCDEFGHJKMNPQRSTVWXYZ';
        const time = Date.now().toString(32).toUpperCase().padStart(10, '0');
        let random = '';
        for (let i = 0; i < 16; i++) random += chars[Math.floor(Math.random() * 32)];
        return time + random;
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
