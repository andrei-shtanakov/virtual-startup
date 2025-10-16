"""Workflow API routes."""

from flask import Blueprint, jsonify, request

from app import db
from app.models import Workflow, Task
from app.services import get_workflow_orchestrator

bp = Blueprint("workflows", __name__, url_prefix="/api/workflows")


@bp.route("", methods=["GET"])
def get_workflows() -> tuple[dict, int]:
    """Get all workflows."""
    workflows = Workflow.query.all()
    return jsonify([wf.to_dict() for wf in workflows]), 200


@bp.route("/<int:workflow_id>", methods=["GET"])
def get_workflow(workflow_id: int) -> tuple[dict, int]:
    """Get single workflow by ID."""
    workflow = Workflow.query.get_or_404(workflow_id)
    return jsonify(workflow.to_dict()), 200


@bp.route("", methods=["POST"])
def create_workflow() -> tuple[dict, int]:
    """Create a new workflow."""
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Workflow name required"}), 400

    workflow = Workflow(
        name=data["name"],
        description=data.get("description"),
        meta=data.get("meta"),
    )
    db.session.add(workflow)
    db.session.commit()

    return jsonify(workflow.to_dict()), 201


@bp.route("/<int:workflow_id>/status", methods=["GET"])
def get_workflow_status(workflow_id: int) -> tuple[dict, int]:
    """Get workflow status with tasks."""
    workflow = Workflow.query.get_or_404(workflow_id)
    tasks = [task.to_dict() for task in workflow.tasks]

    return jsonify({"workflow": workflow.to_dict(), "tasks": tasks}), 200


@bp.route("/execute", methods=["POST"])
def execute_workflow() -> tuple[dict, int]:
    """Execute a complete end-to-end workflow."""
    data = request.get_json()

    if not data or "task" not in data:
        return jsonify({"error": "Task description required"}), 400

    orchestrator = get_workflow_orchestrator()

    try:
        result = orchestrator.execute_complete_workflow(data["task"])
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/<int:workflow_id>/start", methods=["POST"])
def start_workflow(workflow_id: int) -> tuple[dict, int]:
    """Start a workflow with an initial message."""
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Message required"}), 400

    orchestrator = get_workflow_orchestrator()

    try:
        result = orchestrator.start_workflow(workflow_id, data["message"])
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
