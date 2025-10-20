"""Creator Agent - Researcher and Idea Generator.

The Creator agent handles research, ideation, and creative problem-solving
using RAG, web search, and other tools.
"""

from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from autogen_ext.models.openai import OpenAIChatCompletionClient

from .base_agent import BaseVirtualAgent
from .config import AGENT_CONFIGS, get_model_client


class CreatorAgent(BaseVirtualAgent):
    """Creator Agent - Researcher and Idea Generator.

    This agent performs research, generates ideas, and provides insights.
    """

    def __init__(
        self,
        db_session: Optional[Session] = None,
        model_client: Optional[OpenAIChatCompletionClient] = None,
        rag_service: Optional[Any] = None,
    ):
        """Initialize the Creator agent.

        Args:
            db_session: Database session for persistence
            model_client: Optional custom model client
            rag_service: Optional RAG service for knowledge base search
        """
        config = AGENT_CONFIGS["creator"]

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

        # Optional RAG service for research
        self.rag_service = rag_service

        # Research cache
        self.research_cache: Dict[str, Any] = {}

    async def research_topic(
        self, topic: str, use_rag: bool = True, use_web: bool = False
    ) -> Dict[str, Any]:
        """Research a topic using available tools.

        Args:
            topic: Topic to research
            use_rag: Whether to use RAG/vector search
            use_web: Whether to use web search

        Returns:
            Research results
        """
        results: Dict[str, Any] = {"topic": topic, "sources": [], "summary": ""}

        # Check cache first
        if topic in self.research_cache:
            return self.research_cache[topic]

        # Use RAG if available
        if use_rag and self.rag_service:
            try:
                rag_results = await self.rag_service.search(topic, k=5)
                results["sources"].extend(
                    [{"type": "rag", "content": r} for r in rag_results]
                )
            except Exception as e:
                self.log_message(
                    content=f"RAG search error: {str(e)}",
                    sender=self.name,
                    meta={"type": "error", "tool": "rag"},
                )

        # Process with LLM for summary
        context = (
            f"Research topic: {topic}\n\n"
            f"Sources found: {len(results['sources'])}\n"
            "Please provide a comprehensive summary of this topic."
        )

        summary = await self.send_message(context)
        results["summary"] = summary

        # Cache the results
        self.research_cache[topic] = results

        return results

    async def generate_ideas(
        self, context: str, constraints: Optional[Dict[str, Any]] = None
    ) -> list[str]:
        """Generate creative ideas based on context.

        Args:
            context: Context for idea generation
            constraints: Optional constraints (budget, time, tech stack, etc.)

        Returns:
            List of generated ideas
        """
        prompt = f"Generate creative ideas for:\n{context}\n"

        if constraints:
            prompt += "\nConstraints:\n"
            for key, value in constraints.items():
                prompt += f"- {key}: {value}\n"

        prompt += "\nProvide 3-5 innovative and practical ideas."

        response = await self.send_message(prompt)

        # Parse ideas from response (simplified)
        # In production, you might want more structured output
        ideas = [
            line.strip("- ").strip()
            for line in response.split("\n")
            if line.strip().startswith("-") or line.strip().startswith("•")
        ]

        return ideas if ideas else [response]

    async def request_specialist(
        self, role: str, reason: str, capabilities: Optional[list[str]] = None
    ) -> str:
        """Request a specialized agent from the Generator.

        Args:
            role: Role for the specialist agent
            reason: Why this specialist is needed
            capabilities: Optional specific capabilities needed

        Returns:
            Request message
        """
        request = f"AGENT REQUEST:\nRole: {role}\nReason: {reason}\n"

        if capabilities:
            request += f"Capabilities: {', '.join(capabilities)}\n"

        self.log_message(
            content=request,
            sender=self.name,
            meta={
                "type": "agent_request",
                "role": role,
                "capabilities": capabilities or [],
            },
        )

        return request

    def clear_cache(self) -> None:
        """Clear the research cache."""
        self.research_cache.clear()
        self.log_message(
            content="Research cache cleared", sender=self.name, meta={"type": "system"}
        )


