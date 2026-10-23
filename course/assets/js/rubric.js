// Rubric self-assessment and calibration (BUILDER_RULES §5.4.3, BLUEPRINT §5.2).
//
// A rubric-graded page carries a <table class="rubric"> whose criterion rows have data-criterion, annotated
// exemplars (<article class="exemplar" data-level data-scores="4,4,3,...">) and a <section class="rubric-self">
// naming both. The learner scores their own work on every criterion, then scores each exemplar with its
// annotations hidden, then reveals the official scoring. The page then shows, criterion by criterion, where
// their scoring of each exemplar diverged from it, next to their self-scores, and offers a plain-text summary
// to keep with the work. Scores live in the learner's browser through store.js; every storage access here is
// wrapped, so blocked or cleared storage costs persistence, never the form. Nothing leaves the browser.

import * as defaultStore from "./store.js";

export const LEVELS = [4, 3, 2, 1];
const SELF = "self";

/** True for an integer level 1-4. */
export function isLevel(value) {
  return Number.isInteger(value) && value >= 1 && value <= 4;
}

/** "4,3,2" -> [4, 3, 2] when there is one valid level per criterion, else null. */
export function parseScores(text, count) {
  const parts = String(text ?? "")
    .split(",")
    .map((part) => part.trim());
  if (parts.length !== count || parts.some((part) => !/^[1-4]$/.test(part))) return null;
  return parts.map(Number);
}

/** A fresh record: no scores for any target, official scoring hidden. */
export function emptyRecord(criteria, targets) {
  const scores = {};
  for (const target of targets) scores[target] = {};
  return { scores, revealed: false };
}

/** A stored record, cleaned: unknown targets and criteria dropped, anything but a level 1-4 discarded. */
export function cleanRecord(raw, criteria, targets) {
  const record = emptyRecord(criteria, targets);
  if (!raw || typeof raw !== "object") return record;
  for (const target of targets) {
    const given = raw.scores?.[target];
    if (!given || typeof given !== "object") continue;
    for (const id of criteria) {
      if (isLevel(given[id])) record.scores[target][id] = given[id];
    }
  }
  record.revealed = raw.revealed === true;
  return record;
}

/** Per criterion: the learner's level, the official one, and learner minus official (null when unscored). */
export function compare(learner, official, criteria) {
  const rows = criteria.map((criterion, i) => {
    const mine = isLevel(learner?.[criterion]) ? learner[criterion] : null;
    return { criterion, learner: mine, official: official[i], diff: mine === null ? null : mine - official[i] };
  });
  const pick = (test) => rows.filter(test).map((row) => row.criterion);
  return {
    rows,
    matched: pick((row) => row.diff === 0),
    higher: pick((row) => row.diff !== null && row.diff > 0),
    lower: pick((row) => row.diff !== null && row.diff < 0),
    unscored: pick((row) => row.diff === null),
  };
}

function list(ids) {
  return ids.length <= 1 ? ids.join("") : `${ids.slice(0, -1).join(", ")} and ${ids[ids.length - 1]}`;
}

/** One plain sentence on how the learner's scoring of one exemplar compares with the official scoring. */
export function summarize(label, result) {
  const scored = result.rows.length - result.unscored.length;
  if (scored === 0) return `${label}: not scored yet.`;
  const parts = [`${label}: you matched the official level on ${result.matched.length} of ${scored} criteria scored`];
  if (result.higher.length) parts.push(`you scored higher on ${list(result.higher)}`);
  if (result.lower.length) parts.push(`lower on ${list(result.lower)}`);
  let text = `${parts.join("; ")}.`;
  if (result.unscored.length) text += ` Not scored: ${list(result.unscored)}.`;
  return text;
}

/** The record for `key`, cleaned; an empty record when storage is unavailable or holds nothing usable. */
export async function loadRecord(key, criteria, targets, store = defaultStore) {
  try {
    return cleanRecord(await store.get("kv", key), criteria, targets);
  } catch {
    return emptyRecord(criteria, targets);
  }
}

/** Saves the record; returns whether storage accepted it. store.js's put resolves false when the backend
 * refused the write (it catches the error itself), and a store that throws counts as a refusal too. */
export async function saveRecord(key, record, store = defaultStore) {
  try {
    return (await store.put("kv", key, record)) !== false;
  } catch {
    return false;
  }
}

/** A plain-text summary of the self-scores and the calibration, for the learner to keep with the work. */
export function plainSummary(criteria, record, exemplars) {
  const lines = ["Self-assessment"];
  for (const { id, name } of criteria) {
    const level = record.scores[SELF]?.[id];
    lines.push(`${name}: ${isLevel(level) ? `level ${level}` : "not scored"}`);
  }
  lines.push("", "Calibration on the exemplars");
  for (const exemplar of exemplars) {
    const ids = criteria.map((c) => c.id);
    lines.push(summarize(exemplar.label, compare(record.scores[exemplar.id], exemplar.official, ids)));
  }
  return lines.join("\n");
}

function el(tag, attrs = {}, text = "") {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
  if (text) node.textContent = text;
  return node;
}

function readCriteria(table) {
  return [...table.querySelectorAll("tr[data-criterion]")].map((row) => ({
    id: row.dataset.criterion,
    name: (row.querySelector("th")?.textContent || row.dataset.criterion).trim(),
  }));
}

function radioGroup(prefix, target, criterion, checked) {
  const group = el("fieldset", { class: "rubric-levels" });
  group.append(el("legend", {}, criterion.name));
  for (const level of LEVELS) {
    const label = el("label", { class: "rubric-level" });
    const input = el("input", { type: "radio", name: `${prefix}-${target}-${criterion.id}`, value: String(level) });
    input.dataset.target = target;
    input.dataset.criterion = criterion.id;
    if (checked === level) input.checked = true;
    label.append(input, document.createTextNode(` ${level}`));
    group.append(label);
  }
  return group;
}

function setRevealed(exemplars, revealed) {
  for (const { node } of exemplars) {
    for (const part of node.querySelectorAll(".annotation, [data-reveal]")) part.hidden = !revealed;
    node.classList.toggle("revealed", revealed);
  }
}

/**
 * The words the form uses for the learner's own work, read from optional data attributes on the
 * self-assessment section; the defaults are S7's memo wording.
 */
export function workWording(dataset = {}) {
  const pick = (value, fallback) => (typeof value === "string" && value.trim() ? value.trim() : fallback);
  return {
    label: pick(dataset.workLabel, "Your memo"),
    noun: pick(dataset.workNoun, "memo"),
    summaryPath: pick(dataset.summaryPath, "memo/self_assessment.md"),
  };
}

function comparisonTable(criteria, record, exemplars, ownLabel) {
  const ids = criteria.map((c) => c.id);
  const results = exemplars.map((e) => compare(record.scores[e.id], e.official, ids));
  const table = el("table", { class: "rubric-compare" });
  table.append(el("caption", {}, "Your scoring against the official scoring, criterion by criterion"));
  const head = el("tr");
  head.append(el("th", { scope: "col" }, "Criterion"), el("th", { scope: "col", class: "num" }, ownLabel));
  for (const e of exemplars) {
    head.append(el("th", { scope: "col", class: "num" }, `${e.label}: you`));
    head.append(el("th", { scope: "col", class: "num" }, `${e.label}: official`));
  }
  table.append(el("thead"));
  table.tHead.append(head);
  const body = el("tbody");
  criteria.forEach((criterion, i) => {
    const row = el("tr");
    row.append(el("th", { scope: "row" }, criterion.name));
    const own = record.scores[SELF]?.[criterion.id];
    row.append(el("td", { class: "num" }, isLevel(own) ? String(own) : "–"));
    results.forEach((result) => {
      const { learner, official, diff } = result.rows[i];
      const cell = el("td", { class: "num" }, learner === null ? "–" : String(learner));
      if (diff !== null && diff !== 0) {
        cell.classList.add(diff > 0 ? "higher" : "lower");
        cell.append(el("span", { class: "diff" }, ` (${diff > 0 ? "+" : "−"}${Math.abs(diff)})`));
      }
      row.append(cell, el("td", { class: "num" }, String(official)));
    });
    body.append(row);
  });
  table.append(body);
  return { table, results };
}

/** Builds the self-assessment form inside `section` and restores the learner's saved scores. */
export async function initRubric(section, { store = defaultStore } = {}) {
  const table = document.getElementById(section.dataset.rubric || "");
  if (!table) throw new Error(`rubric table #${section.dataset.rubric} not found`);
  const criteria = readCriteria(table);
  if (criteria.length === 0) throw new Error("the rubric has no rows with data-criterion");
  const ids = criteria.map((c) => c.id);
  const exemplars = (section.dataset.exemplars || "")
    .split(/\s+/)
    .filter(Boolean)
    .map((id) => {
      const node = document.getElementById(id);
      const official = node ? parseScores(node.dataset.scores, ids.length) : null;
      if (!node || !official) throw new Error(`exemplar #${id} is missing or has no data-scores for every criterion`);
      return { id, node, official, label: node.dataset.label || id };
    });
  const wording = workWording(section.dataset);
  const targets = [SELF, ...exemplars.map((e) => e.id)];
  const key = `rubric:${section.dataset.storeKey || location.pathname}`;
  const prefix = key.replace(/[^A-Za-z0-9]+/g, "-");
  let record = await loadRecord(key, ids, targets, store);

  const host = section.querySelector("[data-rubric-form]") || section;
  host.replaceChildren();
  const form = el("form", { class: "rubric-form", novalidate: "" });
  form.addEventListener("submit", (event) => event.preventDefault());
  const blocks = [{ id: SELF, label: wording.label }, ...exemplars];
  for (const target of blocks) {
    const box = el("fieldset", { class: "rubric-target" });
    const title = target.id === SELF ? wording.label : `${target.label}, scored before you reveal its annotations`;
    box.append(el("legend", {}, title));
    for (const criterion of criteria) {
      box.append(radioGroup(prefix, target.id, criterion, record.scores[target.id][criterion.id]));
    }
    form.append(box);
  }
  const status = el("p", { class: "rubric-status", role: "status", "aria-live": "polite" });
  const actions = el("div", { class: "rubric-actions" });
  const reveal = el("button", { type: "button", class: "button primary" }, "Reveal the official scoring");
  const clear = el("button", { type: "button", class: "button" }, "Clear my scores");
  actions.append(reveal, clear);
  const results = el("div", { class: "rubric-results" });
  host.append(form, actions, status, results);

  const persist = async (message) => {
    const ok = await saveRecord(key, record, store);
    const kept = ok && store.persistent !== false;
    status.textContent = kept
      ? message
      : "Not saved: this browser is not storing data for the course, so these scores last only until you leave the page.";
  };

  const render = () => {
    setRevealed(exemplars, record.revealed);
    results.replaceChildren();
    reveal.textContent = record.revealed ? "Hide the official scoring" : "Reveal the official scoring";
    reveal.setAttribute("aria-expanded", String(record.revealed));
    if (!record.revealed) return;
    const { table: compareTable, results: comparisons } = comparisonTable(criteria, record, exemplars, wording.label);
    const wrap = el("div", { class: "table-wrap" });
    wrap.append(compareTable);
    results.append(wrap);
    for (const [i, e] of exemplars.entries()) {
      results.append(el("p", { class: "rubric-summary" }, summarize(e.label, comparisons[i])));
    }
    const generous = [...new Set(comparisons.flatMap((c) => c.higher))];
    if (generous.length) {
      const advice = `You were more generous than the rubric on ${list(generous)}: re-read your own ${wording.noun} against those descriptors before you keep your score.`;
      results.append(el("p", { class: "rubric-summary" }, advice));
    }
    const label = el("label", { class: "rubric-copy" }, `Summary to keep as ${wording.summaryPath}`);
    const text = el("textarea", { readonly: "", rows: String(criteria.length + exemplars.length + 4) });
    text.value = plainSummary(criteria, record, exemplars);
    label.append(text);
    results.append(label);
  };

  form.addEventListener("change", async (event) => {
    const input = event.target;
    if (!(input instanceof HTMLInputElement) || input.type !== "radio") return;
    record.scores[input.dataset.target][input.dataset.criterion] = Number(input.value);
    await persist("Saved in this browser.");
    if (record.revealed) render();
  });
  reveal.addEventListener("click", async () => {
    record.revealed = !record.revealed;
    await persist(record.revealed ? "Official scoring shown." : "Official scoring hidden.");
    render();
  });
  clear.addEventListener("click", async () => {
    record = emptyRecord(ids, targets);
    for (const input of form.querySelectorAll("input[type=radio]")) input.checked = false;
    await persist("Scores cleared.");
    render();
  });
  render();
}
