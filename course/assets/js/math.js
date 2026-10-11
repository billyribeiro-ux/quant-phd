// Math rendering with the vendored KaTeX (loaded by the page as classic scripts).
// Delimiters follow BUILDER_RULES §3: \( … \) inline, \[ … \] display.
// A KaTeX parse error is reported with console.error so the smoke test fails.

export function initMath(root = document.body, macros = {}) {
  if (typeof window.renderMathInElement !== "function") {
    if (root.textContent.includes("\\(") || root.textContent.includes("\\[")) {
      console.error("Page contains math but KaTeX auto-render is not loaded");
    }
    return;
  }
  window.renderMathInElement(root, {
    delimiters: [
      { left: "\\[", right: "\\]", display: true },
      { left: "\\(", right: "\\)", display: false },
    ],
    macros,
    throwOnError: false,
    strict: "error",
  });
  for (const failure of root.querySelectorAll(".katex-error")) {
    console.error(`KaTeX could not render: ${failure.getAttribute("title") ?? failure.textContent}`);
  }
}
