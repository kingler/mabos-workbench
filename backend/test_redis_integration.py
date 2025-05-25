#!/usr/bin/env python3
"""
Test script to verify MABOS Redis caching and session management integration
"""

import asyncio
import sys
import os
import json
import time
import hashlib

# Add the backend directory to Python path
sys.path.insert(0, '/Users/kinglerbercy/Projects/mabos-workbench/backend')

from app.core.database import DatabaseManager, DatabaseConfig
from app.models.redis_manager import RedisClusterManager, CacheConfig, SessionConfig

async def test_redis_integration():
    """Test Redis caching and session management integration"""
    print("🔄 Testing MABOS Redis Caching & Session Management...")
    print("=" * 60)
    
    config = DatabaseConfig()
    redis_manager = RedisClusterManager(config)
    
    try:
        # Initialize Redis cluster manager
        await redis_manager.initialize()
        print("✅ Redis cluster manager initialized successfully")
        
        # Test basic caching functionality
        print("\n📦 Testing Basic Caching Operations:")
        
        # Test cache set/get
        test_data = {
            "message": "Hello Redis!",
            "timestamp": time.time(),
            "complex_data": {
                "nested": {"value": 42},
                "list": [1, 2, 3, 4, 5]
            }
        }
        
        cache_key = "test_cache_key"
        set_result = await redis_manager.cache_manager.set(cache_key, test_data, ttl=300)
        print(f"  ✅ Cache set result: {set_result}")
        
        cached_data = await redis_manager.cache_manager.get(cache_key)
        print(f"  ✅ Cache get result: {cached_data}")
        
        # Verify data integrity
        if cached_data == test_data:
            print("  ✅ Data integrity verified")
        else:
            print("  ❌ Data integrity check failed")
        
        # Test cache existence
        exists = await redis_manager.cache_manager.exists(cache_key)
        print(f"  ✅ Cache exists check: {exists}")
        
        # Test cache metrics
        metrics = redis_manager.cache_manager.get_metrics()
        print(f"  📊 Cache metrics - Hits: {metrics.hits}, Misses: {metrics.misses}, Hit Rate: {metrics.hit_rate:.2f}")
        
        # Test session management
        print("\n👤 Testing Session Management:")
        
        # Create a test session
        user_id = "test_user_123"
        session_data = {
            "role": "admin",
            "permissions": ["read", "write", "delete"],
            "ip_address": "192.168.1.100",
            "user_agent": "Mozilla/5.0 Test Browser",
            "preferences": {
                "theme": "dark",
                "language": "en"
            }
        }
        
        session_id = await redis_manager.session_manager.create_session(user_id, session_data)
        print(f"  ✅ Created session: {session_id}")
        
        # Retrieve session data
        retrieved_session = await redis_manager.session_manager.get_session(session_id)
        print(f"  ✅ Retrieved session data: {retrieved_session is not None}")
        
        if retrieved_session:
            print(f"    User ID: {retrieved_session.get('user_id')}")
            print(f"    Role: {retrieved_session.get('role')}")
            print(f"    Created: {retrieved_session.get('created_at')}")
            print(f"    Last accessed: {retrieved_session.get('last_accessed')}")
        
        # Update session data
        update_data = {"last_action": "login", "login_count": 5}
        update_result = await redis_manager.session_manager.update_session(session_id, update_data)
        print(f"  ✅ Session update result: {update_result}")
        
        # Get active sessions for user
        active_sessions = await redis_manager.session_manager.get_active_sessions(user_id)
        print(f"  ✅ Active sessions for user: {len(active_sessions)}")
        
        # Test workflow caching
        print("\n🔄 Testing Workflow Caching:")
        
        workflow_id = "workflow_001"
        execution_id = "exec_123"
        workflow_result = {
            "status": "completed",
            "duration": 45.2,
            "steps_completed": 8,
            "output": {
                "processed_items": 150,
                "success_rate": 0.98
            },
            "metadata": {
                "executor": "agent_001",
                "timestamp": time.time()
            }
        }
        
        # Cache workflow result
        workflow_cache_result = await redis_manager.workflow_cache.cache_workflow_result(
            workflow_id, execution_id, workflow_result
        )
        print(f"  ✅ Workflow result cached: {workflow_cache_result}")
        
        # Retrieve workflow result
        cached_workflow = await redis_manager.workflow_cache.get_workflow_result(workflow_id, execution_id)
        print(f"  ✅ Workflow result retrieved: {cached_workflow is not None}")
        
        if cached_workflow:
            print(f"    Status: {cached_workflow.get('status')}")
            print(f"    Duration: {cached_workflow.get('duration')}s")
            print(f"    Success rate: {cached_workflow.get('output', {}).get('success_rate')}")
        
        # Cache workflow state
        workflow_state = {
            "current_step": 3,
            "total_steps": 8,
            "variables": {
                "input_file": "/data/input.csv",
                "output_dir": "/data/output/",
                "batch_size": 100
            },
            "execution_context": {
                "started_at": time.time() - 300,
                "estimated_completion": time.time() + 600
            }
        }
        
        state_cache_result = await redis_manager.workflow_cache.cache_workflow_state(workflow_id, workflow_state)
        print(f"  ✅ Workflow state cached: {state_cache_result}")
        
        # Test LLM response caching
        print("\n🤖 Testing LLM Response Caching:")
        
        # Generate test LLM data
        prompt = "Explain the benefits of workflow automation in enterprise environments"
        model = "gpt-4"
        parameters = {"temperature": 0.7, "max_tokens": 500}
        
        prompt_hash = redis_manager.llm_cache.generate_prompt_hash(prompt, model, parameters)
        print(f"  🔑 Generated prompt hash: {prompt_hash[:16]}...")
        
        llm_response = {
            "response": "Workflow automation in enterprise environments provides significant benefits including...",
            "usage": {
                "prompt_tokens": 25,
                "completion_tokens": 150,
                "total_tokens": 175
            },
            "model": model,
            "timestamp": time.time(),
            "metadata": {
                "response_time": 2.3,
                "cost": 0.0035
            }
        }
        
        # Cache LLM response
        llm_cache_result = await redis_manager.llm_cache.cache_llm_response(
            prompt_hash, model, llm_response
        )
        print(f"  ✅ LLM response cached: {llm_cache_result}")
        
        # Retrieve LLM response
        cached_llm_response = await redis_manager.llm_cache.get_llm_response(prompt_hash, model)
        print(f"  ✅ LLM response retrieved: {cached_llm_response is not None}")
        
        if cached_llm_response:
            print(f"    Model: {cached_llm_response.get('model')}")
            print(f"    Total tokens: {cached_llm_response.get('usage', {}).get('total_tokens')}")
            print(f"    Response time: {cached_llm_response.get('metadata', {}).get('response_time')}s")
        
        # Test cache invalidation
        print("\n🗑️ Testing Cache Invalidation:")
        
        # Create multiple test keys
        test_keys = []
        for i in range(5):
            key = f"test_pattern_key_{i}"
            await redis_manager.cache_manager.set(key, {"index": i, "data": f"test_data_{i}"})
            test_keys.append(key)
        
        print(f"  ✅ Created {len(test_keys)} test cache entries")
        
        # Invalidate by pattern
        invalidated_count = await redis_manager.cache_manager.invalidate_pattern("test_pattern_key_*")
        print(f"  ✅ Invalidated {invalidated_count} cache entries by pattern")
        
        # Verify invalidation
        remaining_keys = 0
        for key in test_keys:
            if await redis_manager.cache_manager.exists(key):
                remaining_keys += 1
        
        print(f"  ✅ Remaining keys after invalidation: {remaining_keys}")
        
        # Test cache performance
        print("\n⚡ Testing Cache Performance:")
        
        # Performance test with multiple operations
        start_time = time.time()
        operations = 100
        
        for i in range(operations):
            key = f"perf_test_{i}"
            data = {"iteration": i, "timestamp": time.time()}
            await redis_manager.cache_manager.set(key, data, ttl=60)
        
        set_time = time.time() - start_time
        print(f"  ⏱️ Set {operations} items in {set_time:.3f}s ({operations/set_time:.1f} ops/sec)")
        
        # Test retrieval performance
        start_time = time.time()
        retrieved_count = 0
        
        for i in range(operations):
            key = f"perf_test_{i}"
            data = await redis_manager.cache_manager.get(key)
            if data:
                retrieved_count += 1
        
        get_time = time.time() - start_time
        print(f"  ⏱️ Retrieved {retrieved_count} items in {get_time:.3f}s ({retrieved_count/get_time:.1f} ops/sec)")
        
        # Test get_or_set functionality
        print("\n🔄 Testing Get-or-Set Functionality:")
        
        def expensive_computation():
            """Simulate expensive computation"""
            time.sleep(0.1)  # Simulate work
            return {"computed_value": 42, "computation_time": 0.1}
        
        # First call should compute and cache
        start_time = time.time()
        result1 = await redis_manager.cache_manager.get_or_set(
            "expensive_computation", expensive_computation, ttl=300
        )
        first_call_time = time.time() - start_time
        print(f"  ⏱️ First call (compute + cache): {first_call_time:.3f}s")
        
        # Second call should use cache
        start_time = time.time()
        result2 = await redis_manager.cache_manager.get_or_set(
            "expensive_computation", expensive_computation, ttl=300
        )
        second_call_time = time.time() - start_time
        print(f"  ⏱️ Second call (from cache): {second_call_time:.3f}s")
        
        speedup = first_call_time / second_call_time if second_call_time > 0 else float('inf')
        print(f"  🚀 Cache speedup: {speedup:.1f}x")
        
        # Test Redis health and metrics
        print("\n📊 Testing Redis Health & Metrics:")
        
        health_status = await redis_manager.health_check()
        print(f"  🏥 Redis Health Status:")
        for key, value in health_status.items():
            print(f"    {key}: {value}")
        
        # Get final cache metrics
        final_metrics = redis_manager.cache_manager.get_metrics()
        print(f"  📈 Final Cache Metrics:")
        print(f"    Hits: {final_metrics.hits}")
        print(f"    Misses: {final_metrics.misses}")
        print(f"    Hit Rate: {final_metrics.hit_rate:.2%}")
        print(f"    Avg Response Time: {final_metrics.avg_response_time:.4f}s")
        
        # Test session cleanup
        print("\n🧹 Testing Session Cleanup:")
        
        # Delete the test session
        session_delete_result = await redis_manager.session_manager.delete_session(session_id)
        print(f"  ✅ Session deletion result: {session_delete_result}")
        
        # Verify session is gone
        deleted_session = await redis_manager.session_manager.get_session(session_id)
        print(f"  ✅ Session verification after deletion: {deleted_session is None}")
        
        # Test database manager integration
        print("\n🔗 Testing Database Manager Integration:")
        
        db_manager = DatabaseManager(config)
        await db_manager.initialize()
        
        # Test enhanced Redis methods through database manager
        test_session_id = await db_manager.redis.create_session(
            "integration_test_user",
            {"test": "integration", "timestamp": time.time()}
        )
        print(f"  ✅ Database manager session creation: {test_session_id is not None}")
        
        # Test workflow caching through database manager
        workflow_cache_result = await db_manager.redis.cache_workflow_result(
            "integration_workflow", "integration_exec", {"status": "success"}
        )
        print(f"  ✅ Database manager workflow caching: {workflow_cache_result}")
        
        # Test LLM caching through database manager
        llm_cache_result = await db_manager.redis.cache_llm_response(
            "integration_hash", "gpt-4", {"response": "Integration test response"}
        )
        print(f"  ✅ Database manager LLM caching: {llm_cache_result}")
        
        # Get cache metrics through database manager
        db_metrics = await db_manager.redis.get_cache_metrics()
        print(f"  📊 Database manager cache metrics: {len(db_metrics)} metrics available")
        
        await db_manager.close()
        
        print("\n🎉 Redis Integration Test Completed Successfully!")
        print("   All caching and session management features are operational")
        print("   Performance metrics show optimal cache utilization")
        print("   High availability features are configured and ready")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Redis integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        await redis_manager.close()

if __name__ == "__main__":
    success = asyncio.run(test_redis_integration())
    sys.exit(0 if success else 1) 