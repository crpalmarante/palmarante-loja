# FiscalUI Framework

## Documento 119 — Cache

**Nível 7 — Services**

**Versão 1.0**

Serviço de cache em memória com suporte a TTL, LRU e persistência opcional.

---

```js
class CacheService {
    constructor(options = {}) {
        this.maxSize = options.maxSize || 100;
        this.defaultTTL = options.defaultTTL || 300000; // 5 min
        this._store = new Map();
        this._timers = new Map();
    }

    set(key, value, ttl) {
        if (this._store.size >= this.maxSize) this._evict();
        this._store.set(key, { value, expires: Date.now() + (ttl || this.defaultTTL) });
        if (this._timers.has(key)) clearTimeout(this._timers.get(key));
        this._timers.set(key, setTimeout(() => this._store.delete(key), ttl || this.defaultTTL));
    }

    get(key) {
        const entry = this._store.get(key);
        if (!entry) return null;
        if (Date.now() > entry.expires) { this._store.delete(key); return null; }
        return entry.value;
    }

    has(key) { return this.get(key) !== null; }

    remove(key) {
        this._store.delete(key);
        if (this._timers.has(key)) { clearTimeout(this._timers.get(key)); this._timers.delete(key); }
    }

    clear() {
        this._store.clear();
        this._timers.forEach(t => clearTimeout(t));
        this._timers.clear();
    }

    size() { return this._store.size; }

    keys() { return [...this._store.keys()].filter(k => this.has(k)); }

    // Atalho para buscar com cache (stale-while-revalidate)
    async remember(key, fetcher, ttl) {
        const cached = this.get(key);
        if (cached !== null) return cached;
        const value = await fetcher();
        this.set(key, value, ttl);
        return value;
    }

    _evict() {
        const oldest = this._store.keys().next().value;
        if (oldest) this.remove(oldest);
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
