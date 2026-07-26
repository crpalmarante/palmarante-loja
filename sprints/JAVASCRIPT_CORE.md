# Capítulo 11 — JavaScript Core

## Conceito

O JavaScript Core é o núcleo comportamental do FiscalUI.

Sua responsabilidade é controlar toda a interação da interface, mantendo os componentes independentes, reutilizáveis e desacoplados das regras de negócio.

O JavaScript Core não conhece:

- Banco de Dados
- COBOL
- Python
- PostgreSQL
- APIs de negócio

Ele conhece apenas a interface.

---

# Filosofia

O HTML representa a estrutura.

O CSS representa a aparência.

O JavaScript representa o comportamento.

```text
HTML
 ↓
Estrutura

CSS
 ↓
Aparência

JavaScript
 ↓
Comportamento
```

Cada camada possui uma responsabilidade única.

---

# Objetivos

O JavaScript Core possui os seguintes objetivos:

- Controlar componentes.
- Gerenciar eventos.
- Organizar módulos.
- Controlar navegação.
- Gerenciar estado visual.
- Facilitar extensões.
- Não depender de frameworks externos.

---

# Arquitetura

```text
JavaScript Core

│

├── Core

├── Router

├── Events

├── State

├── Components

├── Services

├── Plugins

└── Utilities
```

---

# Core

O Core inicializa todo o Framework.

Responsabilidades:

- iniciar aplicação
- registrar componentes
- carregar tema
- configurar idioma
- carregar preferências
- iniciar Router
- iniciar Plugins

---

# Router

Controla a navegação entre módulos.

```text
Launchpad

↓

Dashboard

↓

NF-e

↓

Produtos

↓

Clientes

↓

Relatórios
```

O Router não depende do servidor.

A navegação pode ocorrer sem recarregar toda a página.

---

# Event Manager

Todo componente comunica-se através de eventos.

Nunca diretamente.

```text
Button

↓

Evento

↓

Event Manager

↓

Tabela

↓

Atualização
```

Exemplo

```text
button.save

↓

document.save

↓

toast.success

↓

table.refresh
```

---

# State Manager

Responsável pelo estado da interface.

Exemplos

```text
Tema Atual

Sidebar Aberta

Empresa Ativa

Usuário

Idioma

Filtros

Página Atual

Workspace Atual
```

Não armazena regras de negócio.

---

# Component Manager

Controla o ciclo de vida dos componentes.

```text
Criar

↓

Inicializar

↓

Renderizar

↓

Atualizar

↓

Destruir
```

Todos os componentes seguem esse ciclo.

---

# Services

Serviços reutilizáveis.

```text
Toast

Dialog

Modal

Loading

Notification

Storage

Clipboard

Download

Upload

Print
```

---

# Plugin Manager

Permite adicionar funcionalidades.

```text
FiscalUI

↓

Plugin

↓

Registro

↓

Inicialização

↓

Disponível
```

Exemplo

```text
QRCode Plugin

Charts Plugin

Maps Plugin

Editor Plugin
```

---

# Utilities

Funções auxiliares.

```text
Formatar Datas

Formatar Valores

Debounce

Throttle

UUID

Parser

Validador

Conversores
```

---

# Comunicação

Todos os módulos comunicam-se através do Event Manager.

Nunca diretamente.

Errado

```text
Button

↓

Tabela
```

Correto

```text
Button

↓
Evento

↓

Event Manager

↓

Tabela
```

---

# Organização

```text
js/

core/

router/

events/

state/

services/

plugins/

components/

utils/
```

Cada pasta possui responsabilidade única.

---

# Ciclo de Vida

```text
Página

↓

Carregar

↓

Criar Componentes

↓

Registrar Eventos

↓

Renderizar

↓

Interação

↓

Atualização

↓

Destruição
```

---

# Responsabilidades

O JavaScript Core controla:

- Sidebar
- Menus
- Tabs
- Modais
- Toasts
- Tema
- Atalhos
- Tooltips
- Dropdowns
- Accordions
- Paginação
- Seleção
- Pesquisa
- Loading

---

Não controla:

- SQL
- PostgreSQL
- Python
- COBOL
- Regras fiscais
- Regras tributárias
- Autorização SEFAZ

Essas responsabilidades pertencem ao Backend.

---

# Comunicação com Backend

```text
Interface

↓

Service

↓

API REST

↓

Python

↓

COBOL

↓

PostgreSQL
```

O JavaScript nunca acessa o banco diretamente.

---

# Comunicação Assíncrona

Todo acesso ao Backend ocorre de forma assíncrona.

```text
Usuário

↓

Clique

↓

Loading

↓

API

↓

Resposta

↓

Atualização da Interface
```

---

# Tratamento de Erros

Todo erro passa pelo Error Manager.

```text
Erro

↓

Logger

↓

Notificação

↓

Recuperação
```

Nunca utilizar:

```javascript
alert("Erro")
```

---

# Performance

O Core deve:

- reutilizar componentes
- evitar renderizações desnecessárias
- utilizar Lazy Loading
- utilizar Event Delegation
- minimizar consumo de memória

---

# Segurança

O JavaScript nunca deve:

- armazenar senhas
- armazenar tokens inseguros
- executar código remoto
- confiar em validações do navegador

Toda validação definitiva pertence ao Backend.

---

# Benefícios

- Código modular
- Fácil manutenção
- Componentes independentes
- Alta performance
- Escalabilidade
- Facilidade de testes
- Integração simples com APIs

---

# Princípio

O JavaScript Core controla apenas a experiência da interface.

Toda regra de negócio permanece no Backend.

Essa separação garante que o FiscalUI possa ser utilizado com qualquer tecnologia de servidor, incluindo Python, COBOL, Java, C#, Node.js ou Go.
