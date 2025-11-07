"""Route helpers and exports."""

from __future__ import annotations

from flask import current_app

from app.db import Database
from app.services import MessengerService


def get_messenger_service() -> MessengerService:
    """Return a MessengerService bound to the current application context."""

    database: Database = current_app.extensions["database"]
    return MessengerService(database.session)


__all__ = ["get_messenger_service"]

