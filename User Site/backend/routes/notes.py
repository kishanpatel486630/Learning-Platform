"""
Notes Routes — Full CRUD for user notes
GET    /api/notes           — List user's notes
POST   /api/notes           — Create note
PUT    /api/notes/<id>      — Update note
DELETE /api/notes/<id>      — Delete note
"""
from flask import Blueprint, request, jsonify
from middleware.auth import auth_required
from utils.helpers import get_db, to_object_id
from models.note import create_note, note_to_dict
from datetime import datetime

notes_bp = Blueprint("notes", __name__)


# ─── List Notes ──────────────────────────────────────────────
@notes_bp.route("", methods=["GET"])
@auth_required
def list_notes():
    db = get_db()
    search = request.args.get("search", "").strip()
    tag = request.args.get("tag", "").strip()

    query = {"userId": request.user_id}

    if search:
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"content": {"$regex": search, "$options": "i"}},
        ]
    if tag:
        query["tags"] = {"$in": [tag]}

    notes = list(
        db.notes.find(query).sort("updatedAt", -1)
    )
    return jsonify({"notes": [note_to_dict(n) for n in notes]})


# ─── Create Note ─────────────────────────────────────────────
@notes_bp.route("", methods=["POST"])
@auth_required
def create_note_route():
    db = get_db()
    data = request.get_json(silent=True) or {}

    title = data.get("title", "").strip()
    content = data.get("content", "").strip()
    tags = data.get("tags", [])
    color = data.get("color", "#7c3aed")

    if not title and not content:
        return jsonify({"error": "Title or content is required"}), 400

    note_doc = create_note(request.user_id, title, content, tags, color)
    result = db.notes.insert_one(note_doc)
    note_doc["_id"] = result.inserted_id

    return jsonify({
        "message": "Note created",
        "note": note_to_dict(note_doc)
    }), 201


# ─── Update Note ─────────────────────────────────────────────
@notes_bp.route("/<note_id>", methods=["PUT"])
@auth_required
def update_note(note_id):
    db = get_db()
    oid = to_object_id(note_id)
    if not oid:
        return jsonify({"error": "Invalid note ID"}), 400

    note = db.notes.find_one({"_id": oid, "userId": request.user_id})
    if not note:
        return jsonify({"error": "Note not found"}), 404

    data = request.get_json(silent=True) or {}
    updates = {}
    for field in ("title", "content", "tags", "color"):
        if field in data:
            updates[field] = data[field]

    updates["updatedAt"] = datetime.utcnow()

    db.notes.update_one({"_id": oid}, {"$set": updates})
    note = db.notes.find_one({"_id": oid})
    return jsonify({"message": "Note updated", "note": note_to_dict(note)})


# ─── Delete Note ─────────────────────────────────────────────
@notes_bp.route("/<note_id>", methods=["DELETE"])
@auth_required
def delete_note(note_id):
    db = get_db()
    oid = to_object_id(note_id)
    if not oid:
        return jsonify({"error": "Invalid note ID"}), 400

    result = db.notes.delete_one({"_id": oid, "userId": request.user_id})
    if result.deleted_count == 0:
        return jsonify({"error": "Note not found"}), 404

    return jsonify({"message": "Note deleted"})
