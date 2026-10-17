// Page entry point. Every page loads this module; it enhances whatever the page
// contains (math, citations, labs, quizzes, the autograder, the program map, the
// review deck) and records progress. When everything has rendered it sets
// <html data-ready="true">, which tools/page_smoke.py waits for.

import { initLabs } from "./labs.js";
import { renderMath } from "./math.js";
import { initQuizzes } from "./quiz.js";
import { renderCitations } from "./refs.js";
import * as store from "./store.js";

const root = document.documentElement.dataset.root || "./";
const errors = [];
window.__qf = { errors };

function setTheme(theme) {
  if (theme) document.documentElement.dataset.theme = theme;
  else delete document.documentElement.dataset.theme;
  try {
    if (theme) localStorage.setItem("qf-theme", theme);
    else localStorage.removeItem("qf-theme");
  } catch {
    /* storage unavailable: the choice lasts for this page view only */
  }
}

function initThemeToggle() {
  const button = document.querySelector("[data-theme-toggle]");
  if (!button) return;
  const order = [null, "dark", "light"];
  const label = (t) => (t === "dark" ? "Theme: dark" : t === "light" ? "Theme: light" : "Theme: system");
  const current = () => document.documentElement.dataset.theme || null;
  button.textContent = label(current());
  button.addEventListener("click", () => {
    const next = order[(order.indexOf(current()) + 1) % order.length];
    setTheme(next);
    button.textContent = label(next);
  });
}

function initToc() {
  const toc = document.querySelector("nav.toc[data-auto]");
  const main = document.querySelector("main");
  if (!toc || !main) return;
  const heads = [...main.querySelectorAll("h2[id]")];
  const list = document.createElement("ol");
  const links = new Map();
  for (const h of heads) {
    const li = document.createElement("li");
    const a = document.createElement("a");
    a.href = `#${h.id}`;
    a.textContent = h.dataset.toc || h.textContent.replace(/^\s*\d+(\.\d+)*\s*/, "");
    li.append(a);
    list.append(li);
    links.set(h, a);
  }
  toc.append(list);
  if (!("IntersectionObserver" in window)) return;
  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          links.forEach((a) => a.removeAttribute("aria-current"));
          links.get(entry.target)?.setAttribute("aria-current", "true");
        }
      }
    },
    { rootMargin: "0px 0px -70% 0px" },
  );
  heads.forEach((h) => observer.observe(h));
}

async function initProgress() {
  const unit = document.documentElement.dataset.unit;
  const page = document.documentElement.dataset.page;
  const button = document.querySelector("[data-complete]");
  if (unit && page && button) {
    const key = `${unit}/${page}`;
    const render = (done) => {
      button.textContent = done ? "Completed ✓ (click to undo)" : "Mark this lesson complete";
      button.setAttribute("aria-pressed", String(Boolean(done)));
    };
    render((await store.get("progress", key))?.done);
    button.addEventListener("click", async () => {
      const done = !(await store.get("progress", key))?.done;
      await store.put("progress", key, { done, at: Date.now() });
      render(done);
    });
  }
  for (const card of document.querySelectorAll("[data-progress-key]")) {
    const record = await store.get("progress", card.dataset.progressKey);
    if (record?.done) card.classList.add("done");
  }
  const passed = document.querySelector("[data-grader-status]");
  if (passed && unit) {
    const record = await store.get("grader", unit);
    passed.textContent = record
      ? `Autograder: ${record.passed} of ${record.total} tests passed on seed ${record.seed}.`
      : "Autograder: not yet attempted.";
  }
}

function initExport() {
  const exportButton = document.querySelector("[data-export]");
  const importInput = document.querySelector("[data-import]");
  const status = document.querySelector("[data-export-status]");
  exportButton?.addEventListener("click", async () => {
    const blob = new Blob([JSON.stringify(await store.exportAll(), null, 2)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `qf-course-progress-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(a.href);
    if (status) status.textContent = "Progress exported.";
  });
  importInput?.addEventListener("change", async () => {
    const file = importInput.files?.[0];
    if (!file) return;
    try {
      await store.importAll(JSON.parse(await file.text()));
      if (status) status.textContent = "Progress restored. Reloading…";
      location.reload();
    } catch (error) {
      if (status) status.textContent = `Import failed: ${error.message}`;
    }
  });
}

async function storageNotice() {
  await store.get("kv", "probe");
  if (!store.persistent) {
    const note = document.createElement("p");
    note.className = "notice warn";
    note.setAttribute("role", "status");
    note.textContent =
      "This browser is not keeping your progress (private window or blocked storage). Use Export on the program map to save it.";
    document.querySelector("main")?.prepend(note);
  }
}

async function step(name, fn) {
  try {
    await fn();
  } catch (error) {
    errors.push(`${name}: ${error.message}`);
    console.error(`${name}:`, error);
  }
}

async function main() {
  initThemeToggle();
  initToc();
  await step("math", () => renderMath(root));
  await step("citations", async () => {
    const { missing } = await renderCitations(root);
    if (missing.length) throw new Error(`unknown citation keys: ${missing.join(", ")}`);
  });
  await step("labs", () => initLabs());
  await step("quizzes", () => initQuizzes());
  for (const panel of document.querySelectorAll(".grader-panel[data-unit]")) {
    await step("grader", async () => (await import("./grader.js")).initGrader(panel));
  }
  if (document.querySelector("[data-program-map]")) {
    await step("map", async () => (await import("./map.js")).initMap(root));
  }
  if (document.querySelector("[data-review]")) {
    await step("review", async () => (await import("./review.js")).initReview(root));
  }
  const figures = document.documentElement.dataset.figures;
  if (figures) {
    // A module's own figure code (computed live from formulas or embedded data), e.g. "figures.js".
    await step("figures", async () => (await import(new URL(figures, location.href).href)).drawFigures(root));
  }
  await step("progress", initProgress);
  initExport();
  await step("storage", storageNotice);
  document.documentElement.dataset.ready = "true";
}

main();
