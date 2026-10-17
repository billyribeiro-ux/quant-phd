// Retrieval quizzes (BUILDER_RULES §4.2.9). Each item is answered from memory,
// checked instantly, and explained. Completing a lesson's quiz adds that
// lesson's cards (cards.json) to the learner's spaced-retrieval deck, so what
// was retrieved once is retrieved again on the FSRS schedule.

import { newCard } from "./fsrs.js";
import * as store from "./store.js";

function el(tag, attrs = {}, text = "") {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
  if (text) node.textContent = text;
  return node;
}

function grade(item) {
  if (item.dataset.kind === "numeric") {
    const input = item.querySelector("input");
    const value = parseFloat(input.value);
    if (!Number.isFinite(value)) return null;
    const answer = parseFloat(item.dataset.answer);
    const tol = parseFloat(item.dataset.tolerance || "0");
    return Math.abs(value - answer) <= tol;
  }
  const chosen = item.querySelector("input[type=radio]:checked");
  if (!chosen) return null;
  return chosen.closest("label.option").hasAttribute("data-correct");
}

/** Adds a lesson's cards to the deck. Returns how many were new, or null when the lesson has no cards. */
async function addLessonCards(cardsUrl, unit, lesson) {
  let cards = [];
  try {
    const response = await fetch(cardsUrl);
    if (!response.ok) return null;
    cards = (await response.json()).filter((c) => c.lesson === lesson);
  } catch {
    return null;
  }
  if (!cards.length) return null;
  let added = 0;
  for (const card of cards) {
    if (!(await store.get("cards", card.id))) {
      await store.put("cards", card.id, { card: { ...card, unit }, fsrs: newCard() });
      added += 1;
    }
  }
  return added;
}

export function initQuizzes(scope = document) {
  for (const quiz of scope.querySelectorAll("section.quiz")) {
    const unit = quiz.dataset.unit;
    const page = quiz.dataset.page;
    const items = [...quiz.querySelectorAll("li.item")];
    // Placement skill checks: items marked data-skill test what the scaffolded rungs teach, and must all be right.
    const skills = items.flatMap((item, index) => (item.hasAttribute("data-skill") ? [index] : []));
    const score = el("p", { class: "score", role: "status", "aria-live": "polite" });
    quiz.append(score);
    const results = new Map();

    const update = async () => {
      const correct = [...results.values()].filter(Boolean).length;
      score.textContent = `${results.size} of ${items.length} answered · ${correct} correct.`;
      if (results.size === items.length) {
        await store.put("quiz", `${unit}/${page}`, { correct, total: items.length, at: Date.now() });
        const mastery = parseFloat(quiz.dataset.mastery || "");
        if (Number.isFinite(mastery)) {
          // Placement diagnostic: the mastery bar decides whether the scaffolded rungs can be skipped.
          const overall = correct / items.length >= mastery;
          const skilled = skills.every((index) => results.get(index) === true);
          const passed = overall && skilled;
          await store.put("progress", `${unit}/placement`, { done: passed, correct, total: items.length, at: Date.now() });
          score.textContent += passed
            ? ` That meets the ${Math.round(mastery * 100)}% mastery bar and every skill check: you may skip rungs 1–2 of the project ladder.`
            : overall
              ? " You met the overall bar but missed a skill check: work through rungs 1–2 of the project ladder."
              : ` The mastery bar is ${Math.round(mastery * 100)}%: work through the lessons and every rung of the ladder.`;
          return;
        }
        const added = await addLessonCards(quiz.dataset.cards || "cards.json", unit, page);
        if (added) score.textContent += ` ${added} cards from this lesson were added to your review deck.`;
        else if (added === 0) score.textContent += " This lesson's cards are already in your review deck.";
      }
    };

    items.forEach((item, index) => {
      const button = el("button", { type: "button", class: "button" }, "Check");
      const feedback = el("p", { class: "feedback", role: "status", "aria-live": "polite" });
      const explain = item.querySelector(".explain");
      explain.before(button, feedback);
      button.addEventListener("click", () => {
        const verdict = grade(item);
        if (verdict === null) {
          feedback.className = "feedback";
          feedback.textContent = "Answer first, then check.";
          return;
        }
        item.classList.add("answered");
        if (item.dataset.kind !== "numeric") {
          item.querySelectorAll("label.option").forEach((label) => {
            label.classList.toggle("correct", label.hasAttribute("data-correct"));
            label.classList.toggle("chosen", label.querySelector("input").checked);
          });
        }
        feedback.className = `feedback ${verdict ? "ok" : "bad"}`;
        feedback.textContent = verdict ? "Correct." : "Not quite — read the explanation.";
        explain.hidden = false;
        if (!results.has(index)) results.set(index, verdict);
        update();
      });
    });
    update();
  }
}
