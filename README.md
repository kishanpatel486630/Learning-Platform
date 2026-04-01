# LearnPath — Exam & Interview Prep Platform

A full-stack web application designed for **Indian engineering students** to prepare for placement exams, competitive exams, and coding interviews.

---

## 🏗️ Tech Stack

| Layer      | Technology                     |
| ---------- | ------------------------------ |
| Frontend   | Vanilla HTML/CSS/JS (13 pages) |
| Backend    | Python Flask 3.1               |
| Database   | MongoDB (PyMongo)              |
| Auth       | JWT (access + refresh tokens)  |
| AI         | Google Gemini 2.0 Flash        |
| Deployment | Gunicorn / Render / Railway    |

---

## 📁 Project Structure

```
Learning Track Website/
├── frontend/                    # Static frontend files
│   ├── css/
│   │   ├── variables.css        # Design tokens & themes
│   │   ├── sidebar.css          # Collapsible sidebar styles
│   │   └── pages.css            # All page styles
│   ├── js/
│   │   ├── api.js               # Backend API client
│   │   ├── auth.js              # JWT auth handler
│   │   ├── state.js             # State management + backend sync
│   │   ├── sidebar.js           # Sidebar component
│   │   ├── gemini-api.js        # Direct Gemini client (fallback)
│   │   └── data/exams-data.js   # Exam categories data
│   └── *.html                   # 13 pages (login, dashboard, exams, etc.)
│
├── backend/                     # Python Flask API
│   ├── app.py                   # Flask app entry point
│   ├── config.py                # Configuration from .env
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # Environment variables (not in git)
│   ├── models/                  # MongoDB document schemas
│   │   ├── user.py
│   │   ├── note.py
│   │   ├── question.py
│   │   └── race.py
│   ├── middleware/
│   │   └── auth.py              # JWT auth decorator
│   ├── routes/                  # API route blueprints
│   │   ├── auth.py              # /api/auth/*
│   │   ├── user.py              # /api/user/*
│   │   ├── notes.py             # /api/notes/*
│   │   ├── exams.py             # /api/exams/*
│   │   ├── questions.py         # /api/questions/*
│   │   ├── planner.py           # /api/planner/*
│   │   ├── leaderboard.py       # /api/leaderboard/*
│   │   └── ai.py                # /api/ai/*
│   └── utils/
│       └── helpers.py           # DB helpers, XP/streak utils
│
├── .env.example                 # Template for environment vars
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **MongoDB** (local or [MongoDB Atlas](https://www.mongodb.com/atlas) free tier)

### 1. Clone & Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example env and edit
cp ../.env.example .env
# Edit .env with your MongoDB URI, JWT secret, and Gemini API key
```

### 3. Start MongoDB

```bash
# If using local MongoDB
mongod

# Or use MongoDB Atlas — update MONGO_URI in .env
```

### 4. Run the Server

```bash
# Development
python app.py

# Production
gunicorn app:app --bind 0.0.0.0:5000
```

The app runs at **http://localhost:5000**

---

## 📡 API Endpoints

### Auth (`/api/auth`)

| Method | Endpoint  | Description          |
| ------ | --------- | -------------------- |
| POST   | /register | Create new account   |
| POST   | /login    | Login & get tokens   |
| POST   | /refresh  | Refresh access token |
| GET    | /me       | Get current user     |

### User (`/api/user`)

| Method | Endpoint            | Description               |
| ------ | ------------------- | ------------------------- |
| GET    | /profile            | Get user profile          |
| PUT    | /profile            | Update profile fields     |
| PUT    | /profile-setup      | Complete onboarding       |
| PUT    | /settings           | Update settings           |
| GET    | /progress           | Get XP, streak, activity  |
| POST   | /xp                 | Add XP points             |
| PUT    | /exam-progress      | Update exam progress      |
| PUT    | /interview-progress | Update interview progress |
| POST   | /answer-question    | Record question answer    |
| POST   | /bookmark           | Toggle question bookmark  |

### Exams (`/api/exams`)

| Method | Endpoint     | Description         |
| ------ | ------------ | ------------------- |
| GET    | /            | List all exams      |
| GET    | /:id         | Get exam details    |
| POST   | /:id/results | Submit quiz results |

### Questions (`/api/questions`)

| Method | Endpoint | Description               |
| ------ | -------- | ------------------------- |
| GET    | /        | List (filter by category) |
| POST   | /        | Create question           |
| GET    | /:id     | Get single question       |
| DELETE | /:id     | Delete question (owner)   |

### Notes (`/api/notes`)

| Method | Endpoint | Description      |
| ------ | -------- | ---------------- |
| GET    | /        | List with search |
| POST   | /        | Create note      |
| PUT    | /:id     | Update note      |
| DELETE | /:id     | Delete note      |

### Planner (`/api/planner`)

| Method | Endpoint  | Description             |
| ------ | --------- | ----------------------- |
| GET    | /         | List tasks (by date)    |
| POST   | /         | Create task             |
| PUT    | /:id      | Update / toggle task    |
| DELETE | /:id      | Delete task             |
| POST   | /pomodoro | Record pomodoro (+15XP) |

### Leaderboard (`/api/leaderboard`)

| Method | Endpoint        | Description         |
| ------ | --------------- | ------------------- |
| GET    | /               | Get rankings        |
| GET    | /friends        | List friends        |
| POST   | /friends        | Add friend by email |
| DELETE | /friends/:id    | Remove friend       |
| GET    | /races          | List races          |
| POST   | /races          | Create race         |
| GET    | /races/:id      | Race details        |
| POST   | /races/:id/join | Join a race         |

### AI (`/api/ai`)

| Method | Endpoint            | Description                |
| ------ | ------------------- | -------------------------- |
| POST   | /chat               | Free-form AI chat          |
| POST   | /generate-questions | Generate MCQ questions     |
| POST   | /hint               | Get hint for a question    |
| POST   | /explain            | Explain a concept          |
| POST   | /study-plan         | Generate study plan        |
| POST   | /solve              | Solve problem step-by-step |
| POST   | /interview-tips     | Get interview tips         |
| POST   | /mock-interview     | Mock interview questions   |

---

## 📱 Pages

1. **Login** — Email/password auth with JWT
2. **Profile Setup** — 4-step onboarding wizard
3. **Dashboard** — XP, streak, activity overview
4. **Exams** — Browse & practice exam categories
5. **Interview Prep** — Company-wise interview prep
6. **Question Bank** — Searchable questions + bookmarks
7. **AI Tutor** — Gemini-powered study assistant
8. **Study Planner** — Tasks + Pomodoro timer
9. **Notes** — Create & organize study notes
10. **Leaderboard** — Rankings + friend races
11. **Analytics** — Study progress charts
12. **Settings** — Theme, API key, preferences
13. **Profile** — View/edit profile

---

## 🌐 Deployment (Free Tier)

### Render

1. Push to GitHub
2. Create Web Service on [render.com](https://render.com)
3. Build command: `pip install -r backend/requirements.txt`
4. Start command: `cd backend && gunicorn app:app`
5. Add environment variables in Render dashboard

### MongoDB Atlas

1. Create free cluster at [mongodb.com/atlas](https://www.mongodb.com/atlas)
2. Get connection string and add to `MONGO_URI`

---

## 📄 License

MIT — Built for Indian engineering students 🇮🇳
#   L e a r n i n g - P l a t f o r m  
 