"""Statistics API routes."""

from flask import Blueprint, jsonify

from app.models import Agent, Workflow

bp = Blueprint("stats", __name__, url_prefix="/api/stats")


@bp.route("/agents", methods=["GET"])
def get_agent_stats() -> tuple[dict, int]:
    """Get agent statistics."""
    total = Agent.query.count()
    active = Agent.query.filter_by(status="working").count()
    idle = Agent.query.filter_by(status="idle").count()

    return jsonify({"total": total, "active": active, "idle": idle}), 200


@bp.route("/workflows", methods=["GET"])
def get_workflow_stats() -> tuple[dict, int]:
    """Get workflow statistics."""
    total = Workflow.query.count()
    active = Workflow.query.filter_by(status="active").count()
    completed = Workflow.query.filter_by(status="completed").count()
    failed = Workflow.query.filter_by(status="failed").count()

    return jsonify(
        {"total": total, "active": active, "completed": completed, "failed": failed}
    ), 200


@bp.route("/overview", methods=["GET"])
def get_overview() -> tuple[dict, int]:
    """Get system overview."""
    agents = {
        "total": Agent.query.count(),
        "active": Agent.query.filter_by(status="working").count(),
        "idle": Agent.query.filter_by(status="idle").count(),
    }

    workflows = {
        "total": Workflow.query.count(),
        "active": Workflow.query.filter_by(status="active").count(),
        "completed": Workflow.query.filter_by(status="completed").count(),
    }

    return jsonify({"agents": agents, "workflows": workflows, "status": "online"}), 200


