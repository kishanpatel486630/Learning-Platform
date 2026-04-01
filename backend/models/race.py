"""
Race Model — MongoDB schema helpers for the races/leaderboard collection.
"""
from datetime import datetime, timedelta


def create_race(creator_id, name, goal="xp", days=7, participants=None):
    """Build a new race document."""
    now = datetime.utcnow()
    return {
        "creatorId": creator_id,
        "name": name.strip(),
        "goal": goal,           # xp / questions / streak / studyTime
        "startDate": now,
        "endDate": now + timedelta(days=days),
        "participants": participants or [],  # [{ userId, name, color }]
        "scores": {},           # { "userId": score }
        "createdAt": now,
    }


def race_to_dict(race):
    """Convert a MongoDB race document to a JSON-safe dict."""
    race["_id"] = str(race["_id"])
    for field in ("startDate", "endDate", "createdAt"):
        if isinstance(race.get(field), datetime):
            race[field] = race[field].isoformat()
    return race
