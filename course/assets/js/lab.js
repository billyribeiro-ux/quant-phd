// In-page Python labs on the vendored Pyodide runtime (CPython compiled to WebAssembly).
//
//   <section class="lab" data-runtime="python">
//     <div class="lab-head"><h3>Lab 1 · Title</h3><div class="lab-actions"></div></div>
//     <p class="hypothesis">…</p>
//     <pre><code class="language-python" data-run>…</code></pre>
//     <pre class="expected" data-tolerance="1e-9">…</pre>
//     <p class="interpretation">…</p>
//   </section>
//
// Output is compared with the expected block token by token; numeric tokens may
// differ by at most data-tolerance (absolute). The same comparison runs in CI
// against the pytest twin of every lab (tools/run_labs.py).

import { h } from "./data.js";

let runtime = null;

function loadRuntime() {
  if (!runtime) {
    const indexURL = new URL("../vendor/pyodide/", import.meta.url).href;
    runtime = import(new URL("../vendor/pyodide/pyodide.mjs", import.meta.url).href).then(({ loadPyodide }) =>
      loadPyodide({ indexURL }),
    );
  }
  return runtime;
}

const NUMBER = /^[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?$/;

export function outputsMatch(actual, expected, tolerance) {
  const a = actual.trim().split(/\s+/);
  const e = expected.trim().split(/\s+/);
  if (a.length !== e.length) return false;
  return a.every((token, i) => {
    if (token === e[i]) return true;
    if (NUMBER.test(token) && NUMBER.test(e[i])) return Math.abs(Number(token) - Number(e[i])) <= tolerance;
    return false;
  });
}

async function runLab(lab, button, status, output) {
  button.disabled = true;
  status.dataset.state = "running";
  status.textContent = runtime ? "Running…" : "Loading Python runtime…";
  output.textContent = "";
  try {
    const pyodide = await loadRuntime();
    status.textContent = "Running…";
    const lines = [];
    pyodide.setStdout({ batched: (text) => lines.push(text) });
    pyodide.setStderr({ batched: (text) => lines.push(text) });
    await pyodide.runPythonAsync(lab.querySelector("code[data-run]").textContent);
    const actual = lines.join("\n");
    output.textContent = actual;
    const expected = lab.querySelector("pre.expected");
    if (expected) {
      const tolerance = Number(expected.dataset.tolerance ?? 0);
      const ok = outputsMatch(actual, expected.textContent, tolerance);
      status.dataset.state = ok ? "pass" : "fail";
      status.textContent = ok ? "✓ Matches the expected result" : "✗ Output differs from the expected result";
    } else {
      status.dataset.state = "pass";
      status.textContent = "Done";
    }
  } catch (error) {
    status.dataset.state = "fail";
    status.textContent = "✗ Error";
    output.textContent = String(error?.message ?? error);
  } finally {
    button.disabled = false;
  }
}

export function initLabs(root = document) {
  for (const lab of root.querySelectorAll('.lab[data-runtime="python"]')) {
    const actions = lab.querySelector(".lab-actions") ?? lab.querySelector(".lab-head");
    const status = h("span", { class: "lab-status", role: "status", "aria-live": "polite" });
    const button = h("button", { class: "btn btn-primary", type: "button" }, "Run");
    const output = h("pre", { class: "lab-output", "aria-label": "Lab output" });
    actions.append(status, button);
    lab.querySelector("pre.expected")?.insertAdjacentElement("beforebegin", output);
    button.addEventListener("click", () => runLab(lab, button, status, output));
  }
}
