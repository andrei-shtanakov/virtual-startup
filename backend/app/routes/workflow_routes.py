"""Workflow API routes."""

from flask import Blueprint, jsonify, request

from app import db
from app.models import Workflow

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
