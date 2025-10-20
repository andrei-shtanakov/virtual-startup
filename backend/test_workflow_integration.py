"""
Integration tests for Phase 9: Workflow Orchestration

Tests the complete end-to-end workflow where agents collaborate.
"""

import requests
import time
from typing import Dict, Any

# API base URL
BASE_URL = "http://localhost:5000/api"


def print_header(text: str) -> None:
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)


def print_step(step_num: int, text: str) -> None:
    """Print a formatted step"""
    print(f"\n📋 Step {step_num}: {text}")
    print("-" * 80)


def test_system_status() -> bool:
    """Test 1: Check system status"""
    print_header("TEST 1: System Status")
    
    try:
        response = requests.get(f"{BASE_URL}/status")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API: {data.get('api')}")
            print(f"✅ Agents Initialized: {data.get('agents_initialized')}")
            print(f"✅ Database: {data.get('database')}")
            return True
        else:
            print(f"❌ Failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_list_agents() -> bool:
    """Test 2: List all agents"""
    print_header("TEST 2: List Agents")
    
    try:
        response = requests.get(f"{BASE_URL}/agents")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            agents = response.json()
            print(f"✅ Found {len(agents)} agent(s):")
            for agent in agents:
                print(f"   [{agent['id']}] {agent['name']} ({agent['type']}) - {agent['status']}")
            return len(agents) >= 3
        else:
            print(f"❌ Failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_workflow_creation() -> Dict[str, Any] | None:
    """Test 3: Create a workflow"""
    print_header("TEST 3: Create Workflow")
    
    try:
        response = requests.post(
            f"{BASE_URL}/workflows",
            json={
                "name": "Test Workflow",
                "description": "Build a Python REST API",
                "meta": {"test": True},
            },
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            workflow = response.json()
            print(f"✅ Workflow Created:")
            print(f"   ID: {workflow['id']}")
            print(f"   Name: {workflow['name']}")
            print(f"   Status: {workflow['status']}")
            return workflow
        else:
            print(f"❌ Failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_complete_workflow_execution() -> bool:
    """Test 4: Execute complete end-to-end workflow"""
    print_header("TEST 4: Execute Complete Workflow")
    
    task = "Build a Python REST API for a blog platform with user authentication"
    print(f"Task: {task}")
    
    try:
        print_step(1, "Sending workflow execution request...")
        response = requests.post(
            f"{BASE_URL}/workflows/execute", json={"task": task}
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            workflow_id = result.get("workflow_id")
            status = result.get("status")
            steps = result.get("steps", [])
            
            print(f"\n✅ Workflow Executed Successfully!")
            print(f"   Workflow ID: {workflow_id}")
            print(f"   Status: {status}")
            print(f"   Steps Completed: {len(steps)}")
            
            print_step(2, "Workflow Steps:")
            for step in steps:
                step_num = step.get("step")
                agent = step.get("agent")
                result_data = step.get("result", {})
                response_text = result_data.get("response", "No response")[:200]
                
                print(f"\n   Step {step_num}: {agent.upper()}")
                print(f"   Response: {response_text}...")
            
            print_step(3, "Checking workflow status...")
            time.sleep(1)
            status_response = requests.get(
                f"{BASE_URL}/workflows/{workflow_id}/status"
            )
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                wf = status_data.get("workflow", {})
                tasks = status_data.get("tasks", [])
                
                print(f"   Workflow Status: {wf.get('status')}")
                print(f"   Tasks: {len(tasks)}")
                for task in tasks:
                    print(
                        f"      - {task.get('assigned_to')}: {task.get('status')}"
                    )
            
            return True
        else:
            print(f"❌ Failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_agent_collaboration() -> bool:
    """Test 5: Test agent collaboration via messages"""
    print_header("TEST 5: Agent Collaboration")
    
    try:
        # Get Driver agent
        print_step(1, "Getting Driver agent...")
        response = requests.get(f"{BASE_URL}/agents")
        agents = response.json()
        driver = next((a for a in agents if a["type"] == "driver"), None)
        
        if not driver:
            print("❌ Driver agent not found")
            return False
        
        print(f"✅ Found Driver: {driver['name']} (ID: {driver['id']})")
        
        # Send message to Driver
        print_step(2, "Sending task to Driver...")
        message = "Help me research and create a Python backend framework comparison"
        response = requests.post(
            f"{BASE_URL}/agents/{driver['id']}/message", json={"message": message}
        )
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get("response", "")[:300]
            print(f"✅ Driver Response: {response_text}...")
            
            # Check messages
            print_step(3, "Checking message history...")
            messages_response = requests.get(
                f"{BASE_URL}/agents/{driver['id']}/messages"
            )
            
            if messages_response.status_code == 200:
                messages = messages_response.json()
                print(f"✅ Total messages: {len(messages)}")
                if messages:
                    latest = messages[-1]
                    print(f"   Latest from: {latest.get('sender')}")
                    print(f"   Content: {latest.get('content', '')[:100]}...")
            
            return True
        else:
            print(f"❌ Failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_error_handling() -> bool:
    """Test 6: Test error handling"""
    print_header("TEST 6: Error Handling")
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Invalid workflow ID
    print_step(1, "Testing invalid workflow ID...")
    try:
        response = requests.get(f"{BASE_URL}/workflows/99999")
        if response.status_code == 404:
            print("✅ Correctly returns 404 for invalid workflow")
            tests_passed += 1
        else:
            print(f"❌ Expected 404, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Missing required field
    print_step(2, "Testing missing required field...")
    try:
        response = requests.post(f"{BASE_URL}/workflows", json={})
        if response.status_code == 400:
            print("✅ Correctly returns 400 for missing required field")
            tests_passed += 1
        else:
            print(f"❌ Expected 400, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Invalid agent ID
    print_step(3, "Testing invalid agent ID...")
    try:
        response = requests.get(f"{BASE_URL}/agents/99999")
        if response.status_code == 404:
            print("✅ Correctly returns 404 for invalid agent")
            tests_passed += 1
        else:
            print(f"❌ Expected 404, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print(f"\n✅ Error Handling Tests: {tests_passed}/{total_tests} passed")
    return tests_passed == total_tests


def run_all_tests() -> None:
    """Run all integration tests"""
    print("\n" + "=" * 80)
    print("  PHASE 9: WORKFLOW INTEGRATION TESTS")
    print("=" * 80)
    print("\nTesting end-to-end workflow orchestration and agent collaboration...")
    
    tests = [
        ("System Status", test_system_status),
        ("List Agents", test_list_agents),
        ("Workflow Creation", lambda: test_workflow_creation() is not None),
        ("Complete Workflow Execution", test_complete_workflow_execution),
        ("Agent Collaboration", test_agent_collaboration),
        ("Error Handling", test_error_handling),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            time.sleep(0.5)  # Small delay between tests
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print_header("TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{'=' * 80}")
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Phase 9 integration is working correctly.")
    else:
        print(f"⚠️  {total - passed} test(s) failed. Please review the output above.")
    print("=" * 80)


if __name__ == "__main__":
    print("\n⚠️  NOTE: Make sure the backend server is running on http://localhost:5000")
    print("   Start it with: cd backend && uv run python run.py\n")
    
    input("Press Enter to start tests...")
    run_all_tests()



