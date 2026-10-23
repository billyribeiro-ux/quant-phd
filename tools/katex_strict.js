// Strict re-parse of every rendered math expression, used by tools/page_smoke.py.
// site.js renders with throwOnError: false, and KaTeX then shows an undefined control sequence as red text
// without a .katex-error element. This re-parses each expression's TeX source with throwOnError: true and
// strict: "error", so any undefined command or parse error is reported.
// Loaded two ways: injected into a page (defines window.__strictMath) and required by tests/js (CommonJS).

(function (root) {
  /** Re-parses each {tex, display} item; returns [{tex, message}] for every expression that fails. */
  function strictMathErrors(katex, items, macros) {
    const errors = [];
    for (const { tex, display } of items) {
      try {
        katex.renderToString(tex, {
          displayMode: Boolean(display),
          throwOnError: true,
          strict: "error",
          trust: false,
          macros: { ...macros },
        });
      } catch (error) {
        errors.push({ tex, message: String(error && error.message ? error.message : error) });
      }
    }
    return errors;
  }

  /** The TeX source and display mode of every expression KaTeX rendered in the document. */
  function renderedMath(doc) {
    return [...doc.querySelectorAll(".katex")]
      .filter((node) => !node.parentElement || !node.parentElement.closest(".katex"))
      .map((node) => {
        const annotation = node.querySelector('annotation[encoding="application/x-tex"]');
        return { tex: annotation ? annotation.textContent : null, display: Boolean(node.closest(".katex-display")) };
      })
      .filter((item) => item.tex !== null);
  }

  const api = { strictMathErrors, renderedMath };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.__strictMath = api;
})(typeof window !== "undefined" ? window : globalThis);
