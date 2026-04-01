"""
Questions Routes — Question bank CRUD + filtering
GET    /api/questions             — List questions (filterable)
POST   /api/questions             — Create a question
GET    /api/questions/<id>        — Get single question
DELETE /api/questions/<id>        — Delete question (owner only)
"""
from flask import Blueprint, request, jsonify
from bson import ObjectId
from middleware.auth import auth_required
from utils.helpers import get_db, to_object_id
from models.question import create_question, question_to_dict
import math

questions_bp = Blueprint("questions", __name__)


# ─── List Questions (with filters & pagination) ──────────────
@questions_bp.route("", methods=["GET"])
@auth_required
def list_questions():
    db = get_db()

    # Filters
    category = request.args.get("category")          # arrays, dp, os, etc.
    exam_type = request.args.get("exam")              # tcs-nqt, gate-cs, etc.
    difficulty = request.args.get("difficulty")        # easy, medium, hard
    search = request.args.get("search", "").strip()
    bookmarked = request.args.get("bookmarked")       # "true"
    page = max(int(request.args.get("page", 1)), 1)
    limit = min(int(request.args.get("limit", 20)), 50)

    query = {}

    if category:
        query["category"] = category
    if exam_type:
        query["examType"] = exam_type
    if difficulty:
        query["difficulty"] = difficulty
    if search:
        query["$or"] = [
            {"questionText": {"$regex": search, "$options": "i"}},
            {"topic": {"$regex": search, "$options": "i"}},
        ]

    # Bookmarked filter — get user's bookmarks first
    if bookmarked == "true":
        user = db.users.find_one({"_id": to_object_id(request.user_id)})
        bm_ids = user.get("bookmarkedQuestions", []) if user else []
        obj_ids = [to_object_id(bid) for bid in bm_ids if bid]
        query["_id"] = {"$in": obj_ids}

    total = db.questions.count_documents(query)
    skip = (page - 1) * limit

    questions = (
        db.questions.find(query)
        .sort("createdAt", -1)
        .skip(skip)
        .limit(limit)
    )

    return jsonify({
        "questions": [question_to_dict(q) for q in questions],
        "total": total,
        "page": page,
        "pages": math.ceil(total / limit) if total else 1,
    })


# ─── Create Question ─────────────────────────────────────────
@questions_bp.route("", methods=["POST"])
@auth_required
def add_question():
    db = get_db()
    data = request.get_json(silent=True) or {}

    required = ["topic", "questionText", "options", "correct"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    options = data["options"]
    if not isinstance(options, list) or len(options) < 2:
        return jsonify({"error": "At least 2 options required"}), 400

    correct = data["correct"]
    if not isinstance(correct, int) or correct < 0 or correct >= len(options):
        return jsonify({"error": "Invalid correct answer index"}), 400

    question = create_question(
        topic=data["topic"],
        exam_type=data.get("examType", "general"),
        question_text=data["questionText"],
        options=options,
        correct=correct,
        explanation=data.get("explanation", ""),
        difficulty=data.get("difficulty", "medium"),
        category=data.get("category", "general"),
        created_by=request.user_id,
    )

    result = db.questions.insert_one(question)
    question["_id"] = result.inserted_id

    return jsonify({"question": question_to_dict(question)}), 201


# ─── Get Single Question ─────────────────────────────────────
@questions_bp.route("/<question_id>", methods=["GET"])
@auth_required
def get_question(question_id):
    db = get_db()
    oid = to_object_id(question_id)
    if not oid:
        return jsonify({"error": "Invalid question ID"}), 400

    question = db.questions.find_one({"_id": oid})
    if not question:
        return jsonify({"error": "Question not found"}), 404

    return jsonify({"question": question_to_dict(question)})


# ─── Delete Question ──────────────────────────────────────────
@questions_bp.route("/<question_id>", methods=["DELETE"])
@auth_required
def delete_question(question_id):
    db = get_db()
    oid = to_object_id(question_id)
    if not oid:
        return jsonify({"error": "Invalid question ID"}), 400

    question = db.questions.find_one({"_id": oid})
    if not question:
        return jsonify({"error": "Question not found"}), 404

    if question.get("createdBy") != request.user_id:
        return jsonify({"error": "Unauthorized"}), 403

    db.questions.delete_one({"_id": oid})
    return jsonify({"message": "Question deleted"})
