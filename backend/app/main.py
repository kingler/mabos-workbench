"""
MABOS Backend - Main FastAPI Application

Multi-Agent Business Operating System backend service.
Implements BDI (Belief-Desire-Intention) architecture for intelligent workflow automation.
"""

from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app import __version__
from app.core.database import get_database_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title="MABOS Backend API",
    description="Multi-Agent Business Operating System - Backend API for intelligent workflow automation",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configure CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=Dict[str, Any])
async def health_check() -> Dict[str, Any]:
    """
    Comprehensive health check endpoint for service monitoring.
    
    Returns:
        Dict[str, Any]: Health status information including:
            - status: Overall service health status
            - timestamp: Current ISO timestamp
            - version: Application version
            - services: Individual service health status
            - database_health: Detailed database connectivity status
    """
    try:
        # Get database manager and check all database health
        db_manager = await get_database_manager()
        db_health = await db_manager.health_check()
        
        # Determine overall health status
        all_healthy = all(db_health.values())
        overall_status = "healthy" if all_healthy else "degraded"
        
        health_data = {
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat(),
            "version": __version__,
            "service": "mabos-backend",
            "environment": "development",
            "services": {
                "api": "operational",
                "database": "operational" if db_health.get("postgres", False) else "unavailable",
                "cache": "operational" if db_health.get("redis", False) else "unavailable",
                "knowledge_graph": "operational" if db_health.get("neo4j", False) else "unavailable",
                "search": "operational" if db_health.get("elasticsearch", False) else "unavailable"
            },
            "database_health": db_health
        }
        
        logger.info(f"Health check completed - Status: {overall_status}")
        return health_data
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": __version__,
            "service": "mabos-backend",
            "error": str(e),
            "services": {
                "api": "operational",
                "database": "unknown",
                "cache": "unknown",
                "knowledge_graph": "unknown",
                "search": "unknown"
            }
        }


@app.get("/", response_model=Dict[str, str])
async def root() -> Dict[str, str]:
    """
    Root endpoint providing basic API information.
    
    Returns:
        Dict[str, str]: Basic API information
    """
    return {
        "message": "MABOS Backend API",
        "version": __version__,
        "docs": "/docs"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler for unhandled errors.
    
    Args:
        request: The incoming request
        exc: The unhandled exception
        
    Returns:
        JSONResponse: Error response with status 500
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# ===== BDI AGENT KNOWLEDGE GRAPH ENDPOINTS =====

@app.get("/api/agents/{agent_id}/context", response_model=Dict[str, Any])
async def get_agent_context(agent_id: str) -> Dict[str, Any]:
    """
    Get comprehensive context for a BDI agent including knowledge graph and cached state.
    
    Args:
        agent_id: Unique identifier for the BDI agent
        
    Returns:
        Dict[str, Any]: Agent context including beliefs, desires, intentions, and cached state
    """
    try:
        db_manager = await get_database_manager()
        context = await db_manager.get_agent_context(agent_id)
        
        logger.info(f"Retrieved context for agent {agent_id}")
        return context
        
    except Exception as e:
        logger.error(f"Failed to get agent context for {agent_id}: {e}")
        return {
            "agent_id": agent_id,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


@app.post("/api/agents/{agent_id}/beliefs", response_model=Dict[str, Any])
async def create_agent_belief(agent_id: str, belief_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new belief for a BDI agent in the knowledge graph.
    
    Args:
        agent_id: Unique identifier for the BDI agent
        belief_data: Belief information including category, content, confidence, etc.
        
    Returns:
        Dict[str, Any]: Created belief information
    """
    try:
        db_manager = await get_database_manager()
        belief = await db_manager.neo4j.create_agent_belief(agent_id, belief_data)
        
        if belief:
            logger.info(f"Created belief for agent {agent_id}")
            return {
                "success": True,
                "agent_id": agent_id,
                "belief": belief,
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            return {
                "success": False,
                "agent_id": agent_id,
                "error": "Failed to create belief",
                "timestamp": datetime.utcnow().isoformat()
            }
            
    except Exception as e:
        logger.error(f"Failed to create belief for agent {agent_id}: {e}")
        return {
            "success": False,
            "agent_id": agent_id,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


@app.put("/api/agents/intentions/{intention_id}/progress", response_model=Dict[str, Any])
async def update_intention_progress(intention_id: str, progress_data: Dict[str, float]) -> Dict[str, Any]:
    """
    Update the progress of an agent's intention.
    
    Args:
        intention_id: Unique identifier for the intention
        progress_data: Progress information with 'progress' field (0.0 to 1.0)
        
    Returns:
        Dict[str, Any]: Update result
    """
    try:
        progress = progress_data.get("progress", 0.0)
        
        # Validate progress value
        if not 0.0 <= progress <= 1.0:
            return {
                "success": False,
                "intention_id": intention_id,
                "error": "Progress must be between 0.0 and 1.0",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        db_manager = await get_database_manager()
        success = await db_manager.neo4j.update_agent_intention_progress(intention_id, progress)
        
        if success:
            logger.info(f"Updated intention {intention_id} progress to {progress}")
            return {
                "success": True,
                "intention_id": intention_id,
                "progress": progress,
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            return {
                "success": False,
                "intention_id": intention_id,
                "error": "Intention not found",
                "timestamp": datetime.utcnow().isoformat()
            }
            
    except Exception as e:
        logger.error(f"Failed to update intention progress for {intention_id}: {e}")
        return {
            "success": False,
            "intention_id": intention_id,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


@app.post("/api/workflows/sync", response_model=Dict[str, Any])
async def sync_workflow_to_knowledge_graph(workflow_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Synchronize workflow data across all databases including the knowledge graph.
    
    Args:
        workflow_data: Workflow information to synchronize
        
    Returns:
        Dict[str, Any]: Synchronization result
    """
    try:
        db_manager = await get_database_manager()
        success = await db_manager.sync_workflow_to_knowledge_graph(workflow_data)
        
        workflow_id = workflow_data.get("id", "unknown")
        
        if success:
            logger.info(f"Successfully synchronized workflow {workflow_id}")
            return {
                "success": True,
                "workflow_id": workflow_id,
                "message": "Workflow synchronized across all databases",
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            return {
                "success": False,
                "workflow_id": workflow_id,
                "error": "Partial synchronization failure",
                "timestamp": datetime.utcnow().isoformat()
            }
            
    except Exception as e:
        logger.error(f"Failed to sync workflow: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


# Application startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("MABOS Backend starting up...")
    logger.info(f"Version: {__version__}")
    
    # Initialize database manager
    try:
        db_manager = await get_database_manager()
        logger.info("Database manager initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database manager: {e}")


# Application shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    logger.info("MABOS Backend shutting down...")


if __name__ == "__main__":
    import uvicorn
    
    # Run the application with uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 