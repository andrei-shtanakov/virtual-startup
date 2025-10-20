"""Run the Flask application."""

import errno

from werkzeug.serving import WSGIRequestHandler

from app import create_app
from app.utils.async_runner import run_async


_DISCONNECTED_ERRNOS = {
    error
    for error in [
        errno.EBADF,
        getattr(errno, "ENOTCONN", None),
        getattr(errno, "ECONNRESET", None),
        getattr(errno, "EPIPE", None),
    ]
    if error is not None
}


class PatchedWSGIRequestHandler(WSGIRequestHandler):
    """Treat common disconnect errors from dropped clients as benign."""

    def handle(self) -> None:
        try:
            super().handle()
        except OSError as exc:
            if getattr(exc, "errno", None) in _DISCONNECTED_ERRNOS:
                self.connection_dropped(exc)
                return
            raise


app = create_app()

def initialize_agents():
    """Initialize agent system on startup."""
    from app.services import get_agent_service

    agent_service = get_agent_service()

    if not agent_service.initialized:
        print("Initializing agent system...")
        try:
            status = run_async(agent_service.initialize)

            if "error" in status:
                print(f"❌ Agent initialization failed: {status.get('error')}")
            else:
                print("✅ Agent system initialized successfully")
                print(f"   Agents: {', '.join(status.keys())}")
        except Exception as e:
            print(f"❌ Agent initialization error: {e}")

if __name__ == "__main__":
    # Initialize agents before starting server
    with app.app_context():
        initialize_agents()

    print("\n🚀 Starting API server on http://localhost:5000")
    print("💻 TUI interface available via: uv run python tui_app.py")

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000,
        request_handler=PatchedWSGIRequestHandler,
    )
