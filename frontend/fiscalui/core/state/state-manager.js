export default class StateManager {
    constructor() {
        this._state = {};
        this._reducers = new Map();
        this._subscribers = new Set();
        this._middlewares = [];
        this._history = [];
        this._maxHistory = 50;
        this._enabled = true;
        this._id = 0;
        this._batchDepth = 0;
        this._pendingSubscribers = new Set();
        this._lastAction = null;
        this._lastPrevState = null;
    }

    getState() { return this._state; }

    getSlice(key) { return key ? this._state[key] : this._state; }

    addReducer(slice, reducer) {
        if (typeof reducer !== 'function') { console.error(`[StateManager] addReducer(${slice}): must be a function`); return this; }
        if (this._reducers.has(slice)) console.warn(`[StateManager] reducer "${slice}" substituindo`);

        this._reducers.set(slice, reducer);
        if (!(slice in this._state)) this._state[slice] = reducer(undefined, { type: '__init__' });
        return this;
    }

    addReducers(reducers) { for (const [slice, reducer] of Object.entries(reducers)) this.addReducer(slice, reducer); return this; }

    hasReducer(slice) { return this._reducers.has(slice); }

    dispatch(action) {
        if (!this._enabled || !action?.type) return action;

        const prevState = this._state;
        const enhancedDispatch = this._applyMiddlewares(action, prevState);
        if (enhancedDispatch === false) return action;

        this._id++;
        const nextState = this._computeNextState(prevState, action);
        if (nextState === prevState) return action;

        this._state = nextState;

        if (this._maxHistory > 0) {
            this._history.push({ id: this._id, action: { type: action.type, payload: action.payload }, prevState, nextState, timestamp: Date.now() });
            if (this._history.length > this._maxHistory) this._history.shift();
        }

        this._notify(action, prevState);
        return action;
    }

    _computeNextState(prevState, action) {
        let hasChanged = false;
        const nextState = {};
        for (const [slice, reducer] of this._reducers) {
            const nextSlice = reducer(prevState[slice], action);
            if (nextSlice !== prevState[slice]) hasChanged = true;
            nextState[slice] = nextSlice;
        }
        for (const key of Object.keys(prevState)) {
            if (!this._reducers.has(key)) nextState[key] = prevState[key];
        }
        return hasChanged ? nextState : prevState;
    }

    subscribe(callback) {
        if (typeof callback !== 'function') return () => {};
        this._subscribers.add(callback);
        return () => this._subscribers.delete(callback);
    }

    watch(slice, callback) {
        if (typeof callback !== 'function') return () => {};
        let previousValue = this._state[slice];
        const wrapped = (action, prevState) => {
            const currentValue = this._state[slice];
            if (currentValue !== previousValue) { callback(currentValue, previousValue, action); previousValue = currentValue; }
        };
        this._subscribers.add(wrapped);
        return () => this._subscribers.delete(wrapped);
    }

    watchPath(path, callback) {
        const keys = path.split('.');
        if (!callback) return () => {};
        let previousValue = this._resolvePath(this._state, keys);
        const wrapped = () => {
            const currentValue = this._resolvePath(this._state, keys);
            if (currentValue !== previousValue) { callback(currentValue, previousValue); previousValue = currentValue; }
        };
        this._subscribers.add(wrapped);
        return () => this._subscribers.delete(wrapped);
    }

    unsubscribe(callback) { this._subscribers.delete(callback); }
    unsubscribeAll() { this._subscribers.clear(); }

    batch(callback) {
        this._batchDepth++;
        try { callback(); }
        finally {
            this._batchDepth--;
            if (this._batchDepth === 0) this._flushBatch();
        }
    }

    _flushBatch() {
        for (const subscriber of this._pendingSubscribers) try { subscriber(this._lastAction, this._lastPrevState); } catch (e) { console.error('[StateManager] batch error', e); }
        this._pendingSubscribers.clear();
    }

    use(middleware) {
        if (typeof middleware === 'function') this._middlewares.push(middleware);
        return this;
    }

    _applyMiddlewares(action, prevState) {
        if (this._middlewares.length === 0) return action;
        let result = action;
        for (const middleware of this._middlewares) {
            try {
                const returned = middleware({ action: result, prevState, getState: () => this._state, dispatch: (act) => this.dispatch(act), next: (act) => { result = act; } });
                if (returned === false) return false;
                if (returned && returned !== result) result = returned;
            } catch (e) { console.error('[StateManager] middleware error', e); }
        }
        return result;
    }

    select(selector) {
        if (typeof selector === 'function') return selector(this._state);
        if (typeof selector === 'string') return this.getSlice(selector);
        return this._state;
    }

    resetState(newState = {}) {
        const prevState = this._state;
        this._state = { ...newState };
        this._notify({ type: 'state/reset' }, prevState);
        return this;
    }

    resetSlice(slice) {
        const prevState = this._state;
        if (this._reducers.has(slice)) this._state = { ...this._state, [slice]: this._reducers.get(slice)(undefined, { type: '__init__' }) };
        this._notify({ type: `state/reset/${slice}` }, prevState);
        return this;
    }

    enable() { this._enabled = true; }
    disable() { this._enabled = false; }
    clearHistory() { this._history = []; }
    setMaxHistory(max) { this._maxHistory = max; if (this._history.length > max) this._history = this._history.slice(-max); }

    history(limit = 10) { return this._history.slice(-limit); }
    getActionCount() { return this._id; }
    getReducerNames() { return Array.from(this._reducers.keys()); }

    stats() {
        return {
            slices: this._reducers.size, subscribers: this._subscribers.size,
            middlewares: this._middlewares.length, totalActions: this._id,
            historyLength: this._history.length, enabled: this._enabled
        };
    }

    destroy() {
        this._subscribers.clear();
        this._reducers.clear();
        this._middlewares = [];
        this._history = [];
        this._state = {};
        this._enabled = false;
    }

    _notify(action, prevState) {
        if (this._batchDepth > 0) {
            this._lastAction = action;
            this._lastPrevState = prevState;
            for (const sub of this._subscribers) this._pendingSubscribers.add(sub);
            return;
        }
        for (const subscriber of this._subscribers) try { subscriber(action, prevState); } catch (e) { console.error('[StateManager] subscriber error', e); }
    }

    _resolvePath(obj, keys) {
        let current = obj;
        for (const key of keys) { if (current == null) return undefined; current = current[key]; }
        return current;
    }
}
