from flask import Blueprint, request, jsonify, g
from bson import ObjectId

users_bp = Blueprint("users", __name__)

def serialize_user(u):
    u["_id"] = str(u["_id"])
    return u

@users_bp.route("/", methods=["GET"])
def get_users():
    if not g.db:
        return jsonify({"error": "Database not connected"}), 500
    users = list(g.db.users.find({}, {"password": 0}))
    return jsonify({"users": [serialize_user(u) for u in users]})

@users_bp.route("/<user_id>/ban", methods=["POST"])
def ban_user(user_id):
    if not g.db:
        return jsonify({"error": "Database not connected"}), 500
    try:
        g.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"banned": True}})
        return jsonify({"message": "User banned successfully"})
    except Exception:
        return jsonify({"error": "Invalid user ID"}), 400

@users_bp.route("/<user_id>/unban", methods=["POST"])
def unban_user(user_id):
    if not g.db:
        return jsonify({"error": "Database not connected"}), 500
    try:
        g.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"banned": False}})
        return jsonify({"message": "User unbanned successfully"})
    except Exception:
        return jsonify({"error": "Invalid user ID"}), 400
