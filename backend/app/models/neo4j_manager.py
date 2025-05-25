"""
MABOS Neo4j Knowledge Graph Manager

Comprehensive knowledge graph management with SBVR ontology integration
for business rule validation, proof tables, and reasoning engines.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import json
import uuid
from pathlib import Path

from neo4j import AsyncGraphDatabase, AsyncDriver, AsyncSession
from neo4j.exceptions import ServiceUnavailable, AuthError

from app.core.database import DatabaseConfig

# Configure logging
logger = logging.getLogger(__name__)

class SBVROntologyManager:
    """SBVR (Semantics of Business Vocabulary and Business Rules) ontology manager"""
    
    def __init__(self, session: AsyncSession):
        """Initialize SBVR ontology manager with Neo4j session"""
        self.session = session
    
    async def initialize_sbvr_schema(self) -> None:
        """Initialize SBVR ontology schema in Neo4j"""
        
        # Create SBVR node types and constraints
        sbvr_schema_queries = [
            # Core SBVR Classes
            """
            CREATE CONSTRAINT sbvr_vocabulary_element_id IF NOT EXISTS
            FOR (v:VocabularyElement) REQUIRE v.id IS UNIQUE
            """,
            
            """
            CREATE CONSTRAINT sbvr_concept_type_id IF NOT EXISTS
            FOR (c:ConceptType) REQUIRE c.id IS UNIQUE
            """,
            
            """
            CREATE CONSTRAINT sbvr_fact_type_id IF NOT EXISTS
            FOR (f:FactType) REQUIRE f.id IS UNIQUE
            """,
            
            """
            CREATE CONSTRAINT sbvr_rule_id IF NOT EXISTS
            FOR (r:Rule) REQUIRE r.id IS UNIQUE
            """,
            
            # Business Process Extensions
            """
            CREATE CONSTRAINT business_process_id IF NOT EXISTS
            FOR (bp:BusinessProcess) REQUIRE bp.id IS UNIQUE
            """,
            
            """
            CREATE CONSTRAINT workflow_rule_id IF NOT EXISTS
            FOR (wr:WorkflowRule) REQUIRE wr.id IS UNIQUE
            """,
            
            # Proof Table Structures
            """
            CREATE CONSTRAINT proof_table_id IF NOT EXISTS
            FOR (pt:ProofTable) REQUIRE pt.id IS UNIQUE
            """,
            
            """
            CREATE CONSTRAINT proof_entry_id IF NOT EXISTS
            FOR (pe:ProofEntry) REQUIRE pe.id IS UNIQUE
            """,
            
            # Reasoning Engine Components
            """
            CREATE CONSTRAINT reasoning_engine_id IF NOT EXISTS
            FOR (re:ReasoningEngine) REQUIRE re.id IS UNIQUE
            """,
            
            """
            CREATE CONSTRAINT inference_rule_id IF NOT EXISTS
            FOR (ir:InferenceRule) REQUIRE ir.id IS UNIQUE
            """
        ]
        
        for query in sbvr_schema_queries:
            await self.session.run(query)
        
        logger.info("SBVR ontology schema initialized successfully")
    
    async def create_vocabulary_element(self, element_data: Dict[str, Any]) -> str:
        """Create a vocabulary element in the knowledge graph"""
        element_id = element_data.get('id', str(uuid.uuid4()))
        
        query = """
        CREATE (v:VocabularyElement {
            id: $id,
            name: $name,
            definition: $definition,
            type: $type,
            domain: $domain,
            created_at: datetime(),
            updated_at: datetime()
        })
        RETURN v.id as id
        """
        
        result = await self.session.run(query, {
            'id': element_id,
            'name': element_data.get('name', ''),
            'definition': element_data.get('definition', ''),
            'type': element_data.get('type', 'general'),
            'domain': element_data.get('domain', 'business')
        })
        
        record = await result.single()
        return record['id']
    
    async def create_concept_type(self, concept_data: Dict[str, Any]) -> str:
        """Create a concept type with SBVR semantics"""
        concept_id = concept_data.get('id', str(uuid.uuid4()))
        
        query = """
        CREATE (c:ConceptType:VocabularyElement {
            id: $id,
            name: $name,
            definition: $definition,
            properties: $properties,
            constraints: $constraints,
            business_context: $business_context,
            created_at: datetime(),
            updated_at: datetime()
        })
        RETURN c.id as id
        """
        
        result = await self.session.run(query, {
            'id': concept_id,
            'name': concept_data.get('name', ''),
            'definition': concept_data.get('definition', ''),
            'properties': json.dumps(concept_data.get('properties', {})),
            'constraints': json.dumps(concept_data.get('constraints', [])),
            'business_context': concept_data.get('business_context', '')
        })
        
        record = await result.single()
        return record['id']
    
    async def create_fact_type(self, fact_data: Dict[str, Any]) -> str:
        """Create a fact type representing relationships between concepts"""
        fact_id = fact_data.get('id', str(uuid.uuid4()))
        
        query = """
        CREATE (f:FactType:VocabularyElement {
            id: $id,
            name: $name,
            definition: $definition,
            arity: $arity,
            roles: $roles,
            constraints: $constraints,
            business_significance: $business_significance,
            created_at: datetime(),
            updated_at: datetime()
        })
        RETURN f.id as id
        """
        
        result = await self.session.run(query, {
            'id': fact_id,
            'name': fact_data.get('name', ''),
            'definition': fact_data.get('definition', ''),
            'arity': fact_data.get('arity', 2),
            'roles': json.dumps(fact_data.get('roles', [])),
            'constraints': json.dumps(fact_data.get('constraints', [])),
            'business_significance': fact_data.get('business_significance', '')
        })
        
        record = await result.single()
        return record['id']
    
    async def create_business_rule(self, rule_data: Dict[str, Any]) -> str:
        """Create a business rule with SBVR semantics and validation logic"""
        rule_id = rule_data.get('id', str(uuid.uuid4()))
        
        query = """
        CREATE (r:Rule:VocabularyElement {
            id: $id,
            name: $name,
            definition: $definition,
            rule_type: $rule_type,
            condition: $condition,
            action: $action,
            priority: $priority,
            validation_logic: $validation_logic,
            proof_requirements: $proof_requirements,
            business_impact: $business_impact,
            is_active: $is_active,
            created_at: datetime(),
            updated_at: datetime()
        })
        RETURN r.id as id
        """
        
        result = await self.session.run(query, {
            'id': rule_id,
            'name': rule_data.get('name', ''),
            'definition': rule_data.get('definition', ''),
            'rule_type': rule_data.get('rule_type', 'constraint'),
            'condition': rule_data.get('condition', ''),
            'action': rule_data.get('action', ''),
            'priority': rule_data.get('priority', 5),
            'validation_logic': json.dumps(rule_data.get('validation_logic', {})),
            'proof_requirements': json.dumps(rule_data.get('proof_requirements', [])),
            'business_impact': rule_data.get('business_impact', 'medium'),
            'is_active': rule_data.get('is_active', True)
        })
        
        record = await result.single()
        return record['id']
    
    async def create_proof_table(self, proof_data: Dict[str, Any]) -> str:
        """Create a proof table for rule validation and optimization"""
        proof_id = proof_data.get('id', str(uuid.uuid4()))
        
        query = """
        CREATE (pt:ProofTable {
            id: $id,
            name: $name,
            description: $description,
            rule_id: $rule_id,
            input_variables: $input_variables,
            output_variables: $output_variables,
            truth_conditions: $truth_conditions,
            optimization_hints: $optimization_hints,
            performance_metrics: $performance_metrics,
            created_at: datetime(),
            updated_at: datetime()
        })
        RETURN pt.id as id
        """
        
        result = await self.session.run(query, {
            'id': proof_id,
            'name': proof_data.get('name', ''),
            'description': proof_data.get('description', ''),
            'rule_id': proof_data.get('rule_id', ''),
            'input_variables': json.dumps(proof_data.get('input_variables', [])),
            'output_variables': json.dumps(proof_data.get('output_variables', [])),
            'truth_conditions': json.dumps(proof_data.get('truth_conditions', [])),
            'optimization_hints': json.dumps(proof_data.get('optimization_hints', {})),
            'performance_metrics': json.dumps(proof_data.get('performance_metrics', {}))
        })
        
        record = await result.single()
        return record['id']
    
    async def create_proof_entry(self, entry_data: Dict[str, Any]) -> str:
        """Create a proof table entry with specific input/output combinations"""
        entry_id = entry_data.get('id', str(uuid.uuid4()))
        
        query = """
        CREATE (pe:ProofEntry {
            id: $id,
            proof_table_id: $proof_table_id,
            input_values: $input_values,
            output_values: $output_values,
            truth_value: $truth_value,
            confidence: $confidence,
            evidence: $evidence,
            validation_status: $validation_status,
            created_at: datetime(),
            updated_at: datetime()
        })
        RETURN pe.id as id
        """
        
        result = await self.session.run(query, {
            'id': entry_id,
            'proof_table_id': entry_data.get('proof_table_id', ''),
            'input_values': json.dumps(entry_data.get('input_values', {})),
            'output_values': json.dumps(entry_data.get('output_values', {})),
            'truth_value': entry_data.get('truth_value', True),
            'confidence': entry_data.get('confidence', 1.0),
            'evidence': json.dumps(entry_data.get('evidence', [])),
            'validation_status': entry_data.get('validation_status', 'validated')
        })
        
        record = await result.single()
        return record['id']
    
    async def create_reasoning_engine(self, engine_data: Dict[str, Any]) -> str:
        """Create a reasoning engine for automated rule processing"""
        engine_id = engine_data.get('id', str(uuid.uuid4()))
        
        query = """
        CREATE (re:ReasoningEngine {
            id: $id,
            name: $name,
            description: $description,
            engine_type: $engine_type,
            algorithms: $algorithms,
            optimization_strategies: $optimization_strategies,
            performance_config: $performance_config,
            is_active: $is_active,
            created_at: datetime(),
            updated_at: datetime()
        })
        RETURN re.id as id
        """
        
        result = await self.session.run(query, {
            'id': engine_id,
            'name': engine_data.get('name', ''),
            'description': engine_data.get('description', ''),
            'engine_type': engine_data.get('engine_type', 'forward_chaining'),
            'algorithms': json.dumps(engine_data.get('algorithms', [])),
            'optimization_strategies': json.dumps(engine_data.get('optimization_strategies', [])),
            'performance_config': json.dumps(engine_data.get('performance_config', {})),
            'is_active': engine_data.get('is_active', True)
        })
        
        record = await result.single()
        return record['id']
    
    async def establish_sbvr_relationships(self) -> None:
        """Establish SBVR semantic relationships between entities"""
        
        relationship_queries = [
            # ConceptType defines relationships
            """
            MATCH (c:ConceptType), (v:VocabularyElement)
            WHERE c.id <> v.id AND v.business_context CONTAINS c.name
            MERGE (c)-[:DEFINES]->(v)
            """,
            
            # FactType relates to ConceptTypes - using string contains for JSON parsing
            """
            MATCH (f:FactType), (c:ConceptType)
            WHERE f.roles CONTAINS c.name
            MERGE (f)-[:RELATES_TO]->(c)
            """,
            
            # Rules constrain FactTypes
            """
            MATCH (r:Rule), (f:FactType)
            WHERE r.condition CONTAINS f.name OR r.action CONTAINS f.name
            MERGE (r)-[:CONSTRAINS]->(f)
            """,
            
            # ProofTable validates Rules
            """
            MATCH (pt:ProofTable), (r:Rule)
            WHERE pt.rule_id = r.id
            MERGE (pt)-[:VALIDATES]->(r)
            """,
            
            # ProofEntry belongs to ProofTable
            """
            MATCH (pe:ProofEntry), (pt:ProofTable)
            WHERE pe.proof_table_id = pt.id
            MERGE (pe)-[:BELONGS_TO]->(pt)
            """,
            
            # ReasoningEngine processes Rules
            """
            MATCH (re:ReasoningEngine), (r:Rule)
            WHERE r.is_active = true
            MERGE (re)-[:PROCESSES]->(r)
            """
        ]
        
        for query in relationship_queries:
            await self.session.run(query)
        
        logger.info("SBVR semantic relationships established")

class Neo4jKnowledgeGraphManager:
    """Comprehensive Neo4j knowledge graph manager for MABOS"""
    
    def __init__(self, config: DatabaseConfig):
        """Initialize Neo4j knowledge graph manager"""
        self.config = config
        self.driver: Optional[AsyncDriver] = None
        self.sbvr_manager: Optional[SBVROntologyManager] = None
    
    async def initialize(self) -> None:
        """Initialize Neo4j connection and knowledge graph schema"""
        try:
            # Create Neo4j driver
            self.driver = AsyncGraphDatabase.driver(
                self.config.neo4j_uri,
                auth=(self.config.neo4j_user, self.config.neo4j_password),
                database=self.config.neo4j_database
            )
            
            # Verify connection
            await self.driver.verify_connectivity()
            
            # Initialize knowledge graph schema
            async with self.driver.session() as session:
                self.sbvr_manager = SBVROntologyManager(session)
                await self.initialize_knowledge_graph_schema(session)
                await self.sbvr_manager.initialize_sbvr_schema()
                await self.load_initial_sbvr_data(session)
            
            logger.info("Neo4j knowledge graph manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Neo4j knowledge graph: {e}")
            raise
    
    async def initialize_knowledge_graph_schema(self, session: AsyncSession) -> None:
        """Initialize comprehensive knowledge graph schema"""
        
        schema_queries = [
            # Core BDI Agent Schema
            """
            CREATE CONSTRAINT agent_node_id IF NOT EXISTS
            FOR (a:Agent) REQUIRE a.id IS UNIQUE
            """,
            
            """
            CREATE CONSTRAINT belief_node_id IF NOT EXISTS
            FOR (b:Belief) REQUIRE b.id IS UNIQUE
            """,
            
            """
            CREATE CONSTRAINT desire_node_id IF NOT EXISTS
            FOR (d:Desire) REQUIRE d.id IS UNIQUE
            """,
            
            """
            CREATE CONSTRAINT intention_node_id IF NOT EXISTS
            FOR (i:Intention) REQUIRE i.id IS UNIQUE
            """,
            
            # Workflow and Process Schema
            """
            CREATE CONSTRAINT workflow_node_id IF NOT EXISTS
            FOR (w:Workflow) REQUIRE w.id IS UNIQUE
            """,
            
            """
            CREATE CONSTRAINT task_node_id IF NOT EXISTS
            FOR (t:Task) REQUIRE t.id IS UNIQUE
            """,
            
            """
            CREATE CONSTRAINT process_node_id IF NOT EXISTS
            FOR (p:Process) REQUIRE p.id IS UNIQUE
            """,
            
            # Enterprise System Schema
            """
            CREATE CONSTRAINT system_node_id IF NOT EXISTS
            FOR (s:System) REQUIRE s.id IS UNIQUE
            """,
            
            """
            CREATE CONSTRAINT integration_node_id IF NOT EXISTS
            FOR (i:Integration) REQUIRE i.id IS UNIQUE
            """,
            
            # Knowledge and Ontology Schema
            """
            CREATE CONSTRAINT concept_node_id IF NOT EXISTS
            FOR (c:Concept) REQUIRE c.id IS UNIQUE
            """,
            
            """
            CREATE CONSTRAINT relationship_node_id IF NOT EXISTS
            FOR (r:Relationship) REQUIRE r.id IS UNIQUE
            """,
            
            # Performance indexes
            """
            CREATE INDEX agent_type_index IF NOT EXISTS
            FOR (a:Agent) ON (a.type)
            """,
            
            """
            CREATE INDEX workflow_status_index IF NOT EXISTS
            FOR (w:Workflow) ON (w.status)
            """,
            
            """
            CREATE INDEX concept_domain_index IF NOT EXISTS
            FOR (c:Concept) ON (c.domain)
            """,
            
            """
            CREATE INDEX rule_priority_index IF NOT EXISTS
            FOR (r:Rule) ON (r.priority)
            """
        ]
        
        for query in schema_queries:
            await session.run(query)
        
        logger.info("Knowledge graph schema initialized")
    
    async def load_initial_sbvr_data(self, session: AsyncSession) -> None:
        """Load initial SBVR ontology data based on the provided XML"""
        
        # Create core SBVR concepts from the XML
        core_concepts = [
            {
                'name': 'Customer',
                'definition': 'A person or organization that purchases goods or services',
                'properties': {
                    'identifier_attributes': ['customer_id', 'email', 'name'],
                    'behavioral_attributes': ['purchase_history', 'preferences', 'loyalty_status']
                },
                'business_context': 'sales_and_marketing'
            },
            {
                'name': 'Product',
                'definition': 'A good or service offered for sale',
                'properties': {
                    'identifier_attributes': ['product_id', 'sku', 'name'],
                    'descriptive_attributes': ['category', 'price', 'availability']
                },
                'business_context': 'product_management'
            },
            {
                'name': 'Purchase',
                'definition': 'A transaction where a customer buys a product',
                'properties': {
                    'transaction_attributes': ['purchase_id', 'amount', 'date', 'payment_method'],
                    'relationship_attributes': ['customer_id', 'product_ids']
                },
                'business_context': 'transaction_processing'
            },
            {
                'name': 'WorkflowExecution',
                'definition': 'An instance of a workflow being executed in the system',
                'properties': {
                    'execution_attributes': ['execution_id', 'workflow_id', 'status', 'start_time'],
                    'performance_attributes': ['duration', 'success_rate', 'resource_usage']
                },
                'business_context': 'workflow_management'
            }
        ]
        
        # Create concept types
        for concept in core_concepts:
            await self.sbvr_manager.create_concept_type(concept)
        
        # Create fact types
        fact_types = [
            {
                'name': 'CustomerPurchasesProduct',
                'definition': 'Relationship between customer and product through purchase',
                'arity': 3,
                'roles': [
                    {'name': 'customer', 'concept': 'Customer', 'cardinality': '1'},
                    {'name': 'product', 'concept': 'Product', 'cardinality': '1..*'},
                    {'name': 'purchase', 'concept': 'Purchase', 'cardinality': '1'}
                ],
                'business_significance': 'Core business transaction relationship'
            },
            {
                'name': 'WorkflowExecutesTask',
                'definition': 'Relationship between workflow execution and individual tasks',
                'arity': 2,
                'roles': [
                    {'name': 'workflow', 'concept': 'WorkflowExecution', 'cardinality': '1'},
                    {'name': 'task', 'concept': 'Task', 'cardinality': '1..*'}
                ],
                'business_significance': 'Workflow composition and execution tracking'
            }
        ]
        
        for fact_type in fact_types:
            await self.sbvr_manager.create_fact_type(fact_type)
        
        # Create business rules
        business_rules = [
            {
                'name': 'PurchaseValidationRule',
                'definition': 'A purchase can only occur if the customer is verified and the product is available',
                'rule_type': 'constraint',
                'condition': 'Customer.is_verified = true AND Product.availability > 0',
                'action': 'Allow purchase transaction',
                'priority': 9,
                'validation_logic': {
                    'preconditions': ['customer_verification', 'product_availability'],
                    'postconditions': ['transaction_recorded', 'inventory_updated']
                },
                'proof_requirements': ['customer_identity_proof', 'product_stock_proof'],
                'business_impact': 'high'
            },
            {
                'name': 'WorkflowExecutionRule',
                'definition': 'A workflow execution must complete all mandatory tasks before marking as successful',
                'rule_type': 'constraint',
                'condition': 'ALL mandatory_tasks.status = "completed"',
                'action': 'Mark workflow execution as successful',
                'priority': 8,
                'validation_logic': {
                    'preconditions': ['all_mandatory_tasks_identified'],
                    'postconditions': ['workflow_status_updated', 'completion_metrics_recorded']
                },
                'proof_requirements': ['task_completion_proof', 'execution_trace'],
                'business_impact': 'high'
            }
        ]
        
        for rule in business_rules:
            rule_id = await self.sbvr_manager.create_business_rule(rule)
            
            # Create corresponding proof table
            proof_table = {
                'name': f"{rule['name']}_ProofTable",
                'description': f"Proof table for validating {rule['name']}",
                'rule_id': rule_id,
                'input_variables': rule['validation_logic']['preconditions'],
                'output_variables': rule['validation_logic']['postconditions'],
                'truth_conditions': [
                    {'condition': rule['condition'], 'expected_result': True}
                ],
                'optimization_hints': {
                    'indexing_strategy': 'btree_on_conditions',
                    'caching_policy': 'cache_frequent_validations'
                }
            }
            
            proof_table_id = await self.sbvr_manager.create_proof_table(proof_table)
            
            # Create sample proof entries
            sample_entries = [
                {
                    'proof_table_id': proof_table_id,
                    'input_values': {condition: True for condition in rule['validation_logic']['preconditions']},
                    'output_values': {condition: True for condition in rule['validation_logic']['postconditions']},
                    'truth_value': True,
                    'confidence': 0.95,
                    'evidence': ['system_validation', 'business_logic_check'],
                    'validation_status': 'validated'
                }
            ]
            
            for entry in sample_entries:
                await self.sbvr_manager.create_proof_entry(entry)
        
        # Create reasoning engines
        reasoning_engines = [
            {
                'name': 'ForwardChainingEngine',
                'description': 'Forward chaining reasoning engine for rule-based inference',
                'engine_type': 'forward_chaining',
                'algorithms': ['rete_algorithm', 'conflict_resolution'],
                'optimization_strategies': ['rule_ordering', 'fact_indexing', 'partial_matching'],
                'performance_config': {
                    'max_iterations': 1000,
                    'timeout_seconds': 30,
                    'memory_limit_mb': 512
                }
            },
            {
                'name': 'BackwardChainingEngine',
                'description': 'Backward chaining reasoning engine for goal-driven inference',
                'engine_type': 'backward_chaining',
                'algorithms': ['sld_resolution', 'goal_stack_management'],
                'optimization_strategies': ['goal_ordering', 'memoization', 'cut_optimization'],
                'performance_config': {
                    'max_depth': 100,
                    'timeout_seconds': 60,
                    'memory_limit_mb': 256
                }
            }
        ]
        
        for engine in reasoning_engines:
            await self.sbvr_manager.create_reasoning_engine(engine)
        
        # Establish SBVR relationships
        await self.sbvr_manager.establish_sbvr_relationships()
        
        logger.info("Initial SBVR ontology data loaded successfully")
    
    async def execute_cypher_query(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Execute a Cypher query and return results"""
        if not self.driver:
            raise RuntimeError("Neo4j driver not initialized")
        
        async with self.driver.session() as session:
            result = await session.run(query, parameters or {})
            records = await result.data()
            return [self._serialize_neo4j_types(record) for record in records]
    
    def _serialize_neo4j_types(self, obj):
        """Convert Neo4j types to JSON-serializable types"""
        if hasattr(obj, 'isoformat'):  # DateTime objects
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {k: self._serialize_neo4j_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._serialize_neo4j_types(item) for item in obj]
        else:
            return obj
    
    async def validate_business_rule(self, rule_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate business rule using SBVR proof tables"""
        query = """
        MATCH (r:Rule {id: $rule_id})
        MATCH (pt:ProofTable)-[:VALIDATES]->(r)
        MATCH (pe:ProofEntry)-[:BELONGS_TO]->(pt)
        WHERE pe.validation_status = 'validated'
        RETURN r, pt, collect(pe) as proof_entries
        """
        
        result = await self.execute_cypher_query(query, {'rule_id': rule_id})
        
        if not result:
            return {'valid': False, 'reason': 'Rule not found or no proof table available'}
        
        rule_data = result[0]
        proof_entries = rule_data['proof_entries']
        
        # Perform validation logic based on proof table entries
        validation_result = {
            'valid': False,
            'confidence': 0.0,
            'evidence': [],
            'proof_table_matches': []
        }
        
        for entry in proof_entries:
            entry_input = json.loads(entry['input_values'])
            entry_output = json.loads(entry['output_values'])
            
            # Check if input data matches proof entry conditions
            if self._matches_proof_conditions(input_data, entry_input):
                validation_result['valid'] = entry['truth_value']
                validation_result['confidence'] = max(validation_result['confidence'], entry['confidence'])
                validation_result['evidence'].extend(json.loads(entry['evidence']))
                validation_result['proof_table_matches'].append({
                    'entry_id': entry['id'],
                    'expected_output': entry_output,
                    'confidence': entry['confidence']
                })
        
        return validation_result
    
    def _matches_proof_conditions(self, input_data: Dict[str, Any], proof_conditions: Dict[str, Any]) -> bool:
        """Check if input data matches proof table conditions"""
        for key, expected_value in proof_conditions.items():
            if key not in input_data or input_data[key] != expected_value:
                return False
        return True
    
    async def get_agent_knowledge_context(self, agent_id: str) -> Dict[str, Any]:
        """Get comprehensive knowledge context for a BDI agent"""
        query = """
        MATCH (a:Agent {id: $agent_id})
        OPTIONAL MATCH (a)-[:HAS_BELIEF]->(b:Belief)
        OPTIONAL MATCH (a)-[:HAS_DESIRE]->(d:Desire)
        OPTIONAL MATCH (a)-[:HAS_INTENTION]->(i:Intention)
        OPTIONAL MATCH (a)-[:KNOWS_CONCEPT]->(c:ConceptType)
        OPTIONAL MATCH (a)-[:APPLIES_RULE]->(r:Rule)
        RETURN a,
               collect(DISTINCT b) as beliefs,
               collect(DISTINCT d) as desires,
               collect(DISTINCT i) as intentions,
               collect(DISTINCT c) as known_concepts,
               collect(DISTINCT r) as applicable_rules
        """
        
        result = await self.execute_cypher_query(query, {'agent_id': agent_id})
        
        if not result:
            return {'agent_id': agent_id, 'context': 'not_found'}
        
        return result[0]
    
    async def optimize_reasoning_performance(self) -> Dict[str, Any]:
        """Optimize reasoning engine performance using graph analytics"""
        optimization_queries = [
            # Analyze rule complexity and usage patterns
            """
            MATCH (r:Rule)
            OPTIONAL MATCH (pt:ProofTable)-[:VALIDATES]->(r)
            OPTIONAL MATCH (pe:ProofEntry)-[:BELONGS_TO]->(pt)
            RETURN r.id, r.priority, count(pe) as proof_entries_count,
                   avg(pe.confidence) as avg_confidence
            ORDER BY r.priority DESC, proof_entries_count DESC
            """,
            
            # Identify frequently used concept types
            """
            MATCH (c:ConceptType)
            OPTIONAL MATCH (f:FactType)-[:RELATES_TO]->(c)
            OPTIONAL MATCH (c)-[:DEFINES]->(v:VocabularyElement)
            RETURN c.name, count(f) as fact_relationships, count(v) as vocabulary_definitions
            ORDER BY fact_relationships DESC, vocabulary_definitions DESC
            """,
            
            # Analyze reasoning engine performance
            """
            MATCH (re:ReasoningEngine)
            OPTIONAL MATCH (re)-[:PROCESSES]->(r:Rule)
            RETURN re.name, re.engine_type, count(r) as rules_processed,
                   re.performance_config as config
            """
        ]
        
        optimization_results = {}
        
        for i, query in enumerate(optimization_queries):
            result = await self.execute_cypher_query(query)
            optimization_results[f'analysis_{i+1}'] = result
        
        # Generate optimization recommendations
        recommendations = {
            'rule_optimization': 'Prioritize high-confidence rules with many proof entries',
            'concept_indexing': 'Create indexes for frequently referenced concept types',
            'engine_tuning': 'Adjust reasoning engine parameters based on rule complexity',
            'proof_table_optimization': 'Cache frequently validated proof table entries'
        }
        
        return {
            'analysis_results': optimization_results,
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        }
    
    async def close(self) -> None:
        """Close Neo4j connection"""
        if self.driver:
            await self.driver.close()
            logger.info("Neo4j knowledge graph manager closed")

# Utility functions for direct usage
async def initialize_neo4j_knowledge_graph():
    """Initialize Neo4j knowledge graph - can be called directly"""
    config = DatabaseConfig()
    kg_manager = Neo4jKnowledgeGraphManager(config)
    
    try:
        await kg_manager.initialize()
        
        # Test SBVR functionality
        test_rule_validation = await kg_manager.validate_business_rule(
            'test_rule_id',
            {'customer_verified': True, 'product_available': True}
        )
        
        logger.info(f"SBVR test validation result: {test_rule_validation}")
        
        # Test optimization
        optimization_results = await kg_manager.optimize_reasoning_performance()
        logger.info(f"Optimization analysis completed: {len(optimization_results['analysis_results'])} analyses")
        
        return True
        
    except Exception as e:
        logger.error(f"Neo4j knowledge graph initialization failed: {e}")
        return False
    finally:
        await kg_manager.close()

if __name__ == "__main__":
    # Run Neo4j knowledge graph initialization
    asyncio.run(initialize_neo4j_knowledge_graph()) 