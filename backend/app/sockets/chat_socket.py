"""WebSocket event handlers for chat."""

from flask import request
from flask_socketio import emit

from app import socketio


@socketio.on("connect")
def handle_connect() -> None:
    """Handle client connection."""
    print(f"Client connected: {request.sid}")
    emit("connection_response", {"status": "connected"})


@socketio.on("disconnect")
def handle_disconnect() -> None:
    """Handle client disconnection."""
    print(f"Client disconnected: {request.sid}")


@socketio.on("send_message")
def handle_send_message(data: dict) -> None:
    """Handle message from operator to agent.

    Args:
        data: Dictionary with 'agent_id' and 'message'
    """
    agent_id = data.get("agent_id")
    message = data.get("message")

    if not agent_id or not message:
        emit("error", {"error": "agent_id and message required"})
        return

    print(f"Received message for agent {agent_id}: {message}")

    # TODO: Process with agent system
    # For now, echo back
    emit(
        "agent_response",
        {"agent_id": agent_id, "message": f"Echo: {message}", "sender": "agent"},
    )


@socketio.on("agent_status")
def handle_agent_status_request(data: dict) -> None:
    """Handle agent status request.

    Args:
        data: Dictionary with 'agent_id'
    """
    agent_id = data.get("agent_id")

    # TODO: Get actual agent status
    emit("agent_status_response", {"agent_id": agent_id, "status": "idle"})
