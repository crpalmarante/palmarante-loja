# Layout Engine

## Conceito

O Layout Engine é o núcleo estrutural do FiscalUI.

Sua responsabilidade é organizar todos os componentes da interface de maneira consistente, responsiva e reutilizável.

Nenhuma tela do sistema deverá criar um layout próprio.

Todas as páginas serão montadas utilizando a estrutura definida pelo Layout Engine.

---

# Objetivos

O Layout Engine foi projetado para:

- Garantir consistência visual.
- Facilitar a criação de novas telas.
- Reduzir código duplicado.
- Melhorar a experiência do usuário.
- Adaptar automaticamente a interface para diferentes dispositivos.

---

# Estrutura Geral

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ TopBar                                                                      │
├──────────────┬──────────────────────────────────────────────────────────────┤
│              │                                                              │
│ Sidebar      │ Workspace                                                    │
│              │                                                              │
│              │  Header                                                      │
│              │──────────────────────────────────────────────────────────────│
│              │ Toolbar                                                      │
│              │──────────────────────────────────────────────────────────────│
│              │ Filters                                                      │
│              │──────────────────────────────────────────────────────────────│
│              │                                                              │
│              │                Conteúdo                                      │
│              │                                                              │
│              │──────────────────────────────────────────────────────────────│
│              │ Status Bar                                                   │
└──────────────┴──────────────────────────────────────────────────────────────┘
```

---

# Hierarquia

```text
Application

│

├── TopBar

├── Sidebar

└── Workspace

      │

      ├── Header

      ├── Toolbar

      ├── Filters

      ├── Content

      └── Status Bar
```

---

# TopBar

A TopBar representa a navegação global.

Ela permanece fixa durante toda a sessão.

Contém:

- Logo
- Nome da empresa
- Pesquisa global
- Notificações
- Usuário
- Tema
- Menu de aplicativos

Nunca muda entre módulos.

---

# Sidebar

A Sidebar representa a navegação do módulo.

Características:

- recolhível
- expansível
- suporte a submenus
- favoritos
- recentes

No modo mobile ela se transforma em Drawer.

---

# Workspace

Representa a área de trabalho.

É composto por cinco regiões.

```text
Workspace

│

├── Header

├── Toolbar

├── Filters

├── Content

└── Status Bar
```

Cada região possui uma responsabilidade única.

---

# Header

Apresenta o contexto da tela.

Exibe:

- título
- descrição
- breadcrumb
- indicadores

Nunca possui botões de ação.

---

# Toolbar

Concentra todas as ações da tela.

Exemplos:

- Novo
- Salvar
- Editar
- Excluir
- Importar
- Exportar
- Atualizar

Toda ação pertence à Toolbar.

---

# Filters

Área destinada exclusivamente aos filtros.

Pode conter:

- Pesquisa
- Datas
- Empresas
- Status
- Usuários
- Combos

Os filtros nunca ficam misturados com a Toolbar.

---

# Content

Área principal.

Pode conter:

- Tabelas
- Cards
- Dashboards
- Kanban
- Calendários
- Formulários
- Relatórios
- Gráficos

O Layout Engine não impõe qual componente será utilizado.

---

# Status Bar

Área inferior.

Responsável por apresentar:

- mensagens
- usuário
- empresa
- ambiente
- versão
- data/hora

---

# Responsividade

Desktop

```text
Sidebar fixa

Workspace completo
```

Tablet

```text
Sidebar reduzida

Workspace expandido
```

Mobile

```text
Sidebar Drawer

Workspace ocupa toda a tela
```

---

# Regras do Layout Engine

1. Toda página possui TopBar.

2. Toda página possui Workspace.

3. Nenhuma página altera a estrutura principal.

4. Apenas o conteúdo do Workspace muda.

5. Os componentes nunca controlam o layout.

6. O Layout Engine controla toda a composição da interface.

---

# Benefícios

- Consistência entre módulos.
- Facilidade de manutenção.
- Responsividade centralizada.
- Desenvolvimento acelerado.
- Baixo acoplamento.
- Reutilização máxima.

---

# Princípio

O Layout Engine é responsável pela estrutura.

Os componentes são responsáveis pelo conteúdo.

Essa separação garante que o FiscalUI permaneça organizado, escalável e preparado para suportar centenas de telas sem perda de consistência.
