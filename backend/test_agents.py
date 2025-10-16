"""Test script for the agent system.

This script tests the core agent functionality including:
- Agent initialization
- Message sending
- RAG search
- Agent creation
"""

import asyncio
import os
from dotenv import load_dotenv

from app.agents import agent_manager
from app.services import get_rag_service


def check_environment():
    """Check for required environment variables."""
    # Load environment variables
    load_dotenv()

    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not found in environment variables")
        print("Please create a .env file with your OpenAI API key")
        exit(1)


async def test_agent_initialization():
    """Test 1: Initialize core agents"""
    print("\n" + "=" * 50)
    print("TEST 1: Agent Initialization")
    print("=" * 50)

    status = await agent_manager.initialize_core_agents()

    print(f"Driver: {status.get('driver', 'failed')}")
    print(f"Creator: {status.get('creator', 'failed')}")
    print(f"Generator: {status.get('generator', 'failed')}")

    if "error" in status:
        print(f"ERROR: {status['error']}")
        return False

    print("✅ All core agents initialized")
    return True


async def test_rag_service():
    """Test 2: RAG service functionality"""
    print("\n" + "=" * 50)
    print("TEST 2: RAG Service")
    print("=" * 50)

    rag_service = get_rag_service()

    # Initialize with sample data if empty
    if rag_service.count_documents() == 0:
        print("Initializing RAG with sample data...")
        rag_service.initialize_sample_data()

    print(f"Total documents: {rag_service.count_documents()}")

    # Test search
    query = "What is Python?"
    print(f"\nSearching for: '{query}'")
    results = rag_service.search(query, k=3)

    for i, result in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"  Distance: {result['distance']:.4f}")
        print(f"  Document: {result['document'][:100]}...")

    print("\n✅ RAG service working")

    # Set RAG service for agent manager
    agent_manager.set_rag_service(rag_service)

    return True


async def test_driver_agent():
    """Test 3: Driver Agent"""
    print("\n" + "=" * 50)
    print("TEST 3: Driver Agent")
    print("=" * 50)

    if not agent_manager.driver:
        print("❌ Driver agent not initialized")
        return False

    # Test task processing
    task = "Create a simple Python web API"
    print(f"Task: {task}")

    response = await agent_manager.driver.process_operator_task(task)
    print(f"\nDriver response:\n{response}")

    print("\n✅ Driver agent working")
    return True


async def test_creator_agent():
    """Test 4: Creator Agent"""
    print("\n" + "=" * 50)
    print("TEST 4: Creator Agent")
    print("=" * 50)

    if not agent_manager.creator:
        print("❌ Creator agent not initialized")
        return False

    # Test research
    topic = "Python web frameworks"
    print(f"Research topic: {topic}")

    results = await agent_manager.creator.research_topic(topic, use_rag=True)
    print(f"\nFound {len(results['sources'])} sources")
    print(f"Summary:\n{results['summary'][:200]}...")

    # Test idea generation
    print("\n\nGenerating ideas...")
    ideas = await agent_manager.creator.generate_ideas(
        context="Build a real-time chat application",
        constraints={"tech": "Python + React", "time": "1 week"},
    )

    print(f"Generated {len(ideas)} ideas:")
    for i, idea in enumerate(ideas[:3], 1):
        print(f"{i}. {idea[:100]}...")

    print("\n✅ Creator agent working")
    return True


async def test_generator_agent():
    """Test 5: Generator Agent"""
    print("\n" + "=" * 50)
    print("TEST 5: Generator Agent")
    print("=" * 50)

    if not agent_manager.generator:
        print("❌ Generator agent not initialized")
        return False

    # Test agent specification design
    print("Designing agent specification...")
    spec = await agent_manager.generator.design_agent_spec(
        role="Python Developer",
        capabilities=["coding", "testing", "debugging"],
        requirements={"experience": "senior", "specialization": "backend"},
    )

    print("\nAgent spec created:")
    print(f"  Name: {spec['name']}")
    print(f"  Role: {spec['role']}")
    print(f"  Capabilities: {', '.join(spec['capabilities'])}")
    print(f"  Tools: {spec.get('tools', [])}")
    print(f"  System prompt (first 150 chars):\n  {spec['system_message'][:150]}...")

    print("\n✅ Generator agent working")
    return True


async def test_agent_list():
    """Test 6: List all agents"""
    print("\n" + "=" * 50)
    print("TEST 6: Agent List")
    print("=" * 50)

    agents = agent_manager.get_all_agents()

    print(f"Active agents: {len(agents)}")
    for agent in agents:
        print(f"  - {agent['name']} ({agent['role']}) - Status: {agent['status']}")

    print("\n✅ Agent listing working")
    return True


async def main():
    """Run all tests"""
    check_environment()

    print("\n" + "=" * 70)
    print("VIRTUAL STARTUP AGENT SYSTEM - TEST SUITE")
    print("=" * 70)

    tests = [
        ("Agent Initialization", test_agent_initialization),
        ("RAG Service", test_rag_service),
        ("Driver Agent", test_driver_agent),
        ("Creator Agent", test_creator_agent),
        ("Generator Agent", test_generator_agent),
        ("Agent List", test_agent_list),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} FAILED with error:")
            print(f"   {str(e)}")
            import traceback

            traceback.print_exc()
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! 🎉")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")

    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
