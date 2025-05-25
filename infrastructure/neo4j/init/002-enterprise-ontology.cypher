// MABOS Enterprise Systems Ontology
// This script sets up the knowledge graph for enterprise system integration

// ===== ENTERPRISE SYSTEMS =====

// SAP ERP System
CREATE (sap:System {
    id: 'system_sap_001',
    name: 'SAP',
    type: 'ERP',
    vendor: 'SAP SE',
    version: 'S/4HANA',
    status: 'configured',
    connection_type: 'RFC',
    base_url: 'https://sap.company.com',
    capabilities: ['financial_management', 'supply_chain', 'human_resources', 'procurement'],
    created_at: datetime(),
    description: 'Primary SAP ERP system for financial and operational data'
});

// Salesforce CRM System
CREATE (salesforce:System {
    id: 'system_salesforce_001',
    name: 'Salesforce',
    type: 'CRM',
    vendor: 'Salesforce',
    version: 'Enterprise',
    status: 'configured',
    connection_type: 'REST_API',
    base_url: 'https://company.salesforce.com',
    capabilities: ['customer_management', 'sales_automation', 'marketing_automation', 'analytics'],
    created_at: datetime(),
    description: 'Primary CRM system for customer relationship management'
});

// ServiceNow ITSM System
CREATE (servicenow:System {
    id: 'system_servicenow_001',
    name: 'ServiceNow',
    type: 'ITSM',
    vendor: 'ServiceNow',
    version: 'Tokyo',
    status: 'configured',
    connection_type: 'REST_API',
    base_url: 'https://company.service-now.com',
    capabilities: ['incident_management', 'change_management', 'asset_management', 'workflow_automation'],
    created_at: datetime(),
    description: 'IT Service Management platform for operational workflows'
});

// Microsoft 365 System
CREATE (microsoft365:System {
    id: 'system_m365_001',
    name: 'Microsoft 365',
    type: 'PRODUCTIVITY',
    vendor: 'Microsoft',
    version: 'Enterprise E5',
    status: 'configured',
    connection_type: 'GRAPH_API',
    base_url: 'https://graph.microsoft.com',
    capabilities: ['email', 'calendar', 'documents', 'teams', 'sharepoint'],
    created_at: datetime(),
    description: 'Microsoft 365 productivity and collaboration platform'
});

// Oracle Database System
CREATE (oracle:System {
    id: 'system_oracle_001',
    name: 'Oracle Database',
    type: 'DATABASE',
    vendor: 'Oracle',
    version: '19c',
    status: 'configured',
    connection_type: 'JDBC',
    base_url: 'oracle.company.com:1521',
    capabilities: ['data_storage', 'analytics', 'reporting', 'data_warehouse'],
    created_at: datetime(),
    description: 'Oracle database system for enterprise data storage'
});

// ===== CORE BUSINESS ENTITIES =====

// Customer Entity
CREATE (customer:Entity {
    id: 'entity_customer_001',
    type: 'Customer',
    category: 'business_object',
    description: 'Customer business entity across enterprise systems',
    attributes: ['customer_id', 'name', 'email', 'phone', 'address', 'status'],
    created_at: datetime()
});

// Employee Entity
CREATE (employee:Entity {
    id: 'entity_employee_001',
    type: 'Employee',
    category: 'business_object',
    description: 'Employee business entity across enterprise systems',
    attributes: ['employee_id', 'name', 'email', 'department', 'role', 'manager'],
    created_at: datetime()
});

// Product Entity
CREATE (product:Entity {
    id: 'entity_product_001',
    type: 'Product',
    category: 'business_object',
    description: 'Product business entity across enterprise systems',
    attributes: ['product_id', 'name', 'description', 'price', 'category', 'status'],
    created_at: datetime()
});

// Order Entity
CREATE (order:Entity {
    id: 'entity_order_001',
    type: 'Order',
    category: 'business_object',
    description: 'Order business entity across enterprise systems',
    attributes: ['order_id', 'customer_id', 'product_id', 'quantity', 'amount', 'status'],
    created_at: datetime()
});

// Incident Entity
CREATE (incident:Entity {
    id: 'entity_incident_001',
    type: 'Incident',
    category: 'business_object',
    description: 'IT incident business entity for service management',
    attributes: ['incident_id', 'title', 'description', 'priority', 'status', 'assignee'],
    created_at: datetime()
});

// ===== SYSTEM-ENTITY RELATIONSHIPS =====

// SAP System Entities
CREATE (sap)-[:CONTAINS]->(customer);
CREATE (sap)-[:CONTAINS]->(employee);
CREATE (sap)-[:CONTAINS]->(product);
CREATE (sap)-[:CONTAINS]->(order);

// Salesforce System Entities
CREATE (salesforce)-[:CONTAINS]->(customer);
CREATE (salesforce)-[:CONTAINS]->(product);
CREATE (salesforce)-[:CONTAINS]->(order);

// ServiceNow System Entities
CREATE (servicenow)-[:CONTAINS]->(employee);
CREATE (servicenow)-[:CONTAINS]->(incident);

// Microsoft 365 System Entities
CREATE (microsoft365)-[:CONTAINS]->(employee);

// Oracle System Entities
CREATE (oracle)-[:CONTAINS]->(customer);
CREATE (oracle)-[:CONTAINS]->(employee);
CREATE (oracle)-[:CONTAINS]->(product);
CREATE (oracle)-[:CONTAINS]->(order);

// ===== DATA MAPPING DEFINITIONS =====

// Customer Data Mappings
CREATE (customer_sap_mapping:DataMapping {
    id: 'mapping_customer_sap_001',
    source_system: 'SAP',
    target_system: 'Salesforce',
    entity_type: 'Customer',
    source_fields: ['KUNNR', 'NAME1', 'SMTP_ADDR', 'TELF1', 'STRAS'],
    target_fields: ['Id', 'Name', 'Email', 'Phone', 'BillingStreet'],
    transformation_rules: 'KUNNR->External_Id__c,NAME1->Name,SMTP_ADDR->Email,TELF1->Phone,STRAS->BillingStreet',
    created_at: datetime(),
    description: 'Customer data mapping between SAP and Salesforce'
});

// Employee Data Mappings
CREATE (employee_mapping:DataMapping {
    id: 'mapping_employee_001',
    source_system: 'SAP',
    target_system: 'Microsoft 365',
    entity_type: 'Employee',
    source_fields: ['PERNR', 'VORNA', 'NACHN', 'USRID_LONG', 'ORGEH'],
    target_fields: ['id', 'givenName', 'surname', 'userPrincipalName', 'department'],
    transformation_rules: 'PERNR->employeeId,VORNA->givenName,NACHN->surname,USRID_LONG->userPrincipalName,ORGEH->department',
    created_at: datetime(),
    description: 'Employee data mapping between SAP and Microsoft 365'
});

// ===== WORKFLOW PROCESS DEFINITIONS =====

// Customer Onboarding Process
CREATE (customer_onboarding:WorkflowProcess {
    id: 'process_customer_onboarding_001',
    name: 'Customer Onboarding',
    category: 'customer_management',
    systems_involved: ['Salesforce', 'SAP', 'Microsoft 365'],
    estimated_duration: duration('P3D'),
    complexity: 'medium',
    created_at: datetime(),
    description: 'End-to-end customer onboarding process across enterprise systems'
});

// Employee Provisioning Process
CREATE (employee_provisioning:WorkflowProcess {
    id: 'process_employee_provisioning_001',
    name: 'Employee Provisioning',
    category: 'human_resources',
    systems_involved: ['SAP', 'Microsoft 365', 'ServiceNow'],
    estimated_duration: duration('P1D'),
    complexity: 'high',
    created_at: datetime(),
    description: 'New employee provisioning across all enterprise systems'
});

// Incident Resolution Process
CREATE (incident_resolution:WorkflowProcess {
    id: 'process_incident_resolution_001',
    name: 'Incident Resolution',
    category: 'it_service_management',
    systems_involved: ['ServiceNow', 'Microsoft 365'],
    estimated_duration: duration('PT4H'),
    complexity: 'low',
    created_at: datetime(),
    description: 'IT incident resolution workflow'
});

// ===== PROCESS TASK DEFINITIONS =====

// Customer Onboarding Tasks
CREATE (validate_customer:WorkflowTask {
    id: 'task_validate_customer_001',
    name: 'Validate Customer Information',
    process_id: 'process_customer_onboarding_001',
    system: 'Salesforce',
    task_type: 'validation',
    estimated_duration: duration('PT30M'),
    dependencies: [],
    created_at: datetime(),
    description: 'Validate customer information in Salesforce'
});

CREATE (create_sap_customer:WorkflowTask {
    id: 'task_create_sap_customer_001',
    name: 'Create Customer in SAP',
    process_id: 'process_customer_onboarding_001',
    system: 'SAP',
    task_type: 'creation',
    estimated_duration: duration('PT15M'),
    dependencies: ['task_validate_customer_001'],
    created_at: datetime(),
    description: 'Create customer master data in SAP'
});

CREATE (setup_customer_portal:WorkflowTask {
    id: 'task_setup_portal_001',
    name: 'Setup Customer Portal Access',
    process_id: 'process_customer_onboarding_001',
    system: 'Microsoft 365',
    task_type: 'configuration',
    estimated_duration: duration('PT20M'),
    dependencies: ['task_create_sap_customer_001'],
    created_at: datetime(),
    description: 'Configure customer portal access in Microsoft 365'
});

// ===== PROCESS RELATIONSHIPS =====

// Process-Task Relationships
CREATE (customer_onboarding)-[:CONTAINS]->(validate_customer);
CREATE (customer_onboarding)-[:CONTAINS]->(create_sap_customer);
CREATE (customer_onboarding)-[:CONTAINS]->(setup_customer_portal);

// Task Dependencies
CREATE (validate_customer)-[:PRECEDES]->(create_sap_customer);
CREATE (create_sap_customer)-[:PRECEDES]->(setup_customer_portal);

// System-Process Relationships
CREATE (salesforce)-[:SUPPORTS]->(customer_onboarding);
CREATE (sap)-[:SUPPORTS]->(customer_onboarding);
CREATE (microsoft365)-[:SUPPORTS]->(customer_onboarding);

// ===== INTEGRATION PATTERNS =====

// Real-time Synchronization Pattern
CREATE (realtime_sync:IntegrationPattern {
    id: 'pattern_realtime_sync_001',
    name: 'Real-time Data Synchronization',
    type: 'synchronous',
    systems: ['SAP', 'Salesforce'],
    trigger: 'data_change',
    frequency: 'immediate',
    reliability: 'high',
    created_at: datetime(),
    description: 'Real-time synchronization pattern for critical data'
});

// Batch Processing Pattern
CREATE (batch_sync:IntegrationPattern {
    id: 'pattern_batch_sync_001',
    name: 'Batch Data Processing',
    type: 'asynchronous',
    systems: ['Oracle', 'SAP'],
    trigger: 'scheduled',
    frequency: 'daily',
    reliability: 'medium',
    created_at: datetime(),
    description: 'Batch processing pattern for large data volumes'
});

// Event-driven Pattern
CREATE (event_driven:IntegrationPattern {
    id: 'pattern_event_driven_001',
    name: 'Event-driven Integration',
    type: 'asynchronous',
    systems: ['ServiceNow', 'Microsoft 365'],
    trigger: 'business_event',
    frequency: 'on_demand',
    reliability: 'high',
    created_at: datetime(),
    description: 'Event-driven integration for workflow automation'
});

// ===== SYSTEM DEPENDENCIES =====

// System Integration Dependencies
CREATE (sap)-[:INTEGRATES_WITH]->(salesforce);
CREATE (sap)-[:INTEGRATES_WITH]->(oracle);
CREATE (salesforce)-[:INTEGRATES_WITH]->(microsoft365);
CREATE (servicenow)-[:INTEGRATES_WITH]->(microsoft365);
CREATE (servicenow)-[:INTEGRATES_WITH]->(sap);

// Data Flow Dependencies
CREATE (sap)-[:PROVIDES_DATA_TO]->(salesforce);
CREATE (salesforce)-[:PROVIDES_DATA_TO]->(microsoft365);
CREATE (oracle)-[:PROVIDES_DATA_TO]->(sap);

// ===== ENTERPRISE ONTOLOGY SUCCESS MESSAGE =====
CREATE (enterprise_init_success:Event {
    id: 'event_enterprise_init_001',
    type: 'enterprise_ontology_initialization',
    message: 'MABOS enterprise systems ontology successfully initialized',
    timestamp: datetime(),
    details: 'Enterprise systems, entities, mappings, and integration patterns established'
});

// Link to integration agent
MATCH (integration_agent:Agent {id: 'agent_integration_001'})
CREATE (integration_agent)-[:LOGGED]->(enterprise_init_success); 