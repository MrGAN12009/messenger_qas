"""User model definition."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .base import ModelBase, db

if TYPE_CHECKING:
    from .chat import Chat
    from .message import Message


class User(ModelBase):
    """Represents a messenger user."""

    __tablename__ = "users"

    username = db.Column(db.String(80), unique=True, nullable=False)
    display_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)

    messages = db.relationship("Message", back_populates="author", cascade="all, delete-orphan")
    chats = db.relationship("Chat", secondary="chat_users", back_populates="participants")

    def to_dict(self) -> dict[str, str | int | None]:
        """Serialize the user to a dictionary."""

        return {
            "id": self.id,
            "username": self.username,
            "display_name": self.display_name,
            "email": self.email,
        }

