import EventBus from '../../core/event-bus/event-bus.js';

export default class Router {
    constructor() {
        this._routes = new Map();
        this._current = null;
        this._previous = null;
        this._history = [];
        this._maxHistory = 50;
        this._mode = 'hash';
        this._basePath = '';
        this._fallback = null;
        this._guards = { beforeEnter: [], beforeLeave: [] };
        this._listeners = [];
        this._events = null;
        this._initialized = false;
        this._transitioning = false;
        this._boundPopState = this._onPopState.bind(this);
    }

    setMode(mode) { if (mode === 'hash' || mode === 'history') this._mode = mode; return this; }
    setBasePath(path) { this._basePath = path.replace(/\/$/, ''); return this; }
    setFallback(route) { this._fallback = route; return this; }
    setEventBus(eventBus) { this._events = eventBus; return this; }

    addRoute(config) {
        if (!config?.path) { console.error('[Router] addRoute: path obrigatório'); return this; }
        const route = {
            path: config.path, name: config.name || config.path,
            component: config.component || null, module: config.module || null,
            meta: config.meta || {}, guards: config.guards || {},
            children: config.children || [], redirect: config.redirect || null,
            _regex: this._pathToRegex(config.path),
            _params: this._extractParamNames(config.path)
        };
        if (this._routes.has(route.name)) console.warn(`[Router] Rota "${route.name}" substituindo`);
        this._routes.set(route.name, route);
        return this;
    }

    addRoutes(routes) { for (const r of routes) this.addRoute(r); return this; }

    init() {
        if (this._initialized) return this;
        if (this._mode === 'hash') {
            window.addEventListener('hashchange', this._boundPopState);
            this._resolveInitialRoute(this._getHashPath() || '/');
        } else {
            window.addEventListener('popstate', this._boundPopState);
            this._resolveInitialRoute(window.location.pathname.replace(this._basePath, '') || '/');
        }
        this._initialized = true;
        return this;
    }

    _resolveInitialRoute(path) {
        const match = this._matchRoute(path);
        if (match) this._navigate(match, { replace: true, initial: true });
        else if (this._fallback) this._navigate(this._matchRoute(this._fallback.path), { replace: true, initial: true });
    }

    push(location) { return this._navigate(this._resolveLocation(location), { replace: false }); }
    replace(location) { return this._navigate(this._resolveLocation(location), { replace: true }); }
    go(delta) { window.history.go(delta); }
    back() { window.history.back(); }
    forward() { window.history.forward(); }

    get current() { return this._current ? { ...this._current } : null; }
    get previous() { return this._previous ? { ...this._previous } : null; }
    get path() { return this._current?.path || '/'; }
    get params() { return this._current ? { ...this._current.params } : {}; }
    get query() { return this._current ? { ...this._current.query } : {}; }
    get meta() { return this._current ? { ...this._current.meta } : {}; }
    get name() { return this._current?.name || null; }

    isActive(pathOrName) { return this._current?.name === pathOrName || this._current?.path === pathOrName; }

    beforeEnter(guard) { if (typeof guard === 'function') this._guards.beforeEnter.push(guard); return this; }
    beforeLeave(guard) { if (typeof guard === 'function') this._guards.beforeLeave.push(guard); return this; }

    href(location) {
        const path = typeof location === 'string' ? location : this._buildPath(location);
        return this._mode === 'hash' ? `#${this._basePath}${path}` : `${this._basePath}${path}`;
    }

    onNavigate(callback) { if (typeof callback === 'function') this._listeners.push(callback); return () => { const idx = this._listeners.indexOf(callback); if (idx >= 0) this._listeners.splice(idx, 1); }; }

    stats() {
        return { routes: this._routes.size, mode: this._mode, current: this._current?.path || null, historyLength: this._history.length, initialized: this._initialized };
    }

    history(limit = 10) { return this._history.slice(-limit).map(h => ({ path: h.path, name: h.name, timestamp: h.timestamp })); }

    destroy() {
        (this._mode === 'hash' ? window.removeEventListener('hashchange', this._boundPopState) : window.removeEventListener('popstate', this._boundPopState));
        this._routes.clear(); this._current = null; this._previous = null; this._history = [];
        this._guards = { beforeEnter: [], beforeLeave: [] }; this._initialized = false;
    }

    _navigate(match, options = {}) {
        if (!match) {
            if (this._fallback) return this._navigate(this._resolveLocation(this._fallback.path), { ...options, redirected: true });
            return false;
        }
        if (this._transitioning) return false;

        if (this._current && !this._runBeforeLeave(match)) return false;
        if (!this._runBeforeEnter(match)) return false;
        if (match.route.guards?.beforeEnter) {
            const result = match.route.guards.beforeEnter(match, this._current);
            if (result === false) return false;
            if (typeof result === 'string' || result?.path) return this.push(result);
        }

        this._transitioning = true;
        const prev = this._current;
        this._previous = prev ? { ...prev } : null;
        this._current = { path: match.path, name: match.route.name, params: match.params || {}, query: match.query || {}, meta: { ...match.route.meta }, hash: match.hash || '', timestamp: Date.now(), redirected: options.redirected || false };

        this._emitEvent('router:before-change', { route: this._current, previous: prev });
        this._updateURL(this._current, options);
        if (!options.initial) {
            this._history.push({ path: this._current.path, name: this._current.name, params: this._current.params, timestamp: this._current.timestamp });
            if (this._history.length > this._maxHistory) this._history.shift();
        }
        this._updateState(this._current);
        this._notifyListeners(this._current, prev);
        this._emitEvent('router:change', { route: this._current, previous: prev });
        this._transitioning = false;
        if (options.initial === false && this._current?.meta?.scrollToTop !== false) window.scrollTo({ top: 0, behavior: 'auto' });
        return true;
    }

    _resolveLocation(location) {
        if (typeof location === 'string') return this._resolveString(location);
        return this._resolveObject(location);
    }

    _resolveString(path) { return this._matchRoute(this._cleanPath(path)); }

    _resolveObject(location) {
        const route = this._routes.get(location.name);
        if (!route) { console.error(`[Router] Rota não encontrada: ${location.name}`); return null; }
        let path = route.path;
        if (location.params) for (const [k, v] of Object.entries(location.params)) path = path.replace(`:${k}`, encodeURIComponent(v));
        if (location.query) { const qs = this._buildQueryString(location.query); if (qs) path += `?${qs}`; }
        const match = this._matchRoute(path);
        if (match) { match.params = { ...match.params, ...location.params }; match.query = { ...match.query, ...location.query }; }
        return match;
    }

    _matchRoute(path) {
        const cleanPath = this._cleanPath(path);
        const [pathPart, queryPart] = cleanPath.includes('?') ? [cleanPath.split('?')[0], cleanPath.split('?')[1]] : [cleanPath, ''];
        const query = this._parseQueryString(queryPart);
        for (const [, route] of this._routes) {
            const match = pathPart.match(route._regex);
            if (match) {
                const params = {};
                for (let i = 0; i < route._params.length; i++) params[route._params[i]] = decodeURIComponent(match[i + 1] || '');
                if (route.children?.length) {
                    for (const child of route.children) {
                        const childPath = `${route.path}/${child.path}`.replace(/\/\//g, '/');
                        const childRegex = this._pathToRegex(childPath);
                        const childMatch = pathPart.match(childRegex);
                        if (childMatch) {
                            const childParams = {};
                            const childParamNames = this._extractParamNames(childPath);
                            for (let i = 0; i < childParamNames.length; i++) childParams[childParamNames[i]] = decodeURIComponent(childMatch[i + 1] || '');
                            return { path: childPath, route: { ...route, ...child, path: childPath }, params: { ...params, ...childParams }, query, hash: '' };
                        }
                    }
                }
                return { path, route, params, query, hash: '' };
            }
        }
        return null;
    }

    _updateURL(route, options) {
        const url = this._buildURL(route);
        const method = options.replace || options.initial ? 'replaceState' : 'pushState';
        if (this._mode === 'hash') window.history[method](null, '', `#${url}`);
        else window.history[method](null, '', `${this._basePath}${url}`);
    }

    _buildURL(route) {
        let url = route.path;
        if (route.query && Object.keys(route.query).length > 0) { const qs = this._buildQueryString(route.query); if (qs) url += `?${qs}`; }
        return url;
    }

    _buildPath(location) {
        const route = this._routes.get(location.name);
        if (!route) return '/';
        let path = route.path;
        if (location.params) for (const [k, v] of Object.entries(location.params)) path = path.replace(`:${k}`, encodeURIComponent(v));
        if (location.query) { const qs = this._buildQueryString(location.query); if (qs) path += `?${qs}`; }
        return path;
    }

    _onPopState() {
        const path = this._mode === 'hash' ? this._getHashPath() : window.location.pathname.replace(this._basePath, '');
        const match = this._matchRoute(path || '/');
        if (match) this._navigate(match, { replace: true });
        else if (this._fallback) this._navigate(this._matchRoute(this._fallback.path), { replace: true });
    }

    _getHashPath() { const hash = window.location.hash; return hash ? hash.replace('#', '') : '/'; }

    _runBeforeEnter(match) {
        for (const guard of this._guards.beforeEnter) {
            const result = guard(match, this._current);
            if (result === false) return false;
            if (typeof result === 'string' || result?.path) { this._navigate(this._resolveLocation(result), { replace: true }); return false; }
        }
        return true;
    }

    _runBeforeLeave(match) {
        for (const guard of this._guards.beforeLeave) { if (guard(match, this._current) === false) return false; }
        return true;
    }

    _updateState(route) {
        if (this._events) this._emitEvent('router:state', { route });
    }

    _notifyListeners(route, previous) { for (const cb of this._listeners) try { cb(route, previous); } catch (e) { console.error('[Router] listener error', e); } }

    _emitEvent(event, data) {
        if (this._events) this._events.emit(event, { source: 'Router', ...data });
    }

    _pathToRegex(path) { return new RegExp('^' + path.replace(/\//g, '\\/').replace(/:([^/]+)/g, '([^/]+)').replace(/\*/g, '.*') + '$'); }
    _extractParamNames(path) { const names = []; path.replace(/:([^/]+)/g, (_, n) => names.push(n)); return names; }

    _cleanPath(path) {
        if (this._basePath && path.startsWith(this._basePath)) path = path.slice(this._basePath.length);
        if (!path.startsWith('/')) path = `/${path}`;
        if (path.length > 1 && path.endsWith('/')) path = path.slice(0, -1);
        return path;
    }

    _parseQueryString(qs) {
        if (!qs) return {};
        return qs.split('&').reduce((acc, part) => { const [k, v] = part.split('='); if (k) acc[decodeURIComponent(k)] = v ? decodeURIComponent(v.replace(/\+/g, ' ')) : ''; return acc; }, {});
    }

    _buildQueryString(params) {
        const parts = [];
        for (const [k, v] of Object.entries(params)) if (v != null) parts.push(`${encodeURIComponent(k)}=${encodeURIComponent(v)}`);
        return parts.join('&');
    }
}
