# FiscalUI Framework

## Documento 137 — Helpers

**Nível 8 — Utilities**

**Versão 1.0**

Funções utilitárias genéricas: type checking, object/array manipulation, debounce/throttle, async helpers.

---

```js
const Helpers = {
    // ---- Type checking ----
    isObject: (v) => v !== null && typeof v === 'object' && !Array.isArray(v),
    isPlainObject: (v) => Object.prototype.toString.call(v) === '[object Object]',
    isString: (v) => typeof v === 'string',
    isNumber: (v) => typeof v === 'number' && !isNaN(v),
    isBoolean: (v) => typeof v === 'boolean',
    isFunction: (v) => typeof v === 'function',
    isArray: Array.isArray,
    isNull: (v) => v === null,
    isUndefined: (v) => v === undefined,
    isNil: (v) => v === null || v === undefined,
    isEmpty: (v) => v === null || v === undefined || (typeof v === 'string' && v.trim() === '') || (Array.isArray(v) && v.length === 0) || (Helpers.isObject(v) && Object.keys(v).length === 0),
    isPromise: (v) => v instanceof Promise || (Helpers.isObject(v) && typeof v.then === 'function'),

    // ---- Object ----
    pick: (obj, keys) => keys.reduce((acc, k) => { acc[k] = obj[k]; return acc; }, {}),
    omit: (obj, keys) => Object.keys(obj).filter(k => !keys.includes(k)).reduce((acc, k) => { acc[k] = obj[k]; return acc; }, {}),
    deepClone: (obj) => JSON.parse(JSON.stringify(obj)),
    merge: (...objs) => Object.assign({}, ...objs),
    deepMerge: (target, ...sources) => {
        const result = { ...target };
        for (const source of sources) {
            for (const key of Object.keys(source)) {
                if (Helpers.isPlainObject(source[key]) && Helpers.isPlainObject(result[key])) {
                    result[key] = Helpers.deepMerge(result[key], source[key]);
                } else result[key] = source[key];
            }
        }
        return result;
    },

    // ---- Array ----
    unique: (arr) => [...new Set(arr)],
    chunk: (arr, size) => { const res = []; for (let i = 0; i < arr.length; i += size) res.push(arr.slice(i, i + size)); return res; },
    flatten: (arr) => arr.reduce((acc, v) => acc.concat(Array.isArray(v) ? Helpers.flatten(v) : v), []),
    groupBy: (arr, key) => arr.reduce((acc, item) => { const k = typeof key === 'function' ? key(item) : item[key]; (acc[k] = acc[k] || []).push(item); return acc; }, {}),
    sortBy: (arr, key, desc = false) => [...arr].sort((a, b) => (a[key] > b[key] ? 1 : -1) * (desc ? -1 : 1)),
    shuffle: (arr) => { const a = [...arr]; for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; },

    // ---- Async ----
    debounce: (fn, delay = 300) => { let timer; return (...args) => { clearTimeout(timer); timer = setTimeout(() => fn(...args), delay); }; },
    throttle: (fn, limit = 300) => { let inThrottle; return (...args) => { if (!inThrottle) { fn(...args); inThrottle = true; setTimeout(() => inThrottle = false, limit); } }; },
    delay: (ms) => new Promise(resolve => setTimeout(resolve, ms)),
    retry: async (fn, retries = 3, delay = 1000) => { for (let i = 0; i < retries; i++) { try { return await fn(); } catch (e) { if (i === retries - 1) throw e; await Helpers.delay(delay); } } },

    // ---- Number ----
    clamp: (v, min, max) => Math.min(Math.max(v, min), max),
    randomInt: (min, max) => Math.floor(Math.random() * (max - min + 1)) + min,
    roundTo: (v, decimals) => Number(Math.round(v + 'e' + decimals) + 'e-' + decimals),

    // ---- String ----
    capitalize: (s) => s.charAt(0).toUpperCase() + s.slice(1),
    truncate: (s, len = 100) => s.length > len ? s.slice(0, len) + '...' : s,
    slugify: (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, ''),
    camelCase: (s) => s.replace(/[-_\s]+(.)/g, (_, c) => c.toUpperCase()).replace(/^(.)/, c => c.toLowerCase()),
    pascalCase: (s) => { const cc = Helpers.camelCase(s); return cc.charAt(0).toUpperCase() + cc.slice(1); },
    kebabCase: (s) => s.replace(/([A-Z])/g, '-$1').toLowerCase().replace(/^-/, '').replace(/[-_\s]+/g, '-'),
    parseQueryString: (s) => Object.fromEntries(new URLSearchParams(s)),
    toQueryString: (obj) => new URLSearchParams(obj).toString(),

    // ---- Misc ----
    uuid: () => 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => { const r = Math.random()*16|0; return (c==='x'?r:(r&0x3|0x8)).toString(16); }),
    generateId: (prefix = 'ui') => `${prefix}-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    sleep: (ms) => new Promise(r => setTimeout(r, ms)),
    noop: () => {},
    identity: (v) => v,
    pipe: (...fns) => (x) => fns.reduce((v, f) => f(v), x),
    memoize: (fn) => { const cache = new Map(); return (...args) => { const k = JSON.stringify(args); if (cache.has(k)) return cache.get(k); const r = fn(...args); cache.set(k, r); return r; }; }
};
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
