# FiscalUI Framework

## Documento 118 — Storage

**Nível 7 — Services**

**Versão 1.0**

Serviço de armazenamento unificado com adaptadores para localStorage, sessionStorage e IndexedDB.

---

```js
class StorageService {
    constructor(options = {}) {
        this.adapter = options.adapter || 'local'; // local, session, indexeddb
        this.prefix = options.prefix || 'fiscalui_';
        this._adapters = {
            local: {
                get: (k) => { const v = localStorage.getItem(k); return v ? JSON.parse(v) : null; },
                set: (k, v) => localStorage.setItem(k, JSON.stringify(v)),
                remove: (k) => localStorage.removeItem(k),
                clear: () => localStorage.clear(),
                keys: () => Object.keys(localStorage)
            },
            session: {
                get: (k) => { const v = sessionStorage.getItem(k); return v ? JSON.parse(v) : null; },
                set: (k, v) => sessionStorage.setItem(k, JSON.stringify(v)),
                remove: (k) => sessionStorage.removeItem(k),
                clear: () => sessionStorage.clear(),
                keys: () => Object.keys(sessionStorage)
            }
        };
        this._db = null;
        if (this.adapter === 'indexeddb') this._initDB();
    }

    async _initDB() {
        this._db = await new Promise((resolve, reject) => {
            const req = indexedDB.open('FiscalUIStorage', 1);
            req.onupgradeneeded = () => req.result.createObjectStore('store');
            req.onsuccess = () => resolve(req.result);
            req.onerror = () => reject(req.error);
        });
    }

    _key(name) { return this.prefix + name; }

    async get(name) {
        const key = this._key(name);
        if (this.adapter === 'indexeddb' && this._db) {
            return await this._db.transaction('store', 'readonly').objectStore('store').get(key);
        }
        return this._adapters[this.adapter]?.get(key) ?? null;
    }

    async set(name, value) {
        const key = this._key(name);
        if (this.adapter === 'indexeddb' && this._db) {
            await this._db.transaction('store', 'readwrite').objectStore('store').put(value, key);
        } else {
            this._adapters[this.adapter]?.set(key, value);
        }
    }

    async remove(name) {
        const key = this._key(name);
        if (this.adapter === 'indexeddb' && this._db) {
            await this._db.transaction('store', 'readwrite').objectStore('store').delete(key);
        } else {
            this._adapters[this.adapter]?.remove(key);
        }
    }

    async clear() {
        if (this.adapter === 'indexeddb' && this._db) {
            await this._db.transaction('store', 'readwrite').objectStore('store').clear();
        } else {
            this._adapters[this.adapter]?.clear();
        }
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
