"""
User Routes — Profile management, progress, XP
GET    /api/user/profile
PUT    /api/user/profile
PUT    /api/user/profile-setup
PUT    /api/user/settings
GET    /api/user/progress
POST   /api/user/xp
"""
from flask import Blueprint, request, jsonify
from middleware.auth import auth_required
from utils.helpers import get_db, to_object_id, add_xp_to_user
from models.user import user_to_dict

user_bp = Blueprint("user", __name__)


# ─── Get Profile ─────────────────────────────────────────────
@user_bp.route("/profile", methods=["GET"])
@auth_required
def get_profile():
    db = get_db()
    user = db.users.find_one({"_id": to_object_id(request.user_id)})
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"user": user_to_dict(user)})


# ─── Update Profile ──────────────────────────────────────────
@user_bp.route("/profile", methods=["PUT"])
@auth_required
def update_profile():
    db = get_db()
    data = request.get_json(silent=True) or {}

    # Allowed fields to update
    allowed = [
        "name", "phone", "photo", "avatarColor", "bio",
        "qualification", "college", "branch", "year", "cgpa",
        "careerGoal", "dailyHours", "preferredTime", "level",
    ]
    updates = {k: data[k] for k in allowed if k in data}

    if not updates:
        return jsonify({"error": "No valid fields to update"}), 400

    db.users.update_one(
        {"_id": to_object_id(request.user_id)},
        {"$set": updates}
    )
    user = db.users.find_one({"_id": to_object_id(request.user_id)})
    return jsonify({"message": "Profile updated", "user": user_to_dict(user)})


# ─── Profile Setup (onboarding) ──────────────────────────────
@user_bp.route("/profile-setup", methods=["PUT"])
@auth_required
def profile_setup():
    db = get_db()
    data = request.get_json(silent=True) or {}

    setup_fields = [
        "name", "phone", "photo", "avatarColor", "bio",
        "qualification", "college", "branch", "year", "cgpa",
        "targetCompanies", "targetExams", "interviewPrep", "careerGoal",
        "dailyHours", "preferredTime",
    ]
    updates = {k: data[k] for k in setup_fields if k in data}
    updates["profileComplete"] = True
    updates["onboarded"] = True

    db.users.update_one(
        {"_id": to_object_id(request.user_id)},
        {"$set": updates}
    )
    user = db.users.find_one({"_id": to_object_id(request.user_id)})
    return jsonify({"message": "Profile setup complete", "user": user_to_dict(user)})


# ─── Update Settings ─────────────────────────────────────────
@user_bp.route("/settings", methods=["PUT"])
@auth_required
def update_settings():
    db = get_db()
    data = request.get_json(silent=True) or {}

    allowed = [
        "theme", "geminiApiKey", "pomodoroDuration",
        "dailyHours", "level", "reminders", "sounds",
    ]
    updates = {k: data[k] for k in allowed if k in data}

    if not updates:
        return jsonify({"error": "No valid fields to update"}), 400

    db.users.update_one(
        {"_id": to_object_id(request.user_id)},
        {"$set": updates}
    )
    return jsonify({"message": "Settings updated"})


# ─── Get Progress (stats) ────────────────────────────────────
@user_bp.route("/progress", methods=["GET"])
@auth_required
def get_progress():
    db = get_db()
    user = db.users.find_one({"_id": to_object_id(request.user_id)})
    if not user:
        return jsonify({"error": "User not found"}), 404

    notes_count = db.notes.count_documents({"userId": request.user_id})

    return jsonify({
        "xp": user.get("xp", 0),
        "streak": user.get("streak", 0),
        "badges": user.get("badges", []),
        "studyMinutes": user.get("studyMinutes", 0),
        "pomodorosTotal": user.get("pomodorosTotal", 0),
        "activityLog": user.get("activityLog", {}),
        "examProgress": user.get("examProgress", {}),
        "interviewProgress": user.get("interviewProgress", {}),
        "answeredQuestions": user.get("answeredQuestions", {}),
        "bookmarkedQuestions": user.get("bookmarkedQuestions", []),
        "notesCount": notes_count,
        "friendsCount": len(user.get("friends", [])),
    })


# ─── Add XP ──────────────────────────────────────────────────
@user_bp.route("/xp", methods=["POST"])
@auth_required
def add_xp():
    db = get_db()
    data = request.get_json(silent=True) or {}
    amount = data.get("amount", 0)
    source = data.get("source", "general")

    if not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"error": "Invalid XP amount"}), 400

    new_xp = add_xp_to_user(db, request.user_id, int(amount), source)
    return jsonify({"xp": new_xp, "added": int(amount)})


# ─── Update Exam Progress ────────────────────────────────────
@user_bp.route("/exam-progress", methods=["PUT"])
@auth_required
def update_exam_progress():
    db = get_db()
    data = request.get_json(silent=True) or {}
    exam_id = data.get("examId")
    progress = data.get("progress")

    if not exam_id or progress is None:
        return jsonify({"error": "examId and progress are required"}), 400

    db.users.update_one(
        {"_id": to_object_id(request.user_id)},
        {"$set": {f"examProgress.{exam_id}": progress}}
    )
    return jsonify({"message": "Exam progress updated"})


# ─── Update Interview Progress ────────────────────────────────
@user_bp.route("/interview-progress", methods=["PUT"])
@auth_required
def update_interview_progress():
    db = get_db()
    data = request.get_json(silent=True) or {}
    company = data.get("company")
    progress = data.get("progress")

    if not company or progress is None:
        return jsonify({"error": "company and progress are required"}), 400

    db.users.update_one(
        {"_id": to_object_id(request.user_id)},
        {"$set": {f"interviewProgress.{company}": progress}}
    )
    return jsonify({"message": "Interview progress updated"})


# ─── Answer Question ─────────────────────────────────────────
@user_bp.route("/answer-question", methods=["POST"])
@auth_required
def answer_question():
    db = get_db()
    data = request.get_json(silent=True) or {}
    question_id = data.get("questionId")
    correct = data.get("correct", False)

    if not question_id:
        return jsonify({"error": "questionId is required"}), 400

    db.users.update_one(
        {"_id": to_object_id(request.user_id)},
        {"$set": {f"answeredQuestions.{question_id}": correct}}
    )

    # Add XP
    xp = 10 if correct else 2
    new_xp = add_xp_to_user(db, request.user_id, xp, "question")
    return jsonify({"xp": new_xp, "correct": correct})


# ─── Bookmark Question ───────────────────────────────────────
@user_bp.route("/bookmark", methods=["POST"])
@auth_required
def toggle_bookmark():
    db = get_db()
    data = request.get_json(silent=True) or {}
    question_id = data.get("questionId")
    bookmarked = data.get("bookmarked", True)

    if not question_id:
        return jsonify({"error": "questionId is required"}), 400

    if bookmarked:
        db.users.update_one(
            {"_id": to_object_id(request.user_id)},
            {"$addToSet": {"bookmarkedQuestions": question_id}}
        )
    else:
        db.users.update_one(
            {"_id": to_object_id(request.user_id)},
            {"$pull": {"bookmarkedQuestions": question_id}}
        )
    return jsonify({"message": "Bookmark updated"})
