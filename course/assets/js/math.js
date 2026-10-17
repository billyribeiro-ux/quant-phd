// KaTeX rendering with the program's registered macros (notation/notation.json).
// Errors render visibly (KaTeX marks them .katex-error) so page_smoke.py can fail
// a page with any unrendered expression.

export async function renderMath(root, scope = document.body) {
  if (typeof window.renderMathInElement !== "function") {
    throw new Error("KaTeX auto-render is not loaded");
  }
  let macros = {};
  const response = await fetch(`${root}assets/data/notation.json`);
  if (response.ok) {
    const notation = await response.json();
    macros = Object.fromEntries(Object.entries(notation.macros).map(([name, def]) => [name, def.tex]));
  }
  window.renderMathInElement(scope, {
    delimiters: [
      { left: "\\[", right: "\\]", display: true },
      { left: "\\(", right: "\\)", display: false },
    ],
    macros,
    throwOnError: false,
    strict: "error",
    trust: false,
    ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code", "option"],
    ignoredClasses: ["no-math"],
    errorCallback: (message, error) => console.error(`KaTeX: ${message}`, error),
  });
}
