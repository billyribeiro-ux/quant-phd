// Global Spotlight search (Cmd+K). Allows learners to search across
// all 1,138 concepts, 134 modules, and registered notation macros from any page.

let dialog = null;
let cache = null;
let activeIndex = -1;

async function loadData(root) {
  if (cache) return cache;
  try {
    const [progRes, glossRes, notRes] = await Promise.all([
      fetch(`${root}assets/data/program.json`),
      fetch(`${root}assets/data/glossary.json`),
      fetch(`${root}assets/data/notation.json`),
    ]);
    const program = await progRes.json();
    const glossary = await glossRes.json();
    const notation = await notRes.json();

    const modules = program.parts.flatMap((p) =>
      p.modules.map((m) => ({
        type: "module",
        id: m.id,
        title: m.title,
        core: m.core || "",
        tier: m.tier,
        href: `${root}${m.href || `modules/${p.code}/${m.id}/index.html`}`,
      }))
    );

    const concepts = Object.entries(glossary).map(([id, c]) => ({
      type: "concept",
      id,
      title: c.name || c.term,
      sub: `Concept · introduced in ${c.module}`,
      href: `${root}${c.href || `concepts.html#def-${id}`}`,
    }));

    const macros = Object.entries(notation.macros || {}).map(([sym, m]) => ({
      type: "notation",
      id: sym,
      title: `${sym} (${m.meaning})`,
      sub: `Notation · ${m.tex}`,
      href: `${root}concepts.html#notation-conventions`,
    }));

    cache = { modules, concepts, macros };
    return cache;
  } catch (err) {
    console.warn("spotlight loadData:", err);
    return { modules: [], concepts: [], macros: [] };
  }
}

function escapeHtml(str) {
  return String(str || "").replace(/[&<>"']/g, (m) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[m]);
}

function createDialog(root) {
  if (dialog) return dialog;
  dialog = document.createElement("dialog");
  dialog.className = "spotlight-dialog";
  dialog.setAttribute("aria-label", "Search course concepts and modules");

  dialog.innerHTML = `
    <div class="spotlight-frame">
      <div class="spotlight-header">
        <span class="spotlight-icon" aria-hidden="true">🔍</span>
        <input type="search" class="spotlight-input" placeholder="Search concepts, modules, notation... (e.g. GMM, Ito, Sharpe, M2)" autofocus autocomplete="off" spellcheck="false">
        <kbd class="spotlight-esc" title="Close">esc</kbd>
      </div>
      <div class="spotlight-results" role="listbox">
        <p class="spotlight-hint">Type a concept, module code (e.g. M1, DV1), or topic name.</p>
      </div>
      <div class="spotlight-footer">
        <span><kbd>↑</kbd><kbd>↓</kbd> Navigate</span>
        <span><kbd>↵</kbd> Select</span>
        <span><kbd>esc</kbd> Close</span>
      </div>
    </div>
  `;

  document.body.append(dialog);

  const input = dialog.querySelector(".spotlight-input");
  const resultsContainer = dialog.querySelector(".spotlight-results");

  const close = () => {
    dialog.close();
    input.value = "";
    resultsContainer.innerHTML = `<p class="spotlight-hint">Type a concept, module code, or topic name.</p>`;
    activeIndex = -1;
  };

  dialog.addEventListener("click", (e) => {
    if (e.target === dialog) close();
  });

  dialog.querySelector(".spotlight-esc")?.addEventListener("click", close);

  const updateSelection = (items) => {
    items.forEach((item, idx) => {
      const isSelected = idx === activeIndex;
      item.classList.toggle("is-active", isSelected);
      item.setAttribute("aria-selected", String(isSelected));
      if (isSelected) item.scrollIntoView({ block: "nearest" });
    });
  };

  input.addEventListener("keydown", (e) => {
    const items = [...resultsContainer.querySelectorAll(".spotlight-item")];
    if (e.key === "Escape") {
      e.preventDefault();
      close();
    } else if (e.key === "ArrowDown") {
      e.preventDefault();
      if (!items.length) return;
      activeIndex = (activeIndex + 1) % items.length;
      updateSelection(items);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      if (!items.length) return;
      activeIndex = (activeIndex - 1 + items.length) % items.length;
      updateSelection(items);
    } else if (e.key === "Enter") {
      e.preventDefault();
      if (activeIndex >= 0 && items[activeIndex]) {
        items[activeIndex].click();
      } else if (items[0]) {
        items[0].click();
      }
    }
  });

  input.addEventListener("input", async () => {
    const q = input.value.trim().toLowerCase();
    activeIndex = -1;
    if (!q) {
      resultsContainer.innerHTML = `<p class="spotlight-hint">Type a concept, module code (e.g. M1, DV1), or topic name.</p>`;
      return;
    }

    const { modules, concepts, macros } = await loadData(root);

    const matchMod = modules
      .filter((m) => m.id.toLowerCase().includes(q) || m.title.toLowerCase().includes(q) || m.core.toLowerCase().includes(q))
      .slice(0, 5);

    const matchCon = concepts
      .filter((c) => c.title.toLowerCase().includes(q) || c.id.toLowerCase().includes(q))
      .slice(0, 10);

    const matchMac = macros
      .filter((m) => m.id.toLowerCase().includes(q) || m.title.toLowerCase().includes(q))
      .slice(0, 3);

    const allMatches = [...matchMod, ...matchCon, ...matchMac];

    if (!allMatches.length) {
      resultsContainer.innerHTML = `<p class="spotlight-empty">No matching concepts, modules, or notation found for "<strong>${escapeHtml(q)}</strong>".</p>`;
      return;
    }

    resultsContainer.innerHTML = "";
    allMatches.forEach((res, idx) => {
      const a = document.createElement("a");
      a.className = "spotlight-item";
      a.href = res.href;
      a.setAttribute("role", "option");
      a.dataset.index = String(idx);

      const icon = res.type === "module" ? "📘" : res.type === "concept" ? "💡" : "📐";
      const tag = res.type === "module" ? `Tier ${res.tier}` : res.type === "concept" ? "Concept" : "Notation";

      a.innerHTML = `
        <span class="spotlight-item-icon">${icon}</span>
        <div class="spotlight-item-text">
          <div class="spotlight-item-title">${escapeHtml(res.title)}</div>
          <div class="spotlight-item-sub">${escapeHtml(res.sub || res.core || "")}</div>
        </div>
        <span class="badge spotlight-item-badge">${tag}</span>
      `;

      a.addEventListener("click", () => {
        close();
      });

      resultsContainer.append(a);
    });

    if (allMatches.length) {
      activeIndex = 0;
      updateSelection([...resultsContainer.querySelectorAll(".spotlight-item")]);
    }
  });

  return dialog;
}

export function openSpotlight(root) {
  const dlg = createDialog(root);
  if (!dlg.open) {
    dlg.showModal();
    const input = dlg.querySelector(".spotlight-input");
    input.focus();
    input.select();
  }
}

export function initSpotlight(root) {
  document.addEventListener("keydown", (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      openSpotlight(root);
    } else if (e.key === "/" && !["INPUT", "TEXTAREA"].includes(document.activeElement?.tagName)) {
      e.preventDefault();
      openSpotlight(root);
    }
  });

  const headerActions = document.querySelector(".header-actions");
  if (headerActions && !headerActions.querySelector("[data-spotlight-btn]")) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "icon-button spotlight-btn";
    btn.setAttribute("data-spotlight-btn", "");
    btn.setAttribute("title", "Search concepts, notation, and modules (Cmd+K)");
    btn.innerHTML = `Search <kbd>⌘K</kbd>`;
    btn.addEventListener("click", () => openSpotlight(root));
    headerActions.prepend(btn);
  }
}
