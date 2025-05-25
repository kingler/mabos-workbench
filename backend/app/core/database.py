"""
MABOS Database Manager

Multi-database coordination system for PostgreSQL, Neo4j, Redis, and Elasticsearch.
Implements the database architecture plan with BDI agent knowledge graph integration.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import json

# Database drivers
import asyncpg
from neo4j import AsyncGraphDatabase
import redis.asyncio as redis
from elasticsearch import AsyncElasticsearch

# Configuration and utilities
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Logging setup
logger = logging.getLogger(__name__)


class DatabaseConfig(BaseSettings):
    """Database configuration settings"""
    
    # PostgreSQL Configuration
    postgres_url: str = "postgresql+asyncpg://mabos_user:mabos_password@localhost:5433/mabos_db"
    postgres_pool_size: int = 20
    postgres_max_overflow: int = 30
    
    # Neo4j Configuration
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "neo4j_password"
    neo4j_database: str = "mabos"
    
    # Redis Configuration
    redis_url: str = "redis://localhost:6380/0"
    redis_max_connections: int = 50
    
    # Elasticsearch Configuration
    elasticsearch_url: str = "http://localhost:9200"
    elasticsearch_index_prefix: str = "mabos"
    
    class Config:
        env_file = ".env"


class PostgreSQLManager:
    """PostgreSQL database manager for primary relational data"""
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.engine = None
        self.session_factory = None
        
    async def initialize(self):
        """Initialize PostgreSQL connection and session factory"""
        try:
            self.engine = create_async_engine(
                self.config.postgres_url,
                pool_size=self.config.postgres_pool_size,
                max_overflow=self.config.postgres_max_overflow,
                echo=False  # Set to True for SQL debugging
            )
            
            self.session_factory = sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            
            logger.info("PostgreSQL manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize PostgreSQL: {e}")
            raise
    
    async def get_session(self) -> AsyncSession:
        """Get an async database session"""
        if not self.session_factory:
            await self.initialize()
        return self.session_factory()
    
    async def execute_query(self, query: str, params: Dict = None) -> List[Dict]:
        """Execute a raw SQL query"""
        async with self.engine.begin() as conn:
            from sqlalchemy import text
            result = await conn.execute(text(query), params or {})
            return [dict(row) for row in result.fetchall()]
    
    async def health_check(self) -> bool:
        """Check PostgreSQL connection health"""
        try:
            async with self.engine.begin() as conn:
                from sqlalchemy import text
                await conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"PostgreSQL health check failed: {e}")
            return False


class Neo4jManager:
    """Neo4j graph database manager for BDI agent knowledge"""
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.driver = None
        
    async def initialize(self):
        """Initialize Neo4j driver"""
        try:
            self.driver = AsyncGraphDatabase.driver(
                self.config.neo4j_uri,
                auth=(self.config.neo4j_user, self.config.neo4j_password)
            )
            
            # Verify connectivity
            await self.driver.verify_connectivity()
            logger.info("Neo4j manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Neo4j: {e}")
            raise
    
    async def execute_query(self, query: str, params: Dict = None) -> List[Dict]:
        """Execute a Cypher query"""
        async with self.driver.session(database=self.config.neo4j_database) as session:
            result = await session.run(query, params or {})
            records = await result.data()
            # Convert Neo4j DateTime objects to ISO strings for JSON serialization
            return [self._serialize_neo4j_types(record) for record in records]
    
    def _serialize_neo4j_types(self, obj):
        """Convert Neo4j types to JSON-serializable types"""
        if hasattr(obj, '__dict__'):
            # Handle Neo4j DateTime objects
            from neo4j.time import DateTime
            if isinstance(obj, DateTime):
                return obj.isoformat()
        
        if isinstance(obj, dict):
            return {key: self._serialize_neo4j_types(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._serialize_neo4j_types(item) for item in obj]
        elif hasattr(obj, 'isoformat'):  # Handle datetime-like objects
            return obj.isoformat()
        else:
            return obj
    
    async def create_agent_belief(self, agent_id: str, belief_data: Dict) -> Dict:
        """Create a new belief for a BDI agent"""
        query = """
        MATCH (agent:Agent {id: $agent_id})
        CREATE (belief:Belief {
            id: $belief_id,
            category: $category,
            content: $content,
            confidence: $confidence,
            source: $source,
            created_at: datetime(),
            last_updated: datetime(),
            description: $description
        })
        CREATE (agent)-[:HAS_BELIEF]->(belief)
        RETURN belief
        """
        
        params = {
            "agent_id": agent_id,
            "belief_id": f"belief_{agent_id}_{datetime.now().timestamp()}",
            **belief_data
        }
        
        result = await self.execute_query(query, params)
        return result[0] if result else None
    
    async def update_agent_intention_progress(self, intention_id: str, progress: float) -> bool:
        """Update the progress of an agent's intention"""
        query = """
        MATCH (intention:Intention {id: $intention_id})
        SET intention.progress = $progress,
            intention.last_updated = datetime()
        RETURN intention.id as id
        """
        
        result = await self.execute_query(query, {"intention_id": intention_id, "progress": progress})
        return len(result) > 0
    
    async def get_agent_knowledge_graph(self, agent_id: str) -> Dict:
        """Get the complete knowledge graph for a specific agent"""
        query = """
        MATCH (agent:Agent {id: $agent_id})
        OPTIONAL MATCH (agent)-[:HAS_BELIEF]->(belief:Belief)
        OPTIONAL MATCH (agent)-[:HAS_DESIRE]->(desire:Desire)
        OPTIONAL MATCH (agent)-[:HAS_INTENTION]->(intention:Intention)
        OPTIONAL MATCH (intention)-[:ACHIEVED_BY]->(plan:Plan)
        RETURN agent, 
               collect(DISTINCT belief) as beliefs,
               collect(DISTINCT desire) as desires,
               collect(DISTINCT intention) as intentions,
               collect(DISTINCT plan) as plans
        """
        
        result = await self.execute_query(query, {"agent_id": agent_id})
        return result[0] if result else None
    
    async def health_check(self) -> bool:
        """Check Neo4j connection health"""
        try:
            result = await self.execute_query("RETURN 1 as health")
            return len(result) > 0
        except Exception as e:
            logger.error(f"Neo4j health check failed: {e}")
            return False


class RedisManager:
    """Redis cache and session manager"""
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.redis_client = None
        
    async def initialize(self):
        """Initialize Redis connection"""
        try:
            self.redis_client = redis.from_url(
                self.config.redis_url,
                max_connections=self.config.redis_max_connections,
                decode_responses=True
            )
            
            # Test connection
            await self.redis_client.ping()
            logger.info("Redis manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Redis: {e}")
            raise
    
    async def set_cache(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set a cache value with TTL"""
        try:
            serialized_value = json.dumps(value) if not isinstance(value, str) else value
            await self.redis_client.setex(key, ttl, serialized_value)
            return True
        except Exception as e:
            logger.error(f"Failed to set cache key {key}: {e}")
            return False
    
    async def get_cache(self, key: str) -> Optional[Any]:
        """Get a cache value"""
        try:
            value = await self.redis_client.get(key)
            if value:
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            return None
        except Exception as e:
            logger.error(f"Failed to get cache key {key}: {e}")
            return None
    
    async def delete_cache(self, key: str) -> bool:
        """Delete a cache key"""
        try:
            result = await self.redis_client.delete(key)
            return result > 0
        except Exception as e:
            logger.error(f"Failed to delete cache key {key}: {e}")
            return False
    
    async def set_agent_state(self, agent_id: str, state: Dict) -> bool:
        """Set agent state in cache"""
        key = f"agent:state:{agent_id}"
        return await self.set_cache(key, state, ttl=1800)  # 30 minutes
    
    async def get_agent_state(self, agent_id: str) -> Optional[Dict]:
        """Get agent state from cache"""
        key = f"agent:state:{agent_id}"
        return await self.get_cache(key)
    
    async def health_check(self) -> bool:
        """Check Redis connection health"""
        try:
            await self.redis_client.ping()
            return True
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return False


class ElasticsearchManager:
    """Elasticsearch manager for search and analytics"""
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.client = None
        
    async def initialize(self):
        """Initialize Elasticsearch client"""
        try:
            self.client = AsyncElasticsearch([self.config.elasticsearch_url])
            
            # Test connection
            await self.client.ping()
            logger.info("Elasticsearch manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Elasticsearch: {e}")
            raise
    
    async def index_workflow(self, workflow_id: str, workflow_data: Dict) -> bool:
        """Index a workflow for search"""
        try:
            index_name = f"{self.config.elasticsearch_index_prefix}_workflows"
            
            doc = {
                "workflow_id": workflow_id,
                "indexed_at": datetime.utcnow().isoformat(),
                **workflow_data
            }
            
            await self.client.index(
                index=index_name,
                id=workflow_id,
                document=doc
            )
            return True
            
        except Exception as e:
            logger.error(f"Failed to index workflow {workflow_id}: {e}")
            return False
    
    async def search_workflows(self, query: str, filters: Dict = None) -> List[Dict]:
        """Search workflows"""
        try:
            index_name = f"{self.config.elasticsearch_index_prefix}_workflows"
            
            search_body = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "multi_match": {
                                    "query": query,
                                    "fields": ["name", "description", "tags"]
                                }
                            }
                        ]
                    }
                }
            }
            
            # Add filters if provided
            if filters:
                search_body["query"]["bool"]["filter"] = []
                for field, value in filters.items():
                    search_body["query"]["bool"]["filter"].append({
                        "term": {field: value}
                    })
            
            response = await self.client.search(
                index=index_name,
                body=search_body
            )
            
            return [hit["_source"] for hit in response["hits"]["hits"]]
            
        except Exception as e:
            logger.error(f"Failed to search workflows: {e}")
            return []
    
    async def health_check(self) -> bool:
        """Check Elasticsearch connection health"""
        try:
            await self.client.ping()
            return True
        except Exception as e:
            logger.error(f"Elasticsearch health check failed: {e}")
            return False


class DatabaseManager:
    """
    Unified database manager coordinating PostgreSQL, Neo4j, Redis, and Elasticsearch
    Implements the MABOS multi-database architecture
    """
    
    def __init__(self, config: DatabaseConfig = None):
        self.config = config or DatabaseConfig()
        
        # Initialize database managers
        self.postgres = PostgreSQLManager(self.config)
        self.neo4j = Neo4jManager(self.config)
        self.redis = RedisManager(self.config)
        self.elasticsearch = ElasticsearchManager(self.config)
        
        self._initialized = False
    
    async def initialize(self):
        """Initialize all database connections"""
        if self._initialized:
            return
        
        logger.info("Initializing MABOS database manager...")
        
        # Initialize all database managers concurrently
        await asyncio.gather(
            self.postgres.initialize(),
            self.neo4j.initialize(),
            self.redis.initialize(),
            self.elasticsearch.initialize(),
            return_exceptions=True
        )
        
        self._initialized = True
        logger.info("MABOS database manager initialized successfully")
    
    async def sync_workflow_to_knowledge_graph(self, workflow_data: Dict) -> bool:
        """
        Synchronize workflow data across all databases
        1. Store workflow in PostgreSQL
        2. Update agent beliefs in Neo4j
        3. Cache workflow state in Redis
        4. Index workflow in Elasticsearch
        """
        try:
            workflow_id = workflow_data.get("id")
            
            # Update agent beliefs about new workflow
            belief_data = {
                "category": "workflow_status",
                "content": f"workflow_{workflow_id}_created",
                "confidence": 0.95,
                "source": "workflow_manager",
                "description": f"New workflow {workflow_data.get('name')} created"
            }
            
            # Execute synchronization tasks concurrently
            tasks = [
                self.neo4j.create_agent_belief("agent_workflow_001", belief_data),
                self.redis.set_cache(f"workflow:cache:{workflow_id}", workflow_data),
                self.elasticsearch.index_workflow(workflow_id, workflow_data)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Check if all operations succeeded
            success = all(not isinstance(result, Exception) for result in results)
            
            if success:
                logger.info(f"Successfully synchronized workflow {workflow_id} across all databases")
            else:
                logger.warning(f"Partial synchronization failure for workflow {workflow_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to sync workflow to knowledge graph: {e}")
            return False
    
    async def get_agent_context(self, agent_id: str) -> Dict:
        """
        Get comprehensive agent context from multiple databases
        Combines Neo4j knowledge graph with Redis cached state
        """
        try:
            # Get data from multiple sources concurrently
            knowledge_graph_task = self.neo4j.get_agent_knowledge_graph(agent_id)
            cached_state_task = self.redis.get_agent_state(agent_id)
            
            knowledge_graph, cached_state = await asyncio.gather(
                knowledge_graph_task,
                cached_state_task,
                return_exceptions=True
            )
            
            # Combine results
            context = {
                "agent_id": agent_id,
                "knowledge_graph": knowledge_graph if not isinstance(knowledge_graph, Exception) else None,
                "cached_state": cached_state if not isinstance(cached_state, Exception) else None,
                "retrieved_at": datetime.utcnow().isoformat()
            }
            
            return context
            
        except Exception as e:
            logger.error(f"Failed to get agent context for {agent_id}: {e}")
            return {"agent_id": agent_id, "error": str(e)}
    
    async def health_check(self) -> Dict[str, bool]:
        """Check health of all database connections"""
        health_tasks = {
            "postgres": self.postgres.health_check(),
            "neo4j": self.neo4j.health_check(),
            "redis": self.redis.health_check(),
            "elasticsearch": self.elasticsearch.health_check()
        }
        
        results = await asyncio.gather(*health_tasks.values(), return_exceptions=True)
        
        health_status = {}
        for db_name, result in zip(health_tasks.keys(), results):
            health_status[db_name] = result if not isinstance(result, Exception) else False
        
        return health_status
    
    async def close(self):
        """Close all database connections"""
        try:
            if self.neo4j.driver:
                await self.neo4j.driver.close()
            if self.redis.redis_client:
                await self.redis.redis_client.close()
            if self.elasticsearch.client:
                await self.elasticsearch.client.close()
            if self.postgres.engine:
                await self.postgres.engine.dispose()
                
            logger.info("All database connections closed")
            
        except Exception as e:
            logger.error(f"Error closing database connections: {e}")


# Global database manager instance
db_manager = DatabaseManager()


async def get_database_manager() -> DatabaseManager:
    """Dependency injection for database manager"""
    if not db_manager._initialized:
        await db_manager.initialize()
    return db_manager


# Convenience functions for specific database access
async def get_postgres_session():
    """Get PostgreSQL session"""
    manager = await get_database_manager()
    return await manager.postgres.get_session()


async def get_neo4j_session():
    """Get Neo4j session"""
    manager = await get_database_manager()
    return manager.neo4j


async def get_redis_client():
    """Get Redis client"""
    manager = await get_database_manager()
    return manager.redis


async def get_elasticsearch_client():
    """Get Elasticsearch client"""
    manager = await get_database_manager()
    return manager.elasticsearch 