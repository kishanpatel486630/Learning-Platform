// ============================================================
//  FIREBASE CONFIGURATION
//  Replace the values below with your own Firebase project.
//  Get them from: https://console.firebase.google.com/
//  → Project Settings → Your Apps → Web App → Config
// ============================================================

const FIREBASE_CONFIG = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID",
};

// ── Firebase SDK (loaded via CDN in HTML) ──────────────────
// We lazily initialise so the app still works offline / without
// a real config (falls back to localStorage only).

let db = null;
let auth = null;
let currentUser = null;

function isFirebaseConfigured() {
  return (
    FIREBASE_CONFIG.apiKey &&
    FIREBASE_CONFIG.apiKey !== "YOUR_API_KEY" &&
    !FIREBASE_CONFIG.apiKey.startsWith("YOUR_") &&
    FIREBASE_CONFIG.projectId &&
    FIREBASE_CONFIG.projectId !== "YOUR_PROJECT_ID" &&
    !FIREBASE_CONFIG.projectId.startsWith("YOUR_")
  );
}

function initFirebase() {
  try {
    if (typeof firebase === "undefined") return false;
    if (!isFirebaseConfigured()) {
      console.info("Firebase not configured – running in demo / offline mode.");
      return false;
    }
    if (!firebase.apps.length) firebase.initializeApp(FIREBASE_CONFIG);
    auth = firebase.auth();
    db = firebase.firestore();
    return true;
  } catch (e) {
    console.warn("Firebase init failed – running in offline mode.", e.message);
    return false;
  }
}

// ── AUTH HELPERS ────────────────────────────────────────────

async function fbRegister(email, password, displayName, avatarColor) {
  const cred = await auth.createUserWithEmailAndPassword(email, password);
  await cred.user.updateProfile({ displayName });
  currentUser = cred.user;
  await fbSaveProfile({ displayName, avatarColor, email });
  return cred.user;
}

async function fbLogin(email, password) {
  const cred = await auth.signInWithEmailAndPassword(email, password);
  currentUser = cred.user;
  return cred.user;
}

async function fbLoginGoogle() {
  const provider = new firebase.auth.GoogleAuthProvider();
  const cred = await auth.signInWithPopup(provider);
  currentUser = cred.user;
  // Create profile if first time
  const snap = await db.collection("users").doc(cred.user.uid).get();
  if (!snap.exists) {
    await fbSaveProfile({
      displayName: cred.user.displayName || "Learner",
      avatarColor: randomColor(),
      email: cred.user.email,
    });
  }
  return cred.user;
}

async function fbLogout() {
  await auth.signOut();
  currentUser = null;
}

async function fbResetPassword(email) {
  await auth.sendPasswordResetEmail(email);
}

// ── FIRESTORE HELPERS ───────────────────────────────────────

async function fbSaveProfile(data) {
  if (!db || !currentUser) return;
  await db.collection("users").doc(currentUser.uid).set(data, { merge: true });
}

async function fbLoadProfile() {
  if (!db || !currentUser) return null;
  const snap = await db.collection("users").doc(currentUser.uid).get();
  return snap.exists ? snap.data() : null;
}

// Save full state to Firestore (replaces localStorage copy)
async function fbSaveState(stateObj) {
  if (!db || !currentUser) return;
  await db.collection("progress").doc(currentUser.uid).set(stateObj);
}

// Read state from Firestore
async function fbLoadState() {
  if (!db || !currentUser) return null;
  const snap = await db.collection("progress").doc(currentUser.uid).get();
  return snap.exists ? snap.data() : null;
}

// ── LEADERBOARD ─────────────────────────────────────────────

async function fbSubmitScore(name, xp, avatarColor) {
  if (!db || !currentUser) return;
  await db.collection("leaderboard").doc(currentUser.uid).set({
    name,
    xp,
    avatarColor,
    uid: currentUser.uid,
    updatedAt: firebase.firestore.FieldValue.serverTimestamp(),
  });
}

async function fbFetchLeaderboard(limit = 20) {
  if (!db) return [];
  const snap = await db
    .collection("leaderboard")
    .orderBy("xp", "desc")
    .limit(limit)
    .get();
  return snap.docs.map((d) => ({ id: d.id, ...d.data() }));
}

// ── QUIZ RESULTS ─────────────────────────────────────────────

async function fbSaveQuizResult(topicKey, correct, total) {
  if (!db || !currentUser) return;
  await db
    .collection("quizResults")
    .doc(currentUser.uid)
    .collection("topics")
    .doc(topicKey)
    .set({ correct, total, date: new Date().toISOString() }, { merge: true });
}

// ── UTILITY ──────────────────────────────────────────────────

function randomColor() {
  const colors = [
    "#00d4ff",
    "#7c3aed",
    "#f59e0b",
    "#10b981",
    "#ef4444",
    "#06b6d4",
    "#8b5cf6",
    "#ec4899",
  ];
  return colors[Math.floor(Math.random() * colors.length)];
}
