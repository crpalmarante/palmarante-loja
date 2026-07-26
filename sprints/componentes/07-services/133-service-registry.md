# FiscalUI Framework

## Documento 133 — Service Registry

**Nível 7 — Services**

**Versão 1.0**

Registry central de serviços com lazy loading, dependências e ciclo de vida.

---

```js
class ServiceRegistry {
    constructor() {
        this._services = new Map();
        this._instances = new Map();
        this._lazyLoaders = new Map();
    }

    register(name, serviceClass, options = {}) {
        if (this._services.has(name)) throw new Error(`Serviço '${name}' já registrado`);
        this._services.set(name, { serviceClass, options });
    }

    registerLazy(name, loader, options = {}) {
        this._lazyLoaders.set(name, { loader, options });
    }

    async boot(...names) {
        const toBoot = names.length ? names : Array.from(this._services.keys());
        for (const name of toBoot) {
            if (!this._instances.has(name)) await this.resolve(name);
        }
    }

    async resolve(name) {
        if (this._instances.has(name)) return this._instances.get(name);

        const lazy = this._lazyLoaders.get(name);
        if (lazy) {
            const service = await lazy.loader();
            this.register(name, service, lazy.options);
            this._lazyLoaders.delete(name);
        }

        const entry = this._services.get(name);
        if (!entry) throw new Error(`Serviço '${name}' não registrado`);

        const { serviceClass, options } = entry;

        // Resolve dependências automaticamente
        const deps = options.dependencies || [];
        const resolvedDeps = await Promise.all(deps.map(d => this.resolve(d)));

        const instance = typeof serviceClass === 'function' && !this._isClass(serviceClass)
            ? serviceClass(...resolvedDeps)
            : new serviceClass(...resolvedDeps, options);

        if (instance.init && typeof instance.init === 'function') {
            await instance.init();
        }

        this._instances.set(name, instance);

        // Notifica listeners
        this._emit(`registered:${name}`, instance);

        return instance;
    }

    get(name) {
        const instance = this._instances.get(name);
        if (!instance) throw new Error(`Serviço '${name}' não foi inicializado. Chame resolve() primeiro.`);
        return instance;
    }

    has(name) { return this._services.has(name) || this._instances.has(name) || this._lazyLoaders.has(name); }

    async destroy(name) {
        const instance = this._instances.get(name);
        if (instance?.destroy && typeof instance.destroy === 'function') await instance.destroy();
        this._instances.delete(name);
    }

    async destroyAll() {
        for (const name of this._instances.keys()) await this.destroy(name);
        this._services.clear();
        this._lazyLoaders.clear();
    }

    list() {
        return {
            registered: Array.from(this._services.keys()),
            instantiated: Array.from(this._instances.keys()),
            lazy: Array.from(this._lazyLoaders.keys())
        };
    }

    _isClass(fn) {
        return typeof fn === 'function' && /^\s*class\s+/.test(fn.toString());
    }

    _emit(event, data) {
        document.dispatchEvent(new CustomEvent(`sr:${event}`, { detail: data }));
    }
}
```

```js
// Exemplo de uso:
// const registry = new ServiceRegistry();
// registry.register('config', ConfigService);
// registry.register('http', ApiClient, { dependencies: ['config'] });
// registry.registerLazy('heavy', () => import('./heavy-service.js'));
// await registry.boot('config', 'http');
// const config = registry.get('config');
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
