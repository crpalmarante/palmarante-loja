-- Document Platform
-- Single BusinessDocument model with metadata-driven definitions

-- Document Definitions (DDX Engine)
CREATE TABLE IF NOT EXISTS document_definitions (
    id          VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    name        VARCHAR(255) NOT NULL,
    code        VARCHAR(100) NOT NULL UNIQUE,
    description TEXT DEFAULT '',
    direction   VARCHAR(20) DEFAULT 'out',
    has_lines   BOOLEAN DEFAULT TRUE,
    has_parties BOOLEAN DEFAULT TRUE,
    has_totals  BOOLEAN DEFAULT TRUE,
    has_workflow BOOLEAN DEFAULT FALSE,
    workflow_code VARCHAR(100) DEFAULT '',
    behaviors   JSONB DEFAULT '[]',
    header_fields JSONB DEFAULT '[]',
    line_fields JSONB DEFAULT '[]',
    party_types JSONB DEFAULT '["customer","supplier"]',
    active      BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Document Numbering Rules
CREATE TABLE IF NOT EXISTS document_numbering (
    id              VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    document_type   VARCHAR(100) NOT NULL,
    code            VARCHAR(100) NOT NULL DEFAULT '',
    name            VARCHAR(255) DEFAULT '',
    pattern         VARCHAR(255) DEFAULT '{year}{month}{seq:06d}',
    prefix          VARCHAR(20) DEFAULT '',
    suffix          VARCHAR(20) DEFAULT '',
    next_number     INTEGER DEFAULT 1,
    digits          INTEGER DEFAULT 6,
    series          VARCHAR(10) DEFAULT '1',
    active          BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_doc_numbering_type_series ON document_numbering(document_type, series);

-- Business Documents (single aggregate root)
CREATE TABLE IF NOT EXISTS business_documents (
    id              VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    document_type   VARCHAR(100) NOT NULL,
    definition_id   VARCHAR(36) REFERENCES document_definitions(id),
    number          VARCHAR(100) NOT NULL DEFAULT '',
    status          VARCHAR(30) DEFAULT 'draft',
    organization_id VARCHAR(36) DEFAULT '',
    branch_id       VARCHAR(36) DEFAULT '',
    direction       VARCHAR(20) DEFAULT 'out',
    -- Header fields (normalized for query performance)
    header_date     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    header_currency VARCHAR(10) DEFAULT 'BRL',
    header_notes    TEXT DEFAULT '',
    header_responsible VARCHAR(255) DEFAULT '',
    header_department VARCHAR(255) DEFAULT '',
    header_cost_center VARCHAR(255) DEFAULT '',
    header_custom   JSONB DEFAULT '{}',
    -- Totals
    subtotal        DECIMAL(18,4) DEFAULT 0,
    discount_total  DECIMAL(18,4) DEFAULT 0,
    freight         DECIMAL(18,4) DEFAULT 0,
    insurance       DECIMAL(18,4) DEFAULT 0,
    tax_total       DECIMAL(18,4) DEFAULT 0,
    other_costs     DECIMAL(18,4) DEFAULT 0,
    total           DECIMAL(18,4) DEFAULT 0,
    -- Workflow
    workflow_instance_id VARCHAR(36) DEFAULT '',
    -- Metadata
    metadata        JSONB DEFAULT '{}',
    created_by      VARCHAR(255) DEFAULT '',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_business_docs_type ON business_documents(document_type);
CREATE INDEX IF NOT EXISTS idx_business_docs_status ON business_documents(status);
CREATE INDEX IF NOT EXISTS idx_business_docs_number ON business_documents(number);

-- Document Lines
CREATE TABLE IF NOT EXISTS document_lines (
    id              VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    document_id     VARCHAR(36) NOT NULL REFERENCES business_documents(id) ON DELETE CASCADE,
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
    custom_fields   JSONB DEFAULT '{}',
    sort_order      INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_doc_lines_doc_id ON document_lines(document_id);
CREATE INDEX IF NOT EXISTS idx_doc_lines_item ON document_lines(item_id);

-- Document Parties
CREATE TABLE IF NOT EXISTS document_parties (
    id              VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    document_id     VARCHAR(36) NOT NULL REFERENCES business_documents(id) ON DELETE CASCADE,
    party_id        VARCHAR(36) NOT NULL,
    party_type      VARCHAR(50) NOT NULL DEFAULT 'customer',
    party_name      VARCHAR(255) DEFAULT '',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_doc_parties_doc_id ON document_parties(document_id);
CREATE INDEX IF NOT EXISTS idx_doc_parties_party ON document_parties(party_id);

-- Document References
CREATE TABLE IF NOT EXISTS document_references (
    id              VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    document_id     VARCHAR(36) NOT NULL REFERENCES business_documents(id) ON DELETE CASCADE,
    reference_type  VARCHAR(50) NOT NULL,
    reference_id    VARCHAR(36) NOT NULL,
    reference_number VARCHAR(255) DEFAULT '',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_doc_refs_doc_id ON document_references(document_id);
CREATE INDEX IF NOT EXISTS idx_doc_refs_ref ON document_references(reference_id);

-- Document Attachments
CREATE TABLE IF NOT EXISTS document_attachments (
    id              VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    document_id     VARCHAR(36) NOT NULL REFERENCES business_documents(id) ON DELETE CASCADE,
    filename        VARCHAR(255) NOT NULL,
    file_path       VARCHAR(500) DEFAULT '',
    file_size       INTEGER DEFAULT 0,
    mime_type       VARCHAR(100) DEFAULT '',
    notes           TEXT DEFAULT '',
    uploaded_by     VARCHAR(255) DEFAULT '',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_doc_attachments_doc_id ON document_attachments(document_id);

-- Document Notes
CREATE TABLE IF NOT EXISTS document_notes (
    id              VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    document_id     VARCHAR(36) NOT NULL REFERENCES business_documents(id) ON DELETE CASCADE,
    content         TEXT NOT NULL,
    note_type       VARCHAR(50) DEFAULT 'general',
    created_by      VARCHAR(255) DEFAULT '',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_doc_notes_doc_id ON document_notes(document_id);

-- Document History (Audit Trail)
CREATE TABLE IF NOT EXISTS document_history (
    id              VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    document_id     VARCHAR(36) NOT NULL REFERENCES business_documents(id) ON DELETE CASCADE,
    action          VARCHAR(100) NOT NULL,
    from_status     VARCHAR(30) DEFAULT '',
    to_status       VARCHAR(30) DEFAULT '',
    comment         TEXT DEFAULT '',
    performed_by    VARCHAR(255) DEFAULT '',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_doc_history_doc_id ON document_history(document_id);
