"""
Tests for workflow API endpoints.
"""

import pytest
import json


class TestWorkflowAPI:
    """Tests for workflow API endpoints."""

    def test_get_workflows_empty(self, client):
        """Test getting workflows when none exist."""
        response = client.get("/api/workflows")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0

    def test_get_workflows(self, client, sample_workflow):
        """Test getting list of workflows."""
        response = client.get("/api/workflows")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]["name"] == "Test Workflow"

    def test_get_workflow_by_id(self, client, sample_workflow):
        """Test getting a specific workflow by ID."""
        response = client.get(f"/api/workflows/{sample_workflow.id}")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["id"] == sample_workflow.id
        assert data["name"] == sample_workflow.name

    def test_get_workflow_not_found(self, client):
        """Test getting non-existent workflow."""
        response = client.get("/api/workflows/9999")
        assert response.status_code == 404

    def test_create_workflow(self, client):
        """Test creating a workflow."""
        response = client.post(
            "/api/workflows",
            json={
                "name": "New Workflow",
                "description": "Test workflow",
                "meta": {"test": True},
            },
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["name"] == "New Workflow"
        assert data["description"] == "Test workflow"
        # Workflow status defaults to "active" when created
        assert data["status"] in ["pending", "active"]

    def test_create_workflow_missing_name(self, client):
        """Test creating workflow without name."""
        response = client.post("/api/workflows", json={})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_get_workflow_status(self, client, sample_workflow, sample_task):
        """Test getting workflow status with tasks."""
        response = client.get(f"/api/workflows/{sample_workflow.id}/status")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "workflow" in data
        assert "tasks" in data
        assert len(data["tasks"]) == 1

    def test_execute_workflow_missing_task(self, client):
        """Test executing workflow without task description."""
        response = client.post("/api/workflows/execute", json={})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_start_workflow_missing_message(self, client, sample_workflow):
        """Test starting workflow without message."""
        response = client.post(
            f"/api/workflows/{sample_workflow.id}/start", json={}
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data


class TestStatsAPI:
    """Tests for stats API endpoints."""

    def test_get_agent_stats(self, client):
        """Test getting agent statistics."""
        response = client.get("/api/stats/agents")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "total" in data

    def test_get_workflow_stats(self, client):
        """Test getting workflow statistics."""
        response = client.get("/api/stats/workflows")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "total" in data

    def test_get_overview_stats(self, client):
        """Test getting overview statistics."""
        response = client.get("/api/stats/overview")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "agents" in data
        assert "workflows" in data

