// Injected into a page by tools/page_smoke.py to sweep live figures (course/assets/js/chart.js mountFigure).
// Defines window.__figureSweep with three functions of a [data-chart] element:
//   controls(chart)             the figure's controls, in document order, with their values
//   set(chart, index, value)    set one control and fire the event the figure listens for (a button is pressed)
//   collisions(chart)           every geometry problem of the chart in its current state

(() => {
  const CONTROLS = ".figure-controls input, .figure-controls select, .figure-controls button";
  const nameOf = (control) => control.closest("label").querySelector(".control-name").textContent;

  function controls(chart) {
    return [...chart.querySelectorAll(CONTROLS)].map((c) => {
      if (c.tagName === "BUTTON") return { kind: "button", label: c.textContent };
      if (c.tagName === "SELECT") return { kind: "select", label: nameOf(c), values: [...c.options].map((o) => o.value), value: c.value };
      if (c.type === "checkbox") return { kind: "check", label: nameOf(c), values: [false, true], value: c.checked };
      return { kind: "range", label: nameOf(c), min: Number(c.min), max: Number(c.max), step: Number(c.step), value: Number(c.value) };
    });
  }

  function set(chart, index, value) {
    const c = [...chart.querySelectorAll(CONTROLS)][index];
    if (c.tagName === "BUTTON") {
      c.click();
    } else if (c.type === "checkbox") {
      if (c.checked !== value) c.click();
    } else {
      c.value = String(value);
      c.dispatchEvent(new Event(c.tagName === "SELECT" ? "change" : "input"));
    }
  }

  // A text's glyph band is its line box less the space above the ascenders and below the descenders.
  function glyphs(node) {
    const r = node.getBoundingClientRect();
    return { l: r.left + 0.5, r: r.right - 0.5, t: r.top + 0.22 * r.height, b: r.bottom - 0.18 * r.height };
  }

  const meets = (a, b) => Math.min(a.r, b.r) - Math.max(a.l, b.l) > 0.5 && Math.min(a.b, b.b) - Math.max(a.t, b.t) > 0.5;
  const inside = (p, box) => p.x >= box.l && p.x <= box.r && p.y >= box.t && p.y <= box.b;

  /** Points along every plotted line, segment and rule, one per pixel of length, in client coordinates. */
  function markPoints(svg) {
    const points = [];
    for (const path of svg.querySelectorAll("path.line")) {
      const m = path.getScreenCTM();
      const length = path.getTotalLength();
      for (let s = 0; s <= length; s += 1) {
        const q = path.getPointAtLength(s);
        points.push(["line", new DOMPoint(q.x, q.y).matrixTransform(m)]);
      }
    }
    for (const line of svg.querySelectorAll("line.line, .rule line")) {
      const m = line.getScreenCTM();
      const [x1, y1, x2, y2] = ["x1", "y1", "x2", "y2"].map((a) => line[a].baseVal.value);
      const n = Math.max(2, Math.ceil(Math.hypot(x2 - x1, y2 - y1)));
      const kind = line.closest(".rule") ? "rule" : "segment";
      for (let k = 0; k <= n; k += 1) {
        points.push([kind, new DOMPoint(x1 + ((x2 - x1) * k) / n, y1 + ((y2 - y1) * k) / n).matrixTransform(m)]);
      }
    }
    return points;
  }

  function collisions(chart) {
    const problems = [];
    for (const svg of chart.querySelectorAll("svg[role='img']")) {
      const frame = svg.getBoundingClientRect();
      const texts = [...svg.querySelectorAll("text")].flatMap((t) => {
        const parts = t.querySelectorAll("tspan").length ? [...t.querySelectorAll("tspan")] : [t];
        return parts.filter((n) => n.textContent.trim()).map((n) => ({ text: JSON.stringify(n.textContent.trim()), box: glyphs(n), node: n }));
      });
      // fitLabel cuts an axis label only when it cannot fit at its smallest size; a cut label hides words, so it fails.
      for (const label of svg.querySelectorAll("text.axis-label")) {
        if (label.querySelector("title")) problems.push(`axis label ${JSON.stringify(label.querySelector("title").textContent)} is cut to fit`);
      }
      for (const t of texts) {
        if (t.node.closest("[clip-path]")) continue; // the clip hides what spills
        const r = t.node.getBoundingClientRect();
        if (r.left < frame.left - 1 || r.right > frame.right + 1 || r.top < frame.top - 1 || r.bottom > frame.bottom + 1) {
          problems.push(`text ${t.text} leaves its SVG`);
        }
      }
      for (let i = 0; i < texts.length; i += 1) {
        for (let j = i + 1; j < texts.length; j += 1) {
          if (meets(texts[i].box, texts[j].box)) problems.push(`texts ${texts[i].text} and ${texts[j].text} overlap`);
        }
      }
      // Every axis shows distinct tick labels: a repeated one means the format is coarser than the tick step.
      for (const axis of svg.querySelectorAll(".axis")) {
        const ticks = [...axis.querySelectorAll(".tick text")].map((t) => t.textContent.trim()).filter(Boolean);
        const repeated = ticks.filter((t, i) => ticks.indexOf(t) !== i);
        if (repeated.length) problems.push(`an axis repeats tick labels ${JSON.stringify([...new Set(repeated)])}`);
      }
      // A plotted segment drawn outside the plot area is clipped away: its data are not shown.
      const clip = svg.querySelector("clipPath rect");
      if (clip) {
        // A clipPath rect is never rendered (its client rect is empty): map its own attributes to the screen.
        const m = svg.getScreenCTM();
        const [x, y, w, h] = ["x", "y", "width", "height"].map((a) => clip[a].baseVal.value);
        const a = new DOMPoint(x, y).matrixTransform(m);
        const b = new DOMPoint(x + w, y + h).matrixTransform(m);
        const area = { left: Math.min(a.x, b.x), right: Math.max(a.x, b.x), top: Math.min(a.y, b.y), bottom: Math.max(a.y, b.y) };
        for (const line of svg.querySelectorAll(".plot line.line")) {
          const r = line.getBoundingClientRect();
          if (r.bottom < area.top - 0.5 || r.top > area.bottom + 0.5 || r.right < area.left - 0.5 || r.left > area.right + 0.5) {
            problems.push("a plotted segment lies outside the plot area");
          }
        }
      }
      const points = markPoints(svg);
      const boxes = [...svg.querySelectorAll(".plot .dot, .plot .bar")].map((n) => {
        const r = n.getBoundingClientRect();
        return [n.classList.contains("bar") ? "bar" : "dot", { l: r.left, r: r.right, t: r.top, b: r.bottom }];
      });
      for (const t of texts) {
        const hit = new Set();
        for (const [kind, p] of points) if (inside(p, t.box)) hit.add(kind);
        for (const [kind, b] of boxes) if (meets(t.box, b)) hit.add(kind);
        for (const kind of hit) problems.push(`a ${kind} crosses text ${t.text}`);
      }
    }
    return [...new Set(problems)];
  }

  window.__figureSweep = { controls, set, collisions };
})();
