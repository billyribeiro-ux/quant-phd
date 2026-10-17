// In-browser autograder (BLUEPRINT §5.2). Runs the project's pytest suite in
// Pyodide against the learner's code, on the learner's own instance: the seed
// comes from their workspace ID, so two learners get materially different
// instances. The suite is the same file the learner can download and run
// locally with `pytest`; it is not secret, and the page does not pretend it is.

import { runPytest } from "./python.js";
import * as store from "./store.js";

function el(tag, attrs = {}, text = "") {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
  if (text) node.textContent = text;
  return node;
}

async function text(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`${url}: HTTP ${response.status}`);
  return response.text();
}

export async function initGrader(panel) {
  const unit = panel.dataset.unit;
  const base = panel.dataset.grader;
  const suite = panel.dataset.suite;
  const support = (panel.dataset.support || "").split(/\s+/).filter(Boolean);
  const solutionPath = panel.dataset.solution;
  const packages = (panel.dataset.packages || "").split(/\s+/).filter(Boolean);
  const draftKey = `${unit}/${solutionPath}`;

  const starter = await text(`${base}${panel.dataset.starter}`);
  const seed = await store.unitSeed(unit);
  const saved = await store.get("files", draftKey);

  const label = el("label", { for: `${unit}-solution` }, `Your ${solutionPath}`);
  const editor = el("textarea", {
    id: `${unit}-solution`,
    spellcheck: "false",
    autocapitalize: "off",
    autocomplete: "off",
  });
  editor.value = typeof saved === "string" ? saved : starter;
  const runButton = el("button", { type: "button", class: "button primary" }, "Run the autograder");
  const resetButton = el("button", { type: "button", class: "button" }, "Reset to starter");
  const fileInput = el("input", { type: "file", accept: ".py", "aria-label": `Load ${solutionPath} from a file` });
  const status = el("span", { class: "status", role: "status", "aria-live": "polite" });
  const controls = el("div", { class: "controls" });
  controls.append(runButton, resetButton, fileInput, status);
  const seedNote = el(
    "p",
    { class: "notice" },
    `Your instance seed is ${seed} (derived from your workspace ID). Locally: QF_SEED=${seed} pytest ${suite}`,
  );
  const results = el("ul", { class: "test-results", "aria-label": "Test results" });
  panel.append(seedNote, label, editor, controls, results);

  let timer = null;
  editor.addEventListener("input", () => {
    clearTimeout(timer);
    timer = setTimeout(() => store.put("files", draftKey, editor.value), 400);
  });
  editor.addEventListener("keydown", (event) => {
    if (event.key === "Tab" && !event.shiftKey && !event.ctrlKey && !event.metaKey && !event.altKey) {
      event.preventDefault();
      editor.setRangeText("    ", editor.selectionStart, editor.selectionEnd, "end");
    }
    if (event.key === "Escape") editor.blur();
  });
  resetButton.addEventListener("click", async () => {
    editor.value = starter;
    await store.put("files", draftKey, starter);
    status.textContent = "Reset to the starter code.";
  });
  fileInput.addEventListener("change", async () => {
    const file = fileInput.files?.[0];
    if (!file) return;
    editor.value = await file.text();
    await store.put("files", draftKey, editor.value);
    status.textContent = `Loaded ${file.name}.`;
  });

  runButton.addEventListener("click", async () => {
    runButton.disabled = true;
    results.replaceChildren();
    status.textContent = "Running the suite in your browser…";
    try {
      const files = [{ path: suite, text: await text(`${base}${suite}`) }];
      for (const name of support) files.push({ path: name, text: await text(`${base}${name}`) });
      const parts = solutionPath.split("/");
      for (let i = 1; i < parts.length; i += 1) {
        files.push({ path: `${parts.slice(0, i).join("/")}/__init__.py`, text: "" });
      }
      files.push({ path: solutionPath, text: editor.value });
      const outcome = await runPytest({ files, test: suite, env: { QF_SEED: String(seed) }, packages });
      if (outcome.error) {
        status.textContent = `The suite could not run: ${outcome.error}`;
        return;
      }
      const passed = outcome.results.filter((r) => r.outcome === "passed").length;
      const total = outcome.results.filter((r) => r.when === "call" || r.outcome !== "passed").length;
      for (const r of outcome.results) {
        const li = el("li", { class: r.outcome });
        li.append(el("span", { class: "outcome" }, r.outcome === "passed" ? "PASS" : "FAIL"), r.test);
        if (r.message) li.append(el("span", { class: "message" }, r.message));
        results.append(li);
      }
      const all = outcome.exit === 0;
      status.textContent = all
        ? `All ${passed} tests pass on seed ${seed}.`
        : `${passed} of ${total} tests pass on seed ${seed}.`;
      await store.put("grader", unit, { passed, total, all, seed, at: Date.now() });
      panel.dispatchEvent(new CustomEvent("grader:done", { bubbles: true, detail: { all, passed, total } }));
    } catch (error) {
      status.textContent = `The suite could not run: ${error.message}`;
    } finally {
      runButton.disabled = false;
    }
  });
}
