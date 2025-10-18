"""WebSocket handlers package."""


def register_socketio_handlers() -> None:
    """Ensure Socket.IO event handlers are imported and registered."""
    import app.sockets.chat_socket  # noqa: F401
