// Learner state: progress, quiz results, grader results, spaced-retrieval cards
// and workspace files, kept in IndexedDB in the learner's own browser.
//
// Browsers may clear this storage, and private windows may refuse it, so every
// access is wrapped: when IndexedDB is unavailable the store falls back to
// memory for the session and reports `persistent === false`, and the page tells
// the learner to export. Nothing here ever leaves the browser.

const DB_NAME = "qf-course";
const DB_VERSION = 1;
export const STORES = ["kv", "progress", "quiz", "grader", "cards", "files"];

function openDb() {
  return new Promise((resolve, reject) => {
    let request;
    try {
      request = indexedDB.open(DB_NAME, DB_VERSION);
    } catch (error) {
      reject(error);
      return;
    }
    request.onupgradeneeded = () => {
      const db = request.result;
      for (const name of STORES) {
        if (!db.objectStoreNames.contains(name)) db.createObjectStore(name);
      }
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
    request.onblocked = () => reject(new Error("IndexedDB upgrade blocked by another tab"));
  });
}

function wrap(request) {
  return new Promise((resolve, reject) => {
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

class MemoryBackend {
  constructor() {
    this.data = new Map(STORES.map((name) => [name, new Map()]));
  }
  async get(store, key) {
    return this.data.get(store).get(key);
  }
  async put(store, key, value) {
    this.data.get(store).set(key, value);
  }
  async delete(store, key) {
    this.data.get(store).delete(key);
  }
  async entries(store) {
    return [...this.data.get(store).entries()];
  }
  async clear(store) {
    this.data.get(store).clear();
  }
}

class IdbBackend {
  constructor(db) {
    this.db = db;
  }
  tx(store, mode) {
    return this.db.transaction(store, mode).objectStore(store);
  }
  async get(store, key) {
    return wrap(this.tx(store, "readonly").get(key));
  }
  async put(store, key, value) {
    await wrap(this.tx(store, "readwrite").put(value, key));
  }
  async delete(store, key) {
    await wrap(this.tx(store, "readwrite").delete(key));
  }
  async entries(store) {
    const os = this.tx(store, "readonly");
    const [keys, values] = await Promise.all([wrap(os.getAllKeys()), wrap(os.getAll())]);
    return keys.map((key, i) => [key, values[i]]);
  }
  async clear(store) {
    await wrap(this.tx(store, "readwrite").clear());
  }
}

let backendPromise = null;
export let persistent = true;

function backend() {
  if (!backendPromise) {
    backendPromise = openDb()
      .then((db) => new IdbBackend(db))
      .catch(() => {
        persistent = false;
        return new MemoryBackend();
      });
  }
  return backendPromise;
}

async function safely(fn, fallback) {
  try {
    return await fn(await backend());
  } catch (error) {
    console.warn("store:", error);
    return fallback;
  }
}

export const get = (store, key) => safely((b) => b.get(store, key), undefined);
export const put = (store, key, value) => safely((b) => b.put(store, key, value), undefined);
export const remove = (store, key) => safely((b) => b.delete(store, key), undefined);
export const entries = (store) => safely((b) => b.entries(store), []);

/** A random identifier for this learner's workspace, created once. Seeds per-learner project instances. */
export async function workspaceId() {
  let id = await get("kv", "workspace-id");
  if (!id) {
    const bytes = new Uint8Array(8);
    crypto.getRandomValues(bytes);
    id = [...bytes].map((b) => b.toString(16).padStart(2, "0")).join("");
    await put("kv", "workspace-id", id);
  }
  return id;
}

/** Deterministic 31-bit seed for a unit, derived from the workspace ID (FNV-1a). */
export async function unitSeed(unit) {
  const text = `${await workspaceId()}:${unit}`;
  let hash = 0x811c9dc5;
  for (let i = 0; i < text.length; i += 1) {
    hash ^= text.charCodeAt(i);
    hash = Math.imul(hash, 0x01000193) >>> 0;
  }
  return hash & 0x7fffffff;
}

/** Every store as plain JSON, for the learner to save. */
export async function exportAll() {
  const out = { format: "qf-course-export", version: 1, exported_at: new Date().toISOString(), stores: {} };
  for (const name of STORES) {
    out.stores[name] = Object.fromEntries(await entries(name));
  }
  return out;
}

/** Restore from an export. Validates the shape before touching anything. */
export async function importAll(payload) {
  if (!payload || payload.format !== "qf-course-export" || typeof payload.stores !== "object") {
    throw new Error("Not a course export file.");
  }
  for (const name of Object.keys(payload.stores)) {
    if (!STORES.includes(name)) throw new Error(`Unknown store in export: ${name}`);
  }
  for (const name of STORES) {
    const rows = payload.stores[name];
    if (!rows) continue;
    await safely((b) => b.clear(name), undefined);
    for (const [key, value] of Object.entries(rows)) {
      await put(name, key, value);
    }
  }
}
