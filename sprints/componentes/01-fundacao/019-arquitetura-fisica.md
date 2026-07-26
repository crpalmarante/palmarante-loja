# FiscalUI Framework

## Fase 3 — Arquitetura Física

**Versão 1.0**

Este documento define como o FiscalUI será organizado no disco. Estrutura de diretórios, convenções de arquivos, empacotamento, sistema de build e distribuição. Nenhuma lógica de negócio aqui — apenas a planta física do projeto.

---

# Índice

1. Introdução
2. Estrutura Raiz
3. Core (`core/`)
4. Componentes (`components/`)
5. Layout (`layout/`)
6. Temas (`theme/`)
7. Tokens (`tokens/`)
8. Serviços (`services/`)
9. Router (`router/`)
10. Plugins (`plugins/`)
11. Ícones (`icons/`)
12. Animações (`animations/`)
13. Dashboard (`dashboard/`)
14. DataGrid (`datagrid/`)
15. Formulários (`forms/`)
16. Utilitários (`utils/`)
17. Vendor (`vendor/`)
18. Build (`build/`)
19. Documentação (`docs/`)
20. Convenções de Arquivos
21. Empacotamento
22. Distribuição
23. Ciclo de Build

---

# 1. Introdução

## 1.1 Propósito

Definir a organização física do código fonte do FiscalUI. Todo arquivo, pasta e módulo tem um lugar definido. Não há decisão de organização ad-hoc — cada diretório tem responsabilidade clara e exclusiva.

## 1.2 Princípios

```
1. Um arquivo, uma responsabilidade — nunca misturar concerns no mesmo arquivo
2. Nome do arquivo revela o conteúdo — sem abrir o arquivo para saber o que é
3. Profundidade máxima de 3 níveis — navegação rápida
4. Separação clara entre core e extensões — core nunca depende de componentes
5. Tudo que é público tem entry point explícito — nada vaza acidentalmente
```

---

# 2. Estrutura Raiz

```
FiscalUI/
│
├── core/                    # Núcleo do framework (zero dependência de componentes)
│   ├── event-bus/           # Sistema de comunicação pub/sub
│   ├── state/               # Gerenciamento de estado (Redux-like)
│   ├── router/              # Roteamento SPA
│   ├── di/                  # Service container / injeção de dependência
│   ├── component/           # Component base (UIComponent)
│   ├── scheduler/           # Event loop e scheduling
│   ├── registry/            # Registry de componentes, serviços, plugins
│   └── factory/             # Factory pattern para criação de instâncias
│
├── components/              # Componentes visuais do framework
│   ├── button/              # UIButton
│   ├── icon-button/         # UIIconButton
│   ├── card/                # UICard
│   ├── badge/               # UIBadge
│   ├── tag/                 # UITag
│   ├── spinner/             # UISpinner
│   ├── tooltip/             # UITooltip
│   ├── progress/            # UIProgress
│   ├── avatar/              # UIAvatar
│   ├── modal/               # UIModal
│   ├── toast/               # UIToast
│   ├── drawer/              # UIDrawer
│   ├── tabs/                # UITabs
│   ├── accordion/           # UIAccordion
│   ├── dropdown/            # UIDropdown
│   ├── menu/                # UIMenu
│   ├── table/               # UITable
│   └── datagrid/            # UIDataGrid
│
├── layout/                  # Sistema de layout
│   ├── workspace/           # Workspace (container principal)
│   ├── sidebar/             # Sidebar
│   ├── topbar/              # Topbar / header
│   ├── content/             # Área de conteúdo
│   ├── footer/              # Footer
│   ├── panel/               # Painéis (direita/esquerda)
│   └── grid/                # Sistema de grid
│
├── theme/                   # Sistema de temas
│   ├── themes/              # Temas oficiais (light, dark, high-contrast)
│   └── engine/              # Theme engine (aplicação de temas)
│
├── tokens/                  # Design tokens
│   ├── colors/              # Paleta de cores
│   ├── typography/          # Tipografia
│   ├── spacing/             # Espaçamentos
│   ├── sizing/              # Tamanhos
│   ├── borders/             # Bordas
│   ├── shadows/             # Sombras
│   ├── motion/              # Animações e transições
│   ├── z-index/             # Camadas
│   └── breakpoints/         # Breakpoints responsivos
│
├── services/                # Serviços do framework
│   ├── http/                # HTTP service
│   ├── auth/                # Autenticação
│   ├── cache/               # Cache
│   ├── logger/              # Logging
│   ├── config/              # Configurações
│   └── storage/             # LocalStorage / SessionStorage
│
├── plugins/                 # Sistema de plugins
│   └── engine/              # Plugin engine
│
├── icons/                   # Sistema de ícones
│   ├── svg/                 # SVGs individuais
│   └── engine/              # Icon engine
│
├── animations/              # Sistema de animações
│   └── engine/              # Motion engine
│
├── dashboard/               # Módulo de dashboard
│   ├── widgets/             # Widgets de dashboard
│   └── layouts/             # Layouts de dashboard
│
├── datagrid/                # Módulo de DataGrid
│   ├── columns/             # Tipos de coluna
│   ├── editors/             # Editores in-cell
│   ├── filters/             # Filtros
│   ├── renderers/           # Renderizadores customizados
│   ├── sorters/             # Ordenadores
│   └── plugins/             # Plugins do datagrid
│
├── forms/                   # Módulo de formulários
│   ├── inputs/              # Inputs (text, number, date, etc.)
│   ├── selects/             # Selects e combo
│   ├── checkboxes/          # Checkboxes e radios
│   ├── validators/          # Validadores
│   └── layout/              # Layout de formulários
│
├── utils/                   # Utilitários
│   ├── dom/                 # Manipulação DOM
│   ├── format/              # Formatação (moeda, data, CPF/CNPJ)
│   ├── math/                # Operações matemáticas
│   ├── string/              # Manipulação de strings
│   ├── array/               # Manipulação de arrays
│   ├── object/              # Manipulação de objetos
│   ├── date/                # Manipulação de datas
│   ├── validation/          # Validação genérica
│   └── debounce/            # Debounce e throttle
│
├── vendor/                  # Dependências externas (se necessárias)
│   └── .gitkeep
│
├── build/                   # Scripts de build e config
│   ├── scripts/             # Scripts de build
│   ├── postcss/             # Config PostCSS
│   ├── esbuild/             # Config esbuild
│   └── karma/               # Config Karma
│
├── docs/                    # Documentação
│   └── sprints/             # RFCs e especificações
│
├── test/                    # Testes
│   ├── unit/                # Testes unitários
│   ├── integration/         # Testes de integração
│   ├── e2e/                 # Testes end-to-end
│   ├── fixtures/            # Dados de teste
│   └── mocks/               # Mocks e stubs
│
├── package.json
├── fiscalui.json            # Configuração do framework
├── README.md
├── LICENSE
└── CHANGELOG.md
```

---

# 3. Core (`core/`)

Módulos fundamentais do framework. Zero dependência de componentes.

```
core/
├── event-bus/
│   ├── event-bus.js         # Classe EventBus
│   ├── event-bus.test.js    # Testes
│   └── README.md            # Documentação interna
│
├── state/
│   ├── state-manager.js     # Classe StateManager
│   ├── state-manager.test.js
│   └── README.md
│
├── router/
│   ├── router.js            # Classe Router
│   ├── route.js             # Classe Route (config)
│   ├── router.test.js
│   └── README.md
│
├── di/
│   ├── service-container.js # Classe ServiceContainer
│   ├── service-container.test.js
│   └── README.md
│
├── component/
│   ├── ui-component.js      # Classe base UIComponent
│   ├── ui-component.test.js
│   └── README.md
│
├── scheduler/
│   ├── scheduler.js         # Event loop scheduling
│   └── scheduler.test.js
│
├── registry/
│   ├── registry.js          # Registry genérico
│   └── registry.test.js
│
└── factory/
    ├── factory.js           # Factory pattern
    └── factory.test.js
```

### Convenções

```
- Cada módulo do core tem sua própria pasta
- Arquivo principal tem o mesmo nome da pasta
- Testes ficam junto do código (não em pasta separada)
- README.md documenta API pública do módulo
```

---

# 4. Componentes (`components/`)

Cada componente visual tem sua própria pasta com CSS + JS + testes.

```
components/
├── button/
│   ├── button.js            # Classe UIButton
│   ├── button.css           # Estilos (BEM)
│   ├── button.test.js       # Testes do componente
│   └── README.md
│
├── modal/
│   ├── modal.js
│   ├── modal.css
│   ├── modal.test.js
│   └── README.md
│
├── toast/
│   ├── toast.js
│   ├── toast.css
│   ├── toast.test.js
│   └── README.md
│
├── datagrid/
│   ├── datagrid.js
│   ├── datagrid.css
│   ├── datagrid.test.js
│   ├── datagrid-column.js
│   ├── datagrid-sort.js
│   ├── datagrid-filter.js
│   └── README.md
│
└── ... (demais componentes)
```

### Convenções

```
- Pasta nomeada no singular sem prefixo: button, modal, toast
- Classe JS prefixada com UI: UIButton, UIModal, UIToast
- CSS prefixado com ui-: .ui-btn, .ui-modal, .ui-toast
- Componente complexo pode ter múltiplos arquivos JS (ex: datagrid)
- Todo componente tem testes
```

---

# 5. Layout (`layout/`)

Sistema de layout do Workspace.

```
layout/
├── workspace/
│   ├── workspace.js         # Workspace (container de toda UI)
│   ├── workspace.css
│   └── workspace.test.js
│
├── sidebar/
│   ├── sidebar.js
│   ├── sidebar.css
│   └── sidebar.test.js
│
├── topbar/
│   ├── topbar.js
│   ├── topbar.css
│   └── topbar.test.js
│
├── content/
│   ├── content.js
│   ├── content.css
│   └── content.test.js
│
├── footer/
│   ├── footer.js
│   ├── footer.css
│   └── footer.test.js
│
├── panel/
│   ├── panel.js
│   ├── panel.css
│   └── panel.test.js
│
└── grid/
    ├── grid.css             # Grid responsivo (CSS puro)
    └── grid.test.js
```

---

# 6. Temas (`theme/`)

Sistema de temas. Cada tema é um arquivo CSS com variáveis.

```
theme/
├── engine/
│   ├── theme-engine.js      # Aplicação e gerenciamento de temas
│   └── theme-engine.test.js
│
├── themes/
│   ├── light.css            # Tema claro (padrão)
│   ├── dark.css             # Tema escuro
│   ├── high-contrast.css    # Alto contraste (acessibilidade)
│   └── corporate.css        # Tema corporativo (exemplo)
│
└── README.md
```

---

# 7. Tokens (`tokens/`)

Design tokens em CSS custom properties.

```
tokens/
├── colors/
│   ├── colors.css           # Paleta completa
│   └── colors.test.js       # Testes de contraste
│
├── typography/
│   ├── typography.css       # Fontes, tamanhos, pesos
│   └── typography.test.js
│
├── spacing/
│   └── spacing.css          # Espaçamentos (4px base)
│
├── sizing/
│   └── sizing.css           # Tamanhos de componentes
│
├── borders/
│   └── borders.css          # Border radius, border width
│
├── shadows/
│   └── shadows.css          # Box shadows (elevação)
│
├── motion/
│   └── motion.css           # Durações e easings
│
├── z-index/
│   └── z-index.css          # Camadas (stacking context)
│
└── breakpoints/
    └── breakpoints.css      # Media query breakpoints
```

---

# 8. Serviços (`services/`)

Serviços do framework.

```
services/
├── http/
│   ├── http-service.js      # Requisições HTTP (fetch wrapper)
│   └── http-service.test.js
│
├── auth/
│   ├── auth-service.js      # Autenticação e sessão
│   └── auth-service.test.js
│
├── cache/
│   ├── cache-service.js     # Cache em memória
│   └── cache-service.test.js
│
├── logger/
│   ├── logger-service.js    # Logging
│   └── logger-service.test.js
│
├── config/
│   ├── config-service.js    # Configurações
│   └── config-service.test.js
│
└── storage/
    ├── storage-service.js   # LocalStorage / SessionStorage
    └── storage-service.test.js
```

---

# 9. Router (`router/`)

Roteamento SPA.

```
router/
├── router.js                # Classe Router
├── route.js                 # Definição de rota
├── link.js                  # Componente de link
├── router.test.js
└── README.md
```

---

# 10. Plugins (`plugins/`)

Sistema de plugins.

```
plugins/
└── engine/
    ├── plugin-engine.js     # Plugin engine
    └── plugin-engine.test.js
```

---

# 11. Ícones (`icons/`)

Sistema de ícones.

```
icons/
├── engine/
│   ├── icon-engine.js       # Icon engine
│   └── icon-engine.test.js
│
├── svg/
│   ├── save.svg
│   ├── delete.svg
│   ├── edit.svg
│   ├── arrow-down.svg
│   ├── arrow-up.svg
│   ├── arrow-left.svg
│   ├── arrow-right.svg
│   ├── close.svg
│   ├── check.svg
│   ├── alert.svg
│   ├── info.svg
│   ├── search.svg
│   ├── menu.svg
│   ├── more.svg
│   ├── download.svg
│   ├── upload.svg
│   ├── print.svg
│   ├── file.svg
│   ├── folder.svg
│   ├── user.svg
│   ├── settings.svg
│   ├── logout.svg
│   ├── dashboard.svg
│   ├── nfe.svg               # Ícone específico de domínio
│   └── ...                    # ~50-100 ícones
│
└── README.md
```

---

# 12. Animações (`animations/`)

Sistema de animações.

```
animations/
└── engine/
    ├── motion-engine.js      # Motion engine (easing, duration, animations)
    └── motion-engine.test.js
```

---

# 13. Dashboard (`dashboard/`)

Módulo de dashboard.

```
dashboard/
├── widgets/
│   ├── widget-base.js       # Classe base de widget
│   ├── widget-chart.js      # Widget de gráfico
│   ├── widget-table.js      # Widget de tabela
│   ├── widget-metric.js     # Widget de métrica (KPI)
│   ├── widget-list.js       # Widget de lista
│   └── widget-base.test.js
│
├── layouts/
│   ├── dashboard-layout.js  # Layout de dashboard (grid)
│   └── dashboard-layout.css
│
└── README.md
```

---

# 14. DataGrid (`datagrid/`)

Módulo de DataGrid (componente mais complexo do sistema).

```
datagrid/
├── datagrid.js              # Classe principal UIDataGrid
├── datagrid.css
├── datagrid.test.js
│
├── columns/
│   ├── column-text.js       # Coluna de texto
│   ├── column-number.js     # Coluna numérica
│   ├── column-date.js       # Coluna de data
│   ├── column-currency.js   # Coluna de moeda
│   ├── column-boolean.js    # Coluna booleana
│   ├── column-action.js     # Coluna de ações (botões)
│   └── column-select.js     # Coluna de seleção (checkbox)
│
├── editors/
│   ├── editor-text.js       # Editor de texto in-cell
│   ├── editor-select.js     # Editor de select in-cell
│   └── editor-date.js       # Editor de data in-cell
│
├── filters/
│   ├── filter-text.js       # Filtro de texto
│   ├── filter-select.js     # Filtro de seleção
│   ├── filter-date.js       # Filtro de data
│   └── filter-number.js     # Filtro numérico
│
├── renderers/
│   ├── renderer-status.js   # Renderizador de status (cores)
│   ├── renderer-progress.js # Renderizador de barra de progresso
│   └── renderer-actions.js  # Renderizador de ações
│
├── sorters/
│   ├── sorter-text.js       # Ordenação de texto
│   ├── sorter-number.js     # Ordenação numérica
│   └── sorter-date.js       # Ordenação por data
│
├── plugins/
│   ├── plugin-pagination.js # Paginação
│   ├── plugin-grouping.js   # Agrupamento
│   ├── plugin-export.js     # Exportação (CSV, Excel)
│   └── plugin-print.js      # Impressão
│
└── README.md
```

---

# 15. Formulários (`forms/`)

Módulo de formulários.

```
forms/
├── form.js                  # Form base
├── form.css
├── form.test.js
│
├── inputs/
│   ├── input-text.js        # Input de texto
│   ├── input-number.js      # Input numérico
│   ├── input-phone.js       # Input de telefone (máscara)
│   ├── input-cpf.js         # Input de CPF (máscara)
│   ├── input-cnpj.js        # Input de CNPJ (máscara)
│   ├── input-cep.js         # Input de CEP (máscara)
│   ├── input-date.js        # Input de data
│   ├── input-currency.js    # Input de moeda (máscara)
│   ├── input-password.js    # Input de senha
│   ├── input-search.js      # Input de busca
│   └── input-file.js        # Input de arquivo
│
├── selects/
│   ├── select.js            # Select simples
│   ├── select-search.js     # Select com busca
│   └── select-multiple.js   # Select múltiplo
│
├── checkboxes/
│   ├── checkbox.js          # Checkbox
│   ├── radio.js             # Radio button
│   └── toggle.js            # Toggle switch
│
├── validators/
│   ├── validator-required.js
│   ├── validator-email.js
│   ├── validator-cpf.js
│   ├── validator-cnpj.js
│   ├── validator-phone.js
│   ├── validator-cep.js
│   ├── validator-min.js
│   ├── validator-max.js
│   ├── validator-minlength.js
│   ├── validator-maxlength.js
│   └── validator-pattern.js
│
├── layout/
│   ├── form-group.js        # Grupo de campo (label + input + erro)
│   ├── form-row.js          # Linha de formulário
│   └── form-section.js      # Seção de formulário
│
└── README.md
```

---

# 16. Utilitários (`utils/`)

Funções utilitárias puras (sem estado, sem DOM).

```
utils/
├── dom/
│   ├── dom.js               # createElement, removeElement, etc.
│   └── dom.test.js
│
├── format/
│   ├── format.js            # Formatação geral
│   ├── format-currency.js   # Formatação de moeda
│   ├── format-date.js       # Formatação de data
│   ├── format-cpf.js        # Formatação de CPF
│   ├── format-cnpj.js       # Formatação de CNPJ
│   ├── format-phone.js      # Formatação de telefone
│   └── format-cep.js        # Formatação de CEP
│
├── mask/
│   ├── mask-cpf.js          # Máscara de CPF
│   ├── mask-cnpj.js         # Máscara de CNPJ
│   ├── mask-phone.js        # Máscara de telefone
│   ├── mask-cep.js          # Máscara de CEP
│   ├── mask-currency.js     # Máscara de moeda
│   └── mask-date.js         # Máscara de data
│
├── validation/
│   ├── validation.js        # Validação genérica
│   ├── validate-cpf.js      # Validação de CPF
│   ├── validate-cnpj.js     # Validação de CNPJ
│   ├── validate-email.js    # Validação de email
│   ├── validate-phone.js    # Validação de telefone
│   └── validate-cep.js      # Validação de CEP
│
├── math.js                  # Operações matemáticas
├── string.js                # Manipulação de strings
├── array.js                 # Manipulação de arrays
├── object.js                # Manipulação de objetos
├── date.js                  # Manipulação de datas
├── debounce.js              # Debounce e throttle
├── color.js                 # Manipulação de cores (hex, rgb, hsl)
└── README.md
```

---

# 17. Vendor (`vendor/`)

Dependências externas que não podem ser evitadas. Mínimo possível.

```
vendor/
├── normalize.css            # CSS reset (única dependência externa)
└── .gitkeep
```

---

# 18. Build (`build/`)

Scripts e configurações de build.

```
build/
├── scripts/
│   ├── build-css.js         # Build de CSS via PostCSS
│   ├── build-js.js          # Build de JS via esbuild
│   ├── build-icons.js       # Geração de sprite SVG
│   ├── dev-server.js        # Servidor de desenvolvimento
│   └── release.js           # Script de release (versionamento)
│
├── postcss/
│   └── postcss.config.js    # Configuração do PostCSS
│
├── esbuild/
│   └── esbuild.config.js    # Configuração do esbuild
│
├── karma/
│   └── karma.conf.js        # Configuração do Karma
│
└── eslint/
    └── .eslintrc.js          # Configuração do ESLint
```

---

# 19. Documentação (`docs/`)

Documentação do projeto.

```
docs/
├── sprints/                 # RFCs e especificações
│   ├── FISCALUI.md          # Arquitetura conceitual (21 capítulos)
│   └── componentes/         # Especificações funcionais
│       ├── 01-fundacao/     # Nível 1 (018 documentos)
│       ├── 02-fundamentais/ # Nível 2 (planejado)
│       ├── 03-navegacao/    # Nível 3 (planejado)
│       ├── 04-formularios/  # Nível 4 (planejado)
│       └── 05-corporativos/ # Nível 5 (planejado)
│
├── api/                     # Documentação da API pública
├── guides/                  # Guias de uso
└── examples/                # Exemplos de código
```

---

# 20. Convenções de Arquivos

## 20.1 Nomenclatura

```
Diretórios:  kebab-case (button, event-bus, http-service)
Arquivos JS: kebab-case (ui-component.js, state-manager.js)
Arquivos CSS: kebab-case (button.css, grid.css)
Arquivos SVG: kebab-case (arrow-down.svg)
Classes JS:  PascalCase (UIButton, StateManager, EventBus)
Constantes:  UPPER_SNAKE_CASE (BREAKPOINTS, COLORS)
```

## 20.2 Estrutura de Cada Componente

```
components/button/
├── button.js            # Implementação
├── button.css           # Estilos
├── button.test.js       # Testes
└── README.md            # Documentação do componente
```

## 20.3 Entry Points

Cada módulo pode expor:

```js
// ES Module (padrão)
import { UIButton } from 'fiscalui/components/button/button.js';

// CSS
import 'fiscalui/components/button/button.css';
```

---

# 21. Empacotamento

## 21.1 Formatos

```
FiscalUI será distribuído em 3 formatos:

1. ESM (ES Module)   → dist/esm/fiscalui.js     (padrão moderno)
2. CJS (CommonJS)    → dist/cjs/fiscalui.js     (Node.js/legado)
3. IIFE (Browser)    → dist/iife/fiscalui.min.js (script tag)
```

## 21.2 Bundle por Módulo

```
Além do bundle completo, cada módulo pode ser importado individualmente:

fiscalui/core/event-bus.js
fiscalui/core/state-manager.js
fiscalui/core/router.js
fiscalui/components/button.js
fiscalui/components/modal.js
fiscalui/forms/inputs/input-text.js
fiscalui/forms/validators/validator-cpf.js
```

---

# 22. Distribuição

## 22.1 npm Package

```json
{
    "name": "fiscalui",
    "version": "1.0.0",
    "description": "FiscalUI — Framework de componentes para sistemas fiscais",
    "type": "module",
    "main": "dist/cjs/fiscalui.js",
    "module": "dist/esm/fiscalui.js",
    "unpkg": "dist/iife/fiscalui.min.js",
    "style": "dist/css/fiscalui.min.css",
    "files": [
        "dist/",
        "core/",
        "components/",
        "LICENSE",
        "README.md"
    ],
    "exports": {
        ".": {
            "import": "./dist/esm/fiscalui.js",
            "require": "./dist/cjs/fiscalui.js"
        },
        "./core/event-bus": "./core/event-bus/event-bus.js",
        "./core/state-manager": "./core/state/state-manager.js",
        "./core/router": "./core/router/router.js",
        "./components/button": "./components/button/button.js",
        "./components/modal": "./components/modal/modal.js",
        "./components/toast": "./components/toast/toast.js",
        "./components/datagrid": "./components/datagrid/datagrid.js",
        "./forms/input-text": "./forms/inputs/input-text.js",
        "./forms/validator-cpf": "./forms/validators/validator-cpf.js",
        "./styles": "./dist/css/fiscalui.min.css"
    },
    "keywords": [
        "ui",
        "components",
        "fiscal",
        "nfe",
        "erp",
        "vanilla-js"
    ],
    "license": "MIT"
}
```

## 22.2 Estrutura de Distribuição

```
dist/
├── esm/
│   └── fiscalui.js              # ES Module (moderno)
├── cjs/
│   └── fiscalui.js              # CommonJS (Node)
├── iife/
│   ├── fiscalui.js              # IIFE (dev, sem minify)
│   └── fiscalui.min.js          # IIFE (produção, minified)
├── css/
│   ├── fiscalui.css             # CSS completo (dev)
│   ├── fiscalui.min.css         # CSS completo (produção)
│   └── themes/
│       ├── light.css
│       ├── dark.css
│       ├── high-contrast.css
│       └── corporate.css
├── icons/
│   └── sprite.svg               # Sprte único de ícones
└── fiscalui.d.ts                # TypeScript definitions (opcional)
```

---

# 23. package.json

```json
{
    "name": "fiscalui",
    "version": "1.0.0",
    "description": "FiscalUI — Framework de componentes para sistemas fiscais",
    "type": "module",
    "scripts": {
        "dev": "node build/scripts/dev-server.js",
        "build": "npm run build:css && npm run build:js && npm run build:icons",
        "build:css": "node build/scripts/build-css.js",
        "build:js": "node build/scripts/build-js.js",
        "build:icons": "node build/scripts/build-icons.js",
        "test": "vitest run",
        "test:watch": "vitest",
        "test:coverage": "vitest run --coverage",
        "lint": "eslint core/ components/ services/ forms/ utils/",
        "lint:css": "stylelint '**/*.css'",
        "format": "prettier --write '**/*.{js,css,md}'"
    },
    "devDependencies": {
        "postcss": "^8.4.0",
        "autoprefixer": "^10.4.0",
        "cssnano": "^6.0.0",
        "esbuild": "^0.19.0",
        "vitest": "^1.0.0",
        "eslint": "^8.0.0",
        "stylelint": "^15.0.0",
        "prettier": "^3.0.0",
        "svg-sprite": "^3.0.0",
        "chokidar": "^3.0.0"
    },
    "dependencies": {},
    "files": [
        "dist/",
        "core/",
        "components/",
        "services/",
        "forms/",
        "utils/",
        "icons/svg/",
        "LICENSE",
        "README.md"
    ],
    "exports": {
        ".": {
            "import": "./dist/esm/fiscalui.js",
            "require": "./dist/cjs/fiscalui.js"
        },
        "./core/*": "./core/*/*.js",
        "./components/*": "./components/*/*.js",
        "./services/*": "./services/*/*.js",
        "./forms/*": "./forms/**/*.js",
        "./utils/format": "./utils/format/format.js",
        "./utils/validation": "./utils/validation/validation.js",
        "./styles": "./dist/css/fiscalui.css"
    },
    "license": "MIT"
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial — Arquitetura Física completa |
