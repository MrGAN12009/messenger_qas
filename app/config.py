"""Application configuration settings."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass(slots=True)
class Config:
    """Base configuration for the Flask application."""

    app_name: str = field(default_factory=lambda: os.getenv("APP_NAME", "Messenger"))
    secret_key: str = field(default_factory=lambda: os.getenv("SECRET_KEY", "change-me"))
    database_url: str = field(
        default_factory=lambda: os.getenv(
            "DATABASE_URL", "postgresql+psycopg2://messenger:messenger@db:5432/messenger"
        )
    )

    def to_mapping(self) -> dict[str, str]:
        """Return config mapping for Flask."""

        return {
            "SECRET_KEY": self.secret_key,
            "SQLALCHEMY_DATABASE_URI": self.database_url,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "APP_NAME": self.app_name,
        }

