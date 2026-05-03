"""
Exams Routes — Exam categories, sections, quiz results
GET    /api/exams                    — List all exam categories
GET    /api/exams/<exam_id>          — Get exam details
POST   /api/exams/<exam_id>/results  — Submit quiz results for a section
"""
from flask import Blueprint, request, jsonify
from middleware.auth import auth_required
from utils.helpers import get_db, to_object_id, add_xp_to_user

exams_bp = Blueprint("exams", __name__)

# ── Static exam data (mirrors exams-data.js) ────────────────
# Loaded from the frontend's exams-data.js structure
# In production, this would be stored in MongoDB
EXAM_CATEGORIES = {
    "tcs-nqt": {
        "name": "TCS NQT",
        "company": "TCS",
        "icon": "🏢",
        "color": "#0066b3",
        "type": "placement",
        "description": "TCS National Qualifier Test — gateway to TCS hiring",
        "duration": "180 min",
        "totalQuestions": 90,
        "sections": ["verbal", "aptitude", "reasoning", "coding"],
    },
    "infosys": {
        "name": "Infosys SP & DSE",
        "company": "Infosys",
        "icon": "🔷",
        "color": "#007cc3",
        "type": "placement",
        "description": "Infosys System Engineer & Digital Specialist placement exam",
        "duration": "170 min",
        "totalQuestions": 85,
        "sections": ["aptitude", "reasoning", "verbal", "coding"],
    },
    "wipro": {
        "name": "Wipro NLTH",
        "company": "Wipro",
        "icon": "🟣",
        "color": "#44166b",
        "type": "placement",
        "description": "Wipro National Level Talent Hunt exam",
        "duration": "150 min",
        "totalQuestions": 80,
        "sections": ["aptitude", "verbal", "coding"],
    },
    "cognizant": {
        "name": "Cognizant GenC",
        "company": "Cognizant",
        "icon": "🔵",
        "color": "#0033a1",
        "type": "placement",
        "description": "Cognizant GenC hiring assessment",
        "duration": "120 min",
        "totalQuestions": 70,
        "sections": ["aptitude", "reasoning", "coding"],
    },
    "accenture": {
        "name": "Accenture Hiring",
        "company": "Accenture",
        "icon": "🟢",
        "color": "#a100ff",
        "type": "placement",
        "description": "Accenture campus hiring assessment",
        "duration": "120 min",
        "totalQuestions": 70,
        "sections": ["aptitude", "verbal", "reasoning", "coding"],
    },
    "gate-cs": {
        "name": "GATE CS/IT",
        "company": "GATE",
        "icon": "🎓",
        "color": "#d32f2f",
        "type": "govt",
        "description": "Graduate Aptitude Test in Engineering — CS/IT",
        "duration": "180 min",
        "totalQuestions": 65,
        "sections": ["engineering-math", "algorithms", "os", "dbms", "networks", "compiler", "toc"],
    },
    "dsa-placement": {
        "name": "DSA & Coding",
        "company": "All",
        "icon": "💻",
        "color": "#2e7d32",
        "type": "coding",
        "description": "Data Structures & Algorithms for coding interviews",
        "duration": "Varies",
        "totalQuestions": 200,
        "sections": ["arrays", "strings", "linked-lists", "trees", "graphs", "dp", "sorting", "searching"],
    },
}


# ─── List All Exam Categories ────────────────────────────────
@exams_bp.route("", methods=["GET"])
@auth_required
def list_exams():
    exam_type = request.args.get("type")  # placement / govt / coding
    exams = []

    for exam_id, exam in EXAM_CATEGORIES.items():
        if exam_type and exam["type"] != exam_type:
            continue
        exams.append({"id": exam_id, **exam})

    return jsonify({"exams": exams})


# ─── Get Exam Details ────────────────────────────────────────
@exams_bp.route("/<exam_id>", methods=["GET"])
@auth_required
def get_exam(exam_id):
    exam = EXAM_CATEGORIES.get(exam_id)
    if not exam:
        return jsonify({"error": "Exam not found"}), 404

    # Get user's progress for this exam
    db = get_db()
    user = db.users.find_one({"_id": to_object_id(request.user_id)})
    progress = (user.get("examProgress", {}) or {}).get(exam_id, {})

    return jsonify({
        "exam": {"id": exam_id, **exam},
        "progress": progress,
    })


# ─── Submit Quiz Results ─────────────────────────────────────
@exams_bp.route("/<exam_id>/results", methods=["POST"])
@auth_required
def submit_results(exam_id):
    if exam_id not in EXAM_CATEGORIES:
        return jsonify({"error": "Exam not found"}), 404

    db = get_db()
    data = request.get_json(silent=True) or {}

    section = data.get("section")
    score = data.get("score", 0)
    total = data.get("total", 0)
    answers = data.get("answers", {})  # { "qid": selected_index }

    if not section:
        return jsonify({"error": "Section is required"}), 400

    # Update exam progress
    progress_key = f"examProgress.{exam_id}.sections.{section}"
    db.users.update_one(
        {"_id": to_object_id(request.user_id)},
        {"$set": {
            progress_key: {
                "score": score,
                "total": total,
                "completedAt": __import__("datetime").datetime.utcnow().isoformat(),
            }
        }}
    )

    # Update answered questions
    for qid, answer in answers.items():
        correct = answer.get("correct", False) if isinstance(answer, dict) else False
        db.users.update_one(
            {"_id": to_object_id(request.user_id)},
            {"$set": {f"answeredQuestions.{qid}": correct}}
        )

    # Award XP
    xp_earned = (score * 10) + (total * 2)
    new_xp = add_xp_to_user(db, request.user_id, xp_earned, f"exam-{exam_id}")

    return jsonify({
        "message": "Results saved",
        "score": score,
        "total": total,
        "xpEarned": xp_earned,
        "totalXp": new_xp,
    })
