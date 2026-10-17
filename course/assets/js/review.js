// Spaced-retrieval review session (BLUEPRINT §4). Shows due cards one at a
// time: the learner recalls the answer, reveals it, and rates their recall;
// FSRS-4.5 schedules the next review. Cards come from each module's cards.json
// and live only in this browser (export them from the progress panel).

import { renderMath } from "./math.js";
import { preview, RATINGS, review } from "./fsrs.js";
import * as store from "./store.js";

function el(tag, attrs = {}, text = "") {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
  if (text) node.textContent = text;
  return node;
}

export async function initReview(root) {
  const host = document.querySelector("[data-review]");
  if (!host) return;
  const counts = document.querySelector("[data-review-counts]");

  const due = async () => {
    const now = Date.now();
    const all = (await store.entries("cards")).map(([, v]) => v);
    return { all, due: all.filter((c) => c.fsrs.due <= now).sort((a, b) => a.fsrs.due - b.fsrs.due) };
  };

  const show = async () => {
    const { all, due: queue } = await due();
    counts.textContent = `${queue.length} due now · ${all.length} cards in your deck.`;
    if (!queue.length) {
      const next = all.length ? Math.min(...all.map((c) => c.fsrs.due)) : null;
      host.replaceChildren(
        el(
          "p",
          { class: "notice" },
          all.length
            ? `Nothing is due. The next card is due ${new Date(next).toLocaleString()}.`
            : "Your deck is empty. Finishing a lesson's retrieval quiz adds its cards here.",
        ),
      );
      return;
    }
    const entry = queue[0];
    const card = el("article", { class: "review-card", "aria-live": "polite" });
    card.append(el("p", { class: "eyebrow" }, `${entry.card.unit} · ${entry.card.lesson}${entry.card.grade ? ` · grade ${entry.card.grade}` : ""}`));
    const front = el("div", { class: "front" });
    front.textContent = entry.card.front;
    const back = el("div", { class: "back", hidden: "" });
    back.textContent = entry.card.back;
    card.append(front, back);
    const reveal = el("button", { type: "button", class: "button primary" }, "Show answer");
    const actions = el("div", { class: "review-actions", hidden: "" });
    const intervals = preview(entry.fsrs);
    for (const [name, grade] of Object.entries(RATINGS)) {
      const button = el("button", { type: "button", class: "button" });
      button.append(name[0].toUpperCase() + name.slice(1), el("span", { class: "interval" }, intervals[name]));
      button.addEventListener("click", async () => {
        await store.put("cards", entry.card.id, { card: entry.card, fsrs: review(entry.fsrs, grade) });
        show();
      });
      actions.append(button);
    }
    reveal.addEventListener("click", () => {
      back.hidden = false;
      actions.hidden = false;
      reveal.remove();
      actions.querySelector("button:nth-child(3)")?.focus();
    });
    host.replaceChildren(card, reveal, actions);
    await renderMath(root, card);
  };

  await show();
}
