# FiscalUI Framework

## Documento 001 — Arquitetura Base

**Versão 1.0**

Este documento é o mais importante do projeto.

Ele responde: **Como o FiscalUI funciona internamente?**

---

# Índice

1. Introdução
2. Objetivos
3. Filosofia
4. Arquitetura Geral
5. Camadas
6. Núcleo
7. Componentes
8. Serviços
9. Eventos
10. Estado Global
11. Ciclo de Vida
12. Renderização
13. Organização
14. Performance
15. Segurança
16. Extensibilidade
17. Roadmap

---

# 1. Introdução

## 1.1 O que é o FiscalUI

O FiscalUI é um Framework UI corporativo construído integralmente com HTML5, CSS3 e JavaScript ES6+. Zero dependências externas. Zero frameworks terceiros. Zero build step obrigatório.

Ele foi projetado para sistemas ERP de ciclo de vida longo (10+ anos), onde consistência, performance e independência tecnológica são requisitos não negociáveis.

## 1.2 Para quem este documento foi escrito

- **Arquitetos de software** que precisam entender como o Framework opera internamente
- **Desenvolvedores** que construirão componentes, serviços ou plugins
- **Mantenedores** que evoluirão o Framework ao longo dos anos
- **Tomadores de decisão** que avaliarão o FiscalUI como base tecnológica

## 1.3 Como este documento está organizado

Cada seção aprofunda um aspecto da arquitetura. A leitura deve ser sequencial na primeira vez. Seções posteriores podem ser consultadas independentemente como referência.

## 1.4 Convenções tipográficas

```
Termo técnico    → Primeira ocorrência em itálico
Código           → Bloco monoespaçado
Regra            → Lista numerada com ✅ (certo) e ❌ (errado)
Aviso            → ⚠️ Notas importantes sobre decisões arquiteturais
```

---

# 2. Objetivos

## 2.1 Objetivo Geral

Construir um Framework UI corporativo que permita o desenvolvimento de sistemas ERP completos com HTML5, CSS3 e JavaScript vanilla — sem React, Vue, Angular, Bootstrap, jQuery, Tailwind ou qualquer dependência externa.

## 2.2 Objetivos Específicos

1. **Independência Tecnológica** — O Framework não deve depender de bibliotecas que possam se tornar obsoletas ou exigir migrações forçadas.
2. **Ciclo de Vida Longo** — Sistemas construídos com o FiscalUI devem operar por 10+ anos sem necessidade de reescrita.
3. **Performance** — Primeira renderização < 300ms, scroll a 60 FPS, bundle mínimo.
4. **Acessibilidade** — Conformidade WCAG 2.2 AA desde a concepção.
5. **Consistência Visual** — Design System completo via Design Tokens e Theme Engine.
6. **Extensibilidade** — Plugins, temas e componentes sem modificar o núcleo.
7. **Manutenibilidade** — Código modular, documentado e testado.

## 2.3 O que o FiscalUI não é

- Não é um framework JavaScript reativo (não há Virtual DOM, não há two-way binding automático)
- Não é um substituto para React, Vue ou Angular
- Não é uma biblioteca de componentes prontos para consumo imediato
- Não é um CMS, ERP ou sistema fiscal — é a base sobre a qual estes são construídos

## 2.4 Métricas de Sucesso

| Métrica | Meta | Como medir |
|---------|------|------------|
| Tempo de inicialização | < 300ms | Performance.now() |
| Bundle total (gzip) | < 50KB | Webpack/Rollup report |
| Cobertura de testes | ≥ 90% | Jest coverage |
| Acessibilidade | WCAG 2.2 AA | axe-core + manual |
| Compatibilidade | 2 versões recentes de cada browser | Can I Use |
| Temas entregues | 4 (Dark, Light, High Contrast, Liquid Glass) | Build release |
| Documentação | 100% dos componentes | README checklist |

---

# 3. Filosofia

## 3.1 Princípios Fundamentais

O FiscalUI é governado por 7 princípios. Toda decisão arquitetural deve ser validada contra eles.

### 3.1.1 Zero Dependências

Nenhuma biblioteca externa é utilizada em runtime. Nem Bootstrap, jQuery, React, Vue, Angular, Tailwind, Material UI, Font Awesome, Google Fonts, Moment.js, Lodash ou qualquer outro.

**Por quê?** Frameworks JavaScript têm obsolescência programada. O Eco de 2023 não é o mesmo de 2028. Um ERP de vida longa não pode refatorar sua interface a cada 2-3 anos porque uma dependência mudou ou foi abandonada.

```js
// ❌ Dependência externa
import React from 'react';
import { Button } from '@mui/material';

// ✅ Código nativo
class Button extends ComponentBase { /* ... */ }
```

⚠️ **Exceção permitida:** Ferramentas de desenvolvimento (bundlers, linters, test runners) são aceitas no ambiente de desenvolvimento, desde que não gerem dependência em runtime.

### 3.1.2 HTML5 Semântico

Todo componente utiliza o elemento HTML mais apropriado semanticamente. `<nav>` para navegação, `<button>` para botões, `<table>` para dados tabulares, `<header>` para cabeçalhos.

```html
<!-- ❌ Divite -->
<div class="header">
    <div class="nav" onclick="navegar()">Home</div>
</div>

<!-- ✅ Semântico -->
<header>
    <nav>
        <button type="button" onclick="navegar()">Home</button>
    </nav>
</header>
```

### 3.1.3 CSS Modular com BEM

Cada componente possui seu próprio escopo CSS. A nomenclatura segue BEM (Block, Element, Modifier) com prefixo `ui-`.

```css
/* Bloco */
.ui-card { }
/* Elemento */
.ui-card__title { }
/* Modificador */
.ui-card--highlighted { }
```

### 3.1.4 Design Tokens como Fonte Única da Verdade Visual

Nenhum valor fixo de cor, espaçamento, borda, sombra, tipografia ou animação existe em qualquer arquivo de componente. Tudo é referenciado via `var(--token)`.

```css
/* ❌ Valor fixo */
.button { color: #14b8a6; padding: 12px; }

/* ✅ Token */
.button { color: var(--color-primary); padding: var(--spacing-4); }
```

### 3.1.5 Separação de Responsabilidades

Cada módulo tem uma e apenas uma responsabilidade. Um arquivo = uma responsabilidade.

```
variaveis.css    → tokens
layout.css       → grid, containers
style.css        → componentes
temas.css        → temas
```

### 3.1.6 Backend Opaco

O frontend conhece apenas a API REST. Nunca acessa banco de dados, camada de negócio, COBOL ou qualquer recurso backend diretamente.

```
Frontend → API REST (JSON) → Backend (Python/COBOL) → PostgreSQL
```

### 3.1.7 Melhoria Contínua

O Framework evolui por camadas, nunca por revolução. Novas versões são sempre compatíveis com código existente. Nenhuma funcionalidade é removida sem 2 versões de depreciação.

## 3.2 Trade-offs Arquiteturais

Toda arquitetura envolve trade-offs. O FiscalUI faz escolhas conscientes:

| Decisão | Benefício | Custo |
|---------|-----------|-------|
| Zero dependências | Vida útil de 10+ anos | Mais código para escrever e manter |
| Vanilla JS | Sem lock-in de framework | Sem Virtual DOM, sem reatividade automática |
| CSS Variables nativo | Tema troca em runtime, sem build | Sem suporte a IE11 (deliberado) |
| BEM manual | Sem build step, sem CSS-in-JS | Mais verbose que Tailwind |
| SVG sprite único | Uma requisição HTTP para dezenas de ícones | Mais trabalho ao adicionar novo ícone |
| Pub/sub (Event Bus) | Componentes desacoplados | Mais complexo que chamada direta |

---

# 4. Arquitetura Geral

## 4.1 Visão Macro

O FiscalUI opera em 4 camáveis horizontais que se comunicam verticalmente através de interfaces bem definidas.

```
                    ┌──────────────────────────────────────┐
                    │         APLICAÇÃO (ERP)              │
                    │  Módulos: NF-e, Produtos, Clientes   │
                    ├──────────────────────────────────────┤
                    │      COMPONENTES VISUAIS             │
                    │  Button, Card, Modal, DataGrid, etc  │
                    ├──────────────────────────────────────┤
                    │      ENGINES ESPECIALIZADAS          │
                    │  Router | State | Responsive | A11y  │
                    │  Motion | Icons | Plugins             │
                    ├──────────────────────────────────────┤
                    │      NÚCLEO DO FRAMEWORK             │
                    │  FiscalUI | EventBus | ComponentBase │
                    │  ServiceContainer | CSS Core          │
                    └──────────────────────────────────────┘
```

## 4.2 Arquitetura em Camadas

### 4.2.1 Camada 1 — Infraestrutura

```
┌─────────────────────────────────────────────────────────┐
│                  INFRAESTRUTURA                          │
├────────────┬────────────┬────────────┬──────────────────┤
│            │            │            │                  │
│ Design     │ Theme      │ CSS Core   │ Layout Core      │
│ Tokens     │ Engine     │ (reset,    │ (grid, flex,     │
│ (variáveis)│ (data-theme)│ tipografia)│ containers)      │
│            │            │            │                  │
└────────────┴────────────┴────────────┴──────────────────┘
```

**Responsabilidade:** Fornecer a base visual do sistema. Nenhuma lógica JavaScript. Tudo é CSS.

**Tecnologia exclusiva:** CSS3 (variáveis, custom properties, media queries).

### 4.2.2 Camada 2 — Núcleo

```
┌─────────────────────────────────────────────────────────┐
│                     NÚCLEO                               │
├──────────┬───────────┬──────────┬───────────┬───────────┤
│          │           │          │           │           │
│ FiscalUI │ EventBus  │ Component│ Service   │ State     │
│ (init)   │ (pub/sub) │ Base     │ Container │ Manager   │
│          │           │          │ (DI)      │ (global)  │
│          │           │          │           │           │
└──────────┴───────────┴──────────┴───────────┴───────────┘
```

**Responsabilidade:** Orquestrar a inicialização, fornecer a infraestrutura de comunicação e o ciclo de vida de componentes.

**Tecnologia:** JavaScript ES6+ (classes, promises, modules).

### 4.2.3 Camada 3 — Engines

```
┌─────────────────────────────────────────────────────────┐
│                    ENGINES                               │
├──────────┬───────────┬───────────┬──────────┬───────────┤
│          │           │           │          │           │
│ Router   │ Responsive│ Accessibil│ Motion   │ Icon      │
│ (SPA)    │ (breakpts)│ ity (A11y)│ (anim)   │ (SVG)     │
│          │           │           │          │           │
├──────────┴───────────┴───────────┴──────────┴───────────┤
│                      Plugin Engine                       │
└─────────────────────────────────────────────────────────┘
```

**Responsabilidade:** Fornecer capacidades transversais que qualquer componente pode consumir.

### 4.2.4 Camada 4 — Componentes

```
┌─────────────────────────────────────────────────────────┐
│                   COMPONENTES                            │
├──────────┬───────────┬──────────┬───────────┬───────────┤
│ Button   │ Card      │ Modal    │ DataGrid  │ Form      │
│ IconBtn  │ Panel     │ Toast    │ TreeGrid  │ Input     │
│ SplitBtn │ Badge     │ Tooltip  │ Dashboard │ Select    │
│ ...      │ ...       │ ...      │ ...       │ ...       │
└──────────┴───────────┴──────────┴───────────┴───────────┘
```

**Responsabilidade:** Interface com o usuário. Componentes consomem as camadas inferiores mas nunca as modificam.

### 4.2.5 Camada 5 — Aplicação

```
┌─────────────────────────────────────────────────────────┐
│                    APLICAÇÃO                             │
├──────────┬───────────┬──────────┬───────────┬───────────┤
│ NF-e     │ NFC-e     │ Produtos │ Clientes  │ Relatórios│
│ Módulo   │ Módulo    │ Módulo   │ Módulo    │ Módulo    │
└──────────┴───────────┴──────────┴───────────┴───────────┘
```

**Responsabilidade:** Implementar as regras de negócio do ERP utilizando os componentes do Framework.

## 4.3 Fluxo de Dados entre Camadas

```
Usuário
   │
   ▼
Componente Visual (Button, Form, Grid)
   │
   ▼
Event Bus ──→ Service Layer ──→ HTTP Service ──→ API REST
   │                              │
   ▼                              ▼
State Manager ←────────────── Resposta JSON
   │
   ▼
Componente atualiza (re-render)
   │
   ▼
Usuário vê o resultado
```

**Regra fundamental:** Nenhum componente visual faz chamada de API diretamente. Toda comunicação passa pelo Service Layer e Event Bus.

## 4.4 Diagrama de Implantação

```
┌───────────────────┐       ┌───────────────────┐
│   Navegador       │       │   Servidor         │
│                   │ HTTP  │                    │
│ FiscalUI (HTML/   │──────▶│ Python (server.py) │──────▶ PostgreSQL
│ CSS/JS)           │◀──────│ COBOL (subprocess) │◀──────┐
│                   │ JSON  │ SEFAZ (SOAP/XML)   │       │
└───────────────────┘       └───────────────────┘       │
                                                         │
                          ┌───────────────────┐          │
                          │   Sistema         │──────────┘
                          │   Arquivos (.dat) │
                          └───────────────────┘
```

## 4.5 Compatibilidade

| Browser | Suporte |
|---------|---------|
| Chrome 90+ | ✅ Completo |
| Firefox 90+ | ✅ Completo |
| Edge 90+ | ✅ Completo |
| Safari 15+ | ✅ Completo |
| Opera 76+ | ✅ Completo |
| IE11 | ❌ Não suportado |
| Samsung Internet | ✅ Parcial (testar) |

---

# 5. Camadas

## 5.1 Camada de Infraestrutura (CSS)

### 5.1.1 Responsabilidade

Fornecer toda a base visual do sistema. Esta camada contém exclusivamente CSS. Nenhum JavaScript.

### 5.1.2 Arquivos

| Arquivo | Conteúdo | Tamanho estimado |
|---------|----------|------------------|
| `css/tokens.css` | Todas as variáveis CSS do Design System | ~2KB |
| `css/core.css` | Reset, tipografia, utilitários | ~4KB |
| `css/layout.css` | Grid, flex, containers, spacing helpers | ~6KB |
| `css/theme.css` | Tema Light, High Contrast, Liquid Glass | ~3KB |
| `css/motion.css` | Keyframes, transições, easing | ~5KB |
| `css/icons.css` | Classes de ícones, tamanhos, cores | ~3KB |

**Total estimado:** ~23KB (gzip: ~6KB)

### 5.1.3 Regras

1. Nenhum arquivo CSS importa outro — todos são carregados via `<link>` no HTML.
2. A ordem de carregamento no HTML é a ordem de cascata: tokens → core → layout → theme → motion → icons → components.
3. Componentes não definem estilos fora de seus próprios arquivos.
4. O Theme Engine sobrescreve tokens, nunca reescreve componentes.

## 5.2 Camada de Núcleo (JavaScript)

### 5.2.1 Responsabilidade

Orquestrar a inicialização, fornecer event bus, state manager, service container e classe base para componentes.

### 5.2.2 Módulos

| Módulo | Arquivo | Responsabilidade |
|--------|---------|-----------------|
| FiscalUI | `core/FiscalUI.js` | Classe principal, init, orquestração |
| EventBus | `events/EventBus.js` | Pub/sub para comunicação entre módulos |
| ComponentBase | `core/ComponentBase.js` | Classe base para todos os componentes |
| ServiceContainer | `core/ServiceContainer.js` | Injeção de dependências |
| StateManager | `state/StateManager.js` | Estado global reativo |
| Router | `router/Router.js` | Navegação SPA |

### 5.2.3 Dependências entre módulos do núcleo

```
EventBus ←── Nenhuma (carregado primeiro)

ComponentBase ←── EventBus
ServiceContainer ←── EventBus
StateManager ←── EventBus

FiscalUI ←── ComponentBase + ServiceContainer + StateManager

Router ←── FiscalUI
```

## 5.3 Camada de Engines

### 5.3.1 Responsabilidade

Fornecer capacidades transversais que qualquer componente ou serviço pode consumir. Engines são inicializadas pelo FiscalUI e registradas no ServiceContainer.

### 5.3.2 Catálogo de Engines

| Engine | Função | Depende de |
|--------|--------|------------|
| ResponsiveEngine | Detecta breakpoints, notifica mudanças | FiscalUI (events) |
| AccessibilityEngine | Gerencia foco, ARIA, live regions | FiscalUI (events, state) |
| MotionEngine | Gerencia animações, reduced motion | FiscalUI (events) |
| IconEngine | Carrega sprite SVG, gerencia ícones | FiscalUI |
| PluginEngine | Registra, carrega e gerencia plugins | FiscalUI (events, container) |

### 5.3.3 Interface comum de Engine

```js
class Engine {
    constructor(framework) {
        this.framework = framework;
        this.initialized = false;
    }

    async init() {
        this.initialized = true;
        this.framework.events.emit(`${this.name}:ready`);
    }

    destroy() {
        this.initialized = false;
    }
}
```

## 5.4 Camada de Componentes

### 5.4.1 Responsabilidade

Interface com o usuário. Componentes consomem engines e serviços via injeção de dependência. Nunca acessam APIs diretamente.

### 5.4.2 Hierarquia de Componentes

```
Componentes Atômicos
├── Button, IconButton, Link, Badge, Avatar, Divider

Componentes Moleculares
├── Card, Panel, Tooltip, Progress, Spinner, Skeleton

Componentes Organísmicos
├── Modal, Drawer, Toast, Form, DataGrid, Dashboard

Componentes de Layout
├── Toolbar, Sidebar, Navbar, Tabs, Accordion, Breadcrumb

Componentes de Formulário
├── Input, Select, Checkbox, Radio, Switch, Upload, DatePicker
```

## 5.5 Camada de Aplicação

### 5.5.1 Responsabilidade

Implementar as funcionalidades de negócio. Esta camada é de responsabilidade do time de produto, não do Framework. O FiscalUI fornece a infraestrutura; a aplicação fornece os módulos.

---

# 6. Núcleo

## 6.1 FiscalUI — Classe Principal

A classe `FiscalUI` é o ponto de entrada do Framework. Ela é instanciada uma única vez e fica disponível globalmente.

### 6.1.1 Construtor

```js
class FiscalUI {
    constructor(config = {}) {
        this.version = "1.0.0";
        this.config = {
            debug: false,
            theme: "dark",
            lang: "pt-BR",
            router: { mode: "hash" },
            ...config
        };

        // Inicializa núcleo
        this.events = null;
        this.state = null;
        this.container = null;

        // Inicializa engines
        this.router = null;
        this.responsive = null;
        this.a11y = null;
        this.motion = null;
        this.icons = null;
        this.plugins = null;

        // Serviços registrados
        this._services = {};
        this._initialized = false;
    }
}
```

### 6.1.2 Inicialização

```js
async init() {
    if (this._initialized) return;

    // 1. Event Bus (independente)
    this.events = new EventBus();

    // 2. Service Container
    this.container = new ServiceContainer();
    this.container.register("eventBus", this.events);

    // 3. State Manager
    this.state = new StateManager(this.events);
    this.container.register("state", this.state);

    // 4. Component Base
    this.Component = ComponentBase;

    // 5. Engines
    this.router = new Router(this);
    this.responsive = new ResponsiveEngine(this);
    this.a11y = new AccessibilityEngine(this);
    this.motion = new MotionEngine(this);
    this.icons = new IconEngine(this);
    this.plugins = new PluginEngine(this);

    // 6. Inicializa engines em paralelo
    const engines = [
        this.router.init(),
        this.responsive.init(),
        this.a11y.init(),
        this.motion.init(),
        this.icons.init(),
        this.plugins.init()
    ];
    await Promise.all(engines);

    // 7. Aplica tema salvo
    const savedTheme = localStorage.getItem("fiscalui_theme");
    if (savedTheme) {
        this.setTheme(savedTheme);
    }

    // 8. Framework pronto
    this._initialized = true;
    this.events.emit("framework:ready", { version: this.version });

    if (this.config.debug) {
        console.log(`[FiscalUI] v${this.version} initialized`);
    }
}
```

### 6.1.3 API Pública do FiscalUI

```js
// Acesso global
window.FiscalUI = new FiscalUI();

// Métodos principais
FiscalUI.init()
FiscalUI.setTheme(name)
FiscalUI.getService(name)
FiscalUI.registerService(name, instance)
FiscalUI.destroy()

// Propriedades
FiscalUI.version        // "1.0.0"
FiscalUI.events         // EventBus instance
FiscalUI.state          // StateManager instance
FiscalUI.router         // Router instance
FiscalUI.responsive     // ResponsiveEngine instance
FiscalUI.a11y           // AccessibilityEngine instance
FiscalUI.motion         // MotionEngine instance
FiscalUI.icons          // IconEngine instance
FiscalUI.plugins        // PluginEngine instance
FiscalUI.Component      // ComponentBase class
```

## 6.2 Ciclo de Inicialização Detalhado

```
HTML carrega CSS (tokens → core → layout → theme → motion → icons)
       │
       ▼
HTML carrega JS (EventBus → ComponentBase → ServiceContainer → StateManager → FiscalUI)
       │
       ▼
app.js: new FiscalUI() → FiscalUI.init()
       │
       ▼
EventBus criado
       │
       ▼
ServiceContainer criado → registra EventBus
       │
       ▼
StateManager criado → registra no container
       │
       ▼
Router | Responsive | A11y | Motion | Icons | Plugin — engines criadas
       │
       ▼
Engines inicializadas (Promise.all)
       │
       ▼
Tema restaurado do localStorage
       │
       ▼
Evento "framework:ready" disparado
       │
       ▼
Aplicação pode iniciar (app.js continua)
       │
       ▼
Router processa URL → carrega módulo
       │
       ▼
Componentes são montados
```

## 6.3 EventBus — Pub/Sub Central

O EventBus é o sistema de comunicação do FiscalUI. Nenhum componente ou serviço se comunica diretamente com outro. Toda comunicação passa pelo EventBus.

### 6.3.1 API

```js
class EventBus {
    on(event, callback, context)     // Escuta evento
    off(event, callback)             // Remove listener
    emit(event, payload)             // Dispara evento
    once(event, callback)            // Escuta uma única vez
    clear()                          // Remove todos os listeners
    getListeners(event)              // Retorna listeners de um evento
}
```

### 6.3.2 Convenção de Nomes

```
namespace:action
```

Exemplos:

```
framework:ready
router:change
responsive:breakpoint
theme:change
state:change
button:click
modal:open
modal:close
data:loaded
data:error
form:submit
grid:sort
```

### 6.3.3 Regras

1. Eventos são strings no formato `namespace:action`.
2. Namespace é o nome do módulo que dispara o evento.
3. Action é o verbo no passado (exceto para eventos de estado contínuo).
4. Payload é um objeto, nunca um valor primitivo.
5. Listeners não devem modificar o payload (imutabilidade).

### 6.3.4 Exemplo Completo

```js
// Componente Button dispara
class Button extends ComponentBase {
    onClick(e) {
        if (this.opts.loading || this.opts.disabled) return;
        this.framework.events.emit("button:click", {
            element: this.element,
            variant: this.opts.variant,
            originalEvent: e
        });
    }
}

// Qualquer módulo escuta
FiscalUI.events.on("button:click", (payload) => {
    console.log(`Botão ${payload.variant} clicado`);
});
```

## 6.4 ServiceContainer — Injeção de Dependências

O ServiceContainer gerencia o ciclo de vida de todos os serviços do Framework. Ele implementa um padrão de Service Locator, permitindo que qualquer módulo resolva suas dependências sem conhecimento de como são criadas.

### 6.4.1 API

```js
class ServiceContainer {
    register(name, instance)       // Registra serviço
    get(name)                      // Resolve serviço
    has(name)                      // Verifica existência
    remove(name)                   // Remove serviço
    clear()                        // Remove todos
    getNames()                     // Lista serviços registrados
}
```

### 6.4.2 Exemplo

```js
// Registro
FiscalUI.container.register("http", new HTTPService());
FiscalUI.container.register("auth", new AuthService());
FiscalUI.container.register("toast", new ToastService());

// Resolução em componentes
class DataGrid extends ComponentBase {
    constructor(opts) {
        super(opts);
        this.http = FiscalUI.container.get("http");
        this.toast = FiscalUI.container.get("toast");
    }
}
```

---

# 7. Componentes

## 7.1 O que é um Componente no FiscalUI

Um componente é uma unidade autônoma de interface que encapsula HTML, CSS e comportamento JavaScript. Todo componente:

- Possui uma responsabilidade única
- É instanciável
- Possui ciclo de vida gerenciado
- Comunica-se via EventBus
- Consome Design Tokens
- É acessível por padrão
- É responsivo por padrão

## 7.2 ComponentBase — Classe Base

Todos os componentes estendem `ComponentBase`.

### 7.2.1 API do ComponentBase

```js
class ComponentBase {
    constructor(opts = {}) {
        this.opts = opts;
        this.framework = window.FiscalUI;
        this.element = null;
        this.children = [];
        this._listeners = [];
        this._initialized = false;
    }

    // Ciclo de Vida
    create()          // Cria DOM element
    init()            // Registra eventos
    render()          // Atualiza DOM
    destroy()         // Remove eventos + DOM

    // Utilitários
    on(event, callback)        // Escuta evento (auto cleanup)
    emit(event, payload)       // Dispara evento
    listenTo(el, event, fn)    // Escuta DOM event (auto cleanup)
    find(selector)             // Query dentro do componente
    findAll(selector)          // QueryAll dentro do componente
    addChild(component)        // Gerencia sub-componente
    removeChild(component)     // Remove sub-componente

    // Template
    template()                 // Retorna HTML string
    renderTo(container)        // Anexa ao DOM

    // Estado
    setState(state)            // Atualiza estado interno
    getState()                 // Retorna estado interno
}
```

### 7.2.2 Exemplo de Componente

```js
class Button extends ComponentBase {
    constructor(opts) {
        super(opts);
        this.state = { loading: false, disabled: false };
    }

    template() {
        const { label, variant = "primary", size = "md", icon } = this.opts;
        const cls = `ui-btn ui-btn--${variant} ui-btn--${size}`;

        return `
            <button class="${cls}" type="button">
                ${icon ? `<svg class="ui-btn__icon icon icon-sm"><use href="#${icon}"/></svg>` : ''}
                <span class="ui-btn__label">${label}</span>
                <span class="ui-btn__spinner spinner" aria-hidden="true" hidden></span>
            </button>
        `;
    }

    create() {
        this.element = this.templateToDOM(this.template());
    }

    init() {
        this.listenTo(this.element, 'click', (e) => this.onClick(e));
    }

    setLoading(loading) {
        this.state.loading = loading;
        this.render();
    }

    render() {
        this.element.classList.toggle('ui-btn--loading', this.state.loading);
        const spinner = this.find('.ui-btn__spinner');
        if (spinner) spinner.hidden = !this.state.loading;
        this.element.disabled = this.state.loading || this.state.disabled;
    }

    onClick(e) {
        if (this.state.loading || this.opts.disabled) return;
        this.emit('button:click', { variant: this.opts.variant });
        if (this.opts.onClick) this.opts.onClick(e);
    }

    destroy() {
        super.destroy();
    }
}
```

## 7.3 Tipos de Componentes

### 7.3.1 Componentes Atômicos

Componentes simples, sem estado interno significativo. Exemplos: Button, Badge, Avatar, Icon.

### 7.3.2 Componentes Moleculares

Componentes com estado interno e composição de atômicos. Exemplos: Card, Tooltip, Progress.

### 7.3.3 Componentes Organísmicos

Componentes complexos com estado, sub-componentes e comunicação com serviços. Exemplos: Modal, DataGrid, Form, Dashboard.

### 7.3.4 Componentes de Layout

Componentes que organizam outros componentes no espaço. Exemplos: Sidebar, Toolbar, Tabs, Accordion, Grid.

## 7.4 Registro de Componentes

Componentes podem ser registrados globalmente para uso declarativo:

```js
// Registro
FiscalUI.registerComponent('button', Button);
FiscalUI.registerComponent('card', Card);
FiscalUI.registerComponent('modal', Modal);

// Uso declarativo
<div data-component="button" data-opts='{"label":"Salvar","variant":"primary"}'></div>

// O FiscalUI.scan() processa data-component no DOM
FiscalUI.scan(document.getElementById('app'));
```

---

# 8. Serviços

## 8.1 O que é um Serviço

Um serviço é um módulo de infraestrutura que executa operações específicas sem manter estado visual. Diferente de componentes, serviços não renderizam HTML.

## 8.2 Serviços Oficiais

| Serviço | Responsabilidade |
|---------|-----------------|
| HTTPService | Requisições HTTP (GET, POST, PUT, PATCH, DELETE) |
| AuthService | Login, logout, refresh token, sessão |
| ToastService | Notificações toast |
| ModalService | Janelas modais |
| LoadingService | Indicador de carregamento global |
| DialogService | Confirmações, alertas, prompts |
| StorageService | Abstração sobre localStorage/sessionStorage/IndexedDB |
| CacheService | Cache LRU com TTL |
| LoggerService | Log estruturado |
| i18nService | Internacionalização |
| FormatService | Formatação de datas, moedas, documentos |
| ValidateService | Validação de formulários |
| PrintService | Impressão de documentos |
| DownloadService | Download de arquivos |
| UploadService | Upload com progresso |

## 8.3 Interface de Serviço

```js
class BaseService {
    constructor(framework) {
        this.framework = framework;
        this.name = 'BaseService';
    }

    async init() {
        // Inicialização assíncrona opcional
    }

    destroy() {
        // Limpeza opcional
    }
}
```

## 8.4 Registro e Resolução

```js
// Registro manual
FiscalUI.registerService('http', new HTTPService(FiscalUI));
FiscalUI.registerService('toast', new ToastService(FiscalUI));

// Ou automático via ServiceContainer
FiscalUI.container.register('http', HTTPService);
FiscalUI.container.register('toast', ToastService);
FiscalUI.container.resolveAll(); // Instancia todos

// Resolução
const http = FiscalUI.getService('http');
const toast = FiscalUI.getService('toast');
```

## 8.5 Ciclo de Vida de Serviço

```
Registro (register)
   │
   ▼
Inicialização (init) — assíncrono, resolvido pelo container
   │
   ▼
Uso — componentes consomem via getService()
   │
   ▼
Destruição (destroy) — quando o Framework é descarregado
```

---

# 9. Eventos

## 9.1 Sistema de Eventos

O FiscalUI possui três tipos de evento:

| Tipo | Mecanismo | Uso |
|------|-----------|-----|
| Eventos do Framework | EventBus | Comunicação entre módulos |
| Eventos de DOM | addEventListener | Interação do usuário |
| Eventos de Estado | StateManager observers | Reação a mudanças de estado |

## 9.2 EventBus (Pub/Sub)

Já detalhado na seção 6.3. Aqui estão os eventos oficiais do Framework:

### 9.2.1 Eventos do Framework

```
framework:ready           → Framework inicializado
framework:error           → Erro não tratado
framework:destroy         → Framework sendo destruído

theme:change              → Tema alterado
theme:before-change       → Tema será alterado

router:change             → Rota alterada
router:before-change      → Rota será alterada
router:not-found          → Rota não encontrada

responsive:breakpoint     → Breakpoint mudou
responsive:orientation    → Orientação mudou
responsive:resize         → Viewport redimensionada

state:change              → Estado global alterado
state:change:{key}        → Chave específica alterada

a11y:announce             → Anúncio para screen reader
a11y:focus-trap           → Foco preso em container
a11y:focus-release        → Foco liberado

motion:reduced            → prefers-reduced-motion detectado
motion:animation-end      → Animação concluída

icons:loaded              → Sprite SVG carregado
icons:error               → Falha ao carregar sprite

plugins:register          → Plugin registrado
plugins:before-init       → Plugin será inicializado
plugins:ready             → Plugin inicializado
plugins:error             → Plugin falhou ao inicializar
```

### 9.2.2 Eventos de Componentes

```
button:click
card:hover
modal:open
modal:close
modal:confirm
modal:cancel
drawer:open
drawer:close
toast:show
toast:hide
tab:change
accordion:toggle
tooltip:show
tooltip:hide
dropdown:open
dropdown:close
form:submit
form:validate
form:validate-error
form:validate-success
form:serialize
grid:sort
grid:filter
grid:select
grid:page
grid:load
grid:loaded
grid:error
```

## 9.3 Padrão de Implementação

```js
// Disparar evento
this.emit('component:action', {
    source: this,
    data: { /* payload */ }
});

// Escutar evento (com auto cleanup na destruição)
this.on('framework:ready', () => {
    console.log('Framework pronto');
});

// Escutar evento de outro componente
FiscalUI.events.on('modal:confirm', (payload) => {
    this.saveData(payload.data);
});
```

---

# 10. Estado Global

## 10.1 StateManager

O StateManager gerencia o estado global do Framework. Ele é reativo: quando o estado muda, observadores são notificados automaticamente.

## 10.2 API

```js
class StateManager {
    constructor(eventBus) {
        this.state = {};
        this.eventBus = eventBus;
    }

    get(key)                // Retorna valor de uma chave
    set(key, value)         // Define valor e notifica
    has(key)                // Verifica se chave existe
    remove(key)             // Remove chave
    clear()                 // Limpa todo o estado
    observe(key, callback)  // Observa mudanças em uma chave
    unobserve(key, callback)// Remove observador
    snapshot()              // Retorna cópia do estado
    persist(keys)           // Salva chaves no localStorage
    restore(keys)           // Restaura chaves do localStorage
}
```

## 10.3 Estado Oficial do Framework

```js
// Estado inicial padrão
{
    // Framework
    initialized: false,
    version: "1.0.0",
    debug: false,

    // Tema
    theme: "dark",
    themeAvailable: ["dark", "light", "high-contrast"],

    // Router
    route: null,
    routeParams: {},
    moduleId: null,

    // Responsivo
    breakpoint: "lg",
    isMobile: false,
    isTablet: false,
    isDesktop: true,
    viewportWidth: 1440,
    viewportHeight: 900,

    // Acessibilidade
    reducedMotion: false,
    highContrast: false,
    focusVisible: false,

    // Aplicação
    user: null,
    authenticated: false,
    loading: false,
    notifications: []
}
```

## 10.4 Exemplos de Uso

```js
// Ler estado
const theme = FiscalUI.state.get('theme');
const isMobile = FiscalUI.state.get('isMobile');

// Definir estado
FiscalUI.state.set('theme', 'light');

// Observar mudanças
const unsub = FiscalUI.state.observe('breakpoint', (newVal, oldVal) => {
    console.log(`Breakpoint mudou: ${oldVal} → ${newVal}`);
    if (newVal === 'xs') sidebar.collapse();
});

// Estado reativo em componentes
class Sidebar extends ComponentBase {
    init() {
        this.on('state:change:breakpoint', (payload) => {
            if (payload.value === 'xs') this.toDrawer();
        });
    }
}
```

## 10.5 Persistência

```js
// Salvar preferências do usuário
FiscalUI.state.persist(['theme', 'sidebarCollapsed', 'lang']);

// Restaurar ao iniciar
FiscalUI.state.restore(['theme', 'sidebarCollapsed', 'lang']);
```

---

# 11. Ciclo de Vida

## 11.1 Ciclo de Vida do Framework

```
HTML carrega → CSS carrega → JS carrega → FiscalUI.init()
   │
   ▼
framework:ready → Aplicação inicia
   │
   ▼
Aplicação roda (anos)
   │
   ▼
Usuário sai → FiscalUI.destroy() → framework:destroy
```

## 11.2 Ciclo de Vida de Componentes

```
Criação (create)
   │
   ▼
Inicialização (init) → Registra eventos
   │
   ▼
Renderização (render) → Atualiza DOM
   │
   ▼
Renderizações parciais (re-render)
   │
   ▼
Destruição (destroy) → Remove eventos + DOM
```

### 11.2.1 create()

Cria o elemento DOM do componente a partir de um template.

```js
create() {
    this.element = document.createElement('div');
    this.element.className = 'ui-component';
    this.element.innerHTML = this.template();
}
```

### 11.2.2 init()

Registra event listeners e inicializa sub-componentes.

```js
init() {
    this.listenTo(this.element, 'click', this.onClick);
    this.listenTo(document, 'keydown', this.onKeyDown);
    this.on('state:change', this.onStateChange);
    this.children.forEach(child => child.init());
}
```

### 11.2.3 render()

Atualiza o DOM do componente sem recriá-lo.

```js
render() {
    this.element.classList.toggle('is-active', this.state.active);
    this.element.querySelector('.ui-component__label').textContent = this.state.label;
}
```

### 11.2.4 destroy()

Remove listeners, sub-componentes e o elemento do DOM.

```js
destroy() {
    // Remove event listeners (automático via ComponentBase)
    super.destroy();

    // Remove sub-componentes
    this.children.forEach(child => child.destroy());
    this.children = [];

    // Remove do DOM
    if (this.element && this.element.parentNode) {
        this.element.parentNode.removeChild(this.element);
    }

    // Remove referências
    this.element = null;
    this.framework = null;
}
```

## 11.3 Ciclo de Vida de Serviços

```
Registro → init() → Uso → destroy()
```

## 11.4 Ciclo de Vida de Engines

```
Construtor → init() (assíncrono) → Uso → destroy()
```

## 11.5 Ciclo de Vida da Aplicação (SPA)

```
Usuário clica em link
   │
   ▼
Router intercepta → event: router:before-change
   │
   ▼
Componente atual é destruído (destroy)
   │
   ▼
Novo módulo é carregado
   │
   ▼
Componentes do módulo são criados (create)
   │
   ▼
Componentes são inicializados (init)
   │
   ▼
event: router:change → Módulo visível
```

---

# 12. Renderização

## 12.1 Filosofia de Renderização

O FiscalUI não utiliza Virtual DOM. A renderização é feita por atualização direta do DOM real, seguindo os princípios:

1. **Mínimo de manipulações** — alterar apenas o que mudou
2. **Sem reconciliação difusa** — o componente sabe exatamente o que mudou via setState
3. **Re-render completo quando necessário** — para mudanças grandes, o template é reexecutado

## 12.2 Quando o Componente Re-renderiza

1. `setState()` é chamado — atualiza estado interno e chama `render()`
2. `render()` é chamado explicitamente
3. Observador de estado global notifica mudança

## 12.3 Estratégias de Renderização

### 12.3.1 Renderização Direta (padrão)

```js
class Button extends ComponentBase {
    render() {
        // Atualiza classes
        this.element.className = `ui-btn ui-btn--${this.opts.variant} ui-btn--${this.opts.size}`;

        // Atualiza atributos
        this.element.disabled = this.opts.disabled || this.state.loading;

        // Atualiza conteúdo
        this.element.querySelector('.ui-btn__label').textContent = this.opts.label;

        // Estado loading
        this.element.querySelector('.ui-btn__spinner').hidden = !this.state.loading;
    }
}
```

### 12.3.2 Renderização por Sub-Componente

Componentes complexos delegam renderização a sub-componentes:

```js
class DataGrid extends ComponentBase {
    render() {
        // Header não re-renderiza se colunas não mudaram
        if (this._columnsChanged) {
            this.header.render();
        }

        // Body re-renderiza apenas linhas visíveis
        this.body.render(this.getVisibleRows());
    }
}
```

### 12.3.3 Renderização com Template String (para mudanças completas)

```js
class Card extends ComponentBase {
    render() {
        // Regenera HTML completo
        this.element.innerHTML = this.template();
        // Re-inicializa eventos
        this.init();
    }
}
```

---

# 13. Organização

## 13.1 Estrutura de Diretórios (Completa)

```
fiscalui/
│
├── index.html                  Launchpad + Workspace
├── login.html                  Tela de autenticação
├── server.py                   Servidor de desenvolvimento Python
│
├── css/
│   ├── tokens.css              Design Tokens
│   ├── core.css                Reset, tipografia, utilitários
│   ├── layout.css              Grid, containers
│   ├── theme.css               Tema Light, High Contrast
│   ├── motion.css              Animações, keyframes
│   ├── icons.css               Classes de ícones
│   ├── components/             Estilos por componente
│   │   ├── button.css
│   │   ├── card.css
│   │   ├── modal.css
│   │   └── ...
│   └── pages/                  Estilos por página
│       ├── login.css
│       └── dashboard.css
│
├── js/
│   ├── core/
│   │   ├── FiscalUI.js         Orquestrador principal
│   │   ├── ComponentBase.js    Classe base de componentes
│   │   └── ServiceContainer.js Injeção de dependências
│   ├── events/
│   │   └── EventBus.js         Pub/sub
│   ├── state/
│   │   └── StateManager.js     Estado global
│   ├── router/
│   │   └── Router.js           Navegação SPA
│   ├── responsive/
│   │   └── ResponsiveEngine.js Breakpoints
│   ├── accessibility/
│   │   └── AccessibilityEngine.js Acessibilidade
│   ├── motion/
│   │   └── MotionEngine.js     Animações
│   ├── icons/
│   │   └── IconEngine.js       Gerenciamento de ícones
│   ├── plugins/
│   │   └── PluginEngine.js     Gerenciamento de plugins
│   ├── services/               Serviços de infraestrutura
│   │   ├── HTTPService.js
│   │   ├── AuthService.js
│   │   ├── ToastService.js
│   │   ├── ModalService.js
│   │   ├── LoadingService.js
│   │   ├── StorageService.js
│   │   ├── CacheService.js
│   │   ├── LoggerService.js
│   │   ├── i18nService.js
│   │   └── ...
│   ├── components/             Componentes visuais
│   │   ├── Button.js
│   │   ├── Card.js
│   │   ├── Modal.js
│   │   ├── DataGrid.js
│   │   └── ...
│   ├── utils/                  Utilitários
│   │   ├── format.js           Datas, moedas, documentos
│   │   └── helpers.js          Debounce, throttle, uuid
│   └── app.js                  Inicialização da aplicação
│
├── assets/
│   ├── fonts/                  Inter (self-hosted)
│   ├── data/
│   │   ├── menu.json           Navegação
│   │   └── messages.json       Strings i18n
│   └── img/
│       └── icons.svg           Sprte SVG
│
├── img/
│   └── logo.svg                Logotipo
│
├── sprints/                    Documentação
│   ├── componentes/            RFCs de componentes
│   └── ... (demais capítulos)
│
├── FISCALUI.md                 RFC mestre
│
└── README.md
```

## 13.2 Convenções de Organização

| Recurso | Convenção | Exemplo |
|---------|-----------|---------|
| Arquivos CSS | kebab-case | `data-grid.css` |
| Arquivos JS | PascalCase (classes) kebab-case (arquivos) | `class DataGrid` → `data-grid.js` |
| Classes CSS | BEM: `.ui-nome__elemento--modificador` | `.ui-btn__icon--large` |
| IDs | camelCase | `#sidebar`, `#launchpad` |
| Constantes | UPPER_SNAKE_CASE | `DEFAULT_TIMEOUT` |
| Variáveis | camelCase | `userName`, `isVisible` |
| Métodos | camelCase | `setLoading()`, `render()` |
| Pastas | kebab-case | `css/components/` |

---

# 14. Performance

## 14.1 Metas de Performance

| Métrica | Target | Medição |
|---------|--------|---------|
| Time to Interactive | < 500ms | Lighthouse |
| First Contentful Paint | < 300ms | Lighthouse |
| Bundle total (gzip) | < 50KB | Build report |
| Scroll | 60 FPS | DevTools Performance |
| Re-render | < 16ms | performance.now() |
| Cache hit | > 80% | CacheService stats |
| Lighthouse score | ≥ 95 | Lighthouse CI |

## 14.2 Estratégias de Performance

### 14.2.1 Virtual DOM não utilizado

Escolha intencional. Para aplicações ERP, a árvore DOM raramente ultrapassa alguns milhares de nós. O custo de um Virtual DOM não se justifica.

### 14.2.2 Virtualização de grids

Para DataGrid com > 1000 linhas, apenas as linhas visíveis são renderizadas no DOM (viewport + buffer). O cálculo é feito pelo VirtualScroll interno do DataGrid.

### 14.2.3 Lazy loading de módulos

Módulos ERP (NF-e, Produtos, etc.) são carregados sob demanda via import() dinâmico ou script tag.

### 14.2.4 Sprite SVG único

Todos os ícones em uma única requisição HTTP. Zero requests por ícone.

### 14.2.5 CSS modular sem imports

Cada arquivo CSS é carregado via `<link>` no HTML. Sem @import, sem CSS-in-JS, sem build step.

### 14.2.6 Fonte self-hosted

Inter é servida localmente como woff2. Zero requisição externa de fontes.

### 14.2.7 GPU-accelerated animations

Todas as animações usam `transform` e `opacity` (propriedades aceleradas por GPU). Nunca `width`, `height`, `top`, `left`.

```css
/* ❌ Ruim — causa reflow */
.modal { left: 100px; transition: left 250ms; }

/* ✅ Bom — GPU acelerado */
.modal { transform: translateX(100px); transition: transform 250ms; }
```

### 14.2.8 Debounce e Throttle

Eventos de alto volume (resize, scroll, input) utilizam debounce/throttle:

```js
// Utilitários disponíveis
FiscalUI.utils.debounce(fn, 150);    // Input search
FiscalUI.utils.throttle(fn, 16);     // Scroll/resize (60fps)
```

### 14.2.9 Reflow mínimo

Manipulações de DOM são minimizadas através de batch updates. Componentes acumulam mudanças e aplicam em um único cycle:

```js
class DataGrid extends ComponentBase {
    addRows(rows) {
        // Acumula mudanças
        this._pendingRows.push(...rows);
        // Agenda render para próximo frame
        if (!this._raf) {
            this._raf = requestAnimationFrame(() => {
                this.render();
                this._raf = null;
            });
        }
    }
}
```

## 14.3 Monitoramento

```js
// Performance marks automáticos
FiscalUI.events.on('framework:ready', () => {
    performance.mark('fiscalui-ready');
    performance.measure('fiscalui-init', 'fiscalui-start', 'fiscalui-ready');
});
```

---

# 15. Segurança

## 15.1 Princípios

1. **Nunca confie no cliente** — toda validação definitiva é feita no backend
2. **Mínimo privilégio** — o frontend só tem acesso ao que precisa
3. **Defesa em profundidade** — múltiplas camadas de proteção
4. **Segurança por padrão** — as configurações seguras são o default

## 15.2 Práticas no Frontend

### 15.2.1 XSS (Cross-Site Scripting)

```js
// ❌ Nunca usar innerHTML com dados não sanitizados
element.innerHTML = userInput;

// ✅ Usar textContent
element.textContent = userInput;

// ✅ Ou sanitizar com DOMPurify (quando necessário)
element.innerHTML = DOMPurify.sanitize(userInput);
```

### 15.2.2 CSRF (Cross-Site Request Forgery)

Toda requisição ao backend inclui token CSRF no header:

```js
HTTPService.prototype.request = function(method, url, data) {
    const headers = {
        'X-CSRF-Token': this.getCSRFToken(),
        'Content-Type': 'application/json'
    };
    return fetch(url, { method, headers, body: JSON.stringify(data) });
};
```

### 15.2.3 Armazenamento Seguro

```js
// ❌ Nunca armazenar tokens JWT em localStorage sem proteção
localStorage.setItem('token', jwt);

// ✅ Utilizar httpOnly cookies quando possível
// ✅ Se for necessário localStorage, ao menos criptografar
StorageService.prototype.setSecure = function(key, value) {
    const encrypted = btoa(JSON.stringify(value)); // Simbólico — usar crypto real
    localStorage.setItem(`_secure_${key}`, encrypted);
};
```

### 15.2.4 Content Security Policy

```html
<meta http-equiv="Content-Security-Policy" content="
    default-src 'self';
    script-src 'self';
    style-src 'self' 'unsafe-inline';
    img-src 'self' data:;
    font-src 'self';
    connect-src 'self' https://api.fiscalui.com;
">
```

### 15.2.5 Autenticação

```js
class AuthService {
    async login(username, password) {
        // Nunca logar senhas
        // Nunca enviar senha em URL
        // Usar HTTPS obrigatório
        const response = await fetch('https://api.fiscalui.com/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        // Token armazenado via callback, não diretamente
        return response.json();
    }
}
```

---

# 16. Extensibilidade

## 16.1 Formas de Estender o FiscalUI

O FiscalUI pode ser estendido por:

1. **Plugins** — funcionalidades novas que se integram ao EventBus
2. **Temas** — novos conjuntos de Design Tokens
3. **Componentes** — novos componentes visuais que estendem ComponentBase
4. **Serviços** — novos serviços registrados no ServiceContainer
5. **Ícones** — novos ícones adicionados ao sprite SVG

## 16.2 Plugin Engine

### 16.2.1 Interface de Plugin

```js
class Plugin {
    constructor(framework) {
        this.id = 'meu-plugin';
        this.name = 'Meu Plugin';
        this.version = '1.0.0';
        this.framework = framework;
        this.dependencies = []; // IDs de plugins necessários
    }

    async init() {
        // Registra listeners
        this.framework.events.on('button:click', this.onButtonClick);
    }

    destroy() {
        this.framework.events.off('button:click', this.onButtonClick);
    }
}
```

### 16.2.2 Registro

```js
// Registrar plugin
FiscalUI.plugins.register(MeuPlugin);

// Habilitar/desabilitar
FiscalUI.plugins.enable('meu-plugin');
FiscalUI.plugins.disable('meu-plugin');

// Listar plugins ativos
FiscalUI.plugins.getActive(); // ['meu-plugin', 'outro-plugin']
```

## 16.3 Criação de Temas

```css
/* Adicionar novo tema no themes.css */
[data-theme="corporate"] {
    --color-primary: #1e40af;
    --color-primary-hover: #1e3a8a;
    --bg-gradient: linear-gradient(135deg, #f8fafc, #e2e8f0);
    --glass-bg: rgba(255, 255, 255, 0.85);
    --text-primary: #0f172a;
}

/* Registrar */
FiscalUI.theme.register('corporate', {
    name: 'Corporate',
    icon: 'icon-building'
});
```

## 16.4 Criação de Componentes

```js
class MeuComponente extends ComponentBase {
    // Seguir o template de componente (seção 7.2.2)
}

// Registrar globalmente
FiscalUI.registerComponent('meu-componente', MeuComponente);
```

## 16.5 Criação de Serviços

```js
class MeuServico extends BaseService {
    constructor(framework) {
        super(framework);
        this.name = 'meu-servico';
    }

    async init() {
        // Configuração inicial
    }

    minhaFuncao() {
        // Implementação
    }
}

// Registrar
FiscalUI.registerService('meu-servico', new MeuServico(FiscalUI));

// Consumir
const svc = FiscalUI.getService('meu-servico');
svc.minhaFuncao();
```

---

# 17. Roadmap

## 17.1 Versão 1.0 — Fundação e Componentes Essenciais

**Status:** Em desenvolvimento

### Nível 1 — Fundação
- [x] Arquitetura Base (este documento)
- [ ] Design Tokens
- [ ] Theme Engine
- [ ] CSS Core
- [ ] Layout Core
- [ ] Component Base
- [ ] JavaScript Core
- [ ] Event Bus
- [ ] Service Container
- [ ] State Manager
- [ ] Router
- [ ] Responsive Engine
- [ ] Accessibility Engine
- [ ] Motion Engine
- [ ] Icon Engine
- [ ] Plugin Engine
- [ ] Build System
- [ ] Testing Framework

### Nível 2 — Componentes Fundamentais
- [ ] Button
- [ ] Icon Button
- [ ] Link
- [ ] Card
- [ ] Panel
- [ ] Divider
- [ ] Badge
- [ ] Avatar

### Nível 3 — Navegação
- [ ] Toolbar
- [ ] Sidebar
- [ ] Menu
- [ ] Navbar
- [ ] Breadcrumb
- [ ] Tabs
- [ ] Accordion

### Nível 4 — Formulários
- [ ] Form
- [ ] Input
- [ ] Select
- [ ] Autocomplete
- [ ] Checkbox
- [ ] Radio
- [ ] Switch
- [ ] Upload
- [ ] DatePicker
- [ ] Money
- [ ] CPF
- [ ] CNPJ

### Nível 5 — Componentes Corporativos
- [ ] Data Grid
- [ ] Tree Grid
- [ ] Dashboard
- [ ] Charts
- [ ] Scheduler
- [ ] Calendar

## 17.2 Versão 2.0 — Ecossistema

- CLI oficial
- Marketplace de componentes
- Gerador de projetos
- SDK para plugins
- Suporte a temas por empresa
- Ferramentas de debugging

## 17.3 Versão 3.0 — Inteligência Aumentada

- Editor visual drag-and-drop
- Gerador automático de CRUD
- Sugestões inteligentes
- Pesquisa por linguagem natural
- Assistente corporativo

## 17.4 Manutenção

O FiscalUI segue Semantic Versioning 2.0.0:

- **MAJOR**: mudanças incompatíveis na API pública
- **MINOR**: novas funcionalidades compatíveis
- **PATCH**: correções de bugs sem quebra de compatibilidade

Cada versão MAJOR tem suporte LTS de 3 anos.

---

# Apêndice A — Glossário

| Termo | Definição |
|-------|-----------|
| Componente | Unidade autônoma de interface com HTML/CSS/JS |
| Engine | Módulo transversal que fornece capacidade específica |
| Serviço | Módulo de infraestrutura sem estado visual |
| Design Token | Variável CSS que define um valor de design |
| Theme Engine | Sistema de troca de temas via data-theme |
| Event Bus | Pub/sub central para comunicação entre módulos |
| State Manager | Estado global reativo com observers |
| Service Container | Injeção de dependências |
| Plugin | Extensão que se integra ao EventBus |
| BEM | Block, Element, Modifier — convenção de nomenclatura CSS |

# Apêndice B — Referências

- FISCALUI.md — Documento RFC mestre
- `sprints/componentes/` — RFCs individuais de componentes
- `sprints/GUIA_DESENVOLVEDOR.md` — Guia de desenvolvimento
- `sprints/PLANO_DIRETOR.md` — Plano Diretor 10 anos

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial — documento fundacional de 60+ páginas |
