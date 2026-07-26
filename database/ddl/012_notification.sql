-- Notification & Task Platform
-- Cross-cutting module used by Sales, Purchase, Inventory, Finance, and others.

-- Notifications (inbox messages)
CREATE TABLE IF NOT EXISTS notifications (
    id              VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    user_id         VARCHAR(36) NOT NULL,
    title           VARCHAR(255) NOT NULL,
    message         TEXT DEFAULT '',
    priority        VARCHAR(10) DEFAULT 'normal',   -- low, normal, high, urgent
    channel         VARCHAR(10) DEFAULT 'inbox',     -- inbox, email, push, sms
    read            BOOLEAN DEFAULT FALSE,
    entity_type     VARCHAR(50) DEFAULT '',
    entity_id       VARCHAR(36) DEFAULT '',
    action_url      VARCHAR(500) DEFAULT '',
    icon            VARCHAR(10) DEFAULT '',
    category        VARCHAR(50) DEFAULT '',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_at         TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_notif_user ON notifications(user_id, read, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_notif_entity ON notifications(entity_type, entity_id);

-- Tasks
CREATE TABLE IF NOT EXISTS tasks (
    id              VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    title           VARCHAR(255) NOT NULL,
    assignee_id     VARCHAR(36) NOT NULL,
    status          VARCHAR(20) DEFAULT 'pending',   -- pending, in_progress, completed, cancelled
    priority        VARCHAR(10) DEFAULT 'normal',
    description     TEXT DEFAULT '',
    due_date        TIMESTAMP,
    completed_at    TIMESTAMP,
    entity_type     VARCHAR(50) DEFAULT '',
    entity_id       VARCHAR(36) DEFAULT '',
    created_by      VARCHAR(36) DEFAULT '',
    category        VARCHAR(50) DEFAULT '',
    tags            TEXT[] DEFAULT '{}',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_task_assignee ON tasks(assignee_id, status);
CREATE INDEX IF NOT EXISTS idx_task_due ON tasks(due_date) WHERE status IN ('pending', 'in_progress');

-- Alerts
CREATE TABLE IF NOT EXISTS alerts (
    id              VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    user_id         VARCHAR(36) NOT NULL,
    title           VARCHAR(255) NOT NULL,
    message         TEXT DEFAULT '',
    severity        VARCHAR(10) DEFAULT 'info',      -- info, warning, critical
    acknowledged    BOOLEAN DEFAULT FALSE,
    entity_type     VARCHAR(50) DEFAULT '',
    entity_id       VARCHAR(36) DEFAULT '',
    action_url      VARCHAR(500) DEFAULT '',
    expires_at      TIMESTAMP,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acknowledged_at TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_alert_user ON alerts(user_id, acknowledged);

-- Approvals
CREATE TABLE IF NOT EXISTS approvals (
    id              VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    title           VARCHAR(255) NOT NULL,
    target_type     VARCHAR(50) NOT NULL,
    target_id       VARCHAR(36) NOT NULL,
    requester_id    VARCHAR(36) NOT NULL,
    approver_ids    TEXT[] DEFAULT '{}',
    status          VARCHAR(20) DEFAULT 'pending',   -- pending, approved, rejected, cancelled
    priority        VARCHAR(10) DEFAULT 'normal',
    reason          TEXT DEFAULT '',
    rejection_reason TEXT DEFAULT '',
    decided_by      VARCHAR(36) DEFAULT '',
    decided_at      TIMESTAMP,
    deadline        TIMESTAMP,
    escalation_minutes INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_approval_target ON approvals(target_type, target_id);
CREATE INDEX IF NOT EXISTS idx_approval_pending ON approvals(approver_ids) WHERE status = 'pending';

-- Activities (timeline events for any entity)
CREATE TABLE IF NOT EXISTS activities (
    id              VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    entity_type     VARCHAR(50) NOT NULL,
    entity_id       VARCHAR(36) NOT NULL,
    activity_type   VARCHAR(30) NOT NULL,
    user_id         VARCHAR(36) NOT NULL,
    description     TEXT DEFAULT '',
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_activity_entity ON activities(entity_type, entity_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_activity_user ON activities(user_id, created_at DESC);

-- Reminders
CREATE TABLE IF NOT EXISTS reminders (
    id              VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    user_id         VARCHAR(36) NOT NULL,
    title           VARCHAR(255) NOT NULL,
    remind_at       TIMESTAMP NOT NULL,
    message         TEXT DEFAULT '',
    entity_type     VARCHAR(50) DEFAULT '',
    entity_id       VARCHAR(36) DEFAULT '',
    recurring       VARCHAR(20) DEFAULT '',           -- daily, weekly, monthly, yearly
    fired           BOOLEAN DEFAULT FALSE,
    fired_at        TIMESTAMP,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_reminder_due ON reminders(remind_at) WHERE NOT fired;

-- Watchers (user follows an entity)
CREATE TABLE IF NOT EXISTS watchers (
    id              VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    user_id         VARCHAR(36) NOT NULL,
    entity_type     VARCHAR(50) NOT NULL,
    entity_id       VARCHAR(36) NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, entity_type, entity_id)
);

-- Mentions (@user references)
CREATE TABLE IF NOT EXISTS mentions (
    id              VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    user_id         VARCHAR(36) NOT NULL,
    mentioned_by    VARCHAR(36) NOT NULL,
    entity_type     VARCHAR(50) NOT NULL,
    entity_id       VARCHAR(36) NOT NULL,
    context         TEXT DEFAULT '',
    read            BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_mention_user ON mentions(user_id, read);
