"""Database utilities."""

from __future__ import annotations

from typing import Any

from flask import Flask
from app.models.base import db


class Database:

    def __init__(self) -> None:
        self.db = db

    def init_app(self, app: Flask) -> None:
        self.db.init_app(app)

    @property
    def session(self) -> Any:
        return self.db.session

    def create_all(self) -> None:
        self.db.create_all()

