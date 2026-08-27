from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.chat_promoted_example import ChatPromotedExample
from app.models.conversation import Conversation
from app.models.message import Message
from app.services.chat.orchestrator import handle_chat_message
from app.services.chat.sql_pipeline import SQLValidationError, validate_readonly_sql

chat_bp = Blueprint("chat", __name__)


def _conversation_to_dict(conversation: Conversation) -> dict:
    return {
        "id": conversation.id,
        "title": conversation.title,
        "updated_at": conversation.updated_at.isoformat(),
    }


def _message_to_dict(message: Message) -> dict:
    return {
        "id": message.id,
        "role": message.role,
        "content": message.content,
        "created_at": message.created_at.isoformat(),
        "table": message.table_data,
        "response_source": message.response_source,
        "sql_generated": message.sql_generated,
        "feedback": message.feedback,
    }


@chat_bp.route("/conversations", methods=["GET"])
def list_conversations():
    conversations = (
        Conversation.query.order_by(Conversation.updated_at.desc()).all()
    )
    return jsonify([_conversation_to_dict(c) for c in conversations])


@chat_bp.route("/conversations", methods=["POST"])
def create_conversation():
    conversation = Conversation()
    db.session.add(conversation)
    db.session.commit()
    return jsonify(_conversation_to_dict(conversation)), 201


@chat_bp.route("/conversations/<int:conversation_id>", methods=["GET"])
def get_conversation(conversation_id):
    conversation = Conversation.query.get_or_404(conversation_id)
    return jsonify(
        {
            **_conversation_to_dict(conversation),
            "messages": [_message_to_dict(m) for m in conversation.messages],
        }
    )


@chat_bp.route("/conversations/<int:conversation_id>", methods=["DELETE"])
def delete_conversation(conversation_id):
    conversation = Conversation.query.get_or_404(conversation_id)
    db.session.delete(conversation)
    db.session.commit()
    return jsonify({"message": "Conversation deleted"})


@chat_bp.route("/conversations/<int:conversation_id>/messages", methods=["POST"])
def post_message(conversation_id):
    conversation = Conversation.query.get_or_404(conversation_id)

    data = request.get_json(silent=True) or {}
    question = (data.get("message") or "").strip()

    if not question:
        return jsonify({"error": "message is required"}), 400

    user_message = Message(conversation_id=conversation.id, role="user", content=question)
    db.session.add(user_message)
    if conversation.title == "New conversation":
        conversation.title = question[:80]
    db.session.commit()

    try:
        result = handle_chat_message(conversation, user_message, question)
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 503
    except Exception as exc:
        return jsonify({"error": f"AI request failed: {exc}"}), 502

    db.session.add(
        Message(
            conversation_id=conversation.id,
            role="assistant",
            content=result["reply"],
            table_data=result["table"],
            response_source=result["meta"]["source"],
            sql_generated=result.get("sql"),
        )
    )
    db.session.commit()

    return jsonify(
        {
            "reply": result["reply"],
            "table": result["table"],
            "meta": result["meta"],
            "conversation_id": conversation.id,
        }
    )


@chat_bp.route("/messages/<int:message_id>/feedback", methods=["POST"])
def submit_feedback(message_id):
    message = Message.query.get_or_404(message_id)

    data = request.get_json(silent=True) or {}
    rating = data.get("rating")
    if rating not in ("up", "down"):
        return jsonify({"error": "rating must be 'up' or 'down'"}), 400

    message.feedback = rating
    db.session.commit()

    # Promote a thumbs-up on a real LLM-generated answer into a few-shot
    # example for future SQL generation — mirrors Databricks Genie's
    # "promote a good Q&A to a curated example" feedback loop. Re-validated
    # here too (defense in depth): a user's approval isn't a guarantee the
    # SQL is actually safe to reuse as a prompt example.
    if rating == "up" and message.response_source == "llm" and message.sql_generated:
        try:
            validate_readonly_sql(message.sql_generated)
        except SQLValidationError:
            pass
        else:
            user_message = (
                Message.query
                .filter(Message.conversation_id == message.conversation_id, Message.id < message.id, Message.role == "user")
                .order_by(Message.id.desc())
                .first()
            )
            if user_message:
                db.session.add(
                    ChatPromotedExample(question_text=user_message.content, sql_text=message.sql_generated)
                )
                db.session.commit()

    return jsonify({"message_id": message.id, "feedback": message.feedback})
