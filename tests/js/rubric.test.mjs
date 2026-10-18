// Unit tests for the rubric self-assessment module (course/assets/js/rubric.js).
// Run by tests/test_js.py with Node's built-in test runner (no dependencies). Node has no IndexedDB, so
// store.js falls back to its in-memory backend here, as it does in a browser that blocks storage.

import assert from "node:assert/strict";
import { test } from "node:test";

import {
  cleanRecord,
  compare,
  emptyRecord,
  isLevel,
  loadRecord,
  parseScores,
  plainSummary,
  saveRecord,
  summarize,
} from "../../course/assets/js/rubric.js";
import * as store from "../../course/assets/js/store.js";

const CRITERIA = ["C1", "C2", "C3", "C4", "C5", "C6"];
const TARGETS = ["self", "exemplar-a", "exemplar-b"];

test("levels are the integers 1 to 4 and nothing else", () => {
  for (const ok of [1, 2, 3, 4]) assert.ok(isLevel(ok));
  for (const bad of [0, 5, 2.5, "3", null, undefined, NaN]) assert.ok(!isLevel(bad), String(bad));
});

test("official scores parse only with one valid level per criterion", () => {
  assert.deepEqual(parseScores("2,2,2,2,3,2", 6), [2, 2, 2, 2, 3, 2]);
  assert.deepEqual(parseScores(" 4, 4,4 ,3,4,4", 6), [4, 4, 4, 3, 4, 4]);
  assert.equal(parseScores("4,4,4", 6), null, "too few");
  assert.equal(parseScores("4,4,4,3,4,5", 6), null, "a level outside 1-4");
  assert.equal(parseScores("4,4,4,3,4,2.5", 6), null, "a fractional level");
  assert.equal(parseScores(undefined, 6), null);
});

test("comparison reports learner minus official, criterion by criterion", () => {
  const official = [2, 2, 2, 2, 3, 2];
  const learner = { C1: 2, C2: 3, C3: 4, C4: 1, C6: 2 };
  const result = compare(learner, official, CRITERIA);
  assert.deepEqual(
    result.rows.map((r) => r.diff),
    [0, 1, 2, -1, null, 0],
  );
  assert.deepEqual(result.matched, ["C1", "C6"]);
  assert.deepEqual(result.higher, ["C2", "C3"]);
  assert.deepEqual(result.lower, ["C4"]);
  assert.deepEqual(result.unscored, ["C5"]);
});

test("a non-level stored score counts as unscored, never as a divergence", () => {
  const result = compare({ C1: "4", C2: 9, C3: 2.5 }, [4, 4, 4, 4, 4, 4], CRITERIA);
  assert.deepEqual(result.unscored, CRITERIA);
  assert.equal(result.matched.length + result.higher.length + result.lower.length, 0);
});

test("summaries name the divergent criteria and the unscored ones", () => {
  const result = compare({ C1: 2, C2: 3, C3: 4, C4: 1, C6: 2 }, [2, 2, 2, 2, 3, 2], CRITERIA);
  assert.equal(
    summarize("Exemplar A", result),
    "Exemplar A: you matched the official level on 2 of 5 criteria scored; you scored higher on C2 and C3; " +
      "lower on C4. Not scored: C5.",
  );
  assert.equal(summarize("Exemplar B", compare({}, [4, 4, 4, 3, 4, 4], CRITERIA)), "Exemplar B: not scored yet.");
});

test("stored records are cleaned: unknown targets, criteria and invalid levels are dropped", () => {
  const raw = {
    scores: { self: { C1: 3, C2: 7, C9: 4 }, "exemplar-a": { C3: 2 }, intruder: { C1: 4 } },
    revealed: "yes",
  };
  const record = cleanRecord(raw, CRITERIA, TARGETS);
  assert.deepEqual(record.scores, { self: { C1: 3 }, "exemplar-a": { C3: 2 }, "exemplar-b": {} });
  assert.equal(record.revealed, false, "only a literal true reveals the scoring");
  for (const garbage of [null, undefined, 42, "text", [], { scores: "x" }]) {
    assert.deepEqual(cleanRecord(garbage, CRITERIA, TARGETS), emptyRecord(CRITERIA, TARGETS));
  }
});

test("a store that throws costs persistence, never the form", async () => {
  const broken = {
    async get() {
      throw new Error("SecurityError: storage blocked");
    },
    async put() {
      throw new Error("QuotaExceededError");
    },
  };
  assert.deepEqual(await loadRecord("rubric:x", CRITERIA, TARGETS, broken), emptyRecord(CRITERIA, TARGETS));
  assert.equal(await saveRecord("rubric:x", emptyRecord(CRITERIA, TARGETS), broken), false);
  const synchronous = {
    get() {
      throw new Error("thrown before a promise exists");
    },
    put() {
      throw new Error("thrown before a promise exists");
    },
  };
  assert.deepEqual(await loadRecord("rubric:x", CRITERIA, TARGETS, synchronous), emptyRecord(CRITERIA, TARGETS));
  assert.equal(await saveRecord("rubric:x", {}, synchronous), false);
});

test("scores round-trip through store.js, which falls back to memory without IndexedDB", async () => {
  const record = emptyRecord(CRITERIA, TARGETS);
  record.scores.self.C1 = 3;
  record.scores["exemplar-b"].C4 = 4;
  record.revealed = true;
  assert.equal(await saveRecord("rubric:S7/project/memo", record, store), true);
  assert.deepEqual(await loadRecord("rubric:S7/project/memo", CRITERIA, TARGETS, store), record);
  assert.equal(store.persistent, false, "Node has no IndexedDB, so nothing claims to persist");
});

test("the plain-text summary lists every self-score and one calibration line per exemplar", () => {
  const criteria = CRITERIA.map((id) => ({ id, name: `${id} name` }));
  const record = emptyRecord(CRITERIA, TARGETS);
  record.scores.self = { C1: 4, C2: 3 };
  record.scores["exemplar-a"] = { C1: 2, C2: 2, C3: 2, C4: 2, C5: 3, C6: 2 };
  const exemplars = [
    { id: "exemplar-a", label: "Exemplar A", official: [2, 2, 2, 2, 3, 2] },
    { id: "exemplar-b", label: "Exemplar B", official: [4, 4, 4, 3, 4, 4] },
  ];
  const lines = plainSummary(criteria, record, exemplars).split("\n");
  assert.equal(lines[0], "Self-assessment");
  assert.deepEqual(lines.slice(1, 4), ["C1 name: level 4", "C2 name: level 3", "C3 name: not scored"]);
  assert.ok(lines.includes("Exemplar A: you matched the official level on 6 of 6 criteria scored."));
  assert.ok(lines.includes("Exemplar B: not scored yet."));
});
