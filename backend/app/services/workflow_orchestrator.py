"""
Workflow Orchestration Service

Manages end-to-end workflows where agents collaborate:
1. Operator sends task to Driver
2. Driver analyzes and delegates to Creator
3. Creator researches using RAG
4. Creator requests specialist from Generator
5. Generator creates new agent
6. New agent performs task
7. Results flow back to Driver
8. Driver reports to Operator
"""

from datetime import datetime
from typing import Dict, Any, Optional, List
from flask_socketio import emit
from app import db, socketio
from app.models import Workflow, Task, Agent, Message
from app.services.agent_service import get_agent_service
import json


class WorkflowOrchestrator:
    """Singleton workflow orchestrator"""

    _instance: Optional["WorkflowOrchestrator"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.agent_service = get_agent_service()
        self.active_workflows: Dict[int, Dict[str, Any]] = {}

    def create_workflow(
        self, name: str, description: str, initial_task: str
    ) -> Workflow:
        """Create a new workflow"""
        workflow = Workflow(
            name=name,
            description=description,
            status="pending",
            started_at=datetime.utcnow(),
            meta={"initial_task": initial_task},
        )
        db.session.add(workflow)
        db.session.commit()

        # Emit workflow created event
        self._emit_workflow_update(workflow.id, "created")

        return workflow

    def start_workflow(self, workflow_id: int, initial_message: str) -> Dict[str, Any]:
        """
        Start a workflow with an initial task

        Workflow steps:
        1. Send task to Driver
        2. Driver analyzes task
        3. Driver delegates to appropriate agents
        4. Agents collaborate
        5. Results aggregated and returned
        """
        workflow = Workflow.query.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")

        if workflow.status != "pending":
            raise ValueError(f"Workflow {workflow_id} is not pending")

        # Update workflow status
        workflow.status = "in_progress"
        workflow.started_at = datetime.utcnow()
        db.session.commit()

        # Store workflow context
        self.active_workflows[workflow_id] = {
            "steps": [],
            "current_step": 0,
            "results": {},
        }

        # Create initial task
        task = Task(
            workflow_id=workflow_id,
            assigned_to="driver",
            status="pending",
            description=initial_message,
        )
        db.session.add(task)
        db.session.commit()

        # Emit workflow started
        self._emit_workflow_update(workflow_id, "started")

        # Execute workflow
        try:
            result = self._execute_workflow_step(workflow_id, task.id, initial_message)
            return {
                "workflow_id": workflow_id,
                "status": "in_progress",
                "message": "Workflow started",
                "result": result,
            }
        except Exception as e:
            workflow.status = "failed"
            workflow.completed_at = datetime.utcnow()
            db.session.commit()
            self._emit_workflow_update(workflow_id, "failed")
            raise e

    def _execute_workflow_step(
        self, workflow_id: int, task_id: int, message: str
    ) -> Dict[str, Any]:
        """Execute a single workflow step"""
        task = Task.query.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        # Update task status
        task.status = "in_progress"
        db.session.commit()

        # Get agent for this task
        agent = Agent.query.filter_by(type=task.assigned_to).first()
        if not agent:
            raise ValueError(f"Agent {task.assigned_to} not found")

        # Record step
        if workflow_id in self.active_workflows:
            self.active_workflows[workflow_id]["steps"].append(
                {
                    "task_id": task_id,
                    "agent": task.assigned_to,
                    "message": message,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )

        # Send message to agent (async)
        response = self.agent_service.send_message(agent.id, message)

        # Create message record
        msg = Message(
            agent_id=agent.id,
            sender="system",
            content=f"Workflow task: {message}",
            timestamp=datetime.utcnow(),
        )
        db.session.add(msg)

        response_msg = Message(
            agent_id=agent.id,
            sender=agent.name,
            content=response.get("response", "No response"),
            timestamp=datetime.utcnow(),
        )
        db.session.add(response_msg)

        # Update task
        task.status = "completed"
        task.completed_at = datetime.utcnow()
        db.session.commit()

        # Emit task update
        self._emit_task_update(task_id, "completed")

        return {
            "task_id": task_id,
            "agent": task.assigned_to,
            "response": response.get("response"),
        }

    def complete_workflow(self, workflow_id: int) -> None:
        """Mark workflow as completed"""
        workflow = Workflow.query.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")

        workflow.status = "completed"
        workflow.completed_at = datetime.utcnow()
        db.session.commit()

        # Clean up active workflow
        if workflow_id in self.active_workflows:
            del self.active_workflows[workflow_id]

        self._emit_workflow_update(workflow_id, "completed")

    def fail_workflow(self, workflow_id: int, error: str) -> None:
        """Mark workflow as failed"""
        workflow = Workflow.query.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")

        workflow.status = "failed"
        workflow.completed_at = datetime.utcnow()
        workflow.meta = {**(workflow.meta or {}), "error": error}
        db.session.commit()

        # Clean up active workflow
        if workflow_id in self.active_workflows:
            del self.active_workflows[workflow_id]

        self._emit_workflow_update(workflow_id, "failed")

    def get_workflow_status(self, workflow_id: int) -> Dict[str, Any]:
        """Get current workflow status"""
        workflow = Workflow.query.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")

        tasks = Task.query.filter_by(workflow_id=workflow_id).all()

        return {
            "workflow": workflow.to_dict(),
            "tasks": [task.to_dict() for task in tasks],
            "active": workflow_id in self.active_workflows,
            "context": self.active_workflows.get(workflow_id, {}),
        }

    def execute_complete_workflow(
        self, task_description: str
    ) -> Dict[str, Any]:
        """
        Execute a complete end-to-end workflow demonstration

        Steps:
        1. Create workflow
        2. Send to Driver (CEO)
        3. Driver delegates to Creator (Researcher)
        4. Creator researches
        5. Creator requests specialist from Generator (HR)
        6. Generator designs new agent
        7. Results aggregated
        """
        # Create workflow
        workflow = self.create_workflow(
            name=f"Workflow: {task_description[:50]}",
            description=task_description,
            initial_task=task_description,
        )

        try:
            # Step 1: Send to Driver
            driver_task = Task(
                workflow_id=workflow.id,
                assigned_to="driver",
                status="pending",
                description=f"Coordinate: {task_description}",
            )
            db.session.add(driver_task)
            db.session.commit()

            driver_result = self._execute_workflow_step(
                workflow.id, driver_task.id, task_description
            )

            # Step 2: Driver delegates to Creator for research
            creator_task = Task(
                workflow_id=workflow.id,
                assigned_to="creator",
                status="pending",
                description=f"Research: {task_description}",
            )
            db.session.add(creator_task)
            db.session.commit()

            creator_result = self._execute_workflow_step(
                workflow.id,
                creator_task.id,
                f"Research the following topic: {task_description}",
            )

            # Step 3: Request specialist from Generator
            generator_task = Task(
                workflow_id=workflow.id,
                assigned_to="generator",
                status="pending",
                description=f"Create specialist for: {task_description}",
            )
            db.session.add(generator_task)
            db.session.commit()

            generator_result = self._execute_workflow_step(
                workflow.id,
                generator_task.id,
                f"Design a specialist agent for: {task_description}",
            )

            # Complete workflow
            self.complete_workflow(workflow.id)

            return {
                "workflow_id": workflow.id,
                "status": "completed",
                "steps": [
                    {"step": 1, "agent": "driver", "result": driver_result},
                    {"step": 2, "agent": "creator", "result": creator_result},
                    {"step": 3, "agent": "generator", "result": generator_result},
                ],
            }

        except Exception as e:
            self.fail_workflow(workflow.id, str(e))
            raise e

    def _emit_workflow_update(self, workflow_id: int, event: str) -> None:
        """Emit workflow update via WebSocket"""
        workflow = Workflow.query.get(workflow_id)
        if workflow:
            socketio.emit(
                "workflow_update",
                {
                    "workflow_id": workflow_id,
                    "event": event,
                    "workflow": workflow.to_dict(),
                },
            )

    def _emit_task_update(self, task_id: int, event: str) -> None:
        """Emit task update via WebSocket"""
        task = Task.query.get(task_id)
        if task:
            socketio.emit(
                "task_update",
                {"task_id": task_id, "event": event, "task": task.to_dict()},
            )


# Singleton instance
_orchestrator_instance: Optional[WorkflowOrchestrator] = None


def get_workflow_orchestrator() -> WorkflowOrchestrator:
    """Get the workflow orchestrator singleton"""
    global _orchestrator_instance
    if _orchestrator_instance is None:
        _orchestrator_instance = WorkflowOrchestrator()
    return _orchestrator_instance

