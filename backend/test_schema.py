#!/usr/bin/env python3
"""
Test script to verify MABOS database schema and sample data
"""

import asyncio
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, '/Users/kinglerbercy/Projects/mabos-workbench/backend')

from app.core.database import DatabaseManager, DatabaseConfig
from app.models.migrations import DatabaseManager as MigrationManager

async def test_database():
    """Test database schema and sample data"""
    print("🔍 Testing MABOS Database Schema...")
    print("=" * 50)
    
    config = DatabaseConfig()
    core_db = DatabaseManager(config)
    migration_db = MigrationManager(config)
    
    try:
        # Initialize database connection
        await core_db.initialize()
        
        # Get database info
        print("📊 Database Information:")
        info = await migration_db.get_database_info(core_db.postgres.engine)
        for key, value in info.items():
            print(f"  {key}: {value}")
        
        print("\n🔧 Schema Integrity Check:")
        integrity = await migration_db.verify_schema_integrity(core_db.postgres.engine)
        for key, value in integrity.items():
            status = '✅' if value else '❌'
            print(f"  {status} {key}: {value}")
        
        # Test sample data
        print("\n👥 Sample Data Check:")
        
        # Check users
        users_query = "SELECT email, username, display_name FROM users LIMIT 5"
        async with core_db.postgres.engine.begin() as conn:
            from sqlalchemy import text
            result = await conn.execute(text(users_query))
            users = result.fetchall()
            print(f"  Users found: {len(users)}")
            for user in users:
                print(f"    - {user[2]} ({user[0]})")
        
        # Check organizations
        orgs_query = "SELECT name, slug FROM organizations"
        async with core_db.postgres.engine.begin() as conn:
            result = await conn.execute(text(orgs_query))
            orgs = result.fetchall()
            print(f"  Organizations found: {len(orgs)}")
            for org in orgs:
                print(f"    - {org[0]} ({org[1]})")
        
        # Check agents
        agents_query = "SELECT name, type, status FROM agents"
        async with core_db.postgres.engine.begin() as conn:
            result = await conn.execute(text(agents_query))
            agents = result.fetchall()
            print(f"  Agents found: {len(agents)}")
            for agent in agents:
                print(f"    - {agent[0]} ({agent[1]}) - {agent[2]}")
        
        # Check roles
        roles_query = "SELECT name, display_name FROM roles"
        async with core_db.postgres.engine.begin() as conn:
            result = await conn.execute(text(roles_query))
            roles = result.fetchall()
            print(f"  Roles found: {len(roles)}")
            for role in roles:
                print(f"    - {role[1]} ({role[0]})")
        
        print("\n✅ Database schema and sample data verification completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Database test failed: {e}")
        return False
    finally:
        await core_db.close()

if __name__ == "__main__":
    success = asyncio.run(test_database())
    sys.exit(0 if success else 1) 