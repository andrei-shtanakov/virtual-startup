"""Workflow model."""

from datetime import datetime, timezone

from app import db


class Workflow(db.Model):
    """Workflow model for tracking agent workflows."""

    __tablename__ = "workflows"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(
        db.String(50), default="active"
    )  # 'active', 'completed', 'failed'
    started_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime, nullable=True)
    meta = db.Column(db.JSON, nullable=True)

    # Relationships
    tasks = db.relationship("Task", backref="workflow", lazy=True)

    def to_dict(self) -> dict:
        """Convert workflow to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
            "meta": self.meta,
        }
