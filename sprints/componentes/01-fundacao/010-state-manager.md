# FiscalUI Framework

## Documento 010 — State Manager

**Versão 1.0**

Este documento define o sistema de gerenciamento de estado global do FiscalUI. Inspirado pelo padrão Redux: store único, estado imutável, ações que descrevem mudanças, reducers puros que transformam o estado, e subscriptions que notificam ouvintes.

---

# Índice

1. Introdução
2. Filosofia
3. Arquitetura
4. API Pública
5. Store
6. State (Árvore de Estado)
7. Actions
8. Reducers
9. Dispatch
10. Subscriptions
11. Selectors
12. Middleware
13. Async Actions
14. Estado Imutável
15. Estado Normalizado
16. Slice (Fatia de Estado)
17. Estado de Componentes
18. Integração com EventBus
19. Persistência
20. DevTools
21. Performance
22. Memória
23. Testes
24. Boas Práticas

---

# 1. Introdução

## 1.1 Propósito

O State Manager gerencia o estado global da aplicação FiscalUI em uma única árvore de estado. Inspirado pelo Redux, ele segue o padrão Flux unidirecional:

```
View → dispatch(action) → reducer → new state → View atualiza
```

Toda mudança de estado passa por este ciclo. Não há mutação direta. Não há estado escondido. Cada transição é rastreável, reproduzível e auditável.

## 1.2 Princípios

```
1. Single Source of Truth — uma única store contém todo o estado global
2. Estado é somente leitura — nunca modificar diretamente
3. Mudanças são feitas por ações — dispatch(action) → reducer → novo estado
4. Reducers são funções puras — mesmo input, mesmo output, sem efeitos colaterais
5. Imutabilidade — cada mudança produz um novo objeto de estado
6. Rastreabilidade — toda transição de estado é logada e rastreável
```

## 1.3 Analogia

```
Banco de Dados:       Tabelas → Queries → Transações → Novos dados
State Manager:        Store  → Selector → Dispatch   → Novo estado

Uma transação bancária ou é completa ou não acontece.
Uma ação do State Manager produz um novo estado ou não muda nada.
```

---

# 2. Filosofia

## 2.1 Fluxo Unidirecional

```js
// Única direção: Action → Dispatch → Reducer → Store → View

// 1. Componente dispara uma ação
component.dispatch({ type: 'user/login', payload: { id: 1, name: 'João' } });

// 2. Reducer processa e retorna novo estado
(state, action) => ({ ...state, user: action.payload });

// 3. Store notifica subscribers
store.subscribe((newState) => view.update(newState));

// 4. View re-renderiza com novo estado
```

## 2.2 Imutabilidade

```js
// ❌ Errado — muta o estado diretamente
state.user.name = 'João';

// ✅ Correto — produz um novo objeto
const newState = {
    ...state,
    user: { ...state.user, name: 'João' }
};
```

## 2.3 Reducers Puros

```js
// ✅ Reducer puro — sem efeitos colaterais
function userReducer(state = {}, action) {
    switch (action.type) {
        case 'user/login':
            return { ...state, ...action.payload, logged: true };
        case 'user/logout':
            return { logged: false };
        default:
            return state;
    }
}

// ❌ Reducer impuro — causa efeitos colaterais
function userReducer(state = {}, action) {
    switch (action.type) {
        case 'user/login':
            localStorage.setItem('user', JSON.stringify(action.payload)); // ❌
            state.logged = true; // ❌
            return { ...state, ...action.payload };
    }
}
```

---

# 3. Arquitetura

## 3.1 Diagrama

```
┌──────────┐   dispatch(action)    ┌──────────────────┐
│          │──────────────────────▶│                  │
│  View /  │                       │   StateManager   │
│  Service │◀──────────────────────│                  │
│          │   getState()          │  ┌────────────┐  │
└──────────┘                       │  │   Store    │  │
                                   │  │ (estado)   │  │
┌──────────┐   subscribe(cb)      │  └──────┬─────┘  │
│          │──────────────────────▶│         │        │
│ Listener │                       │  ┌──────┴─────┐  │
│ (outro)  │                       │  │  Reducers  │  │
│          │                       │  │ (Map<slice │  │
│ Component│                       │  │  , Function│  │
│          │                       │  └──────┬─────┘  │
└──────────┘                       │         │        │
                                   │  ┌──────┴─────┐  │
                                   │  │ Middleware │  │
                                   │  │  (chain)   │  │
                                   │  └──────┬─────┘  │
                                   │         │        │
                                   │  ┌──────┴─────┐  │
                                   │  │  DevTools  │  │
                                   │  └────────────┘  │
                                   └──────────────────┘
```

## 3.2 Estrutura Interna

```js
StateManager {
    _store: {
        _state: Object,         // Árvore de estado atual
        _reducers: Map<string, Function>,
        _subscribers: Set<Function>,
        _middlewares: Function[],
        _history: Array<{action, prevState, nextState, timestamp}>,
        _maxHistory: number,
        _enabled: boolean,
        _id: number
    }
}
```

## 3.3 Relação com Outros Módulos

```
StateManager
    │
    ├── Component → this.state.get('slice') → lê estado
    ├── Component → this.dispatch({type})  → modifica estado
    ├── Component → this.watch('slice', cb) → reage a mudanças
    │
    ├── EventBus → emite state:change, state:change:{slice}
    ├── Router → integração com estado de rota (opcional)
    ├── Service Container → registrado como serviço state
    └── DevTools → monitora histórico de ações
```

---

# 4. API Pública

## 4.1 Implementação

```js
class StateManager {
    constructor(framework = null) {
        this.framework = framework;
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
    }

    // ─── Store ──────────────────────────────────────────────

    getState() {
        return this._state;
    }

    getSlice(key) {
        if (!key) return this._state;
        return this._state[key];
    }

    // ─── Reducers ───────────────────────────────────────────

    addReducer(slice, reducer) {
        if (typeof reducer !== 'function') {
            this._log('error', `addReducer(${slice}): reducer must be a function`);
            return this;
        }
        if (this._reducers.has(slice)) {
            this._log('warn', `Reducer para slice "${slice}" já existe — substituindo`);
        }

        this._reducers.set(slice, reducer);

        // Inicializa slice se não existir
        if (!(slice in this._state)) {
            this._state[slice] = reducer(undefined, { type: '__init__' });
        }

        this._log('info', `Reducer registrado: ${slice}`);
        return this;
    }

    addReducers(reducers) {
        for (const [slice, reducer] of Object.entries(reducers)) {
            this.addReducer(slice, reducer);
        }
        return this;
    }

    hasReducer(slice) {
        return this._reducers.has(slice);
    }

    // ─── Dispatch ──────────────────────────────────────────

    dispatch(action) {
        if (!this._enabled) return action;
        if (!action || !action.type) {
            this._log('error', 'dispatch: action precisa de type');
            return action;
        }

        const prevState = this._state;

        // Cria chain de middlewares
        const enhancedDispatch = this._applyMiddlewares(action, prevState);

        if (enhancedDispatch === false) {
            // Middleware cancelou
            this._log('debug', `dispatch: ${action.type} cancelado por middleware`);
            return action;
        }

        this._id++;

        // Aplica reducers
        const nextState = this._computeNextState(prevState, action);

        // Se estado não mudou, não notifica
        if (nextState === prevState) {
            return action;
        }

        this._state = nextState;

        // Histórico
        if (this._maxHistory > 0) {
            this._history.push({
                id: this._id,
                action: { type: action.type, payload: action.payload },
                prevState,
                nextState,
                timestamp: Date.now()
            });
            if (this._history.length > this._maxHistory) {
                this._history.shift();
            }
        }

        // Notifica subscribers
        this._notify(action, prevState);

        // Emite evento no EventBus
        this._emitEventBus(action, prevState);

        this._log('debug', `dispatch: ${action.type} (${this._id})`);
        return action;
    }

    _computeNextState(prevState, action) {
        let hasChanged = false;
        const nextState = {};

        for (const [slice, reducer] of this._reducers) {
            const sliceState = prevState[slice];
            const nextSlice = reducer(sliceState, action);

            if (nextSlice !== sliceState) {
                hasChanged = true;
            }

            nextState[slice] = nextSlice;
        }

        // Inclui slices sem reducer (mantém como estão)
        for (const key of Object.keys(prevState)) {
            if (!this._reducers.has(key)) {
                nextState[key] = prevState[key];
            }
        }

        return hasChanged ? nextState : prevState;
    }

    // ─── Subscriptions ──────────────────────────────────────

    subscribe(callback) {
        if (typeof callback !== 'function') {
            this._log('error', 'subscribe: callback must be a function');
            return () => {};
        }

        this._subscribers.add(callback);

        // Retorna unsubscribe
        return () => {
            this._subscribers.delete(callback);
        };
    }

    watch(slice, callback) {
        if (typeof callback !== 'function') {
            this._log('error', `watch(${slice}): callback must be a function`);
            return () => {};
        }

        let previousValue = this._state[slice];

        const subscriber = (action, prevState, nextState) => {
            const currentValue = nextState[slice];
            if (currentValue !== previousValue) {
                callback(currentValue, previousValue, action);
                previousValue = currentValue;
            }
        };

        // Wrap para receber os parâmetros corretos
        const wrapped = (action, prevState) => {
            subscriber(action, prevState, this._state);
        };

        this._subscribers.add(wrapped);

        return () => {
            this._subscribers.delete(wrapped);
        };
    }

    watchPath(path, callback) {
        const keys = path.split('.');
        if (!callback) return () => {};

        let previousValue = this._resolvePath(this._state, keys);

        const wrapped = (action) => {
            const currentValue = this._resolvePath(this._state, keys);
            if (currentValue !== previousValue) {
                callback(currentValue, previousValue, action);
                previousValue = currentValue;
            }
        };

        this._subscribers.add(wrapped);

        return () => {
            this._subscribers.delete(wrapped);
        };
    }

    unsubscribe(callback) {
        this._subscribers.delete(callback);
    }

    unsubscribeAll() {
        this._subscribers.clear();
    }

    // ─── Batch ──────────────────────────────────────────────

    batch(callback) {
        this._batchDepth++;
        try {
            callback();
        } finally {
            this._batchDepth--;
            if (this._batchDepth === 0) {
                this._flushBatch();
            }
        }
    }

    _flushBatch() {
        for (const subscriber of this._pendingSubscribers) {
            try {
                subscriber(this._lastAction, this._lastPrevState);
            } catch (e) {
                this._log('error', 'batch subscriber error', e);
            }
        }
        this._pendingSubscribers.clear();
    }

    // ─── Middleware ─────────────────────────────────────────

    use(middleware) {
        if (typeof middleware !== 'function') {
            this._log('error', 'use: middleware must be a function');
            return this;
        }
        this._middlewares.push(middleware);
        return this;
    }

    _applyMiddlewares(action, prevState) {
        if (this._middlewares.length === 0) return action;

        let result = action;

        for (const middleware of this._middlewares) {
            try {
                const returned = middleware({
                    action: result,
                    prevState,
                    getState: () => this._state,
                    dispatch: (act) => this.dispatch(act),
                    next: (act) => { result = act; }
                });

                if (returned === false) {
                    return false; // Cancelado
                }

                if (returned && returned !== result) {
                    result = returned;
                }
            } catch (e) {
                this._log('error', 'middleware error', e);
            }
        }

        return result;
    }

    // ─── Selectors ──────────────────────────────────────────

    select(selector) {
        if (typeof selector === 'function') {
            return selector(this._state);
        }
        if (typeof selector === 'string') {
            return this.getSlice(selector);
        }
        return this._state;
    }

    // ─── Resets ─────────────────────────────────────────────

    resetState(newState = {}) {
        const prevState = this._state;
        this._state = { ...newState };
        this._notify({ type: 'state/reset' }, prevState);
        return this;
    }

    resetSlice(slice, initialState) {
        const prevState = this._state;
        const existing = this._reducers.has(slice)
            ? this._reducers.get(slice)(undefined, { type: '__init__' })
            : (initialState !== undefined ? initialState : {});

        this._state = { ...this._state, [slice]: existing };
        this._notify({ type: `state/reset/${slice}` }, prevState);
        return this;
    }

    // ─── Controle ───────────────────────────────────────────

    enable() { this._enabled = true; }
    disable() { this._enabled = false; }
    clearHistory() { this._history = []; }

    setMaxHistory(max) {
        this._maxHistory = max;
        if (this._history.length > this._maxHistory) {
            this._history = this._history.slice(-this._maxHistory);
        }
    }

    // ─── Getters ────────────────────────────────────────────

    history(limit = 10) {
        return this._history.slice(-limit);
    }

    getActionCount() {
        return this._id;
    }

    getReducerNames() {
        return Array.from(this._reducers.keys());
    }

    stats() {
        return {
            slices: this._reducers.size,
            subscribers: this._subscribers.size,
            middlewares: this._middlewares.length,
            totalActions: this._id,
            historyLength: this._history.length,
            enabled: this._enabled
        };
    }

    // ─── Destruição ─────────────────────────────────────────

    destroy() {
        this._subscribers.clear();
        this._reducers.clear();
        this._middlewares = [];
        this._history = [];
        this._state = {};
        this._enabled = false;
    }

    // ─── Internos ───────────────────────────────────────────

    _notify(action, prevState) {
        if (this._batchDepth > 0) {
            this._lastAction = action;
            this._lastPrevState = prevState;
            for (const subscriber of this._subscribers) {
                this._pendingSubscribers.add(subscriber);
            }
            return;
        }

        for (const subscriber of this._subscribers) {
            try {
                subscriber(action, prevState);
            } catch (e) {
                this._log('error', 'subscriber error', e);
            }
        }
    }

    _emitEventBus(action, prevState) {
        if (!this.framework || !this.framework.events) return;

        const bus = this.framework.events;

        bus.emit('state:before-change', {
            source: 'StateManager',
            action: action.type,
            prevState
        });

        bus.emit('state:change', {
            source: 'StateManager',
            action: action.type,
            state: this._state
        });

        // Evento por slice alterada
        const slice = action.type.split('/')[0];
        if (slice && this._reducers.has(slice)) {
            bus.emit(`state:change:${slice}`, {
                source: 'StateManager',
                action: action.type,
                slice: this._state[slice]
            });
        }

        // Evento de erro se action tiver erro
        if (action.error) {
            bus.emit('state:error', {
                source: 'StateManager',
                action: action.type,
                error: action.payload
            });
        }
    }

    _resolvePath(obj, keys) {
        let current = obj;
        for (const key of keys) {
            if (current == null) return undefined;
            current = current[key];
        }
        return current;
    }

    _log(level, message, error = null) {
        if (this.framework && this.framework.log) {
            this.framework.log(level, `StateManager: ${message}`, error);
        } else if (level === 'error') {
            console.error(`[StateManager] ${message}`, error || '');
        } else if (level === 'warn') {
            console.warn(`[StateManager] ${message}`);
        } else if (level === 'debug' && this.framework && this.framework.config && this.framework.config.debug) {
            console.log(`[StateManager] ${message}`);
        }
    }
}
```

## 4.2 Resumo da API

| Método | Descrição |
|--------|-----------|
| `getState()` | Retorna árvore de estado completa |
| `getSlice(key)` | Retorna uma fatia do estado |
| `addReducer(slice, reducer)` | Registra reducer para uma fatia |
| `addReducers(reducers)` | Registra múltiplos reducers |
| `hasReducer(slice)` | Verifica se reducer existe |
| `dispatch(action)` | Dispara ação e computa novo estado |
| `subscribe(callback)` | Inscreve callback em toda mudança |
| `watch(slice, callback)` | Escuta mudanças em uma fatia específica |
| `watchPath(path, callback)` | Escuta mudanças em um caminho aninhado |
| `unsubscribe(callback)` | Remove inscrição |
| `unsubscribeAll()` | Remove todas inscrições |
| `batch(callback)` | Agrupa múltiplos dispatches em uma notificação |
| `use(middleware)` | Adiciona middleware |
| `select(selector)` | Aplica seletor ao estado atual |
| `resetState(newState)` | Substitui estado completo |
| `resetSlice(slice)` | Reseta fatia ao estado inicial |
| `enable()` | Habilita dispatches |
| `disable()` | Desabilita dispatches |
| `clearHistory()` | Limpa histórico |
| `setMaxHistory(max)` | Define tamanho máximo do histórico |
| `history(limit)` | Retorna histórico de ações |
| `getActionCount()` | Número total de actions disparadas |
| `getReducerNames()` | Lista nomes dos reducers |
| `stats()` | Estatísticas do state manager |
| `destroy()` | Remove tudo |

---

# 5. Store

## 5.1 Estrutura da Store

```js
const store = FiscalUI.state;

// Estado inicial (após registro dos reducers)
store.getState();
// {
//     user: { logged: false },
//     ui: { theme: 'light', sidebar: true },
//     nfe: { list: [], loading: false },
//     notification: { items: [] }
// }
```

## 5.2 Acesso ao Estado

```js
// Estado completo
const state = store.getState();

// Fatia específica
const user = store.getSlice('user');
const nfe = store.getSlice('nfe');

// Via seletor
const userName = store.select(state => state.user.name);
const nfeList = store.select(state => state.nfe.list);
```

---

# 6. State (Árvore de Estado)

## 6.1 Formato

O estado global é um objeto plano onde cada chave é uma fatia (slice) gerenciada por um reducer:

```js
{
    user: {
        id: null,
        name: null,
        email: null,
        logged: false,
        permissions: []
    },
    ui: {
        theme: 'light',
        sidebar: true,
        modal: null,
        loading: false
    },
    nfe: {
        list: [],
        selected: null,
        loading: false,
        error: null,
        pagination: { page: 1, total: 0 }
    },
    notification: {
        items: []
    }
}
```

## 6.2 Convenções

```
1. Estado é sempre um objeto (nunca array, string, número)
2. Cada slice é gerenciada por exatamente um reducer
3. Slice é nomeada no singular: user, nfe, ui
4. Estado mínimo — apenas o necessário para a UI
5. Sem dados duplicados entre slices (normalizado)
```

---

# 7. Actions

## 7.1 Formato

```js
{
    type: 'sliceName/actionName',   // Obrigatório
    payload: { ... },               // Opcional — dados da ação
    error: false,                    // Opcional — true se for erro
    meta: { ... }                    // Opcional — metadados (não afetam estado)
}
```

## 7.2 Convenção de Nomes

```
sliceName/actionName
```

| Parte | Descrição | Exemplo |
|-------|-----------|---------|
| sliceName | Fatia do estado que a ação afeta | `user`, `nfe`, `ui` |
| actionName | Verbo no passado que descreve o que aconteceu | `login`, `loaded`, `updated` |

```
✅ user/login
✅ user/logout
✅ nfe/load
✅ nfe/loaded
✅ nfe/error
✅ ui/toggleSidebar
✅ ui/setTheme

❌ LOGIN_USER           (maiúsculo)
❌ setUserLogin         (não segue padrão)
❌ user_login           (underscore)
❌ User/Login           (maiúsculo no slice)
```

## 7.3 Action Creators (Helpers)

```js
// Conveniência — não obrigatório, mas recomendado
const actions = {
    login: (user) => ({ type: 'user/login', payload: user }),
    logout: () => ({ type: 'user/logout' }),
    nfeLoad: () => ({ type: 'nfe/load' }),
    nfeLoaded: (list) => ({ type: 'nfe/loaded', payload: list }),
    nfeError: (error) => ({ type: 'nfe/error', payload: error, error: true })
};

// Uso
store.dispatch(actions.login({ id: 1, name: 'João' }));
store.dispatch(actions.nfeLoad());
```

---

# 8. Reducers

## 8.1 Definição

Reducers são funções puras que recebem o estado atual + uma ação e retornam o novo estado:

```js
function userReducer(state = initialState, action) {
    switch (action.type) {
        case 'user/login':
            return { ...state, ...action.payload, logged: true };
        case 'user/logout':
            return { ...initialState };
        case 'user/update':
            return { ...state, ...action.payload };
        default:
            return state;
    }
}

const initialState = {
    id: null,
    name: null,
    email: null,
    logged: false,
    permissions: []
};
```

## 8.2 Registro

```js
// Individual
store.addReducer('user', userReducer);
store.addReducer('nfe', nfeReducer);
store.addReducer('ui', uiReducer);

// Múltiplos de uma vez
store.addReducers({
    user: userReducer,
    nfe: nfeReducer,
    ui: uiReducer,
    notification: notificationReducer
});
```

## 8.3 Estado Inicial

```js
// O reducer recebe undefined na inicialização
// e deve retornar o estado inicial para o slice:

function userReducer(state = { logged: false, name: null }, action) {
    // Se state é undefined, usa o valor padrão → estado inicial
    switch (action.type) { ... }
}

// Equivalente manual:
// store.dispatch({ type: '__init__' }) é chamado automaticamente
// no addReducer() se o slice ainda não existir
```

## 8.4 Reducers Aninhados (Combinando)

```js
// Em vez de um reducer gigante, componha reducers menores:

const initialState = {
    list: [],
    selected: null,
    loading: false,
    error: null
};

function nfeListReducer(state = [], action) {
    switch (action.type) {
        case 'nfe/loaded':
            return action.payload;
        case 'nfe/clear':
            return [];
        default:
            return state;
    }
}

function nfeSelectedReducer(state = null, action) {
    switch (action.type) {
        case 'nfe/select':
            return action.payload;
        case 'nfe/clear':
            return null;
        default:
            return state;
    }
}

function nfeReducer(state = initialState, action) {
    return {
        list: nfeListReducer(state.list, action),
        selected: nfeSelectedReducer(state.selected, action),
        loading: loadingReducer(state.loading, action),
        error: errorReducer(state.error, action)
    };
}
```

---

# 9. Dispatch

## 9.1 Disparo de Ações

```js
// Disparo direto
store.dispatch({ type: 'user/login', payload: { id: 1, name: 'João' } });
store.dispatch({ type: 'nfe/load' });
store.dispatch({ type: 'ui/toggleSidebar' });

// Com action creator
store.dispatch(actions.login(user));
store.dispatch(actions.nfeLoaded(data));
```

## 9.2 Dispatch em Componentes

```js
class LoginButton extends UIComponent {
    handleClick() {
        // Componente acessa state manager via framework
        FiscalUI.state.dispatch({
            type: 'user/login',
            payload: { id: 1, name: 'João', role: 'admin' }
        });

        // Ou via EventBus (delegado pelo StateManager)
        FiscalUI.events.emit('user:login', { id: 1, name: 'João' });
    }
}
```

## 9.3 Dispatch com Erro

```js
try {
    const data = await api.get('/nfe');
    store.dispatch({ type: 'nfe/loaded', payload: data });
} catch (error) {
    store.dispatch({
        type: 'nfe/error',
        payload: error.message,
        error: true
    });
}
```

---

# 10. Subscriptions

## 10.1 subscribe() — Toda Mudança

```js
const unsubscribe = store.subscribe((action, prevState) => {
    console.log('Ação:', action.type);
    console.log('Estado anterior:', prevState);
    console.log('Estado atual:', store.getState());
});

// Para de escutar
unsubscribe();
```

## 10.2 watch() — Fatia Específica

```js
// Escuta apenas mudanças no slice 'user'
const unsub = store.watch('user', (current, previous, action) => {
    if (current.logged !== previous.logged) {
        console.log('Login mudou:', current.logged);
        updateUI(current);
    }
});
```

## 10.3 watchPath() — Caminho Aninhado

```js
// Escuta apenas nfe.pagination.page
const unsub = store.watchPath('nfe.pagination.page', (page, prevPage) => {
    console.log(`Página mudou: ${prevPage} → ${page}`);
    loadPage(page);
});
```

## 10.4 Em Componentes

```js
class UserProfile extends UIComponent {
    init() {
        this._unsub = FiscalUI.state.watch('user', (user) => {
            this.render(user);
        });
    }

    destroy() {
        if (this._unsub) this._unsub();
    }
}
```

---

# 11. Selectors

## 11.1 Definição

Selectors são funções que extraem e derivam dados do estado:

```js
// Seletor simples
const getUsers = (state) => state.user;

// Seletor derivado (computa novo dado)
const getActiveNFEs = (state) =>
    state.nfe.list.filter(nfe => nfe.status === 'ativo');

// Seletor com parâmetros
const getNFEById = (state, id) =>
    state.nfe.list.find(nfe => nfe.id === id);

// Seletor memoizado (cache de resultado)
function createSelector(fn) {
    let lastState = null;
    let lastResult = null;
    return (state) => {
        if (state !== lastState) {
            lastState = state;
            lastResult = fn(state);
        }
        return lastResult;
    };
}

const getTotalNFEs = createSelector((state) => state.nfe.list.length);
```

## 11.2 Uso

```js
// Via store.select()
const user = store.select((state) => state.user);
const activeNFEs = store.select(getActiveNFEs);
const nfe42 = store.select((state) => getNFEById(state, 42));

// Via getSlice() para acesso direto
const user = store.getSlice('user');
const nfe = store.getSlice('nfe');
```

---

# 12. Middleware

## 12.1 Definição

Middleware intercepta ações antes delas chegarem aos reducers. Pode modificar, cancelar, logar, ou disparar efeitos colaterais.

```js
store.use(({ action, prevState, getState, dispatch, next }) => {
    // action: a ação que foi disparada
    // prevState: estado antes do dispatch
    // getState: () => estado atual
    // dispatch: (action) => dispara nova ação
    // next: (action) → passa para o próximo middleware

    console.log('Middleware:', action.type);

    // Pode modificar a ação
    const enhancedAction = {
        ...action,
        meta: { ...action.meta, timestamp: Date.now() }
    };

    // Passa para o próximo middleware (ou reducer)
    next(enhancedAction);
});
```

## 12.2 Logger Middleware

```js
store.use(({ action, prevState, getState }) => {
    console.group(`Action: ${action.type}`);
    console.log('Prev State:', prevState);
    console.log('Action:', action);
    console.log('Next State:', getState());
    console.groupEnd();
});
```

## 12.3 Throttle Middleware

```js
const timers = {};

store.use(({ action, next }) => {
    const throttleActions = ['nfe/load', 'ui/resize'];

    if (throttleActions.includes(action.type)) {
        if (timers[action.type]) return; // Ignora se já disparou recentemente

        timers[action.type] = setTimeout(() => {
            delete timers[action.type];
        }, 300);

        next(action);
    } else {
        next(action);
    }
});
```

## 12.4 Cancelamento de Ações

```js
// Middleware que bloqueia ações se usuário não tem permissão
store.use(({ action, getState, next }) => {
    const restricted = ['admin/delete', 'admin/update'];
    const user = getState().user;

    if (restricted.includes(action.type) && !user.permissions.includes('admin')) {
        console.warn(`Ação ${action.type} bloqueada — sem permissão`);
        return false; // Cancela a ação
    }

    next(action);
});
```

## 12.5 Efeitos Colaterais

```js
// Middleware que dispara requisições HTTP
store.use(({ action, dispatch }) => {
    if (action.type === 'nfe/load') {
        dispatch({ type: 'nfe/loading' });

        api.get('/nfe')
            .then(data => dispatch({ type: 'nfe/loaded', payload: data }))
            .catch(err => dispatch({ type: 'nfe/error', payload: err.message, error: true }));
    }

    // Não usa next() — a ação original nfe/load não chega ao reducer
    // (apenas as derivadas: nfe/loading, nfe/loaded, nfe/error)
});
```

---

# 13. Async Actions

## 13.1 Padrão com Middleware

```js
// 1. Dispatch ação de início
store.dispatch({ type: 'nfe/loading' });

// 2. Operação assíncrona
api.get('/nfe')
    .then(data => store.dispatch({ type: 'nfe/loaded', payload: data }))
    .catch(err => store.dispatch({ type: 'nfe/error', payload: err.message, error: true }));
```

## 13.2 Thunk Pattern (Ação Assíncrona)

```js
function loadNFEs() {
    return async (dispatch, getState) => {
        dispatch({ type: 'nfe/loading' });

        try {
            const data = await api.get('/nfe');
            dispatch({ type: 'nfe/loaded', payload: data });
        } catch (err) {
            dispatch({ type: 'nfe/error', payload: err.message, error: true });
        }
    };
}

// Middleware thunk
store.use(({ action, dispatch, getState }) => {
    if (typeof action === 'function') {
        return action(dispatch, getState);
    }
    next(action);
});

// Uso
store.dispatch(loadNFEs());
```

## 13.3 Reducer para Loading

```js
function nfeReducer(state = initialState, action) {
    switch (action.type) {
        case 'nfe/loading':
            return { ...state, loading: true, error: null };
        case 'nfe/loaded':
            return { ...state, list: action.payload, loading: false };
        case 'nfe/error':
            return { ...state, error: action.payload, loading: false };
        default:
            return state;
    }
}
```

---

# 14. Estado Imutável

## 14.1 Atualização Segura

```js
// ❌ Mutação direta
state.user.name = 'João'; // NÃO FAÇA ISSO

// ✅ Cópia com spread
const newState = {
    ...state,
    user: { ...state.user, name: 'João' }
};

// ✅ Atualização de array
const newList = [...state.nfe.list, newItem];
const updatedList = state.nfe.list.map(item =>
    item.id === id ? { ...item, status: 'cancelado' } : item
);
const filteredList = state.nfe.list.filter(item => item.status !== 'cancelado');
```

## 14.2 Immer-like Helper (Opcional)

```js
// Helper para atualização imutável (similar Immer)
function produce(state, recipe) {
    const draft = JSON.parse(JSON.stringify(state));
    recipe(draft);
    return draft;
}

// Uso em reducer
function nfeReducer(state, action) {
    switch (action.type) {
        case 'nfe/updateStatus':
            return produce(state, (draft) => {
                const item = draft.list.find(nfe => nfe.id === action.payload.id);
                if (item) item.status = action.payload.status;
            });
        default:
            return state;
    }
}
```

---

# 15. Estado Normalizado

## 15.1 Por que Normalizar?

```js
// ❌ Desnormalizado — dados duplicados, difícil de atualizar
{
    nfe: {
        list: [
            { id: 1, emissor: { id: 10, nome: 'Empresa A' }, itens: [...] },
            { id: 2, emissor: { id: 10, nome: 'Empresa A' }, itens: [...] }
        ]
        // Se o nome da Empresa A mudar, precisa atualizar em TODOS os lugares
    }
}

// ✅ Normalizado — dados únicos, atualização pontual
{
    nfe: {
        byId: {
            1: { id: 1, emissorId: 10, itens: [...] },
            2: { id: 2, emissorId: 10, itens: [...] }
        },
        ids: [1, 2]
    },
    emissor: {
        byId: {
            10: { id: 10, nome: 'Empresa A', cnpj: '...' }
        }
    }
}
```

## 15.2 Reducers com Estado Normalizado

```js
function nfeReducer(state = { byId: {}, ids: [] }, action) {
    switch (action.type) {
        case 'nfe/loaded':
            return {
                byId: action.payload.reduce((acc, nfe) => {
                    acc[nfe.id] = nfe;
                    return acc;
                }, {}),
                ids: action.payload.map(nfe => nfe.id)
            };
        case 'nfe/add':
            return {
                byId: { ...state.byId, [action.payload.id]: action.payload },
                ids: [...state.ids, action.payload.id]
            };
        case 'nfe/remove':
            const { [action.payload]: _, ...rest } = state.byId;
            return {
                byId: rest,
                ids: state.ids.filter(id => id !== action.payload)
            };
        default:
            return state;
    }
}
```

---

# 16. Slice (Fatia de Estado)

## 16.1 Organização Recomendada

```js
// Cada slice em seu próprio arquivo
store/
├── index.js              // Configuração do store
├── slices/
│   ├── userSlice.js      // user reducer + actions
│   ├── nfeSlice.js       // nfe reducer + actions
│   ├── uiSlice.js        // ui reducer + actions
│   └── notificationSlice.js
└── selectors/
    ├── userSelectors.js
    └── nfeSelectors.js
```

## 16.2 Exemplo de Slice

```js
// slices/nfeSlice.js
const initialState = {
    byId: {},
    ids: [],
    selectedId: null,
    loading: false,
    error: null,
    pagination: { page: 1, pageSize: 20, total: 0 }
};

function nfeReducer(state = initialState, action) {
    switch (action.type) {
        case 'nfe/loading':
            return { ...state, loading: true, error: null };
        case 'nfe/loaded':
            return {
                ...state,
                byId: normalizeArray(action.payload, 'id'),
                ids: action.payload.map(n => n.id),
                loading: false,
                pagination: { ...state.pagination, total: action.payload.length }
            };
        case 'nfe/select':
            return { ...state, selectedId: action.payload };
        case 'nfe/error':
            return { ...state, error: action.payload, loading: false };
        case 'nfe/setPage':
            return { ...state, pagination: { ...state.pagination, page: action.payload } };
        default:
            return state;
    }
}

// Helpers
function normalizeArray(arr, key = 'id') {
    return arr.reduce((acc, item) => {
        acc[item[key]] = item;
        return acc;
    }, {});
}

export { nfeReducer, initialState };
```

---

# 17. Estado de Componentes

## 17.1 Estado Local vs Global

```
Estado Local (componente):          Estado Global (store):
  - Input value                       - Usuário logado
  - Dropdown aberto/fechado           - Lista de NFEs
  - Tab ativa                         - Tema atual
  - Tooltip visível                   - Preferências do sistema
  - Animação em andamento             - Dados de domínio
```

## 17.2 Quando Usar Cada Um

```js
// ✅ Estado local — só interessa ao componente
class Dropdown extends UIComponent {
    constructor() {
        this._open = false; // Estado local, não vai para store
    }
    toggle() {
        this._open = !this._open;
        this.render();
    }
}

// ✅ Estado global — interessa a múltiplos componentes
store.dispatch({ type: 'user/login', payload: user });
// Vários componentes escutam e reagem:
store.watch('user', (user) => this.updateHeader(user));
store.watch('user', (user) => this.updateSidebar(user));
```

## 17.3 Sincronização com ComponentBase

```js
class UIDataGrid extends UIComponent {
    init() {
        // Componente lê da store
        this.state = FiscalUI.state;

        // Escuta mudanças relevantes
        this._unsub = this.state.watch('nfe', (nfe) => {
            this.updateGrid(nfe);
        });
    }

    onSort(column) {
        // Componente escreve na store
        this.state.dispatch({
            type: 'nfe/sort',
            payload: { column, direction: 'asc' }
        });
    }

    destroy() {
        if (this._unsub) this._unsub();
    }
}
```

---

# 18. Integração com EventBus

## 18.1 Eventos Emitidos

```js
'state:before-change'       // Antes da mudança de estado
'state:change'              // Estado global mudou
'state:change:{slice}'      // Slice específico mudou (ex: state:change:user)
'state:error'               // Erro em ação (action.error === true)
```

## 18.2 Escutando Mudanças via EventBus

```js
FiscalUI.events.on('state:change', ({ action, state }) => {
    console.log(`Estado mudou via ação: ${action}`);
});

FiscalUI.events.on('state:change:user', ({ slice }) => {
    console.log('Usuário atualizado:', slice);
});

FiscalUI.events.on('state:change:nfe', ({ slice }) => {
    console.log('NFE atualizada:', slice);
});

FiscalUI.events.on('state:error', ({ action, error }) => {
    console.error(`Erro em ${action}:`, error);
});
```

---

# 19. Persistência

## 19.1 Salvando Estado

```js
// Salvar slices específicas no localStorage
function saveState(state) {
    try {
        localStorage.setItem('fiscalui_user', JSON.stringify(state.user));
        localStorage.setItem('fiscalui_ui', JSON.stringify(state.ui));
    } catch (e) {
        console.warn('Não foi possível salvar estado:', e);
    }
}

// Middleware de persistência
store.use(({ action, getState }) => {
    const persistSlices = ['user', 'ui'];

    next(action);

    const state = getState();
    for (const slice of persistSlices) {
        if (state[slice] !== undefined) {
            try {
                localStorage.setItem(`fiscalui_${slice}`, JSON.stringify(state[slice]));
            } catch (e) { /* quota excedida */ }
        }
    }
});
```

## 19.2 Restaurando Estado

```js
function loadPersistedState() {
    const state = {};
    const slices = ['user', 'ui'];

    for (const slice of slices) {
        try {
            const saved = localStorage.getItem(`fiscalui_${slice}`);
            if (saved) {
                state[slice] = JSON.parse(saved);
            }
        } catch (e) { /* ignorar */ }
    }

    return state;
}

// Na inicialização
const persistedState = loadPersistedState();
store.resetState({ ...initialState, ...persistedState });
```

---

# 20. DevTools

## 20.1 Time Travel Debugging

```js
// Histórico completo de ações
const history = store.history(50);

// Cada entrada:
{
    id: 42,
    action: { type: 'user/login', payload: { id: 1 } },
    prevState: { user: { logged: false }, ... },
    nextState: { user: { logged: true, id: 1 }, ... },
    timestamp: 1703456789012
}

// Via EventBus para DevTools
FiscalUI.events.on('state:change', ({ action, state }) => {
    devTools.addEntry({ action, state, timestamp: Date.now() });
});
```

## 20.2 Relatório de Estado

```js
const report = {
    stats: store.stats(),
    slices: store.getReducerNames(),
    lastActions: store.history(5)
};

console.table(report.stats);
// ┌───────────────┬──────┐
// │ slices        │ 4    │
// │ subscribers   │ 3    │
// │ middlewares   │ 2    │
// │ totalActions  │ 27   │
// │ historyLength │ 27   │
// │ enabled       │ true │
// └───────────────┴──────┘
```

---

# 21. Performance

## 21.1 Métricas

| Operação | Performance | Complexidade |
|----------|-------------|--------------|
| `getState()` | < 0.001ms | O(1) |
| `getSlice()` | < 0.001ms | O(1) |
| `dispatch()` (10 slices) | < 0.1ms | O(n) onde n = slices |
| `dispatch()` (50 slices) | < 0.5ms | O(n) |
| `subscribe()` | < 0.01ms | O(1) |
| `watch()` | < 0.01ms | O(1) |
| `batch()` (10 dispatches) | < 0.3ms | O(n) |
| Histórico (append) | < 0.001ms | O(1) |

## 21.2 Otimizações

```js
// 1. Use watch() em vez de subscribe() para escutar apenas slices relevantes
✅ store.watch('nfe', callback)
❌ store.subscribe(callback) // recebe toda mudança

// 2. Use batch() para agrupar múltiplos dispatches
✅ store.batch(() => {
    store.dispatch({ type: 'a' });
    store.dispatch({ type: 'b' });
    store.dispatch({ type: 'c' });
}); // Uma única notificação

// 3. Reduza o histórico em produção
✅ store.setMaxHistory(10)

// 4. Remova subscribers quando não necessários
✅ const unsub = store.watch('user', callback);
// quando sair da tela:
✅ unsub();

// 5. Use selectores memoizados para computações pesadas
✅ const getTotal = createSelector(state => state.nfe.list.length);
```

---

# 22. Memória

## 22.1 Prevenção de Vazamentos

```js
class NFEPanel extends UIComponent {
    init() {
        // Guarda referência do unsubscribe
        this._watchers = [];

        this._watchers.push(
            FiscalUI.state.watch('nfe', (nfe) => this.render(nfe))
        );

        this._watchers.push(
            FiscalUI.state.watch('user', (user) => this.updatePermissions(user))
        );
    }

    destroy() {
        // Remove todos watchers
        this._watchers.forEach(unsub => unsub());
        this._watchers = [];
    }
}

// Auto cleanup via ComponentBase
class UIComponent {
    destroy() {
        this._watchers?.forEach(unsub => unsub());
        this._watchers = null;
    }
}
```

## 22.2 Histórico

```js
// Histórico pode crescer indefinidamente se não limitado
store.setMaxHistory(50); // Limite seguro

// Ou desabilitar histórico em produção
if (process.env.NODE_ENV === 'production') {
    store.clearHistory();
    store.setMaxHistory(0);
}
```

---

# 23. Testes

## 23.1 Teste Unitário

```js
describe('StateManager', () => {
    let store;

    beforeEach(() => {
        store = new StateManager();
    });

    afterEach(() => {
        store.destroy();
    });

    it('should initialize with empty state', () => {
        expect(store.getState()).toEqual({});
    });

    it('should register reducers', () => {
        store.addReducer('counter', (state = 0, action) => {
            switch (action.type) {
                case 'counter/increment':
                    return state + 1;
                case 'counter/decrement':
                    return state - 1;
                default:
                    return state;
            }
        });

        expect(store.getSlice('counter')).toBe(0);
    });

    it('should compute new state on dispatch', () => {
        store.addReducer('counter', (state = 0, action) => {
            return action.type === 'counter/increment' ? state + 1 : state;
        });

        store.dispatch({ type: 'counter/increment' });
        expect(store.getSlice('counter')).toBe(1);

        store.dispatch({ type: 'counter/increment' });
        expect(store.getSlice('counter')).toBe(2);
    });

    it('should notify subscribers on dispatch', () => {
        store.addReducer('test', (state = '') => state);
        const spy = jasmine.createSpy();
        store.subscribe(spy);

        store.dispatch({ type: 'test/action' });
        expect(spy).toHaveBeenCalled();
    });

    it('should notify watchers on slice change', () => {
        store.addReducer('counter', (state = 0, action) => {
            return action.type === 'counter/increment' ? state + 1 : state;
        });

        const spy = jasmine.createSpy();
        store.watch('counter', spy);

        store.dispatch({ type: 'counter/increment' });
        expect(spy).toHaveBeenCalledWith(1, 0, jasmine.any(Object));
    });

    it('should not notify watchers if slice did not change', () => {
        store.addReducer('counter', (state = 0, action) => {
            return action.type === 'counter/increment' ? state + 1 : state;
        });

        const spy = jasmine.createSpy();
        store.watch('counter', spy);

        store.dispatch({ type: 'other/action' });
        expect(spy).not.toHaveBeenCalled();
    });

    it('should support middlewares', () => {
        store.addReducer('test', (state = '', action) => {
            return action.type === 'test/set' ? action.payload : state;
        });

        const spy = jasmine.createSpy();
        store.use(({ action, next }) => {
            spy(action.type);
            next(action);
        });

        store.dispatch({ type: 'test/set', payload: 'hello' });
        expect(spy).toHaveBeenCalledWith('test/set');
        expect(store.getSlice('test')).toBe('hello');
    });

    it('should cancel action if middleware returns false', () => {
        store.addReducer('test', (state = 0, action) => {
            return action.type === 'test/set' ? action.payload : state;
        });

        store.use(({ action }) => {
            if (action.payload === 'blocked') return false;
            next(action);
        });

        store.dispatch({ type: 'test/set', payload: 'blocked' });
        expect(store.getSlice('test')).toBe(0);
    });

    it('should support batch dispatching', () => {
        store.addReducer('counter', (state = 0, action) => {
            return action.type === 'counter/increment' ? state + 1 : state;
        });

        const spy = jasmine.createSpy();
        store.subscribe(spy);

        store.batch(() => {
            store.dispatch({ type: 'counter/increment' });
            store.dispatch({ type: 'counter/increment' });
            store.dispatch({ type: 'counter/increment' });
        });

        expect(store.getSlice('counter')).toBe(3);
        expect(spy.calls.count()).toBe(1); // Apenas uma notificação
    });

    it('should support watchPath', () => {
        store.addReducer('nfe', (state = { pagination: { page: 1 } }, action) => {
            if (action.type === 'nfe/setPage') {
                return {
                    ...state,
                    pagination: { ...state.pagination, page: action.payload }
                };
            }
            return state;
        });

        const spy = jasmine.createSpy();
        store.watchPath('nfe.pagination.page', spy);

        store.dispatch({ type: 'nfe/setPage', payload: 3 });
        expect(spy).toHaveBeenCalledWith(3, 1, jasmine.any(Object));
    });

    it('should return unsubscribe function from subscribe/watch', () => {
        store.addReducer('test', (state = 0) => state);
        const subSpy = jasmine.createSpy();
        const watchSpy = jasmine.createSpy();

        const unsub1 = store.subscribe(subSpy);
        const unsub2 = store.watch('test', watchSpy);

        unsub1();
        unsub2();

        store.dispatch({ type: 'test/action' });
        expect(subSpy).not.toHaveBeenCalled();
        expect(watchSpy).not.toHaveBeenCalled();
    });

    it('should maintain action history', () => {
        store.addReducer('test', (state = 0) => state);
        store.dispatch({ type: 'test/one' });
        store.dispatch({ type: 'test/two' });

        const history = store.history();
        expect(history.length).toBe(2);
        expect(history[0].action.type).toBe('test/one');
        expect(history[1].action.type).toBe('test/two');
    });

    it('should support select()', () => {
        store.addReducer('user', (state = { name: 'João' }) => state);
        const name = store.select(state => state.user.name);
        expect(name).toBe('João');
    });

    it('should support resetState and resetSlice', () => {
        store.addReducer('a', (state = 1) => state);
        store.addReducer('b', (state = 2) => state);

        store.resetState({ x: 10 });
        expect(store.getSlice('x')).toBe(10);
        expect(store.getSlice('a')).toBeUndefined();

        store.addReducer('counter', (state = 0) => state);
        store.resetSlice('counter');
        expect(store.getSlice('counter')).toBe(0);
    });
});
```

## 23.2 Teste de Reducers

```js
describe('nfeReducer', () => {
    it('should return initial state', () => {
        const state = nfeReducer(undefined, { type: '__init__' });
        expect(state.list).toEqual([]);
        expect(state.loading).toBe(false);
    });

    it('should handle nfe/loading', () => {
        const state = nfeReducer(undefined, { type: 'nfe/loading' });
        expect(state.loading).toBe(true);
    });

    it('should handle nfe/loaded', () => {
        const data = [{ id: 1, chave: '123' }];
        const state = nfeReducer({ list: [], loading: true }, {
            type: 'nfe/loaded',
            payload: data
        });
        expect(state.list).toEqual(data);
        expect(state.loading).toBe(false);
    });

    it('should not mutate previous state', () => {
        const prev = { list: [{ id: 1 }], loading: true };
        const next = nfeReducer(prev, {
            type: 'nfe/loaded',
            payload: [{ id: 2 }]
        });
        expect(prev.list).toEqual([{ id: 1 }]); // Imutável
        expect(next.list).toEqual([{ id: 2 }]);
        expect(prev).not.toBe(next);
    });
});
```

---

# 24. Boas Práticas

## 24.1 Regras de Ouro

```
1. NUNCA mude o estado diretamente — sempre dispatch uma ação
2. NUNCA coloque no estado global o que é local do componente
3. SEMPRE use reducers puros — sem efeitos colaterais
4. NUNCA coloque componentes ou classes no estado — apenas dados seriais
5. SEMPRE normalize dados relacionados
6. NUNCA crie estado duplicado em múltiplas slices
7. SEMPRE use watch() ou watchPath() em vez de subscribe() para performance
8. NUNCA dispatch dentro de um reducer
9. SEMPRE use batch() para múltiplos dispatches relacionados
10. NUNCA dependa da ordem de execução entre subscribers
```

## 24.2 Checklist

```
☐ Estado inicial definido para cada slice
☐ Reducers são funções puras (sem efeitos colaterais)
☐ Ações seguem padrão sliceName/actionName
☐ Dados normalizados (byId + ids) quando lista
☐ watch() usado em vez de subscribe() em componentes
☐ unsubscribe() chamado no destroy() do componente
☐ Middleware para logging em desenvolvimento
☐ batch() para dispatches relacionados
☐ Histórico limitado (maxHistory)
☐ Persistência apenas para slices necessárias
```

## 24.3 Estrutura de Arquivos Recomendada

```
src/
├── store/
│   ├── index.js              // Cria e configura o store
│   ├── slices/
│   │   ├── userSlice.js
│   │   ├── nfeSlice.js
│   │   ├── uiSlice.js
│   │   └── notificationSlice.js
│   ├── selectors/
│   │   ├── userSelectors.js
│   │   └── nfeSelectors.js
│   ├── middleware/
│   │   ├── logger.js
│   │   ├── persistence.js
│   │   └── analytics.js
│   └── actions/
│       ├── userActions.js
│       └── nfeActions.js
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial — State Manager completo |
