CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS warehouse (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name        VARCHAR(255) NOT NULL,
    code        VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    address     TEXT,
    responsible VARCHAR(255),
    active      BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS stock_item (
    id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    warehouse_id  UUID NOT NULL REFERENCES warehouse(id) ON DELETE CASCADE,
    item_id       UUID NOT NULL REFERENCES item(id) ON DELETE CASCADE,
    quantity      DECIMAL(15,4) NOT NULL DEFAULT 0,
    reserved      DECIMAL(15,4) NOT NULL DEFAULT 0,
    min_stock     DECIMAL(15,4) NOT NULL DEFAULT 0,
    max_stock     DECIMAL(15,4) NOT NULL DEFAULT 0,
    location      VARCHAR(100),
    created_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(warehouse_id, item_id)
);

CREATE TABLE IF NOT EXISTS stock_movement (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    item_id             UUID NOT NULL REFERENCES item(id) ON DELETE CASCADE,
    warehouse_id        UUID NOT NULL REFERENCES warehouse(id) ON DELETE CASCADE,
    movement_type       VARCHAR(20) NOT NULL,
    quantity            DECIMAL(15,4) NOT NULL,
    reference_type      VARCHAR(50),
    reference_id        UUID,
    notes               TEXT,
    status              VARCHAR(20) NOT NULL DEFAULT 'pending',
    target_warehouse_id UUID REFERENCES warehouse(id),
    created_at          TIMESTAMP NOT NULL DEFAULT NOW(),
    confirmed_at        TIMESTAMP
);

CREATE TABLE IF NOT EXISTS inventory_count (
    id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    warehouse_id      UUID NOT NULL REFERENCES warehouse(id) ON DELETE CASCADE,
    item_id           UUID NOT NULL REFERENCES item(id) ON DELETE CASCADE,
    expected_quantity DECIMAL(15,4) NOT NULL DEFAULT 0,
    actual_quantity   DECIMAL(15,4) NOT NULL DEFAULT 0,
    counted_by        VARCHAR(255),
    notes             TEXT,
    counted_at        TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_stock_warehouse ON stock_item(warehouse_id);
CREATE INDEX idx_stock_item ON stock_item(item_id);
CREATE INDEX idx_movement_warehouse ON stock_movement(warehouse_id);
CREATE INDEX idx_movement_item ON stock_movement(item_id);
CREATE INDEX idx_count_warehouse ON inventory_count(warehouse_id);
