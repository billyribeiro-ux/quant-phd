// L06 figures, computed live from the formulas on the page: the growth of the Bonferroni
// t-statistic hurdle (Definition 2.1, Theorem 2.3), the false-positive rate of reporting the
// best of K correlated analyses (Proposition 3.2), and the lower bound on the posterior
// probability of the null (Theorem 4.2).

import { drawAll, mountFigure, plot } from "../../../assets/js/chart.js";
import { linspace, logIntegers, normCdf, normPdf, normPpf, normSf, simpson } from "../../../assets/js/stats.js";

function hurdleGrowth(el) {
  mountFigure(el, {
    controls: [
      {
        type: "select",
        key: "alpha",
        label: "Level α",
        options: [
          [0.01, "1%"],
          [0.05, "5%"],
          [0.1, "10%"],
        ],
        value: 0.05,
      },
    ],
    draw(area, s, width) {
      const ms = logIntegers(1, 1e6, 12);
      const hurdle = (m) => normPpf(1 - s.alpha / (2 * m));
      // The smallest integer M whose hurdle reaches 3.0, solved exactly from α/(2M) ≤ 1 − Φ(3).
      const crossing = Math.ceil(s.alpha / (2 * normSf(3)));
      plot(area, {
        width,
        title: "The Bonferroni t-statistic hurdle as the number of tests grows",
        desc:
          `The exact Bonferroni hurdle Φ⁻¹(1 − α/(2M)) at α = ${(100 * s.alpha).toFixed(0)}%, against the number of tests M on a log scale from 1 to a million, ` +
          `with the upper bound √(2 ln(2M/α)) of Theorem 2.3 above it and √(2 ln M), its growth rate, below. The hurdle first reaches 3.0 at M = ${crossing}.`,
        x: { label: "Number of tests M (log scale)", log: true, domain: [1, 1e6], format: "~s" },
        y: { label: "t-statistic hurdle", domain: [0, 6.5], format: ".0f" },
        layers: [
          { type: "line", name: "exact hurdle Φ⁻¹(1 − α/(2M))", points: ms.map((m) => [m, hurdle(m)]), series: 0 },
          { type: "line", name: "upper bound √(2 ln(2M/α))", points: ms.map((m) => [m, Math.sqrt(2 * Math.log((2 * m) / s.alpha))]), series: 1, dash: 1 },
          { type: "line", name: "growth rate √(2 ln M)", points: ms.map((m) => [m, Math.sqrt(2 * Math.log(m))]), series: 2, dash: 2 },
          { type: "rule", y: 1.96, label: "1.96", labelAt: 3e4, below: true },
          { type: "rule", y: 3, label: "3.0", labelAt: 3e4, below: true },
        ],
      });
      return `α = ${(100 * s.alpha).toFixed(0)}%: hurdle ${[1, 10, 100, 1000, 1e6].map((m) => `${hurdle(m).toFixed(2)} at M = ${m.toLocaleString("en-US")}`).join(", ")}; it first reaches 3.0 at M = ${crossing}.`;
    },
  });
}

/**
 * P(min of K two-sided p-values ≤ α) for equicorrelated standard normal statistics
 * Z_k = √ρ C + √(1 − ρ) e_k under the null, by integrating over the common factor C.
 */
export function falsePositiveRate(K, rho, alpha) {
  const c = normPpf(1 - alpha / 2);
  if (rho === 0) return 1 - Math.pow(1 - alpha, K);
  const a = Math.sqrt(rho);
  const b = Math.sqrt(1 - rho);
  const allInside = simpson((z) => normPdf(z) * Math.pow(normCdf((c - a * z) / b) - normCdf((-c - a * z) / b), K), -9, 9, 1200);
  return 1 - allInside;
}

function forkingPaths(el) {
  const ks = [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30, 40, 50];
  const rhos = [0, 0.5, 0.8, 0.95];
  const alpha = 0.05;
  const curves = rhos.map((rho) => ks.map((k) => [k, falsePositiveRate(k, rho, alpha)]));
  mountFigure(el, {
    draw(area, _s, width) {
      plot(area, {
        width,
        title: "False-positive rate of reporting the best of K analyses of a true null",
        desc:
          `The probability that the smallest of K two-sided p-values falls below 5% when every analysis tests a true null and the statistics have ` +
          `common correlation ρ. Every curve lies between the bounds of Proposition 3.2, α and min(1, Kα). Independent analyses (ρ = 0) reach ` +
          `${curves[0][7][1].toFixed(2)} at K = 10; highly correlated ones (ρ = 0.95) reach ${curves[3][7][1].toFixed(2)}.`,
        x: { label: "Number of analyses K", domain: [1, 50], format: "d" },
        y: { label: "P(best p-value < 5%)", domain: [0, 1], format: ".1f" },
        layers: [
          ...rhos.map((rho, i) => ({ type: "line", name: `ρ = ${rho}`, points: curves[i], series: i, dash: i % 3 })),
          { type: "line", name: "upper bound min(1, Kα)", points: ks.map((k) => [k, Math.min(1, k * alpha)]), series: 5, dash: 2 },
          { type: "rule", y: alpha, label: "nominal 5%", labelAt: 46 },
        ],
      });
      return `At K = 10: ${rhos.map((rho, i) => `${curves[i][7][1].toFixed(3)} for ρ = ${rho}`).join(", ")}.`;
    },
  });
}

function bayesPosterior(el) {
  const priors = [0.5, 0.8, 0.95, 0.99];
  const posterior = (t, pi0) => {
    const odds = pi0 / (1 - pi0);
    const mbf = Math.exp((-t * t) / 2);
    return (odds * mbf) / (1 + odds * mbf);
  };
  mountFigure(el, {
    controls: [{ type: "range", key: "t", label: "t-statistic", min: 0, max: 5, step: 0.05, value: 3, format: (v) => v.toFixed(2) }],
    draw(area, s, width) {
      const ts = linspace(0, 5, 201);
      plot(area, {
        width,
        title: "The smallest posterior probability of the null that a t-statistic allows",
        desc:
          `Lower bounds on the posterior probability of the null, PO·e^(−t²/2)/(1 + PO·e^(−t²/2)), against the t-statistic for prior null probabilities ` +
          `0.5, 0.8, 0.95 and 0.99, with the two-sided p-value for comparison. At t = ${s.t.toFixed(2)} the p-value is ${(2 * normSf(s.t)).toPrecision(2)}, ` +
          `and the bound is ${priors.map((p) => posterior(s.t, p).toFixed(3)).join(", ")} for the four priors.`,
        x: { label: "t-statistic", domain: [0, 5], format: ".0f" },
        y: { label: "Probability", domain: [0, 1], format: ".1f" },
        layers: [
          ...priors.map((pi0, i) => ({ type: "line", name: `lower bound, prior P(null) = ${pi0}`, points: ts.map((t) => [t, posterior(t, pi0)]), series: i, dash: i % 3 })),
          { type: "line", name: "two-sided p-value", points: ts.map((t) => [t, 2 * normSf(t)]), series: 5, dash: 2 },
          { type: "dots", points: priors.map((pi0) => [s.t, posterior(s.t, pi0)]), series: 5, r: 4 },
          { type: "rule", x: s.t, label: `t = ${s.t.toFixed(2)}` },
        ],
      });
      return (
        `t = ${s.t.toFixed(2)}: two-sided p = ${(2 * normSf(s.t)).toPrecision(3)}, minimum Bayes factor e^(−t²/2) = ${Math.exp((-s.t * s.t) / 2).toPrecision(3)}; ` +
        `posterior probability of the null at least ${priors.map((p) => `${posterior(s.t, p).toFixed(3)} (prior ${p})`).join(", ")}.`
      );
    },
  });
}

const FIGURES = { "hurdle-growth": hurdleGrowth, "forking-paths": forkingPaths, "bayes-posterior": bayesPosterior };

export function drawFigures() {
  drawAll(FIGURES);
}
