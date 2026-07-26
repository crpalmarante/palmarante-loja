CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS item (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name        VARCHAR(255) NOT NULL,
    item_type   VARCHAR(30) NOT NULL DEFAULT 'product',
    sku         VARCHAR(50) UNIQUE,
    ncm         VARCHAR(8),
    cest        VARCHAR(9),
    ean         VARCHAR(13) UNIQUE,
    gtin        VARCHAR(14),
    unit        VARCHAR(10) NOT NULL DEFAULT 'unit',
    cost_price  DECIMAL(15,2) NOT NULL DEFAULT 0,
    sale_price  DECIMAL(15,2) NOT NULL DEFAULT 0,
    category_id UUID,
    supplier_id UUID REFERENCES party(id) ON DELETE SET NULL,
    brand       VARCHAR(255),
    notes       TEXT,
    status      VARCHAR(20) NOT NULL DEFAULT 'active',
    stock       DECIMAL(15,3) NOT NULL DEFAULT 0,
    min_stock   DECIMAL(15,3) NOT NULL DEFAULT 0,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS item_barcode (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    item_id     UUID NOT NULL REFERENCES item(id) ON DELETE CASCADE,
    code        VARCHAR(50) NOT NULL,
    type        VARCHAR(20) NOT NULL DEFAULT 'ean13',
    is_main     BOOLEAN NOT NULL DEFAULT FALSE,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS item_variant (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    item_id     UUID NOT NULL REFERENCES item(id) ON DELETE CASCADE,
    name        VARCHAR(255) NOT NULL,
    sku         VARCHAR(50),
    sale_price  DECIMAL(15,2) NOT NULL DEFAULT 0,
    cost_price  DECIMAL(15,2) NOT NULL DEFAULT 0,
    stock       DECIMAL(15,3) NOT NULL DEFAULT 0,
    active      BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS price_history (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    item_id     UUID NOT NULL REFERENCES item(id) ON DELETE CASCADE,
    cost_price  DECIMAL(15,2) NOT NULL,
    sale_price  DECIMAL(15,2) NOT NULL,
    reason      VARCHAR(255),
    changed_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_item_type ON item(item_type);
CREATE INDEX idx_item_status ON item(status);
CREATE INDEX idx_item_sku ON item(sku);
CREATE INDEX idx_item_supplier ON item(supplier_id);
CREATE INDEX idx_barcode_item ON item_barcode(item_id);
CREATE INDEX idx_variant_item ON item_variant(item_id);
CREATE INDEX idx_price_item ON price_history(item_id);
