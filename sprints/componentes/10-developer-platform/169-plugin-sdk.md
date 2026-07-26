# FiscalUI Framework

## Documento 169 — Plugin SDK

**Nível 10 — Developer Platform**

**Versão 1.0**

SDK para desenvolvimento de plugins. Define contrato, hooks, lifecycle e API pública.

---

```js
// plugin.json — manifesto do plugin
{
  "name": "fiscalui-plugin-relatorio",
  "version": "1.0.0",
  "fiscalui": {
    "minVersion": "1.0.0",
    "type": "plugin"
  },
  "description": "Plugin de relatórios customizados",
  "author": "Dev Name",
  "license": "MIT",
  "hooks": {
    "onInit": "after-framework-init",
    "onRoute": "before-route-change",
    "onRender": "after-component-render"
  }
}
```

```js
// SDK base
class PluginSDK {
  constructor(pluginId, manifest) {
    this.id = pluginId;
    this.manifest = manifest;
    this._hooks = new Map();
    this._commands = [];
    this._components = [];
    this._services = [];
  }

  // Registrar hook no ciclo de vida do FiscalUI
  on(event, handler) {
    if (!this._hooks.has(event)) this._hooks.set(event, []);
    this._hooks.get(event).push(handler);
    return () => this.off(event, handler);
  }

  off(event, handler) {
    const handlers = this._hooks.get(event);
    if (handlers) this._hooks.set(event, handlers.filter(h => h !== handler));
  }

  getHooks() { return this._hooks; }

  // Registrar componente customizado
  registerComponent(name, componentClass) {
    this._components.push({ name, componentClass });
    Registry.register(name, componentClass);
  }

  // Registrar serviço
  registerService(name, serviceClass, deps = []) {
    this._services.push({ name, serviceClass, deps });
    ServiceContainer.register(name, serviceClass, { dependencies: deps });
  }

  // Adicionar comando à paleta
  addCommand(command) {
    this._commands.push(command);
    EventBus.emit('command:register', command);
  }

  // Acessar core do FiscalUI
  get fiscalUI() { return window.FiscalUI; }
  get eventBus() { return EventBus; }
  get registry() { return Registry; }
  get serviceContainer() { return ServiceContainer; }

  // API de internacionalização
  t(key, params) { return I18nService.t(key, params); }

  // API de configuração
  getConfig(key, defaultValue) { return ConfigService.get(`plugins.${this.id}.${key}`, defaultValue); }
  setConfig(key, value) { ConfigService.set(`plugins.${this.id}.${key}`, value); }

  // Logging
  log(...args) { LoggerService.info(`[Plugin:${this.id}]`, ...args); }
  warn(...args) { LoggerService.warn(`[Plugin:${this.id}]`, ...args); }
  error(...args) { LoggerService.error(`[Plugin:${this.id}]`, ...args); }

  // Ciclo de vida
  async activate() { EventBus.emit(`plugin:${this.id}:activated`, this); }
  async deactivate() { EventBus.emit(`plugin:${this.id}:deactivated`, this); }
  async destroy() {
    this._commands.forEach(cmd => EventBus.emit('command:unregister', cmd));
    this._components.forEach(({ name }) => Registry.unregister(name));
    this._services.forEach(({ name }) => ServiceContainer.remove(name));
  }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
