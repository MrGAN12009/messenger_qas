"""Domain service that coordinates messenger operations."""

from __future__ import annotations

from typing import Iterable, Sequence

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.repositories import ChatRepository, MessageRepository, UserRepository
from app.models import Chat, Message, User


class MessengerService:
    """High-level API for the messenger domain."""

    def __init__(self, session: Session) -> None:
        self._session = session
        self._user_repo = UserRepository(session)
        self._chat_repo = ChatRepository(session)
        self._message_repo = MessageRepository(session)

    # Users -----------------------------------------------------------------
    def list_users(self) -> Iterable[User]:
        return self._user_repo.list_users()

    def create_user(self, username: str, display_name: str, email: str | None = None) -> User:
        existing = self._user_repo.get_by_username(username)
        if existing:
            raise ValueError("Username already exists")

        try:
            user = self._user_repo.create(username=username, display_name=display_name, email=email)
            self._session.commit()
        except IntegrityError as exc:  # pragma: no cover - safety net for race conditions
            self._session.rollback()
            raise ValueError("Username already exists") from exc

        return user

    def get_user(self, user_id: int) -> User | None:
        return self._user_repo.get_by_id(user_id)

    # Chats ------------------------------------------------------------------
    def list_chats(self) -> Iterable[Chat]:
        return self._chat_repo.list_chats()

    def get_chat(self, chat_id: int, include_messages: bool = False) -> Chat | None:
        if include_messages:
            return self._chat_repo.get_with_messages(chat_id)
        return self._chat_repo.get_by_id(chat_id)

    def create_chat(
        self, title: str, participant_ids: Sequence[int], description: str | None = None
    ) -> Chat:
        participants = [self._user_repo.get_by_id(user_id) for user_id in participant_ids]
        if not all(participants):
            missing = [pid for pid, user in zip(participant_ids, participants) if user is None]
            raise ValueError(f"Participants not found: {missing}")

        chat = self._chat_repo.create(
            title=title,
            description=description,
            participants=[user for user in participants if user],
        )
        self._session.commit()
        return chat

    # Messages ---------------------------------------------------------------
    def list_messages(self, chat_id: int) -> Iterable[Message]:
        return self._message_repo.list_for_chat(chat_id)

    def send_message(self, chat_id: int, author_id: int, content: str) -> Message:
        chat = self._chat_repo.get_by_id(chat_id)
        if chat is None:
            raise ValueError("Chat not found")

        author = self._user_repo.get_by_id(author_id)
        if author is None:
            raise ValueError("User not found")

        if author not in chat.participants:
            self._chat_repo.add_participant(chat, author)

        message = self._message_repo.create(chat=chat, author=author, content=content)
        self._session.commit()
        return message

