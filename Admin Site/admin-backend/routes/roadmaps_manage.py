from flask import Blueprint, request, jsonify, g
from bson import ObjectId

roadmaps_bp = Blueprint("roadmaps", __name__)

@roadmaps_bp.route("/", methods=["GET"])
def get_all_roadmaps():
    if g.db is None:
        return jsonify({"error": "Database not connected"}), 500

    roadmaps = list(g.db.roadmaps.find({}))
    for r in roadmaps:
        r["_id"] = str(r["_id"])
    return jsonify({"roadmaps": roadmaps})

@roadmaps_bp.route("/", methods=["POST"])
def create_roadmap():
    if g.db is None:
        return jsonify({"error": "Database not connected"}), 500

    data = request.get_json(silent=True) or {}
    new_roadmap = {
        "title": data.get("title", "New Roadmap"),
        "description": data.get("description", ""),
        "icon": data.get("icon", "📚"),
        "is_published": False,
        "nodes": data.get("nodes", [])
    }

    result = g.db.roadmaps.insert_one(new_roadmap)
    new_roadmap["_id"] = str(result.inserted_id)
    return jsonify({"message": "Roadmap created", "roadmap": new_roadmap})

@roadmaps_bp.route("/<roadmap_id>", methods=["PUT"])
def update_roadmap(roadmap_id):
    if g.db is None:
        return jsonify({"error": "Database not connected"}), 500

    data = request.get_json(silent=True) or {}
    update_data = {}
    if "title" in data: update_data["title"] = data["title"]
    if "description" in data: update_data["description"] = data["description"]
    if "icon" in data: update_data["icon"] = data["icon"]
    if "nodes" in data: update_data["nodes"] = data["nodes"]

    try:
        g.db.roadmaps.update_one({"_id": ObjectId(roadmap_id)}, {"$set": update_data})
        return jsonify({"message": "Roadmap updated successfully"})
    except Exception:
        return jsonify({"error": "Invalid roadmap ID"}), 400

@roadmaps_bp.route("/<roadmap_id>/publish", methods=["POST"])
def publish_roadmap(roadmap_id):
    if g.db is None:
        return jsonify({"error": "Database not connected"}), 500

    data = request.get_json(silent=True) or {}
    is_published = data.get("is_published", True)

    try:
        g.db.roadmaps.update_one({"_id": ObjectId(roadmap_id)}, {"$set": {"is_published": is_published}})
        status = "published" if is_published else "unpublished"
        return jsonify({"message": f"Roadmap {status} successfully"})
    except Exception:
        return jsonify({"error": "Invalid roadmap ID"}), 400

@roadmaps_bp.route("/<roadmap_id>", methods=["DELETE"])
def delete_roadmap(roadmap_id):
    if g.db is None:
        return jsonify({"error": "Database not connected"}), 500

    try:
        g.db.roadmaps.delete_one({"_id": ObjectId(roadmap_id)})
        return jsonify({"message": "Roadmap deleted successfully"})
    except Exception:
        return jsonify({"error": "Invalid roadmap ID"}), 400
