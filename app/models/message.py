"""Message model definition."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .base import ModelBase, db

if TYPE_CHECKING:
    from .chat import Chat
    from .user import User


class Message(ModelBase):
    """Represents a message sent in a chat."""

    __tablename__ = "messages"

    content = db.Column(db.Text, nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey("chats.id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    chat = db.relationship("Chat", back_populates="messages")
    author = db.relationship("User", back_populates="messages")

    def to_dict(self, include_author: bool = False) -> dict[str, object]:
        """Serialize message to dictionary."""

        data: dict[str, object] = {
            "id": self.id,
            "content": self.content,
            "chat_id": self.chat_id,
            "author_id": self.author_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

        if include_author and self.author:
            data["author"] = self.author.to_dict()

        return data

