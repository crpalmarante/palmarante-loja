# Visão do Projeto — FiscalBrasil ERP

## Estratégia: duas fases

Construir primeiro o **FiscalUI** (framework visual), depois o **ERP** (negócio em cima dele).
Isola responsabilidades, garante consistência e elimina retrabalho.

---

## Fase 1 — FiscalUI (Framework)

Framework visual completo, sem regra de negócio.
Reutilizável em qualquer sistema, não apenas no ERP.

### Entregas

| Sprint | Foco | Entregáveis |
|--------|------|-------------|
| 01 ✅ | Fundação | HTML semântico, CSS modular, tipografia, ícones SVG, menu.json, autenticação |
| 02 | Navegação | Sidebar retrátil, Topbar com módulos, Toolbar, StatusBar, dark glassmorphism |
| 03 | Dashboard | Cards, Widgets, KPI, Breadcrumb, Search |
| 04 | Componentes | Input, Select, Grid, Modal, Toast, Dialog, Formulários, Tabs, DatePicker |
| 05 | Temas & Refinamento | Light, Dark, Liquid Glass; animações; doc com exemplos |

### Capacidades do FiscalUI

- Sidebar retrátil com módulos
- Topbar com navegação de aplicativos
- Toolbar com ações, busca e alternador de view
- Workspace com painéis glassmorphism
- StatusBar
- Sistema de temas (Light, Dark, Liquid Glass)
- Grid responsivo (12 colunas)
- Componentes reutilizáveis (60+)
- Data Grid com ordenação, filtro, paginação
- Sistema de modais, toasts e notificações
- Validação de formulários
- Documentação com exemplos de uso

---

## Fase 2 — ERP

Sistema de gestão construído sobre o FiscalUI.

### Entregas

| Sprint | Foco | Entregáveis |
|--------|------|-------------|
| 06 | Login + Controle de Acesso | Login, permissões por módulo/aplicativo, sessão |
| 07 | CRUD | Empresas, Clientes, Produtos — criar, editar, listar, excluir |
| 08 | API Python + COBOL | Integração com server.py, execução de COBOL via API |
| 09 | Módulos Fiscais | NF-e, NFC-e, NFS-e, SPED |
| 10 | Relatórios | Vendas, Faturamento, Documentos, Estatísticas |
| 11 | Publicação | Deploy, documentação final, ajustes |

### Módulos do ERP

| Módulo | Aplicativos |
|--------|-------------|
| Dashboard | Home, Indicadores, Metas |
| Empresas | Cadastro, Certificados, CSC, Param. Fiscais |
| Clientes | Cadastro, Contratos, Histórico |
| Produtos | Cadastro, Estoque, Preços, NCM |
| Fiscal | NF-e, NFC-e, NFS-e, CT-e, MDF-e, SPED |
| Vendas | Pedidos, Orçamentos, Faturamento |
| Financeiro | Contas, Boletos, Cobranças |
| RH | Funcionários, Folha, Ponto |
| Relatórios | Vendas, Fiscais, Estatísticos |
| Configurações | Sistema, Usuários, Permissões |

---

## Princípios

1. **Zero dependências externas** — sem Bootstrap, React, jQuery, Tailwind
2. **CSS modular** — cada componente tem seu escopo
3. **ES Modules** — zero globais, imports explícitos
4. **Menu data-driven** — JSON define navegação
5. **Ícones SVG** — sprite próprio, sem font-icons
6. **Temas via CSS variables** — troca instantânea sem JS pesado
7. **Backend opaco** — frontend conhece apenas a API REST, não o COBOL
