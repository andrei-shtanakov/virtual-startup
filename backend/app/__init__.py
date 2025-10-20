"""Flask application factory."""

from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

from app.utils.async_runner import run_async

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(cors_allowed_origins="*")


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
            status = run_async(agent_service.initialize)

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

    socketio.init_app(
        app,
        cors_allowed_origins=app.config.get("SOCKETIO_CORS_ALLOWED_ORIGINS", "*"),
    )

    from app.sockets import init_socketio

    init_socketio(socketio)

    return app
