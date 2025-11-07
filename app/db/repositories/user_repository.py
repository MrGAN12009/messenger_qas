"""Repository for user-related database operations."""

from __future__ import annotations

from typing import Iterable, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User


class UserRepository:
    """Encapsulates queries related to users."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self._session.get(User, user_id)

    def get_by_username(self, username: str) -> Optional[User]:
        statement = select(User).where(User.username == username)
        return self._session.scalar(statement)

    def list_users(self) -> Iterable[User]:
        statement = select(User).order_by(User.username.asc())
        return self._session.scalars(statement)

    def create(self, username: str, display_name: str, email: str | None = None) -> User:
        user = User(username=username, display_name=display_name, email=email)
        self._session.add(user)
        self._session.flush()
        return user

