// L04 figures, computed live: one stationary-bootstrap resample drawn block by block
// (Definition 3.1), the exact bootstrap variance of the mean (Theorem 3.3) against the block
// length for a simulated AR(1) sample (Remark 3.4), and the Reality Check and SPA-style null
// distributions as useless strategies join the universe (Section 6, Lab 3's design).

import { drawAll, mountFigure, plot, svgFrame } from "../../../assets/js/chart.js";
import { stationaryBootstrap } from "../../../assets/js/multitest.js";
import { histogram, logIntegers, rng } from "../../../assets/js/stats.js";

function blocksOf(indices, starts) {
  const blocks = [];
  for (let t = 0; t < indices.length; t += 1) {
    if (starts[t]) blocks.push({ start: t, from: indices[t], length: 0, wraps: false });
    const block = blocks[blocks.length - 1];
    if (block.length && indices[t] === 0) block.wraps = true;
    block.length += 1;
  }
  return blocks;
}

function bootstrapBlocks(el) {
  const n = 30;
  let seed = 4;
  const choices = [1, 2, 4, 8, 15, 30];
  mountFigure(el, {
    controls: [
      { type: "range", key: "bi", label: "Mean block length b", min: 0, max: choices.length - 1, step: 1, value: 2, format: (i) => String(choices[i]) },
      { type: "button", label: "Resample", onClick: () => (seed += 1) },
    ],
    draw(area, s, width) {
      const b = choices[s.bi];
      const { indices, starts } = stationaryBootstrap(n, b, rng(seed * 7919 + b));
      const blocks = blocksOf(indices, starts);
      const left = 8;
      const cell = (width - 2 * left) / n;
      const labels = cell >= 15;
      const rowH = 26;
      const height = 150;
      const shade = (i) => 0.08 + (0.5 * i) / (n - 1);
      const svg = svgFrame(area, {
        width,
        height,
        title: "One stationary-bootstrap resample, block by block",
        desc:
          `The top row is an original sample of ${n} observations, shaded from light (index 0) to dark (index ${n - 1}). ` +
          `The bottom row is one resample with mean block length ${b}: each cell copies the original observation of the same shade. ` +
          `It has ${blocks.length} blocks; within a block the shade deepens by one step, and a block that runs past index ${n - 1} wraps to index 0` +
          `${blocks.some((k) => k.wraps) ? ", as happens here" : ""}.`,
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
      row(
        22,
        Array.from({ length: n }, (_, i) => i),
        "Original sample: observation index",
      );
      row(84, Array.from(indices), "Resample: index of the original observation each period copies");
      for (const block of blocks) {
        const x0 = left + block.start * cell;
        svg.append("line").attr("class", "edge").attr("x1", x0).attr("x2", x0).attr("y1", 80).attr("y2", 84 + rowH + 4).attr("style", "stroke-width:2.5");
        const x1 = left + (block.start + block.length) * cell;
        svg.append("path").attr("class", "edge").attr("d", `M${x0 + 2},${120} v5 H${x1 - 2} v-5`);
        if (block.wraps) {
          svg.append("text").attr("class", "small").attr("x", (x0 + x1) / 2).attr("y", 140).attr("text-anchor", "middle").text("wraps");
        }
      }
      const text = blocks.map((k) => `${k.from}→${(k.from + k.length - 1) % n}`).join(", ");
      return `b = ${b}: ${blocks.length} blocks (mean length ${(n / blocks.length).toFixed(1)}): ${text}.`;
    },
  });
}

/** Circular sample autocovariances ĉ(0..n−1) of x (Theorem 3.3). */
function circularAutocov(x) {
  const n = x.length;
  const m = x.reduce((a, v) => a + v, 0) / n;
  const d = x.map((v) => v - m);
  return Array.from({ length: n }, (_, h) => {
    let s = 0;
    for (let i = 0; i < n; i += 1) s += d[i] * d[(i + h) % n];
    return s / n;
  });
}

/** Formula (2): the stationary-bootstrap variance of the mean for mean block length b. */
function bootstrapVariance(c, b) {
  const n = c.length;
  const keep = 1 - 1 / b;
  let total = c[0];
  let w = 1;
  for (let h = 1; h < n; h += 1) {
    w *= keep;
    total += 2 * (1 - h / n) * w * c[h];
  }
  return total / n;
}

function bootstrapVariancePlot(el) {
  const n = 500;
  let seed = 11;
  let cache = null;
  const sample = (phi) => {
    const g = rng(seed * 1000 + Math.round(phi * 100));
    const x = new Array(n);
    x[0] = g.normal() / Math.sqrt(1 - phi * phi);
    for (let t = 1; t < n; t += 1) x[t] = phi * x[t - 1] + g.normal();
    return circularAutocov(x);
  };
  mountFigure(el, {
    controls: [
      { type: "range", key: "phi", label: "AR(1) coefficient φ", min: 0, max: 0.9, step: 0.1, value: 0.5, format: (v) => v.toFixed(1) },
      { type: "button", label: "Draw a new sample", onClick: () => ((seed += 1), (cache = null)) },
    ],
    draw(area, s, width) {
      if (!cache || cache.phi !== s.phi) cache = { phi: s.phi, c: sample(s.phi) };
      const longRun = 1 / (1 - s.phi) ** 2; // σ² = 1
      const bs = logIntegers(1, n, 30);
      const ratio = (b) => Math.sqrt((n * bootstrapVariance(cache.c, b)) / longRun);
      const points = bs.map((b) => [b, ratio(b)]);
      const best = points.reduce((a, p) => (p[1] > a[1] ? p : a));
      const iidTrue = Math.sqrt((1 - s.phi) / (1 + s.phi));
      plot(area, {
        width,
        title: "Stationary-bootstrap standard error of the mean against the block length",
        desc:
          `For one SIMULATED AR(1) sample of ${n} observations with φ = ${s.phi.toFixed(1)}, the exact bootstrap standard error of the mean from formula (2), ` +
          `as a fraction of the true long-run standard error, against the mean block length on a log scale. It starts at ${ratio(1).toFixed(2)} for b = 1 (the iid bootstrap), ` +
          `peaks at ${best[1].toFixed(2)} near b = ${best[0]}, and falls toward zero as one block covers the whole sample.`,
        x: { label: "Mean block length b (log scale)", log: true, domain: [1, n], format: "~s" },
        y: { label: "Bootstrap s.e. / true long-run s.e.", domain: [0, Math.max(1.3, best[1] * 1.08)], format: ".1f" },
        layers: [
          { type: "line", name: "exact bootstrap s.e., formula (2)", points, series: 0 },
          { type: "rule", y: 1, label: "true long-run s.e.", tone: "strong" },
          { type: "rule", y: iidTrue, label: "population iid level √((1−φ)/(1+φ))", labelAt: 30 },
        ],
      });
      return `φ = ${s.phi.toFixed(1)}, sample ${seed - 10}: the bootstrap recovers ${(100 * ratio(1)).toFixed(0)}% of the true standard error at b = 1, ${(100 * best[1]).toFixed(0)}% at its best (b ≈ ${best[0]}), and ${(100 * ratio(n)).toFixed(0)}% at b = ${n}.`;
    },
  });
}

// The default universe is seed 2024, a median draw: across seeds 2000–2029 the observed maximum has median 2.90
// and the Reality Check p-value median 0.025 with no poor strategies and 0.28 with 100; seed 2024 gives 2.73,
// 0.045 and 0.280. "Draw a new universe" shows the spread.
function universe(seed) {
  // SIMULATED universe with Lab 3's design: one edge worth t ≈ 3, nine nulls, up to 100 poor models (mean −0.25).
  const T = 500;
  const B = 1000;
  const meanBlock = 10;
  const K = 110;
  const g = rng(seed);
  const d = Array.from({ length: T }, () => Float64Array.from({ length: K }, (_, k) => g.normal() + (k === 0 ? 3 / Math.sqrt(T) : k >= 10 ? -0.25 : 0)));
  const means = new Float64Array(K);
  const sds = new Float64Array(K);
  for (let k = 0; k < K; k += 1) {
    let s = 0;
    for (let t = 0; t < T; t += 1) s += d[t][k];
    means[k] = s / T;
    let ss = 0;
    for (let t = 0; t < T; t += 1) ss += (d[t][k] - means[k]) ** 2;
    sds[k] = Math.sqrt(ss / (T - 1));
  }
  // The same B resamples for every universe: bootstrap means of all K columns.
  const boot = Array.from({ length: B }, () => {
    const { indices } = stationaryBootstrap(T, meanBlock, g);
    const sums = new Float64Array(K);
    for (const i of indices) {
      const r = d[i];
      for (let k = 0; k < K; k += 1) sums[k] += r[k];
    }
    return sums.map((v) => v / T);
  });
  return { T, B, means, sds, boot };
}

function realityCheckVsSpa(el) {
  let seed = 2024;
  let u = universe(seed);
  mountFigure(el, {
    controls: [
      { type: "range", key: "poor", label: "Poor strategies added", min: 0, max: 100, step: 10, value: 0 },
      { type: "button", label: "Draw a new universe", onClick: () => ((seed += 1), (u = universe(seed))) },
    ],
    draw(area, s, width) {
      const { T, B, means, sds, boot } = u;
      const root = Math.sqrt(T);
      const threshold = (j) => sds[j] * Math.sqrt((2 * Math.log(Math.log(T))) / T);
      const k = 10 + s.poor;
      const v = root * Math.max(...Array.from(means.subarray(0, k)));
      const rc = boot.map((m) => {
        let best = -Infinity;
        for (let j = 0; j < k; j += 1) best = Math.max(best, root * (m[j] - means[j]));
        return best;
      });
      const centre = Array.from({ length: k }, (_, j) => (means[j] <= -threshold(j) ? means[j] : 0));
      const tObs = Math.max(0, ...Array.from({ length: k }, (_, j) => (root * means[j]) / sds[j]));
      const spa = boot.map((m) => {
        let best = 0;
        for (let j = 0; j < k; j += 1) best = Math.max(best, (root * (m[j] - means[j] + centre[j])) / sds[j]);
        return best;
      });
      const pRc = rc.filter((x) => x >= v).length / B;
      const pSpa = spa.filter((x) => x >= tObs).length / B;
      const asLine = (xs) => histogram(xs, -0.5, 6, 52).flatMap((bin) => [[bin.x0, bin.count / B], [bin.x1, bin.count / B]]);
      plot(area, {
        width,
        title: "Null distributions of the Reality Check and the SPA-style test as poor strategies are added",
        desc:
          `SIMULATED universe of ten strategies, one with a true edge, plus ${s.poor} poor strategies. The Reality Check's bootstrap maximum ` +
          `${s.poor ? "shifts right, because every poor strategy is recentred at zero and competes for the maximum" : "and the SPA-style maximum nearly coincide"}; ` +
          `the SPA-style maximum does not move. p-values: Reality Check ${pRc.toFixed(3)}, SPA-style ${pSpa.toFixed(3)}.`,
        x: { label: "Bootstrap maximum statistic", domain: [-0.5, 6], format: ".0f" },
        y: { label: "Share of the 1,000 resamples", format: ".2f" },
        layers: [
          { type: "line", name: "Reality Check (all recentred at 0)", points: asLine(rc), series: 1 },
          { type: "line", name: "SPA-style (poor strategies keep their mean)", points: asLine(spa), series: 0, dash: 1 },
          { type: "rule", x: v, label: `observed ${v.toFixed(2)}`, tone: "strong" },
        ],
      });
      return `Universe ${seed - 2023}, ${s.poor} poor strategies: Reality Check p = ${pRc.toFixed(3)}; SPA-style p = ${pSpa.toFixed(3)}.`;
    },
  });
}

const FIGURES = { "bootstrap-blocks": bootstrapBlocks, "bootstrap-variance": bootstrapVariancePlot, "rc-vs-spa": realityCheckVsSpa };

export function drawFigures() {
  drawAll(FIGURES);
}
