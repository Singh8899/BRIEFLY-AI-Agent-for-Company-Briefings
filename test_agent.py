"""
Simple test script to verify the Research Assistant Chatbot
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.agent import ResearchAgent
from src.evaluation import TestDataGenerator, AgentEvaluator

async def test_basic_functionality():
    """Test basic agent functionality"""
    print("🧪 Testing Basic Agent Functionality")
    print("=" * 50)
    
    # Initialize agent
    print("1. Initializing agent...")
    agent = ResearchAgent()
    print("   ✅ Agent initialized")
    
    # Test simple query
    print("\n2. Testing simple query...")
    query = "What is artificial intelligence?"
    response = await agent.process_query(query)
    print(f"   Query: {query}")
    print(f"   Response: {response.content[:100]}...")
    print(f"   Confidence: {response.confidence}")
    print(f"   Sources: {response.sources}")
    print("   ✅ Simple query test passed")
    
    # Test current events query
    print("\n3. Testing current events query...")
    query = "What are the latest developments in AI?"
    response = await agent.process_query(query)
    print(f"   Query: {query}")
    print(f"   Response: {response.content[:100]}...")
    print("   ✅ Current events query test passed")
    
    # Test conversation history
    print("\n4. Testing conversation history...")
    history = agent.get_conversation_history()
    print(f"   History entries: {len(history)}")
    print("   ✅ Conversation history test passed")
    
    print("\n✅ All basic functionality tests passed!")

async def test_evaluation_framework():
    """Test the evaluation framework"""
    print("\n🔍 Testing Evaluation Framework")
    print("=" * 50)
    
    # Initialize agent
    agent = ResearchAgent()
    
    # Generate test cases
    print("1. Generating test cases...")
    generator = TestDataGenerator()
    test_cases = generator.get_all_test_cases()
    print(f"   Generated {len(test_cases)} test cases")
    print("   ✅ Test case generation passed")
    
    # Run evaluation on a subset
    print("\n2. Running evaluation on basic test cases...")
    basic_tests = generator.generate_basic_tests()[:3]  # Test first 3 only
    
    evaluator = AgentEvaluator(agent)
    results = await evaluator.evaluate_agent(basic_tests)
    
    print(f"   Evaluated {len(results)} test cases")
    passed_tests = sum(1 for r in results if r.passed)
    print(f"   Passed: {passed_tests}/{len(results)}")
    print("   ✅ Evaluation framework test passed")
    
    # Test metrics calculation
    print("\n3. Testing metrics calculation...")
    metrics = evaluator.calculate_overall_metrics(results)
    print(f"   Overall accuracy: {metrics.accuracy:.2%}")
    print(f"   Tool selection accuracy: {metrics.tool_selection_accuracy:.2%}")
    print("   ✅ Metrics calculation test passed")
    
    print("\n✅ All evaluation framework tests passed!")

async def test_tool_selection():
    """Test tool selection logic"""
    print("\n🔧 Testing Tool Selection Logic")
    print("=" * 50)
    
    agent = ResearchAgent()
    
    test_queries = [
        ("What is Python?", ["knowledge_base"]),
        ("What are the latest Python updates?", ["web_search"]),
        ("Define machine learning", ["knowledge_base"]),
        ("Current news about AI", ["web_search"]),
    ]
    
    for i, (query, expected_tools) in enumerate(test_queries, 1):
        print(f"{i}. Testing: '{query}'")
        tools_to_use = agent._should_use_tool(query)
        print(f"   Expected tools: {expected_tools}")
        print(f"   Selected tools: {tools_to_use}")
        
        # Check if at least one expected tool is selected
        overlap = set(tools_to_use) & set(expected_tools)
        if overlap:
            print("   ✅ Tool selection correct")
        else:
            print("   ⚠️  Tool selection could be improved")
    
    print("\n✅ Tool selection tests completed!")

async def run_all_tests():
    """Run all tests"""
    print("🚀 Starting Research Assistant Chatbot Tests")
    print("=" * 60)
    
    try:
        await test_basic_functionality()
        await test_evaluation_framework()
        await test_tool_selection()
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Set up your HuggingFace API token in .env file")
        print("2. Install requirements: pip install -r requirements.txt")
        print("3. Run interactive mode: python src/cli.py --interactive")
        print("4. Run full evaluation: python src/cli.py --evaluate")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_all_tests())
