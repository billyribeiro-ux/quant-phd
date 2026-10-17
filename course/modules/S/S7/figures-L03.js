// L03 figures, computed live: the geometry of the Benjamini–Hochberg step-up on the
// p-values of Example 2.2, and the p-value histogram behind the π0 estimate of Remark 6.1.

import { drawAll, mountFigure, plot } from "../../../assets/js/chart.js";
import { benjaminiHochberg, benjaminiYekutieli, bonferroni, holm } from "../../../assets/js/multitest.js";
import { histogram, normSf, rng } from "../../../assets/js/stats.js";

// Example 2.2: ten p-values, already sorted.
const EXAMPLE = [0.001, 0.008, 0.012, 0.021, 0.024, 0.046, 0.06, 0.074, 0.205, 0.212];

const count = (mask) => mask.filter(Boolean).length;

function bhGeometry(el) {
  mountFigure(el, {
    controls: [
      { type: "range", key: "q", label: "Level q", min: 0.01, max: 0.2, step: 0.005, value: 0.05, format: (v) => v.toFixed(3) },
      { type: "check", key: "fwer", label: "Holm and Bonferroni", value: true },
      { type: "check", key: "by", label: "Benjamini–Yekutieli", value: false },
    ],
    draw(area, s, width) {
      const m = EXAMPLE.length;
      const bh = benjaminiHochberg(EXAMPLE, s.q);
      const hm = holm(EXAMPLE, s.q);
      const bonf = count(bonferroni(EXAMPLE, s.q));
      const by = benjaminiYekutieli(EXAMPLE, s.q);
      const carried = EXAMPLE.map((p, i) => i + 1).filter((k) => k <= bh.kStar && EXAMPLE[k - 1] > bh.lines[k - 1]);
      const points = EXAMPLE.map((p, i) => [i + 1, p]);
      const layers = [
        { type: "line", name: "BH line k·q/m", points: [[0, 0], [m + 0.5, ((m + 0.5) * s.q) / m]], series: 0 },
        { type: "dots", name: "Rejected by BH", points: points.filter(([k]) => k <= bh.kStar), series: 0, r: 4.6 },
        { type: "dots", name: "Not rejected by BH", points: points.filter(([k]) => k > bh.kStar), series: 5, hollow: true, r: 4.6 },
      ];
      if (s.fwer) {
        layers.push({
          type: "segments",
          name: "Holm thresholds q/(m+1−k)",
          segments: hm.thresholds.map((t, j) => [j + 0.62, t, j + 1.38, t]),
          series: 1,
        });
        layers.push({ type: "line", name: "Bonferroni q/m", points: [[0, s.q / m], [m + 0.5, s.q / m]], series: 5, dash: 2 });
      }
      if (s.by) {
        layers.push({ type: "line", name: "BY line k·q/(m·c(m))", points: [[0, 0], [m + 0.5, ((m + 0.5) * s.q) / (m * by.c)]], series: 3, dash: 1 });
      }
      if (bh.kStar > 0) layers.push({ type: "rule", x: bh.kStar + 0.5, label: `k* = ${bh.kStar}` });
      const yTop = Math.max(0.24, s.q * 1.08);
      plot(area, {
        width,
        title: "The Benjamini–Hochberg step-up on the ten p-values of Example 2.2",
        desc:
          `The ten sorted p-values of Example 2.2 plotted against their rank k, with the BH line k·q/m at q = ${s.q.toFixed(3)}. ` +
          `The largest rank whose p-value lies on or under the line is k* = ${bh.kStar}, so BH rejects the ${bh.kStar} smallest p-values` +
          (carried.length ? `, including rank ${carried.join(" and ")}, which lies above its own line but is carried by the step-up. ` : ". ") +
          `Holm rejects ${count(hm.mask)} and Bonferroni ${bonf}.`,
        x: { label: "Rank k of the sorted p-value", domain: [0, m + 0.5], ticks: m, format: "d" },
        y: { label: "p-value", domain: [0, yTop], format: ".2f" },
        layers,
      });
      return (
        `q = ${s.q.toFixed(3)}: BH rejects ${bh.kStar} of ${m}` +
        (carried.length ? ` (rank ${carried.join(", ")} sits above its own line and is carried by the step-up)` : "") +
        `; Holm rejects ${count(hm.mask)}; Bonferroni rejects ${bonf}` +
        (s.by ? `; Benjamini–Yekutieli rejects ${by.kStar} (c(10) = ${by.c.toFixed(3)})` : "") +
        "."
      );
    },
  });
}

function pvalueHistogram(el) {
  const m = 1000;
  const m0 = 800;
  const effect = 3;
  let seed = 1;
  const sample = () => {
    const g = rng(seed);
    return Array.from({ length: m }, (_, i) => (i < m0 ? g.uniform() : normSf(effect + g.normal())));
  };
  let p = sample();
  mountFigure(el, {
    controls: [
      { type: "range", key: "lambda", label: "λ", min: 0.05, max: 0.95, step: 0.05, value: 0.5, format: (v) => v.toFixed(2) },
      {
        type: "button",
        label: "Draw a new sample",
        onClick: () => {
          seed += 1;
          p = sample();
        },
      },
    ],
    draw(area, s, width) {
      const bins = 20;
      const counts = histogram(p, 0, 1, bins);
      const density = counts.map((b) => ({ x0: b.x0, x1: b.x1, y: b.count / (m / bins) }));
      const above = p.filter((v) => v > s.lambda).length;
      const pi0hat = above / ((1 - s.lambda) * m);
      plot(area, {
        width,
        title: "Histogram of a thousand p-values, eight hundred of them from true nulls",
        desc:
          `A SIMULATED histogram of 1,000 one-sided p-values: 800 true nulls, uniform on (0, 1), and 200 effects of mean ${effect}, ` +
          `which pile up near zero. To the right of λ = ${s.lambda.toFixed(2)} the bars sit on a flat floor near the true share of nulls, 0.8; ` +
          `the estimate of π0 at λ, ${pi0hat.toFixed(3)}, is the height of that floor.`,
        x: { label: "p-value", domain: [0, 1], format: ".1f" },
        y: { label: "Density (1 = uniform)", domain: [0, Math.max(4, Math.ceil(Math.max(...density.map((b) => b.y))))], format: ".1f" },
        layers: [
          { type: "bars", name: "p-values (density)", bins: density, series: 4 },
          { type: "rule", y: m0 / m, label: "true π0 = 0.8", tone: "strong", labelAt: "left" },
          { type: "segments", name: "estimated π0(λ) = #{p > λ} / ((1 − λ) m)", segments: [[s.lambda, pi0hat, 1, pi0hat]], series: 1, dash: 1 },
          { type: "rule", x: s.lambda, label: `λ = ${s.lambda.toFixed(2)}` },
        ],
      });
      return `Sample ${seed}: ${above} of ${m} p-values exceed λ = ${s.lambda.toFixed(2)}, so the estimate is π0(λ) = ${above} / (${(1 - s.lambda).toFixed(2)} × ${m}) = ${pi0hat.toFixed(3)}, against the true π0 = 0.800.`;
    },
  });
}

const FIGURES = { "bh-geometry": bhGeometry, "pvalue-histogram": pvalueHistogram };

export function drawFigures() {
  drawAll(FIGURES);
}
