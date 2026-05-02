# LearnPath Admin Panel — Master Plan

## 🎯 Architecture Overview
The Learning Platform is now divided into two fully independent systems to ensure high security and separate concerns:
1. **User Site** (`/User Site`): The public-facing learning platform.
2. **Admin Site** (`/Admin Site`): A secure, dynamic management dashboard restricted to Administrators.

The Admin Site has its own **Frontend** (`admin-frontend`) and its own **Backend** (`admin-backend`), connected to the same core MongoDB database.

## 🛠️ Tech Stack (Admin Site)
- **Frontend**: Vanilla HTML/CSS/JS (Matching the User Site's clean blue UI theme)
- **Backend**: Python Flask (REST API separated from user-facing routes)
- **Database**: MongoDB (Shared with User Site, but accessed with elevated privileges)
- **Auth**: JWT-based Admin Authentication

---

## 🚀 Features & Capabilities

### 1. 👥 User Management
- **Dashboard**: View total users, active users, and system analytics.
- **List Users**: See all registered users, their XP, their current study plans, and their roles.
- **Actions**: Ban/unban users, reset passwords, or manually grant XP/Achievements.

### 2. 📚 Study Plan & Roadmap Management
- **Dynamic Creation**: Build new roadmaps (e.g., "Python for Beginners", "System Design") entirely from the UI without touching the codebase.
- **Node Management**: Add, edit, or delete specific phases/nodes within a roadmap.
- **Publish/Unpublish**: Keep a study plan in "Draft" mode while building it. Once ready, click "Publish" to make it instantly visible to users on the User Site.
- **Content Linking**: Attach YouTube video URLs, PDFs, or external course links directly to nodes.

### 3. 📝 Task & Question Management
- **Add Tasks**: Define specific "Mini Tasks" or "Project Ideas" for each phase of a study plan.
- **Question Bank Integration**: Add or edit questions for the Exams and Mock Interviews sections.

---

## 📂 File Structure (Admin Site)
```text
Admin Site/
├── admin-backend/                 # Isolated Flask Backend for Admin operations
│   ├── app.py                     # Entry point (runs on port 5001)
│   ├── config.py                  # Database and JWT config
│   └── routes/
│       ├── auth.py                # Admin Login/Logout
│       ├── users_manage.py        # CRUD for users
│       └── roadmaps_manage.py     # CRUD for study plans
├── admin-frontend/                # Admin Dashboard UI
│   ├── index.html                 # Admin Login Page
│   ├── dashboard.html             # Main Dashboard & Analytics
│   ├── users.html                 # User Management View
│   ├── roadmaps.html              # Study Plan Builder & Publisher
│   ├── css/                       # Exact same Blue UI theme as User Site
│   └── js/
│       ├── admin-api.js           # Fetch wrapper for port 5001
│       └── admin-ui.js            # Dashboard interactions
└── ADMIN_README.md
```

## 🔄 How it Works Together
1. The Admin logs into `admin-frontend/index.html`.
2. They navigate to the "Study Plans" tab and create a new roadmap.
3. The `admin-backend` saves this roadmap to the `roadmaps` collection in MongoDB with a flag `is_published: true`.
4. When a student visits the **User Site**, the User Backend queries MongoDB for all published roadmaps and seamlessly displays them.

---

## ❓ Pending Questions for You (Please Answer)
1. **Authentication**: Do you want a hardcoded "Super Admin" account, or do you want to be able to promote normal users to "Admin" status from the database?
2. **Backend Execution**: The User Site backend currently runs on port `5000`. Do you want the Admin backend to run simultaneously on port `5001` so both can be active at the same time?
3. **Drafts vs Live**: When you click "Unpublish" on a study plan, should it completely disappear for users who are *already* enrolled in it, or just prevent *new* users from seeing it?
