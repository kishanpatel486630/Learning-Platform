"""
LearnPath — Flask Backend Application
Entry point for the API server.
"""
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from config import config
import os

# ── App Factory ──────────────────────────────────────────────
app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "..", "frontend"),
    static_url_path="",
)
app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = config.MAX_CONTENT_LENGTH

# ── CORS ─────────────────────────────────────────────────────
CORS(app, origins=config.CORS_ORIGINS, supports_credentials=True)

# ── MongoDB Connection ───────────────────────────────────────
mongo_client = MongoClient(config.MONGO_URI)
db = mongo_client[config.MONGO_DB_NAME]

# Make db accessible to routes
app.config["db"] = db


# ── Register Blueprints (API Routes) ────────────────────────
from routes.auth import auth_bp
from routes.user import user_bp
from routes.notes import notes_bp
from routes.exams import exams_bp
from routes.questions import questions_bp
from routes.planner import planner_bp
from routes.leaderboard import leaderboard_bp
from routes.ai import ai_bp
from routes.skills import skills_bp
from routes.admin import admin_bp

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(user_bp, url_prefix="/api/user")
app.register_blueprint(notes_bp, url_prefix="/api/notes")
app.register_blueprint(exams_bp, url_prefix="/api/exams")
app.register_blueprint(questions_bp, url_prefix="/api/questions")
app.register_blueprint(planner_bp, url_prefix="/api/planner")
app.register_blueprint(leaderboard_bp, url_prefix="/api/leaderboard")
app.register_blueprint(ai_bp, url_prefix="/api/ai")
app.register_blueprint(skills_bp, url_prefix="/api/skills")
app.register_blueprint(admin_bp, url_prefix="/api/admin")


# ── Serve Frontend ───────────────────────────────────────────
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "login.html")


@app.route("/<path:filename>")
def serve_frontend(filename):
    # API routes that don't exist should return JSON 404, not login.html
    if filename.startswith("api/"):
        return jsonify({"error": "API endpoint not found"}), 404
    filepath = os.path.join(app.static_folder, filename)
    if os.path.isfile(filepath):
        return send_from_directory(app.static_folder, filename)
    # SPA fallback — serve index for unknown frontend routes
    return send_from_directory(app.static_folder, "index.html")


# ── Health Check ─────────────────────────────────────────────
@app.route("/api/health")
def health():
    try:
        mongo_client.admin.command("ping")
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return jsonify({
        "status": "ok",
        "database": db_status,
        "version": "2.0.0"
    })


# ── Error Handlers ───────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "File too large (max 5MB)"}), 413


# ── Run ──────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
    print("🚀 LearnPath API running on http://localhost:5000")
    print(f"📦 Database: {config.MONGO_DB_NAME}")
    print(f"🌐 CORS: {config.CORS_ORIGINS}")
    app.run(host="0.0.0.0", port=5000, debug=config.DEBUG)
