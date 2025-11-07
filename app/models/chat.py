"""Chat model definition."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .base import ModelBase, db

if TYPE_CHECKING:
    from .message import Message
    from .user import User


chat_users = db.Table(
    "chat_users",
    db.Column("chat_id", db.Integer, db.ForeignKey("chats.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
)


class Chat(ModelBase):
    """Represents a conversation between users."""

    __tablename__ = "chats"

    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    messages = db.relationship(
        "Message",
        back_populates="chat",
        cascade="all, delete-orphan",
        order_by="Message.created_at",
    )
    participants = db.relationship("User", secondary=chat_users, back_populates="chats")

    def to_dict(self, include_messages: bool = False) -> dict[str, object]:
        """Serialize chat to dictionary."""

        data: dict[str, object] = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "participants": [user.to_dict() for user in self.participants],
        }
        if include_messages:
            data["messages"] = [message.to_dict(include_author=True) for message in self.messages]
        return data

