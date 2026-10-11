// Program map: renders the whole program from curriculum.json (generated and
// validated by tools/render_curriculum.py). Every number shown is computed
// there; this file only presents it.

import { fmt, h, loadJSON } from "./data.js";

const TIER_NAMES = { F: "Foundations", U: "Major", M: "Master's", D: "Doctoral" };
const GRADING = { autograder: "Autograded", rubric: "Rubric", both: "Autograded + rubric" };

function tierBadge(code) {
  return h("span", { class: `tier tier-${code}`, title: TIER_NAMES[code] }, code);
}

/** Search key: lowercase, accents stripped, every dash variant folded to "-" ("Black–Scholes" ≡ "black-scholes"). */
function searchKey(text) {
  return text
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[\u2010-\u2015\u2212]/g, "-")
    .toLowerCase();
}

function moduleIndex(curriculum) {
  const index = new Map();
  for (const part of curriculum.parts) for (const m of part.modules) index.set(m.id, { ...m, partTitle: part.title });
  return index;
}

function renderStats(curriculum, refCount) {
  const s = curriculum.stats;
  const tiles = [
    [fmt.format(s.modules), "modules across " + s.parts + " parts"],
    [fmt.format(s.projects), "graded projects"],
    [fmt.format(s.total_hours), "study hours (incl. projects)"],
    [s.full_time_years.toFixed(1), "full-time years, zero → thesis"],
    [fmt.format(refCount), "Crossref-verified references"],
  ];
  return tiles.map(([value, label]) =>
    h("li", { class: "stat" }, h("span", { class: "stat-value" }, value), h("span", { class: "stat-label" }, label)),
  );
}

function renderCredentials(curriculum, modules) {
  const statsById = new Map(curriculum.stats.credentials.map((c) => [c.id, c]));
  return curriculum.credentials.map((cred) => {
    const cs = statsById.get(cred.id);
    const rows = [];
    let group = null;
    for (const entry of cred.course_map) {
      if (entry.group !== group) {
        group = entry.group;
        rows.push(h("tr", { class: "group-row" }, h("th", { colspan: "3", scope: "colgroup" }, group)));
      }
      const hours = entry.modules.reduce((sum, id) => sum + modules.get(id).hours, 0);
      rows.push(
        h(
          "tr",
          {},
          h("td", {}, entry.course),
          h(
            "td",
            { class: "prereq-links" },
            entry.modules.map((id) => h("a", { href: `#mod-${id}`, title: modules.get(id).title }, id)),
          ),
          h("td", { class: "num" }, `${hours} h`),
        ),
      );
    }
    return h(
      "article",
      { class: "card", id: `cred-${cred.id}` },
      h("p", { class: "eyebrow" }, cred.level === "bachelor" ? "Bachelor's level" : cred.level === "master" ? "Master's level" : "Doctorate"),
      h("h3", {}, cred.name),
      h(
        "dl",
        { class: "card-metrics" },
        h("div", {}, h("dt", {}, "Modules"), h("dd", {}, cs.modules)),
        h("div", {}, h("dt", {}, "Projects"), h("dd", {}, cs.projects)),
        h("div", {}, h("dt", {}, "FTE years"), h("dd", {}, cs.full_time_years.toFixed(2))),
      ),
      h("p", {}, `${fmt.format(cs.hours)} hours ≈ ${cs.credit_equivalent} credits, prerequisites included.`),
      h(
        "details",
        { class: "disclosure" },
        h("summary", {}, `Course map (${cred.course_map.length} courses)`),
        h("table", { class: "course-map" }, h("tbody", {}, rows)),
      ),
    );
  });
}

function renderTracks(curriculum) {
  return h(
    "div",
    { class: "table-wrap" },
    h(
      "table",
      {},
      h(
        "thead",
        {},
        h("tr", {}, h("th", { scope: "col" }, "Track"), h("th", { scope: "col", class: "num" }, "Modules"),
          h("th", { scope: "col", class: "num" }, "Hours"), h("th", { scope: "col", class: "num" }, "FTE years")),
      ),
      h(
        "tbody",
        {},
        curriculum.stats.tracks.map((t) =>
          h(
            "tr",
            {},
            h("td", {}, t.name),
            h("td", { class: "num" }, t.modules),
            h("td", { class: "num" }, fmt.format(t.hours)),
            h("td", { class: "num" }, t.full_time_years.toFixed(2)),
          ),
        ),
      ),
    ),
  );
}

function renderModule(m) {
  const project = m.project;
  const tags = [tierBadge(m.tier), h("span", { class: "chip chip-muted" }, `${m.hours} h`)];
  if (project.atlas) tags.push(h("span", { class: "chip", title: "Atlas milestone" }, `⚑ ${project.atlas}`));
  if (m.debate) tags.push(h("span", { class: "chip", title: m.debate }, "⚖ debate"));
  const rows = [
    ["Core", m.core],
    ["Prerequisites", m.prereqs.length
      ? h("span", { class: "prereq-links" }, m.prereqs.map((id) => h("a", { href: `#mod-${id}` }, id)))
      : "None"],
    ["Project", h("span", {}, h("strong", {}, project.title), ` · ${GRADING[project.grading]}. ${project.brief}`)],
    ["Lab", m.lab],
    ["Debate", m.debate ?? null],
    ["Sources", `${m.sources.length} anchor source${m.sources.length === 1 ? "" : "s"}, each verified before citation`],
  ].filter(([, value]) => value !== null);
  return h(
    "li",
    { class: "module", id: `mod-${m.id}`, dataset: { tier: m.tier, id: m.id, search: searchKey(`${m.id} ${m.title} ${m.core} ${project.title}`) } },
    h(
      "details",
      {},
      h("summary", {}, h("span", { class: "module-id" }, m.id), h("span", { class: "module-title" }, m.title), h("span", { class: "module-tags" }, tags)),
      h("div", { class: "module-body" }, h("dl", {}, rows.flatMap(([label, value]) => [h("dt", {}, label), h("dd", {}, value)]))),
    ),
  );
}

function renderParts(curriculum) {
  return curriculum.parts.map((part) => {
    const hours = part.modules.reduce((sum, m) => sum + m.hours, 0);
    const children = [
      h(
        "div",
        { class: "part-head" },
        h("h3", { id: `part-${part.code}` }, `Part ${part.order} · ${part.title}`),
        h("span", { class: "meta" }, `${part.modules.length} modules · ${fmt.format(hours)} h`),
      ),
    ];
    if (part.studio) {
      const s = part.studio;
      children.push(
        h(
          "div",
          { class: "studio" },
          h("strong", {}, `Studio · ${s.title}`),
          ` · ${s.tier} · ${s.hours} h · ${GRADING[s.grading]}`,
          h("p", {}, s.brief),
        ),
      );
    }
    children.push(h("ol", { class: "modules" }, part.modules.map(renderModule)));
    return h("section", { class: "part", dataset: { part: part.code } }, children);
  });
}

function renderAtlas(curriculum, modules) {
  return curriculum.atlas.map((a) =>
    h(
      "li",
      {},
      h("span", { class: "atlas-id" }, `${a.id} · `, h("a", { href: `#mod-${a.module}` }, a.module)),
      h("strong", {}, a.title),
      h("p", {}, a.delivers),
    ),
  );
}

function renderCoverage(curriculum, modules) {
  return curriculum.bodies_of_knowledge.map((body) =>
    h(
      "div",
      { class: "table-wrap" },
      h(
        "table",
        {},
        h("caption", { class: "visually-hidden" }, body.name),
        h("thead", {}, h("tr", {}, h("th", { scope: "col" }, "Topic area"), h("th", { scope: "col" }, "Covered by"))),
        h(
          "tbody",
          {},
          body.topics.map((t) =>
            h(
              "tr",
              {},
              h("td", {}, t.topic),
              h("td", { class: "prereq-links" }, t.modules.map((id) => h("a", { href: `#mod-${id}`, title: modules.get(id).title }, id))),
            ),
          ),
        ),
      ),
    ),
  );
}

function wireFilters(curriculum) {
  const search = document.getElementById("filter-search");
  const credential = document.getElementById("filter-credential");
  const count = document.getElementById("filter-count");
  const toggles = [...document.querySelectorAll(".tier-toggles button")];
  const closures = new Map(curriculum.stats.credentials.map((c) => [c.id, new Set(c.closure)]));

  for (const cred of curriculum.credentials) credential.append(h("option", { value: cred.id }, cred.name));

  function apply() {
    const query = searchKey(search.value.trim());
    const tiers = new Set(toggles.filter((b) => b.getAttribute("aria-pressed") === "true").map((b) => b.dataset.tier));
    const closure = closures.get(credential.value);
    let shown = 0;
    for (const item of document.querySelectorAll(".module")) {
      const visible =
        (!query || item.dataset.search.includes(query)) &&
        tiers.has(item.dataset.tier) &&
        (!closure || closure.has(item.dataset.id));
      item.hidden = !visible;
      if (visible) shown += 1;
    }
    for (const part of document.querySelectorAll(".part")) {
      part.hidden = !part.querySelector(".module:not([hidden])");
    }
    count.textContent = `${shown} of ${curriculum.stats.modules} modules`;
  }

  search.addEventListener("input", apply);
  credential.addEventListener("change", apply);
  for (const button of toggles) {
    button.addEventListener("click", () => {
      button.setAttribute("aria-pressed", button.getAttribute("aria-pressed") === "true" ? "false" : "true");
      apply();
    });
  }
  apply();
}

function openTarget() {
  document.querySelectorAll(".module.is-target").forEach((el) => el.classList.remove("is-target"));
  const match = /^#mod-(.+)$/.exec(window.location.hash);
  if (!match) return;
  const target = document.getElementById(`mod-${match[1]}`);
  if (!target) return;
  target.hidden = false;
  target.closest(".part").hidden = false;
  target.classList.add("is-target");
  target.querySelector("details").open = true;
  target.scrollIntoView({ block: "center" });
}

export async function initProgramMap() {
  const [curriculum, references] = await Promise.all([loadJSON("curriculum.json"), loadJSON("references.json")]);
  const modules = moduleIndex(curriculum);
  document.getElementById("stats").replaceChildren(...renderStats(curriculum, references.count));
  document.getElementById("credentials").replaceChildren(...renderCredentials(curriculum, modules));
  document.getElementById("tracks").replaceChildren(renderTracks(curriculum));
  document.getElementById("parts").replaceChildren(...renderParts(curriculum));
  document.getElementById("atlas").replaceChildren(...renderAtlas(curriculum, modules));
  document.getElementById("coverage").replaceChildren(...renderCoverage(curriculum, modules));
  document.getElementById("generated").textContent =
    `Curriculum v${curriculum.program.version} (${curriculum.program.date}) · ${references.count} verified references.`;
  wireFilters(curriculum);
  window.addEventListener("hashchange", openTarget);
  openTarget();
  document.documentElement.dataset.mapReady = "true";
}

initProgramMap().catch((error) => console.error(error));
