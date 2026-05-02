# 🚀 LearnPath Master Architecture & Feature Plan

Welcome to the definitive guide for **LearnPath** — a comprehensive exam preparation, interview readiness, and skills learning platform. This document serves as the master blueprint, explaining exactly how the platform works, the extensive features currently implemented, and the future roadmap (including the Admin Panel).

---

## 🏗️ 1. Platform Overview & How It Works

**LearnPath** is designed specifically for students and professionals to systematically prepare for technical interviews, exams, and new software skills. 

### How it operates under the hood:
1. **Frontend (The UI):** Built using vanilla HTML, CSS, and JavaScript. It ensures blazing fast performance without the overhead of heavy frameworks. State management is handled through a central `state.js` file, and UI updates (like XP gains and progress bars) are handled dynamically via DOM manipulation.
2. **Backend (The Engine):** A robust Flask (Python) backend serves as the API layer. It manages secure routes, handles authentication via JSON Web Tokens (JWT), and processes data requests.
3. **Database (The Brain):** MongoDB Atlas is used to store all persistent data. This includes user profiles, XP, completed tasks, notes, and study plans. The NoSQL structure allows flexible storage for complex data like dynamic skill roadmaps.
4. **AI Integration:** Google's Gemini API is deeply integrated to act as a personal tutor, generate dynamic questions, and create custom study plans.

---

## ✨ 2. Detailed Feature Breakdown (User Side)

### 📚 A. Learn Skills (Dynamic Roadmaps)
- **Structured Phases:** Topics (like SQL or DSA) are broken down into 6 distinct phases ranging from Basics to Interview Prep.
- **Rich Media Integration:** Each phase embeds high-quality YouTube resources or PDF documents right into the platform. No downloading necessary.
- **Interactive Tasks:** Users receive specific "Mini Tasks" for each phase. Checking off a task saves the progress to MongoDB and instantly awards XP.

### 🎯 B. Exam & Interview Prep
- **Company-Specific Paths:** Curated tracks for major companies (TCS, Infosys, Cognizant, etc.).
- **Round-by-Round Breakdown:** Users can simulate the exact interview process (Aptitude -> Coding -> Technical HR).
- **Mock Interviews:** AI-driven mock interviews that simulate real pressure.

### 🤖 C. The AI Tutor
- **4 Distinct Modes:** 
  - *Tutor:* Teaches concepts step-by-step.
  - *Solver:* Solves complex algorithms.
  - *Explain:* Breaks down confusing code snippets.
  - *Interview Coach:* Asks questions and evaluates answers.
- **Context-Aware:** The AI knows what exam or topic the user is currently studying.

### 📅 D. Study Planner & Pomodoro Timer
- **Weekly Calendar View:** Users can assign topics to specific days.
- **Task CRUD:** Create, Read, Update, and Delete tasks easily.
- **Built-in Pomodoro:** A sleek 25-minute timer to maintain focus, which logs study hours to the database upon completion.

### 🏆 E. Gamification Engine (XP & Leaderboard)
- **XP System:** Everything from completing a SQL task to finishing a Pomodoro session grants Experience Points (XP).
- **Streaks:** Daily logins and completions build up a streak, encouraging consistency.
- **Leaderboard:** Ranks users globally based on XP, fostering healthy competition.

### 📝 F. Notes & Question Bank
- **Smart Notes:** Color-coded notes with tagging systems for quick retrieval.
- **Infinite Question Bank:** Search through thousands of previous-year questions, filter by difficulty, and bookmark favorites.

---

## 🔒 3. The Future: Comprehensive Admin Panel

To make LearnPath fully dynamic and manageable without touching code, the upcoming **Admin Panel** will introduce powerful features:

### 👥 User Management Hub
- **Total Visibility:** See every registered user, their current XP, streak, and completed courses.
- **Access Control:** Suspend inactive accounts or elevate specific users to Admin status.

### 🛠️ Dynamic Course Builder (Publish/Unpublish System)
- **Visual Roadmap Editor:** Create new skills (e.g., "Advanced System Design" or "Computer Networking") by adding titles, YouTube embed links, and text tasks.
- **Drafting System:** Build a massive course over weeks, saving it as a `Draft`. It remains invisible to users.
- **1-Click Publish:** Once the course is perfect, click "Publish" to instantly push it to the main user dashboard. If something is wrong, "Unpublish" it immediately.

### 🧠 Content Management
- **Question Editor:** Add new aptitude or coding questions to the global database.
- **Company Profiles:** Add new companies to the "Interview Prep" section with their updated hiring patterns.

---

## 💻 4. Technology Stack Summary

| Layer | Technology Used | Purpose |
| :--- | :--- | :--- |
| **Frontend** | HTML5, CSS3 (Blue/Dark Theme), JS | Fast, responsive, client-side rendering |
| **Backend** | Python (Flask) | Secure API, Routing, Logic processing |
| **Database** | MongoDB Atlas | Cloud database for flexible, schema-less data |
| **Authentication** | PyJWT / Firebase | Secure user sessions and password management |
| **Artificial Intelligence**| Google Gemini API | Powers the AI Tutor and Question Generation |
| **Deployment** | Vercel | Serverless hosting for seamless scaling |

---
*This plan represents the complete vision for LearnPath, turning it into an industry-grade EdTech platform.*
