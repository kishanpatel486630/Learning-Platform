"""
Skills Routes — purely dynamic from MongoDB.
Static data removed. Admin manages all roadmaps via /admin.
"""
from flask import Blueprint, request, jsonify
from middleware.auth import auth_required
from utils.helpers import get_db, to_object_id

skills_bp = Blueprint("skills", __name__)


@skills_bp.route("/roadmaps", methods=["GET"])
@auth_required
def get_roadmaps():
    """Return only published roadmaps from DB. Completely dynamic — no static data."""
    db = get_db()
    roadmaps = list(db.roadmaps.find({"is_published": True}))
    for r in roadmaps:
        r["_id"] = str(r["_id"])
    return jsonify({"roadmaps": roadmaps})


@skills_bp.route("/progress", methods=["GET"])
@auth_required
def get_progress():
    db = get_db()
    user = db.users.find_one({"_id": to_object_id(request.user_id)})
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"skillsProgress": user.get("skillsProgress", {})})


@skills_bp.route("/progress", methods=["POST"])
@auth_required
def update_progress():
    db = get_db()
    data = request.get_json(silent=True) or {}
    skill_id = data.get("skillId")
    node_id = data.get("nodeId")
    completed = data.get("completed", True)

    if not skill_id or not node_id:
        return jsonify({"error": "skillId and nodeId are required"}), 400

    if completed:
        db.users.update_one(
            {"_id": to_object_id(request.user_id)},
            {"$addToSet": {f"skillsProgress.{skill_id}": node_id}}
        )
    else:
        db.users.update_one(
            {"_id": to_object_id(request.user_id)},
            {"$pull": {f"skillsProgress.{skill_id}": node_id}}
        )

    return jsonify({"message": "Skill progress updated"})
