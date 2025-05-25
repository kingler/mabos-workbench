# MABOS System Architectural Requirements Document (SARD)

**Document Version:** 1.0  
**Date:** December 2024  
**Project:** Multi-Agent Business Operating System (MABOS)  
**Document Type:** System Architectural Requirements Document  
**Status:** Draft for Review

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [System Architecture Overview](#2-system-architecture-overview)
3. [Detailed Component Descriptions](#3-detailed-component-descriptions)
4. [Database Schema and Implementation](#4-database-schema-and-implementation)
5. [Knowledge Graph / Ontology](#5-knowledge-graph--ontology)
6. [Integration and APIs](#6-integration-and-apis)
7. [Deployment Architecture](#7-deployment-architecture)
8. [Security Architecture](#8-security-architecture)
9. [Performance and Scalability Considerations](#9-performance-and-scalability-considerations)
10. [Monitoring and Logging](#10-monitoring-and-logging)
11. [Disaster Recovery and Business Continuity](#11-disaster-recovery-and-business-continuity)
12. [Development, Testing, and Deployment Processes](#12-development-testing-and-deployment-processes)

---

## 1. Introduction

### 1.1 Purpose of the Document

This System Architectural Requirements Document (TARD) serves as the comprehensive System blueprint for implementing the Multi-Agent Business Operating System (MABOS). It translates business requirements, product specifications, and user experience designs into detailed architectural specifications for software engineering implementation.

The document provides:
- Comprehensive system architecture design and component specifications
- Database schemas and implementation details for all data persistence layers
- Knowledge graph and ontology definitions for semantic reasoning capabilities
- Integration specifications for enterprise systems and external services
- Deployment architecture for cloud-native, scalable infrastructure
- Security architecture implementing zero-trust principles
- Performance, monitoring, and operational requirements

### 1.2 Scope of the Architecture

MABOS represents a revolutionary synthesis of theoretical rigor and practical utility, combining:

**Core Architectural Paradigms:**
- **BDI (Belief-Desire-Intention) Architecture:** Pure theoretical multi-agent reasoning
- **Workflow Orchestration:** Enterprise-grade process automation
- **Microservices Design:** Scalable, cloud-native service architecture
- **Event-Driven Architecture:** Real-time coordination and adaptation
- **Zero-Trust Security:** Enterprise-grade security and compliance

**System Scope:**
- Hybrid agent architecture supporting autonomous reasoning and declarative workflows
- Natural language processing for conversational workflow creation
- Secure sandbox execution environments for tool isolation
- Comprehensive enterprise system integration capabilities
- Real-time collaboration and monitoring systems
- Scalable deployment supporting 100,000+ concurrent users

### 1.3 Intended Audience

**Primary Audience:**
- **System Architects:** Detailed System architecture and design patterns
- **Software Engineers:** Implementation specifications and System requirements
- **DevOps Engineers:** Deployment, monitoring, and operational requirements
- **Security Engineers:** Security architecture and compliance specifications

**Secondary Audience:**
- **Product Managers:** System feasibility and implementation planning
- **QA Engineers:** Testing strategies and quality assurance requirements
- **System Leadership:** Architecture decisions and strategic System direction

---

## 2. System Architecture Overview

### 2.1 High-Level Architecture

<mermaid>
graph TB
    subgraph "User Interface Layer"
        WEB[Web Application<br/>React/TypeScript]
        MOBILE[Mobile Interface<br/>Responsive PWA]
        API_DOC[API Documentation<br/>OpenAPI/Swagger]
    end

    subgraph "API Gateway Layer"
        GATEWAY[API Gateway<br/>Kong/NGINX]
        LB[Load Balancer<br/>HAProxy]
        WAF[Web Application Firewall<br/>CloudFlare/AWS WAF]
    end

    subgraph "Core Services Layer"
        BDI[BDI Engine<br/>Python/FastAPI]
        WORKFLOW[Workflow Orchestrator<br/>Python/Celery]
        TOOL[Tool Executor<br/>Docker/Kubernetes]
        KNOWLEDGE[Knowledge Manager<br/>Neo4j/Owlready2]
        LLM[LLM Gateway<br/>Multi-Provider]
        AUTH[Auth Service<br/>JWT/RBAC]
    end

    subgraph "Data Layer"
        POSTGRES[(PostgreSQL<br/>Primary Database)]
        NEO4J[(Neo4j<br/>Knowledge Graph)]
        REDIS[(Redis<br/>Cache/Session)]
        ELASTIC[(Elasticsearch<br/>Search/Logs)]
    end

    subgraph "External Systems"
        ENTERPRISE[Enterprise Systems<br/>SAP/Salesforce/ServiceNow]
        LLMPROVIDERS[LLM Providers<br/>OpenAI/Claude/Gemini]
        MONITORING[Monitoring<br/>Prometheus/Grafana]
    end

    %% Connections
    WEB --> GATEWAY
    MOBILE --> GATEWAY
    GATEWAY --> LB
    LB --> WAF
    WAF --> BDI
    WAF --> WORKFLOW
    WAF --> TOOL
    WAF --> KNOWLEDGE
    WAF --> LLM
    WAF --> AUTH

    BDI --> POSTGRES
    BDI --> NEO4J
    BDI --> REDIS
    
    WORKFLOW --> POSTGRES
    WORKFLOW --> REDIS
    WORKFLOW --> ELASTIC
    
    TOOL --> POSTGRES
    TOOL --> REDIS
    
    KNOWLEDGE --> NEO4J
    KNOWLEDGE --> POSTGRES
    
    LLM --> REDIS
    LLM --> LLMPROVIDERS
    
    AUTH --> POSTGRES
    AUTH --> REDIS

    BDI -.-> ENTERPRISE
    WORKFLOW -.-> ENTERPRISE
    TOOL -.-> ENTERPRISE

    %% Monitoring connections
    BDI -.-> MONITORING
    WORKFLOW -.-> MONITORING
    TOOL -.-> MONITORING
    KNOWLEDGE -.-> MONITORING
    LLM -.-> MONITORING
    AUTH -.-> MONITORING
</mermaid>

### 2.2 Key Components and Interactions

**Frontend Layer:**
- **Web Application:** React/TypeScript SPA with comprehensive workflow management interface
- **Mobile Interface:** Progressive Web App with responsive design for monitoring and basic management
- **API Documentation:** Interactive OpenAPI documentation for developer integration

**Service Layer:**
- **BDI Engine:** Core multi-agent reasoning system implementing Belief-Desire-Intention architecture
- **Workflow Orchestrator:** Enterprise workflow execution engine with YAML-based definitions
- **Tool Executor:** Secure sandbox environment for isolated tool execution
- **Knowledge Manager:** Semantic knowledge representation and ontology management
- **LLM Gateway:** Multi-provider language model integration with intelligent routing
- **Auth Service:** Authentication, authorization, and user management

**Data Layer:**
- **PostgreSQL:** Primary transactional database for user data, workflows, and system metadata
- **Neo4j:** Graph database for knowledge representation, agent relationships, and ontologies
- **Redis:** High-performance caching and session storage with message queuing capabilities
- **Elasticsearch:** Full-text search, log aggregation, and analytics platform

### 2.3 Design Principles and Patterns

**Architectural Patterns:**
1. **Microservices Architecture:** Independent, loosely-coupled services with clear boundaries
2. **Event-Driven Architecture:** Asynchronous communication using message queues and events
3. **CQRS (Command Query Responsibility Segregation):** Separate read and write operations for optimal performance
4. **Domain-Driven Design:** Business domain modeling with bounded contexts
5. **Hexagonal Architecture:** Clean separation of business logic from external dependencies

**Design Principles:**
1. **Scalability First:** Horizontal scaling capabilities built into every component
2. **Security by Design:** Zero-trust security model with defense in depth
3. **Performance Optimization:** Sub-100ms response times with intelligent caching
4. **Fault Tolerance:** Graceful degradation and automatic recovery mechanisms
5. **Observability:** Comprehensive monitoring, logging, and tracing throughout the system

---

## 3. Detailed Component Descriptions

### 3.1 BDI Engine Service

**Purpose and Responsibilities:**
The BDI Engine implements the core Belief-Desire-Intention architecture, providing autonomous agent reasoning capabilities that enable intelligent workflow adaptation and optimization.

**Key Functionalities:**
- Agent lifecycle management (creation, execution, termination)
- Belief state management and environmental perception
- Goal decomposition and plan generation
- Intention execution and monitoring
- Meta-reasoning capabilities for system self-optimization

**Interfaces and Dependencies:**
```python
# BDI Agent Interface Definition
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Belief:
    predicate: str
    parameters: Dict[str, Any]
    confidence: float
    timestamp: datetime

@dataclass
class Desire:
    goal_id: str
    description: str
    priority: int
    constraints: Dict[str, Any]

@dataclass
class Intention:
    plan_id: str
    actions: List[Dict[str, Any]]
    status: str
    progress: float

class BDIAgent(ABC):
    """Core BDI Agent interface implementing theoretical agent architecture"""
    
    def __init__(self, agent_id: str, knowledge_base: 'KnowledgeBase'):
        self.agent_id = agent_id
        self.beliefs: List[Belief] = []
        self.desires: List[Desire] = []
        self.intentions: List[Intention] = []
        self.knowledge_base = knowledge_base
    
    @abstractmethod
    async def perceive_environment(self) -> List[Belief]:
        """Update beliefs based on environmental perception"""
        pass
    
    @abstractmethod
    async def generate_desires(self) -> List[Desire]:
        """Generate desires based on current beliefs and goals"""
        pass
    
    @abstractmethod
    async def plan_actions(self, desires: List[Desire]) -> List[Intention]:
        """Generate action plans to achieve desires"""
        pass
    
    @abstractmethod
    async def execute_intentions(self) -> None:
        """Execute planned actions and monitor progress"""
        pass
```

**Data Flow:**
1. **Environmental Perception:** Agents continuously monitor workflow execution status, system metrics, and external events
2. **Belief Update:** New information updates the agent's belief state about the world
3. **Goal Assessment:** Agents evaluate current desires against updated beliefs
4. **Plan Generation:** Create or modify action plans to achieve goals
5. **Intention Execution:** Execute planned actions through workflow orchestrator

**Security Considerations:**
- Agent isolation prevents interference between different user contexts
- Capability-based security limits agent actions to authorized operations
- Audit logging captures all agent decisions and actions for compliance

**Scalability and Performance Considerations:**
- Horizontal scaling through agent clustering and load distribution
- Belief state optimization using incremental updates and selective reasoning
- Caching of frequently accessed knowledge and reasoning results

### 3.2 Workflow Orchestrator Service

**Purpose and Responsibilities:**
Enterprise-grade workflow execution engine that translates high-level business processes into executable automation sequences while integrating with BDI agent reasoning.

**Key Functionalities:**
- YAML-based workflow definition parsing and validation
- Dynamic workflow execution with real-time adaptation
- Task scheduling and dependency management
- Integration with enterprise systems and external APIs
- Workflow versioning and rollback capabilities

**Interfaces and Dependencies:**
```python
# Workflow Definition Schema
from pydantic import BaseModel
from typing import Union, Dict, List, Any, Optional
from enum import Enum

class TaskType(str, Enum):
    HTTP_REQUEST = "http_request"
    EMAIL_SEND = "email_send"
    DATA_TRANSFORM = "data_transform"
    AGENT_DECISION = "agent_decision"
    CONDITIONAL = "conditional"
    LOOP = "loop"

class WorkflowTask(BaseModel):
    task_id: str
    task_type: TaskType
    parameters: Dict[str, Any]
    dependencies: List[str] = []
    retry_policy: Optional[Dict[str, Any]] = None
    timeout: int = 300

class WorkflowDefinition(BaseModel):
    workflow_id: str
    name: str
    description: str
    version: str
    tasks: List[WorkflowTask]
    triggers: List[Dict[str, Any]]
    metadata: Dict[str, Any] = {}

class WorkflowExecution(BaseModel):
    execution_id: str
    workflow_id: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    context: Dict[str, Any] = {}

class WorkflowOrchestrator:
    """Core workflow execution engine with BDI integration"""
    
    def __init__(self, bdi_engine, tool_executor):
        self.bdi_engine = bdi_engine
        self.tool_executor = tool_executor
        self.active_workflows: Dict[str, WorkflowExecution] = {}
    
    async def execute_workflow(self, definition: WorkflowDefinition, 
                              context: Dict[str, Any]) -> WorkflowExecution:
        """Execute workflow with BDI agent oversight"""
        execution = WorkflowExecution(
            execution_id=f"exec_{uuid.uuid4()}",
            workflow_id=definition.workflow_id,
            status="running",
            started_at=datetime.utcnow(),
            context=context
        )
        
        # Create oversight agent for this workflow
        agent = await self.bdi_engine.create_workflow_agent(execution)
        
        try:
            await self._execute_tasks(execution, agent)
            execution.status = "completed"
            execution.completed_at = datetime.utcnow()
        except Exception as e:
            execution.status = "failed"
            execution.error = str(e)
            execution.completed_at = datetime.utcnow()
            await agent.handle_failure(e)
        
        return execution
```

**Data Flow:**
1. **Workflow Definition:** YAML workflows parsed into executable task graphs
2. **Dependency Resolution:** Task dependencies analyzed for optimal execution order
3. **Agent Assignment:** BDI agents created to oversee workflow execution
4. **Task Execution:** Individual tasks executed through tool executor
5. **Progress Monitoring:** Real-time status updates and agent-driven adaptations

**Security Considerations:**
- Workflow isolation using containerized execution environments
- Parameter validation and sanitization to prevent injection attacks
- Access control integration with enterprise authentication systems
- Encrypted storage of sensitive workflow parameters and results

**Scalability and Performance Considerations:**
- Async task execution with configurable concurrency limits
- Distributed workflow execution across multiple orchestrator instances
- Intelligent load balancing based on workflow complexity and resource requirements

### 3.3 Tool Executor Service

**Purpose and Responsibilities:**
Secure sandbox execution environment that provides isolated tool execution capabilities while maintaining enterprise-grade security and performance.

**Key Functionalities:**
- Docker container-based tool isolation
- Resource management and monitoring
- Tool plugin system with standardized interfaces
- Security scanning and threat detection
- Performance optimization and caching

**Interfaces and Dependencies:**
```python
# Tool Execution Framework
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import docker
import asyncio
from pydantic import BaseModel

class ToolResult(BaseModel):
    success: bool
    result: Any
    error: Optional[str] = None
    execution_time: float
    resource_usage: Dict[str, float]

class SecurityPolicy(BaseModel):
    allowed_domains: List[str] = []
    blocked_domains: List[str] = []
    max_execution_time: int = 300
    max_memory_mb: int = 512
    max_cpu_percent: int = 50
    network_access: bool = True

class BaseTool(ABC):
    """Abstract base class for all executable tools"""
    
    def __init__(self, tool_id: str, security_policy: SecurityPolicy):
        self.tool_id = tool_id
        self.security_policy = security_policy
    
    @abstractmethod
    async def execute(self, parameters: Dict[str, Any], 
                     context: Dict[str, Any]) -> ToolResult:
        """Execute tool with given parameters in isolated environment"""
        pass
    
    @abstractmethod
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validate input parameters before execution"""
        pass

class ToolExecutor:
    """Secure tool execution service with container isolation"""
    
    def __init__(self):
        self.docker_client = docker.from_env()
        self.tool_registry: Dict[str, BaseTool] = {}
        self.active_executions: Dict[str, asyncio.Task] = {}
    
    async def execute_tool(self, tool_id: str, parameters: Dict[str, Any],
                          security_policy: SecurityPolicy) -> ToolResult:
        """Execute tool in secure container environment"""
        
        # Validate tool exists and parameters are safe
        if tool_id not in self.tool_registry:
            raise ValueError(f"Tool {tool_id} not registered")
        
        tool = self.tool_registry[tool_id]
        if not tool.validate_parameters(parameters):
            raise ValueError("Invalid tool parameters")
        
        # Create isolated container for execution
        container_config = self._create_container_config(security_policy)
        
        try:
            # Execute in container with monitoring
            result = await self._execute_in_container(
                tool, parameters, container_config
            )
            return result
        finally:
            # Cleanup container resources
            await self._cleanup_container(container_config['container_id'])
```

**Data Flow:**
1. **Tool Registration:** Available tools registered with security policies and capabilities
2. **Execution Request:** Workflow orchestrator requests tool execution with parameters
3. **Container Creation:** Isolated Docker container created with security constraints
4. **Tool Execution:** Tool executed within container with resource monitoring
5. **Result Collection:** Results collected and returned with execution metadata

**Security Considerations:**
- Complete container isolation with no shared resources
- Network segmentation with configurable access policies
- Resource limits prevent resource exhaustion attacks
- Security scanning of tool inputs and outputs
- Audit logging of all tool executions with forensic capabilities

**Scalability and Performance Considerations:**
- Container pool management for reduced startup latency
- Horizontal scaling across multiple executor nodes
- Intelligent resource allocation based on tool requirements
- Caching of tool results for frequently executed operations

---

## 4. Database Schema and Implementation

### 4.1 Entity-Relationship Diagram

<mermaid>
erDiagram
    USERS {
        uuid user_id PK
        string email UK
        string password_hash
        string first_name
        string last_name
        string role
        timestamp created_at
        timestamp updated_at
        boolean is_active
        json preferences
    }
    
    ORGANIZATIONS {
        uuid org_id PK
        string name
        string domain
        json settings
        timestamp created_at
        timestamp updated_at
    }
    
    WORKFLOWS {
        uuid workflow_id PK
        uuid user_id FK
        uuid org_id FK
        string name
        text description
        string version
        json definition
        string status
        timestamp created_at
        timestamp updated_at
        json metadata
    }
    
    WORKFLOW_EXECUTIONS {
        uuid execution_id PK
        uuid workflow_id FK
        uuid user_id FK
        string status
        timestamp started_at
        timestamp completed_at
        json context
        text error_message
        json metrics
    }
    
    TASKS {
        uuid task_id PK
        uuid workflow_id FK
        string name
        string task_type
        json parameters
        json dependencies
        string status
        timestamp created_at
        timestamp updated_at
    }
    
    TASK_EXECUTIONS {
        uuid task_execution_id PK
        uuid execution_id FK
        uuid task_id FK
        uuid agent_id FK
        string status
        timestamp started_at
        timestamp completed_at
        json result
        text error_message
        json resource_usage
    }
    
    BDI_AGENTS {
        uuid agent_id PK
        uuid user_id FK
        uuid workflow_id FK
        string name
        string agent_type
        string status
        json knowledge_base
        timestamp created_at
        timestamp last_active
    }
    
    AGENT_BELIEFS {
        uuid belief_id PK
        uuid agent_id FK
        string predicate
        json parameters
        float confidence
        timestamp created_at
        timestamp expires_at
    }
    
    AGENT_DESIRES {
        uuid desire_id PK
        uuid agent_id FK
        string goal_id
        text description
        int priority
        json constraints
        string status
        timestamp created_at
    }
    
    AGENT_INTENTIONS {
        uuid intention_id PK
        uuid agent_id FK
        string plan_id
        json actions
        string status
        float progress
        timestamp created_at
        timestamp updated_at
    }
    
    INTEGRATIONS {
        uuid integration_id PK
        uuid org_id FK
        string name
        string system_type
        json configuration
        json credentials_encrypted
        string status
        timestamp created_at
        timestamp last_sync
    }
    
    AUDIT_LOGS {
        uuid log_id PK
        uuid user_id FK
        string action
        string resource_type
        string resource_id
        json details
        string ip_address
        string user_agent
        timestamp created_at
    }

    USERS ||--o{ WORKFLOWS : creates
    USERS ||--o{ BDI_AGENTS : owns
    USERS ||--o{ AUDIT_LOGS : generates
    ORGANIZATIONS ||--o{ USERS : contains
    ORGANIZATIONS ||--o{ WORKFLOWS : owns
    ORGANIZATIONS ||--o{ INTEGRATIONS : configures
    WORKFLOWS ||--o{ TASKS : contains
    WORKFLOWS ||--o{ WORKFLOW_EXECUTIONS : executes
    WORKFLOWS ||--o{ BDI_AGENTS : manages
    WORKFLOW_EXECUTIONS ||--o{ TASK_EXECUTIONS : includes
    TASKS ||--o{ TASK_EXECUTIONS : instances
    BDI_AGENTS ||--o{ AGENT_BELIEFS : maintains
    BDI_AGENTS ||--o{ AGENT_DESIRES : pursues
    BDI_AGENTS ||--o{ AGENT_INTENTIONS : plans
    BDI_AGENTS ||--o{ TASK_EXECUTIONS : executes
</mermaid>

### 4.2 PostgreSQL Table Definitions

<code language="sql">
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    preferences JSONB DEFAULT '{}',
    CONSTRAINT valid_role CHECK (role IN ('admin', 'user', 'viewer'))
);

-- Organizations table
CREATE TABLE organizations (
    org_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255) UNIQUE NOT NULL,
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- User-Organization relationship
CREATE TABLE user_organizations (
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    org_id UUID REFERENCES organizations(org_id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL DEFAULT 'member',
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, org_id)
);

-- Workflows table
CREATE TABLE workflows (
    workflow_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    org_id UUID NOT NULL REFERENCES organizations(org_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    version VARCHAR(50) NOT NULL DEFAULT '1.0.0',
    definition JSONB NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'draft',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}',
    CONSTRAINT valid_status CHECK (status IN ('draft', 'active', 'inactive', 'archived'))
);

-- Workflow executions table
CREATE TABLE workflow_executions (
    execution_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID NOT NULL REFERENCES workflows(workflow_id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    context JSONB DEFAULT '{}',
    error_message TEXT,
    metrics JSONB DEFAULT '{}',
    CONSTRAINT valid_execution_status CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled'))
);

-- Tasks table
CREATE TABLE tasks (
    task_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID NOT NULL REFERENCES workflows(workflow_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    task_type VARCHAR(100) NOT NULL,
    parameters JSONB NOT NULL DEFAULT '{}',
    dependencies JSONB DEFAULT '[]',
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_task_status CHECK (status IN ('pending', 'ready', 'running', 'completed', 'failed', 'skipped'))
);

-- Task executions table
CREATE TABLE task_executions (
    task_execution_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    execution_id UUID NOT NULL REFERENCES workflow_executions(execution_id) ON DELETE CASCADE,
    task_id UUID NOT NULL REFERENCES tasks(task_id) ON DELETE CASCADE,
    agent_id UUID, -- FK to BDI agents, nullable for non-agent tasks
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    result JSONB,
    error_message TEXT,
    resource_usage JSONB DEFAULT '{}',
    CONSTRAINT valid_task_execution_status CHECK (status IN ('pending', 'running', 'completed', 'failed', 'retrying'))
);

-- BDI Agents table
CREATE TABLE bdi_agents (
    agent_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    workflow_id UUID REFERENCES workflows(workflow_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    agent_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'inactive',
    knowledge_base JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_agent_status CHECK (status IN ('inactive', 'active', 'suspended', 'terminated'))
);

-- Agent beliefs table
CREATE TABLE agent_beliefs (
    belief_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID NOT NULL REFERENCES bdi_agents(agent_id) ON DELETE CASCADE,
    predicate VARCHAR(255) NOT NULL,
    parameters JSONB NOT NULL DEFAULT '{}',
    confidence DECIMAL(3,2) NOT NULL DEFAULT 1.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT valid_confidence CHECK (confidence >= 0.0 AND confidence <= 1.0)
);

-- Agent desires table
CREATE TABLE agent_desires (
    desire_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID NOT NULL REFERENCES bdi_agents(agent_id) ON DELETE CASCADE,
    goal_id VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    priority INTEGER NOT NULL DEFAULT 5,
    constraints JSONB DEFAULT '{}',
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_priority CHECK (priority >= 1 AND priority <= 10),
    CONSTRAINT valid_desire_status CHECK (status IN ('active', 'achieved', 'abandoned', 'blocked'))
);

-- Agent intentions table
CREATE TABLE agent_intentions (
    intention_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID NOT NULL REFERENCES bdi_agents(agent_id) ON DELETE CASCADE,
    plan_id VARCHAR(255) NOT NULL,
    actions JSONB NOT NULL DEFAULT '[]',
    status VARCHAR(50) NOT NULL DEFAULT 'planning',
    progress DECIMAL(3,2) NOT NULL DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_progress CHECK (progress >= 0.0 AND progress <= 1.0),
    CONSTRAINT valid_intention_status CHECK (status IN ('planning', 'executing', 'completed', 'failed', 'suspended'))
);

-- Integrations table
CREATE TABLE integrations (
    integration_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID NOT NULL REFERENCES organizations(org_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    system_type VARCHAR(100) NOT NULL,
    configuration JSONB NOT NULL DEFAULT '{}',
    credentials_encrypted BYTEA, -- Encrypted credentials
    status VARCHAR(50) NOT NULL DEFAULT 'inactive',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_sync TIMESTAMP WITH TIME ZONE,
    CONSTRAINT valid_integration_status CHECK (status IN ('inactive', 'active', 'error', 'disabled'))
);

-- Audit logs table
CREATE TABLE audit_logs (
    log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100) NOT NULL,
    resource_id VARCHAR(255),
    details JSONB DEFAULT '{}',
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Add foreign key constraint for task_executions to bdi_agents
ALTER TABLE task_executions 
ADD CONSTRAINT fk_task_executions_agent 
FOREIGN KEY (agent_id) REFERENCES bdi_agents(agent_id) ON DELETE SET NULL;

-- Indexes for performance optimization
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_org ON users((preferences->>'default_org_id'));
CREATE INDEX idx_workflows_user_org ON workflows(user_id, org_id);
CREATE INDEX idx_workflows_status ON workflows(status);
CREATE INDEX idx_workflow_executions_workflow ON workflow_executions(workflow_id);
CREATE INDEX idx_workflow_executions_status ON workflow_executions(status);
CREATE INDEX idx_workflow_executions_user_date ON workflow_executions(user_id, started_at DESC);
CREATE INDEX idx_tasks_workflow ON tasks(workflow_id);
CREATE INDEX idx_task_executions_execution ON task_executions(execution_id);
CREATE INDEX idx_task_executions_agent ON task_executions(agent_id);
CREATE INDEX idx_bdi_agents_user ON bdi_agents(user_id);
CREATE INDEX idx_bdi_agents_workflow ON bdi_agents(workflow_id);
CREATE INDEX idx_bdi_agents_status ON bdi_agents(status);
CREATE INDEX idx_agent_beliefs_agent ON agent_beliefs(agent_id);
CREATE INDEX idx_agent_beliefs_predicate ON agent_beliefs(predicate);
CREATE INDEX idx_agent_desires_agent ON agent_desires(agent_id);
CREATE INDEX idx_agent_desires_status ON agent_desires(status);
CREATE INDEX idx_agent_intentions_agent ON agent_intentions(agent_id);
CREATE INDEX idx_agent_intentions_status ON agent_intentions(status);
CREATE INDEX idx_integrations_org ON integrations(org_id);
CREATE INDEX idx_integrations_type ON integrations(system_type);
CREATE INDEX idx_audit_logs_user_date ON audit_logs(user_id, created_at DESC);
CREATE INDEX idx_audit_logs_resource ON audit_logs(resource_type, resource_id);

-- GIN indexes for JSONB columns
CREATE INDEX idx_workflows_definition_gin ON workflows USING GIN (definition);
CREATE INDEX idx_workflows_metadata_gin ON workflows USING GIN (metadata);
CREATE INDEX idx_workflow_executions_context_gin ON workflow_executions USING GIN (context);
CREATE INDEX idx_tasks_parameters_gin ON tasks USING GIN (parameters);
CREATE INDEX idx_bdi_agents_knowledge_gin ON bdi_agents USING GIN (knowledge_base);
CREATE INDEX idx_agent_beliefs_parameters_gin ON agent_beliefs USING GIN (parameters);
CREATE INDEX idx_integrations_config_gin ON integrations USING GIN (configuration);
</code>

### 4.3 Indexing Strategy

**Primary Indexes:**
- **B-tree indexes** on frequently queried columns (user_id, workflow_id, status fields)
- **Unique indexes** on email addresses and domain names for data integrity
- **Composite indexes** for multi-column queries (user_id + org_id, user_id + created_at)

**JSONB Indexes:**
- **GIN indexes** on JSONB columns for efficient JSON query operations
- **Partial indexes** on specific JSONB keys for frequently accessed data
- **Expression indexes** on commonly extracted JSON values

**Performance Considerations:**
- **Partitioning** large tables (audit_logs, workflow_executions) by date
- **Connection pooling** to manage database connections efficiently
- **Read replicas** for separating read and write operations
- **Query plan optimization** using EXPLAIN ANALYZE for complex queries

---

## 5. Knowledge Graph / Ontology

### 5.1 Ontology Structure Diagram

<mermaid>
graph TB
    subgraph "Core Ontology Classes"
        Agent[Agent<br/>- hasBeliefs<br/>- hasDesires<br/>- hasIntentions<br/>- participatesIn]
        Workflow[Workflow<br/>- hasTask<br/>- hasExecution<br/>- definedBy<br/>- triggeredBy]
        Task[Task<br/>- hasType<br/>- dependsOn<br/>- executedBy<br/>- hasParameters]
        Knowledge[Knowledge<br/>- hasPredicate<br/>- hasConfidence<br/>- validUntil<br/>- derivedFrom]
    end
    
    subgraph "BDI Mental States"
        Belief[Belief<br/>- believedBy<br/>- aboutWorld<br/>- hasEvidence]
        Desire[Desire<br/>- desiredBy<br/>- hasGoal<br/>- hasPriority]
        Intention[Intention<br/>- intendedBy<br/>- planFor<br/>- hasAction]
    end
    
    subgraph "Enterprise Integration"
        System[EnterpriseSystem<br/>- hasEndpoint<br/>- providesData<br/>- requiresAuth]
        Integration[Integration<br/>- connectsTo<br/>- hasCredentials<br/>- supportsOps]
        Data[BusinessData<br/>- hasSchema<br/>- belongsTo<br/>- updatedAt]
    end
    
    subgraph "Execution Context"
        Execution[Execution<br/>- instanceOf<br/>- hasStatus<br/>- startedAt<br/>- hasResult]
        Environment[Environment<br/>- hasState<br/>- influences<br/>- observedBy]
        Context[Context<br/>- providesInfo<br/>- relevantTo<br/>- hasValue]
    end

    %% Relationships
    Agent --> Belief : hasBeliefs
    Agent --> Desire : hasDesires  
    Agent --> Intention : hasIntentions
    Agent --> Workflow : participatesIn
    Agent --> Knowledge : possesses
    
    Workflow --> Task : hasTask
    Workflow --> Execution : hasExecution
    Task --> Agent : executedBy
    Task --> Task : dependsOn
    
    Belief --> Knowledge : basedOn
    Desire --> Knowledge : motivatedBy
    Intention --> Knowledge : planBasedOn
    
    System --> Integration : connectsTo
    Integration --> Data : accessesData
    Data --> Context : providesContext
    
    Execution --> Environment : operatesIn
    Environment --> Context : hasContext
    Context --> Knowledge : contributesTo
</mermaid>

### 5.2 OWL Ontology Definition

<code language="owl">
@prefix mabos: <http://mabos.ai/ontology#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix time: <http://www.w3.org/2006/time#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

# Ontology Declaration
mabos: rdf:type owl:Ontology ;
    owl:versionIRI <http://mabos.ai/ontology/1.0> ;
    rdfs:label "MABOS Multi-Agent Business Operating System Ontology"@en ;
    rdfs:comment "Formal ontology for BDI agents, workflows, and enterprise integration"@en ;
    owl:versionInfo "1.0" .

# Core Agent Classes
mabos:Agent rdf:type owl:Class ;
    rdfs:label "BDI Agent"@en ;
    rdfs:comment "Autonomous agent implementing Belief-Desire-Intention architecture"@en ;
    rdfs:subClassOf foaf:Agent .

mabos:WorkflowAgent rdf:type owl:Class ;
    rdfs:label "Workflow Agent"@en ;
    rdfs:comment "Specialized agent for workflow orchestration and monitoring"@en ;
    rdfs:subClassOf mabos:Agent .

mabos:MetaAgent rdf:type owl:Class ;
    rdfs:label "Meta Agent"@en ;
    rdfs:comment "Agent responsible for system optimization and meta-reasoning"@en ;
    rdfs:subClassOf mabos:Agent .

# Mental State Classes (BDI)
mabos:MentalState rdf:type owl:Class ;
    rdfs:label "Mental State"@en ;
    rdfs:comment "Abstract class for agent mental states"@en .

mabos:Belief rdf:type owl:Class ;
    rdfs:label "Belief"@en ;
    rdfs:comment "Agent's belief about the world state"@en ;
    rdfs:subClassOf mabos:MentalState .

mabos:Desire rdf:type owl:Class ;
    rdfs:label "Desire"@en ;
    rdfs:comment "Agent's goal or desired future state"@en ;
    rdfs:subClassOf mabos:MentalState .

mabos:Intention rdf:type owl:Class ;
    rdfs:label "Intention"@en ;
    rdfs:comment "Agent's commitment to execute a plan"@en ;
    rdfs:subClassOf mabos:MentalState .

# Workflow and Task Classes
mabos:Workflow rdf:type owl:Class ;
    rdfs:label "Workflow"@en ;
    rdfs:comment "Business process automation workflow"@en .

mabos:Task rdf:type owl:Class ;
    rdfs:label "Task"@en ;
    rdfs:comment "Individual task within a workflow"@en .

mabos:ConditionalTask rdf:type owl:Class ;
    rdfs:label "Conditional Task"@en ;
    rdfs:comment "Task that executes based on conditions"@en ;
    rdfs:subClassOf mabos:Task .

mabos:LoopTask rdf:type owl:Class ;
    rdfs:label "Loop Task"@en ;
    rdfs:comment "Task that repeats based on criteria"@en ;
    rdfs:subClassOf mabos:Task .

mabos:AgentTask rdf:type owl:Class ;
    rdfs:label "Agent Task"@en ;
    rdfs:comment "Task requiring agent decision-making"@en ;
    rdfs:subClassOf mabos:Task .

# Execution and Context Classes
mabos:Execution rdf:type owl:Class ;
    rdfs:label "Execution"@en ;
    rdfs:comment "Runtime instance of workflow or task"@en .

mabos:ExecutionContext rdf:type owl:Class ;
    rdfs:label "Execution Context"@en ;
    rdfs:comment "Environmental context for workflow execution"@en .

mabos:Environment rdf:type owl:Class ;
    rdfs:label "Environment"@en ;
    rdfs:comment "External environment observable by agents"@en .

# Knowledge and Information Classes
mabos:Knowledge rdf:type owl:Class ;
    rdfs:label "Knowledge"@en ;
    rdfs:comment "Structured knowledge representation"@en .

mabos:DomainKnowledge rdf:type owl:Class ;
    rdfs:label "Domain Knowledge"@en ;
    rdfs:comment "Domain-specific business knowledge"@en ;
    rdfs:subClassOf mabos:Knowledge .

mabos:ProceduralKnowledge rdf:type owl:Class ;
    rdfs:label "Procedural Knowledge"@en ;
    rdfs:comment "Knowledge about how to perform tasks"@en ;
    rdfs:subClassOf mabos:Knowledge .

# Enterprise Integration Classes
mabos:EnterpriseSystem rdf:type owl:Class ;
    rdfs:label "Enterprise System"@en ;
    rdfs:comment "External enterprise system for integration"@en .

mabos:Integration rdf:type owl:Class ;
    rdfs:label "Integration"@en ;
    rdfs:comment "Connection to external enterprise system"@en .

mabos:BusinessData rdf:type owl:Class ;
    rdfs:label "Business Data"@en ;
    rdfs:comment "Data from enterprise business systems"@en .

# Object Properties (Relationships)

# Agent Mental State Properties
mabos:hasBeliefs rdf:type owl:ObjectProperty ;
    rdfs:label "has beliefs"@en ;
    rdfs:domain mabos:Agent ;
    rdfs:range mabos:Belief .

mabos:hasDesires rdf:type owl:ObjectProperty ;
    rdfs:label "has desires"@en ;
    rdfs:domain mabos:Agent ;
    rdfs:range mabos:Desire .

mabos:hasIntentions rdf:type owl:ObjectProperty ;
    rdfs:label "has intentions"@en ;
    rdfs:domain mabos:Agent ;
    rdfs:range mabos:Intention .

# Workflow Relationships
mabos:participatesIn rdf:type owl:ObjectProperty ;
    rdfs:label "participates in"@en ;
    rdfs:domain mabos:Agent ;
    rdfs:range mabos:Workflow .

mabos:hasTask rdf:type owl:ObjectProperty ;
    rdfs:label "has task"@en ;
    rdfs:domain mabos:Workflow ;
    rdfs:range mabos:Task .

mabos:dependsOn rdf:type owl:ObjectProperty ;
    rdfs:label "depends on"@en ;
    rdfs:domain mabos:Task ;
    rdfs:range mabos:Task ;
    rdfs:comment "Task dependency relationship"@en .

mabos:executedBy rdf:type owl:ObjectProperty ;
    rdfs:label "executed by"@en ;
    rdfs:domain mabos:Task ;
    rdfs:range mabos:Agent .

mabos:hasExecution rdf:type owl:ObjectProperty ;
    rdfs:label "has execution"@en ;
    rdfs:domain mabos:Workflow ;
    rdfs:range mabos:Execution .

# Knowledge Relationships
mabos:possessesKnowledge rdf:type owl:ObjectProperty ;
    rdfs:label "possesses knowledge"@en ;
    rdfs:domain mabos:Agent ;
    rdfs:range mabos:Knowledge .

mabos:basedOn rdf:type owl:ObjectProperty ;
    rdfs:label "based on"@en ;
    rdfs:domain mabos:Belief ;
    rdfs:range mabos:Knowledge .

mabos:motivatedBy rdf:type owl:ObjectProperty ;
    rdfs:label "motivated by"@en ;
    rdfs:domain mabos:Desire ;
    rdfs:range mabos:Knowledge .

# Integration Relationships
mabos:connectsTo rdf:type owl:ObjectProperty ;
    rdfs:label "connects to"@en ;
    rdfs:domain mabos:Integration ;
    rdfs:range mabos:EnterpriseSystem .

mabos:accessesData rdf:type owl:ObjectProperty ;
    rdfs:label "accesses data"@en ;
    rdfs:domain mabos:Integration ;
    rdfs:range mabos:BusinessData .

mabos:operatesIn rdf:type owl:ObjectProperty ;
    rdfs:label "operates in"@en ;
    rdfs:domain mabos:Execution ;
    rdfs:range mabos:Environment .

# Data Properties (Attributes)

# Agent Properties
mabos:agentID rdf:type owl:DatatypeProperty ;
    rdfs:label "agent ID"@en ;
    rdfs:domain mabos:Agent ;
    rdfs:range xsd:string .

mabos:agentType rdf:type owl:DatatypeProperty ;
    rdfs:label "agent type"@en ;
    rdfs:domain mabos:Agent ;
    rdfs:range xsd:string .

mabos:agentStatus rdf:type owl:DatatypeProperty ;
    rdfs:label "agent status"@en ;
    rdfs:domain mabos:Agent ;
    rdfs:range xsd:string .

mabos:lastActive rdf:type owl:DatatypeProperty ;
    rdfs:label "last active"@en ;
    rdfs:domain mabos:Agent ;
    rdfs:range xsd:dateTime .

# Mental State Properties
mabos:confidence rdf:type owl:DatatypeProperty ;
    rdfs:label "confidence"@en ;
    rdfs:domain mabos:Belief ;
    rdfs:range xsd:float ;
    rdfs:comment "Confidence level between 0.0 and 1.0"@en .

mabos:priority rdf:type owl:DatatypeProperty ;
    rdfs:label "priority"@en ;
    rdfs:domain mabos:Desire ;
    rdfs:range xsd:integer ;
    rdfs:comment "Priority level from 1 (lowest) to 10 (highest)"@en .

mabos:progress rdf:type owl:DatatypeProperty ;
    rdfs:label "progress"@en ;
    rdfs:domain mabos:Intention ;
    rdfs:range xsd:float ;
    rdfs:comment "Execution progress between 0.0 and 1.0"@en .

mabos:predicate rdf:type owl:DatatypeProperty ;
    rdfs:label "predicate"@en ;
    rdfs:domain mabos:Belief ;
    rdfs:range xsd:string .

mabos:goalDescription rdf:type owl:DatatypeProperty ;
    rdfs:label "goal description"@en ;
    rdfs:domain mabos:Desire ;
    rdfs:range xsd:string .

mabos:planID rdf:type owl:DatatypeProperty ;
    rdfs:label "plan ID"@en ;
    rdfs:domain mabos:Intention ;
    rdfs:range xsd:string .

# Workflow Properties
mabos:workflowName rdf:type owl:DatatypeProperty ;
    rdfs:label "workflow name"@en ;
    rdfs:domain mabos:Workflow ;
    rdfs:range xsd:string .

mabos:workflowVersion rdf:type owl:DatatypeProperty ;
    rdfs:label "workflow version"@en ;
    rdfs:domain mabos:Workflow ;
    rdfs:range xsd:string .

mabos:workflowStatus rdf:type owl:DatatypeProperty ;
    rdfs:label "workflow status"@en ;
    rdfs:domain mabos:Workflow ;
    rdfs:range xsd:string .

# Task Properties
mabos:taskName rdf:type owl:DatatypeProperty ;
    rdfs:label "task name"@en ;
    rdfs:domain mabos:Task ;
    rdfs:range xsd:string .

mabos:taskType rdf:type owl:DatatypeProperty ;
    rdfs:label "task type"@en ;
    rdfs:domain mabos:Task ;
    rdfs:range xsd:string .

mabos:taskStatus rdf:type owl:DatatypeProperty ;
    rdfs:label "task status"@en ;
    rdfs:domain mabos:Task ;
    rdfs:range xsd:string .

mabos:timeout rdf:type owl:DatatypeProperty ;
    rdfs:label "timeout"@en ;
    rdfs:domain mabos:Task ;
    rdfs:range xsd:integer ;
    rdfs:comment "Task timeout in seconds"@en .

# Execution Properties
mabos:executionStatus rdf:type owl:DatatypeProperty ;
    rdfs:label "execution status"@en ;
    rdfs:domain mabos:Execution ;
    rdfs:range xsd:string .

mabos:startTime rdf:type owl:DatatypeProperty ;
    rdfs:label "start time"@en ;
    rdfs:domain mabos:Execution ;
    rdfs:range xsd:dateTime .

mabos:endTime rdf:type owl:DatatypeProperty ;
    rdfs:label "end time"@en ;
    rdfs:domain mabos:Execution ;
    rdfs:range xsd:dateTime .

mabos:executionDuration rdf:type owl:DatatypeProperty ;
    rdfs:label "execution duration"@en ;
    rdfs:domain mabos:Execution ;
    rdfs:range xsd:duration .

# Enterprise System Properties
mabos:systemName rdf:type owl:DatatypeProperty ;
    rdfs:label "system name"@en ;
    rdfs:domain mabos:EnterpriseSystem ;
    rdfs:range xsd:string .

mabos:systemType rdf:type owl:DatatypeProperty ;
    rdfs:label "system type"@en ;
    rdfs:domain mabos:EnterpriseSystem ;
    rdfs:range xsd:string .

mabos:apiEndpoint rdf:type owl:DatatypeProperty ;
    rdfs:label "API endpoint"@en ;
    rdfs:domain mabos:EnterpriseSystem ;
    rdfs:range xsd:anyURI .

# Constraints and Rules

# Agent must have at least one mental state
mabos:Agent rdfs:subClassOf [
    rdf:type owl:Restriction ;
    owl:onProperty mabos:hasBeliefs ;
    owl:minCardinality "1"^^xsd:nonNegativeInteger
] .

# Workflow must have at least one task
mabos:Workflow rdfs:subClassOf [
    rdf:type owl:Restriction ;
    owl:onProperty mabos:hasTask ;
    owl:minCardinality "1"^^xsd:nonNegativeInteger
] .

# Confidence must be between 0 and 1
mabos:confidence rdfs:range [
    rdf:type rdfs:Datatype ;
    owl:onDatatype xsd:float ;
    owl:withRestrictions (
        [ xsd:minInclusive "0.0"^^xsd:float ]
        [ xsd:maxInclusive "1.0"^^xsd:float ]
    )
] .

# Priority must be between 1 and 10
mabos:priority rdfs:range [
    rdf:type rdfs:Datatype ;
    owl:onDatatype xsd:integer ;
    owl:withRestrictions (
        [ xsd:minInclusive "1"^^xsd:integer ]
        [ xsd:maxInclusive "10"^^xsd:integer ]
    )
] .

# Progress must be between 0 and 1
mabos:progress rdfs:range [
    rdf:type rdfs:Datatype ;
    owl:onDatatype xsd:float ;
    owl:withRestrictions (
        [ xsd:minInclusive "0.0"^^xsd:float ]
        [ xsd:maxInclusive "1.0"^^xsd:float ]
    )
] .
</code>

### 5.3 SPARQL Query Examples

**Query 1: Find all active agents with their beliefs**
```sparql
PREFIX mabos: <http://mabos.ai/ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?agent ?agentType ?belief ?predicate ?confidence
WHERE {
    ?agent rdf:type mabos:Agent ;
           mabos:agentStatus "active" ;
           mabos:agentType ?agentType ;
           mabos:hasBeliefs ?belief .
    ?belief mabos:predicate ?predicate ;
            mabos:confidence ?confidence .
    FILTER(?confidence > 0.7)
}
ORDER BY DESC(?confidence)
```

**Query 2: Find workflow dependencies**
```sparql
PREFIX mabos: <http://mabos.ai/ontology#>

SELECT ?workflow ?task1 ?task2
WHERE {
    ?workflow mabos:hasTask ?task1 ;
              mabos:hasTask ?task2 .
    ?task1 mabos:dependsOn ?task2 .
}
```

**Query 3: Agent performance analysis**
```sparql
PREFIX mabos: <http://mabos.ai/ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?agent (COUNT(?execution) AS ?executionCount) (AVG(?duration) AS ?avgDuration)
WHERE {
    ?agent mabos:participatesIn ?workflow .
    ?workflow mabos:hasExecution ?execution .
    ?execution mabos:executionStatus "completed" ;
               mabos:executionDuration ?duration .
    FILTER(?execution > "2024-01-01T00:00:00"^^xsd:dateTime)
}
GROUP BY ?agent
ORDER BY DESC(?executionCount)
```

### 5.4 Reasoning Rules

**SWRL Rules for Dynamic Knowledge Inference:**

```
// Rule 1: High confidence beliefs become knowledge
Belief(?b) ∧ confidence(?b, ?c) ∧ swrlb:greaterThan(?c, 0.9) → Knowledge(?b)

// Rule 2: Completed tasks update agent beliefs
TaskExecution(?te) ∧ executedBy(?te, ?agent) ∧ executionStatus(?te, "completed") ∧ 
hasResult(?te, ?result) → hasBeliefs(?agent, ?result)

// Rule 3: Failed executions trigger plan revision
Execution(?e) ∧ executionStatus(?e, "failed") ∧ instanceOf(?e, ?workflow) ∧ 
participatesIn(?agent, ?workflow) → requiresPlanRevision(?agent, ?workflow)

// Rule 4: High priority desires become intentions
Desire(?d) ∧ priority(?d, ?p) ∧ swrlb:greaterThan(?p, 8) ∧ desiredBy(?d, ?agent) → 
hasIntentions(?agent, ?d)
```

### 5.5 Implementation Details

**Python Implementation using Owlready2:**
```python
from owlready2 import *
import rdflib
from rdflib.plugins.sparql import prepareQuery

class MABOSOntology:
    """MABOS Ontology Manager"""
    
    def __init__(self, ontology_file: str):
        self.onto = get_ontology(ontology_file)
        self.onto.load()
        self.graph = default_world.as_rdflib_graph()
    
    def create_agent(self, agent_id: str, agent_type: str) -> Individual:
        """Create new BDI agent instance"""
        with self.onto:
            agent = self.onto.Agent(agent_id)
            agent.agentType = agent_type
            agent.agentStatus = "active"
            agent.lastActive = datetime.now()
            return agent
    
    def add_belief(self, agent: Individual, predicate: str, 
                  confidence: float, parameters: dict) -> Individual:
        """Add belief to agent's mental state"""
        with self.onto:
            belief = self.onto.Belief()
            belief.predicate = predicate
            belief.confidence = confidence
            agent.hasBeliefs.append(belief)
            return belief
    
    def query_sparql(self, query_string: str) -> list:
        """Execute SPARQL query against knowledge graph"""
        query = prepareQuery(query_string, 
                           initNs={"mabos": "http://mabos.ai/ontology#"})
        results = self.graph.query(query)
        return list(results)
    
    def infer_knowledge(self) -> None:
        """Run reasoner to infer new knowledge"""
        with self.onto:
            sync_reasoner(infer_property_values=True)
```

### 5.6 Knowledge Evolution and Versioning

**Versioning Strategy:**
- **Semantic Versioning:** Major.Minor.Patch for ontology evolution
- **Backward Compatibility:** Deprecation strategy for obsolete concepts
- **Migration Scripts:** Automated knowledge base updates
- **Change Tracking:** Audit trail for ontology modifications

**Evolution Patterns:**
- **Concept Addition:** New classes and properties added incrementally
- **Relationship Refinement:** Existing relationships made more specific
- **Domain Extension:** New domain-specific knowledge integration
- **Performance Optimization:** Query optimization through materialization