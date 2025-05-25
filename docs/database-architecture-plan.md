# MABOS Database Architecture Plan

## Phase 1: Core Database Infrastructure (Current Priority)

### 1.1 Primary Databases Setup
```yaml
Priority: IMMEDIATE
Components:
  - PostgreSQL: Primary relational database for users, workflows, tasks
  - Redis: Caching, sessions, real-time data
  - Neo4j: Knowledge graph for BDI agents and ontologies
  - Elasticsearch: Search, analytics, workflow indexing
```

### 1.2 Knowledge Graph & Ontology (CRITICAL FOUNDATION)
```yaml
Database: Neo4j
Purpose: BDI Agent Knowledge Base
Components:
  - Agent Beliefs: Current state knowledge
  - Agent Intentions: Goal hierarchies and plans
  - Domain Ontologies: Business process semantics
  - Enterprise Mappings: System relationship models
  - Workflow Semantics: Process definition relationships
```

## Phase 2: BDI Agent Knowledge Architecture

### 2.1 Core Ontology Structure
```cypher
// Agent Nodes
CREATE (agent:Agent {id: 'agent_001', type: 'workflow_orchestrator'})
CREATE (belief:Belief {id: 'belief_001', content: 'system_status_healthy'})
CREATE (intention:Intention {id: 'intent_001', goal: 'optimize_workflow'})
CREATE (plan:Plan {id: 'plan_001', strategy: 'parallel_execution'})

// Relationships
CREATE (agent)-[:HAS_BELIEF]->(belief)
CREATE (agent)-[:HAS_INTENTION]->(intention)
CREATE (intention)-[:ACHIEVED_BY]->(plan)
```

### 2.2 Enterprise Ontology
```cypher
// Enterprise Systems
CREATE (sap:System {name: 'SAP', type: 'ERP'})
CREATE (salesforce:System {name: 'Salesforce', type: 'CRM'})
CREATE (servicenow:System {name: 'ServiceNow', type: 'ITSM'})

// Data Mappings
CREATE (customer:Entity {type: 'Customer'})
CREATE (sap)-[:CONTAINS]->(customer)
CREATE (salesforce)-[:CONTAINS]->(customer)
```

### 2.3 Workflow Ontology
```cypher
// Workflow Components
CREATE (process:WorkflowProcess {name: 'customer_onboarding'})
CREATE (task:WorkflowTask {name: 'verify_identity'})
CREATE (decision:DecisionPoint {name: 'approval_required'})

// Process Flow
CREATE (process)-[:CONTAINS]->(task)
CREATE (task)-[:LEADS_TO]->(decision)
```

## Phase 3: Database Integration Architecture

### 3.1 Multi-Database Coordination
```python
# Database Manager Architecture
class DatabaseManager:
    def __init__(self):
        self.postgres = PostgreSQLManager()    # Primary data
        self.neo4j = Neo4jManager()           # Knowledge graph
        self.redis = RedisManager()           # Cache/sessions
        self.elasticsearch = ElasticsearchManager()  # Search
    
    async def sync_knowledge_graph(self, workflow_data):
        """Sync workflow changes to knowledge graph"""
        # Update Neo4j with new workflow relationships
        # Update agent beliefs about system state
        pass
```

### 3.2 Data Flow Architecture
```yaml
Data Flow:
  1. User creates workflow (PostgreSQL)
  2. Workflow semantics stored (Neo4j)
  3. Agent beliefs updated (Neo4j)
  4. Workflow indexed (Elasticsearch)
  5. Cache updated (Redis)
```

## Phase 4: Implementation Priority

### Immediate Setup (Week 1-2):
1. **PostgreSQL**: User management, basic workflow storage
2. **Neo4j**: BDI agent knowledge base and ontologies
3. **Redis**: Session management and caching
4. **Basic Integration**: Cross-database synchronization

### Short-term (Week 3-4):
1. **Elasticsearch**: Workflow search and analytics
2. **Advanced Ontologies**: Enterprise system mappings
3. **Agent Reasoning**: BDI logic implementation

### Medium-term (Month 2):
1. **Performance Optimization**: Query optimization across databases
2. **Advanced Analytics**: Complex knowledge graph queries
3. **Enterprise Connectors**: Real-time data synchronization

## Database Schema Priorities

### 1. PostgreSQL Schema (Primary)
```sql
-- Users and Authentication
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Workflows
CREATE TABLE workflows (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    definition JSONB NOT NULL,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 2. Neo4j Schema (Knowledge Graph)
```cypher
// Core BDI Constraints
CREATE CONSTRAINT agent_id FOR (a:Agent) REQUIRE a.id IS UNIQUE;
CREATE CONSTRAINT belief_id FOR (b:Belief) REQUIRE b.id IS UNIQUE;
CREATE CONSTRAINT intention_id FOR (i:Intention) REQUIRE i.id IS UNIQUE;

// Ontology Constraints
CREATE CONSTRAINT system_name FOR (s:System) REQUIRE s.name IS UNIQUE;
CREATE CONSTRAINT entity_type FOR (e:Entity) REQUIRE (e.type, e.system) IS UNIQUE;
```

### 3. Redis Schema (Caching)
```yaml
Key Patterns:
  - user:session:{user_id}: User session data
  - workflow:cache:{workflow_id}: Cached workflow data
  - agent:state:{agent_id}: Current agent state
  - system:health: System health metrics
```

## Integration with MABOS Components

### BDI Agent Engine Integration:
- **Beliefs**: Stored in Neo4j as current system state
- **Desires**: Goal hierarchies in knowledge graph
- **Intentions**: Active plans and strategies
- **Knowledge**: Domain ontologies and enterprise mappings

### Workflow Orchestration Integration:
- **Process Definitions**: PostgreSQL for execution data
- **Semantic Relationships**: Neo4j for process understanding
- **Execution Cache**: Redis for real-time state
- **Search Index**: Elasticsearch for workflow discovery

### Enterprise Connector Integration:
- **System Mappings**: Neo4j ontologies
- **Data Synchronization**: Cross-database updates
- **Relationship Tracking**: Knowledge graph connections

## Next Steps

1. **Setup Neo4j** alongside PostgreSQL and Redis
2. **Create base ontologies** for BDI agents
3. **Implement database synchronization** layer
4. **Build knowledge graph APIs** for agent reasoning
5. **Integrate with workflow engine** for semantic understanding

This architecture ensures that MABOS has the foundational knowledge infrastructure needed for intelligent agent reasoning and enterprise-scale workflow orchestration. 