export default class ServiceContainer {
    constructor() {
        this._services = new Map();
        this._factories = new Map();
        this._instances = new Map();
        this._aliases = new Map();
        this._tags = new Map();
        this._decorators = new Map();
        this._hooks = { beforeRegister: [], afterRegister: [], beforeGet: [], afterGet: [], beforeDestroy: [] };
        this._resolved = new Set();
        this._resolving = new Set();
        this._frozen = false;
        this._id = 0;
    }

    register(name, instance, options = {}) {
        if (this._frozen) { console.warn(`[ServiceContainer] ${name} — congelado`); return this; }
        if (this._services.has(name) || this._factories.has(name)) { console.warn(`[ServiceContainer] ${name} já registrado`); return this; }

        this._runHooks('beforeRegister', { name, instance, options });

        const entry = {
            name, instance,
            options: { singleton: true, lazy: false, tags: [], ...options },
            initialized: false, id: ++this._id
        };

        this._services.set(name, entry);
        if (entry.options.tags?.length) for (const tag of entry.options.tags) this._addTag(tag, name);

        this._runHooks('afterRegister', { name, instance, options });
        return this;
    }

    registerFactory(name, factory, options = {}) {
        if (this._frozen) { console.warn(`[ServiceContainer] factory ${name} — congelado`); return this; }
        if (this._services.has(name) || this._factories.has(name)) { console.warn(`[ServiceContainer] ${name} já registrado`); return this; }

        const entry = { name, factory, options: { singleton: true, tags: [], ...options }, instance: null, id: ++this._id };
        this._factories.set(name, entry);
        if (entry.options.tags?.length) for (const tag of entry.options.tags) this._addTag(tag, name);
        return this;
    }

    alias(alias, target) {
        if (this._aliases.has(alias)) { console.warn(`[ServiceContainer] alias ${alias} já existe`); return this; }
        this._aliases.set(alias, target);
        return this;
    }

    get(name) {
        this._runHooks('beforeGet', { name });
        const resolvedName = this._aliases.get(name) || name;

        if (this._instances.has(resolvedName)) {
            const instance = this._instances.get(resolvedName);
            this._runHooks('afterGet', { name, instance });
            return instance;
        }

        if (this._resolving.has(resolvedName)) throw new Error(`[ServiceContainer] Dependência circular: "${resolvedName}"`);
        this._resolving.add(resolvedName);

        let instance = null;
        if (this._services.has(resolvedName)) instance = this._resolveService(resolvedName);
        else if (this._factories.has(resolvedName)) instance = this._resolveFactory(resolvedName);
        else console.error(`[ServiceContainer] "${name}" não encontrado`);

        this._resolving.delete(resolvedName);

        if (instance && this._decorators.has(resolvedName)) {
            for (const decorator of this._decorators.get(resolvedName)) instance = decorator(instance, this);
        }

        this._runHooks('afterGet', { name, instance });
        return instance;
    }

    _resolveService(name) {
        const entry = this._services.get(name);
        if (entry.options.lazy && !entry.initialized) {
            entry.instance.init?.();
            entry.initialized = true;
        }
        if (entry.options.singleton) { this._instances.set(name, entry.instance); this._resolved.add(name); return entry.instance; }
        return entry.instance;
    }

    _resolveFactory(name) {
        const entry = this._factories.get(name);
        if (entry.options.singleton) {
            if (!entry.instance) { entry.instance = entry.factory(this); this._instances.set(name, entry.instance); this._resolved.add(name); }
            return entry.instance;
        }
        return entry.factory(this);
    }

    has(name) { return this._services.has(this._aliases.get(name) || name) || this._factories.has(this._aliases.get(name) || name); }
    isResolved(name) { return this._instances.has(this._aliases.get(name) || name); }

    remove(name) {
        const resolvedName = this._aliases.get(name) || name;
        this._runHooks('beforeDestroy', { name: resolvedName });

        if (this._instances.has(resolvedName)) {
            const instance = this._instances.get(resolvedName);
            instance.destroy?.();
            this._instances.delete(resolvedName);
        }
        this._services.delete(resolvedName);
        this._factories.delete(resolvedName);
        this._resolved.delete(resolvedName);
        for (const [tag, services] of this._tags) services.delete(resolvedName);
    }

    invoke(fn, dependencies = []) {
        const resolved = dependencies.map(dep => this.get(dep));
        const missing = dependencies.filter((dep, i) => resolved[i] === null);
        if (missing.length) { console.error(`[ServiceContainer] invoke: dependências não encontradas: ${missing.join(', ')}`); return null; }
        return fn(...resolved);
    }

    getByTag(tag) { return this._tags.has(tag) ? Array.from(this._tags.get(tag)).map(n => this.get(n)).filter(Boolean) : []; }
    hasTag(tag) { return this._tags.has(tag) && this._tags.get(tag).size > 0; }

    decorate(name, fn) {
        if (!this._decorators.has(name)) this._decorators.set(name, []);
        this._decorators.get(name).push(fn);
        return this;
    }

    on(event, callback) { if (this._hooks[event]) this._hooks[event].push(callback); return this; }
    _runHooks(event, data) { if (this._hooks[event]) for (const hook of this._hooks[event]) try { hook(data, this); } catch (e) { console.error(`[ServiceContainer] hook ${event} error`, e); } }

    freeze() { this._frozen = true; return this; }
    unfreeze() { this._frozen = false; return this; }
    isFrozen() { return this._frozen; }

    _addTag(tag, name) {
        if (!this._tags.has(tag)) this._tags.set(tag, new Set());
        this._tags.get(tag).add(name);
    }

    stats() {
        return {
            services: this._services.size, factories: this._factories.size,
            instances: this._instances.size, aliases: this._aliases.size,
            tags: this._tags.size, resolved: this._resolved.size, frozen: this._frozen
        };
    }

    getNames() { return [...Array.from(this._services.keys()), ...Array.from(this._factories.keys())]; }

    clear() {
        for (const [name, instance] of this._instances) instance.destroy?.();
        this._services.clear();
        this._factories.clear();
        this._instances.clear();
        this._aliases.clear();
        this._tags.clear();
        this._decorators.clear();
        this._resolved.clear();
        this._resolving.clear();
        this._frozen = false;
    }
}
