# FiscalUI Framework

## Documento 115 — HTTP Client

**Nível 7 — Services**

**Versão 1.0**

Cliente HTTP com suporte a interceptors, retry, timeout, cache e serialização automática.

---

```js
class HttpClient {
    constructor(options = {}) {
        this.baseURL = options.baseURL || '';
        this.headers = options.headers || {};
        this.timeout = options.timeout || 30000;
        this.retry = options.retry || 0;
        this.interceptors = { request: [], response: [] };
    }

    async request(config) {
        config = { method: 'GET', headers: { ...this.headers }, ...config };
        config.url = this.baseURL + config.url;

        for (const interceptor of this.interceptors.request) {
            config = await interceptor(config) || config;
        }

        let lastError;
        for (let attempt = 0; attempt <= this.retry; attempt++) {
            try {
                const controller = new AbortController();
                const timer = setTimeout(() => controller.abort(), this.timeout);
                config.signal = controller.signal;

                if (config.body && typeof config.body === 'object') {
                    config.body = JSON.stringify(config.body);
                    config.headers['Content-Type'] = config.headers['Content-Type'] || 'application/json';
                }

                const response = await fetch(config.url, config);
                clearTimeout(timer);

                let data = null;
                const ct = response.headers.get('content-type') || '';
                if (ct.includes('application/json')) data = await response.json();
                else if (ct.includes('text/')) data = await response.text();
                else data = await response.blob();

                const result = { status: response.status, ok: response.ok, data, headers: response.headers };

                for (const interceptor of this.interceptors.response) {
                    await interceptor(result);
                }

                if (!response.ok) throw new HttpError(result.status, result.data || 'Erro HTTP', result);
                return result;
            } catch (err) {
                lastError = err;
                if (attempt < this.retry) await new Promise(r => setTimeout(r, 1000 * (attempt + 1)));
            }
        }
        throw lastError;
    }

    get(url, config) { return this.request({ ...config, url, method: 'GET' }); }
    post(url, body, config) { return this.request({ ...config, url, method: 'POST', body }); }
    put(url, body, config) { return this.request({ ...config, url, method: 'PUT', body }); }
    patch(url, body, config) { return this.request({ ...config, url, method: 'PATCH', body }); }
    delete(url, config) { return this.request({ ...config, url, method: 'DELETE' }); }

    addRequestInterceptor(fn) { this.interceptors.request.push(fn); }
    addResponseInterceptor(fn) { this.interceptors.response.push(fn); }
}

class HttpError extends Error {
    constructor(status, message, response) {
        super(message);
        this.name = 'HttpError';
        this.status = status;
        this.response = response;
    }
}
```

```css
/* Sem CSS — service-only */
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
