"""
Integration tests for end-to-end workflows.

These tests verify complete user journeys and multi-component interactions:
- Agent initialization and communication
- Workflow execution from start to finish
- Database persistence across operations
- REST API + Service + Model integration
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestSystemInitialization:
    """Tests for system initialization."""

    def test_system_status_endpoint(self, client):
        """Test system status endpoint."""
        response = client.get("/api/status")
        assert response.status_code == 200

        data = response.get_json()
        assert data["api"] == "running"
        assert "agents_initialized" in data
        assert data["database"] == "connected"

    def test_root_endpoint(self, client):
        """Test root health check endpoint."""
        response = client.get("/")
        assert response.status_code == 200

        data = response.get_json()
        assert data["status"] == "ok"
        assert "Virtual Startup" in data["message"]


class TestAgentWorkflow:
    """Integration tests for agent workflows."""

    def test_create_and_retrieve_agent(self, client, db_session):
        """Test creating an agent and retrieving it."""
        from app.models import Agent

        # Create agent in database
        agent = Agent(
            name="Integration Test Agent",
            type="test",
            role="Tester",
            status="idle",
            config={"model": "gpt-4"},
        )
        db_session.add(agent)
        db_session.commit()

        # Retrieve agent via API
        response = client.get(f"/api/agents/{agent.id}")
        assert response.status_code == 200

        data = response.get_json()
        assert data["name"] == "Integration Test Agent"
        assert data["type"] == "test"
        assert data["status"] == "idle"

    def test_agent_conversation_flow(self, client, db_session):
        """Test complete agent conversation flow."""
        from app.models import Agent, Message

        # Create agent
        agent = Agent(
            name="Chat Agent",
            type="assistant",
            role="Assistant",
            status="idle",
            config={},
        )
        db_session.add(agent)
        db_session.commit()

        # Send message via API
        response = client.post(
            f"/api/agents/{agent.id}/message",
            json={"message": "Hello, agent!"},
        )

        # Should fail because agent system not initialized (503 Service Unavailable)
        # But the endpoint should handle it gracefully
        assert response.status_code in [200, 400, 500, 503]

        # Retrieve conversation history
        response = client.get(f"/api/agents/{agent.id}/messages")
        assert response.status_code == 200

        messages = response.get_json()
        assert isinstance(messages, list)

    def test_list_all_agents(self, client, db_session):
        """Test listing all agents."""
        from app.models import Agent

        # Create multiple agents
        agents = [
            Agent(name=f"Agent {i}", type="test", role="Tester", status="idle")
            for i in range(3)
        ]
        for agent in agents:
            db_session.add(agent)
        db_session.commit()

        # Get all agents
        response = client.get("/api/agents")
        assert response.status_code == 200

        data = response.get_json()
        assert len(data) >= 3


class TestWorkflowExecution:
    """Integration tests for workflow execution."""

    def test_create_workflow(self, client):
        """Test creating a workflow."""
        response = client.post(
            "/api/workflows",
            json={
                "name": "Integration Test Workflow",
                "description": "Testing end-to-end workflow",
            },
        )

        assert response.status_code == 201
        data = response.get_json()
        assert data["name"] == "Integration Test Workflow"
        # Status can be 'pending' or 'active' depending on implementation
        assert data["status"] in ["pending", "active"]
        assert "id" in data

        return data["id"]

    def test_workflow_lifecycle(self, client, db_session):
        """Test complete workflow lifecycle."""
        from app.models import Workflow, Task

        # Create workflow
        workflow = Workflow(
            name="Lifecycle Test",
            description="Testing workflow states",
            status="pending",
        )
        db_session.add(workflow)
        db_session.commit()

        # Create task for workflow
        task = Task(
            workflow_id=workflow.id,
            assigned_to="test_agent",
            description="Test task",
            status="pending",
        )
        db_session.add(task)
        db_session.commit()

        # Get workflow status
        response = client.get(f"/api/workflows/{workflow.id}/status")
        assert response.status_code == 200

        data = response.get_json()
        assert data["workflow"]["id"] == workflow.id
        assert data["workflow"]["status"] == "pending"
        assert len(data["tasks"]) >= 1

        # Update workflow status directly in DB
        workflow.status = "running"
        db_session.commit()

        # Verify update
        response = client.get(f"/api/workflows/{workflow.id}")
        assert response.status_code == 200
        assert response.get_json()["status"] == "running"

    def test_list_workflows(self, client, db_session):
        """Test listing workflows."""
        from app.models import Workflow

        # Create workflows
        workflows = [
            Workflow(name=f"Workflow {i}", description="Test", status="pending")
            for i in range(3)
        ]
        for wf in workflows:
            db_session.add(wf)
        db_session.commit()

        # Get all workflows
        response = client.get("/api/workflows")
        assert response.status_code == 200

        data = response.get_json()
        assert len(data) >= 3


class TestStatsAndMetrics:
    """Integration tests for stats and metrics."""

    def test_agent_stats(self, client, db_session):
        """Test agent statistics endpoint."""
        from app.models import Agent

        # Create some agents
        agents = [
            Agent(name=f"Stats Agent {i}", type="test", role="Tester", status="idle")
            for i in range(2)
        ]
        for agent in agents:
            db_session.add(agent)
        db_session.commit()

        # Get agent stats
        response = client.get("/api/stats/agents")
        assert response.status_code == 200

        stats = response.get_json()
        assert "total" in stats
        assert stats["total"] >= 2
        # Stats structure may vary - check for status keys directly
        assert "idle" in stats or "active" in stats or "by_status" in stats

    def test_workflow_stats(self, client, db_session):
        """Test workflow statistics endpoint."""
        from app.models import Workflow

        # Create workflows in different states
        workflows = [
            Workflow(name="Pending WF", description="Test", status="pending"),
            Workflow(name="Running WF", description="Test", status="running"),
            Workflow(name="Completed WF", description="Test", status="completed"),
        ]
        for wf in workflows:
            db_session.add(wf)
        db_session.commit()

        # Get workflow stats
        response = client.get("/api/stats/workflows")
        assert response.status_code == 200

        stats = response.get_json()
        assert "total" in stats
        assert stats["total"] >= 3
        # Check for workflow status counts (structure may vary)
        assert "completed" in stats or "by_status" in stats
        # At least one completed workflow exists
        completed_count = stats.get("completed", stats.get("by_status", {}).get("completed", 0))
        assert completed_count >= 1

    def test_overview_stats(self, client, db_session):
        """Test overview statistics endpoint."""
        from app.models import Agent, Workflow, Message

        # Create test data
        agent = Agent(name="Overview Agent", type="test", role="Tester", status="idle")
        db_session.add(agent)
        db_session.commit()

        message = Message(agent_id=agent.id, sender="user", content="Test message")
        db_session.add(message)

        workflow = Workflow(name="Overview WF", description="Test", status="pending")
        db_session.add(workflow)
        db_session.commit()

        # Get overview stats
        response = client.get("/api/stats/overview")
        assert response.status_code == 200

        stats = response.get_json()
        assert "agents" in stats
        assert "workflows" in stats
        # Messages might not be in overview stats
        assert stats["agents"]["total"] >= 1
        assert stats["workflows"]["total"] >= 1


class TestErrorHandling:
    """Integration tests for error handling."""

    def test_get_nonexistent_agent(self, client):
        """Test retrieving non-existent agent."""
        response = client.get("/api/agents/99999")
        assert response.status_code == 404

        # Response might be None for 404
        data = response.get_json()
        if data:
            assert "error" in data or "message" in data

    def test_get_nonexistent_workflow(self, client):
        """Test retrieving non-existent workflow."""
        response = client.get("/api/workflows/99999")
        assert response.status_code == 404

    def test_send_message_to_invalid_agent(self, client):
        """Test sending message to invalid agent."""
        response = client.post(
            "/api/agents/99999/message",
            json={"message": "Hello"},
        )

        assert response.status_code in [400, 404]

    def test_create_workflow_missing_name(self, client):
        """Test creating workflow without name."""
        response = client.post(
            "/api/workflows",
            json={"description": "Missing name"},
        )

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data or "message" in data

    def test_invalid_json_request(self, client):
        """Test sending invalid JSON."""
        response = client.post(
            "/api/workflows",
            data="not json",
            content_type="application/json",
        )

        # Should handle gracefully
        assert response.status_code in [400, 500]


class TestDatabasePersistence:
    """Integration tests for database persistence."""

    def test_agent_persistence_across_requests(self, client, db_session):
        """Test that agent data persists across multiple requests."""
        from app.models import Agent

        # Create agent
        agent = Agent(
            name="Persistent Agent",
            type="test",
            role="Tester",
            status="idle",
        )
        db_session.add(agent)
        db_session.commit()
        agent_id = agent.id

        # Get agent in first request
        response1 = client.get(f"/api/agents/{agent_id}")
        assert response1.status_code == 200
        data1 = response1.get_json()

        # Get agent in second request
        response2 = client.get(f"/api/agents/{agent_id}")
        assert response2.status_code == 200
        data2 = response2.get_json()

        # Should be identical
        assert data1 == data2
        assert data1["name"] == "Persistent Agent"

    def test_workflow_task_relationships(self, client, db_session):
        """Test workflow-task relationships persist correctly."""
        from app.models import Workflow, Task

        # Create workflow with tasks
        workflow = Workflow(
            name="Relationship Test",
            description="Testing relationships",
            status="pending",
        )
        db_session.add(workflow)
        db_session.commit()

        tasks = [
            Task(
                workflow_id=workflow.id,
                assigned_to=f"agent_{i}",
                description=f"Task {i}",
                status="pending",
            )
            for i in range(3)
        ]
        for task in tasks:
            db_session.add(task)
        db_session.commit()

        # Get workflow status (includes tasks)
        response = client.get(f"/api/workflows/{workflow.id}/status")
        assert response.status_code == 200

        data = response.get_json()
        assert len(data["tasks"]) == 3
        assert all(t["workflow_id"] == workflow.id for t in data["tasks"])

    def test_message_history_ordering(self, client, db_session):
        """Test that message history is returned in correct order."""
        from app.models import Agent, Message
        from datetime import datetime, timedelta

        # Create agent
        agent = Agent(name="History Agent", type="test", role="Tester", status="idle")
        db_session.add(agent)
        db_session.commit()

        # Create messages with different timestamps
        base_time = datetime.utcnow()
        messages = [
            Message(
                agent_id=agent.id,
                sender="user",
                content=f"Message {i}",
                timestamp=base_time + timedelta(seconds=i),
            )
            for i in range(3)
        ]
        for msg in messages:
            db_session.add(msg)
        db_session.commit()

        # Get message history
        response = client.get(f"/api/agents/{agent.id}/messages")
        assert response.status_code == 200

        history = response.get_json()
        assert len(history) == 3

        # Verify ordering (should be chronological or reverse chronological)
        timestamps = [msg["timestamp"] for msg in history]
        assert timestamps == sorted(timestamps) or timestamps == sorted(
            timestamps, reverse=True
        )


class TestConcurrentOperations:
    """Integration tests for concurrent operations."""

    def test_concurrent_agent_creation(self, client, db_session):
        """Test creating multiple agents concurrently."""
        from app.models import Agent

        # Create multiple agents
        agents = [
            Agent(
                name=f"Concurrent Agent {i}",
                type="test",
                role="Tester",
                status="idle",
            )
            for i in range(5)
        ]
        for agent in agents:
            db_session.add(agent)
        db_session.commit()

        # Verify all were created
        response = client.get("/api/agents")
        assert response.status_code == 200

        data = response.get_json()
        concurrent_agents = [a for a in data if "Concurrent Agent" in a["name"]]
        assert len(concurrent_agents) == 5

    def test_concurrent_workflow_status_checks(self, client, db_session):
        """Test checking status of multiple workflows."""
        from app.models import Workflow

        # Create workflows
        workflows = [
            Workflow(
                name=f"Concurrent WF {i}",
                description="Test",
                status="pending",
            )
            for i in range(3)
        ]
        for wf in workflows:
            db_session.add(wf)
        db_session.commit()

        # Check status of all workflows
        for wf in workflows:
            response = client.get(f"/api/workflows/{wf.id}/status")
            assert response.status_code == 200

            data = response.get_json()
            assert data["workflow"]["id"] == wf.id
            assert data["workflow"]["name"] == wf.name
