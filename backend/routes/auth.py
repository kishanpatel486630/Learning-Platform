"""
Auth Routes — Register, Login, Refresh Token, Password Reset
POST /api/auth/register
POST /api/auth/login
POST /api/auth/refresh
GET  /api/auth/me
"""
from flask import Blueprint, request, jsonify
from models.user import create_user, verify_password, user_to_dict
from middleware.auth import create_access_token, create_refresh_token, decode_token, auth_required
from utils.helpers import get_db

auth_bp = Blueprint("auth", __name__)


# ─── Register ────────────────────────────────────────────────
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password are required"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    db = get_db()

    # Check if email already exists
    if db.users.find_one({"email": email}):
        return jsonify({"error": "Email already registered"}), 409

    # Create user
    user_doc = create_user(name, email, password)
    result = db.users.insert_one(user_doc)
    user_id = str(result.inserted_id)

    # Generate tokens
    access_token = create_access_token(user_id, email)
    refresh_token = create_refresh_token(user_id)

    return jsonify({
        "message": "Registration successful",
        "accessToken": access_token,
        "refreshToken": refresh_token,
        "user": {
            "_id": user_id,
            "name": name,
            "email": email,
            "profileComplete": False,
        }
    }), 201


# ─── Login ───────────────────────────────────────────────────
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    db = get_db()
    user = db.users.find_one({"email": email})

    if not user or not verify_password(password, user["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    user_id = str(user["_id"])
    access_token = create_access_token(user_id, email)
    refresh_token = create_refresh_token(user_id)

    return jsonify({
        "message": "Login successful",
        "accessToken": access_token,
        "refreshToken": refresh_token,
        "user": user_to_dict(user),
    })


# ─── Refresh Token ───────────────────────────────────────────
@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    data = request.get_json(silent=True) or {}
    token = data.get("refreshToken", "")

    if not token:
        return jsonify({"error": "Refresh token required"}), 400

    payload = decode_token(token)
    if not payload or payload.get("type") != "refresh":
        return jsonify({"error": "Invalid refresh token"}), 401

    user_id = payload["sub"]
    db = get_db()
    from bson import ObjectId
    user = db.users.find_one({"_id": ObjectId(user_id)})

    if not user:
        return jsonify({"error": "User not found"}), 404

    access_token = create_access_token(user_id, user["email"])
    return jsonify({"accessToken": access_token})


# ─── Get Current User ────────────────────────────────────────
@auth_bp.route("/me", methods=["GET"])
@auth_required
def get_me():
    db = get_db()
    from bson import ObjectId
    user = db.users.find_one({"_id": ObjectId(request.user_id)})

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"user": user_to_dict(user)})
