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

    def test_rag_add_documents(self, app):
        """Test adding documents to RAG."""
        with app.app_context():
            from app.services import get_rag_service
            from unittest.mock import MagicMock

            service = get_rag_service()

            # Mock the collection
            service.collection = MagicMock()
            service.collection.add = MagicMock()

            # Add documents
            docs = ["Document 1", "Document 2"]
            metadatas = [{"source": "test1"}, {"source": "test2"}]

            service.add_documents(documents=docs, metadatas=metadatas)

            # Verify collection.add was called
            service.collection.add.assert_called_once()
            call_args = service.collection.add.call_args
            assert len(call_args.kwargs["documents"]) == 2
            assert len(call_args.kwargs["metadatas"]) == 2

    def test_rag_search(self, app):
        """Test searching RAG knowledge base."""
        with app.app_context():
            from app.services import get_rag_service
            from unittest.mock import MagicMock

            service = get_rag_service()

            # Mock the collection.query method
            service.collection.query = MagicMock(
                return_value={
                    "documents": [["Test document 1", "Test document 2"]],
                    "metadatas": [[{"source": "test1"}, {"source": "test2"}]],
                    "distances": [[0.1, 0.2]],
                    "ids": [["id1", "id2"]],
                }
            )

            # Search
            results = service.search("test query", k=2)

            # Verify results
            assert len(results) == 2
            assert results[0]["document"] == "Test document 1"
            assert results[0]["metadata"]["source"] == "test1"
            assert results[0]["distance"] == 0.1
            assert results[1]["document"] == "Test document 2"

    def test_rag_get_relevant_context(self, app):
        """Test getting relevant context as string."""
        with app.app_context():
            from app.services import get_rag_service
            from unittest.mock import MagicMock

            service = get_rag_service()

            # Mock the search method
            service.search = MagicMock(
                return_value=[
                    {"document": "Context 1", "metadata": {}, "distance": 0.1},
                    {"document": "Context 2", "metadata": {}, "distance": 0.2},
                ]
            )

            # Get context
            context = service.get_relevant_context("test query", k=2)

            # Verify context
            assert "Context 1" in context
            assert "Context 2" in context
            assert "---" in context  # Separator

    def test_rag_count_documents(self, app):
        """Test counting documents in RAG."""
        with app.app_context():
            from app.services import get_rag_service
            from unittest.mock import MagicMock

            service = get_rag_service()

            # Mock count
            service.collection.count = MagicMock(return_value=10)

            # Count
            count = service.count_documents()
            assert count == 10

    def test_rag_delete_documents(self, app):
        """Test deleting documents from RAG."""
        with app.app_context():
            from app.services import get_rag_service
            from unittest.mock import MagicMock

            service = get_rag_service()

            # Mock delete
            service.collection.delete = MagicMock()

            # Delete
            service.delete_documents(["id1", "id2"])

            # Verify delete was called
            service.collection.delete.assert_called_once_with(ids=["id1", "id2"])

    def test_rag_update_document(self, app):
        """Test updating a document in RAG."""
        with app.app_context():
            from app.services import get_rag_service
            from unittest.mock import MagicMock

            service = get_rag_service()

            # Mock update
            service.collection.update = MagicMock()

            # Update document
            service.update_document(
                id="id1",
                document="Updated document",
                metadata={"source": "updated"}
            )

            # Verify update was called
            service.collection.update.assert_called_once()
            call_args = service.collection.update.call_args
            assert call_args.kwargs["ids"] == ["id1"]
            assert call_args.kwargs["documents"] == ["Updated document"]


class TestAgentService:
    """Tests for AgentService."""

    def test_agent_service_singleton(self, app):
        """Test that agent service is a singleton."""
        with app.app_context():
            from app.services import get_agent_service

            service1 = get_agent_service()
            service2 = get_agent_service()
            assert service1 is service2

    def test_agent_service_initialization_status(self, app):
        """Test agent service initialization status."""
        with app.app_context():
            from app.services import get_agent_service

            service = get_agent_service()

            # Initially not initialized
            assert service.initialized is False

            # Calling ensure_initialized should raise error
            with pytest.raises(RuntimeError, match="Agent system not initialized"):
                service.ensure_initialized()

    def test_get_all_agents_not_initialized(self, app, db_session, sample_agent):
        """Test getting all agents when system not initialized."""
        with app.app_context():
            from app.services import get_agent_service

            service = get_agent_service()

            # Should return from database when not initialized
            agents = service.get_all_agents()
            assert len(agents) >= 1
            assert any(a["name"] == "Test Agent" for a in agents)

    def test_get_conversation_history(self, app, db_session, sample_agent, sample_message):
        """Test getting conversation history."""
        with app.app_context():
            from app.services import get_agent_service

            service = get_agent_service()

            # Get conversation history
            history = service.get_agent_conversation_history(sample_agent.id, limit=10)

            # Verify history
            assert len(history) >= 1
            assert history[0]["content"] == "Test message"
            assert history[0]["sender"] == "user"


class TestTaskProcessor:
    """Tests for TaskProcessor service."""

    def test_task_processor_singleton(self, app):
        """Test that task processor is a singleton."""
        with app.app_context():
            from app.services import get_task_processor

            processor1 = get_task_processor()
            processor2 = get_task_processor()
            assert processor1 is processor2

