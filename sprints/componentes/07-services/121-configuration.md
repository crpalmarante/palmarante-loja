# FiscalUI Framework

## Documento 121 — Configuration

**Nível 7 — Services**

**Versão 1.0**

Serviço de configuração centralizada. Carrega de múltiplas fontes (JSON, ambiente, URL) com merge.

---

```js
class ConfigService {
    constructor(options = {}) {
        this._config = {};
        this._sources = options.sources || [];
        this._loaded = false;
    }

    async load() {
        this._config = {};
        for (const source of this._sources) {
            const data = await this._loadSource(source);
            this._merge(data);
        }
        this._loaded = true;
        return this._config;
    }

    async _loadSource(source) {
        if (typeof source === 'object') return source;
        if (typeof source === 'string') {
            if (source.startsWith('http')) {
                const res = await fetch(source);
                return res.json();
            }
            if (source.endsWith('.json')) {
                const res = await fetch(source);
                return res.json();
            }
        }
        return {};
    }

    _merge(data) {
        this._config = deepMerge(this._config, data);
    }

    get(key, defaultValue) {
        const keys = key.split('.');
        let val = this._config;
        for (const k of keys) {
            if (val === null || val === undefined) return defaultValue;
            val = val[k];
        }
        return val !== undefined ? val : defaultValue;
    }

    set(key, value) {
        const keys = key.split('.');
        let obj = this._config;
        for (let i = 0; i < keys.length - 1; i++) {
            if (!obj[keys[i]] || typeof obj[keys[i]] !== 'object') obj[keys[i]] = {};
            obj = obj[keys[i]];
        }
        obj[keys[keys.length - 1]] = value;
    }

    getAll() { return { ...this._config }; }

    isLoaded() { return this._loaded; }
}

function deepMerge(target, source) {
    const result = { ...target };
    for (const key of Object.keys(source)) {
        if (source[key] instanceof Object && target[key] instanceof Object && !Array.isArray(source[key])) {
            result[key] = deepMerge(target[key], source[key]);
        } else {
            result[key] = source[key];
        }
    }
    return result;
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
