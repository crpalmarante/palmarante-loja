export default class EventBus {
    constructor() {
        this._listeners = new Map();
        this._wildcards = new Map();
        this._middlewares = new Map();
        this._history = [];
        this._maxHistory = 100;
        this._stats = new Map();
        this._id = 0;
        this._enabled = true;
    }

    on(event, callback, context = null, options = {}) {
        if (!this._enabled || typeof callback !== 'function') return () => {};

        if (event.includes('*')) return this._onWildcard(event, callback, context, options);

        if (!this._listeners.has(event)) this._listeners.set(event, new Map());

        const id = ++this._id;
        this._listeners.get(event).set(id, {
            id, callback, context,
            priority: options.priority || 0,
            once: options.once || false,
            async: options.async || false
        });

        if (!this._stats.has(event)) this._stats.set(event, { emitted: 0, subscribers: 0 });
        this._stats.get(event).subscribers++;

        return () => this.off(event, callback);
    }

    once(event, callback, context = null) {
        return this.on(event, callback, context, { once: true });
    }

    off(event, callback) {
        if (!this._listeners.has(event)) return;
        const listeners = this._listeners.get(event);
        for (const [id, entry] of listeners) {
            if (entry.callback === callback) {
                listeners.delete(id);
                if (this._stats.has(event)) this._stats.get(event).subscribers--;
                return;
            }
        }
    }

    offAll(event = null) {
        if (event) { this._listeners.delete(event); this._stats.delete(event); }
        else { this._listeners.clear(); this._stats.clear(); }
    }

    emit(event, payload = {}, options = {}) {
        if (!this._enabled) return;

        const timestamp = Date.now();
        const envelope = { event, payload, timestamp, id: `${event}_${timestamp}_${++this._id}` };

        if (options.history !== false) this._addToHistory(envelope);

        if (!this._stats.has(event)) this._stats.set(event, { emitted: 0, subscribers: 0 });
        this._stats.get(event).emitted++;

        if (!this._runMiddlewares(event, envelope)) return;

        this._dispatch(event, envelope);
        this._dispatchWildcards(event, envelope);
    }

    has(event) {
        return this._listeners.has(event) && this._listeners.get(event).size > 0;
    }

    listeners(event) {
        return this._listeners.has(event) ? Array.from(this._listeners.get(event).values()) : [];
    }

    events() { return Array.from(this._listeners.keys()); }

    stats(event = null) {
        if (event) return this._stats.get(event) || { emitted: 0, subscribers: 0 };
        const result = {};
        for (const [ev, st] of this._stats) result[ev] = st;
        return result;
    }

    history(limit = 10) { return this._history.slice(-limit); }

    use(patternOrFn, fn) {
        if (typeof patternOrFn === 'function') {
            fn = patternOrFn;
            patternOrFn = '*';
        }
        if (!this._middlewares.has(patternOrFn)) this._middlewares.set(patternOrFn, []);
        this._middlewares.get(patternOrFn).push(fn);
        return this;
    }

    enable() { this._enabled = true; }
    disable() { this._enabled = false; }
    clearHistory() { this._history = []; }

    destroy() {
        this._listeners.clear();
        this._wildcards.clear();
        this._middlewares.clear();
        this._history = [];
        this._stats.clear();
        this._enabled = false;
    }

    _dispatch(event, envelope) {
        if (!this._listeners.has(event)) return;
        const listeners = Array.from(this._listeners.get(event).values())
            .sort((a, b) => b.priority - a.priority);

        for (const entry of listeners) {
            try {
                if (entry.async) {
                    setTimeout(() => entry.callback.call(entry.context || this, envelope.payload, envelope), 0);
                } else {
                    entry.callback.call(entry.context || this, envelope.payload, envelope);
                }
                if (entry.once) this._listeners.get(event).delete(entry.id);
            } catch (e) {
                console.error(`[EventBus] Error in listener for "${event}":`, e);
            }
        }
    }

    _dispatchWildcards(event, envelope) {
        for (const [pattern, entries] of this._wildcards) {
            if (this._matchWildcard(event, pattern)) {
                for (const [id, entry] of entries) {
                    try {
                        entry.callback.call(entry.context || this, envelope.payload, envelope);
                        if (entry.once) entries.delete(id);
                    } catch (e) {
                        console.error(`[EventBus] Wildcard error: ${pattern}`, e);
                    }
                }
            }
        }
    }

    _matchWildcard(event, pattern) {
        return new RegExp('^' + pattern.replace(/\*/g, '.*') + '$').test(event);
    }

    _onWildcard(pattern, callback, context, options) {
        if (!this._wildcards.has(pattern)) this._wildcards.set(pattern, new Map());
        const id = ++this._id;
        this._wildcards.get(pattern).set(id, { id, callback, context, priority: options.priority || 0, once: options.once || false });
        return () => { if (this._wildcards.has(pattern)) this._wildcards.get(pattern).delete(id); };
    }

    _addToHistory(envelope) {
        this._history.push(envelope);
        if (this._history.length > this._maxHistory) this._history.shift();
    }

    _runMiddlewares(event, envelope) {
        for (const [pattern, middlewares] of this._middlewares) {
            if (pattern !== '*' && !this._matchWildcard(event, pattern)) continue;
            for (const middleware of middlewares) {
                try {
                    if (middleware(envelope.payload, envelope, this) === false) return false;
                } catch (e) {
                    console.error(`[EventBus] Middleware error: ${event}`, e);
                }
            }
        }
        return true;
    }
}
