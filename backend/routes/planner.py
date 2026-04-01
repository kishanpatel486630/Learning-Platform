"""
Planner Routes — Study planner tasks + Pomodoro tracking
GET    /api/planner               — List tasks (by date range)
POST   /api/planner               — Create a task
PUT    /api/planner/<id>          — Update / toggle task
DELETE /api/planner/<id>          — Delete task
POST   /api/planner/pomodoro      — Record completed pomodoro session
"""
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from middleware.auth import auth_required
from utils.helpers import get_db, to_object_id, add_xp_to_user

planner_bp = Blueprint("planner", __name__)


def task_to_dict(task):
    """Convert MongoDB task document to JSON-safe dict."""
    if not task:
        return None
    task["id"] = str(task.pop("_id"))
    task.pop("userId", None)
    return task


# ─── List Tasks ───────────────────────────────────────────────
@planner_bp.route("", methods=["GET"])
@auth_required
def list_tasks():
    db = get_db()

    date_str = request.args.get("date")        # YYYY-MM-DD
    range_days = int(request.args.get("range", 1))  # how many days to show

    query = {"userId": request.user_id}

    if date_str:
        try:
            start = datetime.strptime(date_str, "%Y-%m-%d")
            end = start + timedelta(days=range_days)
            query["date"] = {"$gte": date_str, "$lt": end.strftime("%Y-%m-%d")}
        except ValueError:
            pass

    tasks = db.planner_tasks.find(query).sort("time", 1)
    return jsonify({"tasks": [task_to_dict(t) for t in tasks]})


# ─── Create Task ─────────────────────────────────────────────
@planner_bp.route("", methods=["POST"])
@auth_required
def create_task():
    db = get_db()
    data = request.get_json(silent=True) or {}

    title = (data.get("title") or "").strip()
    if not title:
        return jsonify({"error": "Title is required"}), 400

    task = {
        "userId": request.user_id,
        "title": title,
        "description": data.get("description", ""),
        "date": data.get("date", datetime.utcnow().strftime("%Y-%m-%d")),
        "time": data.get("time", "09:00"),
        "duration": data.get("duration", 30),       # minutes
        "category": data.get("category", "study"),   # study / revision / practice / break
        "priority": data.get("priority", "medium"),  # low / medium / high
        "exam": data.get("exam", ""),                # linked exam id
        "done": False,
        "pomodorosPlanned": data.get("pomodorosPlanned", 0),
        "pomodorosCompleted": 0,
        "createdAt": datetime.utcnow().isoformat(),
    }

    result = db.planner_tasks.insert_one(task)
    task["_id"] = result.inserted_id

    return jsonify({"task": task_to_dict(task)}), 201


# ─── Update Task ──────────────────────────────────────────────
@planner_bp.route("/<task_id>", methods=["PUT"])
@auth_required
def update_task(task_id):
    db = get_db()
    oid = to_object_id(task_id)
    if not oid:
        return jsonify({"error": "Invalid task ID"}), 400

    task = db.planner_tasks.find_one({"_id": oid, "userId": request.user_id})
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json(silent=True) or {}
    allowed = ["title", "description", "date", "time", "duration",
               "category", "priority", "exam", "done", "pomodorosPlanned"]

    updates = {}
    for key in allowed:
        if key in data:
            updates[key] = data[key]

    # Award XP when completing a task
    if updates.get("done") is True and not task.get("done"):
        add_xp_to_user(db, request.user_id, 10, "task-complete")

    if updates:
        db.planner_tasks.update_one({"_id": oid}, {"$set": updates})

    updated = db.planner_tasks.find_one({"_id": oid})
    return jsonify({"task": task_to_dict(updated)})


# ─── Delete Task ──────────────────────────────────────────────
@planner_bp.route("/<task_id>", methods=["DELETE"])
@auth_required
def delete_task(task_id):
    db = get_db()
    oid = to_object_id(task_id)
    if not oid:
        return jsonify({"error": "Invalid task ID"}), 400

    result = db.planner_tasks.delete_one({"_id": oid, "userId": request.user_id})
    if result.deleted_count == 0:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"message": "Task deleted"})


# ─── Record Pomodoro Session ─────────────────────────────────
@planner_bp.route("/pomodoro", methods=["POST"])
@auth_required
def record_pomodoro():
    db = get_db()
    data = request.get_json(silent=True) or {}

    task_id = data.get("taskId")
    duration = data.get("duration", 25)  # minutes

    # If linked to a task, increment its pomodoro count
    if task_id:
        oid = to_object_id(task_id)
        if oid:
            db.planner_tasks.update_one(
                {"_id": oid, "userId": request.user_id},
                {"$inc": {"pomodorosCompleted": 1}}
            )

    # Track in user's daily activity
    today = datetime.utcnow().strftime("%Y-%m-%d")
    db.users.update_one(
        {"_id": to_object_id(request.user_id)},
        {
            "$inc": {f"activity.{today}.pomodoros": 1, f"activity.{today}.studyMinutes": duration},
            "$set": {f"activity.{today}.date": today},
        }
    )

    # Award XP for completing a pomodoro
    new_xp = add_xp_to_user(db, request.user_id, 15, "pomodoro")

    return jsonify({
        "message": "Pomodoro recorded",
        "xpEarned": 15,
        "totalXp": new_xp,
    })
