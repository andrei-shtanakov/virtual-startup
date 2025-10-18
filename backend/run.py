"""Run the Flask application."""

import asyncio
import os
from app import create_app, socketio

app = create_app()

def initialize_agents():
    """Initialize agent system on startup."""
    from app.services import get_agent_service

    agent_service = get_agent_service()

    if not agent_service.initialized:
        print("Initializing agent system...")
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            status = loop.run_until_complete(agent_service.initialize())
            loop.close()

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

    print("\n🚀 Starting server on http://localhost:5000")

    # Disable Flask's reloader in debug mode to prevent WebSocket handler issues
    # The reloader creates a child process which doesn't properly re-register Socket.IO handlers
    use_reloader = os.environ.get('FLASK_USE_RELOADER', 'false').lower() == 'true'

    socketio.run(app, debug=True, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True, use_reloader=use_reloader)

