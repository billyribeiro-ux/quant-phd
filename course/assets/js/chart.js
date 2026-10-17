// Chart wrappers over the vendored D3 v7 (BUILDER_RULES §6.4). Every chart has
// labelled axes with units, a source line and a caption stating the one thing
// to see; colours come from CSS tokens via the .series-N classes, so charts
// follow the light and dark themes. Pages that draw charts load d3.min.js.

function d3() {
  if (!window.d3) throw new Error("d3 is not loaded on this page");
  return window.d3;
}

function frame(container, { width = 640, height = 360, title, desc }) {
  const svg = d3()
    .select(container)
    .append("svg")
    .attr("viewBox", `0 0 ${width} ${height}`)
    .attr("role", "img")
    .attr("preserveAspectRatio", "xMidYMid meet");
  svg.append("title").text(title);
  svg.append("desc").text(desc);
  return svg;
}

function axes(svg, x, y, { width, height, margin, xLabel, yLabel, xFormat, yFormat }) {
  const g = svg.append("g");
  g.append("g")
    .attr("class", "grid")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3().axisLeft(y).ticks(6).tickSize(-(width - margin.left - margin.right)).tickFormat(""))
    .call((sel) => sel.select(".domain").remove());
  g.append("g")
    .attr("class", "axis")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3().axisBottom(x).ticks(7, xFormat));
  g.append("g").attr("class", "axis").attr("transform", `translate(${margin.left},0)`).call(d3().axisLeft(y).ticks(6, yFormat));
  g.append("text")
    .attr("x", (margin.left + width - margin.right) / 2)
    .attr("y", height - 6)
    .attr("text-anchor", "middle")
    .text(xLabel);
  g.append("text")
    .attr("transform", `translate(14,${(margin.top + height - margin.bottom) / 2}) rotate(-90)`)
    .attr("text-anchor", "middle")
    .text(yLabel);
}

function legend(svg, series, { margin, position = "top-left" }) {
  // Top-left by default: most curves in this program rise to the right.
  const g = svg.append("g").attr("transform", `translate(${margin.left + 12},${margin.top + 8})`);
  const width = 12 + 34 + Math.max(...series.map((s) => s.name.length)) * 6.2;
  g.append("rect").attr("class", "legend-bg").attr("x", -6).attr("y", -10).attr("width", width).attr("height", series.length * 17 + 6).attr("rx", 4);
  series.forEach((s, i) => {
    const row = g.append("g").attr("transform", `translate(0,${i * 17})`);
    row.append("line").attr("x1", 0).attr("x2", 26).attr("y1", 0).attr("y2", 0).attr("class", `series-${i}`).attr("stroke-width", 2.5);
    row.append("text").attr("x", 34).attr("y", 4).attr("text-anchor", "start").text(s.name);
  });
  return position;
}

/**
 * Line chart. spec = {series: [{name, points: [[x, y], ...]}], xLabel, yLabel, title, desc,
 *                     xLog?, xDomain?, yDomain?, xFormat?, yFormat?}
 */
export function lineChart(container, spec) {
  const width = 640;
  const height = 360;
  const margin = { top: 16, right: 16, bottom: 46, left: 58 };
  const all = spec.series.flatMap((s) => s.points);
  const xScale = spec.xLog ? d3().scaleLog() : d3().scaleLinear();
  const x = xScale.domain(spec.xDomain || d3().extent(all, (p) => p[0])).range([margin.left, width - margin.right]);
  const y = d3()
    .scaleLinear()
    .domain(spec.yDomain || [Math.min(0, d3().min(all, (p) => p[1])), d3().max(all, (p) => p[1])])
    .nice()
    .range([height - margin.bottom, margin.top]);
  const svg = frame(container, { width, height, title: spec.title, desc: spec.desc });
  axes(svg, x, y, { width, height, margin, ...spec });
  const line = d3()
    .line()
    .x((p) => x(p[0]))
    .y((p) => y(p[1]));
  spec.series.forEach((s, i) => {
    svg.append("path").datum(s.points).attr("class", `series-${i}`).attr("fill", "none").attr("stroke-width", 2.5).attr("d", line);
  });
  if (spec.series.length > 1) legend(svg, spec.series, { margin });
  return svg.node();
}

/** Scatter chart. spec as lineChart; points are drawn as dots; optional diagonal y = x. */
export function scatterChart(container, spec) {
  const width = 640;
  const height = 380;
  const margin = { top: 16, right: 16, bottom: 46, left: 58 };
  const all = spec.series.flatMap((s) => s.points);
  const x = d3()
    .scaleLinear()
    .domain(spec.xDomain || d3().extent(all, (p) => p[0]))
    .nice()
    .range([margin.left, width - margin.right]);
  const y = d3()
    .scaleLinear()
    .domain(spec.yDomain || d3().extent(all, (p) => p[1]))
    .nice()
    .range([height - margin.bottom, margin.top]);
  const svg = frame(container, { width, height, title: spec.title, desc: spec.desc });
  axes(svg, x, y, { width, height, margin, ...spec });
  if (spec.zeroLines) {
    svg.append("line").attr("class", "axis").attr("x1", x(0)).attr("x2", x(0)).attr("y1", y.range()[0]).attr("y2", y.range()[1]).attr("stroke", "currentColor").attr("stroke-dasharray", "3 3").attr("opacity", 0.5);
    svg.append("line").attr("x1", x.range()[0]).attr("x2", x.range()[1]).attr("y1", y(0)).attr("y2", y(0)).attr("stroke", "currentColor").attr("stroke-dasharray", "3 3").attr("opacity", 0.5);
  }
  spec.series.forEach((s, i) => {
    svg
      .append("g")
      .selectAll("circle")
      .data(s.points)
      .join("circle")
      .attr("class", `series-${i}`)
      .attr("cx", (p) => x(p[0]))
      .attr("cy", (p) => y(p[1]))
      .attr("r", 2.6)
      .attr("fill-opacity", 0.55);
  });
  if (spec.series.length > 1) legend(svg, spec.series, { margin });
  return svg.node();
}
