CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS organization (
    party_id    UUID PRIMARY KEY REFERENCES party(id) ON DELETE CASCADE,
    legal_name  VARCHAR(255) NOT NULL,
    trade_name  VARCHAR(255),
    cnpj        VARCHAR(14),
    ie          VARCHAR(20),
    im          VARCHAR(20),
    crt         VARCHAR(20) NOT NULL DEFAULT 'regime_normal',
    cnae        VARCHAR(10),
    tax_regime  VARCHAR(30) NOT NULL DEFAULT 'lucro_presumido',
    active      BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS branch (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organization(party_id) ON DELETE CASCADE,
    party_id        UUID NOT NULL REFERENCES party(id) ON DELETE CASCADE,
    code            VARCHAR(20),
    name            VARCHAR(255),
    cnpj            VARCHAR(14),
    ie              VARCHAR(20),
    phone           VARCHAR(20),
    email           VARCHAR(255),
    active          BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_org_cnpj ON organization(cnpj);
CREATE INDEX idx_branch_org ON branch(organization_id);
