// L01 figures, computed live from the formulas on the page (no data files): the
// distribution of the best of N null Sharpe ratios, and the exact expected maximum of
// N standard normals against the Bailey–López de Prado approximation and the √(2 ln N) bound.

import { drawAll, lineChart, mountFigure, plot } from "../../../assets/js/chart.js";
import { approxExpectedMax, expectedMaxNormal, linspace, logIntegers, maxNormalPdf, normCdf } from "../../../assets/js/stats.js";

const PERIODS_PER_YEAR = 252;
const TRIALS = [1, 10, 100, 1000];
const EXPECTED_MAX = new Map(TRIALS.map((n) => [n, expectedMaxNormal(n)]));

function maxSharpeDensity(el) {
  mountFigure(el, {
    controls: [{ type: "range", key: "years", label: "Years of daily data", min: 1, max: 20, step: 1, value: 5 }],
    draw(area, s, width) {
      const T = s.years * PERIODS_PER_YEAR;
      // Under the null each trial's annualized Sharpe ratio is approximately N(0, P/T) (S1).
      const scale = Math.sqrt(PERIODS_PER_YEAR / T);
      // The axis reaches past the right tail of the best of 1,000 in every state (its density is negligible beyond 5 standard errors).
      const right = Math.max(3, Math.ceil(2 * scale * 5) / 2);
      const xs = linspace(-1.5, right, 361);
      const layers = TRIALS.map((n, i) => ({
        type: "line",
        name: `best of N = ${n.toLocaleString("en-US")}`,
        points: xs.map((x) => [x, maxNormalPdf(x / scale, n) / scale]),
        series: i,
        dash: i % 3,
      }));
      layers.push({ type: "rule", x: 1, label: "annualized Sharpe 1.0" });
      const tail = (n) => 1 - Math.pow(normCdf(1 / scale), n);
      plot(area, {
        width,
        title: "Distribution of the best annualized Sharpe ratio among N independent skill-free strategies",
        desc:
          `Densities of the largest annualized Sharpe ratio among N = 1, 10, 100 and 1,000 independent skill-free strategies, each estimated on ${s.years} ` +
          `year${s.years > 1 ? "s" : ""} of daily data. As N grows the density moves right and narrows; more data pulls every curve toward zero only like one over the square root of T. The expected best of 100 is ` +
          `${(scale * EXPECTED_MAX.get(100)).toFixed(2)} and it exceeds 1.0 with probability ${tail(100).toFixed(2)}.`,
        x: { label: "Best annualized Sharpe ratio", domain: [-1.5, right], format: ".1f" },
        y: { label: "Probability density" },
        layers,
      });
      return (
        `${s.years} year${s.years > 1 ? "s" : ""} of daily data (T = ${T.toLocaleString("en-US")}): expected best Sharpe ` +
        TRIALS.slice(1)
          .map((n) => `${(scale * EXPECTED_MAX.get(n)).toFixed(2)} for N = ${n.toLocaleString("en-US")}`)
          .join(", ") +
        `; the best of 100 exceeds 1.0 with probability ${tail(100).toFixed(3)}.`
      );
    },
  });
}

function expectedMaxFigure(el) {
  const ns = logIntegers(2, 10000);
  lineChart(el, {
    title: "Expected maximum of N standard normal statistics",
    desc: "Three curves against the number of trials N on a log scale from 2 to 10,000: the exact expected maximum computed by numerical integration, the Bailey and López de Prado approximation, which lies below it at N = 2 and just above it from N = 3 on, and the bound square root of 2 ln N, which lies well above both. All three grow slowly with N.",
    xLabel: "Number of independent trials N (log scale)",
    yLabel: "Expected maximum (SD units)",
    xLog: true,
    xDomain: [2, 10000],
    xFormat: "~s",
    series: [
      { name: "Exact (numerical integration)", points: ns.map((n) => [n, expectedMaxNormal(n)]) },
      { name: "Bailey–López de Prado approximation", points: ns.map((n) => [n, approxExpectedMax(n)]) },
      { name: "Bound √(2 ln N)", points: ns.map((n) => [n, Math.sqrt(2 * Math.log(n))]) },
    ],
  });
}

const FIGURES = { "max-sharpe-density": maxSharpeDensity, "expected-max": expectedMaxFigure };

export function drawFigures() {
  drawAll(FIGURES);
}
