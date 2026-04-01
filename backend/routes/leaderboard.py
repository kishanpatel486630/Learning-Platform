"""
Leaderboard Routes — Rankings, friends, races
GET    /api/leaderboard              — Get rankings
GET    /api/leaderboard/friends      — Get friends list
POST   /api/leaderboard/friends      — Add friend by email
DELETE /api/leaderboard/friends/<id> — Remove friend
GET    /api/leaderboard/races        — List user's races
POST   /api/leaderboard/races        — Create a race
GET    /api/leaderboard/races/<id>   — Get race details
POST   /api/leaderboard/races/<id>/join — Join a race
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from middleware.auth import auth_required
from utils.helpers import get_db, to_object_id
from models.race import create_race, race_to_dict

leaderboard_bp = Blueprint("leaderboard", __name__)


# ─── Get Rankings ─────────────────────────────────────────────
@leaderboard_bp.route("", methods=["GET"])
@auth_required
def get_rankings():
    db = get_db()
    sort_by = request.args.get("sort", "xp")  # xp / streak / questions
    limit = min(int(request.args.get("limit", 50)), 100)

    sort_field_map = {
        "xp": "xp",
        "streak": "streak.current",
        "questions": "totalQuestions",
    }
    sort_field = sort_field_map.get(sort_by, "xp")

    # Get current user for friend filtering
    user = db.users.find_one({"_id": to_object_id(request.user_id)})
    friends_only = request.args.get("friends") == "true"

    query = {}
    if friends_only and user:
        friend_ids = [to_object_id(fid) for fid in user.get("friends", [])]
        friend_ids.append(to_object_id(request.user_id))
        query["_id"] = {"$in": friend_ids}

    users = (
        db.users.find(query, {
            "name": 1, "email": 1, "photo": 1,
            "xp": 1, "streak": 1, "totalQuestions": 1,
            "examProgress": 1,
        })
        .sort(sort_field, -1)
        .limit(limit)
    )

    rankings = []
    for i, u in enumerate(users, 1):
        rankings.append({
            "rank": i,
            "id": str(u["_id"]),
            "name": u.get("name", "Anonymous"),
            "photo": u.get("photo", ""),
            "xp": u.get("xp", 0),
            "streak": (u.get("streak") or {}).get("current", 0),
            "totalQuestions": u.get("totalQuestions", 0),
            "isCurrentUser": str(u["_id"]) == request.user_id,
        })

    return jsonify({"rankings": rankings, "sortBy": sort_by})


# ─── Get Friends List ─────────────────────────────────────────
@leaderboard_bp.route("/friends", methods=["GET"])
@auth_required
def list_friends():
    db = get_db()
    user = db.users.find_one({"_id": to_object_id(request.user_id)})
    friend_ids = user.get("friends", []) if user else []

    friends = []
    for fid in friend_ids:
        friend = db.users.find_one(
            {"_id": to_object_id(fid)},
            {"name": 1, "email": 1, "photo": 1, "xp": 1, "streak": 1}
        )
        if friend:
            friends.append({
                "id": str(friend["_id"]),
                "name": friend.get("name", "Anonymous"),
                "email": friend.get("email", ""),
                "photo": friend.get("photo", ""),
                "xp": friend.get("xp", 0),
                "streak": (friend.get("streak") or {}).get("current", 0),
            })

    return jsonify({"friends": friends})


# ─── Add Friend ───────────────────────────────────────────────
@leaderboard_bp.route("/friends", methods=["POST"])
@auth_required
def add_friend():
    db = get_db()
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()

    if not email:
        return jsonify({"error": "Email is required"}), 400

    friend = db.users.find_one({"email": email})
    if not friend:
        return jsonify({"error": "User not found with that email"}), 404

    friend_id = str(friend["_id"])
    if friend_id == request.user_id:
        return jsonify({"error": "Cannot add yourself"}), 400

    # Add to both users' friend lists (mutual friendship)
    db.users.update_one(
        {"_id": to_object_id(request.user_id)},
        {"$addToSet": {"friends": friend_id}}
    )
    db.users.update_one(
        {"_id": friend["_id"]},
        {"$addToSet": {"friends": request.user_id}}
    )

    return jsonify({
        "message": "Friend added",
        "friend": {
            "id": friend_id,
            "name": friend.get("name", "Anonymous"),
            "email": friend.get("email", ""),
            "photo": friend.get("photo", ""),
            "xp": friend.get("xp", 0),
        }
    })


# ─── Remove Friend ───────────────────────────────────────────
@leaderboard_bp.route("/friends/<friend_id>", methods=["DELETE"])
@auth_required
def remove_friend(friend_id):
    db = get_db()

    # Remove from both users
    db.users.update_one(
        {"_id": to_object_id(request.user_id)},
        {"$pull": {"friends": friend_id}}
    )
    db.users.update_one(
        {"_id": to_object_id(friend_id)},
        {"$pull": {"friends": request.user_id}}
    )

    return jsonify({"message": "Friend removed"})


# ─── List Races ───────────────────────────────────────────────
@leaderboard_bp.route("/races", methods=["GET"])
@auth_required
def list_races():
    db = get_db()

    races = db.races.find({
        "participants.userId": request.user_id
    }).sort("createdAt", -1)

    return jsonify({"races": [race_to_dict(r) for r in races]})


# ─── Create Race ──────────────────────────────────────────────
@leaderboard_bp.route("/races", methods=["POST"])
@auth_required
def create_new_race():
    db = get_db()
    data = request.get_json(silent=True) or {}

    name = (data.get("name") or "").strip()
    goal = data.get("goal", "xp")          # xp / questions / streak
    target = data.get("target", 1000)      # goal target value
    days = data.get("days", 7)

    if not name:
        return jsonify({"error": "Race name is required"}), 400

    # Get creator's info
    user = db.users.find_one({"_id": to_object_id(request.user_id)})

    race = create_race(
        creator_id=request.user_id,
        name=name,
        goal=goal,
        days=days,
        participants=[{
            "userId": request.user_id,
            "name": user.get("name", "Anonymous") if user else "Anonymous",
            "progress": 0,
        }],
    )
    race["target"] = target

    result = db.races.insert_one(race)
    race["_id"] = result.inserted_id

    return jsonify({"race": race_to_dict(race)}), 201


# ─── Get Race Details ─────────────────────────────────────────
@leaderboard_bp.route("/races/<race_id>", methods=["GET"])
@auth_required
def get_race(race_id):
    db = get_db()
    oid = to_object_id(race_id)
    if not oid:
        return jsonify({"error": "Invalid race ID"}), 400

    race = db.races.find_one({"_id": oid})
    if not race:
        return jsonify({"error": "Race not found"}), 404

    return jsonify({"race": race_to_dict(race)})


# ─── Join Race ────────────────────────────────────────────────
@leaderboard_bp.route("/races/<race_id>/join", methods=["POST"])
@auth_required
def join_race(race_id):
    db = get_db()
    oid = to_object_id(race_id)
    if not oid:
        return jsonify({"error": "Invalid race ID"}), 400

    race = db.races.find_one({"_id": oid})
    if not race:
        return jsonify({"error": "Race not found"}), 404

    # Check if already joined
    for p in race.get("participants", []):
        if p.get("userId") == request.user_id:
            return jsonify({"error": "Already in this race"}), 400

    user = db.users.find_one({"_id": to_object_id(request.user_id)})
    db.races.update_one(
        {"_id": oid},
        {"$push": {"participants": {
            "userId": request.user_id,
            "name": user.get("name", "Anonymous") if user else "Anonymous",
            "progress": 0,
        }}}
    )

    updated = db.races.find_one({"_id": oid})
    return jsonify({"race": race_to_dict(updated)})
