"""Agent API routes."""

from flask import Blueprint, jsonify, request

from app.models import Agent
from app.services import get_agent_service
from app.utils.async_runner import run_async

bp = Blueprint("agents", __name__, url_prefix="/api/agents")


@bp.route("", methods=["GET"])
def get_agents() -> tuple[dict, int]:
    """Get all agents."""
    agent_service = get_agent_service()
    agents = agent_service.get_all_agents()
    return jsonify(agents), 200


@bp.route("/<int:agent_id>", methods=["GET"])
def get_agent(agent_id: int) -> tuple[dict, int]:
    """Get single agent by ID."""
    agent = Agent.query.get_or_404(agent_id)
    return jsonify(agent.to_dict()), 200


@bp.route("/<int:agent_id>/status", methods=["GET"])
def get_agent_status(agent_id: int) -> tuple[dict, int]:
    """Get agent status."""
    agent_service = get_agent_service()

    try:
        status = agent_service.get_agent_status(agent_id)
        return jsonify(status), 200
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503


@bp.route("/<int:agent_id>/messages", methods=["GET"])
def get_agent_messages(agent_id: int) -> tuple[dict, int]:
    """Get all messages for an agent."""
    agent = Agent.query.get_or_404(agent_id)

    limit = request.args.get("limit", 50, type=int)
    agent_service = get_agent_service()

    messages = agent_service.get_agent_conversation_history(agent.id, limit=limit)
    return jsonify(messages), 200


@bp.route("/<int:agent_id>/message", methods=["POST"])
def send_message_to_agent(agent_id: int) -> tuple[dict, int]:
    """Send message to an agent and get response."""
    agent = Agent.query.get_or_404(agent_id)
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Message content required"}), 400

    # Get agent service
    agent_service = get_agent_service()

    try:
        result = run_async(
            agent_service.send_message_to_agent, agent.id, data["message"]
        )

        if result.get("success"):
            return (
                jsonify(
                    {
                        "message": data["message"],
                        "response": result.get("response"),
                        "agent_id": agent.id,
                        "agent_name": result.get("agent_name"),
                        "status": result.get("status"),
                    }
                ),
                200,
            )
        else:
            return jsonify({"error": result.get("error")}), 500

    except RuntimeError as e:
        # Agent system not initialized
        return jsonify({"error": str(e), "hint": "Call /api/init first"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/task", methods=["POST"])
def send_task_to_driver() -> tuple[dict, int]:
    """Send a task to the Driver agent."""
    data = request.get_json()

    if not data or "task" not in data:
        return jsonify({"error": "Task content required"}), 400

    agent_service = get_agent_service()

    try:
        result = run_async(
            agent_service.process_operator_task,
            data["task"],
            data.get("workflow_id"),
        )

        if result.get("success"):
            return jsonify(result), 200
        else:
            return jsonify({"error": result.get("error")}), 500

    except RuntimeError as e:
        return jsonify({"error": str(e), "hint": "Call /api/init first"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/create", methods=["POST"])
def create_dynamic_agent() -> tuple[dict, int]:
    """Create a new dynamic agent."""
    data = request.get_json()

    required_fields = ["role", "capabilities", "reason"]
    if not data or not all(field in data for field in required_fields):
        return (
            jsonify({"error": f"Required fields: {', '.join(required_fields)}"}),
            400,
        )

    agent_service = get_agent_service()

    try:
        result = run_async(
            agent_service.create_dynamic_agent,
            data["role"],
            data["capabilities"],
            data["reason"],
        )

        if result.get("success"):
            return jsonify(result), 201
        else:
            return jsonify({"error": result.get("error")}), 500

    except RuntimeError as e:
        return jsonify({"error": str(e), "hint": "Call /api/init first"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500
