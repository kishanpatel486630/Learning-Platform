"""
Utility helpers shared across routes.
"""
from flask import current_app
from bson import ObjectId


def get_db():
    """Get the MongoDB database instance."""
    return current_app.config["db"]


def to_object_id(id_string):
    """Safely convert string to ObjectId, returns None on failure."""
    try:
        return ObjectId(id_string)
    except Exception:
        return None


def update_streak(user_doc):
    """Recalculate streak based on lastStudyDate."""
    from datetime import datetime, timedelta

    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
    last = user_doc.get("lastStudyDate", "")

    if last == today_str:
        return user_doc.get("streak", 0)  # already counted today
    elif last == yesterday:
        return user_doc.get("streak", 0) + 1
    else:
        return 1  # streak resets


def add_xp_to_user(db, user_id, amount, source="general"):
    """Add XP to a user and update activity log + streak."""
    from datetime import datetime

    today = datetime.utcnow().strftime("%Y-%m-%d")

    user = db.users.find_one({"_id": to_object_id(user_id)})
    if not user:
        return None

    new_xp = user.get("xp", 0) + amount
    activity_log = user.get("activityLog", {})
    activity_log[today] = activity_log.get(today, 0) + amount

    streak = update_streak(user)

    db.users.update_one(
        {"_id": to_object_id(user_id)},
        {
            "$set": {
                "xp": new_xp,
                "streak": streak,
                "lastStudyDate": today,
                "activityLog": activity_log,
            }
        },
    )
    return new_xp
