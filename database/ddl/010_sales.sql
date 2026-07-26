-- Sales Platform
-- These tables complement business_document with sales-specific data.
-- The generic document lives in business_documents (009_document.sql).

-- Sales Orders (complemento do business_document)
CREATE TABLE IF NOT EXISTS sales_order (
    id              VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    document_id     VARCHAR(36) NOT NULL REFERENCES business_documents(id) ON DELETE CASCADE,
    document_number VARCHAR(100) DEFAULT '',
    document_type   VARCHAR(30) DEFAULT 'sale_order',
    customer_id     VARCHAR(36) NOT NULL,
    customer_name   VARCHAR(255) DEFAULT '',
    sales_rep_id    VARCHAR(36) DEFAULT '',
    sales_rep_name  VARCHAR(255) DEFAULT '',
    rep_commission  DECIMAL(18,4) DEFAULT 0,
    payment_method  VARCHAR(30) DEFAULT 'pix',
    installments    INTEGER DEFAULT 1,
    due_days        INTEGER DEFAULT 30,
    status          VARCHAR(30) DEFAULT 'draft',
    subtotal        DECIMAL(18,4) DEFAULT 0,
    discount_total  DECIMAL(18,4) DEFAULT 0,
    tax_total       DECIMAL(18,4) DEFAULT 0,
    freight         DECIMAL(18,4) DEFAULT 0,
    total           DECIMAL(18,4) DEFAULT 0,
    notes           TEXT DEFAULT '',
    opportunity_id  VARCHAR(36) DEFAULT '',
    expected_delivery VARCHAR(20) DEFAULT '',
    workflow_instance_id VARCHAR(36) DEFAULT '',
    created_by      VARCHAR(255) DEFAULT '',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_sales_order_document ON sales_order(document_id);
CREATE INDEX IF NOT EXISTS idx_sales_order_customer ON sales_order(customer_id);
CREATE INDEX IF NOT EXISTS idx_sales_order_status ON sales_order(status);

-- Sales Order Lines (visão de venda das linhas do documento)
CREATE TABLE IF NOT EXISTS sales_order_line (
    id              VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    order_id        VARCHAR(36) NOT NULL REFERENCES sales_order(id) ON DELETE CASCADE,
    item_id         VARCHAR(36) DEFAULT '',
    item_code       VARCHAR(100) DEFAULT '',
    item_name       VARCHAR(255) DEFAULT '',
    quantity        DECIMAL(18,4) DEFAULT 1,
    unit            VARCHAR(20) DEFAULT 'UN',
    unit_price      DECIMAL(18,4) DEFAULT 0,
    discount_pct    DECIMAL(18,4) DEFAULT 0,
    discount_value  DECIMAL(18,4) DEFAULT 0,
    tax_value       DECIMAL(18,4) DEFAULT 0,
    total           DECIMAL(18,4) DEFAULT 0,
    notes           TEXT DEFAULT '',
    sort_order      INTEGER DEFAULT 0
);

-- Sales Conditions (condições específicas da venda)
CREATE TABLE IF NOT EXISTS sales_condition (
    id              VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    order_id        VARCHAR(36) NOT NULL REFERENCES sales_order(id) ON DELETE CASCADE,
    field           VARCHAR(100) NOT NULL,
    operator        VARCHAR(30) DEFAULT 'equals',
    value           TEXT DEFAULT '',
    description     TEXT DEFAULT ''
);

-- Sales Commissions
CREATE TABLE IF NOT EXISTS sales_commission (
    id              VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    order_id        VARCHAR(36) NOT NULL REFERENCES sales_order(id) ON DELETE CASCADE,
    rep_id          VARCHAR(36) NOT NULL,
    rep_name        VARCHAR(255) DEFAULT '',
    rate            DECIMAL(18,4) DEFAULT 0,
    base_amount     DECIMAL(18,4) DEFAULT 0,
    value           DECIMAL(18,4) DEFAULT 0,
    status          VARCHAR(30) DEFAULT 'pending',
    paid_at         TIMESTAMP
);

-- Sales Contracts
CREATE TABLE IF NOT EXISTS sales_contract (
    id              VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    customer_id     VARCHAR(36) NOT NULL,
    customer_name   VARCHAR(255) DEFAULT '',
    contract_number VARCHAR(100) DEFAULT '',
    title           VARCHAR(255) DEFAULT '',
    status          VARCHAR(30) DEFAULT 'draft',
    start_date      DATE,
    end_date        DATE,
    billing_cycle   VARCHAR(30) DEFAULT 'monthly',
    value           DECIMAL(18,4) DEFAULT 0,
    renewal_type    VARCHAR(30) DEFAULT 'automatic',
    notes           TEXT DEFAULT '',
    sales_rep       VARCHAR(255) DEFAULT '',
    document_id     VARCHAR(36) REFERENCES business_documents(id),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sales Shipments (entregas)
CREATE TABLE IF NOT EXISTS sales_shipment (
    id              VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    order_id        VARCHAR(36) REFERENCES sales_order(id) ON DELETE CASCADE,
    document_id     VARCHAR(36) REFERENCES business_documents(id),
    document_number VARCHAR(100) DEFAULT '',
    carrier         VARCHAR(255) DEFAULT '',
    tracking_code   VARCHAR(255) DEFAULT '',
    status          VARCHAR(30) DEFAULT 'pending',
    origin_warehouse VARCHAR(36) DEFAULT '',
    destination     TEXT DEFAULT '',
    notes           TEXT DEFAULT '',
    shipped_at      TIMESTAMP,
    delivered_at    TIMESTAMP,
    created_by      VARCHAR(255) DEFAULT '',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed defaults
INSERT INTO sales_contract (id, customer_id, customer_name, title, status, start_date, end_date, billing_cycle, value)
SELECT gen_random_uuid()::text, 'seed-default', 'Cliente Padrão', 'Contrato Padrão', 'active', CURRENT_DATE, CURRENT_DATE + INTERVAL '1 year', 'monthly', 0
WHERE NOT EXISTS (SELECT 1 FROM sales_contract LIMIT 1);
