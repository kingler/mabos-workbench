"""
MABOS Database Migration System

Handles database schema creation, updates, and version management.
"""

import asyncio
import logging
import re
from pathlib import Path
from typing import List, Dict, Any
import asyncpg
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from app.core.database import DatabaseConfig

# Configure logging
logger = logging.getLogger(__name__)

class DatabaseMigration:
    """Database migration management system"""
    
    def __init__(self, config: DatabaseConfig):
        """Initialize migration system with database configuration"""
        self.config = config
        self.migrations_dir = Path(__file__).parent
        
    def split_sql_statements(self, sql_content: str) -> List[str]:
        """Split SQL content into individual statements"""
        # Remove single-line comments but preserve structure
        lines = []
        for line in sql_content.split('\n'):
            # Remove inline comments but keep the line structure
            if '--' in line:
                line = line.split('--')[0].rstrip()
            if line.strip():
                lines.append(line)
        
        # Join lines with spaces
        content = '\n'.join(lines)
        
        # Split by semicolon but be careful with function definitions and DO blocks
        statements = []
        current_statement = ""
        in_function = False
        in_do_block = False
        paren_count = 0
        
        i = 0
        while i < len(content):
            char = content[i]
            current_statement += char
            
            # Track parentheses for complex statements
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
            
            # Check for function definitions
            if 'CREATE OR REPLACE FUNCTION' in current_statement.upper() or 'CREATE FUNCTION' in current_statement.upper():
                in_function = True
            
            # Check for DO blocks
            if current_statement.upper().strip().startswith('DO $$'):
                in_do_block = True
            
            # Check for end of function or DO block
            if in_function and '$$ language' in current_statement.lower():
                in_function = False
            elif in_do_block and current_statement.endswith('$$;'):
                in_do_block = False
            
            # Split on semicolon if not in function/DO block and parentheses are balanced
            if char == ';' and not in_function and not in_do_block and paren_count == 0:
                stmt = current_statement.strip()
                if stmt and not stmt.startswith('--'):
                    statements.append(stmt)
                current_statement = ""
            
            i += 1
        
        # Add any remaining statement
        if current_statement.strip():
            statements.append(current_statement.strip())
        
        # Filter out empty statements and comments
        return [stmt for stmt in statements if stmt.strip() and not stmt.strip().startswith('--')]
        
    async def create_migration_table(self, engine: AsyncEngine) -> None:
        """Create migrations tracking table if it doesn't exist"""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            id SERIAL PRIMARY KEY,
            version VARCHAR(50) UNIQUE NOT NULL,
            name VARCHAR(200) NOT NULL,
            applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            checksum VARCHAR(64)
        );
        """
        
        async with engine.begin() as conn:
            await conn.execute(text(create_table_sql))
            logger.info("Migration tracking table created/verified")
    
    async def get_applied_migrations(self, engine: AsyncEngine) -> List[str]:
        """Get list of already applied migrations"""
        query = "SELECT version FROM schema_migrations ORDER BY applied_at"
        
        async with engine.begin() as conn:
            result = await conn.execute(text(query))
            return [row[0] for row in result.fetchall()]
    
    async def apply_migration(self, engine: AsyncEngine, version: str, name: str, sql_content: str) -> None:
        """Apply a single migration by executing statements individually"""
        try:
            # Split SQL into individual statements
            statements = self.split_sql_statements(sql_content)
            
            async with engine.begin() as conn:
                # Execute each statement individually
                for i, statement in enumerate(statements):
                    if statement.strip():
                        try:
                            logger.debug(f"Executing statement {i+1}/{len(statements)}: {statement[:100]}...")
                            await conn.execute(text(statement))
                        except Exception as e:
                            logger.error(f"Failed to execute statement {i+1}: {statement[:200]}...")
                            logger.error(f"Error: {e}")
                            raise
                
                # Record the migration as applied
                insert_sql = """
                INSERT INTO schema_migrations (version, name, checksum) 
                VALUES (:version, :name, :checksum)
                """
                
                import hashlib
                checksum = hashlib.sha256(sql_content.encode()).hexdigest()
                
                await conn.execute(text(insert_sql), {
                    'version': version,
                    'name': name,
                    'checksum': checksum
                })
                
                logger.info(f"Applied migration {version}: {name} ({len(statements)} statements)")
                
        except Exception as e:
            logger.error(f"Failed to apply migration {version}: {e}")
            raise
    
    async def run_initial_schema(self, engine: AsyncEngine) -> None:
        """Run the initial database schema creation"""
        schema_file = self.migrations_dir / "database_schema.sql"
        
        if not schema_file.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_file}")
        
        # Read the schema file
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        
        # Check if this migration has already been applied
        applied_migrations = await self.get_applied_migrations(engine)
        
        if "001_initial_schema" not in applied_migrations:
            logger.info("Applying initial database schema...")
            await self.apply_migration(
                engine, 
                "001_initial_schema", 
                "Initial MABOS database schema",
                schema_sql
            )
        else:
            logger.info("Initial schema already applied, skipping")
    
    async def create_sample_data(self, engine: AsyncEngine) -> None:
        """Create sample data for development and testing"""
        sample_data_sql = """
        -- Insert sample data for development
        DO $$
        DECLARE
            org_id UUID;
            admin_role_id UUID;
            user_role_id UUID;
            admin_user_id UUID;
        BEGIN
            -- Get the default organization ID
            SELECT id INTO org_id FROM organizations WHERE slug = 'mabos-default';
            
            -- Get role IDs
            SELECT id INTO admin_role_id FROM roles WHERE name = 'admin';
            SELECT id INTO user_role_id FROM roles WHERE name = 'workflow_user';
            
            -- Create admin user if not exists
            INSERT INTO users (
                email, username, password_hash, first_name, last_name, 
                display_name, is_active, is_verified, is_superuser
            ) VALUES (
                'admin@mabos.dev', 'admin', 
                '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3bp.Gm.F5e', -- password: admin123
                'MABOS', 'Administrator', 'MABOS Admin',
                true, true, true
            ) ON CONFLICT (email) DO NOTHING
            RETURNING id INTO admin_user_id;
            
            -- If user already exists, get the ID
            IF admin_user_id IS NULL THEN
                SELECT id INTO admin_user_id FROM users WHERE email = 'admin@mabos.dev';
            END IF;
            
            -- Assign admin role to admin user
            INSERT INTO user_roles (user_id, role_id, assigned_by)
            VALUES (admin_user_id, admin_role_id, admin_user_id)
            ON CONFLICT (user_id, role_id) DO NOTHING;
            
            -- Add user to default organization
            INSERT INTO organization_members (organization_id, user_id, role, invited_by)
            VALUES (org_id, admin_user_id, 'admin', admin_user_id)
            ON CONFLICT (organization_id, user_id) DO NOTHING;
            
            -- Create sample workflow orchestrator agent
            INSERT INTO agents (
                organization_id, name, type, description, configuration, 
                capabilities, status, created_by
            ) VALUES (
                org_id, 'Main Orchestrator', 'orchestrator',
                'Primary workflow orchestration agent for MABOS platform',
                '{"max_concurrent_workflows": 10, "priority_levels": 5}',
                '["workflow_execution", "task_scheduling", "resource_management"]',
                'active', admin_user_id
            ) ON CONFLICT DO NOTHING;
            
            -- Create sample integration agent
            INSERT INTO agents (
                organization_id, name, type, description, configuration,
                capabilities, status, created_by
            ) VALUES (
                org_id, 'Integration Manager', 'integration',
                'Manages external system integrations and data synchronization',
                '{"supported_systems": ["salesforce", "sap", "servicenow"], "sync_interval": 300}',
                '["data_sync", "api_integration", "error_handling"]',
                'active', admin_user_id
            ) ON CONFLICT DO NOTHING;
            
            RAISE NOTICE 'Sample data created successfully';
        END $$;
        """
        
        applied_migrations = await self.get_applied_migrations(engine)
        
        if "002_sample_data" not in applied_migrations:
            logger.info("Creating sample data...")
            await self.apply_migration(
                engine,
                "002_sample_data",
                "Sample data for development",
                sample_data_sql
            )
        else:
            logger.info("Sample data already created, skipping")

class DatabaseManager:
    """High-level database management operations"""
    
    def __init__(self, config: DatabaseConfig):
        """Initialize database manager"""
        self.config = config
        self.migration = DatabaseMigration(config)
    
    async def initialize_database(self, engine: AsyncEngine) -> None:
        """Initialize database with schema and sample data"""
        try:
            logger.info("Starting database initialization...")
            
            # Create migration tracking table
            await self.migration.create_migration_table(engine)
            
            # Apply initial schema
            await self.migration.run_initial_schema(engine)
            
            # Create sample data for development
            await self.migration.create_sample_data(engine)
            
            logger.info("Database initialization completed successfully")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    async def get_database_info(self, engine: AsyncEngine) -> Dict[str, Any]:
        """Get database information and statistics"""
        info_queries = {
            "version": "SELECT version()",
            "current_database": "SELECT current_database()",
            "current_user": "SELECT current_user",
            "table_count": """
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """,
            "migrations_applied": "SELECT COUNT(*) FROM schema_migrations",
            "users_count": "SELECT COUNT(*) FROM users",
            "workflows_count": "SELECT COUNT(*) FROM workflows",
            "agents_count": "SELECT COUNT(*) FROM agents"
        }
        
        result = {}
        
        async with engine.begin() as conn:
            for key, query in info_queries.items():
                try:
                    db_result = await conn.execute(text(query))
                    result[key] = db_result.scalar()
                except Exception as e:
                    result[key] = f"Error: {e}"
        
        return result
    
    async def verify_schema_integrity(self, engine: AsyncEngine) -> Dict[str, bool]:
        """Verify database schema integrity"""
        checks = {}
        
        # Check if all required tables exist
        required_tables = [
            'users', 'user_sessions', 'roles', 'user_roles', 'organizations',
            'organization_members', 'workflows', 'workflow_versions', 
            'workflow_executions', 'task_executions', 'agents', 'agent_beliefs',
            'agent_desires', 'agent_intentions', 'agent_messages', 'integrations',
            'integration_sync_logs', 'audit_logs', 'system_events', 'performance_metrics'
        ]
        
        async with engine.begin() as conn:
            for table in required_tables:
                query = """
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = :table_name
                    )
                """
                result = await conn.execute(text(query), {'table_name': table})
                checks[f"table_{table}"] = result.scalar()
            
            # Check if required extensions are installed
            extensions_query = """
                SELECT extname FROM pg_extension 
                WHERE extname IN ('uuid-ossp', 'pgcrypto', 'pg_trgm')
            """
            result = await conn.execute(text(extensions_query))
            installed_extensions = [row[0] for row in result.fetchall()]
            
            checks["extension_uuid_ossp"] = "uuid-ossp" in installed_extensions
            checks["extension_pgcrypto"] = "pgcrypto" in installed_extensions
            checks["extension_pg_trgm"] = "pg_trgm" in installed_extensions
        
        return checks

# Utility functions for direct usage
async def initialize_mabos_database():
    """Initialize MABOS database - can be called directly"""
    from app.core.database import DatabaseManager as CoreDatabaseManager, DatabaseConfig
    
    config = DatabaseConfig()
    core_db_manager = CoreDatabaseManager(config)
    db_manager = DatabaseManager(config)
    
    try:
        # Initialize core database manager
        await core_db_manager.initialize()
        
        # Initialize database schema
        await db_manager.initialize_database(core_db_manager.postgres.engine)
        
        # Get database info
        info = await db_manager.get_database_info(core_db_manager.postgres.engine)
        logger.info(f"Database info: {info}")
        
        # Verify schema integrity
        integrity = await db_manager.verify_schema_integrity(core_db_manager.postgres.engine)
        logger.info(f"Schema integrity: {integrity}")
        
        return True
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False
    finally:
        await core_db_manager.close()

if __name__ == "__main__":
    # Run database initialization
    asyncio.run(initialize_mabos_database()) 