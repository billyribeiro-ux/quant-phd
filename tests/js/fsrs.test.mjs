// Unit tests for the browser-side scheduler and lab-output comparison.
// Run by tests/test_js.py with Node's built-in test runner (no dependencies).

import assert from "node:assert/strict";
import { test } from "node:test";

import { DEFAULT_WEIGHTS as W, intervalDays, newCard, retrievability, review } from "../../course/assets/js/fsrs.js";
import { compareOutput } from "../../course/assets/js/labs.js";

const DAY = 86400000;
const close = (a, b, tol = 1e-9) => assert.ok(Math.abs(a - b) <= tol, `${a} != ${b}`);

test("retrievability is 0.9 one stability after review, and the interval at 0.9 equals S", () => {
  for (const s of [0.5, 3.7, 40, 900]) {
    close(retrievability(s, s), 0.9, 1e-12);
    close(intervalDays(s, 0.9), s, 1e-9);
  }
  assert.ok(intervalDays(10, 0.95) < 10 && intervalDays(10, 0.8) > 10, "higher target retention means shorter intervals");
});

test("a new card takes the initial stability and difficulty of its first grade", () => {
  for (const grade of [1, 2, 3, 4]) {
    const card = review(newCard(0), grade, 0);
    close(card.stability, W[grade - 1]);
    close(card.difficulty, Math.min(10, Math.max(1, W[4] - (grade - 3) * W[5])));
    assert.equal(card.reps, 1);
    assert.equal(card.lapses, 0, "a first 'again' is a first exposure, not a lapse");
  }
});

test("a review at time zero still counts as a review (regression: falsy timestamp)", () => {
  const first = review(newCard(0), 3, 0);
  const second = review(first, 3, first.due);
  assert.ok(second.stability > first.stability * 2, "a successful second review must grow stability");
});

test("successful recall follows the FSRS-4.5 stability formula", () => {
  const first = review(newCard(0), 3, 0);
  const elapsed = 6;
  const r = retrievability(elapsed, first.stability);
  const d = first.difficulty;
  const expected = first.stability * (1 + Math.exp(W[8]) * (11 - d) * first.stability ** -W[9] * (Math.exp(W[10] * (1 - r)) - 1));
  close(review(first, 3, elapsed * DAY).stability, expected, 1e-9);
  const hard = review(first, 2, elapsed * DAY).stability;
  const easy = review(first, 4, elapsed * DAY).stability;
  assert.ok(hard < expected && expected < easy, "hard penalty below good, easy bonus above");
});

test("a lapse follows the forgetting formula, counts a lapse and comes back in ten minutes", () => {
  const first = review(newCard(0), 3, 0);
  const second = review(first, 3, first.due);
  const r = retrievability((second.due - second.last_review) / DAY, second.stability);
  const lapsed = review(second, 1, second.due);
  const d = second.difficulty;
  close(lapsed.stability, W[11] * d ** -W[12] * ((second.stability + 1) ** W[13] - 1) * Math.exp(W[14] * (1 - r)), 1e-9);
  assert.equal(lapsed.lapses, 1);
  assert.equal(lapsed.due - second.due, 10 * 60 * 1000);
});

test("difficulty stays within [1, 10] under any sequence of grades", () => {
  let card = newCard(0);
  let now = 0;
  for (let i = 0; i < 200; i += 1) {
    card = review(card, (i * 7) % 4 + 1, now);
    assert.ok(card.difficulty >= 1 && card.difficulty <= 10);
    now = card.due;
  }
});

test("invalid grades are rejected", () => {
  assert.throws(() => review(newCard(0), 5, 0), RangeError);
});

test("lab output comparison: numbers within tolerance, other tokens exact", () => {
  assert.ok(compareOutput("x 1.0001", "x 1.0", 1e-3).ok);
  assert.ok(!compareOutput("x 1.01", "x 1.0", 1e-3).ok);
  assert.ok(!compareOutput("y 1.0", "x 1.0", 1e-3).ok, "labels must match exactly");
  assert.ok(!compareOutput("1 2", "1 2 3", 1).ok, "token counts must match");
  assert.ok(compareOutput("12.5%", "12.50%", 1e-9).ok, "percent tokens compare numerically");
});
