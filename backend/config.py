"""
LearnPath Backend Configuration
All settings loaded from environment variables with sensible defaults.
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration."""

    # ── Flask ───────────────────────────────────────
    SECRET_KEY = os.getenv("SECRET_KEY", "learnpath-dev-secret-change-me")
    DEBUG = os.getenv("FLASK_DEBUG", "true").lower() == "true"

    # ── MongoDB ─────────────────────────────────────
    MONGO_URI = os.getenv(
        "MONGO_URI", "mongodb://localhost:27017/learnpath"
    )
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "learnpath")

    # ── JWT ──────────────────────────────────────────
    JWT_SECRET = os.getenv("JWT_SECRET", "learnpath-jwt-secret-change-me")
    JWT_ACCESS_EXPIRY = timedelta(
        hours=int(os.getenv("JWT_ACCESS_HOURS", "24"))
    )
    JWT_REFRESH_EXPIRY = timedelta(
        days=int(os.getenv("JWT_REFRESH_DAYS", "30"))
    )

    # ── Gemini AI ────────────────────────────────────
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    # ── CORS ─────────────────────────────────────────
    CORS_ORIGINS = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5000,http://127.0.0.1:5000,http://localhost:5500,http://127.0.0.1:5500,http://localhost:3000"
    ).split(",")

    # ── File Uploads ─────────────────────────────────
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB
    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "uploads"
    )


config = Config()
