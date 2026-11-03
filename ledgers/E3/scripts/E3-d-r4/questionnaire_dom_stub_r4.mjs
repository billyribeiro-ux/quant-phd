// Round-4 verifier (E3-d): drives the project.html questionnaire script against a minimal DOM stub (no browser).
// Usage: node questionnaire_dom_stub_r4.mjs <path-to-extracted-script.js>
import { readFileSync } from "node:fs";

class El {
  constructor(tag) { this.tagName = tag; this.children = []; this.attrs = {}; this.listeners = {}; this.style = {};
    this.disabled = false; this.checked = false; this.value = ""; this.name = ""; this.type = ""; this._text = ""; this.parent = null; }
  setAttribute(k, v) { this.attrs[k] = String(v); if (k === "name") this.name = String(v); }
  getAttribute(k) { return this.attrs[k] ?? null; }
  addEventListener(ev, fn) { (this.listeners[ev] ??= []).push(fn); }
  dispatch(ev) { for (const fn of this.listeners[ev] ?? []) fn({ target: this }); }
  get textContent() { return this._text + this.children.map((c) => (typeof c === "string" ? c : c.textContent)).join(""); }
  set textContent(v) { this._text = String(v); this.children = []; }
  append(...nodes) { for (const n of nodes) { if (typeof n !== "string") n.parent = this; this.children.push(n); } }
  replaceChildren(...nodes) { this.children = []; this.append(...nodes); }
  remove() { if (this.parent) this.parent.children = this.parent.children.filter((c) => c !== this); }
  click() { this.dispatch("click"); }
  all(pred, out = []) { for (const c of this.children) { if (typeof c !== "string") { if (pred(c)) out.push(c); c.all(pred, out); } } return out; }
  querySelector(sel) {
    const m = /^input\[name="([^"]+)"\]:checked$/.exec(sel);
    if (m) return this.all((e) => e.tagName === "input" && e.name === m[1] && e.checked)[0] ?? null;
    throw new Error("unsupported selector " + sel);
  }
}
const document = {
  body: new El("body"),
  createElement: (t) => new El(t),
  querySelector(sel) { const want = /^\[data-(\w+)\]$/.exec(sel)?.[1]; return root.attrs[`data-${want}`] !== undefined ? root : null; },
};
const root = new El("div"); root.setAttribute("data-questionnaire", "");
root.children = [new El("p")];
const blobs = []; let revoked = 0;
globalThis.document = document;
globalThis.Blob = class { constructor(parts, opts) { this.text = parts.join(""); this.type = opts?.type; blobs.push(this); } };
globalThis.URL = { createObjectURL: () => "blob:stub", revokeObjectURL: () => { revoked++; } };
const realTimeout = globalThis.setTimeout;
const noopTimeout = () => 0;
const src = readFileSync(process.argv[2], "utf8");
// The script looks up [data-questionnaire] with querySelector; the stub returns root for that selector.
new Function("document", "Blob", "URL", "setTimeout", src)(document, Blob, URL, noopTimeout);

const tick = () => new Promise((r) => realTimeout(r, 0));
const statusLine = root.all((e) => e.getAttribute("role") === "status")[0];
const fileInput = root.all((e) => e.tagName === "input" && e.type === "file")[0];
const pairList = root.all((e) => e.tagName === "ol")[0];
const exportButton = root.all((e) => e.tagName === "button")[0];
const results = [];
const check = (name, ok, detail = "") => results.push(`${ok ? "PASS" : "FAIL"} ${name}${detail ? " | " + detail : ""}`);

async function load(text) {
  fileInput.files = [{ text: async () => text }];
  fileInput.dispatch("change");
  for (let i = 0; i < 5; i++) await tick();
}
const instrument = [
  { pair_id: 0, prizes_a: [1000, -500], probs_a: ["1/2", "1/2"], prizes_b: [300], probs_b: ["1"] },
  { pair_id: 7, prizes_a: [2000], probs_a: ["1"], prizes_b: [3000, -1000], probs_b: ["1/4", "3/4"] },
];
await load(JSON.stringify(instrument));
check("instrument loads two pairs", statusLine.textContent.startsWith("2 pairs loaded."), statusLine.textContent);
check("export enabled after load", exportButton.disabled === false);
check("one fieldset per pair", pairList.children.length === 2, `items=${pairList.children.length}`);
exportButton.dispatch("click");
check("export refused with no choices", statusLine.textContent === "No export: pair 0, 7 has no choice yet.", statusLine.textContent);
check("no Blob created when refused", blobs.length === 0);
const radios = (i) => root.all((e) => e.tagName === "input" && e.type === "radio" && e.name === `q-pair-${i}`);
radios(0).find((r) => r.value === "A").checked = true;
exportButton.dispatch("click");
check("export refused with one pair missing", statusLine.textContent === "No export: pair 7 has no choice yet.", statusLine.textContent);
radios(1).find((r) => r.value === "B").checked = true;
exportButton.dispatch("click");
check("export accepted when every pair has a choice", blobs.length === 1 && statusLine.textContent === "Exported 2 responses to responses.json.", statusLine.textContent);
const out = JSON.parse(blobs[0].text);
check("export shape matches responses (b)", JSON.stringify(out) === JSON.stringify([
  { pair_id: 0, choice: "A", prizes_a: [1000, -500], probs_a: ["1/2", "1/2"], prizes_b: [300], probs_b: ["1"] },
  { pair_id: 7, choice: "B", prizes_a: [2000], probs_a: ["1"], prizes_b: [3000, -1000], probs_b: ["1/4", "3/4"] },
]), JSON.stringify(out));
check("download name and type", blobs[0].type === "application/json");
await load("[]");
check("empty list refused with message", statusLine.textContent === "The file was not loaded: the file must be a non-empty JSON list of pairs.", statusLine.textContent);
check("export disabled after bad file", exportButton.disabled === true);
await load(JSON.stringify([{ pair_id: 1, prizes_a: [1.5], probs_a: ["1"], prizes_b: [0], probs_b: ["1"] }]));
check("fractional cents refused", /lacks a whole-number pair_id/.test(statusLine.textContent), statusLine.textContent);
await load(JSON.stringify([{ pair_id: 2, prizes_a: [100], probs_a: ["0.5"], prizes_b: [0], probs_b: ["1"] }]));
check("decimal probability refused (numerator/denominator required)", /lacks a whole-number pair_id/.test(statusLine.textContent), statusLine.textContent);
await load(JSON.stringify([{ pair_id: 3, prizes_a: [100, 200], probs_a: ["1/2", "1/2"], prizes_b: [50], probs_b: ["1"] }]));
check("valid second load replaces the list", statusLine.textContent.startsWith("1 pairs loaded."), statusLine.textContent);
console.log(results.join("\n"));
console.log("PASSES:", results.filter((r) => r.startsWith("PASS")).length, "of", results.length);
