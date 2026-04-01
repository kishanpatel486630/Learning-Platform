# Learning Platform

Full-stack learning platform for exam preparation and interview practice. Backend: Flask + MongoDB with JWT auth and Gemini-powered AI. Frontend: static HTML/CSS/JS served by Flask.

## Tech Stack

- Frontend: Vanilla HTML/CSS/JS (13 pages)
- Backend: Python Flask 3.1
- Database: MongoDB (PyMongo)
- Auth: JWT access + refresh tokens
- AI: Google Gemini (configurable key)

## Structure

```
frontend/   # Static pages, styles, and JS (api/auth/state/sidebar helpers)
backend/    # Flask app, routes, models, middleware, helpers
.env.example # Environment template
```

## Quick Start

1. Copy env file and fill values

```
cp .env.example .env   # or copy via Explorer on Windows
```

2. Create venv and install deps

```
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # macOS/Linux
pip install -r backend/requirements.txt
```

3. Run MongoDB locally (or point MONGO_URI to Atlas).
4. Launch server

```
python backend/app.py
```

Server runs on http://localhost:5000 and serves the frontend (login at /login.html).

## Environment Variables (.env)

- SECRET_KEY, JWT_SECRET: signing keys
- MONGO_URI, MONGO_DB_NAME: Mongo connection
- GEMINI_API_KEY, GEMINI_MODEL: Gemini access
- CORS_ORIGINS: comma-separated allowed origins
- FLASK_DEBUG: true/false

## Core Endpoints (prefixed with /api)

- Auth: /auth/register, /auth/login, /auth/refresh, /auth/me
- User: /user/profile, /profile-setup, /settings, /progress, /xp, /exam-progress, /interview-progress, /bookmark
- Notes: /notes (CRUD with search/tag)
- Questions: /questions (CRUD), /exams, /exams/{id}/results
- Planner: /planner (CRUD), /planner/pomodoro
- Leaderboard: /leaderboard, /friends, /races
- AI: /ai/chat, /generate-questions, /hint, /explain, /study-plan, /solve, /interview-tips, /mock-interview
- Health: /health

## Frontend Pages

Login, Profile Setup, Dashboard, Exams, Interview Prep, Question Bank, AI Tutor, Study Planner, Notes, Leaderboard, Analytics, Settings, Profile.

## Production Notes

- Keep secrets out of git; set env vars in hosting provider.
- Set CORS_ORIGINS to your deployed domains.
- Run with a WSGI server for production, e.g.:

```
cd backend
gunicorn app:app --bind 0.0.0.0:5000
```
