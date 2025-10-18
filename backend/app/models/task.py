"""Task model."""

from datetime import datetime, timezone

from app import db


class Task(db.Model):
    """Task model for workflow tasks."""

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey("workflows.id"), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey("agents.id"), nullable=True)
    status = db.Column(
        db.String(50), default="pending"
    )  # 'pending', 'in_progress', 'completed', 'failed'
    description = db.Column(db.Text, nullable=False)
    result = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self) -> dict:
        """Convert task to dictionary."""
        return {
            "id": self.id,
            "workflow_id": self.workflow_id,
            "assigned_to": self.assigned_to,
            "status": self.status,
            "description": self.description,
            "result": self.result,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
        }

