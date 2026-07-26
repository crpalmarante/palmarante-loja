-- Inventory Platform v2.0
-- Stock Ledger como fonte da verdade.
-- Saldos são calculados a partir das movimentações.

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ── Stock Ledger (Razão de Estoque) ─────────────────────────
-- Única fonte da verdade. Saldo é sempre calculado.
CREATE TABLE IF NOT EXISTS stock_movement (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    item_id         UUID NOT NULL REFERENCES item(id) ON DELETE CASCADE,
    warehouse_id    UUID NOT NULL REFERENCES warehouse(id) ON DELETE CASCADE,
    movement_type   VARCHAR(20) NOT NULL,
    quantity        DECIMAL(15,4) NOT NULL,
    location_id     UUID REFERENCES inventory_location(id),
    lot_id          UUID REFERENCES lot(id),
    serial_number   VARCHAR(100),
    reference_type  VARCHAR(50),
    reference_id    UUID,
    document_number VARCHAR(100),
    unit_cost       DECIMAL(15,4) NOT NULL DEFAULT 0,
    notes           TEXT,
    created_by      VARCHAR(255),
    status          VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    confirmed_at    TIMESTAMP
);

-- ── Locations (Estrutura Hierárquica) ───────────────────────
CREATE TABLE IF NOT EXISTS inventory_location (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    warehouse_id    UUID NOT NULL REFERENCES warehouse(id) ON DELETE CASCADE,
    code            VARCHAR(100) NOT NULL,
    name            VARCHAR(255),
    parent_id       UUID REFERENCES inventory_location(id) ON DELETE SET NULL,
    type            VARCHAR(20) NOT NULL DEFAULT 'rack',
    active          BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(warehouse_id, code)
);

-- ── Lots ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS lot (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    item_id             UUID NOT NULL REFERENCES item(id) ON DELETE CASCADE,
    warehouse_id        UUID NOT NULL REFERENCES warehouse(id) ON DELETE CASCADE,
    lot_number          VARCHAR(100) NOT NULL,
    supplier_lot        VARCHAR(100),
    manufacturing_date  DATE,
    expiry_date         DATE,
    origin              VARCHAR(100),
    status              VARCHAR(20) NOT NULL DEFAULT 'active',
    notes               TEXT,
    created_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ── Serial Numbers ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS serial_number (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    item_id         UUID NOT NULL REFERENCES item(id) ON DELETE CASCADE,
    warehouse_id    UUID NOT NULL REFERENCES warehouse(id) ON DELETE CASCADE,
    serial          VARCHAR(100) NOT NULL UNIQUE,
    lot_id          UUID REFERENCES lot(id),
    location_id     UUID REFERENCES inventory_location(id),
    status          VARCHAR(20) NOT NULL DEFAULT 'available',
    notes           TEXT,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ── Reservations ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS reservation (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    item_id         UUID NOT NULL REFERENCES item(id) ON DELETE CASCADE,
    warehouse_id    UUID NOT NULL REFERENCES warehouse(id) ON DELETE CASCADE,
    quantity        DECIMAL(15,4) NOT NULL,
    order_type      VARCHAR(50),
    order_id        UUID,
    location_id     UUID REFERENCES inventory_location(id),
    lot_id          UUID REFERENCES lot(id),
    status          VARCHAR(20) NOT NULL DEFAULT 'active',
    notes           TEXT,
    created_by      VARCHAR(255),
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    expires_at      TIMESTAMP
);

-- ── Transfer Orders ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS transfer_order (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    from_warehouse_id   UUID NOT NULL REFERENCES warehouse(id),
    to_warehouse_id     UUID NOT NULL REFERENCES warehouse(id),
    notes               TEXT,
    status              VARCHAR(20) NOT NULL DEFAULT 'draft',
    created_by          VARCHAR(255),
    created_at          TIMESTAMP NOT NULL DEFAULT NOW(),
    sent_at             TIMESTAMP,
    received_at         TIMESTAMP,
    completed_at        TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transfer_order_item (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    transfer_id     UUID NOT NULL REFERENCES transfer_order(id) ON DELETE CASCADE,
    item_id         UUID NOT NULL REFERENCES item(id),
    quantity        DECIMAL(15,4) NOT NULL,
    lot_id          UUID REFERENCES lot(id),
    unit_cost       DECIMAL(15,4) NOT NULL DEFAULT 0
);

-- ── Inventory Counts ────────────────────────────────────────
CREATE TABLE IF NOT EXISTS inventory_count (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    warehouse_id    UUID NOT NULL REFERENCES warehouse(id) ON DELETE CASCADE,
    status          VARCHAR(20) NOT NULL DEFAULT 'draft',
    counted_by      VARCHAR(255),
    notes           TEXT,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at    TIMESTAMP
);

CREATE TABLE IF NOT EXISTS inventory_count_line (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    count_id            UUID NOT NULL REFERENCES inventory_count(id) ON DELETE CASCADE,
    item_id             UUID NOT NULL REFERENCES item(id),
    expected_quantity   DECIMAL(15,4) NOT NULL DEFAULT 0,
    actual_quantity     DECIMAL(15,4) NOT NULL DEFAULT 0,
    location_id         UUID REFERENCES inventory_location(id),
    lot_id              UUID REFERENCES lot(id),
    notes               TEXT
);

-- ── Índices ─────────────────────────────────────────────────
CREATE INDEX idx_movement_item ON stock_movement(item_id);
CREATE INDEX idx_movement_warehouse ON stock_movement(warehouse_id);
CREATE INDEX idx_movement_type ON stock_movement(movement_type);
CREATE INDEX idx_movement_reference ON stock_movement(reference_type, reference_id);
CREATE INDEX idx_movement_created ON stock_movement(created_at DESC);
CREATE INDEX idx_location_warehouse ON inventory_location(warehouse_id);
CREATE INDEX idx_lot_item ON lot(item_id);
CREATE INDEX idx_lot_expiry ON lot(expiry_date);
CREATE INDEX idx_serial_item ON serial_number(item_id);
CREATE INDEX idx_serial_status ON serial_number(status);
CREATE INDEX idx_reservation_item ON reservation(item_id);
CREATE INDEX idx_reservation_order ON reservation(order_type, order_id);
CREATE INDEX idx_reservation_status ON reservation(status);
CREATE INDEX idx_transfer_from ON transfer_order(from_warehouse_id);
CREATE INDEX idx_transfer_to ON transfer_order(to_warehouse_id);
CREATE INDEX idx_transfer_status ON transfer_order(status);
