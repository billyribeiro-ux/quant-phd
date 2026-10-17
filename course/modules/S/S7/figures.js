// S7 figures. Every value is computed in the browser from the formulas on the
// page (no data files): the exact expected maximum of N standard normals by
// numerical integration, the Bailey–López de Prado approximation, and the
// sqrt(2 ln N) bound proved in L01 §2.

import { lineChart } from "../../../assets/js/chart.js";

const EULER_MASCHERONI = 0.5772156649015329;

/** Standard normal density. */
function pdf(x) {
  return Math.exp(-0.5 * x * x) / Math.sqrt(2 * Math.PI);
}

/** Standard normal CDF via the complementary error function; fractional error below 1.2e-7, ample for a chart. */
function cdf(x) {
  return 0.5 * erfc(-x / Math.SQRT2);
}

function erfc(x) {
  const z = Math.abs(x);
  let result;
  if (z < 0.5) {
    result = 1 - erf(z);
  } else {
    const t = 1 / (1 + 0.5 * z);
    // Chebyshev fit for erfc (Press et al., Numerical Recipes, routine erfcc): fractional error < 1.2e-7.
    const y =
      t *
      Math.exp(
        -z * z -
          1.26551223 +
          t * (1.00002368 + t * (0.37409196 + t * (0.09678418 + t * (-0.18628806 + t * (0.27886807 + t * (-1.13520398 + t * (1.48851587 + t * (-0.82215223 + t * 0.17087277)))))))),
      );
    result = y;
  }
  return x >= 0 ? result : 2 - result;
}

function erf(x) {
  // Maclaurin series; converges fast for |x| < 0.5.
  let sum = x;
  let term = x;
  for (let n = 1; n < 40; n += 1) {
    term *= (-x * x) / n;
    sum += term / (2 * n + 1);
  }
  return (2 / Math.sqrt(Math.PI)) * sum;
}

/** Standard normal quantile (Wichura 1988, algorithm AS 241, PPND16; relative accuracy about 1e-16). */
function ppf(p) {
  if (!(p > 0 && p < 1)) throw new RangeError("p must lie in (0, 1)");
  const q = p - 0.5;
  if (Math.abs(q) <= 0.425) {
    const r = 0.180625 - q * q;
    return (
      (q *
        (((((((2509.0809287301226727 * r + 33430.575583588128105) * r + 67265.770927008700853) * r + 45921.953931549871457) * r +
          13731.693765509461125) *
          r +
          1971.5909503065514427) *
          r +
          133.14166789178437745) *
          r +
          3.387132872796366608)) /
      (((((((5226.495278852545925 * r + 28729.085735721942674) * r + 39307.89580009271061) * r + 21213.794301586595867) * r +
        5394.1960214247511077) *
        r +
        687.1870074920579083) *
        r +
        42.313330701600911252) *
        r +
        1)
    );
  }
  let r = q < 0 ? p : 1 - p;
  r = Math.sqrt(-Math.log(r));
  let value;
  if (r <= 5) {
    r -= 1.6;
    value =
      (((((((7.7454501427834140764e-4 * r + 0.0227238449892691845833) * r + 0.24178072517745061177) * r + 1.27045825245236838258) * r +
        3.64784832476320460504) *
        r +
        5.7694972214606914055) *
        r +
        4.6303378461565452959) *
        r +
        1.42343711074968357734) /
      (((((((1.05075007164441684324e-9 * r + 5.475938084995344946e-4) * r + 0.0151986665636164571966) * r + 0.14810397642748007459) * r +
        0.68976733498510000455) *
        r +
        1.6763848301838038494) *
        r +
        2.05319162663775882187) *
        r +
        1);
  } else {
    r -= 5;
    value =
      (((((((2.01033439929228813265e-7 * r + 2.71155556874348757815e-5) * r + 0.0012426609473880784386) * r + 0.026532189526576123093) * r +
        0.29656057182850489123) *
        r +
        1.7848265399172913358) *
        r +
        5.4637849111641143699) *
        r +
        6.6579046435011037772) /
      (((((((2.04426310338993978564e-15 * r + 1.4215117583164458887e-7) * r + 1.8463183175100546818e-5) * r + 7.868691311456132591e-4) * r +
        0.0148753612908506148525) *
        r +
        0.13692988092273580531) *
        r +
        0.59983220655588793769) *
        r +
        1);
  }
  return q < 0 ? -value : value;
}

/** Exact E[max of n iid N(0,1)] by composite Simpson integration of x · n φ(x) Φ(x)^(n−1). */
export function exactExpectedMax(n) {
  const lo = -8;
  const hi = 10;
  const steps = 6000;
  const h = (hi - lo) / steps;
  let total = 0;
  for (let i = 0; i <= steps; i += 1) {
    const x = lo + i * h;
    const weight = i === 0 || i === steps ? 1 : i % 2 ? 4 : 2;
    total += weight * x * n * pdf(x) * Math.pow(cdf(x), n - 1);
  }
  return (total * h) / 3;
}

export function approxExpectedMax(n) {
  return (1 - EULER_MASCHERONI) * ppf(1 - 1 / n) + EULER_MASCHERONI * ppf(1 - 1 / (n * Math.E));
}

function expectedMaxFigure(container) {
  const grid = [];
  for (let e = Math.log10(2); e <= 4.0001; e += 0.05) grid.push(Math.round(Math.pow(10, e)));
  const ns = [...new Set(grid)];
  lineChart(container, {
    title: "Expected maximum of N standard normal statistics",
    desc: "Three curves against the number of trials N on a log scale from 2 to 10,000: the exact expected maximum computed by numerical integration, the Bailey and López de Prado approximation, which lies just above it, and the bound square root of 2 ln N, which lies well above both. All three grow slowly with N.",
    xLabel: "Number of independent trials N (log scale)",
    yLabel: "Expected maximum (standard-normal units)",
    xLog: true,
    xDomain: [2, 10000],
    xFormat: "~s",
    series: [
      { name: "Exact (numerical integration)", points: ns.map((n) => [n, exactExpectedMax(n)]) },
      { name: "Bailey–López de Prado approximation", points: ns.filter((n) => n >= 2).map((n) => [n, approxExpectedMax(n)]) },
      { name: "Bound √(2 ln N)", points: ns.map((n) => [n, Math.sqrt(2 * Math.log(n))]) },
    ],
  });
}

const FIGURES = { "expected-max": expectedMaxFigure };

export function drawFigures() {
  for (const el of document.querySelectorAll("[data-chart]")) {
    const draw = FIGURES[el.dataset.chart];
    if (!draw) throw new Error(`unknown figure ${el.dataset.chart}`);
    draw(el);
  }
}
