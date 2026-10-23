// Unit tests for the strict math re-parse used by tools/page_smoke.py (tools/katex_strict.js).
// A stub stands in for KaTeX so the test runs offline; when the vendored KaTeX is present
// (tools/fetch_vendor.py), the real parser is checked too.

import assert from "node:assert/strict";
import { existsSync } from "node:fs";
import { createRequire } from "node:module";
import { test } from "node:test";

const require = createRequire(import.meta.url);
const { strictMathErrors } = require("../../tools/katex_strict.js");

const stub = {
  calls: [],
  renderToString(tex, options) {
    this.calls.push(options);
    if (/\\Sigmab/.test(tex)) throw new Error("KaTeX parse error: Undefined control sequence: \\Sigmab");
    return "<span></span>";
  },
};

test("every expression is re-parsed with throwOnError and strict errors, and failures are reported", () => {
  const items = [
    { tex: "\\Sigma b_v", display: false },
    { tex: "\\Sigmab_v", display: true },
  ];
  const errors = strictMathErrors(stub, items, { "\\E": "\\mathbb{E}" });
  assert.deepEqual(errors, [{ tex: "\\Sigmab_v", message: "KaTeX parse error: Undefined control sequence: \\Sigmab" }]);
  for (const options of stub.calls) {
    assert.equal(options.throwOnError, true);
    assert.equal(options.strict, "error");
  }
  assert.deepEqual(
    stub.calls.map((o) => o.displayMode),
    [false, true],
  );
});

test("the macros object passed in is not mutated", () => {
  const macros = { "\\R": "\\mathbb{R}" };
  strictMathErrors({ renderToString: (_t, o) => ((o.macros["\\new"] = "x"), "") }, [{ tex: "x" }], macros);
  assert.deepEqual(macros, { "\\R": "\\mathbb{R}" });
});

const vendored = new URL("../../course/assets/vendor/katex/katex.min.js", import.meta.url);
test("the vendored KaTeX flags undefined control sequences", { skip: !existsSync(vendored) }, () => {
  const katex = require(vendored.pathname);
  const errors = strictMathErrors(
    katex,
    [
      { tex: "\\E[x] + \\Sigma b_v", display: false },
      { tex: "\\Sigmab_v", display: false },
      { tex: "\\topb_v", display: true },
      { tex: "\\frac{1}{", display: false },
    ],
    { "\\E": "\\mathbb{E}" },
  );
  assert.deepEqual(
    errors.map((e) => e.tex),
    ["\\Sigmab_v", "\\topb_v", "\\frac{1}{"],
  );
});
