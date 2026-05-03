# LearnPath — Exam & Interview Prep Platform

A comprehensive exam preparation and interview readiness platform built for Indian engineering students. Pure vanilla HTML/CSS/JS — no build tools required.

## Features

- **Exam Preparation** — TCS NQT, Infosys, Wipro, Cognizant, Accenture, GATE CS, DSA Placement
- **Interview Prep** — Round-by-round workflows with AI feedback
- **AI Tutor** — Powered by Google Gemini (Tutor, Solver, Explain, Interview Coach modes)
- **Question Bank** — 1000s of previous year questions with AI generation
- **Study Planner** — Weekly calendar, task management, Pomodoro timer
- **Notes** — Personal notes with tags, colors, search
- **Leaderboard** — Compete with friends, study races
- **Analytics** — Progress tracking, heatmaps, category breakdowns
- **XP & Gamification** — Earn XP, maintain streaks, unlock achievements
- **Dual Theme** — Dark (purple neon) & Light (clean white)

## Tech Stack


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
=======
# LearnPath — Exam & Interview Prep Platform

A comprehensive exam preparation and interview readiness platform built for Indian engineering students. Pure vanilla HTML/CSS/JS — no build tools required.

## Features

- **Exam Preparation** — TCS NQT, Infosys, Wipro, Cognizant, Accenture, GATE CS, DSA Placement
- **Interview Prep** — Round-by-round workflows with AI feedback
- **AI Tutor** — Powered by Google Gemini (Tutor, Solver, Explain, Interview Coach modes)
- **Question Bank** — 1000s of previous year questions with AI generation
- **Study Planner** — Weekly calendar, task management, Pomodoro timer
- **Notes** — Personal notes with tags, colors, search
- **Leaderboard** — Compete with friends, study races
- **Analytics** — Progress tracking, heatmaps, category breakdowns
- **XP & Gamification** — Earn XP, maintain streaks, unlock achievements
- **Dual Theme** — Dark (purple neon) & Light (clean white)

## Tech Stack

| Layer    | Technology                                        |
| -------- | ------------------------------------------------- |
| Frontend | Vanilla HTML, CSS, JS                             |
| Auth     | Firebase 9.23.0 (compat SDK)                      |
| AI       | Google Gemini API (gemini-2.0-flash)              |
| PDF      | jsPDF 2.5.1                                       |
| Fonts    | Syne, DM Sans, JetBrains Mono                     |
| State    | localStorage (syncs to Firestore when configured) |

## Project Structure

```
├── login.html            # Auth (login/register/Google)
├── profile-setup.html    # 4-step onboarding wizard
├── index.html            # Dashboard
├── exams.html            # Exam categories & quiz engine
├── interview-prep.html   # Company interview workflows
├── question-bank.html    # Question bank with AI generation
├── ai-tutor.html         # Chat-based AI tutor
├── study-planner.html    # Calendar + Pomodoro timer
├── notes.html            # Personal notes
├── leaderboard.html      # Friend races & rankings
├── analytics.html        # Progress analytics
├── settings.html         # API key, theme, preferences
├── profile.html          # Profile view & edit
├── css/
│   ├── variables.css     # Theme variables (dark/light)
│   ├── sidebar.css       # Collapsible sidebar
│   └── pages.css         # Shared component library
└── js/
    ├── state.js          # State management (40+ fields)
    ├── sidebar.js        # Sidebar component & navigation
    ├── gemini-api.js     # Gemini AI integration
    ├── firebase-config.js # Firebase auth & Firestore
    └── data/
        └── exams-data.js # Exam categories, companies, sample questions
```

## Setup

1. Open `login.html` in a browser
2. Register/login (works in demo mode without Firebase)
3. Complete the 4-step profile setup
4. Start studying!

**Optional:** Add your Gemini API key in Settings → AI Configuration for AI-powered features.

## Pages Overview

| Page           | Description                                            |
| -------------- | ------------------------------------------------------ |
| Login          | Split-panel auth with Google sign-in                   |
| Profile Setup  | Personal → Education → Goals → Schedule wizard         |
| Dashboard      | Welcome banner, stats, quick actions, activity heatmap |
| Exams          | Category grid, section drilldown, timed quiz engine    |
| Interview Prep | Company cards, round timelines, mock interviews        |
| Question Bank  | Search/filter/bookmark, AI question generation         |
| Layer    | Technology                                        |
| -------- | ------------------------------------------------- |
| Frontend | Vanilla HTML, CSS, JS                             |
| Auth     | Firebase 9.23.0 (compat SDK)                      |
| AI       | Google Gemini API (gemini-2.0-flash)              |
| PDF      | jsPDF 2.5.1                                       |
| Fonts    | Syne, DM Sans, JetBrains Mono                     |
| State    | localStorage (syncs to Firestore when configured) |

## Project Structure

```
├── login.html            # Auth (login/register/Google)
├── profile-setup.html    # 4-step onboarding wizard
├── index.html            # Dashboard
├── exams.html            # Exam categories & quiz engine
├── interview-prep.html   # Company interview workflows
├── question-bank.html    # Question bank with AI generation
├── ai-tutor.html         # Chat-based AI tutor
├── study-planner.html    # Calendar + Pomodoro timer
├── notes.html            # Personal notes
├── leaderboard.html      # Friend races & rankings
├── analytics.html        # Progress analytics
├── settings.html         # API key, theme, preferences
├── profile.html          # Profile view & edit
├── css/
│   ├── variables.css     # Theme variables (dark/light)
│   ├── sidebar.css       # Collapsible sidebar
│   └── pages.css         # Shared component library
└── js/
    ├── state.js          # State management (40+ fields)
    ├── sidebar.js        # Sidebar component & navigation
    ├── gemini-api.js     # Gemini AI integration
    ├── firebase-config.js # Firebase auth & Firestore
    └── data/
        └── exams-data.js # Exam categories, companies, sample questions
```

## Setup

1. Open `login.html` in a browser
2. Register/login (works in demo mode without Firebase)
3. Complete the 4-step profile setup
4. Start studying!

**Optional:** Add your Gemini API key in Settings → AI Configuration for AI-powered features.

## Pages Overview

| Page           | Description                                            |
| -------------- | ------------------------------------------------------ |
| Login          | Split-panel auth with Google sign-in                   |
| Profile Setup  | Personal → Education → Goals → Schedule wizard         |
| Dashboard      | Welcome banner, stats, quick actions, activity heatmap |
| Exams          | Category grid, section drilldown, timed quiz engine    |
| Interview Prep | Company cards, round timelines, mock interviews        |
| Question Bank  | Search/filter/bookmark, AI question generation         |
| AI Tutor       | 4-mode chat with context-aware prompts                 |
| Study Planner  | Week view, task CRUD, Pomodoro timer, AI plans         |
| Notes          | Create/edit/delete with tags and color coding          |
| Leaderboard    | XP/streak/questions rankings, study races              |
| Analytics      | Stats grid, heatmap, charts, activity timeline         |
| Settings       | API key, theme, study prefs, data export/import        |
| Profile        | Full profile view with achievements system             |
