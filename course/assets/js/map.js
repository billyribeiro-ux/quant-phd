// Program map interactions. The map's markup is rendered statically by
// tools/build_site.py; this module adds selection (a module's full prerequisite
// closure and everything that depends on it), credential and track views,
// search across titles, cores and concepts, and the learner's progress.

import * as store from "./store.js";

function closure(id, modules, edge) {
  const seen = new Set();
  const stack = [...edge(modules[id])];
  while (stack.length) {
    const next = stack.pop();
    if (seen.has(next)) continue;
    seen.add(next);
    stack.push(...edge(modules[next]));
  }
  return seen;
}

function el(tag, attrs = {}, text = "") {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
  if (text) node.textContent = text;
  return node;
}

export async function initMap(root) {
  const map = document.querySelector("[data-program-map]");
  if (!map) return;
  const program = await (await fetch(`${root}assets/data/program.json`)).json();
  const modules = Object.fromEntries(program.parts.flatMap((p) => p.modules).map((m) => [m.id, m]));
  const dependents = Object.fromEntries(Object.keys(modules).map((id) => [id, []]));
  for (const m of Object.values(modules)) for (const p of m.prereqs) dependents[p].push(m.id);
  const chips = new Map([...map.querySelectorAll(".chip[data-id]")].map((c) => [c.dataset.id, c]));
  const detail = document.querySelector("[data-map-detail]");
  const search = document.querySelector("[data-map-search]");
  const view = document.querySelector("[data-map-view]");
  const summary = document.querySelector("[data-map-summary]");

  const passed = new Set((await store.entries("grader")).filter(([, v]) => v && v.all).map(([k]) => k));
  for (const id of passed) chips.get(id)?.classList.add("done");

  let selected = null;
  let viewSet = null;

  const paint = () => {
    const query = (search?.value || "").trim().toLowerCase();
    const pre = selected ? closure(selected, modules, (m) => m.prereqs) : new Set();
    const post = selected ? closure(selected, modules, (m) => dependents[m.id]) : new Set();
    let shown = 0;
    for (const [id, chip] of chips) {
      const m = modules[id];
      const haystack = `${m.id} ${m.title} ${m.core} ${m.introduces.join(" ")}`.toLowerCase();
      const matches = !query || haystack.includes(query);
      const inView = !viewSet || viewSet.has(id);
      chip.classList.toggle("dimmed", !(matches && inView));
      chip.classList.toggle("in-set", Boolean(viewSet && viewSet.has(id)));
      chip.classList.toggle("is-prereq", pre.has(id));
      chip.classList.toggle("is-dependent", post.has(id));
      chip.setAttribute("aria-pressed", String(id === selected));
      if (matches && inView) shown += 1;
    }
    if (summary) {
      const hours = viewSet ? [...viewSet].reduce((sum, id) => sum + modules[id].hours, 0) : null;
      summary.textContent = viewSet
        ? `${viewSet.size} modules, ${hours.toLocaleString()} module hours in this view; ${shown} match the search.`
        : `${shown} of ${chips.size} modules match.`;
    }
  };

  const describe = (id) => {
    const m = modules[id];
    const pre = closure(id, modules, (x) => x.prereqs);
    const hours = [...pre].reduce((sum, p) => sum + modules[p].hours, 0) + m.hours;
    const panel = el("div", { class: "panel" });
    panel.append(el("p", { class: "eyebrow" }, `${m.id} · tier ${m.tier} · ${m.hours} h`));
    panel.append(el("h3", {}, m.title));
    panel.append(el("p", {}, m.core));
    const facts = el("ul", { class: "meta-row" });
    facts.append(el("li", {}, `Prerequisites: ${m.prereqs.length ? m.prereqs.join(", ") : "none"}`));
    facts.append(el("li", {}, `Path from zero: ${pre.size + 1} modules, ${hours.toLocaleString()} h`));
    facts.append(el("li", {}, `Unlocks: ${dependents[id].length ? dependents[id].join(", ") : "none"}`));
    panel.append(facts);
    panel.append(el("h4", {}, `Project · ${m.project.title}`));
    panel.append(el("p", {}, `${m.project.brief} Grading: ${m.project.grading}.`));
    if (m.debate) panel.append(el("p", {}, `Debate: ${m.debate}`));
    panel.append(el("h4", {}, `Introduces ${m.introduces.length} concepts`));
    panel.append(el("p", { class: "concepts" }, m.introduces.join(" · ")));
    if (m.href) {
      const open = el("a", { class: "button primary", href: `${root}${m.href}` }, `Open ${m.id}`);
      panel.append(open);
    } else {
      panel.append(el("p", { class: "notice" }, "Not yet built. Modules are released after independent verification."));
    }
    detail.replaceChildren(panel);
  };

  for (const [id, chip] of chips) {
    chip.addEventListener("click", () => {
      selected = selected === id ? null : id;
      if (selected) describe(selected);
      paint();
    });
  }
  search?.addEventListener("input", paint);
  view?.addEventListener("change", () => {
    const value = view.value;
    viewSet = null;
    if (value.startsWith("credential:")) {
      viewSet = new Set(program.credentials.find((c) => c.id === value.slice(11)).closure);
    } else if (value.startsWith("track:")) {
      viewSet = new Set(program.tracks.find((t) => t.id === value.slice(6)).closure);
    } else if (value.startsWith("tier:")) {
      viewSet = new Set(Object.values(modules).filter((m) => m.tier === value.slice(5)).map((m) => m.id));
    }
    paint();
  });
  paint();
}
