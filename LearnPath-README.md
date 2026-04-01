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
| AI Tutor       | 4-mode chat with context-aware prompts                 |
| Study Planner  | Week view, task CRUD, Pomodoro timer, AI plans         |
| Notes          | Create/edit/delete with tags and color coding          |
| Leaderboard    | XP/streak/questions rankings, study races              |
| Analytics      | Stats grid, heatmap, charts, activity timeline         |
| Settings       | API key, theme, study prefs, data export/import        |
| Profile        | Full profile view with achievements system             |
