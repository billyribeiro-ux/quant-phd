// Citations and evidence grades.
//
// Pages never contain bibliographic text: they carry registry keys
// (`data-cite="lo1990data white2000reality"`) and, for quoted numbers, an exact
// `data-locator`. This module renders them from `assets/data/references.json`,
// which tools/build_site.py generates from the verified registry. It numbers
// references by first appearance, adds the grade badge and reference markers
// to every claim, fills short and full citation slots, builds the page's
// reference list, and shows a popover with the full citation on hover or focus.

export const GRADES = {
  T: "Theorem: proved on the page or by a precisely cited proof",
  A: "Replicated out of sample by independent teams",
  B: "Published in a top peer-reviewed venue; not robustly replicated or contested",
  C: "Working paper, practitioner research, or single-sample evidence",
  D: "Practitioner lore without systematic evidence",
  X: "Refuted, failed to replicate, or retracted",
};

function keysOf(el) {
  return (el.dataset.cite || "").split(/\s+/).filter(Boolean);
}

function make(tag, attrs = {}, text = "") {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v);
  if (text) el.textContent = text;
  return el;
}

function link(entry) {
  if (entry.doi) return { href: `https://doi.org/${entry.doi}`, label: `doi:${entry.doi}` };
  if (entry.url) return { href: entry.url, label: new URL(entry.url).hostname };
  return null;
}

let popover = null;
function showPopover(anchor, entry, locator) {
  hidePopover();
  popover = make("div", { class: "popover", role: "tooltip", id: "cite-popover" });
  popover.append(make("span", {}, entry.full));
  if (locator) popover.append(make("span", { class: "ref-locator" }, `Locator: ${locator}`));
  document.body.append(popover);
  const rect = anchor.getBoundingClientRect();
  const width = popover.offsetWidth;
  const left = Math.min(Math.max(8, rect.left + window.scrollX - width / 2), window.scrollX + innerWidth - width - 8);
  popover.style.left = `${left}px`;
  popover.style.top = `${rect.bottom + window.scrollY + 6}px`;
  anchor.setAttribute("aria-describedby", "cite-popover");
}
function hidePopover() {
  if (popover) {
    document.querySelectorAll('[aria-describedby="cite-popover"]').forEach((a) => a.removeAttribute("aria-describedby"));
    popover.remove();
    popover = null;
  }
}

function addGrade(el) {
  const grade = el.dataset.grade;
  if (grade && !el.querySelector(":scope > .grade")) {
    const badge = make("span", { class: "grade", "data-grade": grade, title: GRADES[grade] || "" }, grade);
    badge.prepend(make("span", { class: "visually-hidden" }, "evidence grade "));
    el.append(badge);
  }
  el.classList.add("is-enhanced");
}

export async function renderCitations(root) {
  // Claims proved on the page carry a grade but no citation; they still get their badge.
  for (const claim of document.querySelectorAll(".claim:not([data-cite])")) addGrade(claim);
  const targets = [...document.querySelectorAll("[data-cite]")];
  if (!targets.length) return { keys: [], missing: [] };
  const response = await fetch(`${root}assets/data/references.json`);
  if (!response.ok) throw new Error(`references.json: HTTP ${response.status}`);
  const registry = await response.json();

  const order = [];
  const number = new Map();
  const missing = new Set();
  for (const el of targets) {
    for (const key of keysOf(el)) {
      if (!(key in registry)) missing.add(key);
      else if (!number.has(key)) {
        number.set(key, order.length + 1);
        order.push(key);
      }
    }
  }

  const refAnchor = (key, locator) => {
    const n = number.get(key);
    const a = make("a", { href: `#ref-${n}`, "data-key": key }, String(n));
    a.addEventListener("mouseenter", () => showPopover(a, registry[key], locator));
    a.addEventListener("focus", () => showPopover(a, registry[key], locator));
    a.addEventListener("mouseleave", hidePopover);
    a.addEventListener("blur", hidePopover);
    return a;
  };

  for (const el of targets) {
    const keys = keysOf(el).filter((k) => number.has(k));
    const locator = el.dataset.locator || "";
    if (el.classList.contains("claim")) {
      addGrade(el);
      if (keys.length) {
        const sup = make("sup", { class: "cite-refs" });
        sup.append("[");
        keys.forEach((key, i) => {
          if (i) sup.append(", ");
          sup.append(refAnchor(key, locator));
        });
        sup.append("]");
        el.append(sup);
      }
    } else if (el.matches(".ref") && !el.textContent.trim()) {
      keys.forEach((key, i) => {
        if (i) el.append("; ");
        const a = make("a", { href: `#ref-${number.get(key)}`, "data-key": key }, registry[key].short);
        a.addEventListener("mouseenter", () => showPopover(a, registry[key], locator));
        a.addEventListener("focus", () => showPopover(a, registry[key], locator));
        a.addEventListener("mouseleave", hidePopover);
        a.addEventListener("blur", hidePopover);
        el.append(a);
      });
    } else if (el.matches(".reading-list [data-cite]") && !el.textContent.trim()) {
      for (const key of keys) {
        el.append(make("span", {}, registry[key].full), " ");
        const target = link(registry[key]);
        if (target) el.append(make("a", { href: target.href, rel: "noopener" }, target.label));
      }
    }
  }

  for (const list of document.querySelectorAll("ol[data-references]")) {
    list.replaceChildren();
    for (const key of order) {
      const entry = registry[key];
      const li = make("li", { id: `ref-${number.get(key)}` });
      li.append(make("span", {}, entry.full), " ");
      const target = link(entry);
      if (target) li.append(make("a", { href: target.href, rel: "noopener" }, target.label), " ");
      li.append(make("span", { class: "ref-key" }, key));
      list.append(li);
    }
  }

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") hidePopover();
  });
  for (const key of missing) {
    console.error(`Unknown citation key: ${key}`);
  }
  return { keys: order, missing: [...missing] };
}
