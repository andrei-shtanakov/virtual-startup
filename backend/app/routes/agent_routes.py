"""Agent API routes."""

from flask import Blueprint, jsonify, request

from app import db
from app.models import Agent, Message

bp = Blueprint("agents", __name__, url_prefix="/api/agents")


@bp.route("", methods=["GET"])
def get_agents() -> tuple[dict, int]:
    """Get all agents."""
    agents = Agent.query.all()
    return jsonify([agent.to_dict() for agent in agents]), 200


@bp.route("/<int:agent_id>", methods=["GET"])
def get_agent(agent_id: int) -> tuple[dict, int]:
    """Get single agent by ID."""
    agent = Agent.query.get_or_404(agent_id)
    return jsonify(agent.to_dict()), 200


@bp.route("/<int:agent_id>/messages", methods=["GET"])
def get_agent_messages(agent_id: int) -> tuple[dict, int]:
    """Get all messages for an agent."""
    agent = Agent.query.get_or_404(agent_id)
    messages = (
        Message.query.filter_by(agent_id=agent.id)
        .order_by(Message.timestamp.asc())
        .all()
    )
    return jsonify([msg.to_dict() for msg in messages]), 200


@bp.route("/<int:agent_id>/message", methods=["POST"])
def send_message_to_agent(agent_id: int) -> tuple[dict, int]:
    """Send message to an agent."""
    agent = Agent.query.get_or_404(agent_id)
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Message content required"}), 400

    # Create message record
    message = Message(agent_id=agent.id, sender="operator", content=data["message"])
    db.session.add(message)
    db.session.commit()

    # TODO: Process message with agent system

    return jsonify(message.to_dict()), 201
