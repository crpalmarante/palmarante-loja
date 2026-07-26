# FiscalUI Framework

## Documento 016 — Plugin Engine

**Versão 1.0**

Este documento define o sistema de plugins do FiscalUI. Extensão do Framework sem modificar seu código fonte. Ciclo de vida de plugins, hooks, API pública, e segurança.

---

# Índice

1. Introdução
2. Filosofia
3. Arquitetura
4. API Pública
5. Ciclo de Vida
6. Hooks
7. Plugin API
8. Registro
9. Dependências
10. Segurança
11. Performance
12. Testes
13. Boas Práticas

---

# 1. Introdução

## 1.1 Propósito

O Plugin Engine permite estender o FiscalUI com funcionalidades adicionais sem modificar o core. Plugins podem registrar componentes, serviços, rotas, hooks, e estilos.

---

# 2. Filosofia

```
1. Core nunca depende de plugins — plugins sempre dependem do core
2. Plugins são isolados — um plugin não quebra o sistema
3. Plugins têm ciclo de vida gerenciado (register → init → enable → disable → destroy)
4. Plugins não podem acessar o core fora da API pública
5. Ordem de inicialização é gerenciada por dependências
```

---

# 3. Arquitetura

```
Plugin Engine
    │
    ├── Registry: Map<name, PluginInstance>
    ├── Hooks: Map<hookName, Set<callback>>
    ├── Dependencies: Graph de dependências entre plugins
    └── Sandbox: API limitada exposta ao plugin
```

---

# 4. API Pública

```js
class PluginEngine {
    constructor(framework = null) {
        this.framework = framework;
        this._plugins = new Map();
        this._hooks = new Map();
        this._initialized = false;
    }

    register(plugin) {
        if (this._plugins.has(plugin.name)) {
            this._log('warn', `Plugin "${plugin.name}" já registrado`);
            return this;
        }
        if (!plugin.name || !plugin.version) {
            this._log('error', 'Plugin precisa de name e version');
            return this;
        }

        this._plugins.set(plugin.name, {
            ...plugin,
            enabled: false,
            initialized: false
        });

        this._log('info', `Plugin registrado: ${plugin.name} v${plugin.version}`);
        return this;
    }

    init() {
        const order = this._resolveOrder();
        for (const name of order) {
            const plugin = this._plugins.get(name);
            try {
                if (plugin.init) {
                    plugin.init(this._createPluginAPI(plugin));
                }
                plugin.initialized = true;
                this._log('info', `Plugin inicializado: ${name}`);
            } catch (e) {
                this._log('error', `Plugin "${name}" falhou na inicialização`, e);
            }
        }
        this._initialized = true;
        return this;
    }

    enable(name) {
        const plugin = this._plugins.get(name);
        if (!plugin) { this._log('warn', `Plugin não encontrado: ${name}`); return this; }
        if (plugin.enabled) return this;

        try {
            if (plugin.enable) plugin.enable();
            plugin.enabled = true;
            this._log('info', `Plugin ativado: ${name}`);
        } catch (e) {
            this._log('error', `Plugin "${name}" falhou ao ativar`, e);
        }
        return this;
    }

    disable(name) {
        const plugin = this._plugins.get(name);
        if (!plugin) return this;
        if (!plugin.enabled) return this;

        try {
            if (plugin.disable) plugin.disable();
            plugin.enabled = false;
            this._log('info', `Plugin desativado: ${name}`);
        } catch (e) {
            this._log('error', `Plugin "${name}" falhou ao desativar`, e);
        }
        return this;
    }

    destroy(name) {
        const plugin = this._plugins.get(name);
        if (!plugin) return this;

        try {
            if (plugin.destroy) plugin.destroy();
            this._plugins.delete(name);
            this._log('info', `Plugin destruído: ${name}`);
        } catch (e) {
            this._log('error', `Plugin "${name}" falhou ao destruir`, e);
        }
        return this;
    }

    hook(name, callback) {
        if (!this._hooks.has(name)) this._hooks.set(name, new Set());
        this._hooks.get(name).add(callback);
        return () => this._hooks.get(name)?.delete(callback);
    }

    emit(name, data) {
        if (!this._hooks.has(name)) return;
        for (const cb of this._hooks.get(name)) {
            try { cb(data); } catch (e) {
                this._log('error', `Hook "${name}" error`, e);
            }
        }
    }

    isEnabled(name) {
        return this._plugins.get(name)?.enabled || false;
    }

    getPlugin(name) {
        return this._plugins.get(name) || null;
    }

    get enabled() {
        return Array.from(this._plugins.values()).filter(p => p.enabled);
    }

    _resolveOrder() {
        const names = Array.from(this._plugins.keys());
        const visited = new Set();
        const order = [];

        function visit(name, stack) {
            if (stack.has(name)) throw new Error(`Dependência circular: ${name}`);
            if (visited.has(name)) return;
            visited.add(name);
            stack.add(name);

            const plugin = this._plugins.get(name);
            if (plugin.dependsOn) {
                for (const dep of plugin.dependsOn) {
                    if (!this._plugins.has(dep)) {
                        this._log('warn', `Plugin "${name}" depende de "${dep}" que não existe`);
                        continue;
                    }
                    visit.call(this, dep, stack);
                }
            }

            stack.delete(name);
            order.push(name);
        }

        for (const name of names) {
            visit.call(this, name, new Set());
        }

        return order;
    }

    _createPluginAPI(plugin) {
        return {
            name: plugin.name,
            version: plugin.version,
            framework: this.framework,

            registerComponent: (name, component) => {
                if (this.framework?.component) {
                    this.framework.component.register(name, component);
                }
            },
            registerService: (name, service) => {
                if (this.framework?.container) {
                    this.framework.container.register(name, service);
                }
            },
            addRoute: (route) => {
                if (this.framework?.router) {
                    this.framework.router.addRoute(route);
                }
            },
            addReducer: (slice, reducer) => {
                if (this.framework?.state) {
                    this.framework.state.addReducer(slice, reducer);
                }
            },
            on: (event, cb) => {
                if (this.framework?.events) {
                    return this.framework.events.on(event, cb);
                }
            },
            hook: (name, cb) => this.hook(name, cb),
            log: (level, msg) => this._log(level, `[${plugin.name}] ${msg}`)
        };
    }

    get stats() {
        return {
            total: this._plugins.size,
            initialized: Array.from(this._plugins.values()).filter(p => p.initialized).length,
            enabled: Array.from(this._plugins.values()).filter(p => p.enabled).length,
            hooks: this._hooks.size
        };
    }

    destroyAll() {
        const names = Array.from(this._plugins.keys());
        for (const name of names.reverse()) {
            this.destroy(name);
        }
        this._hooks.clear();
        this._initialized = false;
    }

    _log(level, msg, err) {
        if (this.framework?.log) this.framework.log(level, `PluginEngine: ${msg}`, err);
    }
}
```

---

# 5. Ciclo de Vida

```
register → init → enable → (uso) → disable → destroy
```

| Fase | Descrição |
|------|-----------|
| register | Plugin é registrado no engine |
| init | Plugin se prepara (registra componentes, hooks) |
| enable | Plugin ativo e funcional |
| disable | Plugin inativo (sem remover) |
| destroy | Plugin é completamente removido |

---

# 6. Estrutura de um Plugin

```js
const meuPlugin = {
    name: 'meu-plugin',
    version: '1.0.0',
    description: 'Descrição do plugin',
    dependsOn: ['core-plugin'], // Opcional

    init(api) {
        // Registra componentes, serviços, rotas
        api.registerComponent('meu-componente', MeuComponente);
        api.addRoute({
            path: '/meu-plugin',
            name: 'meu-plugin',
            component: 'meu-componente'
        });
    },

    enable() {
        // Plugin ativado
    },

    disable() {
        // Plugin desativado (mas ainda registrado)
    },

    destroy() {
        // Limpeza final
    }
};
```

---

# 7. Testes

```js
describe('PluginEngine', () => {
    it('should register and initialize plugins', () => {
        const spy = jasmine.createSpy();
        const plugin = { name: 'test', version: '1.0', init: spy };
        engine.register(plugin);
        engine.init();
        expect(spy).toHaveBeenCalled();
    });

    it('should resolve dependency order', () => {
        const order = [];
        engine.register({ name: 'b', version: '1.0', dependsOn: ['a'], init: () => order.push('b') });
        engine.register({ name: 'a', version: '1.0', init: () => order.push('a') });
        engine.init();
        expect(order).toEqual(['a', 'b']);
    });

    it('should enable/disable plugins', () => {
        const plugin = { name: 'test', version: '1.0', enable: spy, disable: spy };
        engine.register(plugin);
        engine.init();
        engine.enable('test');
        expect(spy).toHaveBeenCalled();
        engine.disable('test');
        expect(spy).toHaveBeenCalled();
    });
});
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial — Plugin Engine |
