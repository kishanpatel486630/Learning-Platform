"""
Question Model — MongoDB schema helpers for the questions collection.
"""
from datetime import datetime


def create_question(topic, exam_type, question_text, options, correct, explanation, difficulty="medium", category="general", created_by=None):
    """Build a new question document."""
    return {
        "topic": topic,
        "examType": exam_type,
        "question": question_text,
        "options": options,
        "correct": correct,          # index of correct option (0-3)
        "explanation": explanation,
        "difficulty": difficulty,     # easy / medium / hard
        "category": category,        # aptitude / verbal / coding / reasoning
        "createdBy": created_by,     # user_id or "ai" or "system"
        "createdAt": datetime.utcnow(),
    }


def question_to_dict(q):
    """Convert a MongoDB question document to a JSON-safe dict."""
    q["_id"] = str(q["_id"])
    if isinstance(q.get("createdAt"), datetime):
        q["createdAt"] = q["createdAt"].isoformat()
    return q
