# FiscalUI Framework

## Documento 005 — Layout Core

**Versão 1.0**

Este documento define a arquitetura de layout do FiscalUI. Como Workspace, Sidebar, Header, Content, Footer e Panels se organizam, se comunicam e respondem a diferentes dispositivos.

---

# Índice

1. Introdução
2. Filosofia de Layout
3. Arquitetura Geral
4. Viewport
5. Workspace
6. Sidebar
7. Topbar
8. Header
9. Content
10. Footer
11. Status Bar
12. Panels
13. Drawer
14. Modal
15. Overlay
16. Launchpad
17. Grid
18. Container
19. Breakpoints
20. Responsividade
21. Sidebar Responsiva
22. Workspace Responsivo
23. Painéis Responsivos
24. Fullscreen
25. Split Panels
26. Accordion Layout
27. Tabs Layout
28. Wizard Layout
29. Steps Layout
30. Master-Detail
31. Form Layout
32. Dashboard Layout
33. DataGrid Layout
34. Empty State
35. Loading State
36. Error State
37. Layers
38. Performance
39. Boas Práticas

---

# 1. Introdução

## 1.1 Propósito

O Layout Core define como os elementos da interface se organizam no espaço disponível. Diferente de componentes individuais (Button, Card, Modal), o Layout Core trata da composição — como Sidebar, Topbar, Workspace, Painéis e Footer se relacionam para formar a tela do sistema.

## 1.2 Abordagem

```
Layout Core
    │
    ├── Estrutura Macro → Workspace, Sidebar, Topbar, Footer
    ├── Estrutura Micro → Painéis, Drawers, Modais
    ├── Estrutura de Dados → Grid, Containers, Seções
    └── Estrutura Adaptativa → Breakpoints, Responsividade
```

## 1.3 Princípio Fundamental

**O Layout pertence ao Framework, não à página.**

Nenhuma página ou módulo define seu próprio layout. Toda tela do sistema segue a mesma estrutura. O que muda é o conteúdo inserido nas regiões de layout.

---

# 2. Filosofia de Layout

## 2.1 Hierarquia

```
App (aplicação)
    │
    ├── Sidebar (navegação)
    ├── Main Area
    │   ├── Topbar (contexto global)
    │   └── Workspace (conteúdo)
    │       ├── Header (título + breadcrumb)
    │       ├── Toolbar (ações)
    │       ├── Filters (filtros)
    │       ├── Content (tabela/form/dashboard)
    │       └── Status Bar (informação)
    └── Footer (opcional)
```

## 2.2 Regras de Layout

1. **Sidebar é fixa** — 260px (expandida) ou 64px (colapsada)
2. **Topbar é fixa** — 56px, sempre visível
3. **Workspace é flexível** — ocupa todo o espaço restante
4. **Content é scrollável** — apenas o conteúdo rola, sidebar e topbar ficam fixas
5. **Status Bar é fixa** — 32px, sempre visível
6. **Nunca** sidebar e workspace scrollam juntos
7. **Nunca** conteúdo ultrapassa os limites do workspace

## 2.3 Mobile First

Todo layout é projetado primeiro para mobile (XS). Conforme a tela aumenta, mais elementos se tornam visíveis.

```
XS (0-575px)         → Sidebar oculta (drawer), workspace full
SM (576-767px)       → Sidebar oculta (drawer), workspace full
MD (768-1023px)      → Sidebar hover-expand, workspace reduzido
LG (1024-1439px)     → Sidebar fixa, workspace fluido
XL (1440-1919px)     → Sidebar fixa, workspace máximo 1600px
XXL (1920px+)        → Sidebar fixa, workspace centralizado
```

---

# 3. Arquitetura Geral

## 3.1 Estrutura DOM

```html
<div id="app">
    <!-- Sidebar (navegação principal) -->
    <aside id="sidebar" class="sidebar">
        <div class="sidebar__header">
            <!-- Logo + empresa -->
        </div>
        <nav class="sidebar__nav">
            <!-- Menu de navegação -->
        </nav>
        <div class="sidebar__footer">
            <!-- Informações do usuário -->
        </div>
    </aside>

    <!-- Área principal -->
    <div id="main-area" class="main-area">
        <!-- Topbar (contexto global) -->
        <header id="topbar" class="topbar">
            <div class="topbar__left">
                <!-- Menu toggle, breadcrumb -->
            </div>
            <div class="topbar__center">
                <!-- Título do módulo -->
            </div>
            <div class="topbar__right">
                <!-- Notificações, tema, usuário -->
            </div>
        </header>

        <!-- Workspace (conteúdo do módulo) -->
        <main id="workspace" class="workspace">
            <!-- Header -->
            <div class="workspace__header">
                <h1 class="workspace__title">Título</h1>
                <nav class="workspace__breadcrumb">
                    <a href="/">Home</a> / <span>Módulo</span>
                </nav>
            </div>

            <!-- Toolbar -->
            <div class="workspace__toolbar">
                <button class="ui-btn ui-btn--primary">Novo</button>
                <button class="ui-btn ui-btn--outline">Pesquisar</button>
            </div>

            <!-- Filters -->
            <div class="workspace__filters" hidden>
                <!-- Filtros colapsáveis -->
            </div>

            <!-- Content -->
            <div class="workspace__content">
                <!-- Tabela, formulário, dashboard -->
            </div>

            <!-- Status Bar -->
            <div class="workspace__status-bar">
                <span>Usuário: Admin</span>
                <span>v1.0.0</span>
                <span>Produção</span>
            </div>
        </main>
    </div>
</div>
```

## 3.2 CSS Estrutural

```css
/* App container */
#app {
    display: flex;
    width: 100%;
    height: 100vh;
    overflow: hidden;
    background: var(--surface-page);
}

/* Sidebar */
#sidebar {
    width: var(--sidebar-width, 260px);
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    background: var(--surface-sidebar);
    border-right: var(--border-thin) solid var(--color-border);
    transition: width var(--transition-smooth);
    z-index: var(--z-fixed);
    overflow: hidden;
}

#sidebar.collapsed {
    width: var(--sidebar-collapsed, 64px);
}

/* Main Area */
.main-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-width: 0; /* necessário para flex não estourar */
    overflow: hidden;
}

/* Topbar */
#topbar {
    height: 56px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    padding: 0 var(--spacing-5);
    background: var(--surface-card);
    border-bottom: var(--border-thin) solid var(--color-border);
    z-index: var(--z-sticky);
}

/* Workspace */
#workspace {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    padding: var(--spacing-5);
    gap: var(--spacing-4);
}

/* Content (scrollável) */
.workspace__content {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    min-height: 0;
}

/* Status Bar */
.workspace__status-bar {
    height: 32px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    padding: 0 var(--spacing-4);
    background: var(--surface-card);
    border-top: var(--border-thin) solid var(--color-border);
    font-size: var(--font-size-xs);
    color: var(--text-tertiary);
}
```

---

# 4. Viewport

## 4.1 Definição

O Viewport é a área total disponível no navegador para renderização do FiscalUI. Todo o layout do sistema opera dentro deste espaço.

```css
html, body {
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
    overflow: hidden;
}

#app {
    width: 100%;
    height: 100vh;
    overflow: hidden;
}
```

## 4.2 Como o Viewport é Ocupado

```
┌──────────────────────────────────────────────────────────┐
│ Topbar (56px fixo)                                       │
├────────────┬─────────────────────────────────────────────┤
│            │  Header (variável)                          │
│  Sidebar   ├─────────────────────────────────────────────┤
│  260px     │  Toolbar (variável)                         │
│  (fixa)    ├─────────────────────────────────────────────┤
│            │  Filters (opcional, colapsável)             │
│            ├─────────────────────────────────────────────┤
│            │  Content (flexível, scrollável)             │
│            │                                             │
│            │                                             │
│            ├─────────────────────────────────────────────┤
│            │  Status Bar (32px fixo)                     │
└────────────┴─────────────────────────────────────────────┘
```

## 4.3 Regras do Viewport

1. Viewport total = 100vh
2. Sidebar ocupa altura total (100vh)
3. Topbar ocupa 56px do topo
4. Status Bar ocupa 32px da base
5. Content ocupa TODO o espaço restante
6. Nada ultrapassa os limites do viewport
7. Scroll acontece APENAS no Content

---

# 5. Workspace

## 5.1 Definição

O Workspace é a região principal do sistema, onde o conteúdo de cada módulo é exibido. Todo módulo (NF-e, Produtos, Clientes, Dashboard, etc.) segue a mesma estrutura de Workspace.

## 5.2 Estrutura do Workspace

```
┌──────────────────────────────────────────────────────────┐
│ Header                                                    │
│ Título do Módulo │ Breadcrumb > Subseção                 │
├──────────────────────────────────────────────────────────┤
│ Toolbar                                                   │
│ [+ Novo] [Importar] [Exportar] [🔍 Pesquisar]            │
├──────────────────────────────────────────────────────────┤
│ Filters (colapsável)                                      │
│ [Pesquisar...]  [Status: ▼]  [Data: ▼]  [Filtrar]       │
├──────────────────────────────────────────────────────────┤
│ Content                                                   │
│ ┌──────────────────────────────────────────────────────┐ │
│ │ Tabela / Formulário / Dashboard / Gráfico / etc.     │ │
│ │                                                      │ │
│ │                              (scrollável)            │ │
│ └──────────────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────────────┤
│ Status Bar                                               │
│ Usuário: Admin │ Empresa: ABC │ v1.0.0 │ Produção │ 14:32│
└──────────────────────────────────────────────────────────┘
```

## 5.3 Regiões do Workspace

| Região | Altura | Comportamento | Sempre Visível? |
|--------|--------|---------------|-----------------|
| Header | Automática (conteúdo) | Fixa no topo do workspace | Sim |
| Toolbar | Automática (conteúdo) | Fixa abaixo do header | Sim |
| Filters | Automática (conteúdo) | Colapsável, toggle visibilidade | Não |
| Content | Flexível (restante) | Scrollável verticalmente | Sim |
| Status Bar | 32px | Fixa na base do workspace | Sim |

## 5.4 CSS do Workspace

```css
#workspace {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    padding: var(--spacing-5);
    gap: var(--spacing-4);
}

/* Header */
.workspace__header {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.workspace__title {
    font-size: var(--font-size-xxl);
    font-weight: var(--font-weight-semibold);
    color: var(--text-primary);
}

.workspace__breadcrumb {
    font-size: var(--font-size-sm);
    color: var(--text-tertiary);
}

.workspace__breadcrumb a {
    color: var(--text-link);
    text-decoration: none;
}

.workspace__breadcrumb a:hover {
    text-decoration: underline;
}

/* Toolbar */
.workspace__toolbar {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    gap: var(--spacing-3);
    padding: var(--spacing-3) 0;
    border-bottom: var(--border-thin) solid var(--color-border);
}

/* Filters */
.workspace__filters {
    flex-shrink: 0;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: var(--spacing-3);
    padding: var(--spacing-3);
    background: var(--surface-card);
    border: var(--border-thin) solid var(--color-border);
    border-radius: var(--radius-md);
}

.workspace__filters[hidden] {
    display: none;
}

/* Content */
.workspace__content {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    min-height: 0;
    padding: var(--spacing-4) 0;
}

/* Status Bar */
.workspace__status-bar {
    flex-shrink: 0;
    height: 32px;
    display: flex;
    align-items: center;
    gap: var(--spacing-5);
    padding: 0 var(--spacing-4);
    background: var(--surface-card);
    border-top: var(--border-thin) solid var(--color-border);
    font-size: var(--font-size-xs);
    color: var(--text-tertiary);
}
```

## 5.5 Estados do Workspace

### 5.5.1 Launchpad (Home)

Quando nenhum módulo está selecionado, o Workspace exibe o Launchpad:

```css
#workspace.launchpad-mode .workspace__header,
#workspace.launchpad-mode .workspace__toolbar,
#workspace.launchpad-mode .workspace__status-bar {
    display: none;
}

#workspace.launchpad-mode .workspace__content {
    padding: 0;
}
```

### 5.5.2 Module Mode

Quando um módulo está ativo, o Workspace exibe a estrutura completa.

### 5.5.3 Form Mode

Quando um formulário está aberto, o conteúdo pode ocupar mais espaço vertical.

### 5.5.4 Fullscreen Mode

```css
#workspace.fullscreen-mode {
    padding: 0;
}

#workspace.fullscreen-mode .workspace__header,
#workspace.fullscreen-mode .workspace__toolbar,
#workspace.fullscreen-mode .workspace__filters,
#workspace.fullscreen-mode .workspace__status-bar {
    display: none;
}

#workspace.fullscreen-mode .workspace__content {
    padding: 0;
}
```

---

# 6. Sidebar

## 6.1 Definição

A Sidebar é o painel de navegação principal do sistema. Ela contém o menu de módulos, o logo da empresa e as informações do usuário logado.

## 6.2 Estados da Sidebar

### 6.2.1 Expandida (Desktop)

```
┌──────────────────┐
│ FiscalUI    [≡]  │  ← Logo + toggle
├──────────────────┤
│ ◨ Dashboard      │
│ 📄 NF-e          │
│ 📄 NFC-e         │
│ 📦 Produtos      │
│ 👥 Clientes      │
│ 📊 Relatórios    │
│ 🏢 Empresas      │
│ ⚙ Configuração   │
├──────────────────┤
│ 👤 Admin         │  ← Usuário
│ 🚪 Sair          │
└──────────────────┘
```

**Largura:** 260px

### 6.2.2 Colapsada (Desktop)

```
┌──────┐
│ ≡    │
├──────┤
│ ◨    │
│ 📄   │
│ 📄   │
│ 📦   │
│ 👥   │
│ 📊   │
│ 🏢   │
│ ⚙    │
├──────┤
│ 👤   │
│ 🚪   │
└──────┘
```

**Largura:** 64px (apenas ícones)

### 6.2.3 Drawer (Mobile)

```
┌──────────────────────────────────┐
│ (Overlay escuro 50%)             │
│ ┌──────────────────┐             │
│ │ FiscalUI    [≡]  │             │
│ ├──────────────────┤             │
│ │ ◨ Dashboard      │             │
│ │ 📄 NF-e          │             │
│ │ 📄 NFC-e         │             │
│ │ 📦 Produtos      │             │
│ │ 👥 Clientes      │             │
│ │ 📊 Relatórios    │             │
│ │ 🏢 Empresas      │             │
│ │ ⚙ Configuração   │             │
│ ├──────────────────┤             │
│ │ 👤 Admin         │             │
│ │ 🚪 Sair          │             │
│ └──────────────────┘             │
└──────────────────────────────────┘
```

## 6.3 CSS da Sidebar

```css
/* Sidebar Container */
#sidebar {
    width: var(--sidebar-width, 260px);
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    background: var(--surface-sidebar);
    border-right: var(--border-thin) solid var(--color-border);
    transition: width var(--transition-smooth);
    z-index: var(--z-fixed);
    overflow: hidden;
}

/* Header (logo + empresa) */
.sidebar__header {
    height: 56px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    padding: 0 var(--spacing-4);
    border-bottom: var(--border-thin) solid var(--color-border);
}

.sidebar__logo {
    width: 32px;
    height: 32px;
    flex-shrink: 0;
}

.sidebar__title {
    font-size: var(--font-size-lg);
    font-weight: var(--font-weight-semibold);
    color: var(--text-primary);
    margin-left: var(--spacing-3);
    white-space: nowrap;
    overflow: hidden;
}

/* Navigation */
.sidebar__nav {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    padding: var(--spacing-3) 0;
}

.sidebar__menu-item {
    display: flex;
    align-items: center;
    height: 44px;
    padding: 0 var(--spacing-4);
    color: var(--text-secondary);
    cursor: pointer;
    transition: background var(--transition-fast),
                color var(--transition-fast);
    white-space: nowrap;
    text-decoration: none;
}

.sidebar__menu-item:hover {
    background: var(--surface-hover);
    color: var(--text-primary);
}

.sidebar__menu-item.active {
    background: var(--surface-selected);
    color: var(--color-primary);
}

.sidebar__menu-icon {
    width: 24px;
    height: 24px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
}

.sidebar__menu-label {
    margin-left: var(--spacing-3);
    font-size: var(--font-size-sm);
    opacity: 1;
    transition: opacity var(--transition-fast);
}

/* Footer (usuário) */
.sidebar__footer {
    flex-shrink: 0;
    padding: var(--spacing-3) var(--spacing-4);
    border-top: var(--border-thin) solid var(--color-border);
}

.sidebar__user {
    display: flex;
    align-items: center;
    gap: var(--spacing-3);
}

.sidebar__user-avatar {
    width: 32px;
    height: 32px;
    border-radius: var(--radius-rounded);
    background: var(--color-primary);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-inverse);
    font-weight: var(--font-weight-semibold);
    font-size: var(--font-size-sm);
    flex-shrink: 0;
}

.sidebar__user-info {
    overflow: hidden;
}

.sidebar__user-name {
    font-size: var(--font-size-sm);
    font-weight: var(--font-weight-medium);
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.sidebar__user-role {
    font-size: var(--font-size-xxs);
    color: var(--text-tertiary);
}

/* Collapsed State */
#sidebar.collapsed {
    width: var(--sidebar-collapsed, 64px);
}

#sidebar.collapsed .sidebar__title,
#sidebar.collapsed .sidebar__menu-label,
#sidebar.collapsed .sidebar__user-info {
    opacity: 0;
    width: 0;
    margin: 0;
}

#sidebar.collapsed .sidebar__menu-item {
    justify-content: center;
    padding: 0;
}

#sidebar.collapsed .sidebar__user {
    justify-content: center;
}

/* Mobile Drawer */
@media (max-width: 767px) {
    #sidebar {
        position: fixed;
        top: 0;
        left: 0;
        height: 100vh;
        z-index: var(--z-modal);
        transform: translateX(-100%);
        transition: transform var(--transition-smooth);
    }

    #sidebar.mobile-open {
        transform: translateX(0);
    }

    .sidebar-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        z-index: calc(var(--z-modal) - 1);
        opacity: 0;
        pointer-events: none;
        transition: opacity var(--transition-smooth);
    }

    .sidebar-overlay.active {
        opacity: 1;
        pointer-events: auto;
    }
}

/* Hover Expand (Tablet) */
@media (min-width: 768px) and (max-width: 1023px) {
    #sidebar {
        width: var(--sidebar-collapsed, 64px);
    }

    #sidebar:hover {
        width: var(--sidebar-width, 260px);
    }

    #sidebar:hover .sidebar__title,
    #sidebar:hover .sidebar__menu-label,
    #sidebar:hover .sidebar__user-info {
        opacity: 1;
        width: auto;
    }
}
```

---

# 7. Topbar

## 7.1 Definição

A Topbar é a barra superior fixa do sistema. Ela contém elementos de contexto global que permanecem visíveis independentemente do módulo ativo.

## 7.2 Estrutura

```
┌──────────────────────────────────────────────────────────┐
│ [≡]  [◁]  Dashboard  │  📄 NF-e  📦 Produtos  👥 Cli…  │
│ Toggle  Voltar         Tab Navigation                    │
│                                                          │
│           🔍                          🔔  🌙  👤         │
│        Pesquisa                    Notif  Tema  Perfil   │
└──────────────────────────────────────────────────────────┘
```

## 7.3 Regiões da Topbar

| Região | Alinhamento | Conteúdo |
|--------|-------------|----------|
| Esquerda | `flex-start` | Toggle sidebar, botão voltar, breadcrumb |
| Centro | `center` | Tabs de navegação entre módulos |
| Direita | `flex-end` | Pesquisa, notificações, tema, usuário |

## 7.4 CSS da Topbar

```css
#topbar {
    height: 56px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 var(--spacing-5);
    background: var(--surface-card);
    border-bottom: var(--border-thin) solid var(--color-border);
    z-index: var(--z-sticky);
    gap: var(--spacing-4);
}

.topbar__left {
    display: flex;
    align-items: center;
    gap: var(--spacing-3);
    flex: 0 1 auto;
}

.topbar__center {
    display: flex;
    align-items: center;
    gap: var(--spacing-1);
    flex: 1;
    justify-content: center;
}

.topbar__right {
    display: flex;
    align-items: center;
    gap: var(--spacing-2);
    flex: 0 1 auto;
}

/* Menu Toggle */
.topbar__toggle {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--radius-md);
    cursor: pointer;
    color: var(--text-secondary);
    transition: background var(--transition-fast);
}

.topbar__toggle:hover {
    background: var(--surface-hover);
    color: var(--text-primary);
}

/* Nav Tabs */
.topbar__tabs {
    display: flex;
    align-items: center;
    gap: var(--spacing-1);
}

.topbar__tab {
    padding: var(--spacing-2) var(--spacing-4);
    border-radius: var(--radius-md);
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
    cursor: pointer;
    transition: background var(--transition-fast),
                color var(--transition-fast);
    white-space: nowrap;
}

.topbar__tab:hover {
    background: var(--surface-hover);
    color: var(--text-primary);
}

.topbar__tab.active {
    background: var(--surface-selected);
    color: var(--color-primary);
}

/* Search */
.topbar__search {
    position: relative;
    width: 240px;
}

.topbar__search-input {
    width: 100%;
    height: 36px;
    padding: 0 var(--spacing-4) 0 var(--spacing-9);
    background: var(--surface-input);
    border: var(--border-thin) solid var(--color-border);
    border-radius: var(--radius-md);
    font-size: var(--font-size-sm);
    color: var(--text-primary);
}

.topbar__search-icon {
    position: absolute;
    left: var(--spacing-3);
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-tertiary);
}

/* Icons */
.topbar__icon-btn {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--radius-md);
    cursor: pointer;
    color: var(--text-secondary);
    position: relative;
    transition: background var(--transition-fast);
}

.topbar__icon-btn:hover {
    background: var(--surface-hover);
    color: var(--text-primary);
}

.topbar__badge {
    position: absolute;
    top: 4px;
    right: 4px;
    width: 16px;
    height: 16px;
    background: var(--color-danger);
    color: white;
    font-size: 10px;
    font-weight: bold;
    border-radius: var(--radius-rounded);
    display: flex;
    align-items: center;
    justify-content: center;
}

@media (max-width: 767px) {
    .topbar__center {
        display: none;
    }

    .topbar__search {
        width: 160px;
    }

    .topbar__search-input {
        width: 160px;
    }
}
```

---

# 8. Header

## 8.1 Definição

O Header do Workspace contém o título do módulo atual e o breadcrumb de navegação. Ele é a primeira seção visível do conteúdo.

## 8.2 Estrutura

```
┌──────────────────────────────────────────────────────────┐
│  Dashboard                                               │
│  Home > Dashboard                                        │
└──────────────────────────────────────────────────────────┘
```

## 8.3 Estados do Header

| Estado | Conteúdo |
|--------|----------|
| Padrão | Título + Breadcrumb |
| Apenas Título | Breadcrumb oculto (espaço reduzido) |
| Ações | Título + Breadcrumb + Ações à direita |
| Mobile | Título apenas (breadcrumb oculto) |

---

# 9. Content

## 9.1 Definição

Content é a região mais importante do Workspace. É onde o conteúdo do módulo é exibido: tabelas, formulários, dashboards, gráficos, etc.

## 9.2 Comportamento

- Content é a única região que scrolla verticalmente
- Content ocupa todo o espaço restante do Workspace
- Content nunca define padding — o componente interno define
- Content não tem background próprio — herda do Workspace

## 9.3 Tipos de Conteúdo

| Tipo | Comportamento de Scroll |
|------|------------------------|
| Tabela | Scroll horizontal + vertical |
| Formulário | Scroll vertical |
| Dashboard | Scroll vertical |
| Card Grid | Scroll vertical |
| Gráfico | Scroll vertical (se necessário) |

## 9.4 CSS do Content

```css
.workspace__content {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    min-height: 0; /* flexbox shrink trick */
    padding: var(--spacing-4) 0;
}

/* Scroll horizontal permitido para tabelas */
.workspace__content--table {
    overflow-x: auto;
}

/* Sem padding para fullscreen */
.workspace__content--flush {
    padding: 0;
}

/* Centralizado verticalmente (empty state) */
.workspace__content--centered {
    display: flex;
    align-items: center;
    justify-content: center;
}
```

---

# 10. Footer

## 10.1 Definição

O Footer é uma região opcional do Workspace. Ele pode conter ações secundárias, informações complementares ou paginação.

## 10.2 Quando Usar

- Paginação de DataGrid
- Ações de formulário (Salvar, Cancelar)
- Informações de resumo (Total de registros)

## 10.3 CSS do Footer

```css
.workspace__footer {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-3) var(--spacing-4);
    border-top: var(--border-thin) solid var(--color-border);
    background: var(--surface-card);
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
}
```

---

# 11. Status Bar

## 11.1 Definição

A Status Bar é a barra fixa na base do Workspace. Ela exibe informações do sistema sempre visíveis: usuário, empresa, versão, ambiente e relógio.

## 11.2 Estrutura

```
┌──────────────────────────────────────────────────────────┐
│ 👤 Admin    🏢 ABC Ltda    v1.0.0    🟢 Produção    ⏰ 14:32│
└──────────────────────────────────────────────────────────┘
```

## 11.3 CSS da Status Bar

```css
.workspace__status-bar {
    flex-shrink: 0;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 var(--spacing-4);
    background: var(--surface-card);
    border-top: var(--border-thin) solid var(--color-border);
    font-size: var(--font-size-xs);
    color: var(--text-tertiary);
}

.status-bar__left,
.status-bar__right {
    display: flex;
    align-items: center;
    gap: var(--spacing-4);
}

.status-bar__item {
    display: flex;
    align-items: center;
    gap: var(--spacing-2);
}

.status-bar__dot {
    width: 6px;
    height: 6px;
    border-radius: var(--radius-rounded);
}

.status-bar__dot--production { background: var(--color-success); }
.status-bar__dot--staging { background: var(--color-warning); }
.status-bar__dot--development { background: var(--color-info); }

/* Mobile */
@media (max-width: 767px) {
    .workspace__status-bar {
        font-size: var(--font-size-xxs);
        padding: 0 var(--spacing-3);
    }

    .status-bar__item--hide-mobile {
        display: none;
    }
}
```

---

# 12. Panels

## 12.1 Definição

Panels são regiões retangulares dentro do Content que organizam informações relacionadas. Eles podem ser fixos, redimensionáveis ou colapsáveis.

## 12.2 Tipos de Panel

### 12.2.1 Glass Panel (Padrão)

```html
<div class="glass-panel">
    <div class="glass-panel__header">
        <h3 class="glass-panel__title">Título</h3>
        <div class="glass-panel__actions">
            <button>...</button>
        </div>
    </div>
    <div class="glass-panel__body">
        <!-- Conteúdo -->
    </div>
    <div class="glass-panel__footer">
        <!-- Opcional -->
    </div>
</div>
```

```css
.glass-panel {
    background: var(--surface-glass);
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    border: var(--border-thin) solid var(--glass-border);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-glass);
}

.glass-panel__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-4) var(--spacing-5);
    border-bottom: var(--border-thin) solid var(--color-border);
}

.glass-panel__title {
    font-size: var(--font-size-base);
    font-weight: var(--font-weight-semibold);
    color: var(--text-primary);
}

.glass-panel__body {
    padding: var(--spacing-5);
}

.glass-panel__footer {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: var(--spacing-3);
    padding: var(--spacing-3) var(--spacing-5);
    border-top: var(--border-thin) solid var(--color-border);
}

/* States */
.glass-panel--collapsible .glass-panel__body[hidden] {
    display: none;
}

.glass-panel--highlighted {
    border-color: var(--color-primary);
    box-shadow: var(--shadow-glow);
}
```

### 12.2.2 Card Panel

```css
.card-panel {
    background: var(--surface-card);
    border: var(--border-thin) solid var(--color-border);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-card);
}

.card-panel__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-5);
    border-bottom: var(--border-thin) solid var(--color-border);
}

.card-panel__body {
    padding: var(--spacing-5);
}

.card-panel__footer {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: var(--spacing-3);
    padding: var(--spacing-4) var(--spacing-5);
    border-top: var(--border-thin) solid var(--color-border);
}
```

## 12.3 Painéis em Grid

```html
<div class="panel-grid">
    <div class="glass-panel">Painel 1</div>
    <div class="glass-panel">Painel 2</div>
    <div class="glass-panel">Painel 3</div>
    <div class="glass-panel">Painel 4</div>
</div>
```

```css
.panel-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: var(--spacing-5);
}

.panel-grid--2 {
    grid-template-columns: repeat(2, 1fr);
}

.panel-grid--3 {
    grid-template-columns: repeat(3, 1fr);
}

.panel-grid--4 {
    grid-template-columns: repeat(4, 1fr);
}

.panel-grid--sidebar {
    grid-template-columns: 320px 1fr;
}

@media (max-width: 767px) {
    .panel-grid,
    .panel-grid--2,
    .panel-grid--3,
    .panel-grid--4,
    .panel-grid--sidebar {
        grid-template-columns: 1fr;
    }
}
```

---

# 13. Drawer

## 13.1 Definição

Drawer é um painel deslizante que aparece a partir de uma das bordas da tela. Diferente de Modal, o Drawer não bloqueia completamente a interação com o conteúdo principal.

## 13.2 Posições

```
┌────────────────────────────────┐
│  ┌─────────┐                   │
│  │ Drawer  │   Content         │
│  │ Left    │                   │
│  │         │                   │
│  └─────────┘                   │
└────────────────────────────────┘

┌────────────────────────────────┐
│                   ┌─────────┐  │
│   Content         │ Drawer  │  │
│                   │ Right   │  │
│                   │         │  │
│                   └─────────┘  │
└────────────────────────────────┘

┌────────────────────────────────┐
│  ┌──────────────────────────┐  │
│  │      Drawer Bottom       │  │
│  └──────────────────────────┘  │
└────────────────────────────────┘
```

## 13.3 CSS do Drawer

```css
.drawer {
    position: fixed;
    background: var(--surface-card);
    box-shadow: var(--shadow-xl);
    z-index: var(--z-modal);
    transition: transform var(--transition-smooth);
}

.drawer--left {
    top: 0;
    left: 0;
    height: 100vh;
    width: 400px;
    transform: translateX(-100%);
}

.drawer--right {
    top: 0;
    right: 0;
    height: 100vh;
    width: 400px;
    transform: translateX(100%);
}

.drawer--bottom {
    bottom: 0;
    left: 0;
    width: 100%;
    max-height: 80vh;
    transform: translateY(100%);
    border-radius: var(--radius-xl) var(--radius-xl) 0 0;
}

.drawer.open {
    transform: translate(0);
}

.drawer__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-5);
    border-bottom: var(--border-thin) solid var(--color-border);
}

.drawer__title {
    font-size: var(--font-size-lg);
    font-weight: var(--font-weight-semibold);
}

.drawer__body {
    padding: var(--spacing-5);
    overflow-y: auto;
    height: calc(100% - 60px);
}

.drawer__close {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--radius-md);
    cursor: pointer;
    color: var(--text-secondary);
}

.drawer__close:hover {
    background: var(--surface-hover);
}
```

---

# 14. Modal

## 14.1 Definição

Modal é uma janela que bloqueia a interação com o restante da interface até ser fechada.

## 14.2 CSS do Modal

```css
.modal-backdrop {
    position: fixed;
    inset: 0;
    background: var(--modal-overlay-bg, rgba(0, 0, 0, 0.6));
    z-index: var(--z-modal-backdrop);
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    pointer-events: none;
    transition: opacity var(--transition-smooth);
}

.modal-backdrop.open {
    opacity: 1;
    pointer-events: auto;
}

.modal {
    background: var(--surface-modal);
    border-radius: var(--radius-xl);
    box-shadow: var(--shadow-modal);
    z-index: var(--z-modal);
    max-height: 90vh;
    display: flex;
    flex-direction: column;
    width: 560px; /* md */
}

.modal--sm { width: 400px; }
.modal--lg { width: 720px; }
.modal--xl { width: 960px; }
.modal--full { width: calc(100vw - 64px); height: calc(100vh - 64px); }

.modal__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-5) var(--spacing-7);
    border-bottom: var(--border-thin) solid var(--color-border);
}

.modal__title {
    font-size: var(--font-size-xl);
    font-weight: var(--font-weight-semibold);
}

.modal__body {
    padding: var(--spacing-7);
    overflow-y: auto;
    flex: 1;
}

.modal__footer {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: var(--spacing-3);
    padding: var(--spacing-4) var(--spacing-7);
    border-top: var(--border-thin) solid var(--color-border);
}

@media (max-width: 767px) {
    .modal {
        width: 100%;
        max-height: 100vh;
        border-radius: 0;
    }

    .modal--sm,
    .modal--lg,
    .modal--xl {
        width: 100%;
    }
}
```

---

# 15. Overlay

## 15.1 Definição

Overlay é uma camada semi-transparente que cobre toda a tela, geralmente usada para modais, drawers e context menus.

## 15.2 CSS do Overlay

```css
.overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: var(--z-modal-backdrop);
    opacity: 0;
    pointer-events: none;
    transition: opacity var(--transition-smooth);
}

.overlay.active {
    opacity: 1;
    pointer-events: auto;
}

.overlay--light {
    background: rgba(0, 0, 0, 0.3);
}

.overlay--heavy {
    background: rgba(0, 0, 0, 0.7);
}
```

---

# 16. Launchpad

## 16.1 Definição

O Launchpad é a tela inicial do sistema, exibida quando nenhum módulo está selecionado. Ele apresenta cards interativos para cada módulo disponível.

## 16.2 Estrutura

```
┌────────────────────────────────────────────────────────┐
│  👋 Bom dia, Admin!                                    │
│                                                         │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                   │
│  │  📄  │ │  📄  │ │  📦  │ │  👥  │                   │
│  │ NF-e │ │ NFC-e│ │ Prod │ │ Cli  │                   │
│  └──────┘ └──────┘ └──────┘ └──────┘                   │
│                                                         │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                   │
│  │  📊  │ │  🏢  │ │  ⚙   │ │  ◨   │                   │
│  │ Rel  │ │  Emp │ │ Config│ │ Dash │                   │
│  └──────┘ └──────┘ └──────┘ └──────┘                   │
└────────────────────────────────────────────────────────┘
```

## 16.3 CSS do Launchpad

```css
#launchpad {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-7);
    padding: var(--spacing-8);
    height: 100%;
}

.launchpad__welcome {
    font-size: var(--font-size-xxl);
    font-weight: var(--font-weight-semibold);
    color: var(--text-primary);
}

.launchpad__subtitle {
    font-size: var(--font-size-base);
    color: var(--text-secondary);
    margin-top: var(--spacing-2);
}

.launchpad__grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: var(--spacing-4);
}

.launchpad__card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-6);
    background: var(--surface-glass);
    backdrop-filter: var(--glass-blur);
    border: var(--border-thin) solid var(--glass-border);
    border-radius: var(--radius-lg);
    cursor: pointer;
    text-decoration: none;
    transition: transform var(--transition-normal),
                box-shadow var(--transition-normal);
    gap: var(--spacing-3);
    aspect-ratio: 1;
}

.launchpad__card:hover {
    transform: scale(1.05);
    box-shadow: var(--shadow-glow);
}

.launchpad__card-icon {
    font-size: 2rem;
    transition: transform var(--transition-fast);
}

.launchpad__card:hover .launchpad__card-icon {
    transform: scale(1.15) translateY(-2px);
}

.launchpad__card-label {
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
    text-align: center;
}

@media (max-width: 575px) {
    .launchpad__grid {
        grid-template-columns: repeat(2, 1fr);
        gap: var(--spacing-3);
    }

    .launchpad__card {
        padding: var(--spacing-4);
    }
}
```

---

# 17. Grid Layout

## 17.1 Container Grid

```css
.layout-grid {
    display: grid;
    gap: var(--spacing-5);
}

.layout-grid--1 { grid-template-columns: 1fr; }
.layout-grid--2 { grid-template-columns: repeat(2, 1fr); }
.layout-grid--3 { grid-template-columns: repeat(3, 1fr); }
.layout-grid--4 { grid-template-columns: repeat(4, 1fr); }

.layout-grid--sidebar {
    grid-template-columns: 260px 1fr;
}

.layout-grid--aside {
    grid-template-columns: 1fr 320px;
}

.layout-grid--header-content {
    grid-template-rows: auto 1fr;
}

.layout-grid--auto {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
}

@media (max-width: 767px) {
    .layout-grid--2,
    .layout-grid--3,
    .layout-grid--4,
    .layout-grid--sidebar,
    .layout-grid--aside {
        grid-template-columns: 1fr;
    }
}
```

## 17.2 Flex Grid

```css
.flex-layout {
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-5);
}

.flex-layout__item {
    flex: 1 1 280px;
    min-width: 0;
}

.flex-layout__item--fixed {
    flex: 0 0 320px;
}

.flex-layout__item--grow {
    flex: 999 1 0;
}
```

---

# 18. Form Layout

## 18.1 Estrutura de Formulário

```html
<div class="form-layout">
    <div class="form-section">
        <h2 class="form-section__title">Dados Gerais</h2>
        <div class="form-row">
            <div class="form-field">
                <label>Nome</label>
                <input>
            </div>
            <div class="form-field">
                <label>CPF/CNPJ</label>
                <input data-mask="cpf">
            </div>
        </div>
        <div class="form-row">
            <div class="form-field form-field--full">
                <label>Endereço</label>
                <input>
            </div>
        </div>
    </div>
</div>
```

## 18.2 CSS de Form Layout

```css
.form-layout {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-7);
    max-width: 960px;
}

.form-section {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-4);
}

.form-section__title {
    font-size: var(--font-size-lg);
    font-weight: var(--font-weight-semibold);
    color: var(--text-primary);
    padding-bottom: var(--spacing-3);
    border-bottom: var(--border-thin) solid var(--color-border);
}

.form-row {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-4);
}

.form-field {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-2);
}

.form-field--full {
    grid-column: 1 / -1;
}

.form-field--sm {
    grid-column: span 1;
}

.form-label {
    font-size: var(--font-size-sm);
    font-weight: var(--font-weight-medium);
    color: var(--text-secondary);
}

@media (max-width: 767px) {
    .form-row {
        grid-template-columns: 1fr;
    }
}
```

---

# 19. Dashboard Layout

## 19.1 Estrutura de Dashboard

```html
<div class="dashboard">
    <!-- KPIs -->
    <div class="dashboard__kpi-grid">
        <div class="kpi-card">...</div>
        <div class="kpi-card">...</div>
        <div class="kpi-card">...</div>
        <div class="kpi-card">...</div>
    </div>

    <!-- Gráficos -->
    <div class="dashboard__chart-grid">
        <div class="glass-panel dashboard__chart">Gráfico 1</div>
        <div class="glass-panel dashboard__chart">Gráfico 2</div>
    </div>

    <!-- Tabela recente -->
    <div class="glass-panel dashboard__table">
        Tabela de dados recentes
    </div>
</div>
```

## 19.2 CSS de Dashboard Layout

```css
.dashboard {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-5);
}

.dashboard__kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: var(--spacing-4);
}

.dashboard__chart-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-4);
}

.dashboard__chart {
    min-height: 320px;
}

.dashboard__table {
    min-height: 200px;
}

@media (max-width: 1023px) {
    .dashboard__kpi-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .dashboard__chart-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 575px) {
    .dashboard__kpi-grid {
        grid-template-columns: 1fr;
    }
}
```

---

# 20. DataGrid Layout

## 20.1 Estrutura

```html
<div class="datagrid-layout">
    <div class="datagrid-toolbar">
        <button>Novo</button>
        <button>Filtrar</button>
        <button>Exportar</button>
    </div>
    <div class="datagrid-container">
        <table class="datagrid">
            <thead>...</thead>
            <tbody>...</tbody>
        </table>
    </div>
    <div class="datagrid-footer">
        <span>1-20 de 150 registros</span>
        <div class="datagrid-pagination">...</div>
    </div>
</div>
```

## 20.2 CSS de DataGrid Layout

```css
.datagrid-layout {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-3);
    height: 100%;
}

.datagrid-toolbar {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    gap: var(--spacing-3);
}

.datagrid-container {
    flex: 1;
    overflow: auto;
    border: var(--border-thin) solid var(--color-border);
    border-radius: var(--radius-md);
}

.datagrid-footer {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-3) 0;
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
}
```

---

# 21. Breakpoints

## 21.1 Breakpoints Oficiais

```css
:root {
    --bp-xs: 0px;
    --bp-sm: 576px;
    --bp-md: 768px;
    --bp-lg: 1024px;
    --bp-xl: 1440px;
    --bp-xxl: 1920px;
}

/* XS: 0-575px (smartphone) */
/* SM: 576-767px (smartphone grande) */
@media (min-width: 576px) {}

/* MD: 768-1023px (tablet) */
@media (min-width: 768px) {}

/* LG: 1024-1439px (notebook) */
@media (min-width: 1024px) {}

/* XL: 1440-1919px (desktop) */
@media (min-width: 1440px) {}

/* XXL: 1920px+ (ultrawide) */
@media (min-width: 1920px) {}
```

## 21.2 Comportamento por Breakpoint

| Elemento | XS | SM | MD | LG | XL | XXL |
|----------|----|----|----|----|----|-----|
| Sidebar | Drawer | Drawer | Hover 64px | 260px | 260px | 260px |
| Topbar Left | Toggle | Toggle | Toggle | Toggle | Toggle | Toggle |
| Topbar Center | Hidden | Hidden | Visible | Visible | Visible | Visible |
| Workspace Padding | 12px | 12px | 16px | 20px | 20px | 20px |
| Grid Cols | 1 | 1 | 2 | 3 | 4 | 4 |
| Form Cols | 1 | 1 | 1 | 2 | 2 | 2 |
| KPI Cards | 1 | 2 | 2 | 4 | 4 | 4 |
| Launchpad | 2 | 2 | 3 | 4 | 4 | 4 |

---

# 22. Layers

## 22.1 Contextos de Empilhamento

```
Z-Index  Camada     Elementos
900      Fullscreen  Loading global, tela cheia
800      Tooltip     Tooltips
700      Toast       Toast notifications
600      Popover     Context menu, popover
500      Modal       Modal dialog
400      Backdrop    Modal overlay, drawer overlay
300      Fixed       Sidebar (mobile drawer)
200      Sticky      Topbar
100      Dropdown    Menus, autocomplete
0        Base        Workspace, content
```

## 22.2 Mapa de Layers

```css
.layer-base { z-index: var(--z-base); }
.layer-dropdown { z-index: var(--z-dropdown); }
.layer-sticky { z-index: var(--z-sticky); }
.layer-fixed { z-index: var(--z-fixed); }
.layer-backdrop { z-index: var(--z-modal-backdrop); }
.layer-modal { z-index: var(--z-modal); }
.layer-popover { z-index: var(--z-popover); }
.layer-toast { z-index: var(--z-toast); }
.layer-tooltip { z-index: var(--z-tooltip); }
.layer-fullscreen { z-index: var(--z-fullscreen); }
```

---

# 23. Performance de Layout

## 23.1 Regras de Performance

1. **Sempre usar flexbox ou grid** — nunca floats para layout
2. **Manter sidebar e topbar fixas** — apenas content scrolla
3. **Evitar reflow** — não animar width/height/top/left
4. **Usar `transform` para animações de painel** — slide, fade
5. **`will-change: transform`** em drawers e modais
6. **`contain: layout style`** em painéis independentes
7. **Evitar aninhamento profundo** — máx 4 níveis de flex/grid

## 23.2 Contain

```css
.glass-panel {
    contain: layout style;
}

.drawer {
    contain: layout style paint;
}

.modal {
    contain: layout style;
}
```

---

# 24. Boas Práticas

## 24.1 Regras de Layout

```
1. NUNCA: página define seu próprio layout
2. SEMPRE: página usa regiões do Workspace
3. NUNCA: sidebar e workspace scrollam juntos
4. SEMPRE: apenas Content scrolla
5. NUNCA: elementos fixos dentro de Content
6. SEMPRE: elementos fixos no Workspace (header, toolbar, status bar)
7. NUNCA: padding no Content (o componente interno define)
8. SEMPRE: gap entre regiões via variáveis do Workspace
9. NUNCA: ultrapassar viewport
10. SEMPRE: 100vh = app
```

## 24.2 Checklist de Layout

- [ ] Sidebar fixa (260px) ou colapsada (64px)
- [ ] Topbar fixa (56px)
- [ ] Workspace ocupa espaço restante
- [ ] Content é scrollável
- [ ] Status Bar fixa (32px)
- [ ] Nada ultrapassa viewport
- [ ] Mobile: sidebar vira drawer
- [ ] Tablet: sidebar hover-expand
- [ ] Desktop: sidebar fixa
- [ ] Formulários 2 colunas em desktop, 1 em mobile

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial — 24 seções, Layout Core completo |
