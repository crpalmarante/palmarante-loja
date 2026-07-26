export default class Factory {
    constructor() {
        this._blueprints = new Map();
    }

    define(name, builder) {
        if (this._blueprints.has(name)) { console.warn(`[Factory] "${name}" já definido`); return this; }
        this._blueprints.set(name, builder);
        return this;
    }

    create(name, ...args) {
        const blueprint = this._blueprints.get(name);
        if (!blueprint) { console.error(`[Factory] "${name}" não encontrado`); return null; }
        return blueprint(...args);
    }

    has(name) { return this._blueprints.has(name); }

    remove(name) { this._blueprints.delete(name); }

    names() { return Array.from(this._blueprints.keys()); }

    clear() { this._blueprints.clear(); }

    stats() { return { blueprints: this._blueprints.size }; }
}
