"""Base agent class for the virtual startup system.

This module provides the base class for all agents, handling common functionality
like message logging, database integration, and communication with the AutoGen framework.
"""

from typing import Any, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient


class BaseVirtualAgent:
    """Base class for all virtual startup agents.

    This class wraps AutoGen's AssistantAgent and adds database integration,
    message logging, and status management.
    """

    def __init__(
        self,
        name: str,
        role: str,
        agent_type: str,
        system_message: str,
        description: str,
        model_client: OpenAIChatCompletionClient,
        db_session: Optional[Session] = None,
        tools: Optional[list] = None,
    ):
        """Initialize a base virtual agent.

        Args:
            name: Agent name
            role: Agent role (e.g., 'CEO', 'Researcher')
            agent_type: Type of agent ('driver', 'creator', 'generator', 'dynamic')
            system_message: System prompt for the agent
            description: Description of the agent's capabilities
            model_client: OpenAI model client for LLM interaction
            db_session: Database session for persistence
            tools: Optional list of tools for the agent
        """
        self.name = name
        self.role = role
        self.agent_type = agent_type
        self.description = description
        self.db_session = db_session

        # Create the underlying AutoGen agent
        self.agent = AssistantAgent(
            name=name,
            model_client=model_client,
            system_message=system_message,
            description=description,
            tools=tools or [],
        )

        # Agent state
        self.status = "idle"  # idle, busy, error
        self.db_id: Optional[int] = None

    def set_db_session(self, session: Session) -> None:
        """Set the database session for this agent."""
        self.db_session = session

    def set_db_id(self, agent_id: int) -> None:
        """Set the database ID for this agent."""
        self.db_id = agent_id

    def update_status(self, status: str) -> None:
        """Update agent status in memory and database.

        Args:
            status: New status ('idle', 'busy', 'error')
        """
        self.status = status

        if self.db_session and self.db_id:
            from app.models.agent import Agent

            agent_record = self.db_session.query(Agent).filter_by(id=self.db_id).first()
            if agent_record:
                agent_record.status = status
                self.db_session.commit()

    def log_message(
        self, content: str, sender: str, meta: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log a message to the database.

        Args:
            content: Message content
            sender: Who sent the message (agent name or 'user')
            meta: Additional metadata for the message
        """
        if not self.db_session or not self.db_id:
            return

        from app.models.message import Message

        message = Message(
            agent_id=self.db_id,
            sender=sender,
            content=content,
            timestamp=datetime.utcnow(),
            meta=meta or {},
        )
        self.db_session.add(message)
        self.db_session.commit()

    async def send_message(
        self, content: str, recipient: Optional["BaseVirtualAgent"] = None
    ) -> str:
        """Send a message to another agent or process internally.

        Args:
            content: Message to send
            recipient: Target agent (None for internal processing)

        Returns:
            Response from the agent
        """
        self.update_status("busy")

        # Log the incoming message
        self.log_message(
            content=content,
            sender="system" if not recipient else recipient.name,
            meta={"type": "incoming"},
        )

        try:
            # Process with AutoGen agent
            from autogen_agentchat.messages import TextMessage

            response = await self.agent.on_messages(
                [TextMessage(content=content, source="user")],
                None,  # cancellation_token
            )

            response_content = str(response.chat_message.content)

            # Log the response
            self.log_message(
                content=response_content, sender=self.name, meta={"type": "outgoing"}
            )

            self.update_status("idle")
            return response_content

        except Exception as e:
            self.update_status("error")
            error_msg = f"Error processing message: {str(e)}"
            self.log_message(
                content=error_msg,
                sender=self.name,
                meta={"type": "error", "error": str(e)},
            )
            return error_msg

    def get_conversation_history(self, limit: int = 50) -> list[Dict[str, Any]]:
        """Get recent conversation history from database.

        Args:
            limit: Maximum number of messages to retrieve

        Returns:
            List of message dictionaries
        """
        if not self.db_session or not self.db_id:
            return []

        from app.models.message import Message

        messages = (
            self.db_session.query(Message)
            .filter_by(agent_id=self.db_id)
            .order_by(Message.timestamp.desc())
            .limit(limit)
            .all()
        )

        return [msg.to_dict() for msg in reversed(messages)]

    def to_dict(self) -> Dict[str, Any]:
        """Convert agent to dictionary representation.

        Returns:
            Dictionary with agent information
        """
        return {
            "id": self.db_id,
            "name": self.name,
            "role": self.role,
            "type": self.agent_type,
            "status": self.status,
            "description": self.description,
        }

