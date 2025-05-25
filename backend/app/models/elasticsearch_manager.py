"""
MABOS Elasticsearch Manager

Comprehensive search and analytics system with advanced indexing strategies,
faceted search capabilities, and real-time data processing.
"""

import asyncio
import logging
import json
import hashlib
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError, RequestError
from pydantic import BaseModel

from app.core.database import DatabaseConfig

# Configure logging
logger = logging.getLogger(__name__)

class IndexType(Enum):
    """Elasticsearch index types for different data categories"""
    WORKFLOWS = "workflows"
    EXECUTIONS = "executions"
    USERS = "users"
    AGENTS = "agents"
    LOGS = "logs"
    METRICS = "metrics"
    EVENTS = "events"
    DOCUMENTS = "documents"

class SearchScope(Enum):
    """Search scope definitions"""
    GLOBAL = "global"
    WORKFLOW = "workflow"
    USER = "user"
    AGENT = "agent"
    SYSTEM = "system"

@dataclass
class IndexConfig:
    """Index configuration settings"""
    name: str
    mappings: Dict[str, Any]
    settings: Dict[str, Any]
    aliases: List[str] = None
    lifecycle_policy: str = None

@dataclass
class SearchQuery:
    """Search query configuration"""
    query: str
    filters: Dict[str, Any] = None
    sort: List[Dict[str, Any]] = None
    size: int = 10
    from_: int = 0
    highlight: Dict[str, Any] = None
    aggregations: Dict[str, Any] = None

class SearchResult(BaseModel):
    """Search result model"""
    total: int
    hits: List[Dict[str, Any]]
    aggregations: Dict[str, Any] = None
    took: int
    timed_out: bool

class ElasticsearchAnalyticsManager:
    """Advanced Elasticsearch analytics and search manager"""
    
    def __init__(self, config: DatabaseConfig):
        """Initialize Elasticsearch analytics manager"""
        self.config = config
        self.client: Optional[AsyncElasticsearch] = None
        self.index_prefix = config.elasticsearch_index_prefix
        
        # Index configurations
        self.index_configs = self._get_index_configurations()
    
    async def initialize(self) -> None:
        """Initialize Elasticsearch connection and indices"""
        try:
            # Create Elasticsearch client with proper configuration
            self.client = AsyncElasticsearch(
                [self.config.elasticsearch_url],
                request_timeout=30,
                max_retries=3,
                retry_on_timeout=True
            )
            
            # Test connection
            await self.client.ping()
            
            # Initialize indices
            await self._initialize_indices()
            
            # Set up index lifecycle policies
            await self._setup_lifecycle_policies()
            
            logger.info("Elasticsearch analytics manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Elasticsearch analytics manager: {e}")
            raise
    
    def _get_index_configurations(self) -> Dict[IndexType, IndexConfig]:
        """Get index configurations for different data types"""
        return {
            IndexType.WORKFLOWS: IndexConfig(
                name=f"{self.index_prefix}_workflows",
                mappings={
                    "properties": {
                        "workflow_id": {"type": "keyword"},
                        "name": {"type": "text", "analyzer": "standard"},
                        "description": {"type": "text", "analyzer": "standard"},
                        "version": {"type": "keyword"},
                        "status": {"type": "keyword"},
                        "created_by": {"type": "keyword"},
                        "created_at": {"type": "date"},
                        "updated_at": {"type": "date"},
                        "tags": {"type": "keyword"},
                        "category": {"type": "keyword"},
                        "complexity_score": {"type": "float"},
                        "execution_count": {"type": "long"},
                        "success_rate": {"type": "float"},
                        "avg_duration": {"type": "float"},
                        "definition": {"type": "object", "enabled": False},
                        "metadata": {"type": "object"}
                    }
                },
                settings={
                    "number_of_shards": 2,
                    "number_of_replicas": 1,
                    "analysis": {
                        "analyzer": {
                            "workflow_analyzer": {
                                "type": "custom",
                                "tokenizer": "standard",
                                "filter": ["lowercase", "stop", "snowball"]
                            }
                        }
                    }
                },
                aliases=["workflows", "workflow_search"]
            ),
            
            IndexType.EXECUTIONS: IndexConfig(
                name=f"{self.index_prefix}_executions",
                mappings={
                    "properties": {
                        "execution_id": {"type": "keyword"},
                        "workflow_id": {"type": "keyword"},
                        "workflow_name": {"type": "text"},
                        "status": {"type": "keyword"},
                        "started_at": {"type": "date"},
                        "completed_at": {"type": "date"},
                        "duration": {"type": "float"},
                        "triggered_by": {"type": "keyword"},
                        "trigger_type": {"type": "keyword"},
                        "input_data": {"type": "object", "enabled": False},
                        "output_data": {"type": "object", "enabled": False},
                        "error_message": {"type": "text"},
                        "step_count": {"type": "integer"},
                        "completed_steps": {"type": "integer"},
                        "failed_steps": {"type": "integer"},
                        "resource_usage": {
                            "properties": {
                                "cpu_time": {"type": "float"},
                                "memory_peak": {"type": "long"},
                                "network_io": {"type": "long"},
                                "disk_io": {"type": "long"}
                            }
                        },
                        "agent_assignments": {"type": "keyword"},
                        "execution_context": {"type": "object"}
                    }
                },
                settings={
                    "number_of_shards": 3,
                    "number_of_replicas": 1,
                    "index.lifecycle.name": "execution_policy"
                },
                aliases=["executions", "execution_logs"]
            ),
            
            IndexType.USERS: IndexConfig(
                name=f"{self.index_prefix}_users",
                mappings={
                    "properties": {
                        "user_id": {"type": "keyword"},
                        "username": {"type": "keyword"},
                        "email": {"type": "keyword"},
                        "full_name": {"type": "text"},
                        "role": {"type": "keyword"},
                        "department": {"type": "keyword"},
                        "organization": {"type": "keyword"},
                        "created_at": {"type": "date"},
                        "last_login": {"type": "date"},
                        "is_active": {"type": "boolean"},
                        "permissions": {"type": "keyword"},
                        "workflow_count": {"type": "integer"},
                        "execution_count": {"type": "integer"},
                        "preferences": {"type": "object"},
                        "activity_summary": {
                            "properties": {
                                "total_workflows": {"type": "integer"},
                                "total_executions": {"type": "integer"},
                                "success_rate": {"type": "float"},
                                "avg_workflow_complexity": {"type": "float"}
                            }
                        }
                    }
                },
                settings={
                    "number_of_shards": 1,
                    "number_of_replicas": 1
                },
                aliases=["users", "user_profiles"]
            ),
            
            IndexType.AGENTS: IndexConfig(
                name=f"{self.index_prefix}_agents",
                mappings={
                    "properties": {
                        "agent_id": {"type": "keyword"},
                        "name": {"type": "text"},
                        "type": {"type": "keyword"},
                        "status": {"type": "keyword"},
                        "capabilities": {"type": "keyword"},
                        "created_at": {"type": "date"},
                        "last_active": {"type": "date"},
                        "owner": {"type": "keyword"},
                        "configuration": {"type": "object"},
                        "performance_metrics": {
                            "properties": {
                                "tasks_completed": {"type": "long"},
                                "success_rate": {"type": "float"},
                                "avg_response_time": {"type": "float"},
                                "error_count": {"type": "long"},
                                "uptime_percentage": {"type": "float"}
                            }
                        },
                        "beliefs": {"type": "object"},
                        "desires": {"type": "object"},
                        "intentions": {"type": "object"},
                        "knowledge_domains": {"type": "keyword"}
                    }
                },
                settings={
                    "number_of_shards": 2,
                    "number_of_replicas": 1
                },
                aliases=["agents", "bdi_agents"]
            ),
            
            IndexType.LOGS: IndexConfig(
                name=f"{self.index_prefix}_logs",
                mappings={
                    "properties": {
                        "timestamp": {"type": "date"},
                        "level": {"type": "keyword"},
                        "logger": {"type": "keyword"},
                        "message": {"type": "text"},
                        "service": {"type": "keyword"},
                        "component": {"type": "keyword"},
                        "trace_id": {"type": "keyword"},
                        "span_id": {"type": "keyword"},
                        "user_id": {"type": "keyword"},
                        "workflow_id": {"type": "keyword"},
                        "execution_id": {"type": "keyword"},
                        "agent_id": {"type": "keyword"},
                        "error_code": {"type": "keyword"},
                        "stack_trace": {"type": "text"},
                        "context": {"type": "object"},
                        "tags": {"type": "keyword"}
                    }
                },
                settings={
                    "number_of_shards": 5,
                    "number_of_replicas": 1,
                    "index.lifecycle.name": "logs_policy"
                },
                aliases=["logs", "system_logs"]
            ),
            
            IndexType.METRICS: IndexConfig(
                name=f"{self.index_prefix}_metrics",
                mappings={
                    "properties": {
                        "timestamp": {"type": "date"},
                        "metric_name": {"type": "keyword"},
                        "metric_type": {"type": "keyword"},
                        "value": {"type": "double"},
                        "unit": {"type": "keyword"},
                        "service": {"type": "keyword"},
                        "component": {"type": "keyword"},
                        "instance": {"type": "keyword"},
                        "tags": {"type": "keyword"},
                        "dimensions": {"type": "object"},
                        "aggregation_period": {"type": "keyword"}
                    }
                },
                settings={
                    "number_of_shards": 3,
                    "number_of_replicas": 1,
                    "index.lifecycle.name": "metrics_policy"
                },
                aliases=["metrics", "performance_metrics"]
            )
        }
    
    async def _initialize_indices(self) -> None:
        """Initialize all required indices"""
        for index_type, config in self.index_configs.items():
            try:
                # Check if index exists
                if not await self.client.indices.exists(index=config.name):
                    # Create index with mappings and settings
                    await self.client.indices.create(
                        index=config.name,
                        body={
                            "mappings": config.mappings,
                            "settings": config.settings
                        }
                    )
                    logger.info(f"Created index: {config.name}")
                
                # Set up aliases
                if config.aliases:
                    for alias in config.aliases:
                        await self.client.indices.put_alias(
                            index=config.name,
                            name=alias
                        )
                
            except Exception as e:
                logger.error(f"Failed to initialize index {config.name}: {e}")
                raise
    
    async def _setup_lifecycle_policies(self) -> None:
        """Set up index lifecycle management policies"""
        policies = {
            "execution_policy": {
                "policy": {
                    "phases": {
                        "hot": {
                            "actions": {
                                "rollover": {
                                    "max_size": "10GB",
                                    "max_age": "7d"
                                }
                            }
                        },
                        "warm": {
                            "min_age": "7d",
                            "actions": {
                                "allocate": {
                                    "number_of_replicas": 0
                                }
                            }
                        },
                        "cold": {
                            "min_age": "30d",
                            "actions": {
                                "allocate": {
                                    "number_of_replicas": 0
                                }
                            }
                        },
                        "delete": {
                            "min_age": "90d"
                        }
                    }
                }
            },
            "logs_policy": {
                "policy": {
                    "phases": {
                        "hot": {
                            "actions": {
                                "rollover": {
                                    "max_size": "5GB",
                                    "max_age": "1d"
                                }
                            }
                        },
                        "warm": {
                            "min_age": "1d",
                            "actions": {
                                "allocate": {
                                    "number_of_replicas": 0
                                }
                            }
                        },
                        "cold": {
                            "min_age": "7d",
                            "actions": {
                                "allocate": {
                                    "number_of_replicas": 0
                                }
                            }
                        },
                        "delete": {
                            "min_age": "30d"
                        }
                    }
                }
            },
            "metrics_policy": {
                "policy": {
                    "phases": {
                        "hot": {
                            "actions": {
                                "rollover": {
                                    "max_size": "2GB",
                                    "max_age": "1d"
                                }
                            }
                        },
                        "warm": {
                            "min_age": "3d",
                            "actions": {
                                "allocate": {
                                    "number_of_replicas": 0
                                }
                            }
                        },
                        "delete": {
                            "min_age": "14d"
                        }
                    }
                }
            }
        }
        
        for policy_name, policy_config in policies.items():
            try:
                await self.client.ilm.put_lifecycle(
                    policy=policy_name,
                    **policy_config
                )
                logger.info(f"Created lifecycle policy: {policy_name}")
            except Exception as e:
                logger.warning(f"Failed to create lifecycle policy {policy_name}: {e}")
    
    async def index_workflow(self, workflow_data: Dict[str, Any]) -> bool:
        """Index a workflow for search and analytics"""
        try:
            index_name = self.index_configs[IndexType.WORKFLOWS].name
            
            # Enrich workflow data with analytics
            enriched_data = {
                **workflow_data,
                "indexed_at": datetime.utcnow().isoformat(),
                "search_text": f"{workflow_data.get('name', '')} {workflow_data.get('description', '')}",
                "complexity_score": self._calculate_workflow_complexity(workflow_data),
                "estimated_duration": self._estimate_workflow_duration(workflow_data)
            }
            
            await self.client.index(
                index=index_name,
                id=workflow_data.get("workflow_id"),
                document=enriched_data
            )
            
            logger.debug(f"Indexed workflow: {workflow_data.get('workflow_id')}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to index workflow: {e}")
            return False
    
    async def index_execution(self, execution_data: Dict[str, Any]) -> bool:
        """Index a workflow execution for analytics"""
        try:
            index_name = self.index_configs[IndexType.EXECUTIONS].name
            
            # Enrich execution data
            enriched_data = {
                **execution_data,
                "indexed_at": datetime.utcnow().isoformat(),
                "execution_date": execution_data.get("started_at", datetime.utcnow().isoformat())[:10],
                "success": execution_data.get("status") == "completed",
                "efficiency_score": self._calculate_execution_efficiency(execution_data)
            }
            
            await self.client.index(
                index=index_name,
                id=execution_data.get("execution_id"),
                document=enriched_data
            )
            
            logger.debug(f"Indexed execution: {execution_data.get('execution_id')}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to index execution: {e}")
            return False
    
    async def index_user_activity(self, user_data: Dict[str, Any]) -> bool:
        """Index user activity and profile data"""
        try:
            index_name = self.index_configs[IndexType.USERS].name
            
            # Enrich user data with activity metrics
            enriched_data = {
                **user_data,
                "indexed_at": datetime.utcnow().isoformat(),
                "activity_score": self._calculate_user_activity_score(user_data),
                "expertise_level": self._determine_user_expertise(user_data)
            }
            
            await self.client.index(
                index=index_name,
                id=user_data.get("user_id"),
                document=enriched_data
            )
            
            logger.debug(f"Indexed user activity: {user_data.get('user_id')}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to index user activity: {e}")
            return False
    
    async def index_agent_data(self, agent_data: Dict[str, Any]) -> bool:
        """Index BDI agent data and performance metrics"""
        try:
            index_name = self.index_configs[IndexType.AGENTS].name
            
            # Enrich agent data
            enriched_data = {
                **agent_data,
                "indexed_at": datetime.utcnow().isoformat(),
                "intelligence_score": self._calculate_agent_intelligence(agent_data),
                "reliability_score": self._calculate_agent_reliability(agent_data)
            }
            
            await self.client.index(
                index=index_name,
                id=agent_data.get("agent_id"),
                document=enriched_data
            )
            
            logger.debug(f"Indexed agent data: {agent_data.get('agent_id')}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to index agent data: {e}")
            return False
    
    async def index_log_entry(self, log_data: Dict[str, Any]) -> bool:
        """Index a log entry for search and analysis"""
        try:
            index_name = self.index_configs[IndexType.LOGS].name
            
            # Enrich log data
            enriched_data = {
                **log_data,
                "indexed_at": datetime.utcnow().isoformat(),
                "severity_score": self._calculate_log_severity(log_data),
                "is_error": log_data.get("level", "").lower() in ["error", "critical", "fatal"]
            }
            
            await self.client.index(
                index=index_name,
                document=enriched_data
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to index log entry: {e}")
            return False
    
    async def index_metrics(self, metrics_data: Dict[str, Any]) -> bool:
        """Index performance metrics"""
        try:
            index_name = self.index_configs[IndexType.METRICS].name
            
            # Enrich metrics data
            enriched_data = {
                **metrics_data,
                "indexed_at": datetime.utcnow().isoformat(),
                "anomaly_score": self._calculate_anomaly_score(metrics_data)
            }
            
            await self.client.index(
                index=index_name,
                document=enriched_data
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to index metrics: {e}")
            return False
    
    async def search_workflows(self, query: SearchQuery, scope: SearchScope = SearchScope.GLOBAL) -> SearchResult:
        """Search workflows with advanced filtering and faceting"""
        try:
            index_name = self.index_configs[IndexType.WORKFLOWS].name
            
            # Build Elasticsearch query
            es_query = self._build_search_query(query, IndexType.WORKFLOWS, scope)
            
            response = await self.client.search(
                index=index_name,
                body=es_query,
                size=query.size,
                from_=query.from_
            )
            
            return SearchResult(
                total=response["hits"]["total"]["value"],
                hits=response["hits"]["hits"],
                aggregations=response.get("aggregations", {}),
                took=response["took"],
                timed_out=response["timed_out"]
            )
            
        except Exception as e:
            logger.error(f"Failed to search workflows: {e}")
            return SearchResult(total=0, hits=[], took=0, timed_out=False)
    
    async def search_executions(self, query: SearchQuery, scope: SearchScope = SearchScope.GLOBAL) -> SearchResult:
        """Search workflow executions with analytics"""
        try:
            index_name = self.index_configs[IndexType.EXECUTIONS].name
            
            # Build Elasticsearch query with execution-specific aggregations
            es_query = self._build_search_query(query, IndexType.EXECUTIONS, scope)
            
            # Add execution-specific aggregations
            es_query["aggs"] = {
                **es_query.get("aggs", {}),
                "status_distribution": {
                    "terms": {"field": "status"}
                },
                "duration_stats": {
                    "stats": {"field": "duration"}
                },
                "executions_over_time": {
                    "date_histogram": {
                        "field": "started_at",
                        "calendar_interval": "1d"
                    }
                }
            }
            
            response = await self.client.search(
                index=index_name,
                body=es_query,
                size=query.size,
                from_=query.from_
            )
            
            return SearchResult(
                total=response["hits"]["total"]["value"],
                hits=response["hits"]["hits"],
                aggregations=response.get("aggregations", {}),
                took=response["took"],
                timed_out=response["timed_out"]
            )
            
        except Exception as e:
            logger.error(f"Failed to search executions: {e}")
            return SearchResult(total=0, hits=[], took=0, timed_out=False)
    
    async def search_logs(self, query: SearchQuery, time_range: Dict[str, str] = None) -> SearchResult:
        """Search system logs with time-based filtering"""
        try:
            index_name = self.index_configs[IndexType.LOGS].name
            
            # Build query with time range
            es_query = self._build_search_query(query, IndexType.LOGS, SearchScope.SYSTEM)
            
            # Add time range filter if provided
            if time_range:
                time_filter = {
                    "range": {
                        "timestamp": time_range
                    }
                }
                
                if "bool" not in es_query["query"]:
                    es_query["query"] = {"bool": {"must": [es_query["query"]]}}
                
                if "filter" not in es_query["query"]["bool"]:
                    es_query["query"]["bool"]["filter"] = []
                
                es_query["query"]["bool"]["filter"].append(time_filter)
            
            # Add log-specific aggregations
            es_query["aggs"] = {
                "log_levels": {
                    "terms": {"field": "level"}
                },
                "services": {
                    "terms": {"field": "service"}
                },
                "error_trends": {
                    "date_histogram": {
                        "field": "timestamp",
                        "calendar_interval": "1h"
                    },
                    "aggs": {
                        "error_count": {
                            "filter": {"term": {"is_error": True}}
                        }
                    }
                }
            }
            
            response = await self.client.search(
                index=index_name,
                body=es_query,
                size=query.size,
                from_=query.from_
            )
            
            return SearchResult(
                total=response["hits"]["total"]["value"],
                hits=response["hits"]["hits"],
                aggregations=response.get("aggregations", {}),
                took=response["took"],
                timed_out=response["timed_out"]
            )
            
        except Exception as e:
            logger.error(f"Failed to search logs: {e}")
            return SearchResult(total=0, hits=[], took=0, timed_out=False)
    
    async def get_analytics_dashboard_data(self, time_range: Dict[str, str] = None) -> Dict[str, Any]:
        """Get comprehensive analytics data for dashboard"""
        try:
            # Default to last 24 hours if no time range provided
            if not time_range:
                time_range = {
                    "gte": (datetime.utcnow() - timedelta(days=1)).isoformat(),
                    "lte": datetime.utcnow().isoformat()
                }
            
            # Parallel queries for different analytics
            tasks = [
                self._get_workflow_analytics(time_range),
                self._get_execution_analytics(time_range),
                self._get_user_analytics(time_range),
                self._get_agent_analytics(time_range),
                self._get_system_health_analytics(time_range)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            return {
                "workflow_analytics": results[0] if not isinstance(results[0], Exception) else {},
                "execution_analytics": results[1] if not isinstance(results[1], Exception) else {},
                "user_analytics": results[2] if not isinstance(results[2], Exception) else {},
                "agent_analytics": results[3] if not isinstance(results[3], Exception) else {},
                "system_health": results[4] if not isinstance(results[4], Exception) else {},
                "generated_at": datetime.utcnow().isoformat(),
                "time_range": time_range
            }
            
        except Exception as e:
            logger.error(f"Failed to get analytics dashboard data: {e}")
            return {}
    
    def _build_search_query(self, query: SearchQuery, index_type: IndexType, scope: SearchScope) -> Dict[str, Any]:
        """Build Elasticsearch query from search parameters"""
        es_query = {
            "query": {
                "bool": {
                    "must": [],
                    "filter": [],
                    "should": [],
                    "must_not": []
                }
            }
        }
        
        # Add main search query
        if query.query:
            if index_type == IndexType.WORKFLOWS:
                es_query["query"]["bool"]["must"].append({
                    "multi_match": {
                        "query": query.query,
                        "fields": ["name^3", "description^2", "tags", "category"],
                        "type": "best_fields",
                        "fuzziness": "AUTO"
                    }
                })
            elif index_type == IndexType.LOGS:
                es_query["query"]["bool"]["must"].append({
                    "multi_match": {
                        "query": query.query,
                        "fields": ["message^2", "logger", "service", "component"],
                        "type": "phrase_prefix"
                    }
                })
            else:
                es_query["query"]["bool"]["must"].append({
                    "query_string": {
                        "query": query.query,
                        "default_operator": "AND"
                    }
                })
        else:
            es_query["query"]["bool"]["must"].append({"match_all": {}})
        
        # Add filters
        if query.filters:
            for field, value in query.filters.items():
                if isinstance(value, list):
                    es_query["query"]["bool"]["filter"].append({
                        "terms": {field: value}
                    })
                elif isinstance(value, dict) and "range" in value:
                    es_query["query"]["bool"]["filter"].append({
                        "range": {field: value["range"]}
                    })
                else:
                    es_query["query"]["bool"]["filter"].append({
                        "term": {field: value}
                    })
        
        # Add sorting
        if query.sort:
            es_query["sort"] = query.sort
        else:
            # Default sorting based on index type
            if index_type == IndexType.EXECUTIONS:
                es_query["sort"] = [{"started_at": {"order": "desc"}}]
            elif index_type == IndexType.LOGS:
                es_query["sort"] = [{"timestamp": {"order": "desc"}}]
            else:
                es_query["sort"] = [{"_score": {"order": "desc"}}]
        
        # Add highlighting
        if query.highlight:
            es_query["highlight"] = query.highlight
        
        # Add aggregations
        if query.aggregations:
            es_query["aggs"] = query.aggregations
        
        return es_query
    
    def _calculate_workflow_complexity(self, workflow_data: Dict[str, Any]) -> float:
        """Calculate workflow complexity score"""
        # Simple complexity calculation based on various factors
        base_score = 1.0
        
        # Factor in number of steps
        steps = workflow_data.get("definition", {}).get("steps", [])
        step_complexity = len(steps) * 0.1
        
        # Factor in conditional logic
        conditions = sum(1 for step in steps if step.get("type") == "condition")
        condition_complexity = conditions * 0.3
        
        # Factor in integrations
        integrations = sum(1 for step in steps if step.get("type") == "integration")
        integration_complexity = integrations * 0.2
        
        return min(base_score + step_complexity + condition_complexity + integration_complexity, 10.0)
    
    def _estimate_workflow_duration(self, workflow_data: Dict[str, Any]) -> float:
        """Estimate workflow execution duration in seconds"""
        # Simple duration estimation
        steps = workflow_data.get("definition", {}).get("steps", [])
        base_duration = len(steps) * 5  # 5 seconds per step base
        
        # Add complexity factors
        complexity = self._calculate_workflow_complexity(workflow_data)
        complexity_factor = complexity * 10
        
        return base_duration + complexity_factor
    
    def _calculate_execution_efficiency(self, execution_data: Dict[str, Any]) -> float:
        """Calculate execution efficiency score"""
        duration = execution_data.get("duration", 0)
        step_count = execution_data.get("step_count", 1)
        completed_steps = execution_data.get("completed_steps", 0)
        
        if step_count == 0:
            return 0.0
        
        completion_rate = completed_steps / step_count
        time_efficiency = max(0, 1 - (duration / (step_count * 10)))  # Assume 10s per step is baseline
        
        return (completion_rate * 0.7 + time_efficiency * 0.3) * 100
    
    def _calculate_user_activity_score(self, user_data: Dict[str, Any]) -> float:
        """Calculate user activity score"""
        workflow_count = user_data.get("workflow_count", 0)
        execution_count = user_data.get("execution_count", 0)
        success_rate = user_data.get("activity_summary", {}).get("success_rate", 0)
        
        activity_score = (workflow_count * 2 + execution_count * 0.1) * success_rate
        return min(activity_score, 100.0)
    
    def _determine_user_expertise(self, user_data: Dict[str, Any]) -> str:
        """Determine user expertise level"""
        activity_score = self._calculate_user_activity_score(user_data)
        
        if activity_score >= 80:
            return "expert"
        elif activity_score >= 50:
            return "advanced"
        elif activity_score >= 20:
            return "intermediate"
        else:
            return "beginner"
    
    def _calculate_agent_intelligence(self, agent_data: Dict[str, Any]) -> float:
        """Calculate agent intelligence score"""
        metrics = agent_data.get("performance_metrics", {})
        success_rate = metrics.get("success_rate", 0)
        response_time = metrics.get("avg_response_time", float('inf'))
        
        # Intelligence based on success rate and response efficiency
        time_score = max(0, 1 - (response_time / 10))  # 10s baseline
        intelligence = (success_rate * 0.8 + time_score * 0.2) * 100
        
        return min(intelligence, 100.0)
    
    def _calculate_agent_reliability(self, agent_data: Dict[str, Any]) -> float:
        """Calculate agent reliability score"""
        metrics = agent_data.get("performance_metrics", {})
        uptime = metrics.get("uptime_percentage", 0)
        error_rate = 1 - (metrics.get("error_count", 0) / max(metrics.get("tasks_completed", 1), 1))
        
        reliability = (uptime * 0.6 + error_rate * 0.4) * 100
        return min(reliability, 100.0)
    
    def _calculate_log_severity(self, log_data: Dict[str, Any]) -> int:
        """Calculate log severity score"""
        level = log_data.get("level", "info").lower()
        severity_map = {
            "debug": 1,
            "info": 2,
            "warning": 3,
            "warn": 3,
            "error": 4,
            "critical": 5,
            "fatal": 5
        }
        return severity_map.get(level, 2)
    
    def _calculate_anomaly_score(self, metrics_data: Dict[str, Any]) -> float:
        """Calculate anomaly score for metrics"""
        # Simple anomaly detection based on value ranges
        value = metrics_data.get("value", 0)
        metric_type = metrics_data.get("metric_type", "")
        
        # This would typically use historical data for proper anomaly detection
        # For now, return a simple score based on value magnitude
        if metric_type in ["cpu_usage", "memory_usage"]:
            if value > 90:
                return 0.9
            elif value > 70:
                return 0.5
            else:
                return 0.1
        
        return 0.0
    
    async def _get_workflow_analytics(self, time_range: Dict[str, str]) -> Dict[str, Any]:
        """Get workflow analytics data"""
        index_name = self.index_configs[IndexType.WORKFLOWS].name
        
        query = {
            "size": 0,
            "query": {
                "range": {
                    "created_at": time_range
                }
            },
            "aggs": {
                "total_workflows": {
                    "value_count": {"field": "workflow_id"}
                },
                "avg_complexity": {
                    "avg": {"field": "complexity_score"}
                },
                "categories": {
                    "terms": {"field": "category"}
                },
                "status_distribution": {
                    "terms": {"field": "status"}
                }
            }
        }
        
        response = await self.client.search(index=index_name, body=query)
        return response.get("aggregations", {})
    
    async def _get_execution_analytics(self, time_range: Dict[str, str]) -> Dict[str, Any]:
        """Get execution analytics data"""
        index_name = self.index_configs[IndexType.EXECUTIONS].name
        
        query = {
            "size": 0,
            "query": {
                "range": {
                    "started_at": time_range
                }
            },
            "aggs": {
                "total_executions": {
                    "value_count": {"field": "execution_id"}
                },
                "success_rate": {
                    "filter": {"term": {"success": True}},
                    "aggs": {
                        "percentage": {
                            "bucket_script": {
                                "buckets_path": {
                                    "success": "_count",
                                    "total": "_parent>_count"
                                },
                                "script": "params.success / params.total * 100"
                            }
                        }
                    }
                },
                "avg_duration": {
                    "avg": {"field": "duration"}
                },
                "executions_over_time": {
                    "date_histogram": {
                        "field": "started_at",
                        "calendar_interval": "1h"
                    }
                }
            }
        }
        
        response = await self.client.search(index=index_name, body=query)
        return response.get("aggregations", {})
    
    async def _get_user_analytics(self, time_range: Dict[str, str]) -> Dict[str, Any]:
        """Get user analytics data"""
        index_name = self.index_configs[IndexType.USERS].name
        
        query = {
            "size": 0,
            "query": {"match_all": {}},
            "aggs": {
                "total_users": {
                    "value_count": {"field": "user_id"}
                },
                "active_users": {
                    "filter": {
                        "range": {
                            "last_login": time_range
                        }
                    }
                },
                "expertise_levels": {
                    "terms": {"field": "expertise_level"}
                },
                "departments": {
                    "terms": {"field": "department"}
                }
            }
        }
        
        response = await self.client.search(index=index_name, body=query)
        return response.get("aggregations", {})
    
    async def _get_agent_analytics(self, time_range: Dict[str, str]) -> Dict[str, Any]:
        """Get agent analytics data"""
        index_name = self.index_configs[IndexType.AGENTS].name
        
        query = {
            "size": 0,
            "query": {
                "range": {
                    "last_active": time_range
                }
            },
            "aggs": {
                "total_agents": {
                    "value_count": {"field": "agent_id"}
                },
                "active_agents": {
                    "filter": {"term": {"status": "active"}}
                },
                "avg_intelligence": {
                    "avg": {"field": "intelligence_score"}
                },
                "avg_reliability": {
                    "avg": {"field": "reliability_score"}
                },
                "agent_types": {
                    "terms": {"field": "type"}
                }
            }
        }
        
        response = await self.client.search(index=index_name, body=query)
        return response.get("aggregations", {})
    
    async def _get_system_health_analytics(self, time_range: Dict[str, str]) -> Dict[str, Any]:
        """Get system health analytics"""
        logs_index = self.index_configs[IndexType.LOGS].name
        metrics_index = self.index_configs[IndexType.METRICS].name
        
        # Get error rate from logs
        logs_query = {
            "size": 0,
            "query": {
                "range": {
                    "timestamp": time_range
                }
            },
            "aggs": {
                "error_rate": {
                    "filter": {"term": {"is_error": True}},
                    "aggs": {
                        "percentage": {
                            "bucket_script": {
                                "buckets_path": {
                                    "errors": "_count",
                                    "total": "_parent>_count"
                                },
                                "script": "params.errors / params.total * 100"
                            }
                        }
                    }
                },
                "services_health": {
                    "terms": {"field": "service"},
                    "aggs": {
                        "error_count": {
                            "filter": {"term": {"is_error": True}}
                        }
                    }
                }
            }
        }
        
        # Get performance metrics
        metrics_query = {
            "size": 0,
            "query": {
                "bool": {
                    "must": [
                        {"range": {"timestamp": time_range}},
                        {"terms": {"metric_name": ["cpu_usage", "memory_usage", "response_time"]}}
                    ]
                }
            },
            "aggs": {
                "performance_metrics": {
                    "terms": {"field": "metric_name"},
                    "aggs": {
                        "avg_value": {"avg": {"field": "value"}},
                        "max_value": {"max": {"field": "value"}}
                    }
                }
            }
        }
        
        # Execute both queries
        logs_response = await self.client.search(index=logs_index, body=logs_query)
        metrics_response = await self.client.search(index=metrics_index, body=metrics_query)
        
        return {
            "logs_analytics": logs_response.get("aggregations", {}),
            "performance_metrics": metrics_response.get("aggregations", {})
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Check Elasticsearch cluster health"""
        try:
            # Get cluster health
            health = await self.client.cluster.health()
            
            # Get index statistics
            stats = await self.client.indices.stats()
            
            # Calculate total documents and size
            total_docs = sum(
                index_stats.get("total", {}).get("docs", {}).get("count", 0)
                for index_stats in stats.get("indices", {}).values()
            )
            
            total_size = sum(
                index_stats.get("total", {}).get("store", {}).get("size_in_bytes", 0)
                for index_stats in stats.get("indices", {}).values()
            )
            
            return {
                "cluster_status": health.get("status"),
                "number_of_nodes": health.get("number_of_nodes"),
                "active_shards": health.get("active_shards"),
                "total_documents": total_docs,
                "total_size_bytes": total_size,
                "indices_count": len(stats.get("indices", {})),
                "available": True
            }
            
        except Exception as e:
            logger.error(f"Elasticsearch health check failed: {e}")
            return {
                "available": False,
                "error": str(e)
            }
    
    async def close(self) -> None:
        """Close Elasticsearch connection"""
        if self.client:
            await self.client.close()
            logger.info("Elasticsearch analytics manager closed")

# Utility functions for direct usage
async def initialize_elasticsearch_analytics():
    """Initialize Elasticsearch analytics manager - can be called directly"""
    config = DatabaseConfig()
    es_manager = ElasticsearchAnalyticsManager(config)
    
    try:
        await es_manager.initialize()
        
        # Test indexing functionality
        test_workflow = {
            "workflow_id": "test_workflow_001",
            "name": "Test Workflow",
            "description": "A test workflow for Elasticsearch integration",
            "status": "active",
            "created_by": "system",
            "created_at": datetime.utcnow().isoformat(),
            "tags": ["test", "elasticsearch", "integration"],
            "category": "testing"
        }
        
        index_result = await es_manager.index_workflow(test_workflow)
        logger.info(f"Test workflow indexing result: {index_result}")
        
        # Test search functionality
        search_query = SearchQuery(
            query="test workflow",
            size=5
        )
        
        search_result = await es_manager.search_workflows(search_query)
        logger.info(f"Test search result: {search_result.total} workflows found")
        
        # Test analytics
        analytics_data = await es_manager.get_analytics_dashboard_data()
        logger.info(f"Analytics data generated with {len(analytics_data)} sections")
        
        return True
        
    except Exception as e:
        logger.error(f"Elasticsearch analytics initialization failed: {e}")
        return False
    finally:
        await es_manager.close()

if __name__ == "__main__":
    # Run Elasticsearch analytics initialization
    asyncio.run(initialize_elasticsearch_analytics()) 