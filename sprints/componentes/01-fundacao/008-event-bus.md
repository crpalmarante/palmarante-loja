# FiscalUI Framework

## Documento 008 — Event Bus

**Versão 1.0**

Este documento define o sistema de comunicação do FiscalUI. Pub/sub central por onde toda comunicação entre componentes, módulos, serviços e engines ocorre. Nenhum componente conversa diretamente com outro.

---

# Índice

1. Introdução
2. Filosofia
3. Arquitetura
4. API Pública
5. Eventos do Framework
6. Eventos de Componentes
7. Eventos de Serviços
8. Eventos de Estado
9. Eventos de Domínio
10. Ciclo de Vida do Evento
11. Payload
12. Assinatura
13. Cancelamento
14. Wildcards
15. Middleware
16. Prioridade
17. Async Events
18. Once Events
19. Namespaces
20. Debugging
21. Performance
22. Memória
23. Testes
24. Boas Práticas

---

# 1. Introdução

## 1.1 Propósito

O Event Bus é o sistema nervoso do FiscalUI. Ele permite que qualquer módulo do Framework se comunique com qualquer outro sem acoplamento direto. Um componente Button pode disparar um evento que um componente Toast escuta, sem que Button conheça Toast.

## 1.2 Princípio Fundamental

```
Nenhum componente chama método de outro componente diretamente.
Toda comunicação passa pelo Event Bus.
```

## 1.3 Analogia

```
Rádio:  Emissor → Antena → Rádio → Receptor
Event Bus: Componente → emit() → Event Bus → on() → Componente
```

O emissor não sabe quem está ouvindo. O ouvinte não sabe quem está emitindo. Ambos conhecem apenas o nome do evento.

---

# 2. Filosofia

## 2.1 Desacoplamento Total

```js
// ❌ Errado — acoplamento direto
class Button {
    onClick() {
        this.grid.refresh();
        this.toast.show('Salvo!');
    }
}

// ✅ Correto — via Event Bus
class Button {
    onClick() {
        FiscalUI.events.emit('document:save');
    }
}

// Em qualquer outro lugar
FiscalUI.events.on('document:save', () => grid.refresh());
FiscalUI.events.on('document:save', () => toast.show('Salvo!'));
```

## 2.2 Imutabilidade do Payload

Eventos nunca devem modificar o payload recebido. O payload é uma fotografia do estado no momento do evento.

```js
// ❌ Errado — modifica payload
FiscalUI.events.on('user:login', (payload) => {
    payload.user.name = 'Modificado'; // NÃO FAÇA ISSO
});

// ✅ Correto — cria cópia se precisar modificar
FiscalUI.events.on('user:login', (payload) => {
    const user = { ...payload.user, name: 'Modificado' };
});
```

## 2.3 Convenção de Nomes

```
namespace:action
```

| Parte | Descrição | Exemplo |
|-------|-----------|---------|
| namespace | Módulo ou componente que dispara | `button`, `modal`, `user` |
| action | O que aconteceu (passado) | `click`, `open`, `login` |

```
✅ button:click
✅ modal:open
✅ modal:close
✅ user:login
✅ user:logout
✅ data:loaded
✅ data:error
✅ framework:ready
✅ theme:change

❌ click          (sem namespace)
❌ onButtonClick  (não segue padrão)
❌ buttonClick    (não usa :)
❌ button_click   (usa underscore)
```

---

# 3. Arquitetura

## 3.1 Diagrama de Fluxo

```
┌──────────┐     emit('event')     ┌──────────────┐
│          │──────────────────────▶│              │
│ Emitter  │                       │  Event Bus   │
│ (quem    │                       │  (pub/sub)   │
│ dispara) │                       │              │
│          │                       │  ┌────────┐  │
└──────────┘                       │  │        │  │
                                   │  │ Queue  │  │
┌──────────┐                       │  │        │  │
│          │                       │  └───┬────┘  │
│ Listener │◀──────────────────────────────┘       │
│ (quem    │     on('event', cb)                  │
│ escuta)  │                                      │
│          │     Múltiplos listeners              │
└──────────┘     por evento                       │
                                   └──────────────┘
```

## 3.2 Estrutura Interna

```
EventBus
    │
    ├── _listeners: Map<event, Set<{callback, context, priority, once}>>
    │
    ├── _middlewares: Map<event, Set<Function>>
    │
    ├── _wildcards: Map<pattern, Set<Function>>
    │
    ├── _history: Array<{event, payload, timestamp}>
    │
    └── _stats: Map<event, {emitted, subscribers}>
```

## 3.3 Relação com Outros Módulos

```
EventBus
    │
    ├── FiscalUI.init() → cria EventBus
    ├── Component.init() → on() para escutar
    ├── Component.action → emit() para disparar
    ├── StateManager → emite state:change
    ├── Router → emite router:change
    ├── ThemeEngine → emite theme:change
    └── Todos os módulos se comunicam via EventBus
```

---

# 4. API Pública

## 4.1 Implementação

```js
class EventBus {
    constructor(framework = null) {
        this.framework = framework;
        this._listeners = new Map();
        this._wildcards = new Map();
        this._middlewares = new Map();
        this._history = [];
        this._maxHistory = 100;
        this._stats = new Map();
        this._id = 0;
        this._enabled = true;
    }

    // ─── Registro ──────────────────────────────────────────

    on(event, callback, context = null, options = {}) {
        if (!this._enabled) return () => {};
        if (typeof callback !== 'function') {
            console.warn(`[EventBus] on(${event}): callback must be a function`);
            return () => {};
        }

        // Suporta wildcards: "user:*"
        if (event.includes('*')) {
            return this._onWildcard(event, callback, context, options);
        }

        if (!this._listeners.has(event)) {
            this._listeners.set(event, new Map());
        }

        const id = ++this._id;
        const entry = {
            id,
            callback,
            context,
            priority: options.priority || 0,
            once: options.once || false,
            async: options.async || false
        };

        this._listeners.get(event).set(id, entry);

        // Atualiza stats
        if (!this._stats.has(event)) {
            this._stats.set(event, { emitted: 0, subscribers: 0 });
        }
        this._stats.get(event).subscribers++;

        // Retorna função de cancelamento
        return () => this.off(event, callback);
    }

    once(event, callback, context = null) {
        return this.on(event, callback, context, { once: true });
    }

    // ─── Remoção ────────────────────────────────────────────

    off(event, callback) {
        if (!this._listeners.has(event)) return;

        const listeners = this._listeners.get(event);
        for (const [id, entry] of listeners) {
            if (entry.callback === callback) {
                listeners.delete(id);
                if (this._stats.has(event)) {
                    this._stats.get(event).subscribers--;
                }
                return;
            }
        }
    }

    offAll(event = null) {
        if (event) {
            this._listeners.delete(event);
            this._stats.delete(event);
        } else {
            this._listeners.clear();
            this._stats.clear();
        }
    }

    // ─── Disparo ────────────────────────────────────────────

    emit(event, payload = {}, options = {}) {
        if (!this._enabled) return;

        const timestamp = Date.now();
        const envelope = {
            event,
            payload,
            timestamp,
            id: `${event}_${timestamp}_${++this._id}`
        };

        // Histórico
        if (options.history !== false) {
            this._addToHistory(envelope);
        }

        // Stats
        if (!this._stats.has(event)) {
            this._stats.set(event, { emitted: 0, subscribers: 0 });
        }
        this._stats.get(event).emitted++;

        // Middlewares
        if (!this._runMiddlewares(event, envelope)) {
            return; // Evento cancelado por middleware
        }

        // Debug
        if (this.framework && this.framework.config && this.framework.config.debug) {
            console.log(`[EventBus] ${event}`, payload);
        }

        // Dispara listeners
        this._dispatch(event, envelope);

        // Dispara wildcards (*:action, namespace:*)
        this._dispatchWildcards(event, envelope);
    }

    // ─── Getters ────────────────────────────────────────────

    has(event) {
        return this._listeners.has(event) && this._listeners.get(event).size > 0;
    }

    listeners(event) {
        if (!this._listeners.has(event)) return [];
        return Array.from(this._listeners.get(event).values());
    }

    events() {
        return Array.from(this._listeners.keys());
    }

    stats(event = null) {
        if (event) return this._stats.get(event) || { emitted: 0, subscribers: 0 };
        const result = {};
        for (const [ev, st] of this._stats) {
            result[ev] = st;
        }
        return result;
    }

    history(limit = 10) {
        return this._history.slice(-limit);
    }

    // ─── Controle ───────────────────────────────────────────

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

    // ─── Internos ───────────────────────────────────────────

    _dispatch(event, envelope) {
        if (!this._listeners.has(event)) return;

        const listeners = this._listeners.get(event);
        const sorted = Array.from(listeners.values())
            .sort((a, b) => b.priority - a.priority);

        for (const entry of sorted) {
            try {
                if (entry.async) {
                    // Async: schedule para não bloquear
                    setTimeout(() => {
                        entry.callback.call(entry.context || this, envelope.payload, envelope);
                    }, 0);
                } else {
                    entry.callback.call(entry.context || this, envelope.payload, envelope);
                }

                // Se for once, remove após executar
                if (entry.once) {
                    listeners.delete(entry.id);
                }
            } catch (e) {
                console.error(`[EventBus] Error in listener for "${event}":`, e);
                if (this.framework) {
                    this.framework.log('error', `EventBus: ${event}`, e);
                }
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
        const regex = new RegExp(
            '^' + pattern.replace(/\*/g, '.*') + '$'
        );
        return regex.test(event);
    }

    _onWildcard(pattern, callback, context, options) {
        if (!this._wildcards.has(pattern)) {
            this._wildcards.set(pattern, new Map());
        }
        const id = ++this._id;
        this._wildcards.get(pattern).set(id, {
            id, callback, context,
            priority: options.priority || 0,
            once: options.once || false
        });
        return () => {
            if (this._wildcards.has(pattern)) {
                this._wildcards.get(pattern).delete(id);
            }
        };
    }

    _addToHistory(envelope) {
        this._history.push(envelope);
        if (this._history.length > this._maxHistory) {
            this._history.shift();
        }
    }

    _runMiddlewares(event, envelope) {
        if (!this._middlewares.has(event)) return true;

        for (const middleware of this._middlewares.get(event)) {
            try {
                const result = middleware(envelope.payload, envelope, this);
                if (result === false) return false;
            } catch (e) {
                console.error(`[EventBus] Middleware error: ${event}`, e);
            }
        }
        return true;
    }
}
```

## 4.2 Resumo da API

| Método | Descrição |
|--------|-----------|
| `on(event, callback, ctx, opts)` | Registra listener |
| `once(event, callback, ctx)` | Registra listener de execução única |
| `off(event, callback)` | Remove listener específico |
| `offAll(event)` | Remove todos listeners de um evento |
| `emit(event, payload, opts)` | Dispara evento |
| `has(event)` | Verifica se há listeners |
| `listeners(event)` | Retorna listeners de um evento |
| `events()` | Lista todos eventos com listeners |
| `stats(event)` | Estatísticas de eventos |
| `history(limit)` | Histórico de eventos |
| `enable()` | Habilita EventBus |
| `disable()` | Desabilita EventBus |
| `clearHistory()` | Limpa histórico |
| `destroy()` | Remove tudo |

---

# 5. Eventos do Framework

## 5.1 Ciclo de Vida do Framework

```js
// Inicialização
'framework:init'              // Framework começou a inicializar
'framework:ready'             // Framework completamente inicializado
'framework:destroy'           // Framework sendo destruído

// Erros
'framework:error'             // Erro não tratado capturado
'framework:warn'              // Aviso do Framework
```

## 5.2 Tema

```js
'theme:before-change'         // Tema vai mudar
'theme:change'                // Tema mudou
'theme:error'                 // Erro ao aplicar tema
```

## 5.3 Router

```js
'router:before-change'        // Rota vai mudar
'router:change'               // Rota mudou
'router:not-found'            // Rota não encontrada
'router:error'                // Erro no roteamento
```

## 5.4 Estado

```js
'state:change'                // Estado global mudou
'state:change:key'            // Chave específica mudou
'state:before-change'         // Estado vai mudar
'state:error'                 // Erro ao modificar estado
```

## 5.5 Responsivo

```js
'responsive:breakpoint'       // Breakpoint mudou
'responsive:orientation'      // Orientação mudou
'responsive:resize'           // Viewport redimensionou
```

## 5.6 Acessibilidade

```js
'a11y:announce'               // Anúncio para leitor de tela
'a11y:focus-trap'             // Focus trap ativado
'a11y:focus-release'          // Focus trap desativado
'a11y:reduced-motion'         // prefers-reduced-motion detectado
```

## 5.7 Ícones

```js
'icons:loaded'                // Sprite SVG carregado
'icons:error'                 // Erro ao carregar sprite
```

## 5.8 Plugins

```js
'plugins:register'            // Plugin registrado
'plugins:before-init'         // Plugin vai iniciar
'plugins:ready'               // Plugin iniciado
'plugins:error'               // Plugin falhou
```

---

# 6. Eventos de Componentes

## 6.1 Ciclo de Vida de Componentes

```js
'component:init'              // Componente inicializado
'component:render'            // Componente renderizado
'component:update'            // Componente atualizado
'component:state-change'      // Estado do componente mudou
'component:before-destroy'    // Componente vai ser destruído
'component:destroyed'         // Componente destruído
'component:mounted'           // Componente montado no DOM
```

## 6.2 Button

```js
'button:click'                // Botão clicado
'button:focus'                // Botão recebeu foco
'button:blur'                 // Botão perdeu foco
```

## 6.3 Modal

```js
'modal:open'                  // Modal aberto
'modal:close'                 // Modal fechado
'modal:confirm'               // Modal confirmado
'modal:cancel'                // Modal cancelado
'modal:before-open'           // Modal vai abrir
'modal:before-close'          // Modal vai fechar
```

## 6.4 Toast

```js
'toast:show'                  // Toast exibido
'toast:hide'                  // Toast oculto
'toast:action'                // Ação do Toast clicada
```

## 6.5 Drawer

```js
'drawer:open'                 // Drawer aberto
'drawer:close'                // Drawer fechado
'drawer:before-open'          // Drawer vai abrir
```

## 6.6 DataGrid

```js
'grid:init'                   // Grid inicializado
'grid:load'                   // Grid carregando dados
'grid:loaded'                 // Grid carregou dados
'grid:sort'                   // Ordenação alterada
'grid:filter'                 // Filtro alterado
'grid:select'                 // Seleção alterada
'grid:page'                   // Paginação alterada
'grid:row-click'              // Linha clicada
'grid:row-dblclick'           // Linha clicada duas vezes
'grid:edit'                   // Célula editada
'grid:save'                   // Dados salvos
'grid:error'                  // Erro no grid
'grid:export'                 // Exportação solicitada
'grid:print'                  // Impressão solicitada
'grid:column-resize'          // Coluna redimensionada
'grid:column-reorder'         // Coluna reordenada
'grid:column-toggle'          // Coluna exibida/oculta
```

## 6.7 Form

```js
'form:init'                   // Formulário inicializado
'form:submit'                 // Formulário submetido
'form:validate'               // Validação solicitada
'form:validate-error'         // Validação falhou
'form:validate-success'       // Validação passou
'form:serialize'              // Dados serializados
'form:reset'                  // Formulário resetado
'form:field-change'           // Campo alterado
'form:before-submit'          // Formulário vai submeter
'form:error'                  // Erro no formulário
```

## 6.8 Tabs

```js
'tab:change'                  // Tab alterada
'tab:before-change'           // Tab vai alterar
'tab:add'                     // Tab adicionada
'tab:remove'                  // Tab removida
```

## 6.9 Accordion

```js
'accordion:toggle'            // Item expandido/recolhido
'accordion:open'              // Item expandido
'accordion:close'             // Item recolhido
```

## 6.10 Tooltip

```js
'tooltip:show'                // Tooltip exibido
'tooltip:hide'                // Tooltip oculto
```

## 6.11 Dropdown

```js
'dropdown:open'               // Dropdown aberto
'dropdown:close'              // Dropdown fechado
'dropdown:select'             // Item selecionado
```

---

# 7. Eventos de Serviços

## 7.1 HTTP

```js
'http:request'                // Requisição iniciada
'http:success'                // Requisição bem-sucedida
'http:error'                  // Requisição falhou
'http:timeout'                // Requisição excedeu timeout
'http:unauthorized'           // 401 não autorizado
'http:forbidden'              // 403 proibido
'http:not-found'              // 404 não encontrado
'http:server-error'           // 500 erro interno
```

## 7.2 Auth

```js
'auth:login'                  // Login realizado
'auth:logout'                 // Logout realizado
'auth:token-refresh'          // Token renovado
'auth:session-expired'        // Sessão expirada
'auth:error'                  // Erro de autenticação
'auth:before-login'           // Vai tentar login
```

## 7.3 Upload

```js
'upload:start'                // Upload iniciado
'upload:progress'             // Progresso do upload
'upload:complete'             // Upload concluído
'upload:error'                // Upload falhou
'upload:cancel'               // Upload cancelado
```

## 7.4 Download

```js
'download:start'              // Download iniciado
'download:progress'           // Progresso do download
'download:complete'           // Download concluído
'download:error'              // Download falhou
```

## 7.5 WebSocket

```js
'ws:open'                     // Conexão aberta
'ws:message'                  // Mensagem recebida
'ws:error'                    // Erro na conexão
'ws:close'                    // Conexão fechada
'ws:reconnect'                // Reconectando
```

---

# 8. Eventos de Domínio (Domínio da Aplicação)

## 8.1 Usuário

```js
'user:login'                  // Usuário logou
'user:logout'                 // Usuário deslogou
'user:profile-update'         // Perfil atualizado
'user:preferences-change'     // Preferências alteradas
```

## 8.2 Dados

```js
'data:create'                 // Registro criado
'data:read'                   // Registro lido
'data:update'                 // Registro atualizado
'data:delete'                 // Registro deletado
'data:loaded'                 // Dados carregados
'data:error'                  // Erro em operação de dados
'data:sync'                   // Sincronização solicitada
'data:synced'                 // Sincronização concluída
```

## 8.3 Navegação

```js
'navigation:module-change'    // Módulo alterado
'navigation:sidebar-toggle'   // Sidebar alternada
'navigation:back'             // Navegação para trás
```

---

# 9. Ciclo de Vida do Evento

## 9.1 Fluxo Completo

```
1. Emitter chama emit('user:login', { user })
       │
       ▼
2. Event Bus recebe o evento
       │
       ├── 2a. Gera envelope { event, payload, timestamp, id }
       │
       ▼
3. Middlewares do evento são executados
       │
       ├── Se retornar false → evento cancelado
       │
       ▼
4. Listeners diretos são executados (ordem de prioridade)
       │
       ├── listenerA({ user })  ← prioridade 100
       ├── listenerB({ user })  ← prioridade 0
       └── listenerC({ user })  ← prioridade -100
       │
       ▼
5. Wildcards são executados
       │
       ├── user:* → escuta
       └── *:login → escuta
       │
       ▼
6. Evento registrado no histórico
```

## 9.2 Envelope

```js
{
    event: 'user:login',          // Nome do evento
    payload: { user: {...} },     // Dados do evento
    timestamp: 1703456789012,     // Timestamp do disparo
    id: 'user:login_1703456789012_42' // ID único
}
```

## 9.3 Sincronia

```js
// Síncrono (padrão)
FiscalUI.events.on('data:loaded', (data) => {
    // Executa imediatamente quando emit() for chamado
    renderTable(data);
});

// Assíncrono (schedule para próximo tick)
FiscalUI.events.on('data:loaded', (data) => {
    renderTable(data);
}, null, { async: true });

// Once (escuta apenas uma vez)
FiscalUI.events.once('framework:ready', () => {
    console.log('Framework pronto (primeira vez)');
});
```

---

# 10. Payload

## 10.1 Convenções

```js
// ✅ Sempre objeto
FiscalUI.events.emit('user:login', { user: { id: 1, name: 'João' } });

// ❌ Nunca valor primitivo
FiscalUI.events.emit('user:login', 'João');

// ✅ Incluir source (quem disparou)
FiscalUI.events.emit('button:click', {
    source: 'Button#42',
    variant: 'primary',
    originalEvent: e
});

// ✅ Incluir metadata útil
FiscalUI.events.emit('data:loaded', {
    source: 'DataGrid#7',
    endpoint: '/api/nfe',
    records: 150,
    duration: 320
});
```

## 10.2 Payload Padrão

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `source` | `string` | Não | Quem disparou o evento |
| `timestamp` | `number` | Automático | Quando foi disparado |
| `data` | `any` | Variável | Dados específicos do evento |

---

# 11. Assinatura

## 11.1 Formas de Assinar

```js
// Listener simples
FiscalUI.events.on('toast:show', (payload) => {
    showToast(payload.message);
});

// Com contexto
const toastService = new ToastService();
FiscalUI.events.on('toast:show', function(payload) {
    this.show(payload.message);
}, toastService);

// Com opções (prioridade, async, once)
FiscalUI.events.on('data:loaded', (data) => {
    renderTable(data);
}, null, {
    priority: 100,       // Executa antes dos outros
    async: true,         // Não bloqueia o emit
    once: false          // Executa toda vez
});

// Once (atalho)
FiscalUI.events.once('framework:ready', () => {
    console.log('Só executa uma vez');
});

// Wildcard — escuta todos eventos de um namespace
FiscalUI.events.on('user:*', (payload, envelope) => {
    console.log(`Evento de usuário: ${envelope.event}`);
});

// Wildcard — escuta todos eventos com uma ação
FiscalUI.events.on('*:error', (payload, envelope) => {
    console.error(`Erro em ${envelope.event}:`, payload);
});
```

## 11.2 on() vs once()

```js
// on() — escuta todas as ocorrências
const unsubscribe = FiscalUI.events.on('router:change', (route) => {
    updateMenu(route);
});
// Nunca é removido — escuta para sempre

// once() — escuta apenas a primeira ocorrência
FiscalUI.events.once('framework:ready', () => {
    initializeApp(); // Executa apenas uma vez
});
```

---

# 12. Cancelamento

## 12.1 Remover Listener

```js
// Usando referência da função
function onReady() {
    console.log('ready');
}
FiscalUI.events.on('framework:ready', onReady);
// Em outro lugar:
FiscalUI.events.off('framework:ready', onReady);

// Usando retorno de on()
const unsubscribe = FiscalUI.events.on('router:change', (route) => {
    updateMenu(route);
});
// Cancelar:
unsubscribe();
```

## 12.2 Remover Todos

```js
// Remove todos listeners de um evento específico
FiscalUI.events.offAll('user:login');

// Remove todos listeners de todos eventos
FiscalUI.events.offAll();
```

## 12.3 Cancelar Evento (Middleware)

```js
FiscalUI.events.use('http:request', (payload, envelope, bus) => {
    if (!navigator.onLine) {
        console.warn('Sem conexão — requisição cancelada');
        return false; // Cancela o evento
    }
    return true; // Continua
});
```

---

# 13. Wildcards

## 13.1 Padrões Suportados

```js
// namespace:* → todos eventos de um módulo
FiscalUI.events.on('user:*', (payload, envelope) => {
    console.log(`Evento de usuário: ${envelope.event}`);
});
// user:login, user:logout, user:update, etc.

// *:action → todos eventos com mesma ação
FiscalUI.events.on('*:error', (payload, envelope) => {
    console.error(`Erro: ${envelope.event}`);
});
// http:error, auth:error, data:error, etc.

// * → todos eventos do sistema
FiscalUI.events.on('*', (payload, envelope) => {
    console.log(`Evento: ${envelope.event}`);
});
```

## 13.2 Performance

Wildcards são processados após os listeners diretos. Para máxima performance, prefira eventos específicos em vez de wildcards.

---

# 14. Middleware

## 14.1 Implementação

```js
// Middleware global (todos eventos)
FiscalUI.events.use((payload, envelope, bus) => {
    console.log(`[Middleware] ${envelope.event}`);
    return true;
});

// Middleware específico
FiscalUI.events.use('http:*', (payload, envelope, bus) => {
    payload.timestamp = Date.now();
    return true;
});

// Middleware que bloqueia
FiscalUI.events.use('http:request', (payload, envelope, bus) => {
    if (!payload.url) {
        console.error('URL não fornecida');
        return false; // Bloqueia o evento
    }
    return true;
});
```

## 14.2 Casos de Uso

```
1. Logging — registrar todos eventos
2. Validação — validar payload antes de entregar
3. Transformação — enriquecer payload
4. Autorização — bloquear eventos não autorizados
5. Throttle — limitar frequência de eventos
6. Debug — inspecionar tráfego de eventos
```

---

# 15. Prioridade

## 15.1 Definição

Listeners com maior prioridade executam primeiro.

```js
// Alta prioridade (executa primeiro)
FiscalUI.events.on('data:loaded', validateData, null, { priority: 100 });

// Prioridade normal
FiscalUI.events.on('data:loaded', renderTable, null, { priority: 0 });

// Baixa prioridade (executa por último)
FiscalUI.events.on('data:loaded', logAnalytics, null, { priority: -100 });
```

## 15.2 Ordem de Execução

```
1. priority: 100  → validateData()
2. priority: 50   → transformData()
3. priority: 0    → renderTable()
4. priority: -50  → updateStats()
5. priority: -100 → logAnalytics()
```

---

# 16. Async Events

## 16.1 Listeners Assíncronos

```js
// Listener assíncrono (não bloqueia o emit)
FiscalUI.events.on('data:loaded', async (data) => {
    await saveToIndexedDB(data);
}, null, { async: true });
```

## 16.2 Disparo com Await

```js
// Para listeners async, o emit não espera
FiscalUI.events.emit('data:loaded', data);
// Continua imediatamente — listeners async rodam em setTimeout
```

---

# 17. Namespaces

## 17.1 Organização

```
framework:     Eventos internos do Framework
component:     Eventos de ciclo de vida de componentes
button:        Eventos de botões
modal:         Eventos de modal
grid:          Eventos de datagrid
form:          Eventos de formulário
user:          Eventos de usuário
auth:          Eventos de autenticação
data:          Eventos de dados
http:          Eventos de requisições HTTP
```

## 17.2 Criação de Novo Namespace

```js
// Qualquer módulo pode criar seu namespace
FiscalUI.events.emit('meu-modulo:init', { version: '1.0' });
FiscalUI.events.emit('meu-modulo:action', { data: 'valor' });

// Convenção: namespace deve ser o nome do módulo em minúsculo, sem espaços
```

---

# 18. Debugging

## 18.1 Modo Debug

```js
// Habilita debug geral
FiscalUI.config.debug = true;

// Todos eventos são logados no console
// [EventBus] user:login { user: {...} }
// [EventBus] router:change { route: '/dashboard' }
```

## 18.2 Monitor de Eventos

```js
// Escutar todos eventos
FiscalUI.events.on('*', (payload, envelope) => {
    console.log(`[EventBus] ${envelope.event}`, payload);
});

// Estatísticas
const stats = FiscalUI.events.stats();
console.table(stats);
// Evento              │ Emitted │ Subscribers
// ────────────────────┼─────────┼────────────
// framework:ready     │ 1       │ 3
// button:click       │ 25      │ 1
// http:request       │ 12      │ 0

// Histórico
const history = FiscalUI.events.history(5);
console.log(history);
```

## 18.3 Visualizador

Uma página de debug que exibe em tempo real todos os eventos do sistema:

```
sprints/tools/event-monitor.html
```

---

# 19. Performance

## 19.1 Métricas

| Operação | Performance | Complexidade |
|----------|------------|--------------|
| `on()` | < 0.01ms | O(1) |
| `off()` | < 0.01ms | O(1) |
| `emit()` sem listeners | < 0.001ms | O(1) |
| `emit()` com 10 listeners | < 0.05ms | O(n) |
| `emit()` com 100 listeners | < 0.5ms | O(n) |
| Wildcard dispatch | < 0.1ms | O(w) onde w = wildcards |
| Histórico (append) | < 0.001ms | O(1) |

## 19.2 Otimizações

```js
// 1. Use eventos específicos em vez de wildcards
✅ 'button:click'
❌ '*'

// 2. Remova listeners que não são mais necessários
const unsub = FiscalUI.events.on('grid:load', handler);
// Quando não precisar mais:
unsub();

// 3. Prefira eventos síncronos para listeners críticos
✅ FiscalUI.events.on('grid:sort', { async: false })

// 4. Use once() para eventos que só disparam uma vez
✅ FiscalUI.events.once('framework:ready', handler)

// 5. Desabilite histórico em produção se não precisar
FiscalUI.events._maxHistory = 0;
```

---

# 20. Memória

## 20.1 Prevenção de Vazamentos

```js
class MyComponent {
    init() {
        // ✅ Correto: armazena referência do unsubscribe
        this._unsubscribers = [];
        this._unsubscribers.push(
            FiscalUI.events.on('user:login', this.onLogin)
        );
        this._unsubscribers.push(
            FiscalUI.events.on('data:loaded', this.onDataLoaded)
        );
    }

    destroy() {
        // ✅ Correto: remove todos listeners
        this._unsubscribers.forEach(unsub => unsub());
        this._unsubscribers = [];
    }
}
```

## 20.2 Auto Cleanup no ComponentBase

```js
class UIComponent {
    init() {
        // this.on() registra e gerencia cleanup automático
        this.on('theme:change', () => this.render());
        this.on('responsive:breakpoint', (p) => this._onBreakpoint(p));

        // No destroy(), todos listeners registrados via on() são removidos
    }
}
```

---

# 21. Testes

## 21.1 Teste Unitário

```js
describe('EventBus', () => {
    let bus;

    beforeEach(() => {
        bus = new EventBus();
    });

    afterEach(() => {
        bus.destroy();
    });

    it('should register and emit events', () => {
        const spy = jasmine.createSpy();
        bus.on('test:event', spy);
        bus.emit('test:event', { data: 1 });
        expect(spy).toHaveBeenCalledWith({ data: 1 });
    });

    it('should support once listeners', () => {
        const spy = jasmine.createSpy();
        bus.once('test:once', spy);
        bus.emit('test:once');
        bus.emit('test:once');
        expect(spy.calls.count()).toBe(1);
    });

    it('should remove listeners', () => {
        const spy = jasmine.createSpy();
        const fn = () => spy();
        bus.on('test:off', fn);
        bus.off('test:off', fn);
        bus.emit('test:off');
        expect(spy).not.toHaveBeenCalled();
    });

    it('should support wildcards', () => {
        const spy = jasmine.createSpy();
        bus.on('user:*', spy);
        bus.emit('user:login');
        bus.emit('user:logout');
        expect(spy.calls.count()).toBe(2);
    });

    it('should support priority ordering', () => {
        const order = [];
        bus.on('test', () => order.push(1), null, { priority: 100 });
        bus.on('test', () => order.push(2), null, { priority: 0 });
        bus.on('test', () => order.push(3), null, { priority: -100 });
        bus.emit('test');
        expect(order).toEqual([1, 2, 3]);
    });

    it('should maintain history', () => {
        bus.emit('test:1');
        bus.emit('test:2');
        const history = bus.history();
        expect(history.length).toBe(2);
        expect(history[0].event).toBe('test:1');
        expect(history[1].event).toBe('test:2');
    });

    it('should support middleware', () => {
        const middleware = jasmine.createSpy('middleware').and.returnValue(true);
        const listener = jasmine.createSpy('listener');
        bus.use(middleware);
        bus.on('test', listener);
        bus.emit('test');
        expect(middleware).toHaveBeenCalled();
        expect(listener).toHaveBeenCalled();
    });

    it('should cancel event if middleware returns false', () => {
        const listener = jasmine.createSpy('listener');
        bus.use(() => false);
        bus.on('test', listener);
        bus.emit('test');
        expect(listener).not.toHaveBeenCalled();
    });

    it('should return unsubscribe function from on()', () => {
        const spy = jasmine.createSpy();
        const unsub = bus.on('test', spy);
        unsub();
        bus.emit('test');
        expect(spy).not.toHaveBeenCalled();
    });

    it('should handle errors in listeners gracefully', () => {
        const spy = jasmine.createSpy();
        bus.on('test', () => { throw new Error('fail'); });
        bus.on('test', spy);
        expect(() => bus.emit('test')).not.toThrow();
        expect(spy).toHaveBeenCalled();
    });
});
```

---

# 22. Boas Práticas

## 22.1 Regras de Ouro

```
1. NUNCA chame métodos de outro componente diretamente
2. SEMPRE use emit() para comunicação entre módulos
3. NUNCA modifique o payload recebido
4. SEMPRE use namespace:action (minúsculo)
5. NUNCA use espaços ou caracteres especiais no nome
6. SEMPRE remova listeners no destroy()
7. NUNCA dependa da ordem de execução entre listeners
8. SEMPRE use once() para eventos de inicialização
9. NUNCA use wildcards em produção sem necessidade
10. SEMPRE documente eventos públicos do seu módulo
```

## 22.2 Checklist

```
☐ Evento segue padrão namespace:action
☐ Payload é um objeto, não primitivo
☐ Listener é removido quando não necessário
☐ once() usado para eventos únicos
☐ Documentação dos eventos do módulo
☐ Testes para eventos críticos
☐ Middleware para validação quando necessário
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial — Event Bus completo |
