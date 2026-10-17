// Multiple-testing kernels for live figures, with the conventions of the Atlas A8
// contract (atlas/A8.contract.md) so a figure can never disagree with the graded
// Python API. tests/test_figure_kernels.py runs each function under Node on fixed
// inputs and requires the same answer as the S7 reference solution.

/** Indices that sort xs ascending, stable on ties. */
export function argsort(xs) {
  return xs.map((x, i) => [x, i]).sort((a, b) => a[0] - b[0] || a[1] - b[1]).map((pair) => pair[1]);
}

/** Bonferroni at level alpha: reject p_i ≤ alpha / m. */
export function bonferroni(pvalues, alpha) {
  const m = pvalues.length;
  return pvalues.map((p) => p <= alpha / m);
}

/**
 * Holm's step-down procedure (L02 Definition 3.1). Returns the rejection mask in input order,
 * the sort order, the thresholds alpha / (m + 1 − k) along it, and the 1-based rank k at which it stops
 * (m + 1 if it rejects everything).
 */
export function holm(pvalues, alpha) {
  const m = pvalues.length;
  const order = argsort(pvalues);
  const thresholds = order.map((_, j) => alpha / (m - j));
  let stop = m + 1;
  for (let j = 0; j < m; j += 1) {
    if (pvalues[order[j]] > thresholds[j]) {
      stop = j + 1;
      break;
    }
  }
  const mask = new Array(m).fill(false);
  for (let j = 0; j < stop - 1; j += 1) mask[order[j]] = true;
  return { mask, order, thresholds, stop };
}

/**
 * Benjamini–Hochberg step-up at level q (L03 Definition 2.1): reject the k* smallest p-values,
 * k* = max{k : p_(k) ≤ k q / m}, 0 if none. Returns the mask in input order, k*, the order and the lines k q / m.
 */
export function benjaminiHochberg(pvalues, q) {
  const m = pvalues.length;
  const order = argsort(pvalues);
  const lines = order.map((_, j) => ((j + 1) * q) / m);
  let kStar = 0;
  for (let j = 0; j < m; j += 1) if (pvalues[order[j]] <= lines[j]) kStar = j + 1;
  const mask = new Array(m).fill(false);
  for (let j = 0; j < kStar; j += 1) mask[order[j]] = true;
  return { mask, kStar, order, lines };
}

/** Benjamini–Yekutieli: BH at level q / c(m), c(m) = Σ_{j ≤ m} 1/j (L03 Definition 5.4). */
export function benjaminiYekutieli(pvalues, q) {
  let c = 0;
  for (let j = 1; j <= pvalues.length; j += 1) c += 1 / j;
  return { ...benjaminiHochberg(pvalues, q / c), c };
}

/**
 * One stationary-bootstrap index vector (L04 Definition 3.1): I_1 uniform; afterwards, with
 * probability 1 / meanBlock a new block starts at a uniform index, otherwise I_t = (I_{t−1} + 1) mod n.
 * `starts[t]` records whether a block starts at t. `gen` is a generator from stats.js rng().
 */
export function stationaryBootstrap(n, meanBlock, gen) {
  if (!(meanBlock >= 1)) throw new RangeError("meanBlock must be at least 1");
  const p = 1 / meanBlock;
  const indices = new Int32Array(n);
  const starts = new Array(n).fill(false);
  indices[0] = gen.integer(n);
  starts[0] = true;
  for (let t = 1; t < n; t += 1) {
    if (gen.uniform() < p) {
      indices[t] = gen.integer(n);
      starts[t] = true;
    } else {
      indices[t] = (indices[t - 1] + 1) % n;
    }
  }
  return { indices, starts };
}

/** The ceil((1 − alpha) B)-th smallest of values (1-based), as in the A8 contract. */
export function upperCritical(values, alpha) {
  const sorted = Float64Array.from(values).sort();
  const rank = Math.ceil((1 - alpha) * sorted.length);
  return sorted[Math.min(sorted.length, Math.max(1, rank)) - 1];
}

/**
 * Romano–Wolf step-down given observed statistics tObs (K) and centred bootstrap statistics
 * tBoot (B rows of K), as stepdown_rejections in the A8 contract. Also returns every step:
 * the active set, its critical value and the hypotheses it rejected.
 */
export function stepdown(tObs, tBoot, alpha) {
  const K = tObs.length;
  let active = [...Array(K).keys()];
  const mask = new Array(K).fill(false);
  const steps = [];
  while (active.length) {
    const maxima = tBoot.map((row) => Math.max(...active.map((k) => row[k])));
    const critical = upperCritical(maxima, alpha);
    const rejected = active.filter((k) => tObs[k] > critical);
    steps.push({ active: [...active], critical, rejected });
    if (!rejected.length) break;
    for (const k of rejected) mask[k] = true;
    active = active.filter((k) => !mask[k]);
  }
  return { mask, steps };
}

/** All k-subsets of {0, …, n − 1} in lexicographic order (the order of Python's itertools.combinations). */
export function combinations(n, k) {
  const out = [];
  const pick = [];
  const visit = (start) => {
    if (pick.length === k) {
      out.push([...pick]);
      return;
    }
    for (let i = start; i <= n - (k - pick.length); i += 1) {
      pick.push(i);
      visit(i + 1);
      pick.pop();
    }
  };
  visit(0);
  return out;
}

/** Whether every row has the same value in column n (the contract's test for zero variance). */
function constantColumn(rows, n) {
  const first = rows[0][n];
  return rows.every((row) => row[n] === first);
}

/** Per-column Sharpe ratio of the given rows: mean / sd (ddof 1); on a constant column 0 if its mean is 0, else ±Infinity. */
export function columnSharpe(rows, columns) {
  const T = rows.length;
  return Array.from({ length: columns }, (_, n) => {
    let total = 0;
    for (const row of rows) total += row[n];
    const m = total / T;
    if (constantColumn(rows, n)) return m === 0 ? 0 : m > 0 ? Infinity : -Infinity;
    let ss = 0;
    for (const row of rows) ss += (row[n] - m) ** 2;
    return m / Math.sqrt(ss / (T - 1));
  });
}

/**
 * Combinatorially symmetric cross-validation (L08 Definition 3.1; probability_of_backtest_overfitting
 * in the A8 contract). matrix: T rows of N per-period returns. Returns the PBO, the logits in
 * combination order, and for each split its in-sample blocks, the selected column, both metric
 * vectors, the out-of-sample rank, ω and the logit.
 */
export function cscv(matrix, S) {
  const N = matrix[0].length;
  if (S % 2 || S < 2 || S > matrix.length) throw new RangeError("S must be even with 2 <= S <= T");
  const rows = matrix.slice(matrix.length % S);
  const size = rows.length / S;
  const blocks = Array.from({ length: S }, (_, s) => rows.slice(s * size, (s + 1) * size));
  const splits = combinations(S, S / 2).map((inSample) => {
    const outSample = [...Array(S).keys()].filter((s) => !inSample.includes(s));
    const isMetric = columnSharpe(inSample.flatMap((s) => blocks[s]), N);
    const oosMetric = columnSharpe(outSample.flatMap((s) => blocks[s]), N);
    let best = 0;
    for (let n = 1; n < N; n += 1) if (isMetric[n] > isMetric[best]) best = n;
    let lower = 0;
    let equal = 0;
    for (let n = 0; n < N; n += 1) {
      if (oosMetric[n] < oosMetric[best]) lower += 1;
      else if (n !== best && oosMetric[n] === oosMetric[best]) equal += 1;
    }
    const rank = 1 + lower + 0.5 * equal;
    const omega = rank / (N + 1);
    return { inSample, outSample, best, isMetric, oosMetric, rank, omega, logit: Math.log(omega / (1 - omega)) };
  });
  const logits = splits.map((s) => s.logit);
  return { pbo: logits.filter((l) => l <= 0).length / logits.length, logits, splits, blockSize: size, dropped: matrix.length % S };
}

/** Column means and sample standard deviations (divisor T − 1) of T rows of K values. */
export function columnMoments(rows) {
  const T = rows.length;
  const K = rows[0].length;
  const mean = new Float64Array(K);
  const sd = new Float64Array(K);
  for (const row of rows) for (let k = 0; k < K; k += 1) mean[k] += row[k] / T;
  for (const row of rows) for (let k = 0; k < K; k += 1) sd[k] += (row[k] - mean[k]) ** 2;
  for (let k = 0; k < K; k += 1) sd[k] = Math.sqrt(sd[k] / (T - 1));
  return { mean, sd };
}

/**
 * Studentized statistics and centred bootstrap statistics, as romano_wolf in the A8 contract:
 * t_k = mean(d_k) / (sd(d_k) / √T) and t*_bk = (mean(d*_k) − mean(d_k)) / (sd(d*_k) / √T), a draw in which
 * the resampled column is constant being studentized by sd(d_k). `draws[b]` is one index vector shared by every column
 * (whole dates resampled) or, with `joint = false`, an array of K index vectors, one per column.
 */
export function studentizedBootstrap(d, draws, joint = true) {
  const T = d.length;
  const K = d[0].length;
  const { mean, sd } = columnMoments(d);
  const root = Math.sqrt(T);
  const t = Array.from(mean, (m, k) => m / (sd[k] / root));
  const boot = draws.map((draw) => {
    const rows = Array.from({ length: T }, (_, i) => (joint ? d[draw[i]] : Array.from({ length: K }, (_, k) => d[draw[k][i]][k])));
    const m = columnMoments(rows);
    return Array.from(m.mean, (v, k) => (v - mean[k]) / ((constantColumn(rows, k) ? sd[k] : m.sd[k]) / root));
  });
  return { t, boot };
}

/** Pearson correlation of two equal-length samples. */
export function correlation(xs, ys) {
  const n = xs.length;
  let mx = 0;
  let my = 0;
  for (let i = 0; i < n; i += 1) {
    mx += xs[i] / n;
    my += ys[i] / n;
  }
  let sxy = 0;
  let sxx = 0;
  let syy = 0;
  for (let i = 0; i < n; i += 1) {
    sxy += (xs[i] - mx) * (ys[i] - my);
    sxx += (xs[i] - mx) ** 2;
    syy += (ys[i] - my) ** 2;
  }
  return sxy / Math.sqrt(sxx * syy);
}

/** Storey's estimate of the share of true nulls: #{p > λ} / ((1 − λ) m) (L03 Remark 6.1). */
export function storeyPi0(pvalues, lambda) {
  return pvalues.filter((p) => p > lambda).length / ((1 - lambda) * pvalues.length);
}

/** Circular sample autocovariances ĉ(0), …, ĉ(n − 1) of x (L04 Theorem 3.3). */
export function circularAutocovariance(x) {
  const n = x.length;
  let m = 0;
  for (const v of x) m += v / n;
  const d = x.map((v) => v - m);
  return Array.from({ length: n }, (_, h) => {
    let s = 0;
    for (let i = 0; i < n; i += 1) s += d[i] * d[(i + h) % n];
    return s / n;
  });
}

/** Formula (2) of L04 Theorem 3.3: the exact stationary-bootstrap variance of the mean, mean block length b. */
export function bootstrapVarianceOfMean(c, b) {
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

/**
 * Reality Check and SPA-style p-values over the first k strategies, as L04 Lab 3 computes them: means and sds
 * of the differentials, bootMeans[b][j] the bootstrap mean of strategy j in draw b, T periods. The Reality Check
 * recentres every strategy at zero; the SPA-style test studentizes and keeps a strategy whose mean lies at or
 * below −sd·√(2 ln ln T / T) at that mean. Returns both observed statistics and both p-values.
 */
export function realityCheckSpa(means, sds, bootMeans, T, k) {
  const root = Math.sqrt(T);
  let v = -Infinity;
  for (let j = 0; j < k; j += 1) v = Math.max(v, root * means[j]);
  let tObs = 0;
  for (let j = 0; j < k; j += 1) tObs = Math.max(tObs, (root * means[j]) / sds[j]);
  const centre = Array.from({ length: k }, (_, j) => (means[j] <= -sds[j] * Math.sqrt((2 * Math.log(Math.log(T))) / T) ? means[j] : 0));
  const rc = [];
  const spa = [];
  for (const m of bootMeans) {
    let a = -Infinity;
    let s = 0;
    for (let j = 0; j < k; j += 1) {
      a = Math.max(a, root * (m[j] - means[j]));
      s = Math.max(s, (root * (m[j] - means[j] + centre[j])) / sds[j]);
    }
    rc.push(a);
    spa.push(s);
  }
  const share = (xs, x) => xs.filter((y) => y >= x).length / xs.length;
  return { v, tObs, rc, spa, pRc: share(rc, v), pSpa: share(spa, tObs), recentred: centre.filter((c) => c !== 0).length };
}
