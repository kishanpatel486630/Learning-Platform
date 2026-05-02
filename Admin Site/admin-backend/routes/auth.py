from flask import Blueprint, request, jsonify
import jwt
import datetime
from config import config

auth_bp = Blueprint("auth", __name__)

# Hardcoded super admin credentials
ADMIN_EMAIL = "admin@learnpath.com"
ADMIN_PASSWORD = "admin" # Simple password for demonstration

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")

    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        token = jwt.encode({
            "email": email,
            "exp": datetime.datetime.utcnow() + config.JWT_ACCESS_EXPIRY
        }, config.JWT_SECRET, algorithm="HS256")
        
        return jsonify({
            "message": "Admin login successful",
            "token": token,
            "admin": {"email": email, "role": "Super Admin"}
        }), 200

    return jsonify({"error": "Invalid admin credentials"}), 401
