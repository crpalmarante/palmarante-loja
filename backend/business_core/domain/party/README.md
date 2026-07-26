# Business Platform — Party Module

- [x] Backend: Party entity + VOs (PersonName, Address, Document, Phone, Email)
- [x] Backend: PartyRole, PartyAddress, PartyContact, PartyDocument
- [x] Backend: Party aggregate com eventos
- [x] Backend: Commands + Use Cases (CRUD)
- [x] Backend: IPartyRepository interface
- [x] Database: DDL (001_party.sql)
- [x] Frontend: Página party.html (lista + formulário + detalhe)
- [x] Backend: Servidor dev (party_server.py — in-memory)

## Arquivos

```
backend/business_core/domain/party/
├── party.py              ← aggregate raiz
├── person_name.py        ← PersonName, CompanyName (VOs)
├── address.py            ← Address (VO)
├── document.py           ← Document, DocumentType (VO)
├── phone_email.py        ← Phone, Email (VOs)
├── party_role.py         ← PartyRole (VO)
├── party_address.py      ← PartyAddress (VO)
├── party_contact.py      ← PartyContact (VO)
└── party_document.py     ← PartyDocument (VO)

backend/business_core/commands/party/
└── party_commands.py     ← CreateParty, UpdateParty, etc.

backend/business_core/use_cases/party/
└── party_use_cases.py    ← CreatePartyUseCase, etc.

backend/business_core/repositories/interfaces/
└── iparty_repository.py  ← IPartyRepository

backend/api/
└── party_server.py       ← Servidor HTTP + rotas REST

database/ddl/
└── 001_party.sql         ← Schema PostgreSQL

frontend/pages/
└── party.html            ← UI completa (tabela + modal + abas)
```

## Como executar

```bash
cd backend/api
python3 party_server.py
# → http://localhost:8081/pages/party.html
```
