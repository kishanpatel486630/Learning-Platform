"""
Note Model — MongoDB schema helpers for the notes collection.
"""
from datetime import datetime


def create_note(user_id, title, content, tags=None, color="#7c3aed"):
    """Build a new note document."""
    now = datetime.utcnow()
    return {
        "userId": user_id,
        "title": title.strip() or "Untitled",
        "content": content.strip(),
        "tags": tags or [],
        "color": color,
        "createdAt": now,
        "updatedAt": now,
    }


def note_to_dict(note):
    """Convert a MongoDB note document to a JSON-safe dict."""
    note["_id"] = str(note["_id"])
    for field in ("createdAt", "updatedAt"):
        if isinstance(note.get(field), datetime):
            note[field] = note[field].isoformat()
    return note
