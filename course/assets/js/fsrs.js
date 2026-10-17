// FSRS-4.5 spaced-repetition scheduler (Free Spaced Repetition Scheduler; the
// model family of Ye, Su & Cao 2022, registry key ye2022stochastic), with the
// published FSRS-4.5 default parameters and formulas as documented in the
// open-spaced-repetition "The Algorithm" wiki. Pure functions; no I/O.
//
// Memory model. Retrievability after t days at stability S:
//   R(t, S) = (1 + F·t/S)^C,  C = −0.5,  F = 19/81,  so R(S, S) = 0.9.
// The interval that brings R down to the target retention r:
//   I(S, r) = (S/F)·(r^(1/C) − 1),  which equals S when r = 0.9.

export const DEFAULT_WEIGHTS = Object.freeze([
  0.4872, 1.4003, 3.7145, 13.8206, 5.1618, 1.2298, 0.8975, 0.031, 1.6474, 0.1367, 1.0461, 2.1072, 0.0793, 0.3246,
  1.587, 0.2272, 2.8755,
]);
export const RATINGS = Object.freeze({ again: 1, hard: 2, good: 3, easy: 4 });
const DECAY = -0.5;
const FACTOR = 19 / 81;
const DAY_MS = 86400000;
const RELEARN_MS = 10 * 60 * 1000;
const MAX_INTERVAL_DAYS = 36500;

const clamp = (x, lo, hi) => Math.min(hi, Math.max(lo, x));

export function retrievability(elapsedDays, stability) {
  return Math.pow(1 + (FACTOR * elapsedDays) / stability, DECAY);
}

export function intervalDays(stability, retention = 0.9) {
  return (stability / FACTOR) * (Math.pow(retention, 1 / DECAY) - 1);
}

function initialStability(w, grade) {
  return Math.max(w[grade - 1], 0.1);
}

function initialDifficulty(w, grade) {
  return clamp(w[4] - (grade - 3) * w[5], 1, 10);
}

function nextDifficulty(w, difficulty, grade) {
  const shifted = difficulty - w[6] * (grade - 3);
  return clamp(w[7] * initialDifficulty(w, 3) + (1 - w[7]) * shifted, 1, 10);
}

function recallStability(w, d, s, r, grade) {
  const hardPenalty = grade === RATINGS.hard ? w[15] : 1;
  const easyBonus = grade === RATINGS.easy ? w[16] : 1;
  return s * (1 + Math.exp(w[8]) * (11 - d) * Math.pow(s, -w[9]) * (Math.exp(w[10] * (1 - r)) - 1) * hardPenalty * easyBonus);
}

function forgetStability(w, d, s, r) {
  return w[11] * Math.pow(d, -w[12]) * (Math.pow(s + 1, w[13]) - 1) * Math.exp(w[14] * (1 - r));
}

/** A card that has never been reviewed. */
export function newCard(now = Date.now()) {
  return { state: "new", due: now, stability: 0, difficulty: 0, reps: 0, lapses: 0, last_review: null };
}

/**
 * Schedule a review. Returns the updated card; `due` is a millisecond timestamp.
 * "Again" re-queues the card for relearning in ten minutes; other grades schedule
 * whole days at the target retention.
 */
export function review(card, grade, now = Date.now(), { retention = 0.9, weights = DEFAULT_WEIGHTS } = {}) {
  if (![1, 2, 3, 4].includes(grade)) throw new RangeError(`grade must be 1-4, got ${grade}`);
  let stability;
  let difficulty;
  if (card.state === "new" || card.last_review === null) {
    stability = initialStability(weights, grade);
    difficulty = initialDifficulty(weights, grade);
  } else {
    const elapsed = Math.max(0, (now - card.last_review) / DAY_MS);
    const r = retrievability(elapsed, card.stability);
    difficulty = nextDifficulty(weights, card.difficulty, grade);
    stability =
      grade === RATINGS.again
        ? forgetStability(weights, card.difficulty, card.stability, r)
        : recallStability(weights, card.difficulty, card.stability, r, grade);
  }
  const days = clamp(Math.round(intervalDays(stability, retention)), 1, MAX_INTERVAL_DAYS);
  return {
    state: "review",
    stability,
    difficulty,
    reps: card.reps + 1,
    lapses: card.lapses + (grade === RATINGS.again && card.state !== "new" ? 1 : 0),
    last_review: now,
    due: grade === RATINGS.again ? now + RELEARN_MS : now + days * DAY_MS,
  };
}

/** Human-readable time until the next review for each grade, for the rating buttons. */
export function preview(card, now = Date.now(), options = {}) {
  const out = {};
  for (const [name, grade] of Object.entries(RATINGS)) {
    const next = review(card, grade, now, options);
    const ms = next.due - now;
    out[name] = ms < DAY_MS ? `${Math.round(ms / 60000)} min` : formatDays(Math.round(ms / DAY_MS));
  }
  return out;
}

function formatDays(days) {
  if (days < 31) return `${days} d`;
  if (days < 365) return `${(days / 30.44).toFixed(1)} mo`;
  return `${(days / 365.25).toFixed(1)} y`;
}
