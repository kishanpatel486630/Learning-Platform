"""
Skills Routes — Skill tracks, roadmaps, and progress tracking
GET    /api/skills/roadmaps
GET    /api/skills/progress
POST   /api/skills/progress
"""
from flask import Blueprint, request, jsonify
from middleware.auth import auth_required
from utils.helpers import get_db, to_object_id

skills_bp = Blueprint("skills", __name__)

SKILL_ROADMAPS = [
    {
        "id": "dsa",
        "title": "Data Structures & Algorithms",
        "description": "Beginner to Expert level. Direct interview level preparation.",
        "icon": "🧠",
        "nodes": [
            {
                "id": "dsa-basics",
                "title": "1. Big O & Complexity",
                "type": "video",
                "url": "https://www.youtube.com/embed/V6mKVRU1evU",
                "task": "Quiz: What is the time complexity of accessing an array element by index?"
            },
            {
                "id": "dsa-arrays",
                "title": "2. Arrays & Strings",
                "type": "video",
                "url": "https://www.youtube.com/embed/RBSGKlAvoiM",
                "task": "Code: Write a function to reverse a string in-place."
            },
            {
                "id": "dsa-linkedlists",
                "title": "3. Linked Lists",
                "type": "video",
                "url": "https://www.youtube.com/embed/WwfhLC16nc8",
                "task": "Code: Detect a cycle in a singly linked list using slow and fast pointers."
            },
            {
                "id": "dsa-stacks",
                "title": "4. Stacks & Queues",
                "type": "video",
                "url": "https://www.youtube.com/embed/wjI1WNcIntg",
                "task": "Code: Implement a Queue using two Stacks."
            },
            {
                "id": "dsa-trees",
                "title": "5. Trees & BST",
                "type": "video",
                "url": "https://www.youtube.com/embed/fAAZixRoSmw",
                "task": "Code: Find the maximum depth of a binary tree."
            },
            {
                "id": "dsa-graphs",
                "title": "6. Graphs (BFS/DFS)",
                "type": "video",
                "url": "https://www.youtube.com/embed/tWVWeAqZ0WU",
                "task": "Code: Implement Breadth-First Search on an adjacency list."
            },
            {
                "id": "dsa-dp",
                "title": "7. Dynamic Programming",
                "type": "video",
                "url": "https://www.youtube.com/embed/oBt53YbR9Kk",
                "task": "Code: Solve the 0/1 Knapsack problem."
            }
        ]
    },
    {
        "id": "python",
        "title": "Python Programming",
        "description": "Learn Python from scratch to advanced concepts.",
        "icon": "🐍",
        "nodes": [
            {
                "id": "py-basics",
                "title": "1. Python Basics & Syntax",
                "type": "video",
                "url": "https://www.youtube.com/embed/kqtD5dpn9C8",
                "task": "Code: Write a program to print the Fibonacci series."
            },
            {
                "id": "py-functions",
                "title": "2. Functions & Scope",
                "type": "video",
                "url": "https://www.youtube.com/embed/9Os0o3wzS_I",
                "task": "Code: Write a function with variable length arguments (*args)."
            },
            {
                "id": "py-oop",
                "title": "3. Object Oriented Programming",
                "type": "video",
                "url": "https://www.youtube.com/embed/JeznW_7DlB0",
                "task": "Code: Create a BankAccount class with deposit and withdraw methods."
            }
        ]
    },
    {
        "id": "sql",
        "title": "SQL & Databases",
        "description": "Master relational databases and advanced queries.",
        "icon": "💾",
        "nodes": [
            {
                "id": "sql-basics",
                "title": "1. Basic Queries (SELECT, WHERE)",
                "type": "video",
                "url": "https://www.youtube.com/embed/HXV3zeQKqGY",
                "task": "Code: Write a query to fetch all employees earning more than $50k."
            },
            {
                "id": "sql-joins",
                "title": "2. SQL Joins",
                "type": "video",
                "url": "https://www.youtube.com/embed/9yeOJ0ZMUYw",
                "task": "Code: Perform an INNER JOIN between Users and Orders tables."
            },
            {
                "id": "sql-advanced",
                "title": "3. Advanced (Window Functions)",
                "type": "video",
                "url": "https://www.youtube.com/embed/Ww71knvhQ-s",
                "task": "Code: Use ROW_NUMBER() to find the second highest salary."
            }
        ]
    },
    {
        "id": "system-design",
        "title": "System Design",
        "description": "Learn how to design scalable and distributed systems.",
        "icon": "🏗️",
        "nodes": [
            {
                "id": "sd-basics",
                "title": "1. Introduction to Scalability",
                "type": "video",
                "url": "https://www.youtube.com/embed/bBcPXqD3wD8",
                "task": "Quiz: What is the difference between vertical and horizontal scaling?"
            },
            {
                "id": "sd-caching",
                "title": "2. Caching & Load Balancing",
                "type": "video",
                "url": "https://www.youtube.com/embed/mPB2CsqgwLM",
                "task": "Task: Design a caching strategy for a high-read web application."
            }
        ]
    },
    {
        "id": "networking",
        "title": "Computer Networking",
        "description": "Understand the internet, OSI model, and protocols.",
        "icon": "🌐",
        "nodes": [
            {
                "id": "net-osi",
                "title": "1. The OSI Model",
                "type": "video",
                "url": "https://www.youtube.com/embed/vv4y_uOneC0",
                "task": "Quiz: Which layer of the OSI model handles routing?"
            },
            {
                "id": "net-tcp",
                "title": "2. TCP/IP & UDP",
                "type": "video",
                "url": "https://www.youtube.com/embed/PpsEaqJV_A0",
                "task": "Quiz: Why is UDP faster than TCP?"
            }
        ]
    }
]

@skills_bp.route("/roadmaps", methods=["GET"])
@auth_required
def get_roadmaps():
    return jsonify({"roadmaps": SKILL_ROADMAPS})

@skills_bp.route("/progress", methods=["GET"])
@auth_required
def get_progress():
    db = get_db()
    user = db.users.find_one({"_id": to_object_id(request.user_id)})
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"skillsProgress": user.get("skillsProgress", {})})

@skills_bp.route("/progress", methods=["POST"])
@auth_required
def update_progress():
    db = get_db()
    data = request.get_json(silent=True) or {}
    skill_id = data.get("skillId")
    node_id = data.get("nodeId")
    completed = data.get("completed", True)

    if not skill_id or not node_id:
        return jsonify({"error": "skillId and nodeId are required"}), 400

    if completed:
        db.users.update_one(
            {"_id": to_object_id(request.user_id)},
            {"$addToSet": {f"skillsProgress.{skill_id}": node_id}}
        )
    else:
        db.users.update_one(
            {"_id": to_object_id(request.user_id)},
            {"$pull": {f"skillsProgress.{skill_id}": node_id}}
        )

    return jsonify({"message": "Skill progress updated"})
