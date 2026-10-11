// Per-reader conveniences only (theme, open panels). Storage can be unavailable
// (private windows, blocked site data), so every access is guarded and every
// caller must work without it. Nothing that matters for grading lives here.

const PREFIX = "qp:";

export function read(key, fallback = null) {
  try {
    const raw = window.localStorage.getItem(PREFIX + key);
    return raw === null ? fallback : JSON.parse(raw);
  } catch {
    return fallback;
  }
}

export function write(key, value) {
  try {
    window.localStorage.setItem(PREFIX + key, JSON.stringify(value));
    return true;
  } catch {
    return false;
  }
}
