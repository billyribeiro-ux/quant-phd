// Round 7 verifier script: render every \( \) and \[ \] span of the slice pages with the vendored KaTeX
// (throwOnError true) and report any parse error. Usage: node katex_render_check.js <repo_root>
const fs = require("fs");
const path = require("path");
const katex = require(path.join(process.argv[2], "course/assets/vendor/katex/katex.min.js"));
const notation = JSON.parse(fs.readFileSync(path.join(process.argv[2], "notation/notation.json"), "utf8"));
const macros = Object.fromEntries(Object.entries(notation.macros).map(([name, def]) => [name, def.tex]));
const pages = ["index.html", "L01.html", "L02.html", "L03.html"];
let total = 0, bad = 0;
for (const p of pages) {
  const f = path.join(process.argv[2], "course/modules/SC/SC1", p);
  let html = fs.readFileSync(f, "utf8");
  html = html.replace(/<[^>]+>/g, " ").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&");
  const spans = [];
  for (const m of html.matchAll(/\\\[([\s\S]*?)\\\]/g)) spans.push([m[1], true]);
  for (const m of html.matchAll(/\\\(([\s\S]*?)\\\)/g)) spans.push([m[1], false]);
  for (const [tex, display] of spans) {
    total++;
    try { katex.renderToString(tex, { displayMode: display, throwOnError: true, macros }); }
    catch (e) { bad++; console.log("ERR", p, JSON.stringify(tex).slice(0, 120), String(e.message).slice(0, 120)); }
  }
}
console.log("math spans:", total, "parse errors:", bad);
