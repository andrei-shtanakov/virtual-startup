"""Generator Agent - HR Manager and Agent Creator.

The Generator agent creates and manages new specialized agents dynamically
based on requirements from the Driver or Creator agents.
"""

from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from autogen_ext.models.openai import OpenAIChatCompletionClient

from .base_agent import BaseVirtualAgent
from .config import AGENT_CONFIGS, get_model_client, DEFAULT_MODEL


class GeneratorAgent(BaseVirtualAgent):
    """Generator Agent - HR Manager and Agent Creator.

    This agent designs and creates new specialized agents.
    """

    def __init__(
        self,
        db_session: Optional[Session] = None,
        model_client: Optional[OpenAIChatCompletionClient] = None,
    ):
        """Initialize the Generator agent.

        Args:
            db_session: Database session for persistence
            model_client: Optional custom model client
        """
        config = AGENT_CONFIGS["generator"]

        if model_client is None:
            model_client = get_model_client(config["model"])

        super().__init__(
            name=config["name"],
            role=config["role"],
            agent_type=config["type"],
            system_message=config["system_message"],
            description=config["description"],
            model_client=model_client,
            db_session=db_session,
        )

        # Track created agents
        self.created_agents: Dict[str, Dict[str, Any]] = {}

    async def design_agent_spec(
        self,
        role: str,
        capabilities: list[str],
        requirements: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Design a specification for a new agent.

        Args:
            role: Role description for the agent
            capabilities: List of required capabilities
            requirements: Additional requirements

        Returns:
            Agent specification dictionary
        """
        prompt = (
            f"Design an agent specification for:\n"
            f"Role: {role}\n"
            f"Capabilities: {', '.join(capabilities)}\n"
        )

        if requirements:
            prompt += "\nAdditional Requirements:\n"
            for key, value in requirements.items():
                prompt += f"- {key}: {value}\n"

        prompt += (
            "\nProvide a detailed system prompt for this agent that includes:\n"
            "1. Clear role definition\n"
            "2. Key responsibilities\n"
            "3. Capabilities and limitations\n"
            "4. Communication style\n"
            "5. Success criteria"
        )

        system_prompt = await self.send_message(prompt)

        # Create agent specification
        spec: Dict[str, Any] = {
            "name": role.replace(" ", ""),
            "role": role,
            "type": "dynamic",
            "capabilities": capabilities,
            "system_message": system_prompt,
            "description": f"Specialized agent for {role.lower()}",
            "model": DEFAULT_MODEL,
            "tools": [],
        }

        # Add tool recommendations based on capabilities
        if "coding" in [c.lower() for c in capabilities]:
            spec["tools"].append("code_executor")
        if "research" in [c.lower() for c in capabilities]:
            spec["tools"].extend(["web_search", "rag_search"])

        return spec

    async def create_agent(self, spec: Dict[str, Any]) -> Optional[BaseVirtualAgent]:
        """Create a new agent from a specification.

        Args:
            spec: Agent specification dictionary

        Returns:
            New agent instance or None if creation fails
        """
        try:
            # Get model client
            model = spec.get("model", DEFAULT_MODEL)
            model_client = get_model_client(model)

            # Create the agent
            new_agent = BaseVirtualAgent(
                name=spec["name"],
                role=spec["role"],
                agent_type=spec["type"],
                system_message=spec["system_message"],
                description=spec["description"],
                model_client=model_client,
                db_session=self.db_session,
                tools=spec.get("tools", []),
            )

            # Register in database if session available
            if self.db_session:
                from app.models.agent import Agent
                from datetime import datetime

                agent_record = Agent(
                    name=spec["name"],
                    type=spec["type"],
                    role=spec["role"],
                    status="active",
                    config=spec,
                    created_at=datetime.utcnow(),
                )

                self.db_session.add(agent_record)
                self.db_session.commit()

                new_agent.set_db_id(agent_record.id)

            # Track the created agent
            self.created_agents[spec["name"]] = {
                "spec": spec,
                "agent": new_agent,
                "created_at": datetime.utcnow() if self.db_session else None,
            }

            self.log_message(
                content=f"Created new agent: {spec['name']} ({spec['role']})",
                sender=self.name,
                meta={"type": "agent_created", "spec": spec},
            )

            return new_agent

        except Exception as e:
            error_msg = f"Failed to create agent: {str(e)}"
            self.log_message(
                content=error_msg,
                sender=self.name,
                meta={"type": "error", "spec": spec, "error": str(e)},
            )
            return None

    async def create_agent_from_request(
        self, role: str, capabilities: list[str], reason: str
    ) -> Optional[BaseVirtualAgent]:
        """Create an agent from a high-level request.

        Args:
            role: Role description
            capabilities: Required capabilities
            reason: Why the agent is needed

        Returns:
            New agent instance or None if creation fails
        """
        # Design the specification
        spec = await self.design_agent_spec(
            role=role, capabilities=capabilities, requirements={"reason": reason}
        )

        # Create the agent
        return await self.create_agent(spec)

    def get_created_agents(self) -> list[Dict[str, Any]]:
        """Get list of all agents created by this Generator.

        Returns:
            List of created agent information
        """
        return [
            {
                "name": name,
                "role": info["spec"]["role"],
                "type": info["spec"]["type"],
                "created_at": str(info["created_at"]) if info["created_at"] else None,
            }
            for name, info in self.created_agents.items()
        ]

    def terminate_agent(self, agent_name: str) -> bool:
        """Terminate a dynamically created agent.

        Args:
            agent_name: Name of the agent to terminate

        Returns:
            True if successful, False otherwise
        """
        if agent_name not in self.created_agents:
            return False

        agent_info = self.created_agents[agent_name]
        agent = agent_info["agent"]

        # Update database status
        if self.db_session and agent.db_id:
            from app.models.agent import Agent

            agent_record = (
                self.db_session.query(Agent).filter_by(id=agent.db_id).first()
            )
            if agent_record:
                agent_record.status = "terminated"
                self.db_session.commit()

        # Remove from tracking
        del self.created_agents[agent_name]

        self.log_message(
            content=f"Terminated agent: {agent_name}",
            sender=self.name,
            meta={"type": "agent_terminated", "agent": agent_name},
        )

        return True

