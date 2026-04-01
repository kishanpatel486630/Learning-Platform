"""
AI Routes — Gemini API proxy for all AI features
POST   /api/ai/chat                — Free-form Gemini chat
POST   /api/ai/generate-questions  — Generate MCQ questions
POST   /api/ai/hint                — Get hint for a question
POST   /api/ai/explain             — Explain a concept
POST   /api/ai/study-plan          — Generate study plan
POST   /api/ai/solve               — Solve a problem step-by-step
POST   /api/ai/interview-tips      — Get interview tips
POST   /api/ai/mock-interview      — Generate mock interview questions
"""
from flask import Blueprint, request, jsonify
import requests
from middleware.auth import auth_required
from config import Config

ai_bp = Blueprint("ai", __name__)

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{Config.GEMINI_MODEL}:generateContent"
)


def _gemini_call(prompt, *, json_mode=False, temperature=0.7, max_tokens=2048, api_key=None):
    """Call Google Gemini API and return the text response."""
    key = api_key or Config.GEMINI_API_KEY
    if not key:
        return None, "Gemini API key not configured"

    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens,
            "topP": 0.9,
        },
    }

    if json_mode:
        body["generationConfig"]["responseMimeType"] = "application/json"

    try:
        resp = requests.post(
            f"{GEMINI_URL}?key={key}",
            json=body,
            headers={"Content-Type": "application/json"},
            timeout=60,
        )

        if not resp.ok:
            err = resp.json().get("error", {}).get("message", f"API error {resp.status_code}")
            return None, err

        data = resp.json()
        text = (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
        )
        return text, None

    except requests.Timeout:
        return None, "Gemini API timed out"
    except Exception as e:
        return None, str(e)


def _get_api_key():
    """Use user's API key if provided, otherwise fall back to server key."""
    data = request.get_json(silent=True) or {}
    return data.get("apiKey") or Config.GEMINI_API_KEY


# ─── Free Chat ────────────────────────────────────────────────
@ai_bp.route("/chat", methods=["POST"])
@auth_required
def chat():
    data = request.get_json(silent=True) or {}
    prompt = (data.get("prompt") or "").strip()
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    text, err = _gemini_call(
        prompt,
        temperature=data.get("temperature", 0.7),
        max_tokens=data.get("maxTokens", 2048),
        api_key=_get_api_key(),
    )
    if err:
        return jsonify({"error": err}), 502

    return jsonify({"response": text})


# ─── Generate Questions ───────────────────────────────────────
@ai_bp.route("/generate-questions", methods=["POST"])
@auth_required
def generate_questions():
    data = request.get_json(silent=True) or {}
    topic = data.get("topic", "General")
    exam_type = data.get("examType", "placement")
    count = min(int(data.get("count", 5)), 20)

    prompt = f"""You are an expert exam question creator for Indian engineering students.

Generate {count} multiple-choice questions for the topic "{topic}" for {exam_type} exam preparation.

Return ONLY valid JSON in this exact format:
{{
  "questions": [
    {{
      "question": "Question text here?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct": 0,
      "explanation": "Brief explanation why this is correct."
    }}
  ]
}}

Make questions ranging from easy to hard. Include commonly asked patterns from previous {exam_type} exams."""

    text, err = _gemini_call(prompt, json_mode=True, temperature=0.8, api_key=_get_api_key())
    if err:
        return jsonify({"error": err}), 502

    import json
    try:
        result = json.loads(text) if isinstance(text, str) else text
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse AI response"}), 502

    return jsonify(result)


# ─── Get Hint ─────────────────────────────────────────────────
@ai_bp.route("/hint", methods=["POST"])
@auth_required
def get_hint():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "")
    topic = data.get("topic", "")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    prompt = f"""You are a friendly tutor helping an Indian engineering student.

The student is stuck on this question from the topic "{topic}":
"{question}"

Give a helpful hint (NOT the answer) in 2-3 sentences. Guide them toward the solution step by step."""

    text, err = _gemini_call(prompt, temperature=0.6, max_tokens=300, api_key=_get_api_key())
    if err:
        return jsonify({"error": err}), 502

    return jsonify({"hint": text})


# ─── Explain Concept ──────────────────────────────────────────
@ai_bp.route("/explain", methods=["POST"])
@auth_required
def explain_concept():
    data = request.get_json(silent=True) or {}
    topic = data.get("topic", "")
    level = data.get("level", "beginner")

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    prompt = f"""Explain "{topic}" to a {level}-level Indian engineering student.

Use simple language, real-world analogies, and examples. Include:
1. What it is (2-3 lines)
2. Why it matters
3. A simple example
4. Key points to remember

Keep it concise but clear. Use bullet points."""

    text, err = _gemini_call(prompt, temperature=0.5, max_tokens=800, api_key=_get_api_key())
    if err:
        return jsonify({"error": err}), 502

    return jsonify({"explanation": text})


# ─── Generate Study Plan ─────────────────────────────────────
@ai_bp.route("/study-plan", methods=["POST"])
@auth_required
def study_plan():
    data = request.get_json(silent=True) or {}
    exam_type = data.get("examType", "placement")
    days_left = data.get("daysLeft", 30)
    hours_per_day = data.get("hoursPerDay", 4)
    topics = data.get("topics", [])

    if not topics:
        return jsonify({"error": "At least one topic is required"}), 400

    topics_str = ", ".join(topics)
    prompt = f"""Create a detailed day-wise study plan for {exam_type} exam preparation.

Details:
- Days remaining: {days_left}
- Study hours per day: {hours_per_day}
- Topics to cover: {topics_str}

Return ONLY valid JSON:
{{
  "plan": [
    {{
      "day": 1,
      "date": "Day 1",
      "topics": ["Topic 1 - subtopic"],
      "hours": 2,
      "tasks": ["Read chapter X", "Solve 20 problems"],
      "tip": "Focus on understanding concepts first"
    }}
  ],
  "tips": ["General tip 1", "General tip 2"]
}}

Make the plan realistic and progressive (easy to hard). Include revision days."""

    text, err = _gemini_call(prompt, json_mode=True, temperature=0.6, max_tokens=4096, api_key=_get_api_key())
    if err:
        return jsonify({"error": err}), 502

    import json
    try:
        result = json.loads(text) if isinstance(text, str) else text
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse AI response"}), 502

    return jsonify(result)


# ─── Solve Problem ────────────────────────────────────────────
@ai_bp.route("/solve", methods=["POST"])
@auth_required
def solve_problem():
    data = request.get_json(silent=True) or {}
    problem = data.get("problem", "")
    subject = data.get("subject", "Computer Science")

    if not problem:
        return jsonify({"error": "Problem is required"}), 400

    prompt = f"""You are a tutor helping an Indian engineering student with {subject}.

Solve this problem step by step:
"{problem}"

Format your response with:
1. Understanding the problem
2. Step-by-step solution
3. Final answer
4. Key takeaway

Use clear formatting with bullet points and numbered steps."""

    text, err = _gemini_call(prompt, temperature=0.3, max_tokens=1500, api_key=_get_api_key())
    if err:
        return jsonify({"error": err}), 502

    return jsonify({"solution": text})


# ─── Interview Tips ───────────────────────────────────────────
@ai_bp.route("/interview-tips", methods=["POST"])
@auth_required
def interview_tips():
    data = request.get_json(silent=True) or {}
    company = data.get("company", "")
    round_type = data.get("round", "Technical")

    if not company:
        return jsonify({"error": "Company is required"}), 400

    prompt = f"""Give preparation tips for the {round_type} round of {company} interview for freshers/engineering students in India.

Include:
1. What to expect in this round
2. Key topics/areas to focus on
3. Common question patterns
4. Do's and Don'ts
5. Time management tips

Keep it practical and actionable. Format with clear headings and bullet points."""

    text, err = _gemini_call(prompt, temperature=0.5, max_tokens=1000, api_key=_get_api_key())
    if err:
        return jsonify({"error": err}), 502

    return jsonify({"tips": text})


# ─── Mock Interview ───────────────────────────────────────────
@ai_bp.route("/mock-interview", methods=["POST"])
@auth_required
def mock_interview():
    data = request.get_json(silent=True) or {}
    company = data.get("company", "")
    round_type = data.get("round", "Technical")
    count = min(int(data.get("count", 10)), 20)

    if not company:
        return jsonify({"error": "Company is required"}), 400

    prompt = f"""Generate {count} realistic {round_type} interview questions for {company} campus placement for Indian engineering freshers.

Return ONLY valid JSON:
{{
  "questions": [
    {{
      "question": "Question text",
      "category": "Category (e.g., Arrays, DBMS, Aptitude)",
      "difficulty": "Easy|Medium|Hard",
      "expectedAnswer": "Brief model answer or key points",
      "timeLimit": 120
    }}
  ]
}}

Include a mix of difficulties. Make them realistic based on actual {company} interview patterns."""

    text, err = _gemini_call(prompt, json_mode=True, temperature=0.7, api_key=_get_api_key())
    if err:
        return jsonify({"error": err}), 502

    import json
    try:
        result = json.loads(text) if isinstance(text, str) else text
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse AI response"}), 502

    return jsonify(result)
