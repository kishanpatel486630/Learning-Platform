// ===== STATE MANAGEMENT (Backend-Synced) =====
let state = loadState();

function defaultState() {
  return {
    // ── Auth & Onboarding ─────────────────────────
    onboarded: false,
    profileComplete: false,

    // ── Personal Info ─────────────────────────────
    name: "",
    email: "",
    phone: "",
    photo: "",
    avatarColor: "#7c3aed",
    bio: "",

    // ── Education ─────────────────────────────────
    qualification: "",
    college: "",
    branch: "",
    year: "",
    cgpa: "",

    // ── Career Goals ──────────────────────────────
    targetCompanies: [],
    targetExams: [],
    interviewPrep: false,
    careerGoal: "",

    // ── Study Preferences ─────────────────────────
    dailyHours: 1,
    preferredTime: "morning",
    level: "beginner",

    // ── Progress & Gamification ───────────────────
    xp: 0,
    streak: 0,
    lastStudyDate: null,
    badges: [],
    completedTopics: {},
    quizResults: {},
    studyMinutes: 0,
    pomodorosTotal: 0,
    activityLog: {},
    joinDate: new Date().toLocaleDateString("en-IN", {
      year: "numeric",
      month: "long",
    }),

    // ── Exam Progress ─────────────────────────────
    examProgress: {},
    interviewProgress: {},

    // ── Questions ─────────────────────────────────
    answeredQuestions: {},
    bookmarkedQuestions: [],

    // ── Study Planner ─────────────────────────────
    studyPlan: {},

    // ── Notes ─────────────────────────────────────
    notes: [],

    // ── Social ────────────────────────────────────
    friends: [],
    races: [],

    // ── Settings ──────────────────────────────────
    theme: "dark",
    geminiApiKey: "",

    // ── Legacy compat ─────────────────────────────
    goal: "",
    tracks: [],
    selectedTracks: [],
    hours: 1,
    customTracks: [],
    challengeDate: null,
    challengeDone: false,
    quizCorrect: 0,
  };
}

function loadState() {
  try {
    const saved = localStorage.getItem("learnpath_state");
    if (saved) {
      const parsed = JSON.parse(saved);
      return { ...defaultState(), ...parsed };
    }
  } catch (e) {}
  return defaultState();
}

function saveState() {
  localStorage.setItem("learnpath_state", JSON.stringify(state));
}

// ─── Backend Sync Helpers ────────────────────────────────────

/**
 * Load user profile from backend and update local state.
 * Call on page load after checkAuth() succeeds.
 */
async function syncFromBackend() {
  if (!window.API || !API.isLoggedIn()) return;
  try {
    const { user } = await API.getProfile();
    if (user) {
      // Merge backend user into local state
      const backendFields = [
        "name",
        "email",
        "phone",
        "photo",
        "avatarColor",
        "bio",
        "qualification",
        "college",
        "branch",
        "year",
        "cgpa",
        "targetCompanies",
        "targetExams",
        "interviewPrep",
        "careerGoal",
        "dailyHours",
        "preferredTime",
        "level",
        "xp",
        "streak",
        "badges",
        "completedTopics",
        "studyMinutes",
        "pomodorosTotal",
        "examProgress",
        "interviewProgress",
        "answeredQuestions",
        "bookmarkedQuestions",
        "friends",
        "profileComplete",
        "joinDate",
      ];
      for (const key of backendFields) {
        if (user[key] !== undefined) state[key] = user[key];
      }
      // Settings
      if (user.settings) {
        if (user.settings.theme) state.theme = user.settings.theme;
        if (user.settings.geminiApiKey)
          state.geminiApiKey = user.settings.geminiApiKey;
      }
      saveState();
    }
  } catch (err) {
    console.warn("Backend sync failed, using local cache:", err.message);
  }
}

/**
 * Push a profile update to the backend.
 * @param {object} fields — key-value pairs to update
 */
async function syncToBackend(fields) {
  if (!window.API || !API.isLoggedIn()) return;
  try {
    await API.updateProfile(fields);
  } catch (err) {
    console.warn("Failed to sync to backend:", err.message);
  }
}

// Helper to add XP with activity logging + backend sync
function addXP(amount, source) {
  state.xp = (state.xp || 0) + amount;
  // Activity log
  const today = new Date().toISOString().split("T")[0];
  state.activityLog[today] = (state.activityLog[today] || 0) + amount;
  // Streak
  const todayStr = new Date().toDateString();
  if (state.lastStudyDate !== todayStr) {
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    if (state.lastStudyDate === yesterday.toDateString()) {
      state.streak = (state.streak || 0) + 1;
    } else if (state.lastStudyDate !== todayStr) {
      state.streak = 1;
    }
    state.lastStudyDate = todayStr;
  }
  saveState();

  // Async sync to backend (fire & forget)
  if (window.API && API.isLoggedIn()) {
    API.addXp(amount, source || "unknown").catch(() => {});
  }
}
