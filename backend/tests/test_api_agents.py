"""
Tests for agent API endpoints.
"""

import pytest
import json


class TestAgentAPI:
    """Tests for agent API endpoints."""

    def test_get_agents_empty(self, client):
        """Test getting agents when none exist."""
        response = client.get("/api/agents")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0

    def test_get_agents(self, client, sample_agent):
        """Test getting list of agents."""
        response = client.get("/api/agents")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]["name"] == "Test Agent"
        assert data[0]["type"] == "test"

    def test_get_agent_by_id(self, client, sample_agent):
        """Test getting a specific agent by ID."""
        response = client.get(f"/api/agents/{sample_agent.id}")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["id"] == sample_agent.id
        assert data["name"] == sample_agent.name
        assert data["type"] == sample_agent.type

    def test_get_agent_not_found(self, client):
        """Test getting non-existent agent."""
        response = client.get("/api/agents/9999")
        assert response.status_code == 404

    def test_get_agent_messages_empty(self, client, sample_agent):
        """Test getting messages when none exist."""
        response = client.get(f"/api/agents/{sample_agent.id}/messages")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0

    def test_get_agent_messages(self, client, sample_agent, sample_message):
        """Test getting agent messages."""
        response = client.get(f"/api/agents/{sample_agent.id}/messages")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]["content"] == "Test message"
        assert data[0]["sender"] == "user"

    def test_get_agent_status(self, client, sample_agent):
        """Test getting agent status."""
        response = client.get(f"/api/agents/{sample_agent.id}/status")
        # May return 503 if agent service isn't initialized (expected in tests)
        assert response.status_code in [200, 503]
        if response.status_code == 200:
            data = json.loads(response.data)
            assert "agent_id" in data
            assert "status" in data
            assert data["agent_id"] == sample_agent.id

    def test_send_message_missing_data(self, client, sample_agent):
        """Test sending message without required data."""
        response = client.post(
            f"/api/agents/{sample_agent.id}/message", json={}
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_send_message_to_invalid_agent(self, client):
        """Test sending message to non-existent agent."""
        response = client.post(
            "/api/agents/9999/message", json={"message": "Hello"}
        )
        assert response.status_code == 404


class TestAgentTaskAPI:
    """Tests for agent task API endpoints."""

    def test_create_task_missing_data(self, client):
        """Test creating task without required data."""
        response = client.post("/api/agents/task", json={})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_create_agent_missing_data(self, client):
        """Test creating agent without required data."""
        response = client.post("/api/agents/create", json={})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

