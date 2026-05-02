from flask import Blueprint, request, jsonify, g
from bson import ObjectId

users_bp = Blueprint("users", __name__)

@users_bp.route("/", methods=["GET"])
def get_users():
    if not g.db:
        return jsonify({"error": "Database not connected"}), 500
        
    users = list(g.db.users.find({}, {"password": 0})) # Exclude passwords
    for u in users:
        u["_id"] = str(u["_id"])
        
    return jsonify({"users": users})

@users_bp.route("/<user_id>/ban", methods=["POST"])
def ban_user(user_id):
    if not g.db:
        return jsonify({"error": "Database not connected"}), 500
        
    try:
        g.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"banned": True}})
        return jsonify({"message": "User banned successfully"})
    except:
        return jsonify({"error": "Invalid user ID"}), 400
