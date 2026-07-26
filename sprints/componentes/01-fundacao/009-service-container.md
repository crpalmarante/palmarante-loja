# FiscalUI Framework

## Documento 009 — Service Container

**Versão 1.0**

Este documento define o sistema de Injeção de Dependência do FiscalUI. O Service Container gerencia o ciclo de vida de serviços, resolve dependências automaticamente, permite substituição de implementações e serve como ponto central de registro para todos os módulos do Framework.

---

# Índice

1. Introdução
2. Filosofia
3. Arquitetura
4. API Pública
5. Registro de Serviços
6. Fábricas
7. Aliases
8. Resolução de Dependências
9. Injeção Automática
10. Ciclo de Vida
11. Lazy Loading
12. Singleton vs Transient
13. Tags e Grupos
14. Substituição e Mocking
15. Decorators
16. Serviços do Framework
17. Eventos do Container
18. Hooks
19. Debugging
20. Performance
21. Memória
22. Testes
23. Boas Práticas

---

# 1. Introdução

## 1.1 Propósito

O Service Container resolve, gerencia e injeta dependências no FiscalUI. Ele elimina a necessidade de módulos criarem suas próprias dependências manualmente, promovendo baixo acoplamento e alta testabilidade.

```js
// ❌ Sem Container — acoplamento direto
class UserService {
    constructor() {
        this.http = new HTTPService();      // Duro de trocar
        this.cache = new CacheService();     // Duro de mockar
        this.logger = new LoggerService();   // Duro de testar
    }
}

// ✅ Com Container — desacoplamento total
class UserService {
    constructor(container) {
        this.http = container.get('http');
        this.cache = container.get('cache');
        this.logger = container.get('logger');
    }
}
```

## 1.2 Princípios

```
1. Serviços nunca criam suas próprias dependências
2. Serviços declaram o que precisam, o Container entrega
3. Qualquer serviço pode ser substituído (mocking, testes)
4. Ciclo de vida de serviços é gerenciado pelo Container
5. Resolução circular é detectada e bloqueada
6. Toda instância criada pode ser destruída centralizadamente
```

## 1.3 O que é um Serviço

Um serviço é qualquer objeto que executa uma função no sistema, sem ser um componente visual:

```
HTTP Service      → requisições HTTP
Auth Service      → autenticação e sessão
Cache Service     → armazenamento em cache
Logger Service    → logging centralizado
Toast Service     → notificações
Modal Service     → gerenciamento de modais
API Service       → abstração de API
Config Service    → configurações do sistema
```

---

# 2. Filosofia

## 2.1 Programação para Interface

Serviços dependem de contratos, não de implementações concretas:

```js
// Container registra implementação concreta
container.register('http', new FetchHTTPService());

// Consumidor depende do contrato (get/post), não da implementação
class UserService {
    constructor(container) {
        this.http = container.get('http'); // Pode ser Fetch, Axios, Mock...
    }
}
```

## 2.2 Inversão de Controle

```
Quem cria não usa. Quem usa não cria.

O Container cria.
O Serviço usa.
```

## 2.3 Um Serviço, Uma Responsabilidade

Cada serviço faz exatamente uma coisa e faz bem:

```js
// ✅ Correto
container.register('http', new HTTPService());      // Só HTTP
container.register('auth', new AuthService());        // Só auth
container.register('cache', new CacheService());      // Só cache

// ❌ Errado — service faz tudo
container.register('gambiarras', new GiantService()); // Tudo junto
```

---

# 3. Arquitetura

## 3.1 Diagrama

```
┌──────────────────────────────────────────────┐
│              Service Container                │
├──────────────────────────────────────────────┤
│                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Services │  │Factories │  │ Aliases  │   │
│  │  Map     │  │  Map     │  │  Map     │   │
│  └──────────┘  └──────────┘  └──────────┘   │
│                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Instances │  │ Resolved │  │Resolving │   │
│  │  Map     │  │   Set    │  │   Set    │   │
│  └──────────┘  └──────────┘  └──────────┘   │
│                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Tags    │  │Decorators│  │  Hooks   │   │
│  │  Map     │  │   Map    │  │   Map    │   │
│  └──────────┘  └──────────┘  └──────────┘   │
│                                              │
└──────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────┐
│         Serviços Registrados                  │
├──────────────────────────────────────────────┤
│  http → HTTPService                           │
│  auth → AuthService                           │
│  api  → APIService (factory)                  │
│  logger → LoggerService (lazy)                │
│  cache → CacheService                         │
│  toast → ToastService                         │
└──────────────────────────────────────────────┘
```

## 3.2 Estrutura Interna

```js
ServiceContainer {
    _services:   Map<string, ServiceEntry>
    _factories:  Map<string, FactoryEntry>
    _instances:  Map<string, Object>
    _aliases:    Map<string, string>
    _tags:       Map<string, Set<string>>
    _decorators: Map<string, Function[]>
    _hooks:      { beforeRegister, afterRegister, beforeGet, afterGet, beforeDestroy }
    _resolved:   Set<string>
    _resolving:  Set<string>   // Prevenção de circular
    _frozen:     boolean       // Impede novos registros após boot
}
```

## 3.3 Relação com Outros Módulos

```
FiscalUI.init()
    │
    ├── Cria Container
    ├── Container.register('http', new HTTPService())
    ├── Container.register('auth', new AuthService())
    ├── Container.register('router', new Router())
    ├── Container.register('eventBus', new EventBus())
    ├── Container.register('theme', new ThemeEngine())
    │
    ├── Container.get('http')       → Resolve sob demanda
    ├── Container.get('router')     → Resolve sob demanda
    │
    └── Container.invoke(fn, deps) → Injeção automática
```

---

# 4. API Pública

## 4.1 Implementação

```js
class ServiceContainer {
    constructor(framework = null) {
        this.framework = framework;
        this._services = new Map();
        this._factories = new Map();
        this._instances = new Map();
        this._aliases = new Map();
        this._tags = new Map();
        this._decorators = new Map();
        this._hooks = {
            beforeRegister: [],
            afterRegister: [],
            beforeGet: [],
            afterGet: [],
            beforeDestroy: [],
            afterDestroy: []
        };
        this._resolved = new Set();
        this._resolving = new Set();
        this._frozen = false;
        this._id = 0;
    }

    // ─── Registro ──────────────────────────────────────────

    register(name, instance, options = {}) {
        if (this._frozen) {
            this._log('warn', `Container: ${name} — container congelado`);
            return this;
        }
        if (this._services.has(name) || this._factories.has(name)) {
            this._log('warn', `Container: ${name} já registrado`);
            return this;
        }

        this._runHooks('beforeRegister', { name, instance, options });

        const entry = {
            name,
            instance,
            options: {
                singleton: true,
                lazy: false,
                tags: [],
                ...options
            },
            initialized: false,
            id: ++this._id
        };

        this._services.set(name, entry);

        // Registra tags
        if (entry.options.tags && entry.options.tags.length) {
            for (const tag of entry.options.tags) {
                this._addTag(tag, name);
            }
        }

        this._log('info', `Container: ${name} registrado`);
        this._runHooks('afterRegister', { name, instance, options });
        return this;
    }

    registerFactory(name, factory, options = {}) {
        if (this._frozen) {
            this._log('warn', `Container: ${name} — container congelado`);
            return this;
        }
        if (this._services.has(name) || this._factories.has(name)) {
            this._log('warn', `Container: ${name} já registrado`);
            return this;
        }

        const entry = {
            name,
            factory,
            options: {
                singleton: true,
                tags: [],
                ...options
            },
            instance: null,
            id: ++this._id
        };

        this._factories.set(name, entry);

        if (entry.options.tags && entry.options.tags.length) {
            for (const tag of entry.options.tags) {
                this._addTag(tag, name);
            }
        }

        this._log('info', `Container: factory ${name} registrada`);
        return this;
    }

    // ─── Aliases ────────────────────────────────────────────

    alias(alias, target) {
        if (this._aliases.has(alias)) {
            this._log('warn', `Container: alias ${alias} já existe`);
            return this;
        }
        this._aliases.set(alias, target);
        return this;
    }

    // ─── Resolução ──────────────────────────────────────────

    get(name) {
        this._runHooks('beforeGet', { name });

        const resolvedName = this._aliases.get(name) || name;

        // Já resolvido → retorna instância em cache
        if (this._instances.has(resolvedName)) {
            const instance = this._instances.get(resolvedName);
            this._runHooks('afterGet', { name, instance });
            return instance;
        }

        // Prevenção de dependência circular
        if (this._resolving.has(resolvedName)) {
            throw new Error(
                `Container: dependência circular detectada em "${resolvedName}"`
            );
        }
        this._resolving.add(resolvedName);

        let instance = null;

        // Busca em serviços registrados
        if (this._services.has(resolvedName)) {
            instance = this._resolveService(resolvedName);
        }
        // Busca em fábricas
        else if (this._factories.has(resolvedName)) {
            instance = this._resolveFactory(resolvedName);
        }
        // Não encontrado
        else {
            this._resolving.delete(resolvedName);
            this._log('error', `Container: "${name}" não encontrado`);
            return null;
        }

        this._resolving.delete(resolvedName);

        // Aplica decorators
        if (this._decorators.has(resolvedName)) {
            const decorators = this._decorators.get(resolvedName);
            for (const decorator of decorators) {
                instance = decorator(instance, this);
            }
        }

        this._runHooks('afterGet', { name, instance });
        return instance;
    }

    _resolveService(name) {
        const entry = this._services.get(name);

        if (entry.options.lazy && !entry.initialized) {
            if (entry.instance.init && typeof entry.instance.init === 'function') {
                entry.instance.init();
            }
            entry.initialized = true;
            this._log('debug', `Container: ${name} inicializado (lazy)`);
        }

        if (entry.options.singleton) {
            this._instances.set(name, entry.instance);
            this._resolved.add(name);
            return entry.instance;
        }

        // Transient: retorna nova instância (precisa ser factory)
        this._log('warn', `Container: ${name} é transient mas foi registrado como instância`);
        return entry.instance;
    }

    _resolveFactory(name) {
        const entry = this._factories.get(name);

        if (entry.options.singleton) {
            if (!entry.instance) {
                entry.instance = entry.factory(this);
                this._instances.set(name, entry.instance);
                this._resolved.add(name);
            }
            return entry.instance;
        }

        // Transient: nova instância a cada get()
        return entry.factory(this);
    }

    // ─── Tags ───────────────────────────────────────────────

    _addTag(tag, serviceName) {
        if (!this._tags.has(tag)) {
            this._tags.set(tag, new Set());
        }
        this._tags.get(tag).add(serviceName);
    }

    getByTag(tag) {
        if (!this._tags.has(tag)) return [];
        return Array.from(this._tags.get(tag))
            .map(name => this.get(name))
            .filter(svc => svc !== null);
    }

    hasTag(tag) {
        return this._tags.has(tag) && this._tags.get(tag).size > 0;
    }

    // ─── Decorators ─────────────────────────────────────────

    decorate(name, decoratorFn) {
        if (!this._decorators.has(name)) {
            this._decorators.set(name, []);
        }
        this._decorators.get(name).push(decoratorFn);
        return this;
    }

    // ─── Hooks ──────────────────────────────────────────────

    on(event, callback) {
        if (this._hooks[event]) {
            this._hooks[event].push(callback);
        }
        return this;
    }

    _runHooks(event, data) {
        if (this._hooks[event]) {
            for (const hook of this._hooks[event]) {
                try {
                    hook(data, this);
                } catch (e) {
                    this._log('error', `Container: hook ${event} error`, e);
                }
            }
        }
    }

    // ─── Verificação ────────────────────────────────────────

    has(name) {
        const resolvedName = this._aliases.get(name) || name;
        return this._services.has(resolvedName)
            || this._factories.has(resolvedName);
    }

    isResolved(name) {
        const resolvedName = this._aliases.get(name) || name;
        return this._instances.has(resolvedName);
    }

    // ─── Remoção ────────────────────────────────────────────

    remove(name) {
        const resolvedName = this._aliases.get(name) || name;

        this._runHooks('beforeDestroy', { name: resolvedName });

        if (this._instances.has(resolvedName)) {
            const instance = this._instances.get(resolvedName);
            if (instance.destroy && typeof instance.destroy === 'function') {
                try { instance.destroy(); } catch (e) {
                    this._log('error', `Container: erro ao destruir ${resolvedName}`, e);
                }
            }
            this._instances.delete(resolvedName);
        }

        this._services.delete(resolvedName);
        this._factories.delete(resolvedName);
        this._resolved.delete(resolvedName);

        // Remove de tags
        for (const [tag, services] of this._tags) {
            services.delete(resolvedName);
        }

        this._runHooks('afterDestroy', { name: resolvedName });
        this._log('info', `Container: ${resolvedName} removido`);
    }

    // ─── Injeção Automática ─────────────────────────────────

    invoke(fn, dependencies = []) {
        const resolved = dependencies.map(dep => this.get(dep));

        // Verifica se alguma dependência não foi resolvida
        const missing = dependencies.filter((dep, i) => resolved[i] === null);
        if (missing.length) {
            this._log('error', `Container: invoke — dependências não encontradas: ${missing.join(', ')}`);
            return null;
        }

        return fn(...resolved);
    }

    // ─── Controle ───────────────────────────────────────────

    freeze() {
        this._frozen = true;
        this._log('info', 'Container: congelado');
        return this;
    }

    unfreeze() {
        this._frozen = false;
        this._log('info', 'Container: descongelado');
        return this;
    }

    isFrozen() {
        return this._frozen;
    }

    // ─── Estatísticas ───────────────────────────────────────

    stats() {
        return {
            services: this._services.size,
            factories: this._factories.size,
            instances: this._instances.size,
            aliases: this._aliases.size,
            tags: this._tags.size,
            resolved: this._resolved.size,
            frozen: this._frozen
        };
    }

    getNames() {
        return [
            ...Array.from(this._services.keys()),
            ...Array.from(this._factories.keys())
        ];
    }

    // ─── Limpeza ────────────────────────────────────────────

    clear() {
        this._runHooks('beforeDestroy', { name: '*all*' });

        this._instances.forEach((instance, name) => {
            if (instance.destroy && typeof instance.destroy === 'function') {
                try {
                    instance.destroy();
                } catch (e) {
                    this._log('error', `Container: erro ao destruir ${name}`, e);
                }
            }
        });

        this._services.clear();
        this._factories.clear();
        this._instances.clear();
        this._aliases.clear();
        this._tags.clear();
        this._decorators.clear();
        this._resolved.clear();
        this._resolving.clear();
        this._frozen = false;

        this._log('info', 'Container: limpo');
    }

    // ─── Internos ───────────────────────────────────────────

    _log(level, message, error = null) {
        if (this.framework && this.framework.log) {
            this.framework.log(level, message, error);
        } else if (level === 'error') {
            console.error(`[ServiceContainer] ${message}`, error || '');
        } else if (level === 'warn') {
            console.warn(`[ServiceContainer] ${message}`);
        } else if (level === 'debug' && this.framework && this.framework.config && this.framework.config.debug) {
            console.log(`[ServiceContainer] ${message}`);
        }
    }
}
```

## 4.2 Resumo da API

| Método | Descrição |
|--------|-----------|
| `register(name, instance, opts)` | Registra instância de serviço |
| `registerFactory(name, factory, opts)` | Registra fábrica de serviço |
| `alias(alias, target)` | Cria apelido para serviço |
| `get(name)` | Resolve e retorna serviço |
| `has(name)` | Verifica se serviço existe |
| `isResolved(name)` | Verifica se já foi resolvido |
| `remove(name)` | Remove e destroi serviço |
| `invoke(fn, deps)` | Executa função com injeção automática |
| `getByTag(tag)` | Retorna todos serviços de uma tag |
| `hasTag(tag)` | Verifica se tag existe |
| `decorate(name, fn)` | Adiciona decorator a serviço |
| `on(event, callback)` | Hook de ciclo de vida |
| `freeze()` | Congela container (impede registros) |
| `unfreeze()` | Descongela container |
| `isFrozen()` | Verifica se está congelado |
| `stats()` | Estatísticas do container |
| `getNames()` | Lista todos serviços registrados |
| `clear()` | Remove e destroi tudo |

---

# 5. Registro de Serviços

## 5.1 Registro Direto (Instância)

```js
container.register('http', new HTTPService(fiscalUI));
container.register('logger', new LoggerService());

// Com opções
container.register('cache', new CacheService(), {
    singleton: true,    // (padrão) mesma instância sempre
    lazy: false,        // (padrão) inicializa na hora
    tags: ['core', 'storage']
});
```

## 5.2 Comportamento

```
Registro direto:
  - Recebe instância já criada
  - Se singleton (padrão): get() retorna sempre a mesma
  - Se lazy: init() é chamado apenas no primeiro get()
  - Se transient: não faz sentido para instância direta (usar factory)
```

---

# 6. Fábricas

## 6.1 Registro via Factory

```js
container.registerFactory('api', (container) => {
    const http = container.get('http');
    const cache = container.get('cache');
    return new APIService(http, cache);
});

container.registerFactory('userService', (c) => {
    return new UserService(c.get('api'), c.get('auth'));
});
```

## 6.2 Singleton vs Transient

```js
// Singleton (padrão) — mesma instância em todos get()
container.registerFactory('config', () => new ConfigService(), {
    singleton: true
});

// Transient — nova instância a cada get()
container.registerFactory('mask', () => new MaskService(), {
    singleton: false
});

const a = container.get('mask'); // Nova instância
const b = container.get('mask'); // Outra instância
console.log(a === b); // false
```

## 6.3 Factory com Parâmetros

```js
// Factory que aceita parâmetros adicionais
container.registerFactory('modal', (c) => {
    return {
        open: (options) => new Modal(options),
        confirm: (message) => new ConfirmModal(message)
    };
});

// Uso
const modal = container.get('modal');
modal.open({ title: 'Aviso', content: 'Salvo com sucesso!' });
```

---

# 7. Aliases

## 7.1 Definição

Aliases permitem referenciar o mesmo serviço por nomes diferentes:

```js
container.register('httpClient', new HTTPService());
container.alias('http', 'httpClient');
container.alias('apiClient', 'httpClient');

// Todos resolvem para a mesma instância
const a = container.get('http');
const b = container.get('httpClient');
const c = container.get('apiClient');
console.log(a === b && b === c); // true
```

## 7.2 Casos de Uso

```
1. Migração — nome antigo → nome novo (backward compat)
2. Contexto — nome genérico → específico
3. Testes — alias para mock sem modificar registros
```

---

# 8. Resolução de Dependências

## 8.1 Resolução Automática

```js
// Serviço A depende de B e C
container.registerFactory('serviceA', (c) => {
    const b = c.get('serviceB');  // Resolve automaticamente
    const cSvc = c.get('serviceC');
    return new ServiceA(b, cSvc);
});

container.register('serviceB', new ServiceB());
container.register('serviceC', new ServiceC());

const a = container.get('serviceA'); // B e C resolvidos automaticamente
```

## 8.2 Detecção de Dependência Circular

```js
// ❌ Circular: A → B → C → A
container.registerFactory('a', (c) => new A(c.get('b')));
container.registerFactory('b', (c) => new B(c.get('c')));
container.registerFactory('c', (c) => new C(c.get('a')));

container.get('a'); // Throws: "Container: dependência circular detectada em 'a'"
```

## 8.3 Cadeia de Resolução

```
get('api')
    │
    ├── alias? 'api' → 'apiService'
    │
    ├── já resolvido? → retorna instância cacheada
    │
    ├── é serviço direto?
    │       ├── lazy? → init() e marca inicializado
    │       ├── singleton? → cacheia e retorna
    │       └── transient? → retorna (não cacheia)
    │
    ├── é factory?
    │       ├── singleton?
    │       │       ├── já tem instância? → retorna
    │       │       └── não tem? → factory() → cacheia → retorna
    │       └── transient? → factory() → retorna (não cacheia)
    │
    ├── aplica decorators
    │
    └── retorna instância
```

---

# 9. Injeção Automática

## 9.1 invoke()

```js
// Em vez de resolver manualmente:
const http = container.get('http');
const auth = container.get('auth');
const toast = container.get('toast');
initApp(http, auth, toast);

// Use invoke() com injeção automática:
container.invoke((http, auth, toast) => {
    initApp(http, auth, toast);
}, ['http', 'auth', 'toast']);
```

## 9.2 invoke() em Construtores

```js
class DashboardService {
    constructor(container) {
        // Injeta dependências via invoke
        container.invoke((http, cache, events) => {
            this.http = http;
            this.cache = cache;
            this.events = events;
        }, ['http', 'cache', 'eventBus']);
    }
}
```

## 9.3 invoke() com Retorno

```js
const result = container.invoke((http, config) => {
    return http.get(config.apiUrl + '/status');
}, ['http', 'config']);

console.log(result); // Retorno da função
```

---

# 10. Ciclo de Vida

## 10.1 Fases

```
Registro → Inicialização → Resolução → Uso → Destruição
```

| Fase | Descrição |
|------|-----------|
| Registro | Serviço é registrado no container |
| Inicialização | Se lazy, init() é chamado no primeiro get() |
| Resolução | Dependências são resolvidas e instância retornada |
| Uso | Serviço é usado pela aplicação |
| Destruição | remove() ou clear() chamam destroy() no serviço |

## 10.2 init() e destroy()

```js
class DatabaseService {
    init() {
        // Chamado automaticamente no primeiro get() (se lazy)
        this.connection = openConnection();
        console.log('DatabaseService: conectado');
    }

    destroy() {
        // Chamado automaticamente em remove() ou clear()
        this.connection.close();
        console.log('DatabaseService: desconectado');
    }
}

// Registro lazy
container.register('db', new DatabaseService(), { lazy: true });

// Neste ponto, DatabaseService ainda não conectou
const db = container.get('db'); // init() é chamado aqui

// Quando não precisar mais:
container.remove('db'); // destroy() é chamado
```

## 10.3 Ordem de Destruição

```js
container.clear(); // Destroi na ordem inversa da resolução

// Último resolvido é o primeiro a ser destruído
// (LIFO — garantindo que dependências sejam destruídas após seus consumidores)
```

---

# 11. Lazy Loading

## 11.1 Serviços Lentos

Serviços com inicialização custosa (conexão de banco, carregamento de config, etc.) devem ser lazy:

```js
container.register('database', new DatabaseService(), {
    lazy: true  // Só inicializa quando alguém chamar get()
});

container.register('config', new ConfigService(), {
    lazy: true  // Carrega arquivo de config apenas quando necessário
});

// Nada aconteceu ainda...

// Agora sim o DatabaseService.init() será chamado
const db = container.get('database');
```

## 11.2 Quando Usar

```
✅ Use lazy para:
  - Serviços de conexão (DB, WebSocket)
  - Serviços de config (leitura de arquivos)
  - Serviços de terceiros (inicialização pesada)
  - Serviços opcionais (só usados em alguns fluxos)

❌ NÃO use lazy para:
  - Serviços críticos usados na inicialização
  - Serviços de logging (precisa estar pronto sempre)
  - Event Bus (precisa estar disponível imediatamente)
```

---

# 12. Singleton vs Transient

## 12.1 Comparação

| Aspecto | Singleton | Transient |
|---------|-----------|-----------|
| Instâncias | Uma para todo o sistema | Nova a cada get() |
| Memória | Menos consumo | Mais consumo |
| Estado compartilhado | Sim | Não |
| Caso típico | HTTP Service, Config | Mask Service, Formatter |
| Cache | Sim | Não |

## 12.2 Escolha Correta

```js
// ✅ Singleton — uma conexão HTTP para todo o sistema
container.registerFactory('http', () => new HTTPService(), {
    singleton: true
});

// ✅ Transient — cada get() uma nova instância (sem estado)
container.registerFactory('formatter', () => new Formatter(), {
    singleton: false
});

// ⚠️ Singleton com estado — cuidado!
container.register('counter', new CounterService(), {
    singleton: true
});
// Qualquer modificação no CounterService afeta todos consumidores
```

---

# 13. Tags e Grupos

## 13.1 Definição

Tags agrupam serviços por categoria:

```js
container.register('http', new HTTPService(), {
    tags: ['core', 'network']
});

container.register('cache', new CacheService(), {
    tags: ['core', 'storage']
});

container.register('logger', new LoggerService(), {
    tags: ['core', 'debug']
});

container.register('analytics', new AnalyticsService(), {
    tags: ['optional', 'network']
});
```

## 13.2 Busca por Tag

```js
// Todos serviços core
const coreServices = container.getByTag('core');
// → [HTTPService, CacheService, LoggerService]

// Todos serviços de rede
const networkServices = container.getByTag('network');
// → [HTTPService, AnalyticsService]

// Verifica se tag existe
if (container.hasTag('debug')) {
    console.log('Serviços de debug disponíveis');
}
```

## 13.3 Tags do Framework

```
Tag         | Descrição
------------|---------------------------
core        | Serviços essenciais do Framework
network     | Serviços de comunicação
storage     | Serviços de armazenamento
debug       | Serviços de logging/debug
optional    | Serviços não essenciais
plugin      | Serviços carregados por plugins
user        | Serviços do usuário/domínio
```

---

# 14. Substituição e Mocking

## 14.1 Substituição em Testes

```js
// Produção
container.register('http', new FetchHTTPService());

// Teste: substitui antes de resolver
beforeEach(() => {
    container.remove('http');
    container.register('http', new MockHTTPService());
});

// O serviço que usa http agora receberá o MockHTTPService
const userService = container.get('userService');
```

## 14.2 Substituição Controlada

```js
// Produção
if (environment === 'production') {
    container.register('analytics', new AnalyticsService());
} else {
    container.register('analytics', new DevAnalyticsService());
}

// Ou via feature flag
if (config.useNewApi) {
    container.register('api', new NewAPIService());
} else {
    container.register('api', new LegacyAPIService());
}
```

## 14.3 Ambiente de Teste

```js
// setup-test.js
container.register('http', new MockHTTPService());
container.register('auth', new MockAuthService());
container.register('cache', new MockCacheService());

// Serviços que dependem de http, auth e cache
// automaticamente receberão as versões mockadas
```

---

# 15. Decorators

## 15.1 Definição

Decorators envolvem um serviço para adicionar comportamento sem modificar o serviço original:

```js
container.register('http', new HTTPService());

// Adiciona logging a todas chamadas HTTP
container.decorate('http', (http, container) => {
    return new Proxy(http, {
        get(target, prop) {
            const original = target[prop];
            if (typeof original === 'function') {
                return function(...args) {
                    console.log(`[HTTP] ${prop} chamado com:`, args);
                    const result = original.apply(this, args);
                    console.log(`[HTTP] ${prop} retornou:`, result);
                    return result;
                };
            }
            return original;
        }
    });
});

const http = container.get('http');
http.get('/api/data');
// Console: [HTTP] get chamado com: ['/api/data']
```

## 15.2 Cache Decorator

```js
container.decorate('userService', (service) => {
    const cache = new Map();

    return new Proxy(service, {
        get(target, prop) {
            if (prop === 'getUser') {
                return async (id) => {
                    if (cache.has(id)) return cache.get(id);
                    const user = await target.getUser(id);
                    cache.set(id, user);
                    return user;
                };
            }
            if (prop === 'clearCache') {
                return () => cache.clear();
            }
            return target[prop];
        }
    });
});
```

---

# 16. Serviços do Framework

## 16.1 Serviços Registrados Automaticamente

```js
// FiscalUI.init() registra estes serviços automaticamente:

container.register('eventBus', eventBus,            { tags: ['core'] });
container.register('theme', themeEngine,             { tags: ['core'] });
container.register('router', router,                 { tags: ['core'] });
container.register('responsive', responsiveEngine,   { tags: ['core'] });
container.register('a11y', a11yEngine,               { tags: ['core'] });
container.register('http', httpService,              { tags: ['core', 'network'] });
container.register('logger', loggerService,          { tags: ['core', 'debug'] });
container.register('config', configService,          { tags: ['core'] });
```

## 16.2 Serviços de Domínio (Aplicação)

```js
// Registrados pela aplicação:

container.register('auth', new AuthService(),        { tags: ['user'] });
container.register('nfe', new NFeService(),          { tags: ['user', 'domain'] });
container.register('cliente', new ClienteService(),  { tags: ['user', 'domain'] });
container.register('produto', new ProdutoService(),  { tags: ['user', 'domain'] });
container.register('dashboard', new DashboardService(), { tags: ['user'] });
```

---

# 17. Eventos do Container

## 17.1 Eventos Emitidos no EventBus

```js
'container:register'      // Serviço registrado
'container:factory'       // Factory registrada
'container:alias'         // Alias criado
'container:resolve'       // Serviço resolvido
'container:remove'        // Serviço removido
'container:clear'         // Container limpo
'container:frozen'        // Container congelado
'container:error'         // Erro no container (circular, não encontrado)
```

## 17.2 Payload

```js
// container:register
{
    source: 'ServiceContainer',
    name: 'http',
    tags: ['core', 'network'],
    singleton: true,
    lazy: false
}

// container:resolve
{
    source: 'ServiceContainer',
    name: 'api',
    singleton: true,
    duration: 2,  // ms para resolver
    fromCache: false
}

// container:error
{
    source: 'ServiceContainer',
    type: 'circular',
    name: 'serviceA',
    message: 'Dependência circular detectada'
}
```

---

# 18. Hooks

## 18.1 Hooks de Ciclo de Vida

```js
container.on('beforeRegister', ({ name, instance, options }) => {
    console.log(`Registrando: ${name}`);
});

container.on('afterRegister', ({ name }) => {
    console.log(`Registrado: ${name}`);
});

container.on('beforeGet', ({ name }) => {
    console.log(`Resolvendo: ${name}`);
});

container.on('afterGet', ({ name, instance }) => {
    console.log(`Resolvido: ${name}`, typeof instance);
});

container.on('beforeDestroy', ({ name }) => {
    console.log(`Destruindo: ${name}`);
});
```

## 18.2 Hooks de Validação

```js
// Impede registro de serviços sem nome
container.on('beforeRegister', ({ name }) => {
    if (!name || name.trim() === '') {
        throw new Error('Serviço precisa de um nome');
    }
});

// Loga quando serviço é resolvido
container.on('afterGet', ({ name, instance }) => {
    if (!instance) {
        console.warn(`Serviço ${name} retornou null`);
    }
});
```

---

# 19. Debugging

## 19.1 Modo Debug

```js
FiscalUI.config.debug = true;

// Loga todos eventos do container:
// [ServiceContainer] http registrado
// [ServiceContainer] factory api registrada
// [ServiceContainer] Resolvendo: http
// [ServiceContainer] http resolvido (1ms)
```

## 19.2 Estatísticas

```js
const stats = container.stats();
console.table(stats);
// ┌───────────┬───────┐
// │ services  │ 8     │
// │ factories │ 3     │
// │ instances │ 6     │
// │ aliases   │ 2     │
// │ tags      │ 4     │
// │ resolved  │ 6     │
// │ frozen    │ false │
// └───────────┴───────┘
```

## 19.3 Lista de Serviços

```js
const services = container.getNames();
console.log('Serviços registrados:', services);

// Aplicação pode exibir painel de debug:
// http      │ HTTPService     │ ✅ resolvido
// api       │ APIService      │ ✅ resolvido
// cache     │ CacheService    │ ✅ resolvido
// logger    │ LoggerService   │ ❌ não resolvido (lazy)
// database  │ DatabaseService │ ❌ não resolvido (lazy)
```

---

# 20. Performance

## 20.1 Métricas

| Operação | Performance | Complexidade |
|----------|-------------|--------------|
| `register()` | < 0.01ms | O(1) |
| `registerFactory()` | < 0.01ms | O(1) |
| `get()` (cacheado) | < 0.001ms | O(1) |
| `get()` (primeira vez) | < 0.1ms | O(1) |
| `get()` com factory | < 0.5ms | O(1) + custo factory |
| `alias()` | < 0.01ms | O(1) |
| `invoke()` | < 0.5ms | O(n) onde n = número de deps |
| `remove()` | < 0.1ms | O(1) |
| `clear()` | < 1ms | O(n) onde n = serviços |
| `getByTag()` | < 0.1ms | O(n) onde n = serviços com tag |

## 20.2 Otimizações

```js
// 1. Prefira register() em vez de registerFactory() quando possível
//    Instâncias diretas evitam overhead de factory
✅ container.register('http', new HTTPService())
❌ container.registerFactory('http', () => new HTTPService())

// 2. Use singleton para serviços usados frequentemente
✅ { singleton: true } // Cacheia após primeiro get()

// 3. Use lazy para serviços pesados que podem nunca ser usados
✅ { lazy: true } // Só inicializa quando necessário

// 4. Congele o container após o boot para prevenir registros acidentais
✅ container.freeze()

// 5. Evite decorators complexos em serviços de alta frequência
//    Decorators adicionam overhead de Proxy em cada chamada
```

---

# 21. Memória

## 21.1 Prevenção de Vazamentos

```js
class MyService {
    constructor(container) {
        this.container = container;
        this.http = container.get('http');
        this.cache = container.get('cache');
    }

    destroy() {
        // Container gerencia destroy automaticamente
        // Mas serviços podem precisar limpar referências próprias
        this.http = null;
        this.cache = null;
        this.container = null;
    }
}

// Container chama destroy() em todos serviços ao limpar
container.clear();
// → MyService.destroy() é chamado
// → HTTPservice.destroy() é chamado
// → CacheService.destroy() é chamado
```

## 21.2 Instâncias Não Referenciadas

Serviços transient (não singleton) criados por factory não são cacheados e precisam ser gerenciados manualmente:

```js
// Transient — container não mantém referência
const mask = container.get('mask');
// mask existe apenas enquanto referenciada

// Singleton — container mantém referência até clear()
const http = container.get('http');
// http existe até container.clear()
```

## 21.3 Referência Circular em Memória

```js
// ❌ Serviço que referencia container pode impedir GC
class LeakyService {
    constructor(container) {
        this.container = container; // Referência mantida
    }
    destroy() {
        this.container = null; // ✅ Necessário para liberar
    }
}
```

---

# 22. Testes

## 22.1 Teste Unitário

```js
describe('ServiceContainer', () => {
    let container;

    beforeEach(() => {
        container = new ServiceContainer();
    });

    afterEach(() => {
        container.clear();
    });

    it('should register and resolve services', () => {
        const service = { name: 'test' };
        container.register('test', service);
        expect(container.get('test')).toBe(service);
    });

    it('should create services via factory', () => {
        container.registerFactory('factory', () => ({ created: true }));
        const instance = container.get('factory');
        expect(instance.created).toBe(true);
    });

    it('should return the same instance for singletons', () => {
        container.registerFactory('singleton', () => ({ id: Math.random() }));
        const a = container.get('singleton');
        const b = container.get('singleton');
        expect(a).toBe(b);
    });

    it('should return different instances for transient', () => {
        container.registerFactory('transient', () => ({ id: Math.random() }), {
            singleton: false
        });
        const a = container.get('transient');
        const b = container.get('transient');
        expect(a).not.toBe(b);
    });

    it('should resolve aliases', () => {
        const service = { name: 'original' };
        container.register('original', service);
        container.alias('alias', 'original');
        expect(container.get('alias')).toBe(service);
    });

    it('should detect circular dependencies', () => {
        container.registerFactory('a', (c) => ({ b: c.get('b') }));
        container.registerFactory('b', (c) => ({ c: c.get('c') }));
        container.registerFactory('c', (c) => ({ a: c.get('a') }));
        expect(() => container.get('a')).toThrowError(/circular/);
    });

    it('should call init() on lazy services', () => {
        const spy = { init: () => {} };
        spyOn(spy, 'init');
        container.register('lazy', spy, { lazy: true });

        expect(spy.init).not.toHaveBeenCalled();
        container.get('lazy');
        expect(spy.init).toHaveBeenCalled();
    });

    it('should call destroy() on remove', () => {
        const spy = { destroy: () => {} };
        spyOn(spy, 'destroy');
        container.register('test', spy);
        container.remove('test');
        expect(spy.destroy).toHaveBeenCalled();
    });

    it('should call destroy() on all services during clear()', () => {
        const a = { destroy: () => {} };
        const b = { destroy: () => {} };
        spyOn(a, 'destroy');
        spyOn(b, 'destroy');
        container.register('a', a);
        container.register('b', b);
        container.clear();
        expect(a.destroy).toHaveBeenCalled();
        expect(b.destroy).toHaveBeenCalled();
    });

    it('should prevent registration when frozen', () => {
        container.freeze();
        container.register('new', {});
        expect(container.has('new')).toBe(false);
    });

    it('should support tags and getByTag', () => {
        container.register('a', { name: 'A' }, { tags: ['core'] });
        container.register('b', { name: 'B' }, { tags: ['core', 'network'] });
        container.register('c', { name: 'C' }, { tags: ['network'] });

        const core = container.getByTag('core');
        expect(core.length).toBe(2);

        const network = container.getByTag('network');
        expect(network.length).toBe(2);
    });

    it('should apply decorators', () => {
        container.register('test', { value: 1 });
        container.decorate('test', (instance) => {
            return { ...instance, value: 2 };
        });
        const resolved = container.get('test');
        expect(resolved.value).toBe(2);
    });

    it('should support invoke with automatic injection', () => {
        container.register('a', { name: 'A' });
        container.register('b', { name: 'B' });

        const fn = jasmine.createSpy();
        container.invoke(fn, ['a', 'b']);
        expect(fn).toHaveBeenCalledWith({ name: 'A' }, { name: 'B' });
    });

    it('should run lifecycle hooks', () => {
        const beforeSpy = jasmine.createSpy();
        const afterSpy = jasmine.createSpy();

        container.on('beforeRegister', beforeSpy);
        container.on('afterRegister', afterSpy);

        container.register('test', {});

        expect(beforeSpy).toHaveBeenCalled();
        expect(afterSpy).toHaveBeenCalled();
    });

    it('should report correct stats', () => {
        container.register('a', {});
        container.register('b', {});

        const stats = container.stats();
        expect(stats.services).toBe(2);
        expect(stats.instances).toBe(0);

        container.get('a');
        const stats2 = container.stats();
        expect(stats2.instances).toBe(1);
    });
});
```

## 22.2 Mocking em Testes

```js
describe('UserService com Container', () => {
    let container;
    let mockHttp;

    beforeEach(() => {
        container = new ServiceContainer();
        mockHttp = {
            get: jasmine.createSpy('get').and.returnValue(Promise.resolve([])),
            post: jasmine.createSpy('post')
        };
        container.register('http', mockHttp);
        container.registerFactory('userService', (c) => {
            return new UserService(c.get('http'));
        });
    });

    it('should call http.get when listing users', async () => {
        const userService = container.get('userService');
        await userService.list();
        expect(mockHttp.get).toHaveBeenCalledWith('/api/users');
    });
});
```

---

# 23. Boas Práticas

## 23.1 Regras de Ouro

```
1. NUNCA crie dependências dentro do serviço — sempre peça ao Container
2. SEMPRE declare tags para agrupar serviços relacionados
3. NUNCA use transient para serviços com estado compartilhado
4. SEMPRE implemente destroy() em serviços com recursos (conexões, timers)
5. NUNCA dependa de ordem de registro — resolva no get()
6. SEMPRE congele o container após o boot em produção
7. NUNCA registre o mesmo serviço duas vezes
8. SEMPRE use aliases para backward compatibility
9. NUNCA acesse serviços que não declarou como dependência
10. SEMPRE substitua serviços reais por mocks em testes
```

## 23.2 Checklist

```
☐ Serviço tem uma única responsabilidade
☐ Serviço declara dependências no construtor
☐ Serviço não cria dependências internamente
☐ Serviço tem destroy() se possui recursos
☐ Tags apropriadas definidas
☐ Nome segue convenção (minúsculo, sem espaços)
☐ Singleton salvo quando apropriado
☐ Lazy para serviços de inicialização custosa
☐ Testes com mocks via substituição no container
☐ Container congelado após boot em produção
```

## 23.3 Convenção de Nomes

```
services:       http, auth, cache, logger, api, config
api services:   userService, nfeService, productService
alias:          httpClient → http, apiClient → api

✅ http, auth, cache, userService, nfeService
❌ HTTP, AuthService, CacheManager, User_Service
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial — Service Container completo |
