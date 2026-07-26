CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS product (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name            VARCHAR(255) NOT NULL,
    product_type    VARCHAR(20) NOT NULL DEFAULT 'product',
    sku             VARCHAR(50) UNIQUE,
    ncm             VARCHAR(8),
    ean             VARCHAR(13) UNIQUE,
    unit            VARCHAR(10) NOT NULL DEFAULT 'unit',
    cost_price      DECIMAL(15,2) NOT NULL DEFAULT 0,
    sale_price      DECIMAL(15,2) NOT NULL DEFAULT 0,
    category        VARCHAR(255),
    supplier_id     UUID REFERENCES party(id) ON DELETE SET NULL,
    notes           TEXT,
    status          VARCHAR(20) NOT NULL DEFAULT 'active',
    stock           DECIMAL(15,3) NOT NULL DEFAULT 0,
    min_stock       DECIMAL(15,3) NOT NULL DEFAULT 0,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_product_name ON product(name);
CREATE INDEX idx_product_status ON product(status);
CREATE INDEX idx_product_category ON product(category);
CREATE INDEX idx_product_supplier ON product(supplier_id);
