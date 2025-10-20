"""Socket.IO event handlers for chat interactions."""

from __future__ import annotations

from typing import Any, Dict

from flask_socketio import SocketIO, emit

from app.services import get_agent_service
from app.utils.async_runner import run_async

__all__ = ["register_chat_events"]


def register_chat_events(socketio: SocketIO) -> None:
    """Register chat-related Socket.IO events."""

    @socketio.on("connect")
    def handle_connect() -> None:
        emit("connection_response", {"status": "connected"})

    @socketio.on("disconnect")
    def handle_disconnect() -> None:  # pragma: no cover - no side effects needed
        emit("connection_response", {"status": "disconnected"})

    @socketio.on("send_message")
    def handle_send_message(payload: Dict[str, Any]) -> None:
        if not isinstance(payload, dict):
            emit("error", {"error": "agent_id and message required"})
            return

        agent_id = payload.get("agent_id")
        message = payload.get("message")

        if agent_id is None or not message:
            emit("error", {"error": "agent_id and message required"})
            return

        emit("agent_status", {"agent_id": agent_id, "status": "busy"})

        service = get_agent_service()

        try:
            result = run_async(
                service.send_message_to_agent,
                int(agent_id),
                str(message),
            )
        except RuntimeError as exc:
            emit(
                "error",
                {"error": str(exc), "hint": "Call /api/init first"},
            )
            emit("agent_status", {"agent_id": agent_id, "status": "idle"})
            return
        except Exception as exc:  # pragma: no cover - defensive
            emit("error", {"error": str(exc)})
            emit("agent_status", {"agent_id": agent_id, "status": "idle"})
            return

        if result.get("success"):
            emit(
                "agent_response",
                {
                    "agent_id": agent_id,
                    "message": result.get("response"),
                    "sender": "agent",
                },
            )
        else:
            emit(
                "error",
                {
                    "error": result.get("error", "Agent processing failed"),
                    "agent_id": agent_id,
                },
            )

        emit(
            "agent_status",
            {
                "agent_id": agent_id,
                "status": result.get("status", "idle"),
                "agent_name": result.get("agent_name"),
            },
        )

    @socketio.on("agent_status_request")
    def handle_agent_status_request(payload: Dict[str, Any]) -> None:
        if not isinstance(payload, dict) or "agent_id" not in payload:
            emit("error", {"error": "agent_id required"})
            return

        service = get_agent_service()
        status = service.get_agent_status(int(payload["agent_id"]))
        emit("agent_status", status)

    @socketio.on("workflow_update")
    def handle_workflow_update(payload: Dict[str, Any]) -> None:
        if not isinstance(payload, dict) or "workflow_id" not in payload:
            emit("error", {"error": "workflow_id required"})
            return

        emit(
            "workflow_status",
            {
                "workflow_id": payload["workflow_id"],
                "status": payload.get("status", "unknown"),
                "message": payload.get("message"),
            },
        )
