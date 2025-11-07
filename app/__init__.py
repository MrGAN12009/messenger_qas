"""Application package initialization."""

from __future__ import annotations

import time

from flask import Flask
from sqlalchemy.exc import OperationalError

from .config import Config
from .db.database import Database
from .routes.api import api_bp
from .routes.web import web_bp


def create_app(config_class: type[Config] | None = None) -> Flask:
    """Application factory."""

    app = Flask(__name__)
    app_config = config_class() if config_class else Config()
    app.config.from_mapping(app_config.to_mapping())

    database = Database()
    database.init_app(app)
    app.extensions["database"] = database

    with app.app_context():
        for attempt in range(5):
            try:
                database.create_all()
                break
            except OperationalError as exc:
                if attempt == 4:
                    raise exc
                time.sleep(2)

    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.shell_context_processor
    def _shell_context() -> dict[str, object]:
        return {"db": database.db}

    return app

