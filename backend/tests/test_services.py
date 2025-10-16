"""
Tests for service layer.
"""

import pytest
from app.services import get_workflow_orchestrator
from app.models import Workflow, Task, Agent
from datetime import datetime


class TestWorkflowOrchestrator:
    """Tests for WorkflowOrchestrator service."""

    def test_create_workflow(self, app, db_session):
        """Test creating a workflow via orchestrator."""
        with app.app_context():
            orchestrator = get_workflow_orchestrator()
            workflow = orchestrator.create_workflow(
                name="Test Workflow",
                description="A test",
                initial_task="Test task",
            )

            assert workflow.id is not None
            assert workflow.name == "Test Workflow"
            assert workflow.status == "pending"
            assert workflow.meta.get("initial_task") == "Test task"

    def test_get_workflow_status(self, app, db_session, sample_workflow, sample_task):
        """Test getting workflow status."""
        with app.app_context():
            orchestrator = get_workflow_orchestrator()
            status = orchestrator.get_workflow_status(sample_workflow.id)

            assert status["workflow"]["id"] == sample_workflow.id
            assert "tasks" in status
            assert len(status["tasks"]) >= 1

    def test_get_workflow_status_not_found(self, app, db_session):
        """Test getting status of non-existent workflow."""
        with app.app_context():
            orchestrator = get_workflow_orchestrator()
            with pytest.raises(ValueError, match="not found"):
                orchestrator.get_workflow_status(9999)

    def test_complete_workflow(self, app, db_session, sample_workflow):
        """Test completing a workflow."""
        with app.app_context():
            orchestrator = get_workflow_orchestrator()
            orchestrator.complete_workflow(sample_workflow.id)

            workflow = Workflow.query.get(sample_workflow.id)
            assert workflow.status == "completed"
            assert workflow.completed_at is not None

    def test_fail_workflow(self, app, db_session, sample_workflow):
        """Test failing a workflow."""
        with app.app_context():
            orchestrator = get_workflow_orchestrator()
            orchestrator.fail_workflow(sample_workflow.id, "Test error")

            workflow = Workflow.query.get(sample_workflow.id)
            assert workflow.status == "failed"
            assert workflow.completed_at is not None
            assert workflow.meta.get("error") == "Test error"


class TestRAGService:
    """Tests for RAG service."""

    def test_rag_service_singleton(self, app):
        """Test that RAG service is a singleton."""
        with app.app_context():
            from app.services import get_rag_service

            service1 = get_rag_service()
            service2 = get_rag_service()
            assert service1 is service2

    @pytest.mark.skip(reason="RAG service requires complex initialization")
    def test_rag_add_document(self, app):
        """Test adding a document to RAG."""
        pass

    @pytest.mark.skip(reason="RAG service requires complex initialization")
    def test_rag_search(self, app):
        """Test searching RAG knowledge base."""
        pass

    @pytest.mark.skip(reason="RAG service requires complex initialization")
    def test_rag_clear(self, app):
        """Test clearing RAG knowledge base."""
        pass


class TestAgentService:
    """Tests for AgentService."""

    def test_agent_service_singleton(self, app):
        """Test that agent service is a singleton."""
        with app.app_context():
            from app.services import get_agent_service

            service1 = get_agent_service()
            service2 = get_agent_service()
            assert service1 is service2

    @pytest.mark.skip(reason="Agent service requires initialization")
    def test_get_agent_status(self, app, db_session, sample_agent):
        """Test getting agent status."""
        pass


class TestTaskProcessor:
    """Tests for TaskProcessor service."""

    def test_task_processor_singleton(self, app):
        """Test that task processor is a singleton."""
        with app.app_context():
            from app.services import get_task_processor

            processor1 = get_task_processor()
            processor2 = get_task_processor()
            assert processor1 is processor2

