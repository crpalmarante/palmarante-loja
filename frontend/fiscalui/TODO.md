# FiscalUI — TODO Geral

## Como ler este arquivo

```
✅ = concluído
⬜ = pendente
🔄 = em andamento
```

---

# FASE 1 — FiscalUI (Interface)

## 1.1 Especificação (RFCs)

**Status:** ✅ Completo — 181 RFCs em 10 níveis

| Nível | RFCs | Status |
|-------|------|--------|
| N1 — Fundação | 19 | ✅ |
| N2 — Basic | 22 | ✅ |
| N3 — Navegação | 14 | ✅ |
| N4 — Formulários | 32 | ✅ |
| N5 — Enterprise | 17 | ✅ |
| N6 — Layouts | 11 | ✅ |
| N7 — Services | 19 | ✅ |
| N8 — Utilities | 17 | ✅ |
| N9 — ERP Business | 15 | ✅ |
| N10 — Developer Platform | 15 | ✅ |

## 1.2 Implementação do Core

| Módulo | Arquivo | Status |
|--------|---------|--------|
| Entry Point | `fiscalui.js` | ✅ |
| EventBus | `core/event-bus/event-bus.js` | ✅ |
| ServiceContainer | `core/di/service-container.js` | ✅ |
| StateManager | `core/state/state-manager.js` | ✅ |
| UIComponent | `core/component/ui-component.js` | ✅ |
| Router | `core/router/router.js` | ✅ |
| Scheduler | `core/scheduler/scheduler.js` | ✅ |
| Registry | `core/registry/registry.js` | ✅ |
| Factory | `core/factory/factory.js` | ✅ |
| DOM Utils | `utils/dom/dom.js` | ✅ |
| package.json | `package.json` | ✅ |

## 1.3 Core — Pendente ⬜

| Módulo | Prioridade | Observação |
|--------|------------|------------|
| CSS Core (reset, variables, utilities) | Alta | Base de estilo |
| Layout Core (workspace, sidebar, topbar) | Alta | Estrutura da tela |
| Theme Engine | Alta | Aplicação de temas |
| Design Tokens (CSS variables) | Alta | Cores, spacing, tipografia |
| Motion Engine | Média | Animações |
| Icon Engine | Média | Sistema de ícones |
| Responsive Engine | Média | Breakpoints |
| Accessibility Engine | Média | Foco, ARIA, teclado |
| Plugin Engine | Baixa | Sistema de plugins |
| Services (http, auth, logger) | Média | Serviços base |
| Format Utils | Média | Formatação BR |
| Mask Utils | Média | Máscaras de input |
| Validation Utils | Média | Validadores BR |

## 1.4 Componentes Visuais — Pendente ⬜

Nenhum componente visual implementado ainda.

Ordem sugerida: Button → Icon Button → Card → Tooltip → Spinner → Modal → Toast → Tabs → Accordion → Input → Select → DataGrid

---

# FASE 2 — BusinessCore (Regras de Negócio)

**Responsabilidade:** decide o que deve acontecer (confirmar venda, aprovar compra, liberar pedido)

## 2.1 Especificação ⬜

| Documento | Status |
|-----------|--------|
| Arquitetura do BusinessCore | ⬜ |
| Contratos de entrada/saída | ⬜ |
| Catálogo de regras de negócio | ⬜ |
| Integração com demais motores | ⬜ |

## 2.2 Módulos ⬜

| Módulo | Descrição |
|--------|-----------|
| Rule Engine | Motor de avaliação de regras (crédito, limite, condições) |
| Order Manager | Gestão de pedidos (venda, compra, transferência) |
| Pricing Engine | Cálculo de preços, descontos, tabelas |
| Credit Analysis | Análise de crédito e limite do cliente |
| Contract Manager | Gestão de contratos comerciais |
| Approval Rules | Regras de alçada e aprovação |
| Event Orchestrator | Orquestração da chamada aos demais motores |

## 2.3 Implementação ⬜

| Etapa | Status |
|-------|--------|
| Estrutura de diretórios | ⬜ |
| Rule Engine (código) | ⬜ |
| Order Manager (código) | ⬜ |
| Event Orchestrator (código) | ⬜ |
| Testes | ⬜ |
| Documentação | ⬜ |

---

# FASE 3 — FiscalCore (Tributação)

**Responsabilidade:** calcula impostos, gera documentos fiscais, SPED Fiscal

## 3.1 Especificação ⬜

| Documento | Status |
|-----------|--------|
| Arquitetura do FiscalCore | ⬜ |
| Contrato de entrada (BusinessCore → FiscalCore) | ⬜ |
| Contrato de saída (FiscalCore → AccountingCore) | ⬜ |
| Tabelas de alíquotas por UF/NCM | ⬜ |
| Mapeamento CST/CSOSN | ⬜ |
| Matriz de regimes tributários | ⬜ |
| Documentação de reforma tributária (IBS/CBS/IS) | ⬜ |

## 3.2 Módulos ⬜

| Módulo | Descrição |
|--------|-----------|
| Tax Calculator | Cálculo de ICMS, PIS, COFINS, IPI, IBS, CBS |
| NCM Engine | Gestão de NCM, CEST, ex-tarifários |
| CST Resolver | Resolução de CST/CSOSN por operação |
| CFOP Resolver | CFOP por operação, UF, regime |
| NFe Engine | Geração e validação de NF-e / NFC-e |
| NFSe Engine | Geração e validação de NFSe |
| MDFe Engine | Geração e validação de MDF-e |
| CT-e Engine | Geração e validação de CT-e |
| SPED Fiscal | Geração de SPED Fiscal |
| SPED PIS/COFINS | Geração de SPED PIS/COFINS |
| SEFAZ Client | Comunicação com SEFAZ (autorização, cancelamento, inutilização) |
| Manifesto Destinatário | Manifesto do destinatário |

## 3.3 Implementação ⬜

| Etapa | Status |
|-------|--------|
| Estrutura de diretórios | ⬜ |
| Tax Calculator (Python/COBOL) | ⬜ |
| NFe Engine (código) | ⬜ |
| SEFAZ Client (código) | ⬜ |
| SPED Fiscal (código) | ⬜ |
| Testes | ⬜ |
| Documentação | ⬜ |

---

# FASE 4 — AccountingCore (Contabilidade)

**Responsabilidade:** gera lançamentos contábeis, plano de contas, balancetes, SPED Contábil

## 4.1 Especificação ⬜

| Documento | Status |
|-----------|--------|
| Arquitetura do AccountingCore | ⬜ |
| Contrato de entrada (FiscalCore → AccountingCore) | ⬜ |
| Plano de Contas REF ( completo ) | ⬜ |
| Mapeamento débito/crédito por operação | ⬜ |
| Centro de custos — estrutura | ⬜ |
| Regras de rateio | ⬜ |
| Cronograma de exercícios | ⬜ |

## 4.2 Módulos ⬜

| Módulo | Descrição |
|--------|-----------|
| Chart of Accounts | Plano de Contas (REF, gerencial, customizado) |
| Double Entry Engine | Motor de partidas dobradas |
| Cost Center Manager | Centro de custos e rateios |
| Journal | Livro Diário |
| Ledger | Livro Razão |
| Trial Balance | Balancete de verificação |
| Balance Sheet | Balanço Patrimonial |
| DRE | Demonstração do Resultado |
| DMPL | Demonstração das Mutações do PL |
| DFC | Demonstração do Fluxo de Caixa |
| Fiscal Year | Exercício, abertura, encerramento |
| SPED ECD | Geração do SPED Contábil |
| SPED ECF | Geração do SPED ECF (contábil-fiscal) |
| Allocation Engine | Rateio automático entre centros |

## 4.3 Implementação ⬜

| Etapa | Status |
|-------|--------|
| Estrutura de diretórios | ⬜ |
| Chart of Accounts (código) | ⬜ |
| Double Entry Engine (código) | ⬜ |
| Trial Balance (código) | ⬜ |
| SPED ECD (código) | ⬜ |
| Testes | ⬜ |
| Documentação | ⬜ |

---

# FASE 5 — WorkflowCore (Processos e Aprovações)

**Responsabilidade:** gerencia estados, aprovações, notificações e ciclo de vida dos processos

## 5.1 Especificação ⬜

| Documento | Status |
|-----------|--------|
| Arquitetura do WorkflowCore | ⬜ |
| Máquina de estados — catálogo | ⬜ |
| Regras de alçada e aprovação | ⬜ |
| Esquema de notificações | ⬜ |
| Contrato com BusinessCore | ⬜ |

## 5.2 Módulos ⬜

| Módulo | Descrição |
|--------|-----------|
| State Machine | Motor de máquina de estados |
| Approval Engine | Motor de aprovações (cascata, paralelo, alçada) |
| Notification Dispatcher | Notificações (email, push, WhatsApp) |
| Deadline Monitor | Prazos, escalonamento, SLA |
| Audit Trail | Histórico de auditoria de cada transição |
| Process Designer | Editor visual de fluxos |

## 5.3 Implementação ⬜

| Etapa | Status |
|-------|--------|
| Estrutura de diretórios | ⬜ |
| State Machine (código) | ⬜ |
| Approval Engine (código) | ⬜ |
| Audit Trail (código) | ⬜ |
| Testes | ⬜ |
| Documentação | ⬜ |

---

# FASE 6 — Infraestrutura Compartilhada

## 6.1 Python API Layer ⬜

| Módulo | Descrição |
|--------|-----------|
| API Gateway | Roteamento para todos os motores |
| Authentication | JWT, OAuth2, SSO |
| Authorization | RBAC, permissões por motor |
| Rate Limiting | Controle de uso |
| Caching | Redis/memória |
| Queue | Filas de processamento assíncrono |

## 6.2 COBOL ⬜

| Módulo | Descrição |
|--------|-----------|
| Regras críticas de tributação | Validação de NF-e, cálculo de impostos |
| Processamento batch | SPED, fechamento contábil |
| Interfaces legadas | Integração com sistemas existentes |

## 6.3 PostgreSQL ⬜

| Item | Descrição |
|------|-----------|
| Schema FiscalCore | Tabelas de tributação, NF-e, SPED |
| Schema AccountingCore | Plano de contas, lançamentos, balancetes |
| Schema BusinessCore | Pedidos, regras, contratos |
| Schema WorkflowCore | Estados, aprovações, auditoria |
| Migrations | Scripts de migração versionados |

---

# FASE 7 — Documentos de Domínio

| Documento | Conteúdo | Status |
|-----------|----------|--------|
| `docs/ARCHITECTURE.md` | Arquitetura geral (4 motores + persistência) | ✅ v3.0 |
| `docs/BC-000_MANIFESTO.md` | Manifesto do BusinessCore (26 artigos) | ✅ |
| `docs/ONTOLOGIA_EMPRESARIAL.md` | Ontologia: significado de cada conceito | ✅ |
| `docs/CANONICAL_MODEL.md` | Modelo Canônico de Negócio | ✅ |
| `docs/PROBLEM.md` | O problema: legislação fiscal brasileira | ✅ |
| `docs/TAX_ENGINE_CONTRACT.md` | Contrato API do motor fiscal | ✅ |
| `docs/TAX_RULES_MATRIX.md` | Matriz de decisão tributária | ✅ |
| `docs/TAX_REFORM.md` | Reforma tributária (IBS/CBS/IS) | ✅ |
| `docs/TAX_DOCUMENTS.md` | Ecossistema de documentos fiscais | ✅ |
| `docs/TAX_PARAMETERIZATION.md` | Parametrização e manutenção | ✅ |
| `docs/BUSINESS_CORE.md` | Arquitetura do BusinessCore | ⬜ |
| `docs/ACCOUNTING_CORE.md` | Arquitetura do AccountingCore | ⬜ |
| `docs/WORKFLOW_CORE.md` | Arquitetura do WorkflowCore | ⬜ |
| `docs/CONTRATOS.md` | Contratos entre motores | ⬜ |

# BusinessCore — Roadmap

| BC | Documento | Arquivo | Status |
|----|-----------|---------|--------|
| BC-000 | Manifesto do BusinessCore | `docs/BC-000_MANIFESTO.md` | ✅ |
| BC-001 | Ontologia Empresarial | `docs/ONTOLOGIA_EMPRESARIAL.md` | ✅ |
| BC-002 | Modelo Canônico | `docs/BC-002_MODELO_CANONICO.md` | ✅ |
| BC-003 | Entidades Fundamentais | `docs/BC-003_ENTIDADES.md` | ✅ |
| BC-003A | Catálogo Universal de Papéis | `docs/BC-003A_ROLE_MODEL.md` | ✅ |
| BC-004 | Value Objects | `docs/BC-004_VALUE_OBJECTS.md` | ✅ |
| BC-004A | Tipos de Dados de Negócio | `docs/BC-004A_DATA_TYPES.md` | ✅ |
| BC-005 | Agregados | `docs/BC-005_AGGREGATES.md` | ✅ |
| BC-005A | Invariantes e Políticas | `docs/BC-005A_INVARIANTS_POLICIES.md` | ✅ |
| BC-005B | Capacidades Empresariais | `docs/BC-005B_BUSINESS_CAPABILITIES.md` | ✅ |
| BC-005C | Value Streams | `docs/BC-005C_VALUE_STREAMS.md` | ✅ |
| BC-006 | Domain Events | `docs/BC-006_DOMAIN_EVENTS.md` | ✅ |
| BC-006A | Contrato Universal de Mensagens | `docs/BC-006A_MESSAGE_CONTRACT.md` | ✅ |
| BC-006B | Protocolo Universal | `docs/BC-006B_UNIVERSAL_PROTOCOL.md` | ✅ |
| BC-006C | Barramento de Serviços | `docs/BC-006C_SERVICE_BUS.md` | ✅ |
| BC-007 | Business Commands | — | ⬜ |
| BC-008 | Use Cases | — | ⬜ |
| BC-009 | Domain Services | — | ⬜ |
| BC-010 | State Machines | — | ⬜ |
| BC-011 | Event Store | — | ⬜ |
| BC-012 | CQRS | — | ⬜ |
| BC-013 | Event Sourcing | — | ⬜ |
| BC-014 | Saga Pattern | — | ⬜ |
| BC-015 | Business Process Engine | — | ⬜ |

---

# Implementação por Nível de Maturidade

A arquitetura conceitual completa (BC-000 a BC-006C, 15 documentos) está documentada como visão.
A implementação segue 3 níveis. **N1 é o foco agora.**

## N1 — MVP (agora)

| O quê | Como | Status |
|-------|------|--------|
| BusinessCore (entidades, VOs, agregados, regras) | Python + COBOL | ⬜ |
| Dispatcher interno (Mediator) | ~10 classes Python | ⬜ |
| Event Log | Tabela `event_log` PostgreSQL | ⬜ |
| Controllers → Use Cases → Core → Repositories | Python FastAPI | ⬜ |
| FiscalCore (impostos, NF-e, SPED) | Python + COBOL | ⬜ |
| AccountingCore (partidas, balancete) | Python | ⬜ |
| WorkflowCore (estados, aprovações) | Python | ⬜ |
| Segurança (auth, RBAC) | Python | ⬜ |
| Componentes visuais FiscalUI | HTML/CSS/JS | ⬜ |

## N2 — Plataforma (próximo ciclo)

| O quê | Quando |
|-------|--------|
| Filas de processamento (SPED, fechamento) | Demanda de tarefas pesadas |
| Cache (Redis) | >100 usuários simultâneos |
| APIs públicas versionadas | Integrações externas |
| Observabilidade (OpenTelemetry) | Múltiplos servidores |
| Sistema de plugins | Marketplace |

## N3 — Enterprise (futuro)

| O quê | Quando |
|-------|--------|
| Kafka / Event Streaming | Alta throughput |
| CQRS / Event Sourcing | Reconstrução de estado |
| Saga Pattern | Transações distribuídas |
| Service Bus / Registry / Discovery | Escalabilidade horizontal |
| Microsserviços | Time >10 pessoas |

---

**Última atualização:** 2026-07-25

