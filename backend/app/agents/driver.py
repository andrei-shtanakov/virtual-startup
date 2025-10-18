"""Driver Agent - CEO and Task Orchestrator.

The Driver agent is the main orchestrator that receives tasks from the operator,
breaks them down, and delegates to other agents.
"""

from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from autogen_ext.models.openai import OpenAIChatCompletionClient

from .base_agent import BaseVirtualAgent
from .config import AGENT_CONFIGS, get_model_client


class DriverAgent(BaseVirtualAgent):
    """Driver Agent - CEO of the virtual startup.

    This agent orchestrates tasks, delegates work, and monitors progress.
    """

    def __init__(
        self,
        db_session: Optional[Session] = None,
        model_client: Optional[OpenAIChatCompletionClient] = None,
    ):
        """Initialize the Driver agent.

        Args:
            db_session: Database session for persistence
            model_client: Optional custom model client
        """
        config = AGENT_CONFIGS["driver"]

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

        # Track active workflows
        self.active_workflows: Dict[int, Dict[str, Any]] = {}

    async def process_operator_task(
        self, task: str, workflow_id: Optional[int] = None
    ) -> str:
        """Process a task from the operator.

        Args:
            task: Task description from operator
            workflow_id: Optional workflow ID to associate with

        Returns:
            Response from the Driver agent
        """
        context = f"New task from operator: {task}"

        if workflow_id:
            context += f"\nWorkflow ID: {workflow_id}"
            self.active_workflows[workflow_id] = {"status": "in_progress", "task": task}

        response = await self.send_message(context)
        return response

    async def delegate_to_creator(
        self, task: str, context: Optional[str] = None
    ) -> str:
        """Delegate a research or ideation task to the Creator agent.

        Args:
            task: Task to delegate
            context: Additional context for the task

        Returns:
            Delegation message
        """
        delegation = f"DELEGATION TO CREATOR:\nTask: {task}"
        if context:
            delegation += f"\nContext: {context}"

        self.log_message(
            content=delegation,
            sender=self.name,
            meta={"type": "delegation", "target": "creator"},
        )

        return delegation

    async def request_new_agent(
        self, role: str, capabilities: list[str], reason: str
    ) -> str:
        """Request a new specialized agent from the Generator.

        Args:
            role: Role description for the new agent
            capabilities: List of required capabilities
            reason: Why this agent is needed

        Returns:
            Request message for Generator
        """
        request = (
            f"REQUEST TO GENERATOR:\n"
            f"Role: {role}\n"
            f"Capabilities: {', '.join(capabilities)}\n"
            f"Reason: {reason}\n"
        )

        self.log_message(
            content=request,
            sender=self.name,
            meta={
                "type": "agent_request",
                "target": "generator",
                "role": role,
                "capabilities": capabilities,
            },
        )

        return request

    async def monitor_workflow(self, workflow_id: int) -> Dict[str, Any]:
        """Monitor the status of a workflow.

        Args:
            workflow_id: ID of the workflow to monitor

        Returns:
            Workflow status information
        """
        if workflow_id in self.active_workflows:
            return self.active_workflows[workflow_id]

        if self.db_session:
            from app.models.workflow import Workflow

            workflow = self.db_session.query(Workflow).filter_by(id=workflow_id).first()

            if workflow:
                return workflow.to_dict()

        return {"status": "not_found"}

    def update_workflow_status(
        self, workflow_id: int, status: str, notes: Optional[str] = None
    ) -> None:
        """Update workflow status.

        Args:
            workflow_id: Workflow ID
            status: New status
            notes: Optional status notes
        """
        if workflow_id in self.active_workflows:
            self.active_workflows[workflow_id]["status"] = status
            if notes:
                self.active_workflows[workflow_id]["notes"] = notes

        if self.db_session:
            from app.models.workflow import Workflow
            from datetime import datetime

            workflow = self.db_session.query(Workflow).filter_by(id=workflow_id).first()

            if workflow:
                workflow.status = status
                if status == "completed":
                    workflow.completed_at = datetime.utcnow()
                self.db_session.commit()

