"""Message model."""

from datetime import datetime, timezone

from app import db


class Message(db.Model):
    """Message model for agent communications."""

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey("agents.id"), nullable=False)
    sender = db.Column(db.String(50), nullable=False)  # 'agent', 'operator', 'system'
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    meta = db.Column(db.JSON, nullable=True)

    def to_dict(self) -> dict:
        """Convert message to dictionary."""
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "sender": self.sender,
            "content": self.content,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "meta": self.meta,
        }
