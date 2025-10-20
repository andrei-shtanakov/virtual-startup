"""Service for coordinating agent operations with Flask app.

This service provides a bridge between the Flask app (API/WebSocket)
and the agent system (AutoGen agents managed by AgentManager).
"""

import asyncio
from typing import Any, Dict, Optional

from app import db
from app.models import Agent, Message
from app.agents import agent_manager
from app.services import get_rag_service


class AgentService:
    """Service for agent operations in the Flask context."""

    def __init__(self):
        """Initialize the agent service."""
        self.initialized = False
        self._init_task: Optional[asyncio.Task] = None

    async def initialize(self) -> Dict[str, str]:
        """Initialize the agent system.

        Returns:
            Status dictionary with initialization results
        """
        if self.initialized:
            return {"status": "already_initialized"}

        try:
            # Initialize RAG service
            rag_service = get_rag_service()

            # Initialize with sample data if empty
            if rag_service.count_documents() == 0:
                rag_service.initialize_sample_data()

            # Set RAG service for agent manager
            agent_manager.set_rag_service(rag_service)

            # Set database session
            agent_manager.set_db_session(db.session)

            # Initialize core agents
            status = await agent_manager.initialize_core_agents(db.session)

            self.initialized = True
            return status

        except Exception as e:
            return {"status": "error", "error": str(e)}

    def ensure_initialized(self) -> None:
        """Ensure agent system is initialized.

        Raises:
            RuntimeError: If agent system is not initialized
        """
        if not self.initialized:
            raise RuntimeError("Agent system not initialized. Call initialize() first.")

    async def send_message_to_agent(
        self, agent_id: int, message_content: str
    ) -> Dict[str, Any]:
        """Send a message to an agent and get response.

        Args:
            agent_id: Database ID of the agent
            message_content: Message to send

        Returns:
            Dictionary with response and metadata
        """
        self.ensure_initialized()

        # Get agent instance from manager
        agent_instance = agent_manager.get_agent(agent_id)

        if not agent_instance:
            return {"error": "Agent not found", "agent_id": agent_id}

        try:
            # Send message and get response
            response = await agent_instance.send_message(message_content)

            return {
                "success": True,
                "agent_id": agent_id,
                "agent_name": agent_instance.name,
                "response": response,
                "status": agent_instance.status,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent_id": agent_id,
            }

    def get_agent_status(self, agent_id: int) -> Dict[str, Any]:
        """Get current status of an agent.

        Args:
            agent_id: Database ID of the agent

        Returns:
            Agent status information
        """
        self.ensure_initialized()
        return agent_manager.get_agent_status(agent_id)

    def get_all_agents(self) -> list[Dict[str, Any]]:
        """Get all active agents.

        Returns:
            List of agent information dictionaries
        """
        if not self.initialized:
            # Return from database if agent system not initialized
            agents = Agent.query.all()
            return [agent.to_dict() for agent in agents]

        # Return from agent manager if initialized
        return agent_manager.get_all_agents()

    def get_agent_conversation_history(
        self, agent_id: int, limit: int = 50
    ) -> list[Dict[str, Any]]:
        """Get conversation history for an agent.

        Args:
            agent_id: Database ID of the agent
            limit: Maximum number of messages to return

        Returns:
            List of message dictionaries
        """
        # Get from database
        messages = (
            Message.query.filter_by(agent_id=agent_id)
            .order_by(Message.timestamp.desc())
            .limit(limit)
            .all()
        )

        return [msg.to_dict() for msg in reversed(messages)]

    async def process_operator_task(
        self, task: str, workflow_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Process a task from the operator using the Driver agent.

        Args:
            task: Task description
            workflow_id: Optional workflow ID to associate

        Returns:
            Response from Driver agent
        """
        self.ensure_initialized()

        if not agent_manager.driver:
            return {"error": "Driver agent not available"}

        try:
            response = await agent_manager.driver.process_operator_task(
                task, workflow_id
            )

            return {
                "success": True,
                "agent": "Driver",
                "response": response,
                "workflow_id": workflow_id,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def create_dynamic_agent(
        self, role: str, capabilities: list[str], reason: str
    ) -> Dict[str, Any]:
        """Create a new dynamic agent via the Generator.

        Args:
            role: Role for the new agent
            capabilities: List of capabilities
            reason: Reason for creating the agent

        Returns:
            Information about the created agent
        """
        self.ensure_initialized()

        if not agent_manager.generator:
            return {"error": "Generator agent not available"}

        try:
            new_agent = await agent_manager.generator.create_agent_from_request(
                role=role, capabilities=capabilities, reason=reason
            )

            if new_agent:
                agent_manager.dynamic_agents[new_agent.name] = new_agent
                return {
                    "success": True,
                    "agent": new_agent.to_dict(),
                    "message": f"Created agent: {new_agent.name}",
                }
            else:
                return {"success": False, "error": "Failed to create agent"}

        except Exception as e:
            return {"success": False, "error": str(e)}


# Global agent service instance
_agent_service: Optional[AgentService] = None


def get_agent_service() -> AgentService:
    """Get or create the global agent service instance.

    Returns:
        AgentService instance
    """
    global _agent_service

    if _agent_service is None:
        _agent_service = AgentService()

    return _agent_service

