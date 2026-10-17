// L07 figure, computed live from formulas (2) and (3): the probabilistic and deflated Sharpe
// ratios as areas under the sampling density of the estimated Sharpe ratio. The defaults are
// the strategy of Examples 2.3 and 3.2.

import { drawAll, mountFigure, plot } from "../../../assets/js/chart.js";
import { EULER_MASCHERONI, linspace, normCdf, normPdf, normPpf } from "../../../assets/js/stats.js";

const TRIALS = [1, 2, 5, 10, 20, 40, 100, 200, 500, 1000];
const DAYS = [126, 252, 504, 756, 1260, 2520, 5040];

/** Formula (3): SR0 for N trials whose Sharpe ratios have cross-sectional standard deviation sd. */
export function benchmarkSharpe(n, sd) {
  if (n === 1) return 0;
  return sd * ((1 - EULER_MASCHERONI) * normPpf(1 - 1 / n) + EULER_MASCHERONI * normPpf(1 - 1 / (n * Math.E)));
}

/** The standard error in formula (2), evaluated at the estimated Sharpe ratio. */
export function sharpeStdError(sr, T, skew, kurt) {
  return Math.sqrt((1 - skew * sr + ((kurt - 1) / 4) * sr * sr) / (T - 1));
}

function dsrExplorer(el) {
  mountFigure(el, {
    controls: [
      { type: "range", key: "sr", label: "Estimated Sharpe ratio (per day)", min: 0, max: 0.2, step: 0.005, value: 0.09, format: (v) => v.toFixed(3) },
      { type: "range", key: "ti", label: "Days T", min: 0, max: DAYS.length - 1, step: 1, value: 3, format: (i) => DAYS[i].toLocaleString("en-US") },
      { type: "range", key: "skew", label: "Skewness γ3", min: -3, max: 1, step: 0.1, value: -1.5, format: (v) => v.toFixed(1) },
      { type: "range", key: "kurt", label: "Kurtosis γ4", min: 3, max: 15, step: 0.5, value: 8, format: (v) => v.toFixed(1) },
      { type: "range", key: "ni", label: "Trials N", min: 0, max: TRIALS.length - 1, step: 1, value: 5, format: (i) => TRIALS[i].toLocaleString("en-US") },
      { type: "range", key: "dispersion", label: "s.d. of trial Sharpe ratios", min: 0.005, max: 0.06, step: 0.005, value: 0.03, format: (v) => v.toFixed(3) },
    ],
    draw(area, s, width) {
      const T = DAYS[s.ti];
      const N = TRIALS[s.ni];
      // No distribution has kurtosis below 1 + skewness² (Pearson's inequality, Problem P1), so no PSR exists there.
      if (s.kurt < 1 + s.skew * s.skew) {
        const note = document.createElement("p");
        note.className = "figure-note";
        note.textContent = `No distribution has kurtosis below 1 + skewness² = ${(1 + s.skew * s.skew).toFixed(2)} (Problem P1); raise the kurtosis or reduce the skewness.`;
        area.append(note);
        return "";
      }
      const bracket = 1 - s.skew * s.sr + ((s.kurt - 1) / 4) * s.sr * s.sr;
      const se = sharpeStdError(s.sr, T, s.skew, s.kurt);
      const sr0 = benchmarkSharpe(N, s.dispersion);
      const psr = normCdf(s.sr / se);
      const dsr = normCdf((s.sr - sr0) / se);
      const lo = Math.min(-4 * se, sr0 - 4 * se, s.sr - se);
      const hi = Math.max(sr0 + 4 * se, s.sr + 2 * se);
      const xs = linspace(lo, hi, 241);
      const density = (centre) => xs.map((x) => [x, normPdf((x - centre) / se) / se]);
      const shade = (centre) => xs.filter((x) => x <= s.sr).map((x) => [x, 0, normPdf((x - centre) / se) / se]);
      plot(area, {
        width,
        title: "The probabilistic and deflated Sharpe ratios as areas",
        desc:
          `Two normal densities with the standard error ${se.toFixed(4)} of formula (2): one centred at 0 (the PSR benchmark) and one at SR0 = ${sr0.toFixed(4)}, ` +
          `the expected maximum of ${N} null trial${N === 1 ? "" : "s"} (the DSR benchmark). The area of each to the left of the estimated Sharpe ratio ${s.sr.toFixed(3)} ` +
          `is PSR = ${psr.toFixed(3)} and DSR = ${dsr.toFixed(3)}.`,
        x: { label: "Sharpe ratio per day", domain: [lo, hi], format: ".2f" },
        y: { label: "Density" },
        layers: [
          { type: "area", name: `DSR = ${dsr.toFixed(3)} (area left of the estimate)`, points: shade(sr0), series: 1 },
          { type: "line", name: "benchmark 0 (PSR)", points: density(0), series: 0, dash: 1 },
          { type: "line", name: `benchmark SR0 = ${sr0.toFixed(4)} (DSR)`, points: density(sr0), series: 1 },
          { type: "rule", x: s.sr, label: `estimate ${s.sr.toFixed(3)}`, tone: "strong" },
          { type: "rule", x: sr0, label: "SR0", row: 1 },
        ],
      });
      return (
        `s.e. = √(${bracket.toFixed(4)}/${T - 1}) = ${se.toFixed(4)}; PSR(0) = Φ(${(s.sr / se).toFixed(3)}) = ${psr.toFixed(3)}; ` +
        `SR0 = ${sr0.toFixed(4)} per day (${(sr0 * Math.sqrt(252)).toFixed(2)} annualized) for N = ${N}; DSR = Φ(${((s.sr - sr0) / se).toFixed(3)}) = ${dsr.toFixed(3)}.`
      );
    },
  });
}

const FIGURES = { "dsr-explorer": dsrExplorer };

export function drawFigures() {
  drawAll(FIGURES);
}
