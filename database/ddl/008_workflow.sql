CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ── Workflow Definitions ─────────────────────────────────────
CREATE TABLE IF NOT EXISTS workflow (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name            VARCHAR(255) NOT NULL,
    code            VARCHAR(50) NOT NULL UNIQUE,
    description     TEXT,
    document_type   VARCHAR(50),
    initial_state_id UUID,
    status          VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS workflow_state (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id     UUID NOT NULL REFERENCES workflow(id) ON DELETE CASCADE,
    name            VARCHAR(255) NOT NULL,
    code            VARCHAR(50) NOT NULL,
    type            VARCHAR(20) NOT NULL DEFAULT 'intermediate',
    description     TEXT,
    color           VARCHAR(7) NOT NULL DEFAULT '#1a73e8',
    sort_order      INT NOT NULL DEFAULT 0,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS workflow_transition (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id         UUID NOT NULL REFERENCES workflow(id) ON DELETE CASCADE,
    name                VARCHAR(255) NOT NULL,
    code                VARCHAR(50) NOT NULL,
    from_state_id       UUID NOT NULL REFERENCES workflow_state(id),
    to_state_id         UUID NOT NULL REFERENCES workflow_state(id),
    description         TEXT,
    requires_approval   BOOLEAN NOT NULL DEFAULT FALSE,
    approval_count      INT NOT NULL DEFAULT 1,
    sort_order          INT NOT NULL DEFAULT 0,
    active              BOOLEAN NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS workflow_rule (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id     UUID NOT NULL REFERENCES workflow(id) ON DELETE CASCADE,
    name            VARCHAR(255) NOT NULL,
    rule_type       VARCHAR(20) NOT NULL DEFAULT 'condition',
    transition_id   UUID REFERENCES workflow_transition(id),
    field           VARCHAR(100),
    operator        VARCHAR(20) NOT NULL DEFAULT 'equals',
    value           TEXT,
    error_message   TEXT,
    target_role     VARCHAR(100),
    sort_order      INT NOT NULL DEFAULT 0,
    active          BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS workflow_assignment (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id     UUID NOT NULL REFERENCES workflow(id) ON DELETE CASCADE,
    transition_id   UUID REFERENCES workflow_transition(id),
    assignment_type VARCHAR(20) NOT NULL,
    value           VARCHAR(255) NOT NULL,
    active          BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ── Workflow Instances ─────────────────────────────────────
CREATE TABLE IF NOT EXISTS workflow_instance (
    id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id       UUID NOT NULL REFERENCES workflow(id),
    document_type     VARCHAR(50) NOT NULL,
    document_id       UUID NOT NULL,
    current_state_id  UUID NOT NULL REFERENCES workflow_state(id),
    document_data     JSONB,
    status            VARCHAR(20) NOT NULL DEFAULT 'active',
    started_at        TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at      TIMESTAMP
);

CREATE TABLE IF NOT EXISTS workflow_history (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    instance_id     UUID NOT NULL REFERENCES workflow_instance(id) ON DELETE CASCADE,
    from_state_id   UUID REFERENCES workflow_state(id),
    to_state_id     UUID REFERENCES workflow_state(id),
    transition_id   UUID REFERENCES workflow_transition(id),
    action          VARCHAR(50) NOT NULL,
    comment         TEXT,
    performed_by    VARCHAR(255),
    metadata        JSONB,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS workflow_approval (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    instance_id     UUID NOT NULL REFERENCES workflow_instance(id) ON DELETE CASCADE,
    transition_id   UUID NOT NULL REFERENCES workflow_transition(id),
    required_count  INT NOT NULL DEFAULT 1,
    status          VARCHAR(20) NOT NULL DEFAULT 'pending',
    role            VARCHAR(100),
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_wf_state ON workflow_state(workflow_id);
CREATE INDEX idx_wf_transition ON workflow_transition(workflow_id);
CREATE INDEX idx_wf_rule_workflow ON workflow_rule(workflow_id);
CREATE INDEX idx_wf_rule_transition ON workflow_rule(transition_id);
CREATE INDEX idx_wf_instance_workflow ON workflow_instance(workflow_id);
CREATE INDEX idx_wf_instance_document ON workflow_instance(document_type, document_id);
CREATE INDEX idx_wf_instance_status ON workflow_instance(status);
CREATE INDEX idx_wf_history_instance ON workflow_history(instance_id);
CREATE INDEX idx_wf_approval_instance ON workflow_approval(instance_id);
CREATE INDEX idx_wf_approval_status ON workflow_approval(status);
