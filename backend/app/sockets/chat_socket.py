"""WebSocket event handlers for chat."""

import asyncio
from flask import request
from flask_socketio import emit

from app import socketio
from app.services import get_agent_service


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

    # Emit status that agent is processing
    emit("agent_status", {"agent_id": agent_id, "status": "busy"}, broadcast=True)

    try:
        # Get agent service
        agent_service = get_agent_service()

        # Process message with agent system (async)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            agent_service.send_message_to_agent(agent_id, message)
        )
        loop.close()

        if result.get("success"):
            # Emit response back to client
            emit(
                "agent_response",
                {
                    "agent_id": agent_id,
                    "message": result.get("response"),
                    "sender": "agent",
                    "agent_name": result.get("agent_name"),
                },
            )

            # Emit status update
            emit(
                "agent_status",
                {"agent_id": agent_id, "status": result.get("status", "idle")},
                broadcast=True,
            )
        else:
            emit("error", {"error": result.get("error"), "agent_id": agent_id})
            emit(
                "agent_status",
                {"agent_id": agent_id, "status": "error"},
                broadcast=True,
            )

    except RuntimeError as e:
        # Agent system not initialized
        emit("error", {"error": str(e), "hint": "Agent system not initialized"})
        emit("agent_status", {"agent_id": agent_id, "status": "error"}, broadcast=True)
    except Exception as e:
        emit("error", {"error": str(e), "agent_id": agent_id})
        emit("agent_status", {"agent_id": agent_id, "status": "error"}, broadcast=True)


@socketio.on("agent_status_request")
def handle_agent_status_request(data: dict) -> None:
    """Handle agent status request.

    Args:
        data: Dictionary with 'agent_id'
    """
    agent_id = data.get("agent_id")

    if not agent_id:
        emit("error", {"error": "agent_id required"})
        return

    try:
        agent_service = get_agent_service()
        status = agent_service.get_agent_status(agent_id)
        emit("agent_status", status)
    except RuntimeError as e:
        emit("error", {"error": str(e)})
    except Exception as e:
        emit("error", {"error": str(e)})


@socketio.on("workflow_update")
def handle_workflow_update(data: dict) -> None:
    """Handle workflow update event.

    Args:
        data: Dictionary with workflow information
    """
    workflow_id = data.get("workflow_id")

    if not workflow_id:
        emit("error", {"error": "workflow_id required"})
        return

    # Broadcast workflow update to all clients
    emit(
        "workflow_status",
        {
            "workflow_id": workflow_id,
            "status": data.get("status"),
            "message": data.get("message"),
        },
        broadcast=True,
    )
