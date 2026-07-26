export default class Registry {
    constructor() {
        this._items = new Map();
        this._aliases = new Map();
    }

    register(name, item) {
        if (this._items.has(name)) { console.warn(`[Registry] "${name}" já registrado`); return this; }
        this._items.set(name, item);
        return this;
    }

    get(name) { return this._items.get(this._aliases.get(name) || name) || null; }
    has(name) { return this._items.has(this._aliases.get(name) || name); }

    alias(alias, target) {
        if (this._aliases.has(alias)) { console.warn(`[Registry] alias "${alias}" já existe`); return this; }
        this._aliases.set(alias, target);
        return this;
    }

    remove(name) {
        const resolved = this._aliases.get(name) || name;
        this._items.delete(resolved);
        for (const [alias, target] of this._aliases) if (target === resolved) this._aliases.delete(alias);
    }

    names() { return Array.from(this._items.keys()); }

    count() { return this._items.size; }

    forEach(fn) { this._items.forEach((v, k) => fn(v, k)); }

    clear() { this._items.clear(); this._aliases.clear(); }

    stats() { return { items: this._items.size, aliases: this._aliases.size }; }
}
