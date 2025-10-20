"""
Pytest configuration and fixtures for testing.
"""

import pytest
import sys
from unittest.mock import MagicMock

# Mock autogen and chromadb modules to avoid import errors during testing
mock_autogen_ext = MagicMock()
mock_autogen_core = MagicMock()
mock_chromadb = MagicMock()

# Comprehensive mocking of autogen modules
sys.modules['autogen_ext'] = mock_autogen_ext
sys.modules['autogen_ext.models'] = MagicMock()
sys.modules['autogen_ext.models.openai'] = MagicMock()
sys.modules['autogen_core'] = mock_autogen_core
sys.modules['autogen_core.models'] = MagicMock()
sys.modules['autogen_core.memory'] = MagicMock()
sys.modules['autogen_core.base'] = MagicMock()
sys.modules['autogen_agentchat'] = MagicMock()
sys.modules['autogen_agentchat.agents'] = MagicMock()

# Mock chromadb
sys.modules['chromadb'] = mock_chromadb
sys.modules['chromadb.config'] = MagicMock()
sys.modules['chromadb.utils'] = MagicMock()
sys.modules['chromadb.utils.embedding_functions'] = MagicMock()

from app import create_app, db
from app.models import Agent, Message, Workflow, Task
from config import TestingConfig


@pytest.fixture(scope="function")
def app():
    """Create application for testing."""
    # Create app with testing config
    app_instance = create_app("testing")
    
    with app_instance.app_context():
        db.create_all()
        yield app_instance
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture(scope="function")
def db_session(app):
    """Create database session for testing."""
    with app.app_context():
        yield db.session


@pytest.fixture(scope="function")
def sample_agent(db_session):
    """Create a sample agent for testing."""
    agent = Agent(
        name="Test Agent",
        type="test",
        role="Tester",
        status="idle",
        config={"model": "gpt-4", "temperature": 0.7},
    )
    db_session.add(agent)
    db_session.commit()
    return agent


@pytest.fixture(scope="function")
def sample_workflow(db_session):
    """Create a sample workflow for testing."""
    workflow = Workflow(
        name="Test Workflow",
        description="A test workflow",
        status="pending",
        meta={"test": True},
    )
    db_session.add(workflow)
    db_session.commit()
    return workflow


@pytest.fixture(scope="function")
def sample_task(db_session, sample_workflow, sample_agent):
    """Create a sample task for testing."""
    task = Task(
        workflow_id=sample_workflow.id,
        assigned_to=sample_agent.id,
        status="pending",
        description="Test task",
    )
    db_session.add(task)
    db_session.commit()
    return task


@pytest.fixture(scope="function")
def sample_message(db_session, sample_agent):
    """Create a sample message for testing."""
    message = Message(
        agent_id=sample_agent.id,
        sender="user",
        content="Test message",
    )
    db_session.add(message)
    db_session.commit()
    return message
