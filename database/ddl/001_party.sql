CREATE TABLE party (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    party_type      VARCHAR(20) NOT NULL CHECK (party_type IN ('person', 'organization')),
    given_name      VARCHAR(100),
    family_name     VARCHAR(100),
    display_name    VARCHAR(200),
    legal_name      VARCHAR(200),
    trade_name      VARCHAR(200),
    status          VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'suspended', 'archived')),
    roles           JSONB NOT NULL DEFAULT '[]',
    version         INTEGER NOT NULL DEFAULT 0,
    created_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE TABLE party_address (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    party_id        UUID NOT NULL REFERENCES party(id) ON DELETE CASCADE,
    street          VARCHAR(100) NOT NULL DEFAULT '',
    number          VARCHAR(20) NOT NULL DEFAULT '',
    complement      VARCHAR(100) DEFAULT '',
    district        VARCHAR(100) DEFAULT '',
    city            VARCHAR(100) NOT NULL DEFAULT '',
    region          VARCHAR(50) DEFAULT '',
    country         VARCHAR(50) NOT NULL DEFAULT 'Brasil',
    postal_code     VARCHAR(20) DEFAULT '',
    address_type    VARCHAR(20) NOT NULL DEFAULT 'main',
    is_main         BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX idx_party_address_party ON party_address(party_id);

CREATE TABLE party_document (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    party_id        UUID NOT NULL REFERENCES party(id) ON DELETE CASCADE,
    doc_type        VARCHAR(20) NOT NULL CHECK (doc_type IN ('cpf', 'cnpj', 'rg', 'ie', 'im', 'passport', 'other')),
    doc_value       VARCHAR(50) NOT NULL,
    is_main         BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE (doc_type, doc_value)
);

CREATE INDEX idx_party_document_value ON party_document(doc_value);
CREATE INDEX idx_party_document_party ON party_document(party_id);

CREATE TABLE party_contact (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    party_id        UUID NOT NULL REFERENCES party(id) ON DELETE CASCADE,
    name            VARCHAR(100) NOT NULL DEFAULT '',
    phone           VARCHAR(30) DEFAULT '',
    email           VARCHAR(200) DEFAULT '',
    contact_role    VARCHAR(100) DEFAULT '',
    contact_type    VARCHAR(20) NOT NULL DEFAULT 'commercial',
    is_main         BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX idx_party_contact_party ON party_contact(party_id);
CREATE INDEX idx_party_contact_email ON party_contact(email);
