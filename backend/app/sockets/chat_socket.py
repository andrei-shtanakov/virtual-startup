"""WebSocket event handlers for chat."""

import asyncio
import uuid
from datetime import datetime
from typing import Any, Awaitable
import sys

from flask import request
from flask_socketio import emit

from app import db, socketio
from app.services import get_agent_service

print("🔧 Loading chat_socket handlers...", file=sys.stderr)


def _run_async(coro: Awaitable[dict[str, Any]]) -> dict[str, Any]:
    """Execute coroutine inside a dedicated event loop.

    This prevents event loop clashes when Flask-SocketIO is running with
    threading or eventlet.
    """
    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)
    finally:
        loop.close()
        asyncio.set_event_loop(None)


def _get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.utcnow().isoformat() + "Z"


def emit_activity_log(
    log_type: str, message: str, metadata: dict[str, Any] | None = None
) -> None:
    """Emit an activity log event to all connected clients.

    Args:
        log_type: Type of log (info, success, warning, error)
        message: Log message
        metadata: Optional metadata dictionary
    """
    log_entry = {
        "id": str(uuid.uuid4()),
        "timestamp": _get_timestamp(),
        "type": log_type,
        "message": message,
        "metadata": metadata or {},
    }

    # Add agent info if available
    if metadata and "agent_id" in metadata:
        try:
            agent_service = get_agent_service()
            agents = agent_service.list_agents()
            agent = next((a for a in agents if a["id"] == metadata["agent_id"]), None)
            if agent:
                log_entry["agent"] = {"id": agent["id"], "name": agent["name"]}
        except Exception:  # noqa: BLE001
            pass

    # Use socketio.emit() to broadcast to all clients from any context
    socketio.emit("activity_log", log_entry)


def emit_workflow_stats(active: int = 0, completed: int = 0, failed: int = 0, current_task: str | None = None) -> None:
    """Emit workflow statistics update to all connected clients.

    Args:
        active: Number of active workflows
        completed: Number of completed workflows
        failed: Number of failed workflows
        current_task: Optional current task description
    """
    stats = {
        "active": active,
        "completed": completed,
        "failed": failed,
        "currentTask": current_task,
    }

    # Use socketio.emit() to broadcast to all clients from any context
    socketio.emit("workflow_stats", stats)


@socketio.on("connect")
def handle_connect():
    """Handle client connection."""
    print(f"🔌 Client connected: {request.sid}", file=sys.stderr)
    # Don't emit anything here - let the connection establish first
    return True  # Accept the connection


@socketio.on("disconnect")
def handle_disconnect():
    """Handle client disconnection."""
    print(f"Client disconnected: {request.sid}", file=sys.stderr)
    emit_activity_log("info", "User disconnected from dashboard")


@socketio.on("send_message")
def handle_send_message(data: dict[str, Any]) -> None:
    """Handle message from operator to agent.

    Args:
        data: Dictionary with 'content' and optional 'agent_id'
              For Quick Chat: only 'content' is required (routes to Driver)
              For specific agent: both 'agent_id' and 'content' required
    """
    content = data.get("content") or data.get("message")
    agent_id = data.get("agent_id", 1)  # Default to Driver (agent_id=1) for Quick Chat

    if not content:
        emit("error", {"error": "message content required"})
        return

    print(f"💬 Received message for agent {agent_id}: {content}", file=sys.stderr)

    # Emit activity log
    emit_activity_log("info", f"User sent message to agent", {"agent_id": agent_id})

    # Emit status that agent is processing
    emit("agent_status", {"agent_id": agent_id, "status": "busy"}, broadcast=True)

    try:
        agent_service = get_agent_service()
        result = _run_async(agent_service.send_message_to_agent(agent_id, content))

        if result.get("success"):
            # Emit agent response (single event to avoid duplicates)
            emit(
                "agent_response",
                {
                    "id": f"agent-{agent_id}-{request.sid}",
                    "timestamp": result.get("timestamp") or _get_timestamp(),
                    "sender": "agent",
                    "agentName": result.get("agent_name", "Agent"),
                    "content": result.get("response"),
                },
            )

            emit(
                "agent_status",
                {"agent_id": agent_id, "status": result.get("status", "idle")},
                broadcast=True,
            )

            # Emit activity log for successful response
            emit_activity_log(
                "success",
                f"{result.get('agent_name', 'Agent')} responded to message",
                {"agent_id": agent_id},
            )
        else:
            emit("error", {"error": result.get("error"), "agent_id": agent_id})
            emit(
                "agent_status",
                {"agent_id": agent_id, "status": "error"},
                broadcast=True,
            )
            emit_activity_log("error", f"Agent {agent_id} failed to respond", {"error": result.get("error")})

    except RuntimeError as exc:
        emit("error", {"error": str(exc), "hint": "Agent system not initialized"})
        emit("agent_status", {"agent_id": agent_id, "status": "error"}, broadcast=True)
        emit_activity_log("error", "Agent system not initialized", {"error": str(exc)})
    except Exception as exc:  # noqa: BLE001
        emit("error", {"error": str(exc), "agent_id": agent_id})
        emit("agent_status", {"agent_id": agent_id, "status": "error"}, broadcast=True)
        emit_activity_log("error", f"Error processing message", {"error": str(exc)})


@socketio.on("agent_status_request")
def handle_agent_status_request(data: dict[str, Any]) -> None:
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
        emit_activity_log("info", f"Agent status requested", {"agent_id": agent_id})
    except RuntimeError as exc:
        emit("error", {"error": str(exc)})
        emit_activity_log("error", "Failed to get agent status", {"error": str(exc)})
    except Exception as exc:  # noqa: BLE001
        emit("error", {"error": str(exc)})
        emit_activity_log("error", "Error getting agent status", {"error": str(exc)})


@socketio.on("workflow_update")
def handle_workflow_update(data: dict[str, Any]) -> None:
    """Handle workflow update event.

    Args:
        data: Dictionary with workflow information
    """
    workflow_id = data.get("workflow_id")

    if not workflow_id:
        emit("error", {"error": "workflow_id required"})
        return

    status = data.get("status", "")
    message = data.get("message", "")

    # Emit traditional workflow_status event using socketio for broadcast
    socketio.emit(
        "workflow_status",
        {
            "workflow_id": workflow_id,
            "status": status,
            "message": message,
        }
    )

    # Emit activity log for workflow update
    log_type = "success" if status == "completed" else "info" if status == "active" else "error"
    emit_activity_log(log_type, f"Workflow {workflow_id}: {message}", {"workflow_id": workflow_id})

    # Update workflow stats (this would need actual counting logic)
    # For now, we'll emit a basic update
    emit_workflow_stats(
        active=1 if status == "active" else 0,
        completed=1 if status == "completed" else 0,
        failed=1 if status == "failed" else 0,
        current_task=message if status == "active" else None,
    )
