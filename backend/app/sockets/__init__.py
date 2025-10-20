"""Socket.IO event registration."""

from __future__ import annotations

from flask_socketio import SocketIO

from .chat_socket import register_chat_events

__all__ = ["init_socketio"]


def init_socketio(socketio: SocketIO) -> None:
    """Register all Socket.IO event handlers."""
    register_chat_events(socketio)
