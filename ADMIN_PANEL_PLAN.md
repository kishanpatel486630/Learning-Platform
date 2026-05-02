# LearnPath — Admin Panel Development Plan

This document outlines the architecture, features, and implementation plan for the **LearnPath Admin Panel**. This panel will act as a centralized, fully dynamic dashboard for administrators to manage users, courses, roadmaps, and platform content.

## 🎯 1. Core Objectives
- Create a secure, isolated web application exclusively for administrators.
- Replace all hardcoded data (like the SQL/DSA roadmaps, mock exams, and questions) with dynamic data managed entirely from the Admin UI.
- Provide full CRUD (Create, Read, Update, Delete) capabilities.
- Implement a "Publish / Unpublish" workflow so admins can stage content before making it live to students.

---

## 🛠️ 2. Proposed Architecture
To keep the Admin Panel secure and maintainable, it should be built as a separate frontend but connected to your existing backend database.

- **Frontend:** A standalone website (e.g., `admin.learnpath.com` or a separate folder `admin-frontend/`). It will use a clean, professional dashboard UI (matching the new blue aesthetic, but tailored for data tables and forms).
- **Backend API:** We will add a new set of protected routes to your existing Flask backend (e.g., `/api/admin/*`). These routes will require an `admin` role in the JWT token to access.
- **Database:** It will connect to the exact same MongoDB Atlas database, but will have write access to core collections like `courses`, `questions`, and `roadmaps`.

---

## 🚀 3. Key Features & Modules

### A. Dashboard Overview
- **Analytics at a glance:** Total active users, new registrations this week, most popular study plans, and total questions in the bank.

### B. User Management
- View all registered users and their details.
- See individual user progress (XP, completed roadmaps, test scores).
- Suspend, ban, or elevate users to 'Admin' status.

### C. Course & Study Plan Management (The "Publish" Workflow)
- **Dynamic Roadmaps:** Create new learning tracks (like the SQL one).
- **Nodes/Tasks:** Add videos, PDFs, and practical tasks to each track.
- **Draft & Publish System:**
  - `Draft`: Admin is still building the course. It is invisible to users.
  - `Published`: Users can see and enroll in it.
  - `Unpublished`: Temporarily hidden from the platform.
- **Edit/Delete:** Modify existing links or delete outdated courses.

### D. Question Bank & Exam Manager
- Interface to add multiple-choice questions for exams (TCS, Infosys, etc.).
- Bulk upload questions via CSV/Excel.
- Edit categories, set difficulty levels, and attach explanations.

---

## 📋 4. Database Schema Updates Needed
To make this fully dynamic, we will transition from hardcoded lists in Python to MongoDB collections:
1. `users` (Add `role: "admin" | "user"`)
2. `roadmaps` (Store title, description, and an array of nodes. Add `status: "draft" | "published"`)
3. `questions` (Store exam questions, options, and correct answers)

---

## 🛤️ 5. Implementation Phases
- **Phase 1: Backend Preparation.** Update MongoDB schemas, create the `/api/admin` blueprint in Flask, and implement Role-Based Access Control (RBAC) to ensure only admins can use these APIs.
- **Phase 2: Admin UI Setup.** Create the basic Admin dashboard layout (Sidebar, Topbar, Data Tables).
- **Phase 3: Content Management.** Build the forms to Create, Edit, Publish, and Delete Study Plans/Roadmaps.
- **Phase 4: User Management & Analytics.** Build the screens to view user data and overall platform statistics.
- **Phase 5: Deployment.** Deploy the Admin Panel securely.

---
