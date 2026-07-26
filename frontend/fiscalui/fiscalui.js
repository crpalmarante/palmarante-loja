import EventBus from './core/event-bus/event-bus.js';
import ServiceContainer from './core/di/service-container.js';
import StateManager from './core/state/state-manager.js';
import Router from './core/router/router.js';
import UIComponent from './core/component/ui-component.js';
import Scheduler from './core/scheduler/scheduler.js';
import Registry from './core/registry/registry.js';
import Factory from './core/factory/factory.js';

const FiscalUI = {
    version: '1.0.0',
    events: null,
    container: null,
    state: null,
    router: null,
    component: UIComponent,
    scheduler: null,
    registry: null,
    factory: null,

    config: {
        debug: false,
        mode: 'hash',
        basePath: ''
    },

    init(options = {}) {
        Object.assign(this.config, options);

        this.events = new EventBus();
        this.container = new ServiceContainer();
        this.state = new StateManager();
        this.router = new Router();
        this.scheduler = new Scheduler();
        this.registry = new Registry();
        this.factory = new Factory();

        this.events.emit('framework:init', { version: this.version });

        if (this.config.debug) console.log('[FiscalUI] Inicializado', this.version);

        this.events.emit('framework:ready', { version: this.version });

        return this;
    },

    plugin(plugin) {
        if (typeof plugin === 'function') plugin(this);
        return this;
    },

    log(level, message, error = null) {
        if (this.config.debug || level === 'error') {
            const prefix = '[FiscalUI]';
            if (level === 'error') console.error(prefix, message, error || '');
            else if (level === 'warn') console.warn(prefix, message);
            else console.log(prefix, message);
        }
    },

    destroy() {
        this.events?.emit('framework:destroy');
        this.scheduler?.destroy();
        this.events?.destroy();
        this.state?.destroy();
        this.router?.destroy();
        this.container?.clear();
        this.scheduler = null;
        this.events = null;
        this.state = null;
        this.router = null;
        this.container = null;
        this.registry = null;
        this.factory = null;
    }
};

if (typeof window !== 'undefined') window.FiscalUI = FiscalUI;

export default FiscalUI;
export { EventBus, ServiceContainer, StateManager, Router, UIComponent, Scheduler, Registry, Factory };
