// MABOS BDI Agent Ontology Initialization
// This script sets up the foundational knowledge graph structure for BDI agents

// ===== CONSTRAINTS AND INDEXES =====

// Core BDI Entity Constraints
CREATE CONSTRAINT agent_id IF NOT EXISTS FOR (a:Agent) REQUIRE a.id IS UNIQUE;
CREATE CONSTRAINT belief_id IF NOT EXISTS FOR (b:Belief) REQUIRE b.id IS UNIQUE;
CREATE CONSTRAINT desire_id IF NOT EXISTS FOR (d:Desire) REQUIRE d.id IS UNIQUE;
CREATE CONSTRAINT intention_id IF NOT EXISTS FOR (i:Intention) REQUIRE i.id IS UNIQUE;
CREATE CONSTRAINT plan_id IF NOT EXISTS FOR (p:Plan) REQUIRE p.id IS UNIQUE;

// Workflow Entity Constraints
CREATE CONSTRAINT workflow_id IF NOT EXISTS FOR (w:Workflow) REQUIRE w.id IS UNIQUE;
CREATE CONSTRAINT task_id IF NOT EXISTS FOR (t:Task) REQUIRE t.id IS UNIQUE;
CREATE CONSTRAINT process_id IF NOT EXISTS FOR (pr:Process) REQUIRE pr.id IS UNIQUE;

// Enterprise System Constraints
CREATE CONSTRAINT system_name IF NOT EXISTS FOR (s:System) REQUIRE s.name IS UNIQUE;
CREATE CONSTRAINT entity_type IF NOT EXISTS FOR (e:Entity) REQUIRE (e.type, e.system) IS UNIQUE;

// Performance Indexes
CREATE INDEX agent_type_idx IF NOT EXISTS FOR (a:Agent) ON (a.type);
CREATE INDEX belief_category_idx IF NOT EXISTS FOR (b:Belief) ON (b.category);
CREATE INDEX workflow_status_idx IF NOT EXISTS FOR (w:Workflow) ON (w.status);
CREATE INDEX system_type_idx IF NOT EXISTS FOR (s:System) ON (s.type);

// ===== CORE BDI AGENT ARCHITECTURE =====

// Master Orchestrator Agent
CREATE (orchestrator:Agent {
    id: 'agent_orchestrator_001',
    name: 'MABOS Orchestrator',
    type: 'orchestrator',
    status: 'active',
    created_at: datetime(),
    capabilities: ['workflow_management', 'resource_allocation', 'system_monitoring'],
    description: 'Primary orchestrator agent responsible for coordinating all MABOS operations'
});

// Workflow Management Agent
CREATE (workflow_agent:Agent {
    id: 'agent_workflow_001',
    name: 'Workflow Manager',
    type: 'workflow_manager',
    status: 'active',
    created_at: datetime(),
    capabilities: ['process_execution', 'task_scheduling', 'dependency_resolution'],
    description: 'Specialized agent for workflow orchestration and execution'
});

// Enterprise Integration Agent
CREATE (integration_agent:Agent {
    id: 'agent_integration_001',
    name: 'Enterprise Integrator',
    type: 'integration_manager',
    status: 'active',
    created_at: datetime(),
    capabilities: ['system_connectivity', 'data_mapping', 'protocol_translation'],
    description: 'Agent responsible for enterprise system integration and data synchronization'
});

// ===== FOUNDATIONAL BELIEFS =====

// System Health Beliefs
CREATE (system_health:Belief {
    id: 'belief_system_health_001',
    category: 'system_status',
    content: 'system_operational',
    confidence: 0.95,
    source: 'health_monitor',
    created_at: datetime(),
    last_updated: datetime(),
    description: 'Current system operational status'
});

// Resource Availability Beliefs
CREATE (resource_belief:Belief {
    id: 'belief_resources_001',
    category: 'resource_status',
    content: 'resources_available',
    confidence: 0.90,
    source: 'resource_monitor',
    created_at: datetime(),
    last_updated: datetime(),
    description: 'Current resource availability status'
});

// Workflow Capacity Beliefs
CREATE (capacity_belief:Belief {
    id: 'belief_capacity_001',
    category: 'workflow_capacity',
    content: 'capacity_normal',
    confidence: 0.85,
    source: 'workflow_monitor',
    created_at: datetime(),
    last_updated: datetime(),
    description: 'Current workflow processing capacity'
});

// ===== CORE DESIRES AND GOALS =====

// System Optimization Desire
CREATE (optimize_desire:Desire {
    id: 'desire_optimize_001',
    goal: 'optimize_system_performance',
    priority: 'high',
    category: 'performance',
    target_metric: 'throughput',
    target_value: 1000,
    current_value: 750,
    created_at: datetime(),
    description: 'Desire to optimize overall system performance and throughput'
});

// Workflow Efficiency Desire
CREATE (efficiency_desire:Desire {
    id: 'desire_efficiency_001',
    goal: 'maximize_workflow_efficiency',
    priority: 'high',
    category: 'efficiency',
    target_metric: 'completion_rate',
    target_value: 0.95,
    current_value: 0.82,
    created_at: datetime(),
    description: 'Desire to maximize workflow completion efficiency'
});

// User Satisfaction Desire
CREATE (satisfaction_desire:Desire {
    id: 'desire_satisfaction_001',
    goal: 'improve_user_satisfaction',
    priority: 'medium',
    category: 'user_experience',
    target_metric: 'satisfaction_score',
    target_value: 4.5,
    current_value: 3.8,
    created_at: datetime(),
    description: 'Desire to improve overall user satisfaction with the system'
});

// ===== ACTIVE INTENTIONS =====

// Performance Monitoring Intention
CREATE (monitor_intention:Intention {
    id: 'intention_monitor_001',
    goal: 'continuous_performance_monitoring',
    status: 'active',
    priority: 'high',
    created_at: datetime(),
    deadline: datetime() + duration('P30D'),
    progress: 0.0,
    description: 'Intention to continuously monitor system performance metrics'
});

// Workflow Optimization Intention
CREATE (optimize_intention:Intention {
    id: 'intention_optimize_001',
    goal: 'implement_workflow_optimizations',
    status: 'planning',
    priority: 'high',
    created_at: datetime(),
    deadline: datetime() + duration('P14D'),
    progress: 0.15,
    description: 'Intention to implement identified workflow optimizations'
});

// ===== EXECUTION PLANS =====

// Performance Monitoring Plan
CREATE (monitor_plan:Plan {
    id: 'plan_monitor_001',
    name: 'Continuous Performance Monitoring',
    strategy: 'real_time_monitoring',
    status: 'active',
    created_at: datetime(),
    steps: [
        'collect_metrics',
        'analyze_trends',
        'identify_bottlenecks',
        'generate_alerts',
        'update_beliefs'
    ],
    estimated_duration: duration('PT24H'),
    description: 'Plan for continuous system performance monitoring'
});

// Optimization Implementation Plan
CREATE (optimize_plan:Plan {
    id: 'plan_optimize_001',
    name: 'Workflow Optimization Implementation',
    strategy: 'incremental_improvement',
    status: 'planning',
    created_at: datetime(),
    steps: [
        'analyze_current_workflows',
        'identify_optimization_opportunities',
        'design_improvements',
        'test_optimizations',
        'deploy_changes',
        'monitor_results'
    ],
    estimated_duration: duration('P14D'),
    description: 'Plan for implementing workflow optimizations'
});

// ===== BDI RELATIONSHIPS =====

// Agent-Belief Relationships
CREATE (orchestrator)-[:HAS_BELIEF]->(system_health);
CREATE (orchestrator)-[:HAS_BELIEF]->(resource_belief);
CREATE (workflow_agent)-[:HAS_BELIEF]->(capacity_belief);

// Agent-Desire Relationships
CREATE (orchestrator)-[:HAS_DESIRE]->(optimize_desire);
CREATE (workflow_agent)-[:HAS_DESIRE]->(efficiency_desire);
CREATE (orchestrator)-[:HAS_DESIRE]->(satisfaction_desire);

// Agent-Intention Relationships
CREATE (orchestrator)-[:HAS_INTENTION]->(monitor_intention);
CREATE (workflow_agent)-[:HAS_INTENTION]->(optimize_intention);

// Desire-Intention Relationships
CREATE (optimize_desire)-[:MOTIVATES]->(monitor_intention);
CREATE (efficiency_desire)-[:MOTIVATES]->(optimize_intention);

// Intention-Plan Relationships
CREATE (monitor_intention)-[:ACHIEVED_BY]->(monitor_plan);
CREATE (optimize_intention)-[:ACHIEVED_BY]->(optimize_plan);

// Belief-Desire Relationships (beliefs inform desires)
CREATE (system_health)-[:INFORMS]->(optimize_desire);
CREATE (capacity_belief)-[:INFORMS]->(efficiency_desire);

// ===== KNOWLEDGE DOMAINS =====

// Workflow Domain Knowledge
CREATE (workflow_domain:Domain {
    id: 'domain_workflow_001',
    name: 'Workflow Management',
    category: 'operational',
    description: 'Knowledge domain for workflow orchestration and management'
});

// Enterprise Integration Domain
CREATE (integration_domain:Domain {
    id: 'domain_integration_001',
    name: 'Enterprise Integration',
    category: 'technical',
    description: 'Knowledge domain for enterprise system integration'
});

// Performance Optimization Domain
CREATE (performance_domain:Domain {
    id: 'domain_performance_001',
    name: 'Performance Optimization',
    category: 'analytical',
    description: 'Knowledge domain for system performance analysis and optimization'
});

// Agent-Domain Relationships
CREATE (workflow_agent)-[:SPECIALIZES_IN]->(workflow_domain);
CREATE (integration_agent)-[:SPECIALIZES_IN]->(integration_domain);
CREATE (orchestrator)-[:SPECIALIZES_IN]->(performance_domain);

// ===== INITIAL SUCCESS MESSAGE =====
CREATE (init_success:Event {
    id: 'event_init_001',
    type: 'system_initialization',
    message: 'MABOS BDI ontology successfully initialized',
    timestamp: datetime(),
    details: 'Core BDI agents, beliefs, desires, intentions, and plans established'
});

// Log initialization completion
CREATE (orchestrator)-[:LOGGED]->(init_success); 