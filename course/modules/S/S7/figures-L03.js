// L03 figures, computed live: the geometry of the Benjamini–Hochberg step-up on the
// p-values of Example 2.2, and the p-value histogram behind the π0 estimate of Remark 6.1.

import { drawAll, mountFigure, plot } from "../../../assets/js/chart.js";
import { benjaminiHochberg, benjaminiYekutieli, bonferroni, holm, storeyPi0, storeyPi0Moments } from "../../../assets/js/multitest.js";
import { histogram, normCdf, normPpf, normSf, rng } from "../../../assets/js/stats.js";

// Example 2.2: ten p-values, already sorted.
const EXAMPLE = [0.001, 0.008, 0.012, 0.021, 0.024, 0.046, 0.06, 0.074, 0.205, 0.212];

const count = (mask) => mask.filter(Boolean).length;

function bhGeometry(el) {
  mountFigure(el, {
    controls: [
      { type: "range", key: "q", label: "Level q", min: 0.01, max: 0.2, step: 0.005, value: 0.05, format: (v) => v.toFixed(3) },
      { type: "check", key: "fwer", label: "Holm and Bonferroni", value: true },
      { type: "check", key: "by", label: "Benjamini–Yekutieli (Section 5)", value: false },
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
        (s.by ? `; Benjamini–Yekutieli (Section 5) rejects ${by.kStar} (c(10) = ${by.c.toFixed(3)})` : "") +
        "."
      );
    },
  });
}

const M = 1000;
const M0 = 800;
const EFFECT = 3;

/** One SIMULATED set of p-values: M0 uniform true nulls and M − M0 one-sided z-tests with mean EFFECT. */
export function pvalueSample(seed) {
  const g = rng(seed);
  return Array.from({ length: M }, (_, i) => (i < M0 ? g.uniform() : normSf(EFFECT + g.normal())));
}

// The default, seed 22, is a median draw at λ = 0.5: its estimate there equals the median over seeds 1–200
// (tests/test_figure_kernels.py checks this). At other λ it is just one sample.
export const PVALUE_DEFAULT_SEED = 22;

/** Mean, leak and sd of the estimate π0(λ) for this design: an effect's p-value exceeds λ with probability Φ(Φ⁻¹(1 − λ) − EFFECT). */
export function pi0Moments(lambda) {
  return storeyPi0Moments(M0, M - M0, lambda, normCdf(normPpf(1 - lambda) - EFFECT));
}

function pvalueHistogram(el) {
  let seed = PVALUE_DEFAULT_SEED;
  let p = pvalueSample(seed);
  mountFigure(el, {
    controls: [
      { type: "range", key: "lambda", label: "λ", min: 0.05, max: 0.95, step: 0.05, value: 0.5, format: (v) => v.toFixed(2) },
      {
        type: "button",
        label: "Draw a new sample",
        onClick: () => {
          seed += 1;
          p = pvalueSample(seed);
        },
      },
    ],
    draw(area, s, width) {
      const bins = 20;
      const counts = histogram(p, 0, 1, bins);
      const density = counts.map((b) => ({ x0: b.x0, x1: b.x1, y: b.count / (M / bins) }));
      const above = p.filter((v) => v > s.lambda).length;
      const pi0hat = storeyPi0(p, s.lambda);
      const moments = pi0Moments(s.lambda);
      const leakDominates = moments.leak > moments.sd;
      plot(area, {
        width,
        title: "Histogram of a thousand p-values, eight hundred of them from true nulls",
        desc:
          `A SIMULATED histogram of 1,000 one-sided p-values: 800 true nulls, uniform on (0, 1), and 200 effects of mean ${EFFECT}, ` +
          `which pile up near zero. To the right of λ = ${s.lambda.toFixed(2)} the null p-values form a flat floor at the true share of nulls, 0.8, ` +
          `and the effects that land past λ add ${moments.leak.toFixed(4)} to it on average, ${leakDominates ? "more" : "less"} than the sampling noise (sd ${moments.sd.toFixed(4)}); ` +
          `the estimate of π0 at λ, ${pi0hat.toFixed(3)}, is the average height of the bars to the right of λ.`,
        x: { label: "p-value", domain: [0, 1], format: ".1f" },
        y: { label: "Density (1 = uniform)", domain: [0, Math.max(4, Math.ceil(Math.max(...density.map((b) => b.y))))], format: ".1f" },
        layers: [
          { type: "bars", name: "p-values (density)", bins: density, series: 4 },
          { type: "segments", name: "estimated π0(λ) = #{p > λ} / ((1 − λ) m)", segments: [[s.lambda, pi0hat, 1, pi0hat]], series: 1, dash: 1 },
          // Named in the legend: the bars scatter around this line, so any label on it would sit on them.
          { type: "rule", y: M0 / M, name: "true π0 = 0.8", tone: "strong" },
          { type: "rule", x: s.lambda, label: `λ = ${s.lambda.toFixed(2)}` },
        ],
      });
      return (
        `Sample ${seed}${seed === PVALUE_DEFAULT_SEED && Math.abs(s.lambda - 0.5) < 1e-9 ? " (a median draw at λ = 0.5)" : ""}: ${above} of ${M} p-values exceed λ = ${s.lambda.toFixed(2)}, ` +
        `so the estimate is π0(λ) = ${above} / (${(1 - s.lambda).toFixed(2)} × ${M}) = ${pi0hat.toFixed(3)}, against the true π0 = 0.800. ` +
        `At this λ the effects that land past it raise the estimate by ${moments.leak.toFixed(4)} on average, ` +
        `${leakDominates ? "more than" : "less than"} the sampling noise (sd ${moments.sd.toFixed(4)}).`
      );
    },
  });
}

const FIGURES = { "bh-geometry": bhGeometry, "pvalue-histogram": pvalueHistogram };

export function drawFigures() {
  drawAll(FIGURES);
}
