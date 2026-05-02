from flask import Blueprint, request, jsonify
import os
import jwt
import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# Secure Admin Credentials (In production, move these to .env)
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin.kishan@gmail.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Admin@123")
JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-key")

@admin_bp.route("/login", methods=["POST"])
def admin_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        # Create a JWT token specifically with an admin role
        token = jwt.encode({
            "user_id": "admin_system",
            "role": "admin",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, JWT_SECRET, algorithm="HS256")
        
        return jsonify({
            "message": "Admin login successful",
            "token": token
        }), 200
    
    return jsonify({"error": "Invalid admin credentials"}), 401

# A decorator to protect admin routes
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Admin token is missing"}), 401
        
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            if payload.get("role") != "admin":
                return jsonify({"error": "Unauthorized access. Admins only."}), 403
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
            
    return decorated

@admin_bp.route("/dashboard-stats", methods=["GET"])
@admin_required
def get_stats():
    from db import get_db
    db = get_db()
    
    user_count = db.users.count_documents({})
    # Just mock stats for now to show the dashboard works
    return jsonify({
        "totalUsers": user_count,
        "activeRoadmaps": 2,
        "totalQuestions": 1500,
        "serverStatus": "Online"
    }), 200
