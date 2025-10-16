"""Flask application factory."""

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

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
    CORS(app)
    socketio.init_app(app)

    # Register blueprints
    from app.routes import agent_routes, workflow_routes, stats_routes

    app.register_blueprint(agent_routes.bp)
    app.register_blueprint(workflow_routes.bp)
    app.register_blueprint(stats_routes.bp)

    # Register socket handlers
    from app.sockets import chat_socket  # noqa: F401

    @app.route("/")
    def index() -> dict[str, str]:
        """Health check endpoint."""
        return {"status": "ok", "message": "Virtual Startup API"}

    return app
