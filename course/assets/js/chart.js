// Chart and figure primitives over the vendored D3 v7 (BUILDER_RULES §6.3–6.5).
//
// * Charts are drawn at the container's real pixel width, so axis text stays at
//   its true size on a 360 px phone instead of shrinking with a fixed viewBox,
//   and they redraw when the container is resized.
// * Colours come only from CSS tokens through the .series-N classes, so every
//   chart follows the light and dark themes; series also differ by dash or
//   marker, so they stay distinguishable without colour and in print.
// * Every SVG carries <title> and <desc>. Interactive figures rewrite the
//   description and a live readout as their controls change.
// Pages that draw charts load d3.min.js.

const SERIES = 6;
let clipCount = 0;

function d3() {
  if (!window.d3) throw new Error("d3 is not loaded on this page");
  return window.d3;
}

/** Width available to a chart inside `container`, in CSS pixels. */
export function widthOf(container) {
  return Math.max(280, Math.floor(container.getBoundingClientRect().width || 640));
}

/** An <svg> of the given pixel size with its accessible name and description. */
export function svgFrame(parent, { width, height, title, desc }) {
  const svg = d3()
    .select(parent)
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", `0 0 ${width} ${height}`)
    .attr("role", "img");
  svg.append("title").text(title);
  svg.append("desc").text(desc);
  return svg;
}

function seriesClass(i) {
  return `series-${((i % SERIES) + SERIES) % SERIES}`;
}

function scale(axis, range, values) {
  const s = axis.log ? d3().scaleLog() : d3().scaleLinear();
  s.domain(axis.domain || d3().extent(values)).range(range);
  if (!axis.domain && axis.nice !== false && !axis.log) s.nice();
  return s;
}

function tickCount(pixels, axis) {
  return axis.ticks ?? Math.max(3, Math.min(10, Math.floor(pixels / 70)));
}

function layerValues(layer, which) {
  const i = which === "x" ? 0 : 1;
  switch (layer.type) {
    case "line":
    case "dots":
      return layer.points.map((p) => p[i]);
    case "area":
      return which === "x" ? layer.points.map((p) => p[0]) : layer.points.flatMap((p) => [p[1], p[2]]);
    case "bars":
      return which === "x" ? layer.bins.flatMap((b) => [b.x0, b.x1]) : layer.bins.flatMap((b) => [0, b.y]);
    case "segments":
      return layer.segments.flatMap((s) => (which === "x" ? [s[0], s[2]] : [s[1], s[3]]));
    case "rule":
      return which === "x" ? (layer.x !== undefined ? [layer.x] : []) : layer.y !== undefined ? [layer.y] : [];
    default:
      return [];
  }
}

function swatch(layer) {
  const cls = seriesClass(layer.series ?? 0);
  const body =
    layer.type === "dots" && layer.symbol === "triangle"
      ? `<path d="M14 1.5 L18.5 10 L9.5 10 Z" class="dot ${cls}${layer.hollow ? " hollow" : ""}"></path>`
      : layer.type === "dots"
      ? `<circle cx="14" cy="6" r="4" class="dot ${cls}${layer.hollow ? " hollow" : ""}"></circle>`
      : layer.type === "bars" || layer.type === "area"
        ? `<rect x="3" y="1" width="22" height="10" rx="2" class="${layer.type === "bars" ? "bar" : "area"} ${cls}"></rect>`
        : layer.type === "rule"
          ? `<g class="rule ${layer.tone ?? "muted"}"><line x1="1" x2="27" y1="6" y2="6"></line></g>`
          : `<line x1="1" x2="27" y1="6" y2="6" class="line ${cls}${layer.dash ? ` dash-${layer.dash}` : ""}"></line>`;
  return `<svg width="28" height="12" aria-hidden="true" focusable="false">${body}</svg>`;
}

/** An HTML legend (wraps at any width and never covers data). */
function legend(parent, layers) {
  const named = layers.filter((l) => l.name);
  if (named.length < 2) return;
  const list = document.createElement("ul");
  list.className = "chart-legend";
  for (const layer of named) {
    const item = document.createElement("li");
    item.innerHTML = swatch(layer);
    item.append(document.createTextNode(layer.name));
    list.append(item);
  }
  parent.append(list);
}

/**
 * Layered x–y plot drawn into `parent` (appended; callers clear it to redraw).
 *
 * spec = {title, desc, width, height?, x: Axis, y: Axis, layers: Layer[], legend?}
 * Axis = {label, domain?, log?, ticks?, format?, nice?}
 * Layer, by type:
 *   line     {points: [[x, y]], series, name?, dash?: 1|2, curve?: "step"}
 *   area     {points: [[x, y0, y1]], series, name?}
 *   dots     {points: [[x, y]], series, name?, hollow?, r?}
 *   bars     {bins: [{x0, x1, y}], series, name?}
 *   segments {segments: [[x1, y1, x2, y2]], series, dash?}
 *   rule     {x? | y?, label?, labelAt?: "left" | x-value, below?, row?, side?: "left" | "right", tone?, name?}
 *            A vertical rule's label goes at the top of the plot, in the first row (from `row`, default 0) and on
 *            the first side (from `side`, default right) where it stays inside the plot, clear of every other
 *            vertical rule and of the labels already placed; an automatic y domain gains headroom above the data
 *            for the rows used (layoutRuleLabels). A rule with a name is listed in the legend instead: use that
 *            for a horizontal rule a curve could cross in some state.
 *   text     {x, y, text, anchor?, dx?, dy?, tone?, candidates?: [{x?, y?, dx, dy, anchor?}]}
 *            With candidates, the text takes the first position (data x and y, default the layer's, plus pixel
 *            offsets) whose glyph box lies inside the plot and clear of every line, segment, rule, dot and bar and
 *            of the texts placed before it (the first if none is).
 */
export function plot(parent, spec) {
  const width = spec.width;
  const height = spec.height ?? Math.round(Math.min(420, Math.max(260, width * 0.58)));
  const margin = { top: 14, right: 18, bottom: 46, left: 60, ...spec.margin };
  if (spec.legend !== false) legend(parent, spec.layers);
  const xs = spec.layers.flatMap((l) => layerValues(l, "x"));
  const ys = spec.layers.flatMap((l) => layerValues(l, "y"));
  const svg = svgFrame(parent, { width, height, title: spec.title, desc: spec.desc });
  const yTicks = tickCount(height - margin.top - margin.bottom, { ticks: spec.y.ticks ?? 6 });
  let x, inner, placed, y;
  const layout = () => {
    x = scale(spec.x, [margin.left, width - margin.right], xs);
    inner = { w: width - margin.left - margin.right, h: height - margin.top - margin.bottom };
    placed = layoutRuleLabels(svg, spec.layers, x, margin, width);
    y = scale(spec.y, [height - margin.bottom, margin.top], withHeadroom(spec.y, ys, inner.h, placed.band));
  };
  layout();
  // The left margin holds the y tick labels and the rotated y-axis label: widen it to the widest tick label as
  // rendered, so no font or locale can push them into each other (Y_LABEL_BAND is the label's glyph band).
  const needed = Math.ceil(widestTick(svg, y, yTicks, spec.y.format) + TICK_OFFSET + Y_LABEL_BAND);
  if (needed > margin.left) {
    margin.left = needed;
    layout();
  }

  const xTicks = tickCount(inner.w, spec.x);
  svg
    .append("g")
    .attr("class", "grid")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3().axisLeft(y).ticks(yTicks).tickSize(-inner.w).tickFormat(""))
    .call((g) => g.select(".domain").remove());
  svg
    .append("g")
    .attr("class", "axis")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3().axisBottom(x).ticks(xTicks, spec.x.format));
  svg
    .append("g")
    .attr("class", "axis")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3().axisLeft(y).ticks(yTicks, spec.y.format));
  fitLabel(
    svg
      .append("text")
      .attr("class", "axis-label")
      .attr("x", margin.left + inner.w / 2)
      .attr("y", height - 8)
      .attr("text-anchor", "middle")
      .text(spec.x.label),
    centredRoom(margin.left + inner.w / 2, width),
  );
  fitLabel(
    svg
      .append("text")
      .attr("class", "axis-label")
      .attr("transform", `translate(14,${margin.top + inner.h / 2}) rotate(-90)`)
      .attr("text-anchor", "middle")
      .text(spec.y.label),
    centredRoom(margin.top + inner.h / 2, height),
  );

  const plotArea = svg.append("g").attr("class", "plot");
  clipCount += 1;
  const clip = `chart-clip-${clipCount}`;
  svg
    .append("clipPath")
    .attr("id", clip)
    .append("rect")
    .attr("x", margin.left)
    .attr("y", margin.top - 4)
    .attr("width", inner.w)
    .attr("height", inner.h + 8);
  plotArea.attr("clip-path", `url(#${clip})`);
  // The exact plot area (the clip adds 4 px above and below so markers on the edge stay whole): the figure
  // sweep checks plotted segments against it.
  plotArea.attr("data-area", [margin.left, margin.top, inner.w, inner.h].join(" "));

  let obstacles = null;
  for (const layer of spec.layers) {
    const cls = seriesClass(layer.series ?? 0);
    if (layer.type === "line") {
      const line = d3()
        .line()
        .defined((p) => Number.isFinite(p[1]))
        .x((p) => x(p[0]))
        .y((p) => y(p[1]));
      if (layer.curve === "step") line.curve(d3().curveStepAfter);
      plotArea
        .append("path")
        .datum(layer.points)
        .attr("class", `line ${cls}${layer.dash ? ` dash-${layer.dash}` : ""}`)
        .attr("d", line);
    } else if (layer.type === "area") {
      const area = d3()
        .area()
        .x((p) => x(p[0]))
        .y0((p) => y(p[1]))
        .y1((p) => y(p[2]));
      plotArea.append("path").datum(layer.points).attr("class", `area ${cls}`).attr("d", area);
    } else if (layer.type === "dots" && layer.symbol) {
      const size = Math.PI * (layer.r ?? 4) ** 2 * 1.3;
      const type = { triangle: d3().symbolTriangle, diamond: d3().symbolDiamond, square: d3().symbolSquare }[layer.symbol];
      plotArea
        .append("g")
        .selectAll("path")
        .data(layer.points)
        .join("path")
        .attr("class", `dot ${cls}${layer.hollow ? " hollow" : ""}`)
        .attr("transform", (p) => `translate(${x(p[0])},${y(p[1])})`)
        .attr("d", d3().symbol().type(type).size(size)());
    } else if (layer.type === "dots") {
      plotArea
        .append("g")
        .selectAll("circle")
        .data(layer.points)
        .join("circle")
        .attr("class", `dot ${cls}${layer.hollow ? " hollow" : ""}`)
        .attr("cx", (p) => x(p[0]))
        .attr("cy", (p) => y(p[1]))
        .attr("r", layer.r ?? 3.4);
    } else if (layer.type === "bars") {
      plotArea
        .append("g")
        .selectAll("rect")
        .data(layer.bins)
        .join("rect")
        .attr("class", (b) => `bar ${b.series === undefined ? cls : seriesClass(b.series)}`)
        .attr("x", (b) => x(b.x0) + 0.5)
        .attr("width", (b) => Math.max(0.5, x(b.x1) - x(b.x0) - 1))
        .attr("y", (b) => y(Math.max(0, b.y)))
        .attr("height", (b) => Math.abs(y(0) - y(b.y)));
    } else if (layer.type === "segments") {
      plotArea
        .append("g")
        .selectAll("line")
        .data(layer.segments)
        .join("line")
        .attr("class", `line ${cls}${layer.dash ? ` dash-${layer.dash}` : ""}`)
        .attr("x1", (s) => x(s[0]))
        .attr("y1", (s) => y(s[1]))
        .attr("x2", (s) => x(s[2]))
        .attr("y2", (s) => y(s[3]));
    } else if (layer.type === "rule") {
      const g = svg.append("g").attr("class", `rule ${layer.tone ?? "muted"}`);
      if (layer.x !== undefined) {
        g.append("line").attr("x1", x(layer.x)).attr("x2", x(layer.x)).attr("y1", margin.top).attr("y2", height - margin.bottom);
        if (layer.label) {
          const { row, side } = placed.at.get(layer);
          g.append("text")
            .attr("x", x(layer.x) + (side === "left" ? -LABEL_GAP : LABEL_GAP))
            .attr("y", margin.top + 11 + row * ROW_HEIGHT)
            .attr("text-anchor", side === "left" ? "end" : "start")
            .text(layer.label);
        }
      } else {
        g.append("line").attr("x1", margin.left).attr("x2", width - margin.right).attr("y1", y(layer.y)).attr("y2", y(layer.y));
        if (layer.label) {
          const at = typeof layer.labelAt === "number" ? x(layer.labelAt) : layer.labelAt === "left" ? margin.left + 5 : width - margin.right - 5;
          g.append("text")
            .attr("x", at)
            .attr("y", y(layer.y) + (layer.below ? 13 : -5))
            .attr("text-anchor", layer.labelAt === "left" ? "start" : typeof layer.labelAt === "number" ? "middle" : "end")
            .text(layer.label);
        }
      }
    } else if (layer.type === "text") {
      const node = svg.append("text").attr("class", `note ${layer.tone ?? ""}`).text(layer.text);
      const options = layer.candidates ?? [{ dx: layer.dx ?? 0, dy: layer.dy ?? 0, anchor: layer.anchor }];
      const length = node.node().getComputedTextLength?.() || layer.text.length * 6.2;
      const at = (o) => [x(o.x ?? layer.x) + o.dx, y(o.y ?? layer.y) + o.dy];
      const boxOf = (o) => {
        const [px, py] = at(o);
        const left = px - ((o.anchor ?? layer.anchor) === "middle" ? length / 2 : (o.anchor ?? layer.anchor) === "end" ? length : 0);
        return { l: left, r: left + length, t: py - 8.5, b: py + 2.5 };
      };
      obstacles ??= markObstacles(spec.layers, x, y, margin, width, height);
      const clear = (b) =>
        b.l >= margin.left && b.r <= width - margin.right && b.t >= margin.top && b.b <= height - margin.bottom && !obstacles.some((o) => o(b));
      const chosen = options.find((o) => clear(boxOf(o))) ?? options[0];
      const box = boxOf(chosen);
      obstacles.push((b) => b.l < box.r + 2 && b.r > box.l - 2 && b.t < box.b + 1 && b.b > box.t - 1);
      node
        .attr("x", at(chosen)[0])
        .attr("y", at(chosen)[1])
        .attr("text-anchor", chosen.anchor ?? layer.anchor ?? "start");
    }
  }
  return { svg, x, y, width, height, margin };
}

/**
 * Tests `(box) => boolean` for whether a glyph box meets a plotted mark: each line or segment (sampled every pixel),
 * each rule across the plot, and each dot and bar by its bounding box.
 */
function markObstacles(layers, x, y, margin, width, height) {
  const tests = [];
  const meetsPath = (pts) => (b) => {
    for (let i = 1; i < pts.length; i += 1) {
      const [x1, y1] = pts[i - 1];
      const [x2, y2] = pts[i];
      if (!(Number.isFinite(y1) && Number.isFinite(y2))) continue;
      const n = Math.max(1, Math.ceil(Math.hypot(x2 - x1, y2 - y1)));
      for (let k = 0; k <= n; k += 1) {
        const px = x1 + ((x2 - x1) * k) / n;
        const py = y1 + ((y2 - y1) * k) / n;
        if (px >= b.l && px <= b.r && py >= b.t && py <= b.b) return true;
      }
    }
    return false;
  };
  const meetsBox = (m) => (b) => b.l < m.r && b.r > m.l && b.t < m.b && b.b > m.t;
  for (const layer of layers) {
    if (layer.type === "line") tests.push(meetsPath(layer.points.map((p) => [x(p[0]), y(p[1])])));
    else if (layer.type === "segments") for (const sg of layer.segments) tests.push(meetsPath([[x(sg[0]), y(sg[1])], [x(sg[2]), y(sg[3])]]));
    else if (layer.type === "rule" && layer.x !== undefined) tests.push(meetsPath([[x(layer.x), margin.top], [x(layer.x), height - margin.bottom]]));
    else if (layer.type === "rule") tests.push(meetsPath([[margin.left, y(layer.y)], [width - margin.right, y(layer.y)]]));
    else if (layer.type === "dots") {
      const r = (layer.r ?? 3.5) + 1;
      for (const [px, py] of layer.points) tests.push(meetsBox({ l: x(px) - r, r: x(px) + r, t: y(py) - r, b: y(py) + r }));
    } else if (layer.type === "bars") {
      for (const bin of layer.bins) tests.push(meetsBox({ l: x(bin.x0), r: x(bin.x1), t: Math.min(y(0), y(bin.y)), b: Math.max(y(0), y(bin.y)) }));
    }
  }
  return tests;
}

/**
 * Mount a figure in its [data-chart] container: optional controls, a drawing area and a live
 * readout. `draw(area, state, width)` renders into the cleared area and returns the readout
 * text (or nothing). The figure redraws when a control changes or the width changes.
 *
 * controls: [{type: "range", key, label, min, max, step, value, format?},
 *            {type: "select", key, label, options: [[value, text]], value},
 *            {type: "check", key, label, value},
 *            {type: "button", label, onClick(state)}]
 */
export function mountFigure(container, { controls = [], draw }) {
  container.replaceChildren();
  const state = {};
  let panel = null;
  if (controls.length) {
    panel = document.createElement("div");
    panel.className = "figure-controls";
    container.append(panel);
  }
  const area = document.createElement("div");
  area.className = "chart-area";
  container.append(area);
  const readout = document.createElement("p");
  readout.className = "figure-readout";
  readout.setAttribute("aria-live", "polite");

  let lastWidth = 0;
  const render = () => {
    const width = widthOf(container);
    lastWidth = width;
    area.replaceChildren();
    const text = draw(area, state, width);
    readout.textContent = text || "";
    readout.hidden = !text;
  };

  for (const c of controls) {
    if (c.type === "button") {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "button small";
      button.textContent = c.label;
      button.addEventListener("click", () => {
        c.onClick(state);
        render();
      });
      panel.append(button);
      continue;
    }
    const label = document.createElement("label");
    const name = document.createElement("span");
    name.className = "control-name";
    name.textContent = c.label;
    label.append(name);
    state[c.key] = c.value;
    if (c.type === "range") {
      const input = document.createElement("input");
      Object.assign(input, { type: "range", min: c.min, max: c.max, step: c.step, value: c.value });
      const output = document.createElement("output");
      const show = () => (output.textContent = c.format ? c.format(state[c.key]) : String(state[c.key]));
      show();
      input.addEventListener("input", () => {
        state[c.key] = Number(input.value);
        show();
        render();
      });
      label.append(input, output);
    } else if (c.type === "select") {
      const select = document.createElement("select");
      for (const [value, text] of c.options) select.append(new Option(text, String(value), false, value === c.value));
      select.addEventListener("change", () => {
        const match = c.options.find(([value]) => String(value) === select.value);
        state[c.key] = match ? match[0] : select.value;
        render();
      });
      label.append(select);
    } else if (c.type === "check") {
      const box = document.createElement("input");
      Object.assign(box, { type: "checkbox", checked: Boolean(c.value) });
      box.addEventListener("change", () => {
        state[c.key] = box.checked;
        render();
      });
      label.classList.add("check");
      label.prepend(box);
    }
    panel.append(label);
  }
  container.append(readout);
  render();
  if (typeof ResizeObserver !== "undefined") {
    let pending = false;
    new ResizeObserver(() => {
      if (pending) return;
      pending = true;
      requestAnimationFrame(() => {
        pending = false;
        if (Math.abs(widthOf(container) - lastWidth) > 1) render();
      });
    }).observe(container);
  }
  return { state, render };
}

/** Wire a module's FIGURES map to every [data-chart] element on the page. */
export function drawAll(figures) {
  for (const el of document.querySelectorAll("[data-chart]")) {
    const make = figures[el.dataset.chart];
    if (!make) throw new Error(`unknown figure ${el.dataset.chart}`);
    make(el);
  }
}

/** Line chart (static). spec = {series: [{name, points}], xLabel, yLabel, title, desc, xLog?, xDomain?, yDomain?, xFormat?, yFormat?} */
export function lineChart(container, spec) {
  return mountFigure(container, {
    draw: (area, _state, width) => {
      plot(area, {
        width,
        title: spec.title,
        desc: spec.desc,
        x: { label: spec.xLabel, log: spec.xLog, domain: spec.xDomain, format: spec.xFormat },
        y: { label: spec.yLabel, domain: spec.yDomain, format: spec.yFormat },
        layers: spec.series.map((s, i) => ({ type: "line", name: s.name, points: s.points, series: i, dash: i ? ((i - 1) % 2) + 1 : 0 })),
      });
    },
  });
}

/** Scatter chart (static). spec as lineChart; optional zeroLines draws x = 0 and y = 0. */
export function scatterChart(container, spec) {
  return mountFigure(container, {
    draw: (area, _state, width) => {
      const layers = spec.series.map((s, i) => ({ type: "dots", name: s.name, points: s.points, series: i, r: 2.6 }));
      if (spec.zeroLines) layers.push({ type: "rule", x: 0 }, { type: "rule", y: 0 });
      plot(area, {
        width,
        title: spec.title,
        desc: spec.desc,
        x: { label: spec.xLabel, domain: spec.xDomain, format: spec.xFormat },
        y: { label: spec.yLabel, domain: spec.yDomain, format: spec.yFormat },
        layers,
      });
    },
  });
}

const TICK_OFFSET = 9; // d3 tick length 6 plus padding 3
const Y_LABEL_BAND = 25; // the rotated y label's glyphs span x = 5..17, plus 8 px clear of the tick labels

/** Width of the widest tick label the y axis will draw, measured as rendered in an axis group. */
function widestTick(svg, y, count, format) {
  const ticks = count ? y.ticks(count) : [];
  if (!ticks.length) return 0;
  const fmt = y.tickFormat(count, format);
  const probe = svg.append("g").attr("class", "axis").append("text");
  let widest = 0;
  for (const t of ticks) {
    probe.text(fmt(t));
    const node = probe.node();
    widest = Math.max(widest, (typeof node.getComputedTextLength === "function" ? node.getComputedTextLength() : 0) || String(fmt(t)).length * 6.6);
  }
  probe.node().parentNode.remove();
  return widest;
}

const LABEL_GAP = 5;
const ROW_HEIGHT = 14;
const MAX_ROWS = 4;

/**
 * Rows and sides for the labels of vertical rules (see plot). Measures each label as rendered, then takes the first
 * row and side where the label lies inside the plot, at least 3 px from every other vertical rule, and at least 6 px
 * from every label already in that row. Returns the placements and the height `band` of the label rows below the top
 * of the plot (0 without labels).
 */
function layoutRuleLabels(svg, layers, x, margin, width) {
  const rules = layers.filter((l) => l.type === "rule" && l.x !== undefined && l.label);
  const lines = layers.filter((l) => l.type === "rule" && l.x !== undefined).map((l) => x(l.x));
  const probe = svg.append("g").attr("class", "rule").append("text");
  const at = new Map();
  const rows = Array.from({ length: MAX_ROWS }, () => []);
  let used = -1;
  for (const rule of rules) {
    probe.text(rule.label);
    const node = probe.node();
    const w = (typeof node.getComputedTextLength === "function" ? node.getComputedTextLength() : 0) || rule.label.length * 6.2;
    const px = x(rule.x);
    const sides = rule.side === "left" ? ["left", "right"] : ["right", "left"];
    const boxOf = (side) => (side === "left" ? [px - LABEL_GAP - w, px - LABEL_GAP] : [px + LABEL_GAP, px + LABEL_GAP + w]);
    const fits = ([l, r], row) =>
      l >= margin.left + 2 &&
      r <= width - margin.right - 2 &&
      lines.every((v) => v === px || v < l - 3 || v > r + 3) &&
      rows[row].every(([a, b]) => r < a - 6 || l > b + 6);
    let choice = null;
    for (let row = rule.row ?? 0; row < MAX_ROWS && !choice; row += 1) {
      const side = sides.find((sd) => fits(boxOf(sd), row));
      if (side) choice = { row, side };
    }
    // Nowhere clear: the first row, on the side with more room.
    if (!choice) choice = { row: rule.row ?? 0, side: px + LABEL_GAP + w > width - margin.right ? "left" : "right" };
    rows[choice.row].push(boxOf(choice.side));
    at.set(rule, choice);
    used = Math.max(used, choice.row);
  }
  probe.node().parentNode.remove();
  return { at, band: used < 0 ? 0 : 11 + used * ROW_HEIGHT + 8 };
}

/**
 * The values an automatic y domain is fitted to, extended so the data stay `band` pixels below the top of a plot
 * `pixels` tall. An explicit domain is the caller's to choose and is left alone.
 */
function withHeadroom(axis, values, pixels, band) {
  if (axis.domain || axis.log || !band || !values.length) return values;
  const lo = Math.min(...values);
  const hi = Math.max(...values);
  return [...values, hi + ((hi - lo) * band) / Math.max(1, pixels - band)];
}

/** Width available to a label centred at `centre` on an axis of length `extent`, keeping 4px clear of each edge. */
function centredRoom(centre, extent) {
  return 2 * Math.min(centre, extent - centre) - 8;
}

const MIN_LABEL_PX = 8;

/**
 * Fit an axis label into `room` pixels so it never leaves the SVG: shrink its font, down to MIN_LABEL_PX, and if it
 * is still too long, cut it at a word with an ellipsis and keep the full text in a <title> child for hover and
 * screen readers. Measures the rendered length when the browser can (getComputedTextLength), else estimates it.
 */
function fitLabel(label, room) {
  const node = label.node();
  const measure = () => (typeof node.getComputedTextLength === "function" ? node.getComputedTextLength() : 0) || node.textContent.length * 6.6;
  const length = measure();
  if (length <= room || room <= 0) return;
  // Shrink to the largest tenth of a pixel that fits, rounding down, then step down until it does: the text's
  // rendered length is not exactly proportional to its size.
  let size = Math.max(MIN_LABEL_PX, Math.floor((120 * room) / length) / 10);
  label.style("font-size", `${size.toFixed(1)}px`);
  while (measure() > room && size > MIN_LABEL_PX) {
    size = Math.max(MIN_LABEL_PX, Math.round((size - 0.1) * 10) / 10);
    label.style("font-size", `${size.toFixed(1)}px`);
  }
  if (measure() <= room) return;
  const full = node.textContent;
  const words = full.split(" ");
  while (words.length > 1 && measure() > room) {
    words.pop();
    node.textContent = `${words.join(" ")}…`;
  }
  label.append("title").text(full);
}

/** Wrap `text` into lines of at most `chars` characters, breaking at spaces. */
export function wrapLines(text, chars) {
  const lines = [];
  let line = "";
  for (const word of text.split(" ")) {
    if (line && (line + " " + word).length > chars) {
      lines.push(line);
      line = word;
    } else {
      line = line ? `${line} ${word}` : word;
    }
  }
  if (line) lines.push(line);
  return lines;
}

/** Append multi-line text to an SVG selection at (x, y); returns the number of lines. */
export function multilineText(g, text, { x, y, chars, lineHeight = 14, cls = "", anchor = "start" }) {
  const lines = wrapLines(text, chars);
  const node = g.append("text").attr("class", cls).attr("text-anchor", anchor);
  lines.forEach((line, i) => node.append("tspan").attr("x", x).attr("y", y + i * lineHeight).text(line));
  return lines.length;
}
