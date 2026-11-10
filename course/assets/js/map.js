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

function escapeHtml(str) {
  return String(str || "").replace(/[&<>"']/g, (m) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[m]);
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

  // Initialize Resume Learning banner
  const banner = document.querySelector("[data-resume-banner]");
  if (banner) {
    try {
      const lastVisited = await store.getLastVisited();
      const progressEntries = await store.entries("progress");
      const completedSet = new Set(progressEntries.filter(([, v]) => v?.done).map(([k]) => k));
      const passedGraderSet = new Set((await store.entries("grader")).filter(([, v]) => v && v.all).map(([k]) => k));

      if (lastVisited && lastVisited.unit && modules[lastVisited.unit]) {
        const m = modules[lastVisited.unit];
        const part = program.parts.find((p) => p.modules.some((x) => x.id === m.id));
        const totalLessons = m.lessons || 8;
        const completedCount = [...completedSet].filter((k) => k.startsWith(`${m.id}/`)).length;
        const pct = Math.min(100, Math.round((completedCount / totalLessons) * 100));

        const pill = banner.querySelector(".resume-pill");
        if (pill) pill.textContent = "Resume Learning";
        const heading = banner.querySelector(".resume-heading");
        if (heading) heading.textContent = `Module ${m.id} · ${m.title}`;
        const sub = banner.querySelector(".resume-sub");
        if (sub) {
          const pageTitle = (lastVisited.title || "").replace(/^L\d+\s*·\s*/, "").split("·")[0].trim() || lastVisited.page;
          sub.innerHTML = `You were working on: <strong>${escapeHtml(lastVisited.page)}</strong> (${escapeHtml(pageTitle)})`;
        }

        const progContainer = banner.querySelector(".resume-progress-container");
        if (progContainer) {
          progContainer.removeAttribute("hidden");
          const fill = progContainer.querySelector(".resume-progress-fill");
          if (fill) fill.style.width = `${Math.max(pct, 6)}%`;
          const text = progContainer.querySelector(".resume-progress-text");
          if (text) text.textContent = `${completedCount} of ${totalLessons} lessons completed (${pct}%)`;
        }

        const btn = banner.querySelector(".resume-btn");
        if (btn) {
          btn.textContent = `Resume ${lastVisited.page} →`;
          btn.href = lastVisited.href || `modules/${part.code}/${m.id}/${lastVisited.page}.html`;
        }
      } else if (completedSet.size > 0) {
        const firstActive = Object.values(modules).find((m) => {
          const total = m.lessons || 8;
          const done = [...completedSet].filter((k) => k.startsWith(`${m.id}/`)).length;
          return done < total || !passedGraderSet.has(m.id);
        }) || modules["M1"];
        const part = program.parts.find((p) => p.modules.some((x) => x.id === firstActive.id));

        const pill = banner.querySelector(".resume-pill");
        if (pill) pill.textContent = "Next Recommended Module";
        const heading = banner.querySelector(".resume-heading");
        if (heading) heading.textContent = `Module ${firstActive.id} · ${firstActive.title}`;
        const sub = banner.querySelector(".resume-sub");
        if (sub) sub.textContent = firstActive.core;

        const btn = banner.querySelector(".resume-btn");
        if (btn) {
          btn.textContent = `Continue ${firstActive.id} →`;
          btn.href = `modules/${part.code}/${firstActive.id}/index.html`;
        }
      } else {
        const pill = banner.querySelector(".resume-pill");
        if (pill) pill.textContent = "Start Your Journey";
        const heading = banner.querySelector(".resume-heading");
        if (heading) heading.textContent = "Begin from Ground Zero";
        const sub = banner.querySelector(".resume-sub");
        if (sub) sub.textContent = "Start with orientation (P0.1) or dive straight into mathematical reasoning and calculus (M1).";
        const btn = banner.querySelector(".resume-btn");
        if (btn) {
          btn.textContent = "Start Module M1 →";
          btn.href = "modules/M/M1/index.html";
        }
      }
    } catch (err) {
      console.warn("resume banner error:", err);
    }
  }

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
