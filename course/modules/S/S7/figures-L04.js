// L04 figures, computed live: one stationary-bootstrap resample drawn block by block
// (Definition 3.1), the exact bootstrap variance of the mean (Theorem 3.3) against the block
// length for a simulated AR(1) sample (Remark 3.4), and the Reality Check and SPA-style null
// distributions as useless strategies join the universe (Section 6, Lab 3's design at a smaller scale).
// Every statistic comes from a kernel in multitest.js or stats.js that tests/test_figure_kernels.py compares
// with Python; this file only simulates data and lays out the results. The same test checks every DEFAULT_*
// claim below.

import { drawAll, mountFigure, plot, svgFrame } from "../../../assets/js/chart.js";
import {
  bootstrapColumnMeans,
  bootstrapVarianceOfMean,
  circularAutocovariance,
  columnMoments,
  realityCheckSpa,
  stationaryBootstrap,
} from "../../../assets/js/multitest.js";
import { histogram, logIntegers, rng } from "../../../assets/js/stats.js";

// ---------------------------------------------------------------- one resample, block by block

export const BLOCK_N = 20;
const BLOCK_CHOICES = [1, 2, 4, 8, 20];
// Seed 2 is a median draw: at b = 4 its number of blocks equals the median over seeds 1–200 (the smallest such seed).
export const DEFAULT_BLOCK_SEED = 2;

/** The stationary-bootstrap resample shown for a seed and mean block length, grouped into blocks. */
export function blockDraw(seed, b) {
  const { indices, starts } = stationaryBootstrap(BLOCK_N, b, rng(seed * 7919 + b));
  const blocks = [];
  for (let t = 0; t < BLOCK_N; t += 1) {
    if (starts[t]) blocks.push({ start: t, from: indices[t], length: 0, wraps: false });
    const block = blocks[blocks.length - 1];
    if (block.length && indices[t] === 0) block.wraps = true;
    block.length += 1;
  }
  return { indices, blocks };
}

function bootstrapBlocks(el) {
  let seed = DEFAULT_BLOCK_SEED;
  mountFigure(el, {
    controls: [
      { type: "range", key: "bi", label: "Mean block length b", min: 0, max: BLOCK_CHOICES.length - 1, step: 1, value: 2, format: (i) => String(BLOCK_CHOICES[i]) },
      { type: "button", label: "Resample", onClick: () => (seed += 1) },
    ],
    draw(area, s, width) {
      const n = BLOCK_N;
      const b = BLOCK_CHOICES[s.bi];
      const { indices, blocks } = blockDraw(seed, b);
      const left = 8;
      const cell = (width - 2 * left) / n;
      const labels = cell >= 14;
      const rowH = 26;
      const shade = (i) => 0.08 + (0.5 * i) / (n - 1);
      const svg = svgFrame(area, {
        width,
        height: 150,
        title: "One stationary-bootstrap resample, block by block",
        desc:
          `The top row is an original sample of ${n} observations, shaded from faint (index 0) to strong (index ${n - 1}). ` +
          `The bottom row is one resample with mean block length ${b}: each cell copies the original observation of the same shade. ` +
          `It has ${blocks.length} block${blocks.length === 1 ? "" : "s"}; within a block the shade strengthens one step at a time, and a block that runs past index ${n - 1} ` +
          `wraps to index 0${blocks.some((k) => k.wraps) ? ", as happens here" : ""}.`,
      });
      const g = svg.append("g").attr("class", "series-0");
      const row = (y, values, title) => {
        svg.append("text").attr("class", "small").attr("x", left).attr("y", y - 6).text(title);
        values.forEach((v, t) => {
          g.append("rect")
            .attr("class", "cell fill-series")
            .attr("x", left + t * cell)
            .attr("y", y)
            .attr("width", cell)
            .attr("height", rowH)
            .attr("style", `fill-opacity:${shade(v).toFixed(3)}`);
          if (labels) {
            svg.append("text").attr("class", "small mono").attr("x", left + (t + 0.5) * cell).attr("y", y + 17).attr("text-anchor", "middle").text(v);
          }
        });
      };
      row(22, Array.from({ length: n }, (_, i) => i), "Original sample: observation index");
      row(84, Array.from(indices), "Resample: the original observation each period copies");
      for (const block of blocks) {
        const x0 = left + block.start * cell;
        svg.append("line").attr("class", "edge").attr("x1", x0).attr("x2", x0).attr("y1", 80).attr("y2", 84 + rowH + 4).attr("style", "stroke-width:2.5");
        const x1 = left + (block.start + block.length) * cell;
        svg.append("path").attr("class", "edge").attr("d", `M${x0 + 2},${120} v5 H${x1 - 2} v-5`);
        if (block.wraps) {
          svg.append("text").attr("class", "small").attr("x", (x0 + x1) / 2).attr("y", 140).attr("text-anchor", "middle").text("wraps");
        }
      }
      const list = blocks.map((k) => `${k.from}→${(k.from + k.length - 1) % n}`).join(", ");
      return (
        `Resample ${seed}${seed === DEFAULT_BLOCK_SEED && b === 4 ? " (a median draw at b = 4)" : ""}, b = ${b}: ${blocks.length} block${blocks.length === 1 ? "" : "s"} ` +
        `(expected 1 + ${n - 1}/${b} = ${+(1 + (n - 1) / b).toFixed(2)}), mean length ${(n / blocks.length).toFixed(1)}: ${list}.`
      );
    },
  });
}

// ---------------------------------------------------------------- the bootstrap variance against block length

const AR_N = 500;
// Seed 186 is a typical draw at ϕ = 0.5: each number the readout prints (the ratio at b = 1, the height and block
// length of the peak, the ratio at b = AR_N) is within 17 ranks of its median over seeds 1–200, so between the
// 41st and 59th percentiles; no seed in 1–200 is closer on all four. At other ϕ it is just one sample.
export const DEFAULT_AR_SEED = 186;

/** Circular autocovariances of one SIMULATED stationary AR(1) sample of AR_N observations, unit innovations. */
export function ar1Autocovariance(seed, phi) {
  const g = rng(seed * 1000 + Math.round(phi * 100));
  const x = new Array(AR_N);
  x[0] = g.normal() / Math.sqrt(1 - phi * phi);
  for (let t = 1; t < AR_N; t += 1) x[t] = phi * x[t - 1] + g.normal();
  return circularAutocovariance(x);
}

/** Bootstrap s.e. of the mean over the true long-run s.e., at mean block lengths on a log grid from 1 to AR_N. */
export function varianceCurve(c, phi) {
  const longRun = 1 / (1 - phi) ** 2;
  return logIntegers(1, AR_N, 30).map((b) => [b, Math.sqrt((AR_N * bootstrapVarianceOfMean(c, b)) / longRun)]);
}

function bootstrapVariancePlot(el) {
  let seed = DEFAULT_AR_SEED;
  let cache = null;
  mountFigure(el, {
    controls: [
      { type: "range", key: "phi", label: "AR(1) coefficient ϕ", min: 0, max: 0.9, step: 0.1, value: 0.5, format: (v) => v.toFixed(1) },
      { type: "button", label: "Draw a new sample", onClick: () => ((seed += 1), (cache = null)) },
    ],
    draw(area, s, width) {
      if (!cache || cache.phi !== s.phi) cache = { phi: s.phi, c: ar1Autocovariance(seed, s.phi) };
      const points = varianceCurve(cache.c, s.phi);
      const best = points.reduce((a, p) => (p[1] > a[1] ? p : a));
      const first = points[0][1];
      const last = points[points.length - 1][1];
      const iidTrue = Math.sqrt((1 - s.phi) / (1 + s.phi));
      plot(area, {
        width,
        title: "Stationary-bootstrap standard error of the mean against the block length",
        desc:
          `For one SIMULATED AR(1) sample of ${AR_N} observations with ϕ = ${s.phi.toFixed(1)}, the exact bootstrap standard error of the mean from formula (2), ` +
          `as a fraction of the true long-run standard error, against the mean block length on a log scale. It is ${first.toFixed(2)} at b = 1 (the iid bootstrap), ` +
          `peaks at ${best[1].toFixed(2)} near b = ${best[0]}, and is ${last.toFixed(2)} at b = ${AR_N}.`,
        x: { label: "Mean block length b (log scale)", log: true, domain: [1, AR_N], format: "~s" },
        y: { label: "Bootstrap s.e. / true s.e.", domain: [0, Math.max(1.3, best[1] * 1.08)], format: ".1f" },
        layers: [
          { type: "line", name: "exact bootstrap s.e., formula (2)", points, series: 0 },
          { type: "rule", y: 1, label: "true s.e.", tone: "strong" },
          // Named in the legend: the curve starts at this level at b = 1, so a label on the line would sit on it.
          { type: "rule", y: iidTrue, name: "iid level √((1−ϕ)/(1+ϕ))" },
        ],
      });
      return (
        `ϕ = ${s.phi.toFixed(1)}, sample ${seed}${seed === DEFAULT_AR_SEED && Math.abs(s.phi - 0.5) < 1e-9 ? " (a typical draw at ϕ = 0.5)" : ""}: the bootstrap gives ${(100 * first).toFixed(0)}% of the true ` +
        `standard error at b = 1, ${(100 * best[1]).toFixed(0)}% at its best (b ≈ ${best[0]}) and ${(100 * last).toFixed(0)}% at b = ${AR_N}.`
      );
    },
  });
}

// ---------------------------------------------------------------- Reality Check against SPA-style recentring

const RC_T = 500;
const RC_B = 1000;
const RC_K = 110;
// Seed 2001 is a median draw: across seeds 2000–2029 its observed maximum and its Reality Check p-values with
// 0 and 100 poor strategies are each within three ranks of the medians (the smallest such seed).
export const DEFAULT_RC_SEED = 2001;

/** A SIMULATED universe of Lab 3's design at a smaller scale, with the bootstrap means of all RC_K strategies. */
export function universe(seed) {
  const g = rng(seed);
  const d = Array.from({ length: RC_T }, () =>
    Float64Array.from({ length: RC_K }, (_, k) => g.normal() + (k === 0 ? 3 / Math.sqrt(RC_T) : k >= 10 ? -0.25 : 0)),
  );
  const { mean: means, sd: sds } = columnMoments(d);
  // The same B resamples for every universe size: bootstrap means of all RC_K columns.
  const bootMeans = Array.from({ length: RC_B }, () => bootstrapColumnMeans(d, stationaryBootstrap(RC_T, 10, g).indices));
  return { means, sds, bootMeans };
}

function realityCheckVsSpa(el) {
  let seed = DEFAULT_RC_SEED;
  let u = universe(seed);
  mountFigure(el, {
    controls: [
      { type: "range", key: "poor", label: "Poor strategies added", min: 0, max: 100, step: 10, value: 0 },
      { type: "button", label: "Draw a new universe", onClick: () => ((seed += 1), (u = universe(seed))) },
    ],
    draw(area, s, width) {
      const now = realityCheckSpa(u.means, u.sds, u.bootMeans, RC_T, 10 + s.poor);
      const base = realityCheckSpa(u.means, u.sds, u.bootMeans, RC_T, 10);
      const asLine = (xs) => histogram(xs, -0.5, 6, 52).flatMap((bin) => [[bin.x0, bin.count / RC_B], [bin.x1, bin.count / RC_B]]);
      const spaMoved = Math.abs(now.pSpa - base.pSpa) >= 0.005;
      plot(area, {
        width,
        title: "Null distributions of the Reality Check and the SPA-style test as poor strategies are added",
        desc:
          `SIMULATED universe of ten strategies, one with a true edge, plus ${s.poor} poor strategies. Each test reads its own observed statistic against its own null: ` +
          `the Reality Check's maximum √T·d̄ is ${now.v.toFixed(2)}, and the SPA-style maximum, studentized by each strategy's standard deviation, is ${now.tObs.toFixed(2)}. ` +
          (s.poor === 0
            ? `With no poor strategies the Reality Check's p-value is ${now.pRc.toFixed(3)} and the SPA-style p-value ${now.pSpa.toFixed(3)}; they differ because the SPA-style statistic is studentized` +
              `${now.recentred ? ` and keeps ${now.recentred} strateg${now.recentred === 1 ? "y" : "ies"} below its threshold at ${now.recentred === 1 ? "its" : "their"} own mean${now.recentred === 1 ? "" : "s"}` : ""}. ` +
              `Adding poor strategies raises the Reality Check's p-value, because each is recentred at zero and competes for the maximum.`
            : `The Reality Check's p-value goes from ${base.pRc.toFixed(3)} with no poor strategies to ${now.pRc.toFixed(3)}, because every poor strategy is recentred at zero and competes for the maximum. ` +
              `The SPA-style p-value ${spaMoved ? `moves from ${base.pSpa.toFixed(3)} to ${now.pSpa.toFixed(3)}, because ${s.poor - now.recentred + base.recentred} poor strateg${s.poor - now.recentred + base.recentred === 1 ? "y escapes" : "ies escape"} the recentring threshold` : `stays at ${now.pSpa.toFixed(3)}`}.`),
        x: { label: "Bootstrap maximum statistic", domain: [-0.5, 6], format: ".0f" },
        y: { label: "Share of resamples", format: ".2f" },
        layers: [
          { type: "line", name: "Reality Check (all recentred at 0)", points: asLine(now.rc), series: 1 },
          { type: "line", name: "SPA-style (poor strategies keep their mean)", points: asLine(now.spa), series: 0, dash: 1 },
          // Named in the legend: the two observed statistics are often a few pixels apart.
          { type: "rule", x: now.v, name: `Reality Check observed V = ${now.v.toFixed(2)}`, tone: "strong" },
          { type: "rule", x: now.tObs, name: `SPA-style observed t = ${now.tObs.toFixed(2)}` },
        ],
      });
      return (
        `Universe ${seed}${seed === DEFAULT_RC_SEED ? " (a median draw)" : ""}, ${s.poor} poor strategies: Reality Check p = ${now.pRc.toFixed(3)}; ` +
        `SPA-style p = ${now.pSpa.toFixed(3)}, with ${now.recentred} of ${10 + s.poor} strategies recentred at their own means.`
      );
    },
  });
}

const FIGURES = { "bootstrap-blocks": bootstrapBlocks, "bootstrap-variance": bootstrapVariancePlot, "rc-vs-spa": realityCheckVsSpa };

export function drawFigures() {
  drawAll(FIGURES);
}
