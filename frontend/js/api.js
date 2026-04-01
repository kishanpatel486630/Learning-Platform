/* api.js — Centralized API client for LearnPath backend */
"use strict";

const API_BASE = window.location.origin + "/api";

// ─── Token Management ────────────────────────────────────────
function getAccessToken() {
  return localStorage.getItem("lp_access_token") || "";
}
function getRefreshToken() {
  return localStorage.getItem("lp_refresh_token") || "";
}
function setTokens(access, refresh) {
  if (access) localStorage.setItem("lp_access_token", access);
  if (refresh) localStorage.setItem("lp_refresh_token", refresh);
}
function clearTokens() {
  localStorage.removeItem("lp_access_token");
  localStorage.removeItem("lp_refresh_token");
}
function logout() {
  clearTokens();
  localStorage.removeItem("learnpath_state");
  localStorage.removeItem("lp_demo_user");
  window.location.href = "/login.html";
}
function isLoggedIn() {
  return !!getAccessToken();
}

// ─── Core Fetch Wrapper ──────────────────────────────────────
let _isRefreshing = false;
let _refreshQueue = [];

async function apiFetch(path, options = {}) {
  const url = `${API_BASE}${path}`;

  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  const token = getAccessToken();
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const resp = await fetch(url, {
    ...options,
    headers,
    body: options.body
      ? typeof options.body === "string"
        ? options.body
        : JSON.stringify(options.body)
      : undefined,
  });

  // Handle 401 — try token refresh once
  if (resp.status === 401 && getRefreshToken() && !options._retried) {
    const refreshed = await _tryRefreshToken();
    if (refreshed) {
      return apiFetch(path, { ...options, _retried: true });
    } else {
      clearTokens();
      window.location.href = "/login.html";
      return null;
    }
  }

  const data = await resp.json().catch(() => ({}));

  if (!resp.ok) {
    const error = new Error(data.error || `API Error ${resp.status}`);
    error.status = resp.status;
    error.data = data;
    throw error;
  }

  return data;
}

async function _tryRefreshToken() {
  if (_isRefreshing) {
    return new Promise((resolve) => _refreshQueue.push(resolve));
  }
  _isRefreshing = true;

  try {
    const resp = await fetch(`${API_BASE}/auth/refresh`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refreshToken: getRefreshToken() }),
    });

    if (!resp.ok) {
      _refreshQueue.forEach((cb) => cb(false));
      _refreshQueue = [];
      return false;
    }

    const data = await resp.json();
    setTokens(data.accessToken, null);
    _refreshQueue.forEach((cb) => cb(true));
    _refreshQueue = [];
    return true;
  } catch {
    _refreshQueue.forEach((cb) => cb(false));
    _refreshQueue = [];
    return false;
  } finally {
    _isRefreshing = false;
  }
}

// ─── Auth API ────────────────────────────────────────────────
async function apiRegister(name, email, password) {
  const data = await apiFetch("/auth/register", {
    method: "POST",
    body: { name, email, password },
  });
  setTokens(data.accessToken, data.refreshToken);
  return data;
}

async function apiLogin(email, password) {
  const data = await apiFetch("/auth/login", {
    method: "POST",
    body: { email, password },
  });
  setTokens(data.accessToken, data.refreshToken);
  return data;
}

async function apiGetMe() {
  return apiFetch("/auth/me");
}

function apiLogout() {
  clearTokens();
  localStorage.removeItem("learnpath_state");
  window.location.href = "/login.html";
}

// ─── User / Profile API ─────────────────────────────────────
async function apiGetProfile() {
  return apiFetch("/user/profile");
}

async function apiUpdateProfile(fields) {
  return apiFetch("/user/profile", {
    method: "PUT",
    body: fields,
  });
}

async function apiCompleteProfileSetup(data) {
  return apiFetch("/user/profile-setup", {
    method: "PUT",
    body: data,
  });
}

async function apiUpdateSettings(settings) {
  return apiFetch("/user/settings", {
    method: "PUT",
    body: settings,
  });
}

async function apiGetProgress() {
  return apiFetch("/user/progress");
}

async function apiAddXp(amount, source) {
  return apiFetch("/user/xp", {
    method: "POST",
    body: { amount, source },
  });
}

async function apiUpdateExamProgress(examId, data) {
  return apiFetch("/user/exam-progress", {
    method: "PUT",
    body: { examId, ...data },
  });
}

async function apiUpdateInterviewProgress(company, data) {
  return apiFetch("/user/interview-progress", {
    method: "PUT",
    body: { company, ...data },
  });
}

async function apiAnswerQuestion(questionId, correct) {
  return apiFetch("/user/answer-question", {
    method: "POST",
    body: { questionId, correct },
  });
}

async function apiToggleBookmark(questionId) {
  return apiFetch("/user/bookmark", {
    method: "POST",
    body: { questionId },
  });
}

// ─── Exams API ───────────────────────────────────────────────
async function apiGetExams(type) {
  const q = type ? `?type=${type}` : "";
  return apiFetch(`/exams${q}`);
}

async function apiGetExam(examId) {
  return apiFetch(`/exams/${examId}`);
}

async function apiSubmitExamResults(examId, results) {
  return apiFetch(`/exams/${examId}/results`, {
    method: "POST",
    body: results,
  });
}

// ─── Questions API ───────────────────────────────────────────
async function apiGetQuestions(filters = {}) {
  const params = new URLSearchParams();
  for (const [k, v] of Object.entries(filters)) {
    if (v !== undefined && v !== null && v !== "") params.set(k, v);
  }
  const q = params.toString();
  return apiFetch(`/questions${q ? "?" + q : ""}`);
}

async function apiCreateQuestion(question) {
  return apiFetch("/questions", {
    method: "POST",
    body: question,
  });
}

async function apiGetQuestion(id) {
  return apiFetch(`/questions/${id}`);
}

async function apiDeleteQuestion(id) {
  return apiFetch(`/questions/${id}`, { method: "DELETE" });
}

// ─── Notes API ───────────────────────────────────────────────
async function apiGetNotes(search, tag) {
  const params = new URLSearchParams();
  if (search) params.set("search", search);
  if (tag) params.set("tag", tag);
  const q = params.toString();
  return apiFetch(`/notes${q ? "?" + q : ""}`);
}

async function apiCreateNote(note) {
  return apiFetch("/notes", {
    method: "POST",
    body: note,
  });
}

async function apiUpdateNote(id, updates) {
  return apiFetch(`/notes/${id}`, {
    method: "PUT",
    body: updates,
  });
}

async function apiDeleteNote(id) {
  return apiFetch(`/notes/${id}`, { method: "DELETE" });
}

// ─── Planner API ─────────────────────────────────────────────
async function apiGetTasks(date, range) {
  const params = new URLSearchParams();
  if (date) params.set("date", date);
  if (range) params.set("range", range);
  const q = params.toString();
  return apiFetch(`/planner${q ? "?" + q : ""}`);
}

async function apiCreateTask(task) {
  return apiFetch("/planner", {
    method: "POST",
    body: task,
  });
}

async function apiUpdateTask(id, updates) {
  return apiFetch(`/planner/${id}`, {
    method: "PUT",
    body: updates,
  });
}

async function apiDeleteTask(id) {
  return apiFetch(`/planner/${id}`, { method: "DELETE" });
}

async function apiRecordPomodoro(taskId, duration) {
  return apiFetch("/planner/pomodoro", {
    method: "POST",
    body: { taskId, duration },
  });
}

// ─── Leaderboard API ─────────────────────────────────────────
async function apiGetRankings(sort, friendsOnly) {
  const params = new URLSearchParams();
  if (sort) params.set("sort", sort);
  if (friendsOnly) params.set("friends", "true");
  const q = params.toString();
  return apiFetch(`/leaderboard${q ? "?" + q : ""}`);
}

async function apiGetFriends() {
  return apiFetch("/leaderboard/friends");
}

async function apiAddFriend(email) {
  return apiFetch("/leaderboard/friends", {
    method: "POST",
    body: { email },
  });
}

async function apiRemoveFriend(friendId) {
  return apiFetch(`/leaderboard/friends/${friendId}`, { method: "DELETE" });
}

async function apiGetRaces() {
  return apiFetch("/leaderboard/races");
}

async function apiCreateRace(race) {
  return apiFetch("/leaderboard/races", {
    method: "POST",
    body: race,
  });
}

async function apiGetRace(id) {
  return apiFetch(`/leaderboard/races/${id}`);
}

async function apiJoinRace(id) {
  return apiFetch(`/leaderboard/races/${id}/join`, { method: "POST" });
}

// ─── AI API ──────────────────────────────────────────────────
async function apiAiChat(prompt, options = {}) {
  return apiFetch("/ai/chat", {
    method: "POST",
    body: { prompt, ...options },
  });
}

async function apiAiGenerateQuestions(topic, examType, count) {
  return apiFetch("/ai/generate-questions", {
    method: "POST",
    body: { topic, examType, count },
  });
}

async function apiAiHint(question, topic) {
  return apiFetch("/ai/hint", {
    method: "POST",
    body: { question, topic },
  });
}

async function apiAiExplain(topic, level) {
  return apiFetch("/ai/explain", {
    method: "POST",
    body: { topic, level },
  });
}

async function apiAiStudyPlan(examType, daysLeft, hoursPerDay, topics) {
  return apiFetch("/ai/study-plan", {
    method: "POST",
    body: { examType, daysLeft, hoursPerDay, topics },
  });
}

async function apiAiSolve(problem, subject) {
  return apiFetch("/ai/solve", {
    method: "POST",
    body: { problem, subject },
  });
}

async function apiAiInterviewTips(company, round) {
  return apiFetch("/ai/interview-tips", {
    method: "POST",
    body: { company, round },
  });
}

async function apiAiMockInterview(company, round, count) {
  return apiFetch("/ai/mock-interview", {
    method: "POST",
    body: { company, round, count },
  });
}

// ─── Health Check ────────────────────────────────────────────
async function apiHealthCheck() {
  try {
    const data = await apiFetch("/health");
    return data.status === "healthy";
  } catch {
    return false;
  }
}

// ─── Exports (global) ───────────────────────────────────────
window.API = {
  // Core
  apiFetch,
  isLoggedIn,
  // Auth
  register: apiRegister,
  login: apiLogin,
  getMe: apiGetMe,
  logout: apiLogout,
  // User
  getProfile: apiGetProfile,
  updateProfile: apiUpdateProfile,
  completeProfileSetup: apiCompleteProfileSetup,
  updateSettings: apiUpdateSettings,
  getProgress: apiGetProgress,
  addXp: apiAddXp,
  updateExamProgress: apiUpdateExamProgress,
  updateInterviewProgress: apiUpdateInterviewProgress,
  answerQuestion: apiAnswerQuestion,
  toggleBookmark: apiToggleBookmark,
  // Exams
  getExams: apiGetExams,
  getExam: apiGetExam,
  submitExamResults: apiSubmitExamResults,
  // Questions
  getQuestions: apiGetQuestions,
  createQuestion: apiCreateQuestion,
  getQuestion: apiGetQuestion,
  deleteQuestion: apiDeleteQuestion,
  // Notes
  getNotes: apiGetNotes,
  createNote: apiCreateNote,
  updateNote: apiUpdateNote,
  deleteNote: apiDeleteNote,
  // Planner
  getTasks: apiGetTasks,
  createTask: apiCreateTask,
  updateTask: apiUpdateTask,
  deleteTask: apiDeleteTask,
  recordPomodoro: apiRecordPomodoro,
  // Leaderboard
  getRankings: apiGetRankings,
  getFriends: apiGetFriends,
  addFriend: apiAddFriend,
  removeFriend: apiRemoveFriend,
  getRaces: apiGetRaces,
  createRace: apiCreateRace,
  getRace: apiGetRace,
  joinRace: apiJoinRace,
  // AI
  aiChat: apiAiChat,
  aiGenerateQuestions: apiAiGenerateQuestions,
  aiHint: apiAiHint,
  aiExplain: apiAiExplain,
  aiStudyPlan: apiAiStudyPlan,
  aiSolve: apiAiSolve,
  aiInterviewTips: apiAiInterviewTips,
  aiMockInterview: apiAiMockInterview,
  // Utils
  healthCheck: apiHealthCheck,
};
