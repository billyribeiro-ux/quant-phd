// L08 figure, computed live on SIMULATED configurations: combinatorially symmetric
// cross-validation (Definition 3.1) one split at a time, from the block assignment through the
// in-sample winner and its out-of-sample rank to the logit and the PBO estimate.

import { drawAll, mountFigure, multilineText, plot, svgFrame } from "../../../assets/js/chart.js";
import { cscv } from "../../../assets/js/multitest.js";
import { rng } from "../../../assets/js/stats.js";

const S = 8;
const BLOCK = 63;
const N = 10;
const VOL = 0.01;
const LETTERS = "ABCDEFGH";

/** A SIMULATED history: S·BLOCK days of N configurations, daily volatility VOL; configuration 1 gets a daily Sharpe ratio of 0.10 with an edge. */
export function simulate(seed, edge) {
  const g = rng(seed);
  return Array.from({ length: S * BLOCK }, () => Array.from({ length: N }, (_, n) => VOL * (g.normal() + (edge && n === 0 ? 0.1 : 0))));
}

function blockStrip(area, width, split) {
  const note = `Filled: in sample J (${S / 2} blocks). Outlined: out of sample J̄. ${BLOCK} days per block, in time order.`;
  const chars = Math.floor((width - 16) / 5.6);
  const lines = Math.ceil(note.length / chars);
  const height = 50 + 13 * lines;
  const left = 8;
  const w = (width - 2 * left) / S;
  const svg = svgFrame(area, {
    width,
    height,
    title: "Block assignment of this split",
    desc: `In-sample blocks ${split.inSample.map((b) => LETTERS[b]).join(", ")}; out-of-sample blocks ${split.outSample.map((b) => LETTERS[b]).join(", ")}.`,
  });
  const g = svg.append("g").attr("class", "series-0");
  for (let b = 0; b < S; b += 1) {
    const inside = split.inSample.includes(b);
    g.append("rect")
      .attr("class", inside ? "cell strong" : "cell")
      .attr("x", left + b * w + 2)
      .attr("y", 6)
      .attr("width", w - 4)
      .attr("height", 30)
      .attr("rx", 3);
    svg
      .append("text")
      .attr("class", inside ? "title-text" : "")
      .attr("x", left + (b + 0.5) * w)
      .attr("y", 26)
      .attr("text-anchor", "middle")
      .text(LETTERS[b]);
  }
  multilineText(svg, note, { x: left, y: 54, chars, lineHeight: 13, cls: "small" });
}

// Seed 501 is a median history in both states: with and without the edge its PBO is one of the two middle values
// over seeds 1–200 (the smallest such seed; tests/test_figure_kernels.py checks this). One history can land far
// from E[PBO] = 1/2 (Lab 2).
export const DEFAULT_CSCV_SEED = 501;

function cscvExplorer(el) {
  let seed = DEFAULT_CSCV_SEED;
  let cache = null;
  mountFigure(el, {
    controls: [
      { type: "range", key: "split", label: "Split", min: 1, max: 70, step: 1, value: 1, format: (v) => `${v} of 70` },
      { type: "check", key: "edge", label: "Give configuration 1 a true edge", value: false },
      { type: "button", label: "Simulate a new history", onClick: () => ((seed += 1), (cache = null)) },
    ],
    draw(area, s, width) {
      if (!cache || cache.edge !== s.edge) cache = { edge: s.edge, result: cscv(simulate(seed, s.edge), S) };
      const { result } = cache;
      const split = result.splits[s.split - 1];
      const annual = Math.sqrt(252);
      blockStrip(area, width, split);
      const side = width >= 600;
      const panel = side ? Math.floor((width - 16) / 2) : width;
      const row = document.createElement("div");
      row.className = "chart-row";
      area.append(row);
      const bars = (metric) =>
        metric.map((v, n) => ({ x0: n + 1 - 0.38, x1: n + 1 + 0.38, y: v * annual, series: n === split.best ? 1 : 0 }));
      const yMax = Math.max(1, ...split.isMetric.map((v) => Math.abs(v * annual)), ...split.oosMetric.map((v) => Math.abs(v * annual)));
      const yDomain = [-yMax * 1.1, yMax * 1.1];
      for (const [label, metric, note] of [
        ["In sample J", split.isMetric, `winner is configuration ${split.best + 1}`],
        ["Out of sample J̄", split.oosMetric, `winner ranks ${split.rank} of ${N} (${N} = best)`],
      ]) {
        const box = document.createElement("div");
        row.append(box);
        plot(box, {
          width: panel,
          height: 220,
          legend: false,
          title: `${label}: annualized Sharpe ratio by configuration`,
          desc: `Annualized Sharpe ratios of the ${N} configurations ${label.startsWith("In") ? "in sample" : "out of sample"}; configuration ${split.best + 1}, the in-sample winner, is highlighted: the ${note}.`,
          margin: { left: 48 },
          x: { label: `${label}: ${note}`, domain: [0.4, N + 0.6], ticks: N, format: "d" },
          y: { label: "Annualized Sharpe", domain: yDomain, format: ".1f" },
          layers: [
            { type: "bars", bins: bars(metric) },
            { type: "rule", y: 0 },
          ],
        });
      }
      // Right-closed bins (x0, x1], so a logit of exactly 0, which PBO counts as overfit, lands in a bin left of zero.
      const width0 = 0.25;
      const bins = Array.from({ length: 20 }, (_, i) => ({ x0: -2.5 + i * width0, x1: -2.5 + (i + 1) * width0, y: 0, series: i < 10 ? 1 : 0 }));
      for (const l of result.logits) bins[Math.min(19, Math.max(0, Math.ceil((l + 2.5) / width0) - 1))].y += 1;
      plot(area, {
        width,
        height: 200,
        title: "Logits of all 70 splits",
        desc: `Histogram of the 70 logits λ = ln(ω/(1 − ω)); the ${result.logits.filter((l) => l <= 0).length} at or below zero, where the in-sample winner lands at or below the out-of-sample median, give PBO = ${result.pbo.toFixed(3)}.`,
        x: { label: "Logit λ of the winner's OOS rank", domain: [-2.5, 2.5], format: ".1f" },
        y: { label: "Splits" },
        layers: [
          { type: "bars", name: "splits with λ ≤ 0 (counted by PBO)", bins: bins.slice(0, 10), series: 1 },
          { type: "bars", name: "splits with λ > 0", bins: bins.slice(10), series: 0 },
          { type: "rule", x: 0, name: "λ = 0: the winner ranks at the out-of-sample median", tone: "strong" },
          // Named in the legend and labelled with its value only: a short label always finds a side clear of λ = 0.
          { type: "rule", x: split.logit, name: "this split's logit", label: `λ = ${split.logit.toFixed(2)}` },
        ],
      });
      return (
        `${seed === DEFAULT_CSCV_SEED ? "A median history. " : ""}Split ${s.split}: in-sample blocks ${split.inSample.map((b) => LETTERS[b]).join("")}; winner configuration ${split.best + 1}; out-of-sample rank ${split.rank} of ${N}, ` +
        `ω = ${split.rank}/${N + 1} = ${split.omega.toFixed(3)}, λ = ${split.logit.toFixed(3)}. Over all 70 splits PBO = ${result.pbo.toFixed(3)}` +
        `${s.edge ? "" : ` (Theorem 4.1 gives E[PBO] = ${(Math.floor((N + 1) / 2) / N).toFixed(1)} when nothing works)`}.`
      );
    },
  });
}

const FIGURES = { "cscv-explorer": cscvExplorer };

export function drawFigures() {
  drawAll(FIGURES);
}
