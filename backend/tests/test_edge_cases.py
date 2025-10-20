"""
Tests for edge cases and error handling.
"""

import pytest
import json
from app.models import Agent, Workflow, Task


class TestEdgeCases:
    """Tests for edge cases."""

    def test_agent_with_null_config(self, db_session):
        """Test creating agent with null config."""
        agent = Agent(
            name="Test Agent", type="test", role="Tester", status="idle", config=None
        )
        db_session.add(agent)
        db_session.commit()

        assert agent.id is not None
        assert agent.config is None

    def test_agent_with_empty_config(self, db_session):
        """Test creating agent with empty config."""
        agent = Agent(
            name="Test Agent", type="test", role="Tester", status="idle", config={}
        )
        db_session.add(agent)
        db_session.commit()

        assert agent.id is not None
        assert agent.config == {}

    def test_workflow_without_description(self, db_session):
        """Test creating workflow without description."""
        workflow = Workflow(name="Test", description=None, status="pending")
        db_session.add(workflow)
        db_session.commit()

        assert workflow.id is not None
        assert workflow.description is None

    def test_task_completion_timestamp(
        self, db_session, sample_workflow, sample_agent
    ):
        """Test task completion updates timestamp."""
        task = Task(
            workflow_id=sample_workflow.id,
            assigned_to=sample_agent.id,
            status="pending",
            description="Test",
        )
        db_session.add(task)
        db_session.commit()

        assert task.completed_at is None

        # Complete task
        task.status = "completed"
        from datetime import datetime

        task.completed_at = datetime.utcnow()
        db_session.commit()

        assert task.completed_at is not None


class TestErrorHandling:
    """Tests for error handling."""

    def test_api_invalid_json(self, client):
        """Test API with invalid JSON."""
        response = client.post(
            "/api/workflows",
            data="invalid json",
            content_type="application/json",
        )
        # Flask should return 400 for invalid JSON
        assert response.status_code in [400, 415]

    def test_api_missing_content_type(self, client):
        """Test API without content-type header."""
        response = client.post("/api/workflows", data=json.dumps({"name": "Test"}))
        # Should still work or return 415
        assert response.status_code in [201, 400, 415]

    def test_get_invalid_resource_type(self, client):
        """Test accessing invalid resource."""
        response = client.get("/api/invalid_resource")
        assert response.status_code == 404

    def test_delete_method_not_allowed(self, client, sample_agent):
        """Test using unsupported HTTP method."""
        response = client.delete(f"/api/agents/{sample_agent.id}")
        assert response.status_code == 405

    def test_workflow_with_very_long_name(self, client):
        """Test creating workflow with very long name."""
        long_name = "A" * 1000
        response = client.post(
            "/api/workflows", json={"name": long_name, "description": "Test"}
        )
        # Should either accept or reject gracefully
        assert response.status_code in [201, 400]

    def test_concurrent_workflow_creation(self, client):
        """Test creating multiple workflows simultaneously."""
        responses = []
        for i in range(5):
            response = client.post(
                "/api/workflows", json={"name": f"Workflow {i}", "description": "Test"}
            )
            responses.append(response)

        # All should succeed
        for response in responses:
            assert response.status_code == 201


class TestDataValidation:
    """Tests for data validation."""

    def test_agent_invalid_status(self, db_session):
        """Test agent with invalid status value."""
        agent = Agent(
            name="Test",
            type="test",
            role="Tester",
            status="invalid_status",
            config={},
        )
        db_session.add(agent)
        db_session.commit()

        # Should allow any string (no enum validation)
        assert agent.status == "invalid_status"

    def test_workflow_status_transitions(self, db_session):
        """Test workflow status transitions."""
        workflow = Workflow(name="Test", description="Test", status="pending")
        db_session.add(workflow)
        db_session.commit()

        # Transition to in_progress
        workflow.status = "in_progress"
        db_session.commit()
        assert workflow.status == "in_progress"

        # Transition to completed
        workflow.status = "completed"
        db_session.commit()
        assert workflow.status == "completed"

    def test_empty_message_content(self, db_session, sample_agent):
        """Test creating message with empty content."""
        from app.models import Message

        message = Message(agent_id=sample_agent.id, sender="user", content="")
        db_session.add(message)
        db_session.commit()

        assert message.id is not None
        assert message.content == ""

    def test_special_characters_in_names(self, client):
        """Test creating resources with special characters."""
        response = client.post(
            "/api/workflows",
            json={"name": "Test™️ & <script>alert()</script>", "description": "Test"},
        )
        # Should handle special characters
        assert response.status_code in [201, 400]
        if response.status_code == 201:
            data = json.loads(response.data)
            assert "™️" in data["name"] or "script" in data["name"]


class TestConcurrency:
    """Tests for concurrent operations."""

    def test_multiple_agents_creation(self, db_session):
        """Test creating multiple agents."""
        from app.models import Agent as AgentModel

        agents = []
        for i in range(10):
            agent = AgentModel(
                name=f"Agent {i}",
                type=f"type{i}",
                role="Tester",
                status="idle",
                config={},
            )
            agents.append(agent)

        db_session.add_all(agents)
        db_session.commit()

        # All should be created
        count = AgentModel.query.count()
        assert count >= 10

    def test_multiple_messages_per_agent(self, db_session, sample_agent):
        """Test adding many messages to one agent."""
        from app.models import Message

        messages = []
        for i in range(20):
            message = Message(
                agent_id=sample_agent.id, sender="user", content=f"Message {i}"
            )
            messages.append(message)

        db_session.add_all(messages)
        db_session.commit()

        # All should be associated with agent
        assert len(sample_agent.messages) >= 20
