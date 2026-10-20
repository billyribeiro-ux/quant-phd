// L02 figures, computed live: how the family-wise error rate of unadjusted tests grows with
// the family, Holm's step-down on Harvey, Liu and Zhu's ten-test example (the data of Lab 2),
// and the power a fixed effect loses as the family grows (Example 4.2).

import { drawAll, mountFigure, plot } from "../../../assets/js/chart.js";
import { bonferroni, holm } from "../../../assets/js/multitest.js";
import { logIntegers, normCdf, normPpf, normSf } from "../../../assets/js/stats.js";

function fwerGrowth(el) {
  mountFigure(el, {
    controls: [{ type: "range", key: "alpha", label: "Per-family level α", min: 0.01, max: 0.1, step: 0.01, value: 0.05, format: (v) => v.toFixed(2) }],
    draw(area, s, width) {
      const ms = logIntegers(1, 1000);
      const naive = (m) => 1 - Math.pow(1 - s.alpha, m);
      const bonf = (m) => 1 - Math.pow(1 - s.alpha / m, m);
      const half = Math.ceil(Math.log(0.5) / Math.log(1 - s.alpha));
      plot(area, {
        width,
        title: "Family-wise error rate of m independent true-null tests",
        desc:
          `Against the number of true nulls m on a log scale from 1 to 1,000: testing each at α = ${s.alpha.toFixed(2)} gives a family-wise error ` +
          `rate 1 − (1 − α)^m that passes one half at m = ${half} and approaches 1; the Bonferroni correction holds it at or just below α for every m (exactly α at m = 1).`,
        x: { label: "Number of true null hypotheses m (log scale)", log: true, domain: [1, 1000], format: "~s" },
        y: { label: "Probability of at least one false rejection", domain: [0, 1], format: ".1f" },
        layers: [
          { type: "line", name: "Each test at α (unadjusted)", points: ms.map((m) => [m, naive(m)]), series: 1 },
          { type: "line", name: "Bonferroni, each test at α/m", points: ms.map((m) => [m, bonf(m)]), series: 0 },
          { type: "rule", y: s.alpha, label: `α = ${s.alpha.toFixed(2)}` },
        ],
      });
      return `α = ${s.alpha.toFixed(2)}: unadjusted testing makes a false rejection more likely than not from m = ${half} true nulls (${naive(20).toFixed(3)} at m = 20); Bonferroni stays at or below α: ${s.alpha.toFixed(2)} at m = 1, falling to ${bonf(1000).toPrecision(3)} at m = 1,000.`;
    },
  });
}

// Harvey, Liu and Zhu's hypothetical ten-test example (Table 4, panel A, p. 18), as in Lab 2.
const T_STATS = [1.99, 2.63, 2.21, 3.43, 2.17, 2.64, 4.56, 5.34, 2.75, 2.49];
const REPORTED_P = [4.66, 0.85, 2.71, 0.05, 3.0, 0.84, 0.0, 0.0, 0.6, 1.28].map((v) => v / 100);
const RECOMPUTED_P = T_STATS.map((t) => 2 * normSf(t));

function holmStaircase(el) {
  mountFigure(el, {
    controls: [
      {
        type: "select",
        key: "source",
        label: "p-values",
        options: [
          ["reported", "as published (two decimals, in %)"],
          ["recomputed", "recomputed from the t-statistics"],
        ],
        value: "reported",
      },
    ],
    draw(area, s, width) {
      const alpha = 0.05;
      const p = s.source === "reported" ? REPORTED_P : RECOMPUTED_P;
      const m = p.length;
      const h = holm(p, alpha);
      const b = bonferroni(p, alpha);
      const pct = (v) => 100 * v;
      const sorted = h.order.map((i, j) => ({ rank: j + 1, test: i + 1, p: p[i], rejected: h.mask[i] }));
      const holmTests = sorted.filter((d) => d.rejected).map((d) => d.test).sort((u, v) => u - v);
      const bonfTests = b.map((r, i) => (r ? i + 1 : 0)).filter(Boolean);
      plot(area, {
        width,
        // Taller than the default on phones, so every rank label fits directly above or below its own dot.
        height: Math.round(Math.min(420, Math.max(290, width * 0.58))),
        title: "Holm's step-down on Harvey, Liu and Zhu's ten tests",
        desc:
          `The ten p-values sorted from smallest to largest, ${s.source === "reported" ? "as published to two decimals" : "recomputed from the published t-statistics"}, ` +
          `against Holm's rising thresholds α/(m + 1 − k) and the flat Bonferroni threshold α/m at α = 5%. Holm rejects tests ${holmTests.join(", ")}; ` +
          `Bonferroni rejects tests ${bonfTests.join(", ")}.`,
        x: { label: "Rank k of the sorted p-value", domain: [0.4, m + 0.6], ticks: m, format: "d" },
        y: { label: "p-value (%)", domain: [0, 5.2], format: ".1f" },
        layers: [
          { type: "segments", name: "Holm threshold α/(m+1−k)", segments: h.thresholds.map((t, j) => [j + 0.6, pct(t), j + 1.4, pct(t)]), series: 1 },
          { type: "line", name: "Bonferroni α/m", points: [[0.4, pct(alpha / m)], [m + 0.6, pct(alpha / m)]], series: 5, dash: 2 },
          { type: "dots", name: "Rejected by Holm", points: sorted.filter((d) => d.rejected).map((d) => [d.rank, pct(d.p)]), series: 0, r: 4.6 },
          { type: "dots", name: "Not rejected", points: sorted.filter((d) => !d.rejected).map((d) => [d.rank, pct(d.p)]), series: 5, hollow: true, r: 4.6 },
          ...sorted.map((d) => ({
            type: "text",
            x: d.rank,
            y: pct(d.p),
            anchor: "middle",
            text: `#${d.test}`,
            // Above the dot unless a threshold runs through the label there; then below, diagonally above, or beside it.
            candidates: [
              { dx: 0, dy: -9 },
              { dx: 0, dy: 18 },
              { dx: 7, dy: -6, anchor: "start" },
              { dx: -7, dy: -6, anchor: "end" },
              { dx: 9, dy: 4, anchor: "start" },
              { dx: -9, dy: 4, anchor: "end" },
              { dx: 7, dy: 14, anchor: "start" },
              { dx: -7, dy: 14, anchor: "end" },
            ],
          })),
        ],
      });
      // Close-up of step five, where the decision turns on the second significant digit of test 6.
      const close = width < 520 ? 150 : 132;
      plot(area, {
        width,
        height: close,
        margin: { top: 10, bottom: 40, left: 60 },
        legend: false,
        title: "Close-up of Holm's fifth step",
        desc: `Test 6's p-value as published, 0.84%, lies just above the fifth Holm threshold of 0.8333%; recomputed from its t-statistic it is 0.8291%, just below.`,
        x: { label: "p-value of test 6 (%) against the fifth threshold", domain: [0.82, 0.85], ticks: 6, format: ".3f" },
        y: { label: "", domain: [0, 1], ticks: 0 },
        layers: [
          { type: "rule", x: pct(alpha / (m + 1 - 5)), label: "threshold 0.8333", tone: "strong" },
          { type: "dots", points: [[0.84, 0.5]], series: s.source === "reported" ? 0 : 5, hollow: s.source !== "reported", r: 5 },
          { type: "dots", points: [[pct(RECOMPUTED_P[5]), 0.5]], series: s.source === "recomputed" ? 0 : 5, hollow: s.source !== "recomputed", r: 5 },
          { type: "text", x: 0.84, y: 0.5, dy: -10, anchor: "middle", text: "published" },
          { type: "text", x: pct(RECOMPUTED_P[5]), y: 0.5, dy: 18, anchor: "middle", text: "recomputed" },
        ],
      });
      return `Holm rejects tests ${holmTests.join(", ")}; Bonferroni rejects tests ${bonfTests.join(", ")}. Test 6: ${pct(p[5]).toFixed(4)}% against the fifth threshold ${pct(alpha / 6).toFixed(4)}%.`;
    },
  });
}

function powerFamily(el) {
  mountFigure(el, {
    controls: [{ type: "range", key: "mu", label: "Effect (mean of the z-statistic)", min: 1.5, max: 5, step: 0.1, value: 3.5, format: (v) => v.toFixed(1) }],
    draw(area, s, width) {
      const alpha = 0.05;
      const ms = logIntegers(1, 10000);
      const critical = (m) => normPpf(1 - alpha / (2 * m));
      // Two-sided power of a z-test centred at mu: both tails.
      const power = (m, mu) => normSf(critical(m) - mu) + normCdf(-critical(m) - mu);
      const marks = [1, 10, 100, 1000];
      plot(area, {
        width,
        title: "Power of a Bonferroni-corrected test as the family grows",
        desc:
          `Two-sided power at α = 5% of a z-test whose statistic is centred at ${s.mu.toFixed(1)}, against the family size m on a log scale. ` +
          `Power is ${marks.map((m) => `${power(m, s.mu).toFixed(3)} at m = ${m}`).join(", ")}.`,
        x: { label: "Family size m (log scale)", log: true, domain: [1, 10000], format: "~s" },
        y: { label: "Power", domain: [0, 1], format: ".1f" },
        layers: [
          { type: "line", name: `effect ${s.mu.toFixed(1)}`, points: ms.map((m) => [m, power(m, s.mu)]), series: 0 },
          { type: "dots", points: marks.map((m) => [m, power(m, s.mu)]), series: 0, r: 4 },
          // Named in the legend, and the four powers are in the readout: the curve crosses one half at a different
          // family size for every effect, so no fixed in-plot label stays clear of it.
          { type: "rule", y: 0.5, name: "coin flip (power 0.5)" },
        ],
      });
      return `Critical values ${marks.map((m) => critical(m).toFixed(3)).join(", ")} for m = 1, 10, 100, 1000; power ${marks.map((m) => power(m, s.mu).toFixed(3)).join(", ")}.`;
    },
  });
}

const FIGURES = { "fwer-growth": fwerGrowth, "holm-staircase": holmStaircase, "power-family": powerFamily };

export function drawFigures() {
  drawAll(FIGURES);
}
