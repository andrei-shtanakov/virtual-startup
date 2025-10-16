"""Test script for API and WebSocket integration with agent system.

This script tests the Phase 4 integration of agents with REST API.
"""

import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = "http://localhost:5000"


def test_health_check():
    """Test 1: Health check endpoint."""
    print("\n" + "=" * 50)
    print("TEST 1: Health Check")
    print("=" * 50)

    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 200
    print("✅ Health check passed")
    return True


def test_system_status():
    """Test 2: System status before initialization."""
    print("\n" + "=" * 50)
    print("TEST 2: System Status (Before Init)")
    print("=" * 50)

    response = requests.get(f"{BASE_URL}/api/status")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")

    assert response.status_code == 200
    assert data["api"] == "running"
    print("✅ System status check passed")
    return True


def test_agent_initialization():
    """Test 3: Initialize agent system."""
    print("\n" + "=" * 50)
    print("TEST 3: Agent System Initialization")
    print("=" * 50)

    response = requests.post(f"{BASE_URL}/api/init")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")

    assert response.status_code == 200
    assert data["status"] in ["initialized", "already_initialized"]

    # Wait a moment for initialization
    time.sleep(2)

    print("✅ Agent system initialized")
    return True


def test_get_agents():
    """Test 4: Get all agents."""
    print("\n" + "=" * 50)
    print("TEST 4: Get All Agents")
    print("=" * 50)

    response = requests.get(f"{BASE_URL}/api/agents")
    print(f"Status: {response.status_code}")
    data = response.json()

    print(f"Found {len(data)} agents:")
    for agent in data:
        print(f"  - {agent['name']} ({agent['type']}) - Status: {agent['status']}")

    assert response.status_code == 200
    assert len(data) >= 3  # At least 3 core agents

    print("✅ Get agents passed")
    return data


def test_send_message_to_agent(agents):
    """Test 5: Send message to Driver agent."""
    print("\n" + "=" * 50)
    print("TEST 5: Send Message to Driver Agent")
    print("=" * 50)

    # Find Driver agent
    driver_agent = next((a for a in agents if a["type"] == "driver"), None)

    if not driver_agent:
        print("❌ Driver agent not found")
        return False

    agent_id = driver_agent["id"]
    message = "Hello! Can you help me create a simple Python web API?"

    print(f"Sending message to agent {agent_id} (Driver):")
    print(f"  Message: {message}")

    response = requests.post(
        f"{BASE_URL}/api/agents/{agent_id}/message", json={"message": message}
    )

    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"\nAgent: {data.get('agent_name')}")
        print(f"Response: {data.get('response')[:200]}...")
        print(f"Status: {data.get('status')}")
        print("✅ Message sent and received successfully")
        return True
    else:
        print(f"❌ Error: {response.json()}")
        return False


def test_send_task_to_driver():
    """Test 6: Send task to Driver agent."""
    print("\n" + "=" * 50)
    print("TEST 6: Send Task to Driver")
    print("=" * 50)

    task = "Research the best Python web frameworks for building APIs"

    print(f"Sending task: {task}")

    response = requests.post(f"{BASE_URL}/api/agents/task", json={"task": task})

    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"\nSuccess: {data.get('success')}")
        print(f"Agent: {data.get('agent')}")
        print(f"Response: {data.get('response')[:200]}...")
        print("✅ Task sent successfully")
        return True
    else:
        print(f"❌ Error: {response.json()}")
        return False


def test_get_agent_messages(agents):
    """Test 7: Get agent conversation history."""
    print("\n" + "=" * 50)
    print("TEST 7: Get Agent Messages")
    print("=" * 50)

    # Use Driver agent
    driver_agent = next((a for a in agents if a["type"] == "driver"), None)

    if not driver_agent:
        print("❌ Driver agent not found")
        return False

    agent_id = driver_agent["id"]

    response = requests.get(f"{BASE_URL}/api/agents/{agent_id}/messages?limit=10")
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        messages = response.json()
        print(f"\nFound {len(messages)} messages")

        for i, msg in enumerate(messages[:3], 1):
            print(f"\n{i}. [{msg['sender']}] ({msg['timestamp']})")
            print(f"   {msg['content'][:100]}...")

        print("✅ Message history retrieved")
        return True
    else:
        print(f"❌ Error: {response.json()}")
        return False


def test_agent_status(agents):
    """Test 8: Get agent status."""
    print("\n" + "=" * 50)
    print("TEST 8: Get Agent Status")
    print("=" * 50)

    driver_agent = next((a for a in agents if a["type"] == "driver"), None)

    if not driver_agent:
        print("❌ Driver agent not found")
        return False

    agent_id = driver_agent["id"]

    response = requests.get(f"{BASE_URL}/api/agents/{agent_id}/status")
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"\nAgent Status:")
        print(f"  Name: {data.get('name')}")
        print(f"  Role: {data.get('role')}")
        print(f"  Type: {data.get('type')}")
        print(f"  Status: {data.get('status')}")
        print("✅ Agent status retrieved")
        return True
    else:
        print(f"❌ Error: {response.json()}")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("PHASE 4: API & WEBSOCKET INTEGRATION TEST SUITE")
    print("=" * 70)

    print("\n⚠️  Make sure the backend server is running on http://localhost:5000")
    input("Press Enter to continue...")

    tests = [
        ("Health Check", test_health_check, []),
        ("System Status", test_system_status, []),
        ("Agent Initialization", test_agent_initialization, []),
        ("Get All Agents", test_get_agents, []),
    ]

    results = []
    agents = None

    # Run initial tests
    for test_name, test_func, args in tests:
        try:
            result = test_func(*args)
            results.append((test_name, True))

            # Save agents list for later tests
            if test_name == "Get All Agents" and result:
                agents = result

        except Exception as e:
            print(f"\n❌ {test_name} FAILED with error:")
            print(f"   {str(e)}")
            import traceback

            traceback.print_exc()
            results.append((test_name, False))

    # Run tests that need agents
    if agents:
        agent_tests = [
            ("Send Message to Agent", test_send_message_to_agent, [agents]),
            ("Send Task to Driver", test_send_task_to_driver, []),
            ("Get Agent Messages", test_get_agent_messages, [agents]),
            ("Get Agent Status", test_agent_status, [agents]),
        ]

        for test_name, test_func, args in agent_tests:
            try:
                test_func(*args)
                results.append((test_name, True))
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
        print("\n✅ Phase 4 API Integration Complete!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")

    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
