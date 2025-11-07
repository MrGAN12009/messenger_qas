"""REST API blueprint mirroring web functionality."""

from __future__ import annotations

from http import HTTPStatus
from typing import Any

from flask import Blueprint, jsonify, request

from . import get_messenger_service


api_bp = Blueprint("api", __name__)


def _json_error(message: str, status: HTTPStatus) -> tuple[dict[str, str], int]:
    return {"error": message}, int(status)


@api_bp.get("/users")
def api_list_users() -> Any:
    service = get_messenger_service()
    users = [user.to_dict() for user in service.list_users()]
    return jsonify(users)


@api_bp.post("/users")
def api_create_user() -> Any:
    service = get_messenger_service()
    payload = request.get_json(silent=True) or {}
    username = str(payload.get("username", "")).strip()
    display_name = str(payload.get("display_name", "")).strip()
    email = payload.get("email")

    if not username or not display_name:
        return _json_error("username and display_name are required", HTTPStatus.BAD_REQUEST)

    try:
        user = service.create_user(username=username, display_name=display_name, email=email)
    except ValueError as exc:
        return _json_error(str(exc), HTTPStatus.BAD_REQUEST)

    return jsonify(user.to_dict()), int(HTTPStatus.CREATED)


@api_bp.get("/chats")
def api_list_chats() -> Any:
    service = get_messenger_service()
    chats = [chat.to_dict() for chat in service.list_chats()]
    return jsonify(chats)


@api_bp.post("/chats")
def api_create_chat() -> Any:
    service = get_messenger_service()
    payload = request.get_json(silent=True) or {}
    title = str(payload.get("title", "")).strip()
    description = payload.get("description")
    participant_ids = payload.get("participant_ids", [])

    if not title:
        return _json_error("title is required", HTTPStatus.BAD_REQUEST)

    if not isinstance(participant_ids, list) or not participant_ids:
        return _json_error("participant_ids must be a non-empty list", HTTPStatus.BAD_REQUEST)

    try:
        chat = service.create_chat(
            title=title,
            description=description,
            participant_ids=[int(value) for value in participant_ids],
        )
    except ValueError as exc:
        return _json_error(str(exc), HTTPStatus.BAD_REQUEST)

    return jsonify(chat.to_dict()), int(HTTPStatus.CREATED)


@api_bp.get("/chats/<int:chat_id>")
def api_get_chat(chat_id: int) -> Any:
    service = get_messenger_service()
    chat = service.get_chat(chat_id, include_messages=True)
    if chat is None:
        return _json_error("chat not found", HTTPStatus.NOT_FOUND)
    return jsonify(chat.to_dict(include_messages=True))


@api_bp.post("/chats/<int:chat_id>/messages")
def api_send_message(chat_id: int) -> Any:
    service = get_messenger_service()
    payload = request.get_json(silent=True) or {}
    author_id = payload.get("author_id")
    content = str(payload.get("content", "")).strip()

    if author_id is None or not content:
        return _json_error("author_id and content are required", HTTPStatus.BAD_REQUEST)

    try:
        message = service.send_message(chat_id=chat_id, author_id=int(author_id), content=content)
    except ValueError as exc:
        return _json_error(str(exc), HTTPStatus.BAD_REQUEST)

    return jsonify(message.to_dict()), int(HTTPStatus.CREATED)

