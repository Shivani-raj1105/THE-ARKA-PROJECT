// ── API base URL ──────────────────────────────────────────────────────────────
const API = window.location.origin;

// ── Token helpers ─────────────────────────────────────────────────────────────
export const getToken = () => localStorage.getItem("ob_token");
export const setToken = (t) => localStorage.setItem("ob_token", t);
export const removeToken = () => localStorage.removeItem("ob_token");
export const getUser = () => {
  try { return JSON.parse(localStorage.getItem("ob_user") || "null"); }
  catch { return null; }
};
export const setUser = (u) => localStorage.setItem("ob_user", JSON.stringify(u));
export const removeUser = () => localStorage.removeItem("ob_user");

export function isLoggedIn() { return !!getToken(); }

export function logout() {
  removeToken();
  removeUser();
  window.location.href = "/login";
}

// ── Fetch wrapper ─────────────────────────────────────────────────────────────
async function apiFetch(path, options = {}) {
  const token = getToken();
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  if (options.body instanceof FormData) delete headers["Content-Type"];

  const res = await fetch(`${API}${path}`, { ...options, headers });
  if (res.status === 401) { logout(); return; }
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || "Request failed");
  return data;
}

// ── Auth ──────────────────────────────────────────────────────────────────────
export async function register(full_name, email, password, phone) {
  const data = await apiFetch("/auth/register", {
    method: "POST",
    body: JSON.stringify({ full_name, email, password, phone }),
  });
  setToken(data.token);
  setUser(data.user);
  return data;
}

export async function login(email, password) {
  const data = await apiFetch("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  setToken(data.token);
  setUser(data.user);
  return data;
}

export async function fetchMe() {
  return apiFetch("/auth/me");
}

export async function updateProfile(payload) {
  return apiFetch("/users/me", { method: "PUT", body: JSON.stringify(payload) });
}

// ── Detection ─────────────────────────────────────────────────────────────────
export async function detect(file) {
  const form = new FormData();
  form.append("file", file);
  const token = getToken();
  const headers = {};
  if (token) headers["Authorization"] = `Bearer ${token}`;
  const res = await fetch(`${API}/detect`, { method: "POST", headers, body: form });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || "Detection failed");
  return data; // { task_id }
}

export async function pollResult(taskId, maxAttempts = 60, intervalMs = 3000) {
  for (let i = 0; i < maxAttempts; i++) {
    const data = await apiFetch(`/result/${taskId}`);
    if (data.status === "SUCCESS" || data.status === "FAILURE") return data;
    await new Promise((r) => setTimeout(r, intervalMs));
  }
  throw new Error("Detection timed out");
}

// ── History ───────────────────────────────────────────────────────────────────
export async function fetchHistory() {
  return apiFetch("/users/me/history");
}
