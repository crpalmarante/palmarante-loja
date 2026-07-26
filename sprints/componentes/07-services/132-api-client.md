# FiscalUI Framework

## Documento 132 — API Client

**Nível 7 — Services**

**Versão 1.0**

Cliente HTTP com suporte a interceptadores, cache, retry e serialização.

---

```js
class ApiClient {
    constructor(options = {}) {
        this.baseURL = options.baseURL || '';
        this.defaults = {
            headers: { 'Content-Type': 'application/json', ...options.headers },
            timeout: options.timeout || 30000,
            ...options.defaults
        };
        this._interceptors = { request: [], response: [] };
        this._cache = new Map();
        this._cacheTTL = options.cacheTTL || 60000;
    }

    async request(config) {
        config = { ...this.defaults, ...config, headers: { ...this.defaults.headers, ...config.headers } };
        config.url = config.url?.startsWith('http') ? config.url : `${this.baseURL}${config.url || ''}`;

        for (const interceptor of this._interceptors.request) {
            config = await interceptor(config);
        }

        if (config.method?.toLowerCase() === 'get' && config.cache !== false) {
            const cached = this._getCache(config.url, config.params);
            if (cached) return cached;
        }

        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), config.timeout);
            config.signal = controller.signal;

            const response = await fetch(config.url, {
                method: config.method || 'GET',
                headers: config.headers,
                body: config.body ? JSON.stringify(config.body) : undefined,
                signal: config.signal
            });

            clearTimeout(timeoutId);

            let data;
            const contentType = response.headers.get('content-type') || '';
            if (contentType.includes('application/json')) data = await response.json();
            else if (contentType.includes('blob') || config.responseType === 'blob') data = await response.blob();
            else data = await response.text();

            const result = { status: response.status, statusText: response.statusText, headers: response.headers, data };

            if (!response.ok) throw new ApiError(result);

            for (const interceptor of this._interceptors.response) {
                await interceptor(result);
            }

            if (config.method?.toLowerCase() === 'get' && config.cache !== false) {
                this._setCache(config.url, config.params, result);
            }

            return result;
        } catch (err) {
            if (err instanceof ApiError) throw err;
            throw new ApiError({ status: 0, statusText: err.name === 'AbortError' ? 'Timeout' : 'Network Error', data: null });
        }
    }

    get(url, config) { return this.request({ ...config, method: 'GET', url }); }
    post(url, body, config) { return this.request({ ...config, method: 'POST', url, body }); }
    put(url, body, config) { return this.request({ ...config, method: 'PUT', url, body }); }
    patch(url, body, config) { return this.request({ ...config, method: 'PATCH', url, body }); }
    delete(url, config) { return this.request({ ...config, method: 'DELETE', url }); }

    addRequestInterceptor(fn) { this._interceptors.request.push(fn); }
    addResponseInterceptor(fn) { this._interceptors.response.push(fn); }

    invalidateCache(pattern) {
        const regex = pattern ? new RegExp(pattern) : null;
        for (const key of this._cache.keys()) {
            if (!regex || regex.test(key)) this._cache.delete(key);
        }
    }

    clearCache() { this._cache.clear(); }

    _getCache(url, params) {
        const key = this._cacheKey(url, params);
        const entry = this._cache.get(key);
        if (entry && Date.now() - entry.timestamp < this._cacheTTL) return entry.data;
        if (entry) this._cache.delete(key);
        return null;
    }

    _setCache(url, params, data) {
        const key = this._cacheKey(url, params);
        this._cache.set(key, { data, timestamp: Date.now() });
    }

    _cacheKey(url, params) { return `${url}?${JSON.stringify(params || {})}`; }
}

class ApiError extends Error {
    constructor(response) {
        super(`Erro ${response.status}: ${response.statusText}`);
        this.name = 'ApiError';
        this.status = response.status;
        this.statusText = response.statusText;
        this.data = response.data;
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
