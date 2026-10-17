// L05 figures, computed live on SIMULATED strategies: the Romano–Wolf StepM procedure step by
// step (Definitions 1.1–1.2), and why the bootstrap must resample whole dates (Section 4).

import { drawAll, mountFigure, plot } from "../../../assets/js/chart.js";
import { correlation, stationaryBootstrap, stepdown, studentizedBootstrap, upperCritical } from "../../../assets/js/multitest.js";
import { rng } from "../../../assets/js/stats.js";

/** B stationary-bootstrap draws: one index vector per draw (whole dates), or K per draw (each strategy apart). */
function bootstrapDraws(T, K, B, meanBlock, g, joint = true) {
  return Array.from({ length: B }, () =>
    joint ? stationaryBootstrap(T, meanBlock, g).indices : Array.from({ length: K }, () => stationaryBootstrap(T, meanBlock, g).indices),
  );
}

export function simulateUniverse(seed) {
  // 20 strategies, pairwise correlation 0.3 through a common factor, eight with a true alpha.
  const T = 250;
  const K = 20;
  const genuine = 8;
  const g = rng(seed);
  const d = Array.from({ length: T }, () => {
    const common = g.normal();
    return Array.from({ length: K }, (_, k) => Math.sqrt(0.3) * common + Math.sqrt(0.7) * g.normal() + (k < genuine ? 0.19 : 0));
  });
  return { d, genuine, K, T };
}

/** One simulated study: the universe, its studentized statistics and the StepM result at 5%. */
export function study(seed) {
  const u = simulateUniverse(seed);
  const { t, boot } = studentizedBootstrap(u.d, bootstrapDraws(u.T, u.K, 500, 5, rng(seed + 1000)));
  return { u, t, result: stepdown(t, boot, 0.05) };
}

// The default, seed 0, is a median study: across seeds 0–299 its single-step and StepM counts equal the medians
// (tests/test_figure_kernels.py checks this). A later step adds a rejection in a minority of studies; the second
// button draws new studies until one does and reports how many it drew.
export const DEFAULT_SEED = 0;

function stepmSteps(el) {
  let seed = DEFAULT_SEED;
  let cache = null;
  let searched = null;
  mountFigure(el, {
    controls: [
      { type: "button", label: "Simulate a new study", onClick: () => ((seed += 1), (cache = null), (searched = null)) },
      {
        type: "button",
        label: "Show a study where a later step rejects",
        onClick: () => {
          let draws = 0;
          do {
            seed += 1;
            draws += 1;
            cache = study(seed);
          } while (cache.result.mask.filter(Boolean).length === cache.result.steps[0].rejected.length && draws < 500);
          searched = draws;
        },
      },
    ],
    draw(area, _s, width) {
      if (!cache) cache = study(seed);
      const { u, t, result } = cache;
      const order = t.map((v, k) => [v, k]).sort((a, b) => b[0] - a[0]);
      const pos = new Map(order.map(([, k], i) => [k, i + 1]));
      const stepOf = new Map();
      result.steps.forEach((step, j) => step.rejected.forEach((k) => stepOf.set(k, j)));
      const layers = [];
      result.steps.forEach((step, j) => {
        const xs = step.active.map((k) => pos.get(k));
        layers.push({
          type: "segments",
          name: j === 0 ? "critical value at each step" : undefined,
          segments: [[Math.min(...xs) - 0.4, step.critical, Math.max(...xs) + 0.4, step.critical]],
          series: 1,
          dash: j === 0 ? 0 : 1,
        });
        // Later steps' labels stack below the line, so equal critical values stay legible.
        layers.push({ type: "text", x: u.K + 0.6, y: step.critical, dy: j === 0 ? -6 : 3 + 13 * j, anchor: "end", text: `step ${j + 1}: c = ${step.critical.toFixed(2)}` });
      });
      const dots = order.map(([v, k]) => [pos.get(k), v, k]);
      layers.push({ type: "dots", name: "rejected", points: dots.filter((p) => stepOf.has(p[2])), series: 0, r: 5 });
      layers.push({ type: "dots", name: "not rejected", points: dots.filter((p) => !stepOf.has(p[2])), series: 5, hollow: true, r: 5 });
      const floor = Math.min(-2.5, ...t) - 0.6;
      layers.push({
        type: "dots",
        name: "true alpha (known only in a simulation)",
        points: dots.filter((p) => p[2] < u.genuine).map((p) => [p[0], floor + 0.25]),
        series: 2,
        symbol: "triangle",
        r: 4,
      });
      const single = result.steps[0].rejected.length;
      const total = result.mask.filter(Boolean).length;
      const found = result.mask.filter((r, k) => r && k < u.genuine).length;
      const falseHits = total - found;
      const steps = result.steps.length;
      const fell = result.steps.some((st, j) => j > 0 && st.critical < result.steps[j - 1].critical);
      plot(area, {
        width,
        title: "The StepM procedure, step by step",
        desc:
          `Twenty SIMULATED strategies sorted by their studentized statistic, eight with a true alpha. The first step's critical value ` +
          `${result.steps[0].critical.toFixed(2)} is the single-step test and rejects ${single}. Each later step drops the rejected strategies ` +
          `and recomputes the critical value over the rest, which is never higher${fell ? " and here falls" : " and here stays the same"}; ` +
          `StepM rejects ${total} in ${steps} step${steps === 1 ? "" : "s"}.`,
        x: { label: "Strategy, sorted by t", domain: [0.3, u.K + 0.7], ticks: 10, format: "d" },
        y: { label: "Studentized statistic t", domain: [floor, Math.max(...t) + 0.8], format: ".0f" },
        layers,
      });
      return (
        `Study ${seed}${seed === DEFAULT_SEED ? " (a median study)" : ""}${searched ? `, found after drawing ${searched} new stud${searched === 1 ? "y" : "ies"}` : ""}: ` +
        result.steps.map((st, j) => `step ${j + 1}: c = ${st.critical.toFixed(3)} over ${st.active.length}, rejects ${st.rejected.length}`).join("; ") +
        `. Single-step rejects ${single}; StepM rejects ${total} (${found} of ${u.genuine} true alphas, ${falseHits} false)` +
        (total > single ? "; a later step added a rejection." : "; no later step added one.")
      );
    },
  });
}

function jointVsIndependent(el) {
  const T = 250;
  const rho = 0.8;
  const g = rng(77);
  const d = Array.from({ length: T }, () => {
    const c = g.normal();
    return Array.from({ length: 10 }, () => Math.sqrt(rho) * c + Math.sqrt(1 - rho) * g.normal());
  });
  const joint = studentizedBootstrap(d, bootstrapDraws(T, 10, 600, 5, rng(78), true), true);
  const indep = studentizedBootstrap(d, bootstrapDraws(T, 10, 600, 5, rng(79), false), false);
  const corr = (boot) => correlation(boot.map((r) => r[0]), boot.map((r) => r[1]));
  const crit = (boot) => upperCritical(boot.map((r) => Math.max(...r)), 0.05);
  mountFigure(el, {
    draw(area, _s, width) {
      plot(area, {
        width,
        title: "Bootstrap statistics of two correlated strategies: whole dates resampled versus each strategy resampled separately",
        desc:
          `Each dot is one bootstrap draw of the centred statistics of two of ten SIMULATED strategies whose returns have correlation ${rho}. ` +
          `Resampling whole dates keeps the correlation (${corr(joint.boot).toFixed(2)} across draws); resampling each strategy separately destroys it ` +
          `(${corr(indep.boot).toFixed(2)}), which inflates the 95% quantile of the maximum over the ten strategies from ${crit(joint.boot).toFixed(2)} to ${crit(indep.boot).toFixed(2)}.`,
        x: { label: "Bootstrap statistic of strategy 1", domain: [-4, 4], format: ".0f" },
        y: { label: "Bootstrap statistic of strategy 2", domain: [-4, 4], format: ".0f" },
        height: Math.min(440, Math.max(300, width * 0.75)),
        layers: [
          { type: "dots", name: "whole dates resampled (joint)", points: joint.boot.map((r) => [r[0], r[1]]), series: 0, r: 2.4 },
          { type: "dots", name: "each strategy resampled separately", points: indep.boot.map((r) => [r[0], r[1]]), series: 1, r: 2.4, hollow: true },
        ],
      });
      return `Correlation of the two bootstrap statistics: ${corr(joint.boot).toFixed(2)} joint, ${corr(indep.boot).toFixed(2)} separate. 95% critical value of the maximum over ten strategies: ${crit(joint.boot).toFixed(2)} joint, ${crit(indep.boot).toFixed(2)} separate.`;
    },
  });
}

const FIGURES = { "stepm-steps": stepmSteps, "joint-vs-independent": jointVsIndependent };

export function drawFigures() {
  drawAll(FIGURES);
}
