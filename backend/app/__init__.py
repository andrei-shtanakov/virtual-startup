"""Flask application factory."""

import asyncio
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(
    cors_allowed_origins="*",
    async_mode="eventlet",
    logger=False,
    engineio_logger=False
)


def create_app(config_name: str = "development") -> Flask:
    """Create and configure the Flask application.

    Args:
        config_name: Configuration name (development, testing, production)

    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)

    # Load configuration
    if config_name == "development":
        app.config.from_object("config.DevelopmentConfig")
    elif config_name == "testing":
        app.config.from_object("config.TestingConfig")
    else:
        app.config.from_object("config.ProductionConfig")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Initialize Socket.IO first
    socketio.init_app(app)

    # Then register socket handlers AFTER Socket.IO is initialized with the app
    # This ensures the decorators have access to the fully configured socketio instance
    from app.sockets import register_socketio_handlers

    register_socketio_handlers()

    # Register blueprints
    from app.routes import agent_routes, workflow_routes, stats_routes

    app.register_blueprint(agent_routes.bp)
    app.register_blueprint(workflow_routes.bp)
    app.register_blueprint(stats_routes.bp)

    @app.route("/")
    def index() -> dict[str, str]:
        """Health check endpoint."""
        return {"status": "ok", "message": "Virtual Startup API"}

    @app.route("/api/init", methods=["POST"])
    def initialize_agents() -> tuple[dict, int]:
        """Initialize the agent system."""
        from app.services import get_agent_service

        agent_service = get_agent_service()

        if agent_service.initialized:
            return jsonify({"status": "already_initialized"}), 200

        try:
            # Initialize agent system (async)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            status = loop.run_until_complete(agent_service.initialize())
            loop.close()

            if "error" in status:
                return jsonify(status), 500

            return jsonify(
                {
                    "status": "initialized",
                    "message": "Agent system initialized successfully",
                    "agents": status,
                }
            ), 200

        except Exception as e:
            return jsonify({"status": "error", "error": str(e)}), 500

    @app.route("/api/status", methods=["GET"])
    def system_status() -> tuple[dict, int]:
        """Get system status."""
        from app.services import get_agent_service

        agent_service = get_agent_service()

        return jsonify(
            {
                "api": "running",
                "agents_initialized": agent_service.initialized,
                "database": "connected",
            }
        ), 200

    return app
