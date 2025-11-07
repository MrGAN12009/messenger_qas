"""Repository for chat persistence operations."""

from __future__ import annotations

from typing import Iterable, Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Chat, Message, User


class ChatRepository:
    """Encapsulates chat-related queries."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, title: str, description: str | None, participants: Sequence[User]) -> Chat:
        chat = Chat(title=title, description=description)
        chat.participants.extend(participants)
        self._session.add(chat)
        self._session.flush()
        return chat

    def get_by_id(self, chat_id: int) -> Optional[Chat]:
        return self._session.get(Chat, chat_id)

    def get_with_messages(self, chat_id: int) -> Optional[Chat]:
        statement = (
            select(Chat)
            .options(
                selectinload(Chat.messages).selectinload(Message.author),
                selectinload(Chat.participants),
            )
            .where(Chat.id == chat_id)
        )
        return self._session.scalar(statement)

    def list_chats(self) -> Iterable[Chat]:
        statement = select(Chat).options(selectinload(Chat.participants)).order_by(Chat.title.asc())
        return self._session.scalars(statement)

    def add_participant(self, chat: Chat, user: User) -> None:
        if user not in chat.participants:
            chat.participants.append(user)

