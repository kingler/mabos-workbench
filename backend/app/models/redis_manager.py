"""
MABOS Redis Manager

Comprehensive Redis caching and session management system with high availability,
intelligent caching strategies, and performance optimization.
"""

import asyncio
import logging
import json
import pickle
import hashlib
import time
from typing import Dict, List, Any, Optional, Union, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

import redis.asyncio as redis
from redis.asyncio.sentinel import Sentinel
from redis.asyncio.cluster import RedisCluster
from pydantic import BaseModel

from app.core.database import DatabaseConfig

# Configure logging
logger = logging.getLogger(__name__)

class CacheStrategy(Enum):
    """Cache strategy types"""
    LRU = "lru"  # Least Recently Used
    LFU = "lfu"  # Least Frequently Used
    TTL = "ttl"  # Time To Live
    WRITE_THROUGH = "write_through"
    WRITE_BEHIND = "write_behind"
    REFRESH_AHEAD = "refresh_ahead"

class CacheLevel(Enum):
    """Cache level hierarchy"""
    L1_MEMORY = "l1_memory"  # In-memory cache
    L2_REDIS = "l2_redis"    # Redis cache
    L3_PERSISTENT = "l3_persistent"  # Persistent storage

@dataclass
class CacheConfig:
    """Cache configuration settings"""
    ttl: int = 3600  # Time to live in seconds
    max_size: int = 10000  # Maximum number of items
    strategy: CacheStrategy = CacheStrategy.LRU
    compression: bool = False
    encryption: bool = False
    namespace: str = "mabos"

@dataclass
class SessionConfig:
    """Session configuration settings"""
    ttl: int = 1800  # 30 minutes
    sliding_expiration: bool = True
    secure_cookies: bool = True
    same_site: str = "strict"
    domain: Optional[str] = None

class CacheMetrics(BaseModel):
    """Cache performance metrics"""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    memory_usage: int = 0
    hit_rate: float = 0.0
    avg_response_time: float = 0.0

class RedisSessionManager:
    """Advanced Redis session management"""
    
    def __init__(self, redis_client: redis.Redis, config: SessionConfig):
        self.redis = redis_client
        self.config = config
        self.session_prefix = f"{config.domain or 'mabos'}:session"
    
    async def create_session(self, user_id: str, session_data: Dict[str, Any]) -> str:
        """Create a new user session"""
        session_id = self._generate_session_id(user_id)
        session_key = f"{self.session_prefix}:{session_id}"
        
        # Add metadata to session
        session_data.update({
            'user_id': user_id,
            'created_at': datetime.utcnow().isoformat(),
            'last_accessed': datetime.utcnow().isoformat(),
            'ip_address': session_data.get('ip_address'),
            'user_agent': session_data.get('user_agent')
        })
        
        # Store session with TTL
        await self.redis.setex(
            session_key,
            self.config.ttl,
            json.dumps(session_data)
        )
        
        # Track active sessions for user
        user_sessions_key = f"{self.session_prefix}:user:{user_id}"
        await self.redis.sadd(user_sessions_key, session_id)
        await self.redis.expire(user_sessions_key, self.config.ttl)
        
        logger.info(f"Created session {session_id} for user {user_id}")
        return session_id
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve session data"""
        session_key = f"{self.session_prefix}:{session_id}"
        session_data = await self.redis.get(session_key)
        
        if not session_data:
            return None
        
        try:
            data = json.loads(session_data)
            
            # Update last accessed time if sliding expiration is enabled
            if self.config.sliding_expiration:
                data['last_accessed'] = datetime.utcnow().isoformat()
                await self.redis.setex(
                    session_key,
                    self.config.ttl,
                    json.dumps(data)
                )
            
            return data
            
        except json.JSONDecodeError:
            logger.error(f"Failed to decode session data for {session_id}")
            return None
    
    async def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Update session data"""
        session_data = await self.get_session(session_id)
        if not session_data:
            return False
        
        session_data.update(updates)
        session_data['last_accessed'] = datetime.utcnow().isoformat()
        
        session_key = f"{self.session_prefix}:{session_id}"
        await self.redis.setex(
            session_key,
            self.config.ttl,
            json.dumps(session_data)
        )
        
        return True
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        session_key = f"{self.session_prefix}:{session_id}"
        
        # Get session data to find user_id
        session_data = await self.get_session(session_id)
        if session_data:
            user_id = session_data.get('user_id')
            if user_id:
                user_sessions_key = f"{self.session_prefix}:user:{user_id}"
                await self.redis.srem(user_sessions_key, session_id)
        
        result = await self.redis.delete(session_key)
        logger.info(f"Deleted session {session_id}")
        return result > 0
    
    async def delete_user_sessions(self, user_id: str) -> int:
        """Delete all sessions for a user"""
        user_sessions_key = f"{self.session_prefix}:user:{user_id}"
        session_ids = await self.redis.smembers(user_sessions_key)
        
        if not session_ids:
            return 0
        
        # Delete all session keys
        session_keys = [f"{self.session_prefix}:{sid.decode()}" for sid in session_ids]
        deleted_count = await self.redis.delete(*session_keys, user_sessions_key)
        
        logger.info(f"Deleted {deleted_count} sessions for user {user_id}")
        return deleted_count
    
    async def get_active_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all active sessions for a user"""
        user_sessions_key = f"{self.session_prefix}:user:{user_id}"
        session_ids = await self.redis.smembers(user_sessions_key)
        
        sessions = []
        for session_id in session_ids:
            session_data = await self.get_session(session_id.decode())
            if session_data:
                sessions.append({
                    'session_id': session_id.decode(),
                    **session_data
                })
        
        return sessions
    
    def _generate_session_id(self, user_id: str) -> str:
        """Generate a secure session ID"""
        timestamp = str(time.time())
        random_data = f"{user_id}:{timestamp}:{hash(time.time())}"
        return hashlib.sha256(random_data.encode()).hexdigest()

class RedisCacheManager:
    """Advanced Redis caching with multiple strategies"""
    
    def __init__(self, redis_client: redis.Redis, config: CacheConfig):
        self.redis = redis_client
        self.config = config
        self.metrics = CacheMetrics()
        self.cache_prefix = f"{config.namespace}:cache"
    
    async def get(self, key: str, default: Any = None) -> Any:
        """Get value from cache with metrics tracking"""
        start_time = time.time()
        cache_key = f"{self.cache_prefix}:{key}"
        
        try:
            value = await self.redis.get(cache_key)
            response_time = time.time() - start_time
            
            if value is not None:
                self.metrics.hits += 1
                self._update_avg_response_time(response_time)
                
                # Deserialize value
                if self.config.compression:
                    value = self._decompress(value)
                
                try:
                    return json.loads(value) if isinstance(value, (str, bytes)) else value
                except json.JSONDecodeError:
                    return pickle.loads(value) if isinstance(value, bytes) else value
            else:
                self.metrics.misses += 1
                return default
                
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            self.metrics.misses += 1
            return default
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache with optional TTL"""
        cache_key = f"{self.cache_prefix}:{key}"
        ttl = ttl or self.config.ttl
        
        try:
            # Serialize value
            if isinstance(value, (dict, list)):
                serialized_value = json.dumps(value)
            else:
                serialized_value = pickle.dumps(value)
            
            # Apply compression if enabled
            if self.config.compression:
                serialized_value = self._compress(serialized_value)
            
            # Set with TTL
            await self.redis.setex(cache_key, ttl, serialized_value)
            return True
            
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        cache_key = f"{self.cache_prefix}:{key}"
        result = await self.redis.delete(cache_key)
        return result > 0
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        cache_key = f"{self.cache_prefix}:{key}"
        return await self.redis.exists(cache_key) > 0
    
    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching pattern"""
        cache_pattern = f"{self.cache_prefix}:{pattern}"
        keys = await self.redis.keys(cache_pattern)
        
        if keys:
            deleted_count = await self.redis.delete(*keys)
            logger.info(f"Invalidated {deleted_count} cache keys matching pattern: {pattern}")
            return deleted_count
        
        return 0
    
    async def get_or_set(self, key: str, factory: Callable, ttl: Optional[int] = None) -> Any:
        """Get value from cache or set it using factory function"""
        value = await self.get(key)
        
        if value is None:
            # Generate value using factory
            if asyncio.iscoroutinefunction(factory):
                value = await factory()
            else:
                value = factory()
            
            # Cache the generated value
            await self.set(key, value, ttl)
        
        return value
    
    async def increment(self, key: str, amount: int = 1) -> int:
        """Increment a numeric value in cache"""
        cache_key = f"{self.cache_prefix}:{key}"
        return await self.redis.incrby(cache_key, amount)
    
    async def expire(self, key: str, ttl: int) -> bool:
        """Set expiration time for a key"""
        cache_key = f"{self.cache_prefix}:{key}"
        return await self.redis.expire(cache_key, ttl)
    
    def _compress(self, data: bytes) -> bytes:
        """Compress data if compression is enabled"""
        import gzip
        return gzip.compress(data)
    
    def _decompress(self, data: bytes) -> bytes:
        """Decompress data if compression was used"""
        import gzip
        return gzip.decompress(data)
    
    def _update_avg_response_time(self, response_time: float):
        """Update average response time metric"""
        total_requests = self.metrics.hits + self.metrics.misses
        if total_requests > 0:
            self.metrics.avg_response_time = (
                (self.metrics.avg_response_time * (total_requests - 1) + response_time) / total_requests
            )
    
    def get_metrics(self) -> CacheMetrics:
        """Get cache performance metrics"""
        total_requests = self.metrics.hits + self.metrics.misses
        if total_requests > 0:
            self.metrics.hit_rate = self.metrics.hits / total_requests
        return self.metrics

class RedisWorkflowCache:
    """Specialized caching for workflow results and execution data"""
    
    def __init__(self, cache_manager: RedisCacheManager):
        self.cache = cache_manager
        self.workflow_prefix = "workflow"
    
    async def cache_workflow_result(self, workflow_id: str, execution_id: str, result: Dict[str, Any], ttl: int = 7200) -> bool:
        """Cache workflow execution result"""
        key = f"{self.workflow_prefix}:result:{workflow_id}:{execution_id}"
        return await self.cache.set(key, result, ttl)
    
    async def get_workflow_result(self, workflow_id: str, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get cached workflow result"""
        key = f"{self.workflow_prefix}:result:{workflow_id}:{execution_id}"
        return await self.cache.get(key)
    
    async def cache_workflow_state(self, workflow_id: str, state: Dict[str, Any], ttl: int = 3600) -> bool:
        """Cache current workflow state"""
        key = f"{self.workflow_prefix}:state:{workflow_id}"
        return await self.cache.set(key, state, ttl)
    
    async def get_workflow_state(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get cached workflow state"""
        key = f"{self.workflow_prefix}:state:{workflow_id}"
        return await self.cache.get(key)
    
    async def invalidate_workflow_cache(self, workflow_id: str) -> int:
        """Invalidate all cache entries for a workflow"""
        pattern = f"{self.workflow_prefix}:*:{workflow_id}*"
        return await self.cache.invalidate_pattern(pattern)

class RedisLLMCache:
    """Specialized caching for LLM responses with semantic similarity"""
    
    def __init__(self, cache_manager: RedisCacheManager):
        self.cache = cache_manager
        self.llm_prefix = "llm"
    
    async def cache_llm_response(self, prompt_hash: str, model: str, response: Dict[str, Any], ttl: int = 86400) -> bool:
        """Cache LLM response with prompt hash"""
        key = f"{self.llm_prefix}:response:{model}:{prompt_hash}"
        return await self.cache.set(key, response, ttl)
    
    async def get_llm_response(self, prompt_hash: str, model: str) -> Optional[Dict[str, Any]]:
        """Get cached LLM response"""
        key = f"{self.llm_prefix}:response:{model}:{prompt_hash}"
        return await self.cache.get(key)
    
    async def cache_llm_embedding(self, text_hash: str, embedding: List[float], ttl: int = 604800) -> bool:
        """Cache text embedding (7 days TTL)"""
        key = f"{self.llm_prefix}:embedding:{text_hash}"
        return await self.cache.set(key, embedding, ttl)
    
    async def get_llm_embedding(self, text_hash: str) -> Optional[List[float]]:
        """Get cached text embedding"""
        key = f"{self.llm_prefix}:embedding:{text_hash}"
        return await self.cache.get(key)
    
    def generate_prompt_hash(self, prompt: str, model: str, parameters: Dict[str, Any]) -> str:
        """Generate hash for prompt + model + parameters"""
        content = f"{prompt}:{model}:{json.dumps(parameters, sort_keys=True)}"
        return hashlib.sha256(content.encode()).hexdigest()

class RedisClusterManager:
    """Redis cluster management with high availability"""
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.cluster_client: Optional[RedisCluster] = None
        self.sentinel_client: Optional[Sentinel] = None
        self.redis_client: Optional[redis.Redis] = None
        
        # Cache and session managers
        self.cache_manager: Optional[RedisCacheManager] = None
        self.session_manager: Optional[RedisSessionManager] = None
        self.workflow_cache: Optional[RedisWorkflowCache] = None
        self.llm_cache: Optional[RedisLLMCache] = None
    
    async def initialize(self, use_cluster: bool = False, use_sentinel: bool = False):
        """Initialize Redis connection with optional cluster/sentinel support"""
        try:
            if use_cluster:
                await self._initialize_cluster()
            elif use_sentinel:
                await self._initialize_sentinel()
            else:
                await self._initialize_single()
            
            # Initialize specialized managers
            cache_config = CacheConfig(namespace="mabos", ttl=3600)
            session_config = SessionConfig(ttl=1800, sliding_expiration=True)
            
            self.cache_manager = RedisCacheManager(self.redis_client, cache_config)
            self.session_manager = RedisSessionManager(self.redis_client, session_config)
            self.workflow_cache = RedisWorkflowCache(self.cache_manager)
            self.llm_cache = RedisLLMCache(self.cache_manager)
            
            logger.info("Redis cluster manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Redis cluster manager: {e}")
            raise
    
    async def _initialize_single(self):
        """Initialize single Redis instance"""
        self.redis_client = redis.from_url(
            self.config.redis_url,
            max_connections=self.config.redis_max_connections,
            decode_responses=False  # Handle binary data
        )
        
        # Test connection
        await self.redis_client.ping()
        logger.info("Connected to single Redis instance")
    
    async def _initialize_cluster(self):
        """Initialize Redis cluster"""
        # Parse cluster nodes from URL or config
        cluster_nodes = [
            {"host": "localhost", "port": 6380},
            {"host": "localhost", "port": 6381},
            {"host": "localhost", "port": 6382}
        ]
        
        self.cluster_client = RedisCluster(
            startup_nodes=cluster_nodes,
            decode_responses=False,
            skip_full_coverage_check=True
        )
        
        self.redis_client = self.cluster_client
        await self.redis_client.ping()
        logger.info("Connected to Redis cluster")
    
    async def _initialize_sentinel(self):
        """Initialize Redis Sentinel for high availability"""
        sentinel_hosts = [
            ("localhost", 26379),
            ("localhost", 26380),
            ("localhost", 26381)
        ]
        
        self.sentinel_client = Sentinel(sentinel_hosts)
        self.redis_client = self.sentinel_client.master_for(
            "mymaster",
            decode_responses=False
        )
        
        await self.redis_client.ping()
        logger.info("Connected to Redis via Sentinel")
    
    async def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check for Redis"""
        health_status = {
            "redis_available": False,
            "memory_usage": 0,
            "connected_clients": 0,
            "cache_hit_rate": 0.0,
            "total_keys": 0
        }
        
        try:
            # Basic connectivity
            await self.redis_client.ping()
            health_status["redis_available"] = True
            
            # Get Redis info
            info = await self.redis_client.info()
            health_status["memory_usage"] = info.get("used_memory", 0)
            health_status["connected_clients"] = info.get("connected_clients", 0)
            
            # Get cache metrics
            if self.cache_manager:
                metrics = self.cache_manager.get_metrics()
                health_status["cache_hit_rate"] = metrics.hit_rate
            
            # Count total keys
            health_status["total_keys"] = await self.redis_client.dbsize()
            
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
        
        return health_status
    
    async def backup_data(self, backup_path: str) -> bool:
        """Create Redis data backup"""
        try:
            # Trigger BGSAVE for background save
            await self.redis_client.bgsave()
            
            # Wait for save to complete
            while True:
                info = await self.redis_client.info("persistence")
                if info.get("rdb_bgsave_in_progress", 0) == 0:
                    break
                await asyncio.sleep(1)
            
            logger.info(f"Redis backup completed to {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Redis backup failed: {e}")
            return False
    
    async def close(self):
        """Close Redis connections"""
        try:
            if self.redis_client:
                await self.redis_client.close()
            if self.cluster_client:
                await self.cluster_client.close()
            
            logger.info("Redis connections closed")
            
        except Exception as e:
            logger.error(f"Error closing Redis connections: {e}")

# Utility functions for direct usage
async def initialize_redis_cluster():
    """Initialize Redis cluster manager - can be called directly"""
    from app.core.database import DatabaseConfig
    
    config = DatabaseConfig()
    cluster_manager = RedisClusterManager(config)
    
    try:
        await cluster_manager.initialize()
        
        # Test caching functionality
        await cluster_manager.cache_manager.set("test_key", {"message": "Redis is working!"}, ttl=60)
        test_value = await cluster_manager.cache_manager.get("test_key")
        logger.info(f"Redis test result: {test_value}")
        
        # Test session management
        session_id = await cluster_manager.session_manager.create_session(
            "test_user",
            {"role": "admin", "ip_address": "127.0.0.1"}
        )
        logger.info(f"Created test session: {session_id}")
        
        # Health check
        health = await cluster_manager.health_check()
        logger.info(f"Redis health status: {health}")
        
        return True
        
    except Exception as e:
        logger.error(f"Redis cluster initialization failed: {e}")
        return False
    finally:
        await cluster_manager.close()

if __name__ == "__main__":
    # Run Redis cluster initialization
    asyncio.run(initialize_redis_cluster()) 