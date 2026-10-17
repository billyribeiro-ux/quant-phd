// Main-thread client for the Python worker (py-worker.js). One worker per page,
// created on first use, so pages that never run code never download Pyodide.

const TIMEOUT_MS = 120000;
let worker = null;
let nextId = 1;
const pending = new Map();

function spawn() {
  worker = new Worker(new URL("./py-worker.js", import.meta.url), { type: "module" });
  worker.onmessage = (event) => {
    const job = pending.get(event.data.id);
    if (!job) return;
    clearTimeout(job.timer);
    pending.delete(event.data.id);
    job.resolve(event.data);
  };
  worker.onerror = (event) => {
    for (const job of pending.values()) {
      clearTimeout(job.timer);
      job.resolve({ error: `Python worker failed: ${event.message || "unknown error"}` });
    }
    pending.clear();
    worker = null;
  };
}

function call(message) {
  if (!worker) spawn();
  const id = nextId++;
  return new Promise((resolve) => {
    const timer = setTimeout(() => {
      pending.delete(id);
      worker.terminate();
      worker = null;
      resolve({ error: `Stopped after ${TIMEOUT_MS / 1000} s. The Python runtime was restarted.` });
    }, TIMEOUT_MS);
    pending.set(id, { resolve, timer });
    worker.postMessage({ id, ...message });
  });
}

export const isStarted = () => worker !== null;
export const runPython = (code, packages = []) => call({ type: "run", code, packages });
export const runPytest = ({ files, test, env, packages = [], workdir = "/home/pyodide/work" }) =>
  call({ type: "pytest", files, test, env, packages, workdir });
