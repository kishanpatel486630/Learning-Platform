"""
User Model — MongoDB schema helpers for the users collection.
"""
from datetime import datetime
import bcrypt


def create_user(name, email, password):
    """Build a new user document."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)

    return {
        # ── Auth ─────────────────────────────
        "email": email.lower().strip(),
        "password": hashed.decode("utf-8"),
        "createdAt": datetime.utcnow(),

        # ── Personal Info ────────────────────
        "name": name.strip(),
        "phone": "",
        "photo": "",
        "avatarColor": "#7c3aed",
        "bio": "",

        # ── Education ────────────────────────
        "qualification": "",
        "college": "",
        "branch": "",
        "year": "",
        "cgpa": "",

        # ── Career Goals ─────────────────────
        "targetCompanies": [],
        "targetExams": [],
        "interviewPrep": False,
        "careerGoal": "",

        # ── Study Preferences ────────────────
        "dailyHours": 1,
        "preferredTime": "morning",
        "level": "beginner",

        # ── Progress & Gamification ──────────
        "xp": 0,
        "streak": 0,
        "lastStudyDate": None,
        "badges": [],
        "studyMinutes": 0,
        "pomodorosTotal": 0,
        "activityLog": {},       # { "2026-03-05": 120 }

        # ── Exam Progress ────────────────────
        "examProgress": {},
        "interviewProgress": {},

        # ── Questions ────────────────────────
        "answeredQuestions": {},  # { "qid": true/false }
        "bookmarkedQuestions": [],

        # ── Social ───────────────────────────
        "friends": [],           # [{ name, color, addedAt }]

        # ── Settings ─────────────────────────
        "theme": "dark",
        "geminiApiKey": "",
        "pomodoroDuration": 25,
        "reminders": True,
        "sounds": True,

        # ── Profile Status ───────────────────
        "onboarded": False,
        "profileComplete": False,
    }


def verify_password(plain_password, hashed_password):
    """Check a password against its bcrypt hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def user_to_dict(user):
    """Convert a MongoDB user document to a JSON-safe dict (strips password)."""
    user["_id"] = str(user["_id"])
    user.pop("password", None)
    if isinstance(user.get("createdAt"), datetime):
        user["createdAt"] = user["createdAt"].isoformat()
    return user
