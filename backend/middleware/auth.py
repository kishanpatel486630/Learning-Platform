"""
JWT Authentication Middleware
Provides token creation and a decorator to protect routes.
"""
import jwt
from datetime import datetime, timezone
from functools import wraps
from flask import request, jsonify, current_app
from config import config


def create_access_token(user_id, email):
    """Generate a JWT access token."""
    payload = {
        "sub": str(user_id),
        "email": email,
        "type": "access",
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + config.JWT_ACCESS_EXPIRY,
    }
    return jwt.encode(payload, config.JWT_SECRET, algorithm="HS256")


def create_refresh_token(user_id):
    """Generate a JWT refresh token (longer-lived)."""
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + config.JWT_REFRESH_EXPIRY,
    }
    return jwt.encode(payload, config.JWT_SECRET, algorithm="HS256")


def decode_token(token):
    """Decode and verify a JWT token. Returns the payload dict or None."""
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def auth_required(f):
    """Decorator: require a valid JWT in the Authorization header."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Try Authorization: Bearer <token>
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]

        if not token:
            return jsonify({"error": "Authentication required"}), 401

        payload = decode_token(token)
        if not payload or payload.get("type") != "access":
            return jsonify({"error": "Invalid or expired token"}), 401

        # Attach user info to request
        request.user_id = payload["sub"]
        request.user_email = payload.get("email", "")

        return f(*args, **kwargs)

    return decorated
