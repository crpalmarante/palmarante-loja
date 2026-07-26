CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS category (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name        VARCHAR(255) NOT NULL,
    parent_id   UUID REFERENCES category(id) ON DELETE SET NULL,
    code        VARCHAR(50),
    description TEXT,
    active      BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS brand (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name        VARCHAR(255) NOT NULL,
    code        VARCHAR(50),
    description TEXT,
    active      BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS manufacturer (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name        VARCHAR(255) NOT NULL,
    cnpj        VARCHAR(14),
    code        VARCHAR(50),
    active      BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS unit (
    code        VARCHAR(10) PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    type        VARCHAR(20) NOT NULL DEFAULT 'units',
    active      BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS unit_conversion (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    from_code   VARCHAR(10) NOT NULL REFERENCES unit(code),
    to_code     VARCHAR(10) NOT NULL REFERENCES unit(code),
    factor      DECIMAL(15,6) NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS attribute (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name        VARCHAR(255) NOT NULL,
    code        VARCHAR(50),
    type        VARCHAR(20) NOT NULL DEFAULT 'text',
    required    BOOLEAN NOT NULL DEFAULT FALSE,
    active      BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS attribute_value (
    id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    attribute_id  UUID NOT NULL REFERENCES attribute(id) ON DELETE CASCADE,
    value         VARCHAR(255) NOT NULL,
    code          VARCHAR(50),
    sort_order    INT NOT NULL DEFAULT 0,
    created_at    TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS variant (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    item_id         UUID NOT NULL REFERENCES item(id) ON DELETE CASCADE,
    sku             VARCHAR(50),
    name            VARCHAR(255),
    attribute_values JSONB,
    active          BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_category_parent ON category(parent_id);
CREATE INDEX idx_variant_item ON variant(item_id);
CREATE INDEX idx_attr_value_attr ON attribute_value(attribute_id);
