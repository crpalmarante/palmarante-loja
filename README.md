# FiscalBrasil ERP

ERP brasileiro moderno com arquitetura limpa: frontend HTML/CSS/JS, backend Python + COBOL, PostgreSQL.

## Estrutura

```
├── frontend/          # Interface do usuário
│   ├── fiscalui/      # Framework de componentes JS (vanilla)
│   ├── assets/        # CSS, JS, imagens, fontes
│   ├── pages/         # Páginas HTML
│   ├── components/    # Componentes reutilizáveis
│   └── layouts/       # Layouts de tela
│
├── backend/           # Lógica de negócio e API
│   ├── business_core/ # Regras de negócio (entidades, agregados, use cases)
│   ├── fiscal_core/   # Tributação (NCM, CST, NF-e, SPED)
│   ├── accounting_core/ # Contabilidade (partidas, balancete, DRE)
│   ├── workflow_core/ # Aprovações e máquina de estados
│   ├── infrastructure/ # Persistência (PostgreSQL, COBOL adapters)
│   └── api/           # REST API (FastAPI)
│
├── cobol/             # Programas COBOL
│   ├── programs/      # Código-fonte .cbl
│   ├── copybooks/     # Copybooks padronizados
│   └── services/      # Serviços COBOL
│
├── database/          # Schema e migrações
│   ├── ddl/           # Definições de tabelas
│   ├── migrations/    # Migrações versionadas
│   ├── views/         # Views e materializadas
│   ├── procedures/    # Stored procedures
│   └── seeds/         # Dados iniciais
│
├── docs/              # Documentação de arquitetura
└── scripts/           # Scripts de deploy e utilidades
```

## Níveis de Maturidade

| Nível | Foco | Status |
|-------|------|--------|
| N1 — MVP | BusinessCore + Dispatcher interno + Event Log | Em desenvolvimento |
| N2 — Plataforma | Filas, cache, APIs públicas, plugins | Futuro |
| N3 — Enterprise | Microsserviços, CQRS, Event Sourcing, Kafka | Futuro |

## Como executar (dev)

```bash
cd backend
python -m api.server
```

Acessar: `http://localhost:8080`

## Documentação

- [Arquitetura](docs/ARCHITECTURE.md)
- [Manifesto do BusinessCore](docs/BC-000_MANIFESTO.md)
- [Roadmap de Implementação](docs/IMPLEMENTATION_ROADMAP.md)
