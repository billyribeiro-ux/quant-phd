// Inline labs: editable Python, run in the page, checked against the expected
// output stated before running (BUILDER_RULES §6.1).
//
// Output comparison is token by token. Numeric tokens agree when
// |actual − expected| ≤ tol·(1 + |expected|), with tol from data-tolerance;
// every other token must match exactly. tools/run_labs.py applies the same rule
// to the lab's byte-identical local twin, so a lab passes in both places or neither.

import { isStarted, runPython } from "./python.js";

const NUMBER = /^[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?%?$/;

export function compareOutput(actual, expected, tolerance) {
  const a = actual.trim().split(/\s+/).filter(Boolean);
  const e = expected.trim().split(/\s+/).filter(Boolean);
  if (a.length !== e.length) return { ok: false, reason: `expected ${e.length} tokens, got ${a.length}` };
  for (let i = 0; i < e.length; i += 1) {
    if (NUMBER.test(e[i]) && NUMBER.test(a[i])) {
      const x = parseFloat(a[i]);
      const y = parseFloat(e[i]);
      if (!(Math.abs(x - y) <= tolerance * (1 + Math.abs(y)))) {
        return { ok: false, reason: `token ${i + 1}: ${a[i]} differs from ${e[i]} beyond tolerance ${tolerance}` };
      }
    } else if (a[i] !== e[i]) {
      return { ok: false, reason: `token ${i + 1}: "${a[i]}" differs from "${e[i]}"` };
    }
  }
  return { ok: true, reason: "" };
}

function el(tag, attrs = {}, text = "") {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
  if (text) node.textContent = text;
  return node;
}

function enhance(lab) {
  const code = lab.querySelector("pre > code[data-run]");
  if (!code) return;
  const original = code.textContent;
  const pre = code.parentElement;
  const expected = lab.querySelector("pre.expected");
  const tolerance = expected ? parseFloat(expected.dataset.tolerance || "0") : 0;
  const packages = (lab.dataset.packages || "").split(/\s+/).filter(Boolean);
  const title = lab.querySelector("h3")?.textContent.trim() || lab.id;

  const editor = el("textarea", {
    class: "code-editor",
    spellcheck: "false",
    autocapitalize: "off",
    autocomplete: "off",
    "aria-label": `Python code for ${title}`,
  });
  editor.value = original;
  editor.rows = Math.min(28, Math.max(8, original.split("\n").length + 1));
  editor.addEventListener("keydown", (event) => {
    if (event.key === "Tab" && !event.shiftKey && !event.altKey && !event.ctrlKey && !event.metaKey) {
      event.preventDefault();
      editor.setRangeText("    ", editor.selectionStart, editor.selectionEnd, "end");
    }
  });

  const run = el("button", { type: "button", class: "button primary" }, "Run");
  const reset = el("button", { type: "button", class: "button" }, "Reset");
  const status = el("span", { class: "status", role: "status", "aria-live": "polite" });
  const toolbar = el("div", { class: "toolbar" });
  toolbar.append(run, reset, status);
  const output = el("pre", { class: "output", hidden: "" });

  pre.replaceWith(editor);
  editor.after(toolbar, output);
  status.textContent = "Press Run to execute in your browser (Esc then Tab leaves the editor).";

  editor.addEventListener("keydown", (event) => {
    if (event.key === "Escape") editor.blur();
    if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) run.click();
  });

  reset.addEventListener("click", () => {
    editor.value = original;
    output.hidden = true;
    status.className = "status";
    status.textContent = "Code reset to the original.";
  });

  run.addEventListener("click", async () => {
    run.disabled = true;
    status.className = "status";
    status.textContent = isStarted() ? "Running…" : "Starting Python (first run on this page downloads the runtime)…";
    const result = await runPython(editor.value, packages);
    run.disabled = false;
    output.hidden = false;
    output.classList.toggle("error", Boolean(result.error || result.stderr));
    const parts = [result.stdout || ""];
    if (result.stderr) parts.push(result.stderr);
    if (result.error) parts.push(result.error);
    output.textContent = parts.filter(Boolean).join("\n");
    const seconds = result.ms ? ` in ${(result.ms / 1000).toFixed(1)} s` : "";
    if (result.error) {
      status.className = "status bad";
      status.textContent = `Error${seconds}.`;
    } else if (expected && (editor.value === original || lab.classList.contains("completion"))) {
      // Completion problems (project rung 2) are graded on output: the learner fills the ___ blanks.
      const verdict = compareOutput(result.stdout || "", expected.textContent, tolerance);
      status.className = `status ${verdict.ok ? "ok" : "bad"}`;
      status.textContent = verdict.ok
        ? `Ran${seconds}; output matches the expected result.`
        : `Ran${seconds}; output differs from the expected result (${verdict.reason}).`;
      if (lab.classList.contains("completion")) {
        lab.dispatchEvent(new CustomEvent("completion:graded", { bubbles: true, detail: { ok: verdict.ok } }));
      }
    } else {
      status.textContent = `Ran${seconds}. You changed the code, so the output is not compared.`;
    }
    lab.dispatchEvent(new CustomEvent("lab:ran", { bubbles: true, detail: { ok: !result.error, result } }));
  });
}

export function initLabs(scope = document) {
  for (const lab of scope.querySelectorAll('section.lab[data-runtime="python"]')) enhance(lab);
}
