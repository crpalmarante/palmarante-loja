-- ══════════════════════════════════════════════════════════════
-- BusinessCore — Party Module
-- v1.0.0
-- ══════════════════════════════════════════════════════════════

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ── Party ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS party (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    party_type      VARCHAR(20) NOT NULL CHECK (party_type IN ('person','company')),
    display_name    VARCHAR(255) NOT NULL,
    given_name      VARCHAR(255) DEFAULT '',
    family_name     VARCHAR(255) DEFAULT '',
    legal_name      VARCHAR(255) DEFAULT '',
    trade_name      VARCHAR(255) DEFAULT '',
    status          VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active','inactive','archived')),
    notes           TEXT DEFAULT '',
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ── Party Role ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS party_role (
    id              SERIAL PRIMARY KEY,
    party_id        UUID NOT NULL REFERENCES party(id) ON DELETE CASCADE,
    role_type       VARCHAR(30) NOT NULL CHECK (role_type IN ('customer','supplier','employee','carrier','bank','vendor','prospect')),
    status          VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active','inactive')),
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_party_role_party ON party_role(party_id);
CREATE UNIQUE INDEX IF NOT EXISTS idx_party_role_unique ON party_role(party_id, role_type);

-- ── Party Document ────────────────────────────────────────
CREATE TABLE IF NOT EXISTS party_document (
    id              SERIAL PRIMARY KEY,
    party_id        UUID NOT NULL REFERENCES party(id) ON DELETE CASCADE,
    doc_type        VARCHAR(30) NOT NULL CHECK (doc_type IN ('cpf','cnpj','rg','ie','im','passport','other')),
    doc_value       VARCHAR(100) NOT NULL,
    issuer          VARCHAR(100) DEFAULT '',
    is_main         BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_party_document_party ON party_document(party_id);
CREATE INDEX IF NOT EXISTS idx_party_document_value ON party_document(doc_value);

-- ── Party Address ────────────────────────────────────────
CREATE TABLE IF NOT EXISTS party_address (
    id              SERIAL PRIMARY KEY,
    party_id        UUID NOT NULL REFERENCES party(id) ON DELETE CASCADE,
    street          VARCHAR(255) DEFAULT '',
    number          VARCHAR(20) DEFAULT '',
    complement      VARCHAR(255) DEFAULT '',
    district        VARCHAR(100) DEFAULT '',
    city            VARCHAR(100) DEFAULT '',
    state           VARCHAR(50) DEFAULT '',
    postal_code     VARCHAR(20) DEFAULT '',
    ibge_code       VARCHAR(10) DEFAULT '',
    country         VARCHAR(50) NOT NULL DEFAULT 'Brasil',
    address_type    VARCHAR(30) NOT NULL DEFAULT 'other' CHECK (address_type IN ('billing','shipping','headquarters','branch','other')),
    is_main         BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_party_address_party ON party_address(party_id);

-- ── Party Contact ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS party_contact (
    id              SERIAL PRIMARY KEY,
    party_id        UUID NOT NULL REFERENCES party(id) ON DELETE CASCADE,
    contact_type    VARCHAR(30) NOT NULL CHECK (contact_type IN ('email','phone','mobile','whatsapp','website','other')),
    contact_value   VARCHAR(255) NOT NULL,
    name            VARCHAR(255) DEFAULT '',
    is_main         BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_party_contact_party ON party_contact(party_id);
