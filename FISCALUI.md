# FiscalUI Framework

**RFC — Request for Comments**

*Especificação oficial de arquitetura do FiscalUI Framework.*

---

## 01. Introdução

### Objetivo

Definir a visão geral do FiscalUI Framework: seus propósitos, público-alvo, escopo e como este documento deve ser lido.

### Motivação

Sistemas ERP têm ciclo de vida longo (10+ anos). A interface precisa ser consistente, extensível e independente de tecnologias terceiras que desaparecem ou mudam radicalmente a cada 2 anos. O FiscalUI nasceu para preencher esse vazio: um framework visual corporativo construído integralmente com HTML, CSS e JavaScript vanilla, sem React, Vue, Angular, Bootstrap, jQuery ou Tailwind.

### Arquitetura

```
FiscalUI Framework
│
├── Fase 1 — Framework Visual (sprints 01–05)
│   ├── Fundação: CSS modular, tipografia, ícones, tokens
│   ├── Navegação: Launchpad, Sidebar, Topbar, Workspace
│   ├── Dashboard: cards, KPI, widgets
│   ├── Componentes: ~50 componentes reutilizáveis
│   └── Temas: Light, Dark, Liquid Glass
│
└── Fase 2 — ERP (sprints 06–11)
    ├── Autenticação e permissões
    ├── CRUD (Empresas, Clientes, Produtos)
    ├── Módulos fiscais (NF-e, NFC-e, NFS-e, SPED)
    ├── Relatórios
    └── Publicação
```

### Público-alvo

- Desenvolvedores front-end construindo interfaces ERP/painéis administrativos
- Equipes que buscam design system consistente sem framework terceiro
- Projetos que priorizam performance, acessibilidade e zero dependências

### Decisões de projeto

| Decisão | Alternativa descartada | Motivo |
|---------|----------------------|--------|
| CSS vanilla | Tailwind, Bootstrap | Zero build step, controle total, sem lock-in |
| JS vanilla | React, Vue, Angular | Ciclo de vida 10+ anos, sem migração forçada |
| SVG sprite | Font icons (FontAwesome) | Performance, sem CDN, escalável |
| Menu data-driven (JSON) | Menu hardcoded no HTML | Navegação vira dado, alteração sem tocar em código |
| Inter self-hosted | Google Fonts | Zero dependência externa, privacidade, offline |

---

## 02. Filosofia

### Objetivo

Estabelecer os princípios fundamentais que guiam todas as decisões de design e implementação do FiscalUI.

### Motivação

Sem princípios claros, cada tela do sistema pode seguir direções diferentes. A filosofia do FiscalUI garante que, mesmo com dezenas de desenvolvedores, a interface permaneça coesa e previsível.

### Princípios

1. **Zero dependências externas** — nem Bootstrap, React, jQuery, Tailwind, Material UI ou Google Fonts. O framework é auto-suficiente.
2. **CSS modular** — cada componente tem seu escopo. Separação clara entre tokens (`variaveis.css`), reset (`reset.css`), layout (`layout.css`), ícones (`icons.css`) e componentes (`style.css`).
3. **Menu data-driven** — a navegação é definida em `assets/data/menu.json`. Alterar o menu não exige tocar em HTML ou JS de renderização.
4. **Ícones SVG nativos** — sprite único (`img/icons.svg`), carregado uma vez. Zero font-icons, zero CDN.
5. **Temas via CSS variables** — troca instantânea entre temas sem JavaScript pesado. Apenas sobrescrever tokens.
6. **Backend opaco** — o front-end conhece apenas a API REST. Nunca acessa COBOL, banco de dados ou camada de negócio diretamente.
7. **Launchpad → Workspace** — a Home apresenta os módulos; o Workspace apresenta o trabalho. Separação clara entre navegação e execução.
8. **FiscalUI é o Design System oficial da plataforma** — toda tela, de qualquer módulo (Cadastro de Clientes, NF-e, Plano de Contas, Estoque, CRM), deve parecer ter sido feita pela mesma equipe. Posição dos botões, comportamento das tabelas, cores, espaçamentos, ícones, animações e formulários seguem exclusivamente os tokens e componentes do FiscalUI. Nenhum módulo cria identidade visual própria. Essa consistência reduz a curva de aprendizado, facilita a manutenção e constrói a identidade do sistema — assim como Odoo, SAP Fiori e Microsoft Dynamics.

### Boas práticas

- Prefira `var(--token)` a valores literais em qualquer contexto visual
- Um arquivo = uma responsabilidade (`variaveis.css` = tokens, `layout.css` = grid, `style.css` = componentes)
- Todo novo módulo começa com uma entrada no `menu.json`, não com uma tag `<a>` no HTML

### Decisões de projeto

| Princípio | Por quê |
|-----------|---------|
| Vanilla JS | Frameworks JS exigem migração forçada. Um ERP vive 10+ anos. |
| CSS modular | Time de 1 dev ou 20 devs — a estrutura escala sem conflito |
| SVG sprite | 27+ ícones numa única requisição HTTP |

---

## 03. Arquitetura Geral

### Objetivo

Descrever a arquitetura macro do sistema, incluindo as duas fases de construção, o fluxo de navegação e as capacidades do framework.

### Motivação

Sistemas ERP são complexos. Tentar construir tudo de uma vez leva a retrabalho e inconsistência. A estratégia de duas fases isola responsabilidades: primeiro o framework visual (reutilizável em qualquer sistema), depois o negócio em cima dele.

### Arquitetura

```
Browser (HTML/CSS/JS)
    │
    │ HTTP REST (JSON)
    ▼
server.py (Python)
    │
    ├── API (autenticação, CRUD, relatórios)
    │
    ├── COBOL (subprocess → .dat)
    │
    └── fiscal/ (Python puro: XML, SOAP SEFAZ)
```

### Fluxo de navegação

```
Login → Launchpad (cards)
           │
           ├── Dashboard
           ├── NF-e ─────────┐
           ├── NFC-e         │
           ├── Produtos      ├── Workspace (sidebar contextual)
           ├── Clientes      │   ├── Header
           ├── Relatórios    │   ├── Toolbar
           ├── Empresas      │   ├── Filters
           └── Configuração  │   ├── Content
                             │   └── Status Bar
                             └── Voltar → Launchpad
```

### Regras

1. Nenhuma página cria layout próprio. Todas usam a estrutura do Layout Engine.
2. Nenhum componente acessa dados diretamente. Toda comunicação é via API REST.
3. Todo módulo segue exatamente a mesma estrutura de Workspace.

### Capacidades entregues (Fase 1)

- Sidebar retrátil com colapso e localStorage
- Topbar com navegação de módulos, pesquisa global e notificações
- Launchpad com 8 cards interativos (hover scale + glow)
- Workspace com Header, Toolbar, Filters, Content, Status Bar
- Sidebar contextual por módulo
- Status bar com usuário, empresa, versão, ambiente e relógio
- Responsividade mobile com sidebar drawer
- 27+ ícones SVG em sprite único
- Fonte Inter self-hosted
- Autenticação via token

### Próximos passos

- Sprint 04: biblioteca de componentes (input, select, tabela, modal, toast)
- Sprint 05: temas Light e Liquid Glass
- Sprint 06+: funcionalidades de negócio do ERP

---

## 04. Launchpad

### Objetivo

Definir a tela inicial do sistema — o Launchpad — como o ponto de partida visual para navegação entre módulos.

### Motivação

Menus textuais tradicionais (listas verticais de links) são eficientes para usuários experientes, mas ruins para descoberta. O Launchpad substitui a lista por **cartões visuais interativos**, cada um representando um módulo do sistema. Isso reduz a carga cognitiva e acelera a orientação de novos usuários.

### Arquitetura

O Launchpad é uma grade CSS de cartões dentro do Workspace, exibida quando nenhum módulo está selecionado (`index.html` sem parâmetro `?mod=`).

```
.workspace
  └── #launchpad
        ├── .welcome-section (saudação dinâmica)
        └── .quick-grid (cartões)
              ├── .quick-card (NF-e)
              ├── .quick-card (NFC-e)
              ├── .quick-card (Produtos)
              ├── .quick-card (Clientes)
              ├── .quick-card (Relatórios)
              ├── .quick-card (Empresas)
              ├── .quick-card (Configuração)
              └── .quick-card (Dashboard)
```

### Regras

1. Todo cartão é um link `<a>` para `?mod=<id>`.
2. Cartões não contêm sub-itens — apenas o nome do módulo e um ícone.
3. A grid é responsiva: `repeat(auto-fill, minmax(140px, 1fr))`.
4. A saudação muda conforme horário (Bom dia / Boa tarde / Boa noite).

### Comportamento

| Estado | Aparência |
|--------|-----------|
| Normal | Glass panel, opacidade base `.12` |
| Hover | `scale(1.03)`, sombra maior + glow teal, ícone sobe 2px |
| Clique | Navega para `?mod=<id>` → Workspace |

### Exemplos

```html
<a class="quick-card" href="?mod=nfe">
    <span class="quick-icon">📄</span>
    <span class="quick-label">NF-e</span>
</a>
```

```css
.quick-card:hover {
    transform: scale(1.03);
    box-shadow: 0 12px 40px rgba(0,0,0,.45),
                0 0 30px rgba(20,184,166,.12);
}
.quick-card:hover .quick-icon {
    transform: scale(1.15) translateY(-2px);
}
```

### Decisões de projeto

| Decisão | Alternativa | Motivo |
|---------|-------------|--------|
| Grid CSS | Flexbox manual | Grid é semanticamente correto para grade 2D |
| `auto-fill` | Colunas fixas | Adapta-se automaticamente a qualquer largura de tela |
| Link `<a>` comum | JavaScript `onclick` | Navegação nativa, funciona sem JS, SEO-friendly |

---

## 05. Workspace

### Objetivo

Definir o ambiente de trabalho de cada módulo — o Workspace — como a estrutura padrão onde todo o conteúdo operacional do sistema é exibido.

### Motivação

Cada módulo (NF-e, Produtos, Clientes, etc.) precisa de um espaço de trabalho específico. Se cada um criasse seu próprio layout, o sistema perderia consistência. O Workspace padroniza a estrutura: todo módulo tem Header, Toolbar, Filters, Content e Status Bar — o que muda é apenas o conteúdo.

### Arquitetura

```
Workspace
│
├── Header      (breadcrumb + título)
├── Toolbar     (ações: Novo, Pesquisar, Filtros)
├── Filters     (colapsável: pesquisa, status, data)
├── Content     (tabela, dashboard, formulário)
└── Status Bar  (usuário, empresa, versão, relógio)
```

### Regras

1. Header nunca possui botões de ação — apenas contexto.
2. Toolbar concentra **todas** as ações da tela.
3. Filters nunca se misturam com a Toolbar.
4. Content é a única região que muda entre módulos.
5. Status Bar é idêntica em todos os módulos.

### Mapeamento Launchpad → Workspace

| Cartão | Módulo no menu | Sidebar contextual |
|--------|----------------|-------------------|
| NF-e | faturamento | Notas, NFC-e, Eventos, Config |
| NFC-e | faturamento | Notas, NFC-e, Eventos, Config |
| Produtos | faturamento | Produtos, Categorias, NCM |
| Clientes | faturamento | Clientes, Contratos |
| Relatórios | faturamento | Relatórios |
| Empresas | faturamento | Empresas, Certificados |
| Config | configuracoes | Configurações |
| Dashboard | dashboard | Dashboard |

### Exemplo — Workspace NF-e

```text
┌──────────────────────────────────────────────────────────────┐
│ FiscalUI                                             Carlos │
├──────────────┬───────────────────────────────────────────────┤
│ Dashboard    │ FiscalBrasil / NF-e                           │
│ Notas        ├───────────────────────────────────────────────┤
│ NFC-e        │ [+ Novo] [Importar] [Exportar] [Pesquisar]   │
│ Eventos      ├───────────────────────────────────────────────┤
│ Config       │ [Pesquisar...] [Status: ▼] [Data: ▼]         │
│              ├───────────────────────────────────────────────┤
│              │ ┌───────────────────────────────────────────┐ │
│              │ │ Número  │ Cliente   │ Valor   │ Status   │ │
│              │ ├─────────┼───────────┼─────────┼──────────┤ │
│              │ │ 000001  │ ABC Ltda  │ 1.500   │ Autorizado│ │
│              │ └───────────────────────────────────────────┘ │
├──────────────┴───────────────────────────────────────────────┤
│ Usuário: Carlos | Empresa: Fiscal Brasil | v1.0.0 | Produção│
└──────────────────────────────────────────────────────────────┘
```

### Decisões de projeto

| Decisão | Alternativa | Motivo |
|---------|-------------|--------|
| Sidebar contextual única | Sidebar fixa global | Reduz poluição visual, exibe só o relevante |
| Filters separados da Toolbar | Tudo na toolbar | Responsabilidade única, evita confusão visual |
| Status Bar fixa | Apenas tooltips | Informação do sistema sempre visível |

---

## 06. Layout Engine

### Objetivo

Definir o núcleo estrutural do FiscalUI: o Layout Engine, responsável por organizar todos os componentes da interface de maneira consistente, responsiva e reutilizável.

### Motivação

Se cada tela criasse seu próprio layout, o sistema se tornaria inconsistente e difícil de manter. O Layout Engine estabelece uma estrutura única que **toda página obrigatoriamente segue**: TopBar + Sidebar + Workspace (Header, Toolbar, Filters, Content, Status Bar).

### Arquitetura

```
┌──────────────────────────────────────────────────────────────┐
│ TopBar (global, fixa)                                        │
├──────────────┬───────────────────────────────────────────────┤
│ Sidebar      │ Workspace                                     │
│ (contextual) │  ┌──────────────────────────────────────────┐ │
│              │  │ Header (título + breadcrumb)              │ │
│              │  ├──────────────────────────────────────────┤ │
│              │  │ Toolbar (ações)                          │ │
│              │  ├──────────────────────────────────────────┤ │
│              │  │ Filters (colapsável)                     │ │
│              │  ├──────────────────────────────────────────┤ │
│              │  │ Content (tabela / dashboard / formulário)│ │
│              │  ├──────────────────────────────────────────┤ │
│              │  │ Status Bar                               │ │
│              │  └──────────────────────────────────────────┘ │
└──────────────┴───────────────────────────────────────────────┘
```

### Hierarquia DOM

```html
<div id="app">                         <!-- flex row -->
    <aside id="sidebar">...</aside>    <!-- 260px | 64px collapsed -->
    <div class="main-area">            <!-- flex column, flex:1 -->
        <header class="topbar">...</header>
        <main class="workspace">       <!-- flex column, flex:1 -->
            <div id="launchpad">...</div>     <!-- ou -->
            <div id="workspace-view">         <!-- flex column -->
                <div class="workspace-header">...</div>
                <div class="workspace-toolbar">...</div>
                <div class="workspace-filters">...</div>
                <div class="workspace-content">...</div>
                <div class="status-bar">...</div>
            </div>
        </main>
    </div>
</div>
```

### Regras

1. Toda página possui TopBar.
2. Toda página possui Workspace.
3. Nenhuma página altera a estrutura principal (`#app > #sidebar + .main-area`).
4. Apenas o conteúdo do Workspace muda entre módulos.
5. Os componentes nunca controlam o layout — o Layout Engine controla a composição.
6. A Sidebar é recolhível via classe `.collapsed` (estado persistido em localStorage).
7. Em telas ≤768px, a Sidebar vira Drawer overlayout.

### Regiões do Workspace

| Região | Função | Comportamento |
|--------|--------|---------------|
| Header | Contexto | Breadcrumb + título. Sempre visível. |
| Toolbar | Ações | Botões de ação. Sempre visível. |
| Filters | Filtros | Colapsável. Exibido/oculto via `toggleFilters()`. |
| Content | Conteúdo | Tabela, formulário, dashboard. Ocupa espaço restante. |
| Status Bar | Informação | Usuário, empresa, versão, ambiente, relógio. Sempre visível. |

### Decisões de projeto

| Decisão | Alternativa | Motivo |
|---------|-------------|--------|
| Flexbox | Grid CSS para layout mestre | Sidebar de largura variável (collapse) exige flex |
| Sidebar recolhível (64px) | Sidebar oculta | Ícones ainda visíveis, acesso rápido |
| Drawer em mobile | Sidebar reduzida | Tela pequena não comporta sidebar fixa |
| Overlay escuro no Drawer | Sem overlay | Foco no conteúdo, fecha ao clicar fora |

### Exemplo — Colapso da Sidebar

```css
#sidebar { width: 260px; transition: width 250ms ease; }
#sidebar.collapsed { width: 64px; }
#sidebar.collapsed .menu-label,
#sidebar.collapsed .user-info { opacity: 0; width: 0; }
```

---

## 07. Design Tokens

> *RFC completa em `sprints/DESIGN_TOKENS.md`*
> *Implementação em `css/variaveis.css`*

### Objetivo

Definir a menor unidade de configuração visual do FiscalUI: os Design Tokens. Nenhum componente deve utilizar valores fixos — toda identidade visual é controlada por variáveis CSS.

### Motivação

Sem tokens, cada desenvolvedor pode usar cores, tamanhos e espaçamentos ligeiramente diferentes, gerando um sistema visual inconsistente. Com tokens centralizados, trocar o tema inteiro (Dark → Light) requer apenas alterar valores no `:root` — nenhum componente é modificado.

### Arquitetura

```
Design Tokens (css/variaveis.css)
│
├── Colors         (primary, secondary, surfaces, text, border, semantic)
├── Typography     (family, scale: display→caption, weight)
├── Spacing        (escala: 0,2,4,8,12,16,24,32,40,48,64,80,96)
├── Radius         (none, sm, md, lg, xl, 2xl, rounded, pill)
├── Borders        (thin, medium, thick)
├── Shadows        (xs, sm, md, lg, xl, glass)
├── Glass          (bg, blur, border, shadow, highlight)
├── Motion         (duration: 100–500ms, easing: 4 curvas)
├── Opacity        (100% → 0%)
└── Z-Index        (base → fullscreen)
```

### Regras

1. Todo valor visual deve ser um token — nunca um valor literal.
2. `❌ color: #14b8a6;` → `✅ color: var(--color-primary);`
3. Componentes nunca definem cores, apenas consomem tokens.
4. Tokens são organizados por categoria, não por componente.

### Exemplos

```css
/* ❌ Ruim — valor fixo */
.button-submit {
    background: #14b8a6;
    border-radius: 12px;
    padding: 12px 22px;
}

/* ✅ Bom — tokens */
.button-submit {
    background: var(--color-primary);
    border-radius: var(--radius-lg);
    padding: var(--spacing-4) var(--spacing-6);
}
```

```css
/* Troca de tema sem tocar em componentes */
[data-theme="light"] {
    --color-primary: #0d9488;
    --surface-glass: rgba(255,255,255,.6);
    --text-primary: #1a202c;
    --bg-gradient: linear-gradient(135deg, #f0f4f8, #e2e8f0);
}
```

### Decisões de projeto

| Decisão | Alternativa | Motivo |
|---------|-------------|--------|
| CSS variables | Pré-processador (Sass) | Nativo, sem build step, tema troca em runtime |
| Escala de 2px (spacing) | Escala de 4px | Mais granularidade para ajustes finos |
| Aliases legado (`--space-*`) | Quebra completa | Compatibilidade com CSS existente |
| Glass como tokens separados | Parte de surfaces | Tema Liquid Glass é o principal, merece destaque |

### Boas práticas

- Use `--spacing-*` para novos componentes; `--space-*` (legado) apenas para compatibilidade
- Prefira `--radius-*` descritivo (md, lg, xl) em vez de valores de pixel
- Cores semânticas (success, warning, danger, info) são para **estados**, não para botões
- `--motion-*` (duration) + `--ease-*` (curva) = `--transition-*`

---

## 08. Sistema de Grid

> *Especificação completa: `sprints/GRID.md`*
> *Implementação: `css/grid.css`*

### Objetivo

Definir o sistema de grid responsivo do FiscalUI, baseado em CSS Grid Layout de 12 colunas. Nenhum componente define sua própria posição — todos ocupam regiões previamente definidas pelo Grid.

### Motivação

Sem um grid padronizado, cada página acaba com CSS específico de posicionamento. Isso gera inconsistência, dificulta manutenção e quebra responsividade. O Grid de 12 colunas resolve isso de forma definitiva.

### Filosofia

**O Grid não pertence ao componente. O componente pertence ao Grid.**

Primeiro define-se a estrutura. Depois inserem-se os componentes. Nunca o contrário.

### Arquitetura

```
Grid (12 colunas)
│
├── Containers (container, container-fluid, container-compact)
├── Columns   (grid-cols-1 a grid-cols-12)
├── Spans     (col-span-1 a col-span-12)
├── Gaps      (gap-0 a gap-10, via tokens de spacing)
├── Alignment (justify-*, items-*)
├── Order     (order-first, order-last, order-1/2/3)
└── Areas     (grid-areas + area-*)
```

### Breakpoints

| Nome | Largura | Comportamento do grid |
|------|---------|----------------------|
| XL | ≥1600px | 12 colunas |
| Desktop | ≥1280px | 12 colunas |
| Notebook | ≥1024px | 12 → 6 colunas (acima de 6) |
| Tablet | ≥768px | 6 → 2 colunas (acima de 4) |
| Mobile | <576px | 1 coluna, spans ignorados |

### Containers

```css
.container { max-width: 1200px; margin: 0 auto; }
.container-fluid { width: 100%; }
.container-compact { max-width: 480px; } /* para login */
```

### Exemplos

**Dashboard — 4 KPIs:**

```html
<div class="grid grid-cols-4">
    <div class="glass-panel">KPI 1</div>
    <div class="glass-panel">KPI 2</div>
    <div class="glass-panel">KPI 3</div>
    <div class="glass-panel">KPI 4</div>
</div>
```

**Formulário — 2 colunas, mobile 1:**

```html
<div class="grid grid-cols-2">
    <div class="field">
        <label>Nome</label>
        <input>
    </div>
    <div class="field">
        <label>CPF/CNPJ</label>
        <input>
    </div>
    <div class="field col-span-2">
        <label>Endereço</label>
        <input>
    </div>
</div>
```

**Layout de áreas:**

```html
<div class="grid-areas" style="grid-template-areas:
    'header header'
    'sidebar content'
    'footer footer'">
    <header class="area-header glass-panel">Header</header>
    <aside class="area-sidebar glass-panel">Sidebar</aside>
    <main class="area-content glass-panel">Content</main>
    <footer class="area-footer glass-panel">Footer</footer>
</div>
```

### Regras

1. Todo elemento visual existe dentro do Sistema de Grid.
2. Nenhum componente define `margin` ou `width` para posicionamento.
3. Espaçamentos usam exclusivamente tokens (`--spacing-*` / `--grid-gutter`).
4. Tabelas ocupam sempre 12 colunas.
5. Cards do Launchpad usam `auto-fill`, não colunas fixas.

### Boas práticas

- Use `container-fluid` para dashboards; `container` para páginas de formulário; `container-compact` para login
- Prefira `col-span-*` explícito em vez de confiar na ordem automática
- Em formulários: use `grid grid-cols-2` que vira 1 coluna no mobile automaticamente
- Evite `order-*` se puder reorganizar o HTML — use order apenas para exceções

### Decisões de projeto

| Decisão | Alternativa | Motivo |
|---------|-------------|--------|
| 12 colunas | 8, 16, 24 colunas | 12 é divisível por 2,3,4,6 — máxima flexibilidade |
| Colapsa para 6 → 2 → 1 | Colapsa direto para 1 | Transição suave, melhor adaptação em tablet |
| CSS Grid nativo | Flexbox, float, framework | Grid é semanticamente correto para layout 2D |
| `gap` via tokens | `gap` fixo | Consistência com o sistema de Design Tokens |
| Responsivo via media query | Classes responsivas (`.col-md-6`) | Menos HTML, mais CSS — decisão intencional |

### Tokens do Grid

```css
--grid-columns: 12;
--grid-gutter: var(--spacing-5);   /* 16px */
--bp-xl: 1600px;
--bp-desktop: 1280px;
--bp-notebook: 1024px;
--bp-tablet: 768px;
--container-max: 1200px;
--container-compact: 480px;
```

### Próximos passos

- Testar o grid com todos os componentes existentes (Launchpad, login, workspace)
- Criar página de demonstração do grid no sistema
- Validar responsividade nos breakpoints reais

## 09. Sistema de Temas (Theme Engine)

> *Especificação completa: `sprints/THEME_ENGINE.md`*
> *Implementação: `css/themes.css`*

### Objetivo

Definir o Theme Engine do FiscalUI: o sistema que controla toda a aparência visual através de Design Tokens, permitindo múltiplos temas sem alterar os componentes.

### Motivação

Sem um sistema de temas, cada alteração visual exige modificar componentes individualmente. Com o Theme Engine, os componentes nunca sabem qual tema está ativo — eles apenas consomem tokens. Trocar de Dark para Light é instantâneo: o `data-theme` muda no `<html>`, e o CSS sobrescreve os tokens.

### Arquitetura

```
[data-theme="dark"]     ← variaveis.css (default)
[data-theme="light"]    ← themes.css
[data-theme="high-contrast"] ← themes.css
```

Mecanismo de troca:

```js
document.documentElement.setAttribute("data-theme","light");
localStorage.setItem("fiscalui_theme","light");
```

### Filosofia

**O componente nunca muda. Quem muda é o tema.**

```
Button → mesmo HTML → mesmo CSS → Dark / Light / Glass / Corporate
```

### Temas oficiais

| Tema | Fundo | Contraste | Ideal para |
|------|-------|-----------|------------|
| Dark | Escuro gradiente | Médio | Uso contínuo, baixa fadiga visual |
| Light | Claro (#f0f4f8) | Alto | Ambientes corporativos |
| High Contrast | Preto (#000) | Máximo | Acessibilidade |

### Regras

1. Nenhum componente depende de um tema específico.
2. Todo componente funciona em todos os temas.
3. Temas fornecem apenas valores — nunca comportamento.
4. A troca de tema é instantânea, sem recarregar a página.
5. O tema é persistido em `localStorage` e restaurado no login.

### Implementação

**Troca de tema:**

```js
const THEMES = ["dark", "light", "high-contrast"];

window.setTheme = function(name) {
    document.documentElement.setAttribute("data-theme", name);
    localStorage.setItem("fiscalui_theme", name);
};

window.toggleTheme = function() {
    const current = document.documentElement.getAttribute("data-theme") || "dark";
    const next = THEMES[(THEMES.indexOf(current) + 1) % THEMES.length];
    setTheme(next);
};
```

**Tema Light (exemplo de sobrescrita):**

```css
[data-theme="light"] {
    --bg-gradient: linear-gradient(135deg, #f0f4f8, #e2e8f0, #cbd5e1);
    --glass-bg: rgba(255,255,255,.7);
    --text-primary: #1a202c;
    --text-secondary: #4a5568;
    --color-primary: #0f766e;
    --border-color: rgba(0,0,0,.1);
}
```

### Boas práticas

- Sempre use `data-theme` no `<html>`, nunca no `<body>`
- Não duplique regras de componente no tema — sobrescreva apenas tokens
- Teste todo novo componente em todos os temas antes de mergear
- Prefira temas pré-definidos a personalizações por empresa (evita fragmentação)

### Decisões de projeto

| Decisão | Alternativa | Motivo |
|---------|-------------|--------|
| `data-theme` no HTML | Classe no body | Herança CSS mais previsível, nível documento |
| Tokens via CSS variables | Pré-processador | Troca em runtime, sem build |
| `themes.css` único | Múltiplos arquivos | Uma requisição, sem dependência de diretório |
| `localStorage` | SessionStorage / cookie | Persiste entre sessões, preferência do usuário |

### Próximos passos

- Criar tema Corporate (customizável por empresa)
- Adicionar tema Liquid Glass como variação do Dark com reflexos
- Botão de tema na tela de login (para acessibilidade antes da autenticação)

---

## 10. Biblioteca de Componentes

> *Documentação completa em `sprints/COMPONENTES.md`*

### Objetivo

Catálogo oficial de todos os componentes do FiscalUI (~50), com status de implementação e sprint de entrega.

### Estado atual

| Componente | Status |
|-----------|--------|
| TopBar, Sidebar, Toolbar, StatusBar | ✅ Implementado |
| Breadcrumb, Search, Filters | ✅ Implementado |
| Launchpad, QuickCard, Workspace | ✅ Implementado |
| KPI Card, Dashboard Grid | ✅ Implementado |
| Glass Panel, Table | ✅ Implementado |
| Formulários (Input, Select, etc.) | ⬜ Sprint 04 |
| Modal, Toast, Dialog, Loading | ⬜ Sprint 04 |
| Grid de dados completo | ⬜ Sprint 04 |

---

## 11. JavaScript Core

> *Especificação completa: `sprints/JAVASCRIPT_CORE.md`*
> *Implementação: `js/core/`, `js/services/`, `js/components/`, `js/utils/`*

### Objetivo

Construir o núcleo comportamental do FiscalUI. Cada módulo possui responsabilidade única. Nenhum módulo conhece o Backend. A comunicação entre módulos ocorre exclusivamente via Event Manager.

### Arquitetura

```
js/
├── core/          Inicialização, ciclo de vida
├── router/        Navegação SPA
├── events/        Event Manager
├── state/         Estado da interface
├── services/      Toast, Modal, Dialog, Loading, Storage
├── components/    Sidebar, Topbar, Table, Form, etc.
├── plugins/       QRCode, Charts, Maps (extensível)
└── utils/         Datas, valores, debounce, validação
```

### Filosofia

| Camada | Responsabilidade | Tecnologia |
|--------|----------------|------------|
| Estrutura | HTML | O que é |
| Aparência | CSS | Como parece |
| Comportamento | JavaScript | Como funciona |

### Core

`js/core/fiscalui.js` — inicializa todo o Framework.

```js
class FiscalUI {
    constructor() {
        this.router   = new Router();
        this.events   = new EventManager();
        this.state    = new StateManager();
        this.services = {};
        this.plugins  = {};
    }
    init() {
        this.state.init();
        this.router.init();
        this.events.init();
        this.loadTheme();
        this.loadLang();
    }
}
```

### Event Manager

Todo componente comunica-se através de eventos. Nunca diretamente.

```js
// Errado — acoplamento direto
button.save → tabela.refresh

// Correto — via Event Manager
button.save → event.emit("document.save")
           → event.on("document.save", tabela.refresh)
           → event.on("document.save", toast.success)
```

### Component Lifecycle

```js
class Component {
    constructor() { /* ... */ }
    create()   { /* monta DOM */ }
    init()     { /* registra eventos */ }
    render()   { /* atualiza DOM */ }
    destroy()  { /* remove eventos, limpa DOM */ }
}
```

### Regras

1. Nenhum módulo depende de outro diretamente — sempre via eventos
2. O JavaScript Core não conhece SQL, COBOL, Python ou regras fiscais
3. Toda validação definitiva pertence ao Backend
4. Nunca usar `alert()`, `confirm()` ou `prompt()` — usar serviços do Framework
5. Navegação SPA sem recarregar a página
6. Todo acesso ao Backend é assíncrono, com Loading e tratamento de erros
7. Nunca armazenar senhas ou tokens inseguros no cliente

### Próximos passos

- Implementar `js/core/fiscalui.js` (classe principal)
- Implementar `js/events/EventManager.js` (pub/sub)
- Implementar `js/state/StateManager.js` (estado global)
- Implementar `js/services/ToastService.js`
- Implementar `js/services/LoadingService.js`
- Implementar `js/services/ModalService.js`
- Implementar `js/services/StorageService.js`
- Implementar `js/utils/format.js` (datas, valores, CPF, CNPJ)
- Implementar `js/utils/helpers.js` (debounce, throttle, uuid)
- Migrar `app.js` para a nova arquitetura modular
- [x] Router (navegação SPA) — `js/router/Router.js`
- [x] Plugin Manager — `js/plugins/PluginManager.js` + `ShortcutsPlugin.js`
- [x] Error Manager — `js/services/ErrorManager.js` (captura, log, notificação Toast)

### Error Manager

Todo erro do sistema passa pelo ErrorManager. Ele captura exceções (`window.onerror`, `unhandledrejection`), normaliza, registra no histórico e notifica o usuário via Toast.

```js
FiscalUI.errors.capture(error, { level: "error", api: "/nfe/salvar" });
FiscalUI.errors.wrap(fn, { context: "click" });
FiscalUI.errors.wrapAsync(promise, { context: "loadData" });
FiscalUI.errors.warn("Menu não carregado");
FiscalUI.errors.fatal("Falha na autenticação");
```

Nunca usar `alert()` — o ErrorManager exibe Toast automaticamente para erros e fatais.

---

## 12. Responsive Engine

> *Especificação completa: `sprints/RESPONSIVE_ENGINE.md`*
> *Implementação: `js/responsive/ResponsiveEngine.js` + `css/responsive.css`*

### Objetivo

Adaptar automaticamente toda a interface a diferentes dispositivos. A responsividade pertence ao Framework, não aos componentes.

### Filosofia

Não existem duas interfaces (Desktop e Mobile). Existe apenas uma interface que se reorganiza conforme o espaço disponível.

```
Mesmo HTML → Mesmo CSS → Mesmo JavaScript → Layouts diferentes
```

Estratégia: **Mobile First** — a interface cresce, nunca diminui.

### Breakpoints oficiais

| ID | Mínimo | Máximo | Nome | Comportamento |
|----|--------|--------|------|---------------|
| XS | 0 | 575px | Telefone | Sidebar drawer, tabelas em card, form 1 col |
| SM | 576px | 767px | Telefone Grande | Sidebar drawer, modais centralizados |
| MD | 768px | 1023px | Tablet | Sidebar hover (64px → 240px), topbar completa |
| LG | 1024px | 1439px | Notebook | Sidebar 240px, colapsável, grid 3 col |
| XL | 1440px | 1919px | Desktop | Grid 4 col, workspace amplo |
| XXL | 1920px+ | — | UltraWide | Workspace centralizado (max 1600px) |

### ResponsiveEngine (JS)

```js
FiscalUI.responsive.breakpoint   // "xs" | "sm" | "md" | "lg" | "xl" | "xxl"
FiscalUI.responsive.isMobile()   // true em XS/SM
FiscalUI.responsive.isTablet()   // true em MD
FiscalUI.responsive.isDesktop()  // true em LG/XL/XXL
FiscalUI.responsive.atLeast("md") // breakpoint ≥ MD
```

Eventos escutáveis:

```js
FiscalUI.on("responsive:change", ({breakpoint, prev, width}) => { ... })
```

Estado sincronizado automaticamente:

```js
FiscalUI.state.get("breakpoint")  // "md"
FiscalUI.state.get("isMobile")    // true
FiscalUI.state.get("viewportWidth") // 375
```

### Comportamentos por componente

| Componente | Mobile (<768px) | Tablet (768-1023px) | Desktop (≥1024px) |
|------------|----------------|---------------------|-------------------|
| Sidebar | Drawer overlay | Hover expand (64→240) | Fixa 240px, colapsável |
| Topbar | Ícone + menu hamburguer | Links + ícones | Completa com nav |
| Tabelas | Card view (vertical) | Completa | Completa |
| Formulários | 1 coluna | 1 coluna | 2+ colunas |
| KPI Cards | 2 por linha | 4 por linha | 4 por linha |
| Dashboard Grid | 1 col | 2 col | 3-4 col |
| Launchpad Cards | 2 por linha | 3 por linha | 4 por linha |
| Modais | Tela cheia | Centralizado 90% | Centralizado |
| Status Bar | Vertical | Horizontal | Horizontal |
| Toolbar | Overflow + wrap | Ícones | Botões completos |

### Implementação

**CSS Mobile First:**

```css
/* Mobile (base) */
#sidebar { transform: translateX(-100%); }          /* drawer */
#sidebar.mobile-open { transform: translateX(0); }
table { font-size: .75rem; }
.modal-box { width: 100%; min-height: 100vh; }    /* tela cheia */

/* Tablet (≥768px) */
@media(min-width:768px){
    #sidebar { width: 64px; }
    #sidebar:hover { width: 240px; }               /* hover expand */
    .modal-box { max-width: 480px; min-height: auto; }
}

/* Desktop (≥1024px) */
@media(min-width:1024px){
    #sidebar { width: 240px; }
    #sidebar.collapsed { width: 64px; }            /* colapsável */
}

/* UltraWide (≥1920px) */
@media(min-width:1920px){
    .workspace { max-width: 1600px; margin: 0 auto; }
}
```

**Tabela → Card (mobile):**

```css
@media(max-width:767px){
    .table-responsive thead { display: none; }
    .table-responsive tbody tr {
        display: block; border-radius: .5rem; padding: .75rem;
    }
    .table-responsive tbody td {
        display: flex; justify-content: space-between;
    }
    .table-responsive tbody td::before {
        content: attr(data-label); font-weight: 600;
    }
}
```

### Próximos passos

- Adicionar `data-label` nos `<td>` das tabelas que ainda não têm
- Testar todos os componentes em XS, MD, LG
- Validar touch events na sidebar (gesto de swipe para abrir/fechar)
- Adicionar container queries nos componentes críticos (Cards, KPIs)

---

## 13. Accessibility Framework

> *Especificação completa: `sprints/ACCESSIBILITY.md`*
> *Implementação: `js/accessibility/AccessibilityEngine.js` + `css/accessibility.css`*

### Objetivo

Garantir que todos os componentes, layouts e interações nasçam acessíveis desde a concepção, em conformidade com WCAG 2.1 AA.

### Princípios (WCAG)

1. **Perceptível** — informação perceptível por qualquer sentido
2. **Operável** — funcionalidade acessível por teclado, voz, toque
3. **Compreensível** — interface previsível, erros explicativos
4. **Robusto** — compatível com tecnologias assistivas atuais e futuras

### AccessibilityEngine (JS)

```js
FiscalUI.a11y.announce("NF-e salva com sucesso");       // ARIA live region
FiscalUI.a11y.focus(el);                                 // Move foco + tabindex
FiscalUI.a11y.trapFocus(container);                      // Trava foco (modais)
FiscalUI.a11y.releaseFocus();                            // Libera + restaura
FiscalUI.a11y.saveFocus();                               // Guarda foco atual
```

### Funcionalidades automáticas

| Funcionalidade | Gatilho | Comportamento |
|---|---|---|
| Focus trap | Modal abre | Foco preso no modal, ESC fecha |
| Focus restore | Modal fecha | Foco volta ao elemento anterior |
| ARIA live region | Toast aparece | Anúncio para screen reader |
| `role="alert"` | Toast | Atribuído automaticamente |
| `role="dialog"` | Modal | Atribuído automaticamente |
| Reduced motion | `prefers-reduced-motion:reduce` | Remove animações |
| Skip link | Carregamento | Link "Pular para conteúdo" |
| MutationObserver | DOM dinâmico | ARIA attributes em elementos novos |

### CSS implementado

| Seletor | Função |
|---|---|
| `.skip-link` | Link de pular para conteúdo, visível no foco |
| `:focus-visible` | Indicador de foco com cor do tema |
| `.sr-only` | Conteúdo apenas para leitores de tela |
| `.reduced-motion` | Remove animações |
| `@media (forced-colors:active)` | Modo alto contraste do SO |
| `@media (prefers-reduced-motion:reduce)` | Animação zero |

### Checklist de componente acessível

- [ ] Navegável apenas com teclado?
- [ ] Foco visível?
- [ ] Compreensível sem depender de cores?
- [ ] HTML semântico?
- [ ] ARIA attributes quando necessário?
- [ ] Funciona com screen readers?
- [ ] Contraste adequado em todos os temas?
- [ ] Responsivo?
- [ ] Mensagens de erro claras?

---

## 14. Motion Design

> *Especificação completa: `sprints/MOTION_DESIGN.md`*
> *Implementação: `css/motion.css`*

### Objetivo

Definir o sistema de animações e transições do FiscalUI: durações, curvas de easing e comportamentos. Movimento é informação — toda animação tem propósito.

### Princípios

1. **Clareza** — a animação explica a ação
2. **Continuidade** — transições naturais, sem saltos
3. **Hierarquia** — elementos importantes têm mais destaque
4. **Feedback** — toda ação produz resposta visual
5. **Performance** — apenas `transform` e `opacity` (GPU)

### Motion Tokens

| Token | Valor | Uso |
|---|---|---|
| `--motion-instant` | 100ms | Microfeedback |
| `--motion-fast` | 150ms | Hover, focus, clique |
| `--motion-normal` | 250ms | Transições padrão |
| `--motion-smooth` | 350ms | Modal, drawer, toast |
| `--motion-slow` | 500ms | Entrada de tela, KPI |
| `--ease-out` | cubic-bezier(.16,1,.3,1) | Saída natural |
| `--ease-spring` | cubic-bezier(.34,1.56,.64,1) | Modal scale |

### Keyframes disponíveis

| Animação | Uso |
|---|---|
| `fadeIn` / `fadeOut` | Modal overlay, transições de conteúdo |
| `slideUp` | Toast, notificações |
| `slideDown` | Dropdown, submenu |
| `scaleIn` | Modal box, dialogo |
| `pulse` | Loading, indicador |
| `shimmer` | Skeleton loading |
| `spin` | Spinner |
| `glassGlow` | Efeito Liquid Glass |
| `countUp` | Valor de KPI ao carregar |

### Transições por componente

| Componente | Propriedade | Duração |
|---|---|---|
| Sidebar | `width`, `transform` | 350ms ease-out |
| Modal overlay | `opacity` | 250ms ease-out |
| Modal box | `transform` + `opacity` | 350ms spring |
| Toast | `transform` + `opacity` | 350ms ease-out |
| Glass panel | `background`, `backdrop-filter` | 250ms ease-out |
| Hover (card) | `transform` + `box-shadow` | 150ms ease-out |
| KPI value | `opacity` + `transform` | 500ms ease-out |

### Redução de movimento

Respeitado automaticamente via `prefers-reduced-motion:reduce` e classe `.reduced-motion` — toda animação cai para 0.01ms.

### Utility classes

```html
<div class="fade-in">...</div>
<div class="slide-up">...</div>
<div class="scale-in">...</div>
```

### Liquid Glass

Efeito premium com `radial-gradient` animado e `glassGlow` — ativado pela classe `.glass-panel.glass-premium`.

---

## 15. Icon System

> *Especificação completa: `sprints/ICON_SYSTEM.md`*
> *Implementação: `css/icons.css` + `js/services/IconManager.js`*

### Objetivo

Padronizar toda a iconografia do FiscalUI: SVG puro, tamanhos via tokens, cores semânticas, estados integrados ao Theme Engine.

### Tecnologia

SVG exclusivamente — sprite único injetado no DOM (`img/icons.svg`). Nunca PNG, JPG, GIF ou font icons.

### Tamanhos oficiais

| Classe | Token | Tamanho | Stroke |
|---|---|---|---|
| `.icon-xs` | `--icon-xs` | 16px | 1.5 |
| `.icon-sm` | `--icon-sm` | 20px | 2 |
| `.icon-md` | `--icon-md` | 24px | 2 |
| `.icon-lg` | `--icon-lg` | 32px | 1.5 |
| `.icon-xl` | `--icon-xl` | 48px | 1.5 |
| `.icon-xxl` | `--icon-xxl` | 64px | 1.25 |

### Cores semânticas

```html
<svg class="icon icon-success"><use href="#icon-check"/></svg>
<svg class="icon icon-error"><use href="#icon-x"/></svg>
<svg class="icon icon-warning"><use href="#icon-alert"/></svg>
<svg class="icon icon-info"><use href="#icon-info"/></svg>
```

Cores definidas pelo Theme Engine (`--color-success`, `--color-error`, etc.).

### Estados

| Classe | Comportamento |
|---|---|
| `.icon-disabled` | Opacidade .5, sem eventos |
| `.icon-spin` | Rotação contínua (loading) |
| `.icon-btn` | Área 44x44 acessível + hover/focus |

### IconManager (JS)

```js
FiscalUI.icons.html("icon-save")          // <svg class="icon icon-sm">...
FiscalUI.icons.html("icon-save","lg")     // tamanho lg
FiscalUI.icons.btn("icon-edit")           // <button class="icon-btn">...
FiscalUI.icons.btn("icon-edit","md","Editar") // com aria-label
FiscalUI.icons.text("icon-user","Cliente")     // ícone + label
FiscalUI.icons.isLoaded()                 // sprite carregado?
```

### Acessibilidade

- Todo ícone isolado tem `aria-label` e `title`
- `aria-hidden="true"` em SVGs decorativos (quando acompanhados de texto)
- `.icon-btn` garante área mínima de 44×44px

### Estrutura do sprite

```
img/icons.svg
├── icon-home, icon-menu, icon-search
├── icon-save, icon-edit, icon-delete, icon-print
├── icon-nfe, icon-nfce, icon-cte
├── icon-user, icon-building, icon-client
├── icon-chevron-down, icon-chevron-left, icon-chevron-right
├── icon-bell, icon-logout, icon-settings
├── icon-file-text, icon-download, icon-upload
├── icon-moon, icon-sun, icon-eye
└── icon-clock, icon-filter, icon-refresh
```

---

## 16. Form System

> *Especificação completa: `sprints/FORM_SYSTEM.md`*
> *Implementação: `css/forms.css` + `js/services/FormService.js`*

### Objetivo

Padronizar todos os formulários do ERP: estrutura, componentes, estados, máscaras, validação de interface e layout responsivo.

### Arquitetura

```
Form Container → Sections → Field Groups → Fields → Validação → API
```

### Componentes de formulário

| Componente | CSS | Máscara nativa |
|---|---|---|
| Input, Textarea | `.form-input` | — |
| Select | `select.form-input` | — |
| Checkbox | `.form-checkbox` | — |
| Radio | `.form-radio` | — |
| Switch | `.form-switch` | — |
| CPF | `.form-input[data-mask="cpf"]` | `000.000.000-00` |
| CNPJ | `.form-input[data-mask="cnpj"]` | `00.000.000/0000-00` |
| CEP | `.form-input[data-mask="cep"]` | `00000-000` |
| Telefone | `.form-input[data-mask="phone"]` | `(00) 00000-0000` |
| Moeda | `.form-input[data-mask="money"]` | `1.234,56` |
| Percentual | `.form-input[data-mask="percent"]` | `99,99%` |

### Estados visuais

| Estado | Classe gerada |
|---|---|
| Default | — |
| Hover | `:hover` |
| Focus | `:focus` |
| Error | `.has-error` (no `.form-field`) |
| Success | `.has-success` |
| Warning | `.has-warning` |
| Disabled | `:disabled` |
| Readonly | `[readonly]` |

### FormService (JS)

```js
// Máscaras — basta adicionar data-mask no HTML
<input data-mask="cpf" class="form-input">

// Ou via JS
FiscalUI.form.mask(el, "cnpj");

// Serializar formulário
const dados = FiscalUI.form.serialize(formEl);

// Popular formulário
FiscalUI.form.populate(formEl, {nome: "João", cpf: "000.000.000-00"});

// Validar
const erros = FiscalUI.form.validate(formEl);
FiscalUI.form.showErrors(formEl, erros);
FiscalUI.form.clearErrors(formEl);
```

### Layout

```html
<div class="form-container">
  <div class="form-section">
    <h3 class="form-section-title">Dados Gerais</h3>
    <div class="form-row">
      <div class="form-field">
        <label class="form-label" for="nome">Nome <span class="required">*</span></label>
        <input id="nome" class="form-input" required>
      </div>
      <div class="form-field">
        <label class="form-label" for="cpf">CPF</label>
        <input id="cpf" class="form-input" data-mask="cpf">
      </div>
    </div>
  </div>
</div>
```

---

## 17. Data Grid Framework

> *Especificação Técnica completa: `sprints/DATA_GRID.md` (29 seções)*
> *Implementação: pendente*

### Objetivo

Disponibilizar um componente corporativo capaz de suportar desde pequenas listas até milhões de registros, com virtualização, alta performance, plugin system e integração total com o FiscalUI.

### Escopo

| Funcionalidade | Versão |
|---|---|
| Listagens, cadastros, consultas | 1.0 |
| Ordenação (asc/desc/multi) | 1.0 |
| Filtros nativos (texto, número, data, lista) | 1.0 |
| Paginação + Scroll infinito | 1.0 |
| Virtualização (viewport → 40 linhas DOM) | 1.0 |
| Seleção (única, múltipla, shift, ctrl, total) | 1.0 |
| Inline Edit | 1.0 |
| Exportação (Excel, PDF) | 1.0 |
| Card View responsivo (mobile) | 1.0 |
| Agrupamentos com subtotais | 2.0 |
| Master Detail | 2.0 |
| Tree Grid, Pivot, Timeline | 2.0 |
| IA, Analytics, colunas calculadas | 3.0 |

### Arquitetura

```
DataGrid
├── Header (Toolbar + FilterBar)
├── Column Manager
├── Virtual Scroll
├── Body (viewport → virtual rows → DOM)
├── Footer (Pagination + Status)
└── Services
```

### API Pública

```js
grid.load() / grid.reload() / grid.refresh()
grid.select() / grid.unselect()
grid.filter() / grid.sort() / grid.group()
grid.export() / grid.print()
grid.scrollTo() / grid.focus()
```

### Eventos

```js
grid:init, grid:load, grid:loaded, grid:sort, grid:filter,
grid:select, grid:edit, grid:save, grid:error, grid:destroy
```

### Colunas

```json
{ "field": "numero", "label": "NF-e", "width": 120,
  "sortable": true, "filterable": true, "editable": false,
  "formatter": "documentoFiscal" }
```

### Performance

| Métrica | Meta |
|---|---|
| Tempo inicial | < 300ms |
| Scroll | 60 FPS |
| DOM simultâneo | Controlado (só visíveis) |

---

## 18. Dashboard System

> *Especificação Técnica completa: `sprints/DASHBOARD_SYSTEM.md` (31 seções)*

### Objetivo

Fornecer uma plataforma flexível para apresentação de informações estratégicas em tempo real. O Dashboard não é apenas uma página inicial — é um Workspace Inteligente.

### Arquitetura

```
Dashboard
├── Layout Engine (Grid 12 colunas)
├── Widget Manager (registro + ciclo de vida)
├── KPI Engine (12 indicadores oficiais)
├── Chart Engine (11 tipos de gráfico)
├── Notification Center
├── Activity Feed
└── Plugin Manager
```

### Componentes Oficiais

KPI Card, Statistic Card, Chart (linha, barra, pizza, radar, heatmap, gauge, etc.), Timeline, Calendar, Notifications, Activity Feed, Quick Actions, Mini Table, Data Grid, Alerts, Shortcuts, Tasks, Favorites.

### Widget API

```js
widget.create() / widget.load() / widget.refresh()
widget.resize() / widget.move() / widget.destroy()
widget.export() / widget.print()
```

### Personalização

- Widgets, posição, tamanho por usuário
- Dashboard por perfil (Admin, Fiscal, Vendas, Estoque)
- Drag & Drop com persistência
- Dashboard por empresa (logo, cores, layout próprio)

### Performance

| Métrica | Meta |
|---|---|
| Inicialização | < 500ms |
| Atualização de Widget | < 100ms |
| Reorganização | 60 FPS |
| Lighthouse | ≥ 95 |

---

## 19. JavaScript Services

> *Especificação Técnica completa: `sprints/JAVASCRIPT_SERVICES.md` (39 seções)*

### Objetivo

Camada de infraestrutura que centraliza toda a comunicação com o backend. Nenhum componente visual acessa APIs ou regras de negócio diretamente — tudo passa pelos Services.

### Arquitetura

```
UI Components → Controllers → JavaScript Services → REST API → Python / COBOL → PostgreSQL
```

### Catálogo de Serviços

| Serviço | Função | Status |
|---------|--------|--------|
| HTTP Service | GET, POST, PUT, PATCH, DELETE | ⬜ |
| Auth Service | Login, Logout, Refresh Token, Sessão | ⬜ |
| Authorization | Role, Permission, Feature Flag | ⬜ |
| Storage | Abstrai localStorage, sessionStorage, IndexedDB | ✅ (parcial) |
| Cache Service | TTL, LRU, FIFO | ⬜ |
| Logger | Debug, Info, Warning, Error, Fatal | ✅ (ErrorManager) |
| Notification | Toast, Alert, Banner, Modal, Badge | ✅ (ToastService) |
| Dialog | Confirm, Prompt, Alert, Wizard | ✅ (ModalService) |
| Upload | Fila, Progresso, Cancelamento, Retentativa | ⬜ |
| Download | PDF, Excel, CSV, XML, ZIP | ⬜ |
| Print | PDF, HTML, Etiqueta, Cupom | ⬜ |
| Configuration | Empresa, Usuário, Tema, Idioma | ⬜ |
| i18n | Tradução, Formatação, Datas, Moedas | ✅ (Format) |
| Theme Service | Light, Dark, Glass, Corporate | ✅ (Theme Engine) |
| WebSocket | Notificações, Dashboard, Chat | ⬜ |
| Worker | XML, Processamento, Sincronização | ⬜ |
| Plugin Service | Registrar, Carregar, Desativar | ✅ (PluginManager) |

### Service Registry

Todos os serviços registrados em um único ponto, resolvidos por injeção.

```js
class BaseService {
    initialize() {}
    execute() {}
    destroy() {}
}
```

### Fluxo completo

```
Usuário → Botão Salvar → Form System → Validation Service →
HTTP Service → REST → Python → COBOL → PostgreSQL →
Resposta → Notification Service → Data Grid → Dashboard
```

### Performance

| Métrica | Meta |
|---|---|
| Resolução de serviço | < 2ms |
| Cache Hit | ≥ 80% |
| Resposta média | < 150ms |

---

## 20. Guia do Desenvolvedor

### Objetivo

Orientar desenvolvedores a navegar pelo código, adicionar módulos e estender o FiscalUI.

### Estrutura de diretórios

```
├── index.html              Launchpad + Workspace
├── login.html              Autenticação
├── css/
│   ├── fonts.css           @font-face da Inter
│   ├── variaveis.css       Design tokens
│   ├── reset.css           Reset global
│   ├── icons.css           Classe .icon
│   ├── layout.css          Grid, flex, responsivo
│   ├── grid.css            Sistema de Grid 12 colunas
│   ├── themes.css          Tema Light, High Contrast
│   ├── services.css        Toast, Modal, Loading
│   ├── responsive.css      Mobile First (6 breakpoints)
│   ├── login.css           Estilos do login
│   └── style.css           Componentes
├── js/
│   ├── core/fiscalui.js    Orquestrador do Framework
│   ├── events/EventManager.js     Pub/sub
│   ├── state/StateManager.js      Estado global
│   ├── router/Router.js           Navegação SPA
│   ├── responsive/ResponsiveEngine.js  Breakpoints
│   ├── services/
│   │   ├── ToastService.js
│   │   ├── LoadingService.js
│   │   ├── ModalService.js
│   │   ├── StorageService.js
│   │   └── ErrorManager.js
│   ├── plugins/
│   │   ├── PluginManager.js
│   │   └── ShortcutsPlugin.js
│   ├── utils/
│   │   ├── format.js       Datas, valores, CPF/CNPJ
│   │   └── helpers.js      Debounce, throttle, uuid
│   ├── login.js            Autenticação
│   └── app.js              Inicialização do sistema
├── assets/
│   ├── fonts/              Inter .ttf
│   └── data/menu.json      Navegação
├── img/icons.svg           Sprite SVG
└── sprints/                Documentação
```

### Como adicionar um módulo

1. Adicione o cartão em `index.html` → `.quick-grid`
2. Mapeie em `moduleMap` no `app.js` (card ID → menu ID)
3. Defina título em `moduleTitles`
4. Defina ações da toolbar em `moduleToolbar`
5. Defina colunas em `moduleContent`
6. Adicione a entry no `assets/data/menu.json`

### Ordem de carregamento CSS

```html
<link rel="stylesheet" href="css/fonts.css">
<link rel="stylesheet" href="css/variaveis.css">
<link rel="stylesheet" href="css/reset.css">
<link rel="stylesheet" href="css/icons.css">
<link rel="stylesheet" href="css/layout.css">
<link rel="stylesheet" href="css/grid.css">
<link rel="stylesheet" href="css/style.css">
<link rel="stylesheet" href="css/themes.css">
<link rel="stylesheet" href="css/services.css">
<link rel="stylesheet" href="css/responsive.css">
```

### Ordem de carregamento JavaScript

```html
<!-- Core modules -->
<script src="js/events/EventManager.js"></script>
<script src="js/state/StateManager.js"></script>
<script src="js/services/StorageService.js"></script>
<script src="js/services/ToastService.js"></script>
<script src="js/services/LoadingService.js"></script>
<script src="js/services/ModalService.js"></script>
<script src="js/services/ErrorManager.js"></script>
<script src="js/utils/format.js"></script>
<script src="js/utils/helpers.js"></script>
<script src="js/router/Router.js"></script>
<script src="js/responsive/ResponsiveEngine.js"></script>
<script src="js/plugins/PluginManager.js"></script>
<script src="js/plugins/ShortcutsPlugin.js"></script>
<script src="js/core/fiscalui.js"></script>
<!-- App -->
<script src="js/app.js"></script>
```

### Para executar

```bash
python3 server.py
# Acesse http://localhost:8080
```

---

## 21. Plano Diretor e Roadmap Estratégico

> *Documento completo: `sprints/PLANO_DIRETOR.md` (27 seções)*

### Objetivo

Consolidar a visão de longo prazo do FiscalUI Framework para os próximos 10 anos. Não apenas um roadmap técnico, mas o Plano Diretor que define onde o projeto quer chegar — quem somos, para onde vamos e como mediremos o sucesso.

### Estrutura do Plano Diretor

- **Visão, Missão e Valores** — Propósito e princípios do FiscalUI
- **Objetivos Estratégicos** — Curto, médio e longo prazo
- **Arquitetura Estratégica** — Frontend, SDK, Ferramentas, Ecossistema
- **Roadmap Técnico** — Versões 1.0 a 5.0 (2024–2034)
- **Roadmap de Componentes** — Básicos e Avançados
- **Ecossistema de Produtos** — Core, Components, Icons, Charts, CLI, SDK
- **Marketplace, CLI, SDK, i18n, Mobile, Cloud, Backend, IA**
- **Governança, Qualidade, Versionamento, Documentação, Comunidade, Sustentabilidade**
- **Métricas de Sucesso** — +100 componentes, ≥90% cobertura, WCAG 2.2 AA, Lighthouse ≥ 95

### Próximos passos

O Plano Diretor é um documento vivo. Deve ser revisado anualmente para refletir o progresso real, ajustar prioridades e incorporar novas oportunidades tecnológicas.

---

*FiscalUI Framework RFC — 2026*
