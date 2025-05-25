#!/usr/bin/env python3
"""
Simple test script to verify MABOS database connections
"""

import asyncio
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, '/Users/kinglerbercy/Projects/mabos-workbench/backend')

from app.core.database import DatabaseManager, DatabaseConfig

async def test_database_connections():
    """Test all database connections"""
    print("🔍 Testing MABOS Database Connections...")
    print("=" * 50)
    
    # Initialize database manager
    config = DatabaseConfig()
    db_manager = DatabaseManager(config)
    
    try:
        # Initialize all connections
        print("📡 Initializing database connections...")
        await db_manager.initialize()
        print("✅ Database manager initialized successfully")
        
        # Test health checks
        print("\n🏥 Running health checks...")
        health_status = await db_manager.health_check()
        
        for db_name, is_healthy in health_status.items():
            status_icon = "✅" if is_healthy else "❌"
            print(f"{status_icon} {db_name.upper()}: {'Connected' if is_healthy else 'Failed'}")
        
        # Test Neo4j knowledge graph
        if health_status.get('neo4j', False):
            print("\n🧠 Testing Neo4j knowledge graph...")
            try:
                result = await db_manager.neo4j.execute_query("RETURN 'Hello MABOS!' as message")
                print(f"✅ Neo4j query result: {result}")
            except Exception as e:
                print(f"❌ Neo4j query failed: {e}")
        
        # Test Redis cache
        if health_status.get('redis', False):
            print("\n💾 Testing Redis cache...")
            try:
                await db_manager.redis.set_cache("test_key", "Hello MABOS!", ttl=60)
                value = await db_manager.redis.get_cache("test_key")
                print(f"✅ Redis cache test: {value}")
            except Exception as e:
                print(f"❌ Redis cache test failed: {e}")
        
        # Test agent context retrieval
        print("\n🤖 Testing agent context retrieval...")
        try:
            context = await db_manager.get_agent_context("agent_orchestrator_001")
            print(f"✅ Agent context retrieved: {context.get('agent_id', 'Unknown')}")
        except Exception as e:
            print(f"❌ Agent context retrieval failed: {e}")
        
        print("\n" + "=" * 50)
        print("🎉 Database connection tests completed!")
        
        # Overall status
        all_healthy = all(health_status.values())
        if all_healthy:
            print("✅ All databases are connected and operational!")
        else:
            failed_dbs = [db for db, healthy in health_status.items() if not healthy]
            print(f"⚠️  Some databases failed: {', '.join(failed_dbs)}")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up connections
        try:
            await db_manager.close()
            print("🔌 Database connections closed")
        except Exception as e:
            print(f"⚠️  Error closing connections: {e}")

if __name__ == "__main__":
    asyncio.run(test_database_connections()) 