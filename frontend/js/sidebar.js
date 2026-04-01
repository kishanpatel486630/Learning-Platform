/* sidebar.js — Collapsible sidebar component injected into every page */
"use strict";

const SIDEBAR_ITEMS = [
  { section: "Main" },
  { id: "dashboard", icon: "📊", label: "Dashboard", href: "index.html" },
  { id: "exams", icon: "📝", label: "Exam Prep", href: "exams.html" },
  {
    id: "interview",
    icon: "💼",
    label: "Interview Prep",
    href: "interview-prep.html",
  },
  {
    id: "questions",
    icon: "❓",
    label: "Question Bank",
    href: "question-bank.html",
  },
  { section: "Study" },
  {
    id: "planner",
    icon: "📅",
    label: "Study Planner",
    href: "study-planner.html",
  },
  { id: "ai-tutor", icon: "🤖", label: "AI Tutor", href: "ai-tutor.html" },
  { id: "notes", icon: "📒", label: "Notes", href: "notes.html" },
  { section: "Social" },
  {
    id: "leaderboard",
    icon: "🏆",
    label: "Leaderboard",
    href: "leaderboard.html",
  },
  { id: "analytics", icon: "📈", label: "Analytics", href: "analytics.html" },
  { section: "Account" },
  { id: "profile", icon: "👤", label: "Profile", href: "profile.html" },
  { id: "settings", icon: "⚙️", label: "Settings", href: "settings.html" },
];

function renderSidebar(activeId) {
  const s = typeof loadState === "function" ? loadState() : {};
  const collapsed = localStorage.getItem("lp_sidebar_collapsed") === "true";

  // Build sidebar HTML
  let navHTML = "";
  SIDEBAR_ITEMS.forEach((item) => {
    if (item.section) {
      navHTML += `<div class="sb-section-title">${item.section}</div>`;
      return;
    }
    const active = item.id === activeId ? " active" : "";
    navHTML += `
      <a class="sb-link${active}" href="${item.href}" data-page="${item.id}">
        <span class="sb-link-icon">${item.icon}</span>
        <span class="sb-link-text">${item.label}</span>
      </a>`;
  });

  // User info
  const userName = s.name || "Learner";
  const userEmail = s.email || "";
  const avatarColor = s.avatarColor || "#7c3aed";

  const sidebarHTML = `
    <div class="sidebar${collapsed ? " collapsed" : ""}" id="sidebarEl">
      <button class="sb-collapse-btn" id="sbCollapseBtn" onclick="toggleSidebar()" title="Toggle sidebar">
        ${collapsed ? "▶" : "◀"}
      </button>
      <a class="sb-logo" href="index.html">
        <div class="sb-logo-icon">⚡</div>
        <span class="sb-logo-text">LearnPath</span>
      </a>
      <nav class="sb-nav">${navHTML}</nav>
      <div class="sb-user">
        <div class="sb-user-avatar" style="background:${avatarColor}">${userName[0].toUpperCase()}</div>
        <div class="sb-user-info">
          <div class="sb-user-name">${userName}</div>
          <div class="sb-user-email">${userEmail}</div>
        </div>
        <div class="sb-user-actions">
          <button class="sb-user-btn" onclick="window.location.href='settings.html'" title="Settings">⚙️</button>
          <button class="sb-user-btn" onclick="lpLogout()" title="Sign Out">🚪</button>
        </div>
      </div>
    </div>
    <div class="sb-overlay" id="sbOverlay" onclick="closeMobileSidebar()"></div>
  `;

  // Inject before main content
  document.body.insertAdjacentHTML("afterbegin", sidebarHTML);

  // Add mobile toggle to topbar if it exists
  const topbar = document.querySelector(".topbar-left");
  if (topbar) {
    const toggle = document.createElement("button");
    toggle.className = "sb-mobile-toggle";
    toggle.innerHTML = "☰";
    toggle.onclick = openMobileSidebar;
    topbar.prepend(toggle);
  }
}

function toggleSidebar() {
  const el = document.getElementById("sidebarEl");
  if (!el) return;
  el.classList.toggle("collapsed");
  const isCollapsed = el.classList.contains("collapsed");
  localStorage.setItem("lp_sidebar_collapsed", isCollapsed);
  const btn = document.getElementById("sbCollapseBtn");
  if (btn) btn.innerHTML = isCollapsed ? "▶" : "◀";
}

function openMobileSidebar() {
  const el = document.getElementById("sidebarEl");
  const ov = document.getElementById("sbOverlay");
  if (el) el.classList.add("mobile-open");
  if (ov) ov.classList.add("active");
}

function closeMobileSidebar() {
  const el = document.getElementById("sidebarEl");
  const ov = document.getElementById("sbOverlay");
  if (el) el.classList.remove("mobile-open");
  if (ov) ov.classList.remove("active");
}

function lpLogout() {
  localStorage.removeItem("lp_demo_user");
  localStorage.removeItem("learnpath_state");
  // Clear JWT tokens if API is available
  if (window.API) {
    API.logout();
  } else {
    localStorage.removeItem("lp_access_token");
    localStorage.removeItem("lp_refresh_token");
    window.location.href = "login.html";
  }
}

// Theme toggle
function lpToggleTheme() {
  const html = document.documentElement;
  const current = html.getAttribute("data-theme");
  const next = current === "dark" ? "light" : "dark";
  html.setAttribute("data-theme", next);
  try {
    const s = JSON.parse(localStorage.getItem("learnpath_state") || "{}");
    s.theme = next;
    localStorage.setItem("learnpath_state", JSON.stringify(s));
  } catch (_) {}
  // Update toggle button text
  const btn = document.getElementById("themeToggleBtn");
  if (btn) btn.textContent = next === "dark" ? "☀️" : "🌙";
}

// Apply saved theme on load
function lpApplyTheme() {
  try {
    const s = JSON.parse(localStorage.getItem("learnpath_state") || "{}");
    const theme = s.theme || "dark";
    document.documentElement.setAttribute("data-theme", theme);
    // Set button text after render
    setTimeout(() => {
      const btn = document.getElementById("themeToggleBtn");
      if (btn) btn.textContent = theme === "dark" ? "☀️" : "🌙";
    }, 100);
  } catch (_) {}
}

// Auth guard — allow if JWT token present OR if state.onboarded (legacy demo mode)
function lpAuthGuard() {
  try {
    // JWT-based auth (primary)
    if (window.API && API.isLoggedIn()) return true;
    // Legacy: local-only onboarded flag
    const s = JSON.parse(localStorage.getItem("learnpath_state") || "{}");
    if (s.onboarded || s.profileComplete) return true;
    const page = window.location.pathname.split("/").pop();
    if (page !== "login.html" && page !== "profile-setup.html") {
      window.location.href = "login.html";
      return false;
    }
  } catch (_) {}
  return true;
}

// Toast notification
function lpToast(msg, duration = 3000) {
  let toast = document.getElementById("lpToastEl");
  if (!toast) {
    toast = document.createElement("div");
    toast.id = "lpToastEl";
    toast.className = "lp-toast";
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), duration);
}

// Initialize page shell
function lpInitPage(pageId) {
  lpApplyTheme();
  renderSidebar(pageId);
}

window.toggleSidebar = toggleSidebar;
window.openMobileSidebar = openMobileSidebar;
window.closeMobileSidebar = closeMobileSidebar;
window.lpLogout = lpLogout;
window.lpToggleTheme = lpToggleTheme;
window.lpToast = lpToast;
window.lpInitPage = lpInitPage;
window.lpAuthGuard = lpAuthGuard;
