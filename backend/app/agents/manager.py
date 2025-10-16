"""Agent Manager - Singleton for managing all agents in the system.

The Agent Manager is responsible for:
- Initializing core agents (Driver, Creator, Generator)
- Managing agent lifecycle
- Routing messages between agents
- Tracking agent status
"""

from typing import Any, Dict, Optional
from sqlalchemy.orm import Session

from .driver import DriverAgent
from .creator import CreatorAgent
from .generator import GeneratorAgent
from .base_agent import BaseVirtualAgent


class AgentManager:
    """Singleton manager for all agents in the system."""

    _instance: Optional["AgentManager"] = None

    def __new__(cls) -> "AgentManager":
        """Ensure only one instance of AgentManager exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the agent manager (only once)."""
        if self._initialized:
            return

        # Core agents
        self.driver: Optional[DriverAgent] = None
        self.creator: Optional[CreatorAgent] = None
        self.generator: Optional[GeneratorAgent] = None

        # Dynamic agents created by Generator
        self.dynamic_agents: Dict[str, BaseVirtualAgent] = {}

        # Database session
        self.db_session: Optional[Session] = None

        # RAG service (will be set later)
        self.rag_service: Optional[Any] = None

        self._initialized = True

    def set_db_session(self, session: Session) -> None:
        """Set the database session for all agents.

        Args:
            session: SQLAlchemy database session
        """
        self.db_session = session

        # Update existing agents
        if self.driver:
            self.driver.set_db_session(session)
        if self.creator:
            self.creator.set_db_session(session)
        if self.generator:
            self.generator.set_db_session(session)

        for agent in self.dynamic_agents.values():
            agent.set_db_session(session)

    def set_rag_service(self, rag_service: Any) -> None:
        """Set the RAG service for the Creator agent.

        Args:
            rag_service: RAG service instance
        """
        self.rag_service = rag_service
        if self.creator:
            self.creator.rag_service = rag_service

    async def initialize_core_agents(
        self, db_session: Optional[Session] = None
    ) -> Dict[str, str]:
        """Initialize the three core agents (Driver, Creator, Generator).

        Args:
            db_session: Optional database session

        Returns:
            Status dictionary with agent names and statuses
        """
        if db_session:
            self.db_session = db_session

        status = {}

        try:
            # Initialize Driver
            self.driver = DriverAgent(db_session=self.db_session)
            await self._sync_agent_with_db(self.driver, "driver")
            status["driver"] = "initialized"

            # Initialize Creator
            self.creator = CreatorAgent(
                db_session=self.db_session, rag_service=self.rag_service
            )
            await self._sync_agent_with_db(self.creator, "creator")
            status["creator"] = "initialized"

            # Initialize Generator
            self.generator = GeneratorAgent(db_session=self.db_session)
            await self._sync_agent_with_db(self.generator, "generator")
            status["generator"] = "initialized"

        except Exception as e:
            status["error"] = str(e)

        return status

    async def _sync_agent_with_db(
        self, agent: BaseVirtualAgent, agent_type: str
    ) -> None:
        """Sync agent with database record.

        Args:
            agent: Agent instance
            agent_type: Type of agent
        """
        if not self.db_session:
            return

        from app.models.agent import Agent

        # Check if agent already exists in database
        db_agent = (
            self.db_session.query(Agent)
            .filter_by(name=agent.name, type=agent_type)
            .first()
        )

        if db_agent:
            # Update status
            db_agent.status = "active"
            agent.set_db_id(db_agent.id)
        else:
            # Create new record
            from datetime import datetime

            db_agent = Agent(
                name=agent.name,
                type=agent_type,
                role=agent.role,
                status="active",
                config={},
                created_at=datetime.utcnow(),
            )
            self.db_session.add(db_agent)
            self.db_session.commit()
            agent.set_db_id(db_agent.id)

        self.db_session.commit()

    def get_agent(self, agent_id: int) -> Optional[BaseVirtualAgent]:
        """Get an agent by database ID.

        Args:
            agent_id: Database ID of the agent

        Returns:
            Agent instance or None
        """
        # Check core agents
        if self.driver and self.driver.db_id == agent_id:
            return self.driver
        if self.creator and self.creator.db_id == agent_id:
            return self.creator
        if self.generator and self.generator.db_id == agent_id:
            return self.generator

        # Check dynamic agents
        for agent in self.dynamic_agents.values():
            if agent.db_id == agent_id:
                return agent

        return None

    def get_agent_by_name(self, name: str) -> Optional[BaseVirtualAgent]:
        """Get an agent by name.

        Args:
            name: Agent name

        Returns:
            Agent instance or None
        """
        # Check core agents
        if self.driver and self.driver.name == name:
            return self.driver
        if self.creator and self.creator.name == name:
            return self.creator
        if self.generator and self.generator.name == name:
            return self.generator

        # Check dynamic agents
        return self.dynamic_agents.get(name)

    async def create_dynamic_agent(
        self, spec: Dict[str, Any]
    ) -> Optional[BaseVirtualAgent]:
        """Create a new dynamic agent through the Generator.

        Args:
            spec: Agent specification

        Returns:
            New agent instance or None
        """
        if not self.generator:
            return None

        new_agent = await self.generator.create_agent(spec)

        if new_agent:
            self.dynamic_agents[new_agent.name] = new_agent

        return new_agent

    def get_all_agents(self) -> list[Dict[str, Any]]:
        """Get information about all active agents.

        Returns:
            List of agent information dictionaries
        """
        agents = []

        if self.driver:
            agents.append(self.driver.to_dict())
        if self.creator:
            agents.append(self.creator.to_dict())
        if self.generator:
            agents.append(self.generator.to_dict())

        for agent in self.dynamic_agents.values():
            agents.append(agent.to_dict())

        return agents

    def terminate_agent(self, agent_id: int) -> bool:
        """Terminate a dynamic agent.

        Args:
            agent_id: Database ID of agent to terminate

        Returns:
            True if successful, False otherwise
        """
        # Cannot terminate core agents
        core_ids = []
        if self.driver:
            core_ids.append(self.driver.db_id)
        if self.creator:
            core_ids.append(self.creator.db_id)
        if self.generator:
            core_ids.append(self.generator.db_id)

        if agent_id in core_ids:
            return False

        # Find and terminate dynamic agent
        for name, agent in list(self.dynamic_agents.items()):
            if agent.db_id == agent_id:
                # Update database
                if self.db_session:
                    from app.models.agent import Agent

                    db_agent = (
                        self.db_session.query(Agent).filter_by(id=agent_id).first()
                    )
                    if db_agent:
                        db_agent.status = "terminated"
                        self.db_session.commit()

                # Remove from tracking
                del self.dynamic_agents[name]
                return True

        return False

    def get_agent_status(self, agent_id: int) -> Dict[str, Any]:
        """Get detailed status of an agent.

        Args:
            agent_id: Database ID of the agent

        Returns:
            Status information dictionary
        """
        agent = self.get_agent(agent_id)

        if not agent:
            return {"error": "Agent not found"}

        return {
            "id": agent.db_id,
            "name": agent.name,
            "role": agent.role,
            "type": agent.agent_type,
            "status": agent.status,
            "description": agent.description,
        }

    async def route_message(
        self, sender_id: int, recipient_name: str, message: str
    ) -> Optional[str]:
        """Route a message from one agent to another.

        Args:
            sender_id: Database ID of sender
            recipient_name: Name of recipient agent
            message: Message content

        Returns:
            Response from recipient or None
        """
        sender = self.get_agent(sender_id)
        recipient = self.get_agent_by_name(recipient_name)

        if not sender or not recipient:
            return None

        # Send message through recipient
        response = await recipient.send_message(message, sender)

        return response

    def shutdown(self) -> None:
        """Shutdown all agents and cleanup resources."""
        # Update all agents to idle status
        for agent in self.get_all_agents():
            if agent["id"]:
                agent_instance = self.get_agent(agent["id"])
                if agent_instance:
                    agent_instance.update_status("idle")

        # Clear agent references
        self.driver = None
        self.creator = None
        self.generator = None
        self.dynamic_agents.clear()


# Global singleton instance
agent_manager = AgentManager()
