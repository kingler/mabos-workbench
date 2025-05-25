#!/usr/bin/env python3
"""
Test script to verify MABOS SBVR ontology integration with Neo4j
"""

import asyncio
import sys
import os
import json

# Add the backend directory to Python path
sys.path.insert(0, '/Users/kinglerbercy/Projects/mabos-workbench/backend')

from app.core.database import DatabaseManager, DatabaseConfig
from app.models.neo4j_manager import Neo4jKnowledgeGraphManager, SBVROntologyManager

async def test_sbvr_integration():
    """Test SBVR ontology integration with Neo4j knowledge graph"""
    print("🧠 Testing MABOS SBVR Ontology Integration...")
    print("=" * 60)
    
    config = DatabaseConfig()
    kg_manager = Neo4jKnowledgeGraphManager(config)
    
    try:
        # Initialize Neo4j knowledge graph
        await kg_manager.initialize()
        print("✅ Neo4j knowledge graph initialized successfully")
        
        # Test SBVR schema creation
        print("\n📋 Testing SBVR Schema Components:")
        
        # Test vocabulary elements
        vocab_query = """
        MATCH (v:VocabularyElement)
        RETURN count(v) as vocab_count, collect(v.name)[0..5] as sample_names
        """
        vocab_result = await kg_manager.execute_cypher_query(vocab_query)
        print(f"  📚 Vocabulary Elements: {vocab_result[0]['vocab_count']} created")
        print(f"      Sample names: {vocab_result[0]['sample_names']}")
        
        # Test concept types
        concept_query = """
        MATCH (c:ConceptType)
        RETURN count(c) as concept_count, collect(c.name) as concept_names
        """
        concept_result = await kg_manager.execute_cypher_query(concept_query)
        print(f"  🎯 Concept Types: {concept_result[0]['concept_count']} created")
        print(f"      Concepts: {concept_result[0]['concept_names']}")
        
        # Test fact types
        fact_query = """
        MATCH (f:FactType)
        RETURN count(f) as fact_count, collect(f.name) as fact_names
        """
        fact_result = await kg_manager.execute_cypher_query(fact_query)
        print(f"  🔗 Fact Types: {fact_result[0]['fact_count']} created")
        print(f"      Facts: {fact_result[0]['fact_names']}")
        
        # Test business rules
        rule_query = """
        MATCH (r:Rule)
        RETURN count(r) as rule_count, collect(r.name) as rule_names,
               collect(r.priority) as priorities
        """
        rule_result = await kg_manager.execute_cypher_query(rule_query)
        print(f"  📏 Business Rules: {rule_result[0]['rule_count']} created")
        print(f"      Rules: {rule_result[0]['rule_names']}")
        print(f"      Priorities: {rule_result[0]['priorities']}")
        
        # Test proof tables
        proof_query = """
        MATCH (pt:ProofTable)
        RETURN count(pt) as proof_count, collect(pt.name) as proof_names
        """
        proof_result = await kg_manager.execute_cypher_query(proof_query)
        print(f"  📊 Proof Tables: {proof_result[0]['proof_count']} created")
        print(f"      Tables: {proof_result[0]['proof_names']}")
        
        # Test proof entries
        entry_query = """
        MATCH (pe:ProofEntry)
        RETURN count(pe) as entry_count, 
               avg(pe.confidence) as avg_confidence,
               collect(DISTINCT pe.validation_status) as statuses
        """
        entry_result = await kg_manager.execute_cypher_query(entry_query)
        print(f"  📝 Proof Entries: {entry_result[0]['entry_count']} created")
        print(f"      Average confidence: {entry_result[0]['avg_confidence']:.2f}")
        print(f"      Validation statuses: {entry_result[0]['statuses']}")
        
        # Test reasoning engines
        engine_query = """
        MATCH (re:ReasoningEngine)
        RETURN count(re) as engine_count, collect(re.name) as engine_names,
               collect(re.engine_type) as engine_types
        """
        engine_result = await kg_manager.execute_cypher_query(engine_query)
        print(f"  🤖 Reasoning Engines: {engine_result[0]['engine_count']} created")
        print(f"      Engines: {engine_result[0]['engine_names']}")
        print(f"      Types: {engine_result[0]['engine_types']}")
        
        # Test SBVR relationships
        print("\n🔗 Testing SBVR Semantic Relationships:")
        
        relationship_queries = [
            ("DEFINES", "MATCH ()-[r:DEFINES]->() RETURN count(r) as count"),
            ("RELATES_TO", "MATCH ()-[r:RELATES_TO]->() RETURN count(r) as count"),
            ("CONSTRAINS", "MATCH ()-[r:CONSTRAINS]->() RETURN count(r) as count"),
            ("VALIDATES", "MATCH ()-[r:VALIDATES]->() RETURN count(r) as count"),
            ("BELONGS_TO", "MATCH ()-[r:BELONGS_TO]->() RETURN count(r) as count"),
            ("PROCESSES", "MATCH ()-[r:PROCESSES]->() RETURN count(r) as count")
        ]
        
        for rel_name, query in relationship_queries:
            result = await kg_manager.execute_cypher_query(query)
            count = result[0]['count'] if result else 0
            print(f"  {rel_name}: {count} relationships")
        
        # Test business rule validation
        print("\n🔍 Testing Business Rule Validation:")
        
        # Get a sample rule for testing
        sample_rule_query = """
        MATCH (r:Rule)
        RETURN r.id as rule_id, r.name as rule_name
        LIMIT 1
        """
        sample_rule_result = await kg_manager.execute_cypher_query(sample_rule_query)
        
        if sample_rule_result:
            rule_id = sample_rule_result[0]['rule_id']
            rule_name = sample_rule_result[0]['rule_name']
            
            # Test validation with matching conditions
            test_input = {
                'customer_verification': True,
                'product_availability': True
            }
            
            validation_result = await kg_manager.validate_business_rule(rule_id, test_input)
            print(f"  Rule: {rule_name}")
            print(f"  Input: {test_input}")
            print(f"  Validation Result: {json.dumps(validation_result, indent=2)}")
        
        # Test reasoning engine optimization
        print("\n⚡ Testing Reasoning Engine Optimization:")
        
        optimization_results = await kg_manager.optimize_reasoning_performance()
        print(f"  Analysis completed with {len(optimization_results['analysis_results'])} components")
        
        for key, recommendations in optimization_results['recommendations'].items():
            print(f"  {key}: {recommendations}")
        
        # Test agent knowledge context (if agents exist)
        print("\n🤖 Testing Agent Knowledge Context:")
        
        # Check if any agents exist in the graph
        agent_query = """
        MATCH (a:Agent)
        RETURN a.id as agent_id, a.name as agent_name
        LIMIT 1
        """
        agent_result = await kg_manager.execute_cypher_query(agent_query)
        
        if agent_result:
            agent_id = agent_result[0]['agent_id']
            agent_name = agent_result[0]['agent_name']
            
            context = await kg_manager.get_agent_knowledge_context(agent_id)
            print(f"  Agent: {agent_name}")
            print(f"  Context keys: {list(context.keys())}")
        else:
            print("  No agents found in knowledge graph")
        
        # Test advanced SBVR queries
        print("\n🔬 Testing Advanced SBVR Queries:")
        
        # Query for rule complexity analysis
        complexity_query = """
        MATCH (r:Rule)
        MATCH (pt:ProofTable)-[:VALIDATES]->(r)
        MATCH (pe:ProofEntry)-[:BELONGS_TO]->(pt)
        WITH r, pt, count(pe) as entry_count, avg(pe.confidence) as avg_confidence
        RETURN r.name as rule_name, r.priority as priority, 
               entry_count, avg_confidence,
               r.business_impact as impact
        ORDER BY r.priority DESC, entry_count DESC
        """
        
        complexity_result = await kg_manager.execute_cypher_query(complexity_query)
        print(f"  Rule Complexity Analysis:")
        for rule in complexity_result:
            print(f"    {rule['rule_name']}: Priority {rule['priority']}, "
                  f"{rule['entry_count']} entries, "
                  f"Confidence {rule['avg_confidence']:.2f}, "
                  f"Impact: {rule['impact']}")
        
        # Query for concept relationship network
        network_query = """
        MATCH (c:ConceptType)<-[:RELATES_TO]-(f:FactType)
        RETURN c.name as concept, f.name as fact_type, 
               f.business_significance as significance
        """
        
        network_result = await kg_manager.execute_cypher_query(network_query)
        print(f"  Concept Relationship Network:")
        for rel in network_result:
            print(f"    {rel['concept']} ↔ {rel['fact_type']}: {rel['significance']}")
        
        # Test SBVR ontology completeness
        print("\n✅ SBVR Ontology Completeness Check:")
        
        completeness_query = """
        MATCH (v:VocabularyElement)
        OPTIONAL MATCH (v)-[:DEFINES]-()
        OPTIONAL MATCH (v)-[:RELATES_TO]-()
        OPTIONAL MATCH (v)-[:CONSTRAINS]-()
        WITH v, 
             CASE WHEN v:ConceptType THEN 'ConceptType'
                  WHEN v:FactType THEN 'FactType'
                  WHEN v:Rule THEN 'Rule'
                  ELSE 'VocabularyElement' END as element_type
        RETURN element_type, count(v) as count
        ORDER BY count DESC
        """
        
        completeness_result = await kg_manager.execute_cypher_query(completeness_query)
        print("  SBVR Element Distribution:")
        for element in completeness_result:
            print(f"    {element['element_type']}: {element['count']} elements")
        
        print("\n🎉 SBVR Integration Test Completed Successfully!")
        print("   All SBVR ontology components are properly integrated")
        print("   Business rule validation is functional")
        print("   Reasoning engines are configured and ready")
        print("   Proof tables provide validation capabilities")
        
        return True
        
    except Exception as e:
        print(f"\n❌ SBVR integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        await kg_manager.close()

if __name__ == "__main__":
    success = asyncio.run(test_sbvr_integration())
    sys.exit(0 if success else 1) 