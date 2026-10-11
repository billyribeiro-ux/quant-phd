// Citations. Every citation on every page resolves against the verified registry
// (assets/data/references.json, published from references/references.json).
//
//   <span class="claim" data-grade="B" data-cite="key1 key2" data-locator="Table 2">…</span>
//   <ol class="reading-list" data-reading="key1 key2"></ol>
//   <section data-references></section>   (numbered list of everything cited on the page)
//
// An unknown key is rendered as a visible red marker and reported with
// console.error, which the browser smoke test treats as a failure.

import { h, loadJSON } from "./data.js";

const SMALL_WORDS = new Set("a an and as at but by for in nor of on or the to vs via with".split(" "));
const GRADE_TEXT = {
  T: "Theorem: proved on the page or with a cited proof",
  A: "Replicated out of sample by independent teams",
  B: "Peer-reviewed, but contested or not robustly replicated",
  C: "Working paper or single-sample evidence",
  D: "Practitioner lore without systematic evidence",
  X: "Refuted, failed replication, or retracted",
};

function displayTitle(title) {
  // Some Crossref records are in ALL CAPS; render those in title case.
  if (title !== title.toUpperCase()) return title;
  return title
    .toLowerCase()
    .split(" ")
    .map((word, i) => (i > 0 && SMALL_WORDS.has(word) ? word : word.charAt(0).toUpperCase() + word.slice(1)))
    .join(" ");
}

function authorLine(authors) {
  const names = (authors ?? []).map((a) => a.family);
  if (names.length === 0) return "Anonymous";
  if (names.length === 1) return names[0];
  if (names.length === 2) return `${names[0]} & ${names[1]}`;
  if (names.length <= 4) return `${names.slice(0, -1).join(", ")} & ${names.at(-1)}`;
  return `${names[0]} et al.`;
}

export function formatReference(ref) {
  const venue = ref.container
    ? `${ref.container}${ref.volume ? ` ${ref.volume}` : ""}${ref.issue ? `(${ref.issue})` : ""}${ref.pages ? `, ${ref.pages}` : ""}`
    : "";
  const fragment = document.createDocumentFragment();
  fragment.append(`${authorLine(ref.authors)} (${ref.year ?? "n.d."}). `);
  fragment.append(h("span", { class: "ref-title" }, displayTitle(ref.title)), ". ");
  if (venue) fragment.append(h("span", { class: "ref-meta" }, h("i", {}, venue), ". "));
  if (ref.doi) fragment.append(h("a", { href: `https://doi.org/${ref.doi}`, rel: "noopener" }, `doi:${ref.doi}`));
  return fragment;
}

let openPopover = null;

function closePopover() {
  openPopover?.remove();
  openPopover = null;
}

function showPopover(anchor, ref, locator) {
  closePopover();
  const pop = h("div", { class: "cite-pop", role: "dialog", "aria-label": "Citation" }, formatReference(ref));
  if (locator) pop.append(h("div", { class: "ref-meta" }, `Locator: ${locator}`));
  document.body.append(pop);
  const rect = anchor.getBoundingClientRect();
  const left = Math.min(window.scrollX + rect.left, window.scrollX + document.documentElement.clientWidth - pop.offsetWidth - 16);
  pop.style.left = `${Math.max(16, left)}px`;
  pop.style.top = `${window.scrollY + rect.bottom + 6}px`;
  openPopover = pop;
}

export async function initCitations(root = document) {
  const claims = root.querySelectorAll(".claim[data-cite], .claim[data-grade]");
  const readingLists = root.querySelectorAll("[data-reading]");
  const referenceSections = root.querySelectorAll("[data-references]");
  if (!claims.length && !readingLists.length) return;

  const registry = (await loadJSON("references.json")).entries;
  const order = new Map(); // key -> citation number, in order of first appearance

  for (const claim of claims) {
    const grade = claim.dataset.grade;
    if (grade) {
      const badge = h("abbr", { class: `grade grade-${grade}`, title: GRADE_TEXT[grade] ?? "Unknown grade" }, grade);
      if (!GRADE_TEXT[grade]) console.error(`Unknown evidence grade "${grade}"`);
      claim.append(badge);
    }
    for (const key of (claim.dataset.cite ?? "").split(/\s+/).filter(Boolean)) {
      const ref = registry[key];
      if (!ref) {
        console.error(`Citation key not in the verified registry: ${key}`);
        claim.append(h("span", { class: "cite cite-missing", title: `Unverified citation: ${key}` }, "?"));
        continue;
      }
      if (!order.has(key)) order.set(key, order.size + 1);
      const button = h(
        "button",
        { class: "cite", type: "button", "aria-label": `Reference ${order.get(key)}: ${authorLine(ref.authors)} ${ref.year}` },
        `[${order.get(key)}]`,
      );
      button.addEventListener("click", (event) => {
        event.stopPropagation();
        showPopover(button, ref, claim.dataset.locator);
      });
      claim.append(button);
    }
  }

  for (const list of readingLists) {
    for (const key of list.dataset.reading.split(/\s+/).filter(Boolean)) {
      const ref = registry[key];
      if (!ref) {
        console.error(`Reading-list key not in the verified registry: ${key}`);
        continue;
      }
      list.append(h("li", { id: `ref-${key}` }, formatReference(ref)));
    }
  }

  for (const section of referenceSections) {
    const list = h("ol", { class: "reading-list" });
    for (const key of order.keys()) list.append(h("li", { id: `cite-${key}` }, formatReference(registry[key])));
    section.append(list);
  }

  document.addEventListener("click", (event) => {
    if (openPopover && !openPopover.contains(event.target)) closePopover();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closePopover();
  });
}
