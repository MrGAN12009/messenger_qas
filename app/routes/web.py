"""Blueprint with HTML routes."""

from __future__ import annotations

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from . import get_messenger_service


web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def home() -> str:
    service = get_messenger_service()
    chats = list(service.list_chats())
    users = list(service.list_users())
    return render_template("index.html", chats=chats, users=users)


@web_bp.route("/users", methods=["POST"])
def create_user() -> str:
    service = get_messenger_service()
    username = request.form.get("username", "").strip()
    display_name = request.form.get("display_name", "").strip()
    email = request.form.get("email") or None
    if not username or not display_name:
        flash("Username and display name are required", "error")
        return redirect(url_for("web.home"))

    try:
        service.create_user(username=username, display_name=display_name, email=email)
    except ValueError as exc:
        flash(str(exc), "error")
        return redirect(url_for("web.home"))

    flash("User created", "success")
    return redirect(url_for("web.home"))


@web_bp.route("/chats", methods=["POST"])
def create_chat() -> str:
    service = get_messenger_service()
    title = request.form.get("title", "").strip()
    description = request.form.get("description") or None
    participant_ids_raw = request.form.get("participant_ids", "")

    if not title:
        flash("Chat title is required", "error")
        return redirect(url_for("web.home"))

    try:
        participant_ids = [int(value) for value in participant_ids_raw.split(",") if value.strip()]
        if not participant_ids:
            flash("Provide at least one participant id", "error")
            return redirect(url_for("web.home"))

        chat = service.create_chat(title=title, participant_ids=participant_ids, description=description)
    except ValueError as exc:
        flash(str(exc), "error")
        return redirect(url_for("web.home"))

    flash(f"Chat '{chat.title}' created", "success")
    return redirect(url_for("web.view_chat", chat_id=chat.id))


@web_bp.route("/chats/<int:chat_id>")
def view_chat(chat_id: int) -> str:
    service = get_messenger_service()
    chat = service.get_chat(chat_id, include_messages=True)
    if chat is None:
        abort(404)
    users = list(service.list_users())
    return render_template("chat.html", chat=chat, users=users)


@web_bp.route("/chats/<int:chat_id>/messages", methods=["POST"])
def post_message(chat_id: int) -> str:
    service = get_messenger_service()
    author_id_raw = request.form.get("author_id", "").strip()
    content = request.form.get("content", "").strip()

    if not author_id_raw or not content:
        flash("Author and content are required", "error")
        return redirect(url_for("web.view_chat", chat_id=chat_id))

    try:
        author_id = int(author_id_raw)
        service.send_message(chat_id=chat_id, author_id=author_id, content=content)
    except ValueError as exc:
        flash(str(exc), "error")

    return redirect(url_for("web.view_chat", chat_id=chat_id))

