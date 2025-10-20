"""Agent model."""

from datetime import datetime, timezone

from app import db


class Agent(db.Model):
    """Agent model representing an AI agent in the system."""

    __tablename__ = "agents"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(
        db.String(50), nullable=False
    )  # 'driver', 'creator', 'generator', 'dynamic'
    role = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default="idle")  # 'idle', 'working', 'waiting'
    config = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    messages = db.relationship("Message", backref="agent", lazy=True)
    tasks = db.relationship("Task", backref="assigned_agent", lazy=True)

    def to_dict(self) -> dict:
        """Convert agent to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "role": self.role,
            "status": self.status,
            "config": self.config,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


