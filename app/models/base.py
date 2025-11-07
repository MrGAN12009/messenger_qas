"""Base model and database binding."""

from __future__ import annotations

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class ModelBase(db.Model):  # type: ignore[misc]
    """Declarative base class for project models."""

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=False
    )


__all__ = ["db", "ModelBase"]

