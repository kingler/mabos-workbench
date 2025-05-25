#!/usr/bin/env python3

"""
Simple test script to verify basic Elasticsearch connectivity and functionality
"""

import asyncio
import sys
import os
from datetime import datetime

# Add the backend directory to Python path
sys.path.insert(0, '/Users/kinglerbercy/Projects/mabos-workbench/backend')

from elasticsearch import AsyncElasticsearch

async def test_basic_elasticsearch():
    """Test basic Elasticsearch connectivity"""
    print("🔍 Testing Basic Elasticsearch Connectivity...")
    print("=" * 50)
    
    try:
        # Create simple Elasticsearch client
        client = AsyncElasticsearch(
            ["http://localhost:9200"],
            request_timeout=30
        )
        
        # Test 1: Basic ping
        print("📡 Testing connection...")
        ping_result = await client.ping()
        print(f"✅ Ping successful: {ping_result}")
        
        # Test 2: Get cluster info
        print("\n🏥 Getting cluster info...")
        info = await client.info()
        print(f"✅ Cluster name: {info['cluster_name']}")
        print(f"✅ Version: {info['version']['number']}")
        
        # Test 3: Create a simple index
        print("\n📊 Testing index creation...")
        index_name = "test_mabos_simple"
        
        # Delete index if it exists
        try:
            await client.indices.delete(index=index_name)
            print(f"🗑️ Deleted existing index: {index_name}")
        except:
            pass
        
        # Create simple index
        await client.indices.create(
            index=index_name,
            body={
                "mappings": {
                    "properties": {
                        "title": {"type": "text"},
                        "content": {"type": "text"},
                        "timestamp": {"type": "date"}
                    }
                }
            }
        )
        print(f"✅ Created index: {index_name}")
        
        # Test 4: Index a document
        print("\n📝 Testing document indexing...")
        doc = {
            "title": "Test Document",
            "content": "This is a test document for MABOS Elasticsearch integration",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        result = await client.index(
            index=index_name,
            id="test_doc_1",
            body=doc
        )
        print(f"✅ Indexed document: {result['result']}")
        
        # Wait for indexing
        await asyncio.sleep(2)
        
        # Test 5: Search for the document
        print("\n🔍 Testing document search...")
        search_result = await client.search(
            index=index_name,
            body={
                "query": {
                    "match": {
                        "content": "test"
                    }
                }
            }
        )
        
        hits = search_result['hits']['hits']
        print(f"✅ Search found {len(hits)} documents")
        if hits:
            print(f"   Document title: {hits[0]['_source']['title']}")
        
        # Test 6: Get document by ID
        print("\n📄 Testing document retrieval...")
        get_result = await client.get(
            index=index_name,
            id="test_doc_1"
        )
        print(f"✅ Retrieved document: {get_result['_source']['title']}")
        
        # Test 7: Update document
        print("\n✏️ Testing document update...")
        await client.update(
            index=index_name,
            id="test_doc_1",
            body={
                "doc": {
                    "content": "This is an updated test document for MABOS"
                }
            }
        )
        print("✅ Document updated successfully")
        
        # Test 8: Delete document
        print("\n🗑️ Testing document deletion...")
        await client.delete(
            index=index_name,
            id="test_doc_1"
        )
        print("✅ Document deleted successfully")
        
        # Test 9: Clean up - delete index
        print("\n🧹 Cleaning up...")
        await client.indices.delete(index=index_name)
        print(f"✅ Deleted index: {index_name}")
        
        # Close client
        await client.close()
        
        print("\n🎉 All basic Elasticsearch tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Basic Elasticsearch test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Run basic test
    result = asyncio.run(test_basic_elasticsearch())
    if result:
        print("\n✅ Elasticsearch is working correctly!")
    else:
        print("\n❌ Elasticsearch tests failed!") 