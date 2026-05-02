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
        "title": "Complete SQL Roadmap",
        "description": "Beginner to Advanced SQL. Master relational databases, complex queries, and system design.",
        "icon": "💾",
        "nodes": [
            {
                "id": "sql-phase1",
                "title": "Phase 1: Basics (Week 1–2)",
                "type": "video",
                "url": "https://www.youtube.com/embed/HXV3zeQKqGY",
                "task": """
<div style='margin-bottom: 8px;'><strong>Goal:</strong> Understand what SQL is and write simple queries</div>
<div style='margin-bottom: 8px;'><strong>Topics:</strong>
  <ul style='margin-left: 20px; list-style-type: disc; margin-top: 4px;'>
    <li>What is Database, DBMS, RDBMS</li>
    <li>Tables, Rows, Columns & SQL syntax basics</li>
    <li>SELECT statement & WHERE conditions (=, >, <, BETWEEN, IN, LIKE)</li>
    <li>Sorting: ORDER BY | Limiting: LIMIT</li>
  </ul>
</div>
<div style='margin-bottom: 12px;'><strong>Practice:</strong> Retrieve specific data from tables, filter records (e.g., users above age 25), and pattern matching.</div>
<div style='padding: 12px; background: var(--surface2); border-radius: 8px;'>
  <strong>👉 Mini Task:</strong><br>
  Create a Student table and:<br>
  - Find top 5 students<br>
  - Filter students with marks > 70
</div>
"""
            },
            {
                "id": "sql-phase2",
                "title": "Phase 2: Intermediate Core (Week 3–4)",
                "type": "video",
                "url": "https://www.youtube.com/embed/9yeOJ0ZMUYw",
                "task": """
<div style='margin-bottom: 8px;'><strong>Goal:</strong> Work with real-world queries</div>
<div style='margin-bottom: 8px;'><strong>Topics:</strong>
  <ul style='margin-left: 20px; list-style-type: disc; margin-top: 4px;'>
    <li>Aggregate Functions: COUNT, SUM, AVG, MAX, MIN</li>
    <li>GROUP BY, HAVING, DISTINCT, Aliases (AS)</li>
    <li>Joins: INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN</li>
  </ul>
</div>
<div style='margin-bottom: 12px;'><strong>Practice:</strong> Total sales per category, Users with no orders (LEFT JOIN), Find duplicates.</div>
<div style='padding: 12px; background: var(--surface2); border-radius: 8px;'>
  <strong>👉 Mini Project Idea:</strong><br>
  Build a simple CRM database (Customers, Orders, Products).<br>
  Write queries like: Total revenue, Top customers.
</div>
"""
            },
            {
                "id": "sql-phase3",
                "title": "Phase 3: Advanced SQL (Week 5–6)",
                "type": "video",
                "url": "https://www.youtube.com/embed/Ww71knvhQ-s",
                "task": """
<div style='margin-bottom: 8px;'><strong>Goal:</strong> Handle complex queries like a pro</div>
<div style='margin-bottom: 8px;'><strong>Topics:</strong>
  <ul style='margin-left: 20px; list-style-type: disc; margin-top: 4px;'>
    <li>Subqueries (Nested queries) & Correlated subqueries</li>
    <li>CASE statements</li>
    <li>Window Functions: ROW_NUMBER(), RANK(), DENSE_RANK()</li>
    <li>Common Table Expressions (CTE) (WITH) & Views</li>
  </ul>
</div>
<div style='margin-bottom: 12px;'><strong>Practice:</strong> Top 3 salaries per department, Running totals, Ranking users.</div>
<div style='padding: 12px; background: var(--surface2); border-radius: 8px;'>
  <strong>👉 Mini Task:</strong><br>
  - Find second highest salary<br>
  - Find duplicate rows
</div>
"""
            },
            {
                "id": "sql-phase4",
                "title": "Phase 4: Database Design (Week 7)",
                "type": "video",
                "url": "https://www.youtube.com/embed/ztHopE5Wnpc",
                "task": """
<div style='margin-bottom: 8px;'><strong>Goal:</strong> Think like a backend developer</div>
<div style='margin-bottom: 8px;'><strong>Topics:</strong>
  <ul style='margin-left: 20px; list-style-type: disc; margin-top: 4px;'>
    <li>Normalization (1NF, 2NF, 3NF)</li>
    <li>Primary Key, Foreign Key</li>
    <li>Relationships: One-to-One, One-to-Many, Many-to-Many</li>
    <li>Indexes</li>
  </ul>
</div>
<div style='padding: 12px; background: var(--surface2); border-radius: 8px;'>
  <strong>👉 Practice / Task:</strong><br>
  Design a database schema for:<br>
  - An E-commerce app<br>
  - Vehicle management system
</div>
"""
            },
            {
                "id": "sql-phase5",
                "title": "Phase 5: Advanced + Real World (Week 8–9)",
                "type": "video",
                "url": "https://www.youtube.com/embed/C-kIH1wYwU8",
                "task": """
<div style='margin-bottom: 8px;'><strong>Goal:</strong> Industry-level SQL</div>
<div style='margin-bottom: 8px;'><strong>Topics:</strong>
  <ul style='margin-left: 20px; list-style-type: disc; margin-top: 4px;'>
    <li>Stored Procedures & Triggers</li>
    <li>Transactions (COMMIT, ROLLBACK)</li>
    <li>Query Optimization & Indexing strategies</li>
  </ul>
</div>
<div style='padding: 12px; background: var(--surface2); border-radius: 8px;'>
  <strong>👉 Practice / Task:</strong><br>
  - Optimize slow queries<br>
  - Create stored procedures for CRUD operations
</div>
"""
            },
            {
                "id": "sql-phase6",
                "title": "Phase 6: Interview & Projects (Week 10+)",
                "type": "video",
                "url": "https://www.youtube.com/embed/VFsQ31_iJHQ",
                "task": """
<div style='margin-bottom: 8px;'><strong>Goal:</strong> Crack interviews + real projects</div>
<div style='margin-bottom: 8px;'><strong>Topics:</strong> SQL interview questions, Complex joins & edge cases, Data analysis queries.</div>
<div style='margin-bottom: 12px;'><strong>Practice Platforms:</strong> LeetCode (SQL section), HackerRank SQL, StrataScratch.</div>
<div style='padding: 12px; background: var(--surface2); border-radius: 8px;'>
  <strong>👉 Final Projects (UI/UX + Data):</strong><br>
  - CRM Database System<br>
  - Parking Management System<br>
  - E-commerce analytics dashboard
</div>
"""
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

