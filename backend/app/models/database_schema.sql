-- MABOS PostgreSQL Database Schema
-- Multi-Agent Business Operating System
-- Comprehensive schema for user management, workflows, agents, and execution tracking

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- =====================================================
-- USERS & AUTHENTICATION TABLES
-- =====================================================

-- Users table with comprehensive profile information
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    display_name VARCHAR(200),
    avatar_url TEXT,
    phone VARCHAR(20),
    timezone VARCHAR(50) DEFAULT 'UTC',
    locale VARCHAR(10) DEFAULT 'en-US',
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    is_superuser BOOLEAN DEFAULT false,
    last_login TIMESTAMP WITH TIME ZONE,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE,
    password_changed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- User sessions for JWT token management
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    refresh_token VARCHAR(255) UNIQUE NOT NULL,
    device_info JSONB,
    ip_address INET,
    user_agent TEXT,
    is_active BOOLEAN DEFAULT true,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Roles and permissions for RBAC
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    display_name VARCHAR(200),
    description TEXT,
    is_system_role BOOLEAN DEFAULT false,
    permissions JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- User role assignments
CREATE TABLE user_roles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_id UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    assigned_by UUID REFERENCES users(id),
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(user_id, role_id)
);

-- Organizations for multi-tenancy
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    logo_url TEXT,
    website_url TEXT,
    settings JSONB DEFAULT '{}',
    subscription_plan VARCHAR(50) DEFAULT 'free',
    subscription_status VARCHAR(20) DEFAULT 'active',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Organization memberships
CREATE TABLE organization_members (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) DEFAULT 'member',
    permissions JSONB DEFAULT '[]',
    invited_by UUID REFERENCES users(id),
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(organization_id, user_id)
);

-- =====================================================
-- BUSINESS ONBOARDING TABLES
-- =====================================================

-- Businesses table for onboarded ventures
CREATE TABLE IF NOT EXISTS businesses (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(500) NOT NULL,
    type VARCHAR(50) NOT NULL,
    legal_name VARCHAR(500),
    description TEXT,
    jurisdiction VARCHAR(100),
    stage VARCHAR(50) DEFAULT 'mvp',
    status VARCHAR(50) DEFAULT 'active',
    agent_roles JSONB DEFAULT '[]'::jsonb,
    ontology_stats JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for business lookups
CREATE INDEX IF NOT EXISTS idx_businesses_type ON businesses(type);
CREATE INDEX IF NOT EXISTS idx_businesses_status ON businesses(status);

-- =====================================================
-- WORKFLOW MANAGEMENT TABLES
-- =====================================================

-- Workflow definitions
CREATE TABLE workflows (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    version VARCHAR(20) DEFAULT '1.0.0',
    yaml_definition TEXT NOT NULL,
    parsed_definition JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'draft', -- draft, active, inactive, archived
    category VARCHAR(100),
    tags TEXT[],
    is_template BOOLEAN DEFAULT false,
    is_public BOOLEAN DEFAULT false,
    created_by UUID NOT NULL REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    published_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Workflow versions for version control
CREATE TABLE workflow_versions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    version VARCHAR(20) NOT NULL,
    yaml_definition TEXT NOT NULL,
    parsed_definition JSONB NOT NULL,
    changelog TEXT,
    created_by UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(workflow_id, version)
);

-- Workflow executions
CREATE TABLE workflow_executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID NOT NULL REFERENCES workflows(id),
    workflow_version VARCHAR(20),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    triggered_by UUID REFERENCES users(id),
    trigger_type VARCHAR(50), -- manual, scheduled, webhook, event
    trigger_data JSONB,
    status VARCHAR(20) DEFAULT 'pending', -- pending, running, completed, failed, cancelled
    priority INTEGER DEFAULT 5,
    input_data JSONB,
    output_data JSONB,
    error_message TEXT,
    execution_context JSONB,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    duration_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Task executions within workflows
CREATE TABLE task_executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_execution_id UUID NOT NULL REFERENCES workflow_executions(id) ON DELETE CASCADE,
    task_name VARCHAR(200) NOT NULL,
    task_type VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    input_data JSONB,
    output_data JSONB,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    duration_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- BDI AGENT SYSTEM TABLES
-- =====================================================

-- Agent definitions
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    type VARCHAR(100) NOT NULL, -- orchestrator, workflow, integration, meta
    description TEXT,
    configuration JSONB NOT NULL DEFAULT '{}',
    capabilities JSONB DEFAULT '[]',
    status VARCHAR(20) DEFAULT 'inactive', -- active, inactive, error, maintenance
    version VARCHAR(20) DEFAULT '1.0.0',
    created_by UUID NOT NULL REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    last_heartbeat TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Agent beliefs (knowledge state)
CREATE TABLE agent_beliefs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    category VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    confidence DECIMAL(3,2) DEFAULT 1.0,
    source VARCHAR(200),
    evidence JSONB,
    is_active BOOLEAN DEFAULT true,
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Agent desires (goals)
CREATE TABLE agent_desires (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    goal_type VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    priority INTEGER DEFAULT 5,
    target_state JSONB,
    success_criteria JSONB,
    status VARCHAR(20) DEFAULT 'active', -- active, achieved, abandoned, blocked
    deadline TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Agent intentions (plans)
CREATE TABLE agent_intentions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    desire_id UUID REFERENCES agent_desires(id) ON DELETE CASCADE,
    plan_name VARCHAR(200) NOT NULL,
    plan_steps JSONB NOT NULL,
    current_step INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'planned', -- planned, executing, completed, failed, suspended
    execution_context JSONB,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Agent communications
CREATE TABLE agent_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sender_agent_id UUID NOT NULL REFERENCES agents(id),
    receiver_agent_id UUID REFERENCES agents(id),
    message_type VARCHAR(100) NOT NULL,
    content JSONB NOT NULL,
    priority INTEGER DEFAULT 5,
    status VARCHAR(20) DEFAULT 'sent', -- sent, delivered, processed, failed
    correlation_id UUID,
    reply_to UUID REFERENCES agent_messages(id),
    processed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- INTEGRATION & CONNECTOR TABLES
-- =====================================================

-- External system connections
CREATE TABLE integrations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    type VARCHAR(100) NOT NULL, -- sap, salesforce, servicenow, microsoft365, oracle
    description TEXT,
    configuration JSONB NOT NULL,
    credentials JSONB NOT NULL, -- encrypted
    status VARCHAR(20) DEFAULT 'inactive',
    last_sync TIMESTAMP WITH TIME ZONE,
    sync_frequency VARCHAR(50), -- hourly, daily, weekly, manual
    error_count INTEGER DEFAULT 0,
    created_by UUID NOT NULL REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Integration sync logs
CREATE TABLE integration_sync_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    integration_id UUID NOT NULL REFERENCES integrations(id) ON DELETE CASCADE,
    sync_type VARCHAR(50) NOT NULL, -- full, incremental, manual
    status VARCHAR(20) NOT NULL, -- success, failed, partial
    records_processed INTEGER DEFAULT 0,
    records_created INTEGER DEFAULT 0,
    records_updated INTEGER DEFAULT 0,
    records_failed INTEGER DEFAULT 0,
    error_details JSONB,
    started_at TIMESTAMP WITH TIME ZONE NOT NULL,
    completed_at TIMESTAMP WITH TIME ZONE,
    duration_ms INTEGER
);

-- =====================================================
-- AUDIT & LOGGING TABLES
-- =====================================================

-- Comprehensive audit trail
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID REFERENCES organizations(id),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100) NOT NULL,
    resource_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    session_id UUID,
    correlation_id UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- System events and notifications
CREATE TABLE system_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID REFERENCES organizations(id),
    event_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) DEFAULT 'info', -- debug, info, warning, error, critical
    title VARCHAR(200) NOT NULL,
    description TEXT,
    metadata JSONB,
    source VARCHAR(100),
    acknowledged BOOLEAN DEFAULT false,
    acknowledged_by UUID REFERENCES users(id),
    acknowledged_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Performance metrics
CREATE TABLE performance_metrics (
    id UUID DEFAULT uuid_generate_v4(),
    organization_id UUID REFERENCES organizations(id),
    metric_type VARCHAR(100) NOT NULL,
    metric_name VARCHAR(200) NOT NULL,
    value DECIMAL(15,6) NOT NULL,
    unit VARCHAR(50),
    tags JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id, timestamp)
) PARTITION BY RANGE (timestamp);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- User indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_active ON users(is_active);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Session indexes
CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_token ON user_sessions(session_token);
CREATE INDEX idx_user_sessions_active ON user_sessions(is_active);
CREATE INDEX idx_user_sessions_expires ON user_sessions(expires_at);

-- Workflow indexes
CREATE INDEX idx_workflows_org_id ON workflows(organization_id);
CREATE INDEX idx_workflows_status ON workflows(status);
CREATE INDEX idx_workflows_created_by ON workflows(created_by);
CREATE INDEX idx_workflows_tags ON workflows USING GIN(tags);
CREATE INDEX idx_workflows_name_trgm ON workflows USING GIN(name gin_trgm_ops);

-- Workflow execution indexes
CREATE INDEX idx_workflow_executions_workflow_id ON workflow_executions(workflow_id);
CREATE INDEX idx_workflow_executions_org_id ON workflow_executions(organization_id);
CREATE INDEX idx_workflow_executions_status ON workflow_executions(status);
CREATE INDEX idx_workflow_executions_triggered_by ON workflow_executions(triggered_by);
CREATE INDEX idx_workflow_executions_created_at ON workflow_executions(created_at);

-- Task execution indexes
CREATE INDEX idx_task_executions_workflow_execution_id ON task_executions(workflow_execution_id);
CREATE INDEX idx_task_executions_status ON task_executions(status);
CREATE INDEX idx_task_executions_created_at ON task_executions(created_at);

-- Agent indexes
CREATE INDEX idx_agents_org_id ON agents(organization_id);
CREATE INDEX idx_agents_type ON agents(type);
CREATE INDEX idx_agents_status ON agents(status);
CREATE INDEX idx_agents_name_trgm ON agents USING GIN(name gin_trgm_ops);

-- Agent belief indexes
CREATE INDEX idx_agent_beliefs_agent_id ON agent_beliefs(agent_id);
CREATE INDEX idx_agent_beliefs_category ON agent_beliefs(category);
CREATE INDEX idx_agent_beliefs_active ON agent_beliefs(is_active);
CREATE INDEX idx_agent_beliefs_created_at ON agent_beliefs(created_at);

-- Agent desire indexes
CREATE INDEX idx_agent_desires_agent_id ON agent_desires(agent_id);
CREATE INDEX idx_agent_desires_status ON agent_desires(status);
CREATE INDEX idx_agent_desires_priority ON agent_desires(priority);

-- Agent intention indexes
CREATE INDEX idx_agent_intentions_agent_id ON agent_intentions(agent_id);
CREATE INDEX idx_agent_intentions_desire_id ON agent_intentions(desire_id);
CREATE INDEX idx_agent_intentions_status ON agent_intentions(status);

-- Agent message indexes
CREATE INDEX idx_agent_messages_sender ON agent_messages(sender_agent_id);
CREATE INDEX idx_agent_messages_receiver ON agent_messages(receiver_agent_id);
CREATE INDEX idx_agent_messages_type ON agent_messages(message_type);
CREATE INDEX idx_agent_messages_status ON agent_messages(status);
CREATE INDEX idx_agent_messages_created_at ON agent_messages(created_at);

-- Integration indexes
CREATE INDEX idx_integrations_org_id ON integrations(organization_id);
CREATE INDEX idx_integrations_type ON integrations(type);
CREATE INDEX idx_integrations_status ON integrations(status);

-- Audit log indexes
CREATE INDEX idx_audit_logs_org_id ON audit_logs(organization_id);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_resource_type ON audit_logs(resource_type);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);

-- System event indexes
CREATE INDEX idx_system_events_org_id ON system_events(organization_id);
CREATE INDEX idx_system_events_type ON system_events(event_type);
CREATE INDEX idx_system_events_severity ON system_events(severity);
CREATE INDEX idx_system_events_created_at ON system_events(created_at);

-- Performance metric indexes
CREATE INDEX idx_performance_metrics_org_id ON performance_metrics(organization_id);
CREATE INDEX idx_performance_metrics_type ON performance_metrics(metric_type);
CREATE INDEX idx_performance_metrics_timestamp ON performance_metrics(timestamp);

-- =====================================================
-- TRIGGERS FOR AUTOMATIC UPDATES
-- =====================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers to relevant tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_roles_updated_at BEFORE UPDATE ON roles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_organizations_updated_at BEFORE UPDATE ON organizations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_workflows_updated_at BEFORE UPDATE ON workflows
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agents_updated_at BEFORE UPDATE ON agents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agent_beliefs_updated_at BEFORE UPDATE ON agent_beliefs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agent_desires_updated_at BEFORE UPDATE ON agent_desires
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agent_intentions_updated_at BEFORE UPDATE ON agent_intentions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_integrations_updated_at BEFORE UPDATE ON integrations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- PARTITIONING FOR LARGE TABLES
-- =====================================================

-- Create monthly partitions for performance metrics (example for current year)
CREATE TABLE performance_metrics_2025_01 PARTITION OF performance_metrics
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

CREATE TABLE performance_metrics_2025_02 PARTITION OF performance_metrics
    FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');

CREATE TABLE performance_metrics_2025_03 PARTITION OF performance_metrics
    FOR VALUES FROM ('2025-03-01') TO ('2025-04-01');

CREATE TABLE performance_metrics_2025_04 PARTITION OF performance_metrics
    FOR VALUES FROM ('2025-04-01') TO ('2025-05-01');

CREATE TABLE performance_metrics_2025_05 PARTITION OF performance_metrics
    FOR VALUES FROM ('2025-05-01') TO ('2025-06-01');

CREATE TABLE performance_metrics_2025_06 PARTITION OF performance_metrics
    FOR VALUES FROM ('2025-06-01') TO ('2025-07-01');

CREATE TABLE performance_metrics_2025_07 PARTITION OF performance_metrics
    FOR VALUES FROM ('2025-07-01') TO ('2025-08-01');

CREATE TABLE performance_metrics_2025_08 PARTITION OF performance_metrics
    FOR VALUES FROM ('2025-08-01') TO ('2025-09-01');

CREATE TABLE performance_metrics_2025_09 PARTITION OF performance_metrics
    FOR VALUES FROM ('2025-09-01') TO ('2025-10-01');

CREATE TABLE performance_metrics_2025_10 PARTITION OF performance_metrics
    FOR VALUES FROM ('2025-10-01') TO ('2025-11-01');

CREATE TABLE performance_metrics_2025_11 PARTITION OF performance_metrics
    FOR VALUES FROM ('2025-11-01') TO ('2025-12-01');

CREATE TABLE performance_metrics_2025_12 PARTITION OF performance_metrics
    FOR VALUES FROM ('2025-12-01') TO ('2026-01-01');

-- =====================================================
-- INITIAL DATA SETUP
-- =====================================================

-- Insert default roles
INSERT INTO roles (name, display_name, description, is_system_role, permissions) VALUES
('super_admin', 'Super Administrator', 'Full system access with all permissions', true, '["*"]'),
('admin', 'Administrator', 'Organization administrator with full access', true, '["org:*", "user:*", "workflow:*", "agent:*"]'),
('workflow_manager', 'Workflow Manager', 'Can create and manage workflows', true, '["workflow:create", "workflow:read", "workflow:update", "workflow:delete", "workflow:execute"]'),
('workflow_user', 'Workflow User', 'Can execute and view workflows', true, '["workflow:read", "workflow:execute"]'),
('viewer', 'Viewer', 'Read-only access to workflows and data', true, '["workflow:read", "agent:read", "integration:read"]');

-- Insert default organization (for single-tenant setups)
INSERT INTO organizations (name, slug, description) VALUES
('MABOS Default', 'mabos-default', 'Default organization for MABOS platform');

-- Create indexes on JSONB columns for better performance
CREATE INDEX idx_workflows_parsed_definition ON workflows USING GIN(parsed_definition);
CREATE INDEX idx_workflow_executions_input_data ON workflow_executions USING GIN(input_data);
CREATE INDEX idx_workflow_executions_output_data ON workflow_executions USING GIN(output_data);
CREATE INDEX idx_agents_configuration ON agents USING GIN(configuration);
CREATE INDEX idx_agents_capabilities ON agents USING GIN(capabilities);
CREATE INDEX idx_integrations_configuration ON integrations USING GIN(configuration);
CREATE INDEX idx_audit_logs_old_values ON audit_logs USING GIN(old_values);
CREATE INDEX idx_audit_logs_new_values ON audit_logs USING GIN(new_values);

-- Comments for documentation
COMMENT ON TABLE users IS 'User accounts with authentication and profile information';
COMMENT ON TABLE workflows IS 'Workflow definitions with YAML and parsed JSON representations';
COMMENT ON TABLE workflow_executions IS 'Individual workflow execution instances with status tracking';
COMMENT ON TABLE agents IS 'BDI agent definitions with configuration and capabilities';
COMMENT ON TABLE agent_beliefs IS 'Agent knowledge state and beliefs';
COMMENT ON TABLE agent_desires IS 'Agent goals and objectives';
COMMENT ON TABLE agent_intentions IS 'Agent plans and execution strategies';
COMMENT ON TABLE integrations IS 'External system integration configurations';
COMMENT ON TABLE audit_logs IS 'Comprehensive audit trail for all system activities';
COMMENT ON TABLE performance_metrics IS 'System performance and monitoring metrics (partitioned by month)'; 