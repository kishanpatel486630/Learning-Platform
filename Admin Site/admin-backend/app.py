import os
from flask import Flask, jsonify, request, g, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
import jwt

from config import config

app = Flask(__name__, static_folder="../admin-frontend", static_url_path="")
CORS(app, origins=config.CORS_ORIGINS, supports_credentials=True)
app.config.from_object(config)

# MongoDB Connection
try:
    client = MongoClient(config.MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client[config.MONGO_DB_NAME]
    print(f"📦 Admin connected to Database: {config.MONGO_DB_NAME}")
except Exception as e:
    print(f"❌ Database connection error: {e}")
    db = None

# Context processor for db access in routes
@app.before_request
def before_request():
    g.db = db  # db is a pymongo Database object or None
    if request.path.startswith("/api/") and request.path != "/api/auth/login":
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid token"}), 401
            
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, config.JWT_SECRET, algorithms=["HS256"])
            g.admin_email = payload.get("email")
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

# Import Routes
from routes.auth import auth_bp
from routes.users_manage import users_bp
from routes.roadmaps_manage import roadmaps_bp

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(users_bp, url_prefix="/api/users")
app.register_blueprint(roadmaps_bp, url_prefix="/api/roadmaps")

# Serve Frontend
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    print("🛡️ LearnPath Admin API running on http://localhost:5001")
    app.run(host="0.0.0.0", port=5001, debug=config.DEBUG)
