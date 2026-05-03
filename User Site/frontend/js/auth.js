/* auth.js — Frontend authentication handler for LearnPath */
"use strict";

const AUTH_PAGES = ["/login.html"]; // Pages that don't require auth
const ONBOARDING_PAGE = "/profile-setup.html";

/**
 * Call on every page load to enforce auth redirects.
 * - If NOT logged in → redirect to login (unless already on login page)
 * - If logged in but profile incomplete → redirect to profile-setup
 */
async function checkAuth() {
  const page = window.location.pathname.split("/").pop() || "index.html";
  const isAuthPage = AUTH_PAGES.some((p) => page === p.replace("/", ""));
  const isOnboarding = page === ONBOARDING_PAGE.replace("/", "");

  // Not logged in
  if (!API.isLoggedIn()) {
    if (!isAuthPage) {
      window.location.href = "/login.html";
    }
    return null;
  }

  // Logged in — verify token is still valid by fetching profile
  try {
    const data = await API.getMe();
    const user = data.user;

    // Update local state cache
    _cacheUserState(user);

    // If on login page but already logged in, redirect to dashboard
    if (isAuthPage) {
      window.location.href = user.profileComplete
        ? "/index.html"
        : "/profile-setup.html";
      return user;
    }

    // If profile not complete and not on onboarding page
    if (!user.profileComplete && !isOnboarding) {
      window.location.href = "/profile-setup.html";
      return user;
    }

    return user;
  } catch (err) {
    // Token is invalid
    if (err.status === 401) {
      clearTokens();
      if (!isAuthPage) {
        window.location.href = "/login.html";
      }
    }
    return null;
  }
}

/**
 * Cache user data from backend into localStorage for quick page renders.
 */
function _cacheUserState(user) {
  if (!user) return;
  try {
    const state = JSON.parse(localStorage.getItem("learnpath_state") || "{}");
    // Merge backend user data into local state
    Object.assign(state, {
      name: user.name || state.name,
      email: user.email || state.email,
      phone: user.phone || state.phone,
      photo: user.photo || state.photo,
      college: user.college || state.college,
      year: user.year || state.year,
      branch: user.branch || state.branch,
      targetExams: user.targetExams || state.targetExams,
      targetCompanies: user.targetCompanies || state.targetCompanies,
      xp: user.xp ?? state.xp,
      streak: user.streak || state.streak,
      theme: user.settings?.theme || state.theme,
      profileComplete: user.profileComplete,
    });
    localStorage.setItem("learnpath_state", JSON.stringify(state));
  } catch (_) {
    /* ignore */
  }
}

/**
 * Quick read of cached user data (synchronous, no API call).
 * Use when you need immediate data while waiting for checkAuth().
 */
function getCachedUser() {
  try {
    return JSON.parse(localStorage.getItem("learnpath_state") || "{}");
  } catch {
    return {};
  }
}

/**
 * Guard: redirect to login if not authenticated (for inline use).
 */
function requireAuth() {
  if (!API.isLoggedIn()) {
    window.location.href = "/login.html";
    return false;
  }
  return true;
}

// ─── Exports ─────────────────────────────────────────────────
window.checkAuth = checkAuth;
window.getCachedUser = getCachedUser;
window.requireAuth = requireAuth;
