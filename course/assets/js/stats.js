// Numerical building blocks for live figures: the standard normal distribution,
// a seeded pseudo-random generator, the expected maximum of independent normals,
// and small descriptive helpers. Pure functions with no DOM access, so the same
// code runs in the browser and under Node: tests/test_figure_kernels.py runs each
// function a figure uses on fixed inputs and compares it with Python.

export const EULER_MASCHERONI = 0.5772156649015329;
const SQRT_2PI = Math.sqrt(2 * Math.PI);

/** Standard normal density φ(x). */
export function normPdf(x) {
  return Math.exp(-0.5 * x * x) / SQRT_2PI;
}

/**
 * Standard normal CDF Φ(x): Hart's (1968) double-precision rational approximation in
 * the arrangement of West (2005). Absolute error below 1e-15 everywhere; relative
 * error of the upper tail 1 − Φ(x) below 1e-8 (computed directly, without cancellation).
 */
export function normCdf(x) {
  const tail = upperTail(Math.abs(x));
  return x > 0 ? 1 - tail : tail;
}

/** Upper tail 1 − Φ(x), accurate in relative terms far into the tail. */
export function normSf(x) {
  return x >= 0 ? upperTail(x) : 1 - upperTail(-x);
}

function upperTail(z) {
  if (z > 37) return 0;
  const e = Math.exp((-z * z) / 2);
  if (z < 7.07106781186547) {
    let n = 3.52624965998911e-2 * z + 0.700383064443688;
    n = n * z + 6.37396220353165;
    n = n * z + 33.912866078383;
    n = n * z + 112.079291497871;
    n = n * z + 221.213596169931;
    n = n * z + 220.206867912376;
    let d = 8.83883476483184e-2 * z + 1.75566716318264;
    d = d * z + 16.064177579207;
    d = d * z + 86.7807322029461;
    d = d * z + 296.564248779674;
    d = d * z + 637.333633378831;
    d = d * z + 793.826512519948;
    d = d * z + 440.413735824752;
    return (e * n) / d;
  }
  let b = z + 0.65;
  b = z + 4 / b;
  b = z + 3 / b;
  b = z + 2 / b;
  b = z + 1 / b;
  return e / b / 2.506628274631;
}

/** Standard normal quantile Φ⁻¹(p) (Wichura 1988, algorithm AS 241, PPND16; relative accuracy about 1e-16). */
export function normPpf(p) {
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

/** Composite Simpson rule for ∫_lo^hi f(x) dx with an even number of steps. */
export function simpson(f, lo, hi, steps = 2000) {
  const n = steps % 2 ? steps + 1 : steps;
  const h = (hi - lo) / n;
  let total = f(lo) + f(hi);
  for (let i = 1; i < n; i += 1) total += (i % 2 ? 4 : 2) * f(lo + i * h);
  return (total * h) / 3;
}

/** Density of the maximum of n iid standard normals: n φ(x) Φ(x)^(n−1). */
export function maxNormalPdf(x, n) {
  return n * normPdf(x) * Math.pow(normCdf(x), n - 1);
}

/** Exact E[max of n iid N(0,1)] by numerical integration of x · n φ(x) Φ(x)^(n−1). */
export function expectedMaxNormal(n) {
  if (!(Number.isInteger(n) && n >= 1)) throw new RangeError("n must be a positive integer");
  return simpson((x) => x * maxNormalPdf(x, n), -9, 10, 6000);
}

/** The Bailey–López de Prado approximation (1 − γ)Φ⁻¹(1 − 1/n) + γΦ⁻¹(1 − 1/(n e)), for n ≥ 2. */
export function approxExpectedMax(n) {
  if (!(n >= 2)) throw new RangeError("the approximation needs n >= 2");
  return (1 - EULER_MASCHERONI) * normPpf(1 - 1 / n) + EULER_MASCHERONI * normPpf(1 - 1 / (n * Math.E));
}

/**
 * Seeded generator (xoshiro128**, state initialized by splitmix32). Deterministic across
 * browsers, so a SIMULATED figure shows the same sample to every reader for the same seed.
 */
export function rng(seed) {
  let a = seed >>> 0;
  const splitmix = () => {
    a = (a + 0x9e3779b9) >>> 0;
    let t = a ^ (a >>> 16);
    t = Math.imul(t, 0x21f0aaad);
    t ^= t >>> 15;
    t = Math.imul(t, 0x735a2d97);
    return (t ^ (t >>> 15)) >>> 0;
  };
  let s0 = splitmix();
  let s1 = splitmix();
  let s2 = splitmix();
  let s3 = splitmix();
  const rotl = (x, k) => (x << k) | (x >>> (32 - k));
  const next = () => {
    const result = Math.imul(rotl(Math.imul(s1, 5), 7), 9) >>> 0;
    const t = s1 << 9;
    s2 ^= s0;
    s3 ^= s1;
    s1 ^= s2;
    s0 ^= s3;
    s2 ^= t;
    s3 = rotl(s3, 11);
    return result;
  };
  let spare = null;
  const uniform = () => ((next() >>> 5) * 67108864 + (next() >>> 6)) / 9007199254740992;
  return {
    /** Uniform on [0, 1) with 53 random bits. */
    uniform,
    /** Uniform integer on {0, …, n − 1}. */
    integer: (n) => Math.floor(uniform() * n),
    /** Standard normal (Marsaglia's polar method). */
    normal() {
      if (spare !== null) {
        const value = spare;
        spare = null;
        return value;
      }
      let u;
      let v;
      let s;
      do {
        u = 2 * uniform() - 1;
        v = 2 * uniform() - 1;
        s = u * u + v * v;
      } while (s >= 1 || s === 0);
      const scale = Math.sqrt((-2 * Math.log(s)) / s);
      spare = v * scale;
      return u * scale;
    },
  };
}

/** Arithmetic mean. */
export function mean(xs) {
  let total = 0;
  for (const x of xs) total += x;
  return total / xs.length;
}

/** Sample standard deviation (divisor n − 1). */
export function sd(xs) {
  const m = mean(xs);
  let total = 0;
  for (const x of xs) total += (x - m) ** 2;
  return Math.sqrt(total / (xs.length - 1));
}

/** n evenly spaced points from lo to hi inclusive. */
export function linspace(lo, hi, n) {
  return Array.from({ length: n }, (_, i) => lo + ((hi - lo) * i) / (n - 1));
}

/** Distinct integers spaced evenly on a log scale from lo to hi inclusive (lo ≥ 1). */
export function logIntegers(lo, hi, perDecade = 20) {
  const out = new Set([lo, hi]);
  for (let e = Math.log10(lo); e <= Math.log10(hi) + 1e-9; e += 1 / perDecade) out.add(Math.round(10 ** e));
  return [...out].filter((n) => n >= lo && n <= hi).sort((x, y) => x - y);
}

/** Histogram of xs on equal-width bins over [lo, hi]; values outside are clamped into the end bins. */
export function histogram(xs, lo, hi, bins) {
  const width = (hi - lo) / bins;
  const counts = new Array(bins).fill(0);
  for (const x of xs) counts[Math.min(bins - 1, Math.max(0, Math.floor((x - lo) / width)))] += 1;
  return counts.map((count, i) => ({ x0: lo + i * width, x1: lo + (i + 1) * width, count }));
}
