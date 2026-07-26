import { createElement, removeElement } from '../../utils/dom/dom.js';

export default class UIComponent {
    constructor(options = {}) {
        this._options = { ...options };
        this._element = null;
        this._children = [];
        this._listeners = [];
        this._watchers = [];
        this._state = {};
        this._initialized = false;
        this._mounted = false;
    }

    get element() { return this._element; }
    get options() { return { ...this._options }; }
    get isMounted() { return this._mounted; }
    get isInitialized() { return this._initialized; }

    setState(state) {
        const prev = { ...this._state };
        this._state = { ...this._state, ...state };
        this.onStateChange(this._state, prev);
    }

    onStateChange(state, prev) {}

    create() {
        if (this._initialized) return;
        this._initialized = true;
        this.onCreate();
        return this;
    }

    onCreate() {}

    init() {
        this.create();
        if (!this._element) this._element = this.template();
        if (typeof this._element === 'string') {
            const wrapper = document.createElement('div');
            wrapper.innerHTML = this._element.trim();
            this._element = wrapper.firstChild;
        }
        this.onInit();
        this._bindEvents();
        return this;
    }

    onInit() {}

    render(data) {
        if (data !== undefined) this._state = { ...this._state, ...data };
        this.onRender();
        return this;
    }

    onRender() {}

    update(data) {
        const prev = { ...this._state };
        this._state = { ...this._state, ...data };
        this.onUpdate(this._state, prev);
        return this;
    }

    onUpdate(state, prev) {}

    mount(target) {
        if (this._mounted) return;
        const el = typeof target === 'string' ? document.querySelector(target) : target;
        if (!el) { console.error('[UIComponent] mount target not found'); return this; }
        el.appendChild(this._element);
        this._mounted = true;
        this.onMount();
        return this;
    }

    onMount() {}

    unmount() {
        if (!this._mounted || !this._element?.parentNode) return this;
        this._element.parentNode.removeChild(this._element);
        this._mounted = false;
        this.onUnmount();
        return this;
    }

    onUnmount() {}

    template() {
        return '<div></div>';
    }

    addChild(component, target) {
        if (!component?.element) return;
        this._children.push(component);
        if (target) component.mount(target);
        else this._element?.appendChild(component.element);
    }

    removeChild(component) {
        const idx = this._children.indexOf(component);
        if (idx >= 0) {
            component.destroy();
            this._children.splice(idx, 1);
        }
    }

    on(event, callback) {
        const unsubscribe = this._getEventBus()?.on(event, callback, this) || (() => {});
        this._listeners.push(unsubscribe);
        return unsubscribe;
    }

    emit(event, payload = {}) {
        this._getEventBus()?.emit(event, { source: this.constructor.name, ...payload });
    }

    watch(slice, callback) {
        const unsubscribe = this._getStateManager()?.watch(slice, callback) || (() => {});
        this._watchers.push(unsubscribe);
        return unsubscribe;
    }

    query(selector) { return this._element?.querySelector(selector); }
    queryAll(selector) { return Array.from(this._element?.querySelectorAll(selector) || []); }

    show() { if (this._element) this._element.style.display = ''; }
    hide() { if (this._element) this._element.style.display = 'none'; }
    toggle() { if (this._element) this._element.style.display = this._element.style.display === 'none' ? '' : 'none'; }

    destroy() {
        this.onDestroy();
        this._listeners.forEach(unsub => unsub());
        this._watchers.forEach(unsub => unsub());
        this._children.forEach(child => child.destroy());
        this._children = [];
        this._listeners = [];
        this._watchers = [];
        if (this._element?.parentNode) removeElement(this._element);
        this._element = null;
        this._initialized = false;
        this._mounted = false;
    }

    onDestroy() {}

    _bindEvents() {}

    _getEventBus() {
        return this._options?.eventBus || (typeof FiscalUI !== 'undefined' ? FiscalUI.events : null);
    }

    _getStateManager() {
        return this._options?.state || (typeof FiscalUI !== 'undefined' ? FiscalUI.state : null);
    }
}
