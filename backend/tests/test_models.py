"""
Tests for database models.
"""

import pytest
from datetime import datetime
from app.models import Agent, Message, Workflow, Task


class TestAgentModel:
    """Tests for Agent model."""

    def test_create_agent(self, db_session):
        """Test creating an agent."""
        agent = Agent(
            name="Test Agent",
            type="test",
            role="Tester",
            status="idle",
            config={"model": "gpt-4"},
        )
        db_session.add(agent)
        db_session.commit()

        assert agent.id is not None
        assert agent.name == "Test Agent"
        assert agent.type == "test"
        assert agent.role == "Tester"
        assert agent.status == "idle"
        assert agent.config == {"model": "gpt-4"}
        assert isinstance(agent.created_at, datetime)

    def test_agent_to_dict(self, sample_agent):
        """Test agent to_dict method."""
        data = sample_agent.to_dict()

        assert data["id"] == sample_agent.id
        assert data["name"] == sample_agent.name
        assert data["type"] == sample_agent.type
        assert data["role"] == sample_agent.role
        assert data["status"] == sample_agent.status
        assert data["config"] == sample_agent.config
        assert "created_at" in data

    def test_agent_relationships(self, db_session, sample_agent):
        """Test agent relationships with messages."""
        message = Message(
            agent_id=sample_agent.id, sender="user", content="Test message"
        )
        db_session.add(message)
        db_session.commit()

        assert len(sample_agent.messages) == 1
        assert sample_agent.messages[0].content == "Test message"


class TestMessageModel:
    """Tests for Message model."""

    def test_create_message(self, db_session, sample_agent):
        """Test creating a message."""
        message = Message(
            agent_id=sample_agent.id,
            sender="user",
            content="Hello, agent!",
            meta={"test": True},
        )
        db_session.add(message)
        db_session.commit()

        assert message.id is not None
        assert message.agent_id == sample_agent.id
        assert message.sender == "user"
        assert message.content == "Hello, agent!"
        assert message.meta == {"test": True}
        assert isinstance(message.timestamp, datetime)

    def test_message_to_dict(self, sample_message):
        """Test message to_dict method."""
        data = sample_message.to_dict()

        assert data["id"] == sample_message.id
        assert data["agent_id"] == sample_message.agent_id
        assert data["sender"] == sample_message.sender
        assert data["content"] == sample_message.content
        assert "timestamp" in data


class TestWorkflowModel:
    """Tests for Workflow model."""

    def test_create_workflow(self, db_session):
        """Test creating a workflow."""
        workflow = Workflow(
            name="Test Workflow",
            description="A test workflow",
            status="pending",
            meta={"key": "value"},
        )
        db_session.add(workflow)
        db_session.commit()

        assert workflow.id is not None
        assert workflow.name == "Test Workflow"
        assert workflow.description == "A test workflow"
        assert workflow.status == "pending"
        assert workflow.meta == {"key": "value"}
        assert isinstance(workflow.started_at, datetime)

    def test_workflow_to_dict(self, sample_workflow):
        """Test workflow to_dict method."""
        data = sample_workflow.to_dict()

        assert data["id"] == sample_workflow.id
        assert data["name"] == sample_workflow.name
        assert data["description"] == sample_workflow.description
        assert data["status"] == sample_workflow.status
        assert "started_at" in data

    def test_workflow_relationships(self, db_session, sample_workflow):
        """Test workflow relationships with tasks."""
        task = Task(
            workflow_id=sample_workflow.id,
            assigned_to="test",
            status="pending",
            description="Test task",
        )
        db_session.add(task)
        db_session.commit()

        assert len(sample_workflow.tasks) == 1
        assert sample_workflow.tasks[0].description == "Test task"


class TestTaskModel:
    """Tests for Task model."""

    def test_create_task(self, db_session, sample_workflow):
        """Test creating a task."""
        task = Task(
            workflow_id=sample_workflow.id,
            assigned_to="driver",
            status="pending",
            description="Test the system",
        )
        db_session.add(task)
        db_session.commit()

        assert task.id is not None
        assert task.workflow_id == sample_workflow.id
        assert task.assigned_to == "driver"
        assert task.status == "pending"
        assert task.description == "Test the system"
        assert isinstance(task.created_at, datetime)

    def test_task_to_dict(self, sample_task):
        """Test task to_dict method."""
        data = sample_task.to_dict()

        assert data["id"] == sample_task.id
        assert data["workflow_id"] == sample_task.workflow_id
        assert data["assigned_to"] == sample_task.assigned_to
        assert data["status"] == sample_task.status
        assert data["description"] == sample_task.description
        assert "created_at" in data


