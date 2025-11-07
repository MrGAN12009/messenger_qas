"""Repository for message persistence."""

from __future__ import annotations

from typing import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Chat, Message, User


class MessageRepository:
    """Encapsulates message-related queries."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, chat: Chat, author: User, content: str) -> Message:
        message = Message(chat=chat, author=author, content=content)
        self._session.add(message)
        self._session.flush()
        return message

    def list_for_chat(self, chat_id: int) -> Iterable[Message]:
        statement = (
            select(Message)
            .options(selectinload(Message.author))
            .where(Message.chat_id == chat_id)
            .order_by(Message.created_at.asc())
        )
        return self._session.scalars(statement)

