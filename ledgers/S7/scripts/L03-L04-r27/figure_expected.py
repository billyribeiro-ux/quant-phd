"""Independent Python port of the five L03/L04 figure computations (course/modules/S/S7/figures-L0{3,4}.js).

Written from the JS source in this checkout (pin 49def2c). Uses only the standard library and numpy for the
bootstrap sums. The JS random generator (stats.js rng: xoshiro128** seeded by splitmix32) is ported bit for bit,
so that seeded draws match the browser. Normal CDF/SF/PPF: the page's own approximations are ported where they
define the displayed numbers (upperTail, normPpf is taken from statistics.NormalDist, AS 241 as in the page).
JS toFixed rounding (ties go to the larger magnitude) is reproduced with Decimal.
"""

from __future__ import annotations

import math
from decimal import ROUND_HALF_UP, Decimal
from statistics import NormalDist

import numpy as np

M32 = 0xFFFFFFFF


def js_fixed(x: float, digits: int) -> str:
    if math.isnan(x):
        return "NaN"
    sign = "-" if x < 0 else ""
    d = Decimal(abs(x)).quantize(Decimal(1).scaleb(-digits), rounding=ROUND_HALF_UP)
    return sign + format(d, f".{digits}f")


def js_num(x: float) -> str:
    """String(Number(x.toFixed(d))) style: drops trailing zeros."""
    s = js_fixed(x, 2)
    return str(float(s)).rstrip("0").rstrip(".") if "." in str(float(s)) else str(float(s))


def js_round(x: float) -> int:
    return math.floor(x + 0.5)


# ---------------------------------------------------------------- stats.js rng (xoshiro128** + splitmix32)
class Rng:
    def __init__(self, seed: int) -> None:
        a = seed & M32

        def splitmix() -> int:
            nonlocal a
            a = (a + 0x9E3779B9) & M32
            t = a ^ (a >> 16)
            t = (t * 0x21F0AAAD) & M32
            t ^= t >> 15
            t = (t * 0x735A2D97) & M32
            return (t ^ (t >> 15)) & M32

        self.s0, self.s1, self.s2, self.s3 = splitmix(), splitmix(), splitmix(), splitmix()
        self.spare: float | None = None

    @staticmethod
    def rotl(x: int, k: int) -> int:
        return ((x << k) | (x >> (32 - k))) & M32

    def next(self) -> int:
        result = (self.rotl((self.s1 * 5) & M32, 7) * 9) & M32
        t = (self.s1 << 9) & M32
        self.s2 ^= self.s0
        self.s3 ^= self.s1
        self.s1 ^= self.s2
        self.s0 ^= self.s3
        self.s2 ^= t
        self.s3 = self.rotl(self.s3, 11)
        return result

    def uniform(self) -> float:
        return ((self.next() >> 5) * 67108864 + (self.next() >> 6)) / 9007199254740992

    def integer(self, n: int) -> int:
        return math.floor(self.uniform() * n)

    def normal(self) -> float:
        if self.spare is not None:
            v = self.spare
            self.spare = None
            return v
        while True:
            u = 2 * self.uniform() - 1
            v = 2 * self.uniform() - 1
            s = u * u + v * v
            if not (s >= 1 or s == 0):
                break
        scale = math.sqrt((-2 * math.log(s)) / s)
        self.spare = v * scale
        return u * scale


# ---------------------------------------------------------------- normal tails
def upper_tail_js(z: float) -> float:
    """stats.js upperTail: the page's rational approximation of 1 - Phi(z), z >= 0."""
    if z > 37:
        return 0.0
    e = math.exp((-z * z) / 2)
    if z < 7.07106781186547:
        n = 3.52624965998911e-2 * z + 0.700383064443688
        n = n * z + 6.37396220353165
        n = n * z + 33.912866078383
        n = n * z + 112.079291497871
        n = n * z + 221.213596169931
        n = n * z + 220.206867912376
        d = 8.83883476483184e-2 * z + 1.75566716318264
        d = d * z + 16.064177579207
        d = d * z + 86.7807322029461
        d = d * z + 296.564248779674
        d = d * z + 637.333633378831
        d = d * z + 793.826512519948
        d = d * z + 440.413735824752
        return (e * n) / d
    b = z + 0.65
    b = z + 4 / b
    b = z + 3 / b
    b = z + 2 / b
    b = z + 1 / b
    return e / b / 2.506628274631


def norm_sf_js(x: float) -> float:
    return upper_tail_js(x) if x >= 0 else 1 - upper_tail_js(-x)


def norm_cdf_js(x: float) -> float:
    tail = upper_tail_js(abs(x))
    return 1 - tail if x > 0 else tail


def norm_ppf(p: float) -> float:
    return NormalDist().inv_cdf(p)


# ---------------------------------------------------------------- multitest.js
def bonferroni(p: list[float], alpha: float) -> list[bool]:
    m = len(p)
    return [x <= alpha / m for x in p]


def argsort(xs: list[float]) -> list[int]:
    return [i for _, i in sorted([(x, i) for i, x in enumerate(xs)])]


def holm(p: list[float], alpha: float) -> dict:
    m = len(p)
    order = argsort(p)
    thr = [alpha / (m - j) for j in range(m)]
    stop = m + 1
    for j in range(m):
        if p[order[j]] > thr[j]:
            stop = j + 1
            break
    mask = [False] * m
    for j in range(stop - 1):
        mask[order[j]] = True
    return {"mask": mask, "thr": thr, "stop": stop}


def bh(p: list[float], q: float) -> dict:
    m = len(p)
    order = argsort(p)
    lines = [((j + 1) * q) / m for j in range(m)]
    k_star = 0
    for j in range(m):
        if p[order[j]] <= lines[j]:
            k_star = j + 1
    mask = [False] * m
    for j in range(k_star):
        mask[order[j]] = True
    return {"mask": mask, "k_star": k_star, "lines": lines}


def by(p: list[float], q: float) -> dict:
    c = 0.0
    for j in range(1, len(p) + 1):
        c += 1 / j
    r = bh(p, q / c)
    r["c"] = c
    return r


def store_pi0(p: list[float], lam: float) -> float:
    return sum(1 for x in p if x > lam) / ((1 - lam) * len(p))


def storey_moments(m0: int, m1: int, lam: float, tail: float) -> dict:
    scale = (1 - lam) * (m0 + m1)
    return {
        "mean": (m0 * (1 - lam) + m1 * tail) / scale,
        "leak": (m1 * tail) / scale,
        "sd": math.sqrt(m0 * (1 - lam) * lam + m1 * tail * (1 - tail)) / scale,
    }


# ---------------------------------------------------------------- L03 figures
EXAMPLE = [0.001, 0.008, 0.012, 0.021, 0.024, 0.046, 0.06, 0.074, 0.205, 0.212]


def bh_expected(q: float, fwer: bool, byon: bool) -> dict:
    m = len(EXAMPLE)
    r_bh = bh(EXAMPLE, q)
    hm = holm(EXAMPLE, q)
    bonf = sum(bonferroni(EXAMPLE, q))
    r_by = by(EXAMPLE, q)
    carried = [k for k in range(1, m + 1) if k <= r_bh["k_star"] and EXAMPLE[k - 1] > r_bh["lines"][k - 1]]
    H = sum(hm["mask"])
    desc = (
        f"The ten sorted p-values of Example 2.2 plotted against their rank k, with the BH line k·q/m at q = {js_fixed(q, 3)}. "
        + ("No p-value lies on or under the line, so BH rejects nothing. " if r_bh["k_star"] == 0 else
           f"The largest rank whose p-value lies on or under the line is k* = {r_bh['k_star']}, so BH rejects "
           + ("the smallest p-value" if r_bh["k_star"] == 1 else f"the {r_bh['k_star']} smallest p-values")
           + (f", including rank {' and '.join(map(str, carried))}, which lies above its own line but is carried by the step-up. " if carried else ". ")))
    desc += f"Holm rejects {H} and Bonferroni {bonf}."
    readout = (
        f"q = {js_fixed(q, 3)}: BH rejects {r_bh['k_star']} of {m}"
        + (f" (rank {', '.join(map(str, carried))} sits above its own line and is carried by the step-up)" if carried else "")
        + f"; Holm rejects {H}; Bonferroni rejects {bonf}"
        + (f"; Benjamini–Yekutieli (Section 5) rejects {sum(r_by['mask'])} (c(10) = {js_fixed(r_by['c'], 3)})" if byon else "")
        + "."
    )
    return {"readout": readout, "desc": desc, "bh_rejects": r_bh["k_star"], "holm": H, "bonf": bonf, "by_rejects": sum(r_by["mask"]), "c10": r_by["c"]}


def pvalue_sample(seed: int) -> list[float]:
    g = Rng(seed)
    out = []
    for i in range(1000):
        if i < 800:
            out.append(g.uniform())
        else:
            out.append(norm_sf_js(3 + g.normal()))
    return out


def pi0_moments(lam: float) -> dict:
    return storey_moments(800, 200, lam, norm_cdf_js(norm_ppf(1 - lam) - 3))


def pvalue_expected(seed: int, lam: float) -> dict:
    p = pvalue_sample(seed)
    above = sum(1 for x in p if x > lam)
    pi0 = store_pi0(p, lam)
    mo = pi0_moments(lam)
    leak_dom = mo["leak"] > mo["sd"]
    median_flag = " (a median draw at λ = 0.5)" if (seed == 22 and abs(lam - 0.5) < 1e-9) else ""
    readout = (
        f"Sample {seed}{median_flag}: {above} of 1000 p-values exceed λ = {js_fixed(lam, 2)}, "
        f"so the estimate is π0(λ) = {above} / ({js_fixed(1 - lam, 2)} × 1000) = {js_fixed(pi0, 3)}, against the true π0 = 0.800. "
        f"At this λ the effects that land past it raise the estimate by {js_fixed(mo['leak'], 4)} on average, "
        f"{'more than' if leak_dom else 'less than'} the sampling noise (sd {js_fixed(mo['sd'], 4)})."
    )
    desc = (
        "A SIMULATED histogram of 1,000 one-sided p-values: 800 true nulls, uniform on (0, 1), and 200 effects of mean 3, "
        f"which pile up near zero. To the right of λ = {js_fixed(lam, 2)} the null p-values form a flat floor at the true share of nulls, 0.8, "
        f"and the effects that land past λ add {js_fixed(mo['leak'], 4)} to it on average, {'more' if leak_dom else 'less'} than the sampling noise (sd {js_fixed(mo['sd'], 4)}); "
        f"the estimate of π0 at λ, {js_fixed(pi0, 3)}, is the average height of the bars to the right of λ."
    )
    return {"readout": readout, "desc": desc, "above": above, "pi0": pi0, "leak": mo["leak"], "sd": mo["sd"]}


# ---------------------------------------------------------------- L04 figures
BLOCK_N = 20
BLOCK_CHOICES = [1, 2, 4, 8, 20]


def stationary_bootstrap(n: int, mean_block: float, gen: Rng) -> tuple[list[int], list[bool]]:
    p = 1 / mean_block
    idx = [0] * n
    starts = [False] * n
    idx[0] = gen.integer(n)
    starts[0] = True
    for t in range(1, n):
        if gen.uniform() < p:
            idx[t] = gen.integer(n)
            starts[t] = True
        else:
            idx[t] = (idx[t - 1] + 1) % n
    return idx, starts


def block_draw(seed: int, b: int) -> tuple[list[int], list[dict]]:
    idx, starts = stationary_bootstrap(BLOCK_N, b, Rng((seed * 7919 + b) & M32 if False else seed * 7919 + b))
    blocks: list[dict] = []
    for t in range(BLOCK_N):
        if starts[t]:
            blocks.append({"start": t, "from": idx[t], "length": 0, "wraps": False})
        blk = blocks[-1]
        if blk["length"] and idx[t] == 0:
            blk["wraps"] = True
        blk["length"] += 1
    return idx, blocks


def blocks_expected(seed: int, b: int) -> dict:
    idx, blocks = block_draw(seed, b)
    nb = len(blocks)
    lst = ", ".join(f"{k['from']}→{(k['from'] + k['length'] - 1) % BLOCK_N}" for k in blocks)
    exp = js_num(1 + (BLOCK_N - 1) / b)
    median_flag = " (a median draw at b = 4)" if (seed == 2 and b == 4) else ""
    readout = (
        f"Resample {seed}{median_flag}, b = {b}: {nb} block{'' if nb == 1 else 's'} "
        f"(expected 1 + {BLOCK_N - 1}/{b} = {exp}), mean length {js_fixed(BLOCK_N / nb, 1)}: {lst}."
    )
    wraps_here = any(k["wraps"] for k in blocks)
    desc = (
        f"The top row is an original sample of {BLOCK_N} observations, shaded from faint (index 0) to strong (index {BLOCK_N - 1}). "
        f"The bottom row is one resample with mean block length {b}: each cell copies the original observation of the same shade. "
        f"It has {nb} block{'' if nb == 1 else 's'}; within a block the shade strengthens one step at a time, and a block that runs past index {BLOCK_N - 1} "
        f"wraps to index 0{', as happens here' if wraps_here else ''}."
    )
    return {"readout": readout, "desc": desc, "blocks": nb, "indices": idx}


AR_N = 500
LOG_EXP = 0.0


def log_integers(lo: int, hi: int, per_decade: int = 20) -> list[int]:
    out = {lo, hi}
    e = math.log10(lo)
    lim = math.log10(hi) + 1e-9
    while e <= lim:
        out.add(js_round(10 ** e))
        e += 1 / per_decade
    return sorted(n for n in out if lo <= n <= hi)


def ar1_autocov(seed: int, phi: float) -> list[float]:
    g = Rng(seed * 1000 + js_round(phi * 100))
    x = [0.0] * AR_N
    x[0] = g.normal() / math.sqrt(1 - phi * phi)
    for t in range(1, AR_N):
        x[t] = phi * x[t - 1] + g.normal()
    m = sum(v / AR_N for v in x)
    d = np.array(x) - m
    out = []
    for h in range(AR_N):
        out.append(float(np.dot(d, np.roll(d, -h))) / AR_N)
    return out


def boot_var_of_mean(c: list[float], b: float) -> float:
    n = len(c)
    keep = 1 - 1 / b
    total = c[0]
    w = 1.0
    for h in range(1, n):
        w *= keep
        total += 2 * (1 - h / n) * w * c[h]
    return total / n


def variance_expected(seed: int, phi: float) -> dict:
    c = ar1_autocov(seed, phi)
    long_run = 1 / (1 - phi) ** 2
    pts = [(b, math.sqrt((AR_N * boot_var_of_mean(c, b)) / long_run)) for b in log_integers(1, AR_N, 30)]
    best = pts[0]
    for p in pts[1:]:
        if p[1] > best[1]:
            best = p
    first = pts[0][1]
    last = pts[-1][1]
    median_flag = " (a typical draw at ϕ = 0.5)" if (seed == 186 and abs(phi - 0.5) < 1e-9) else ""
    readout = (
        f"ϕ = {js_fixed(phi, 1)}, sample {seed}{median_flag}: the bootstrap gives {js_fixed(100 * first, 0)}% of the true "
        f"standard error at b = 1, {js_fixed(100 * best[1], 0)}% at its best (b ≈ {best[0]}) and {js_fixed(100 * last, 0)}% at b = {AR_N}."
    )
    desc = (
        f"For one SIMULATED AR(1) sample of {AR_N} observations with ϕ = {js_fixed(phi, 1)}, the exact bootstrap standard error of the mean from formula (2), "
        f"as a fraction of the true long-run standard error, against the mean block length on a log scale. It is {js_fixed(first, 2)} at b = 1 (the iid bootstrap), "
        f"peaks at {js_fixed(best[1], 2)} near b = {best[0]}, and is {js_fixed(last, 2)} at b = {AR_N}."
    )
    return {"readout": readout, "desc": desc, "first": first, "best": best, "last": last}


RC_T, RC_B, RC_K = 500, 1000, 110


def universe(seed: int) -> dict:
    g = Rng(seed)
    d = np.empty((RC_T, RC_K))
    for t in range(RC_T):
        for k in range(RC_K):
            d[t, k] = g.normal() + (3 / math.sqrt(RC_T) if k == 0 else (-0.25 if k >= 10 else 0.0))
    means = d.mean(axis=0)
    sds = d.std(axis=0, ddof=1)
    boot = np.empty((RC_B, RC_K))
    for bidx in range(RC_B):
        idx, _ = stationary_bootstrap(RC_T, 10, g)
        boot[bidx] = d[np.array(idx)].mean(axis=0)
    return {"means": means, "sds": sds, "boot": boot}


def rc_spa(u: dict, k: int) -> dict:
    root = math.sqrt(RC_T)
    means, sds, boot = u["means"], u["sds"], u["boot"]
    v = max(root * means[j] for j in range(k))
    t_obs = max(0.0, max((root * means[j]) / sds[j] for j in range(k)))
    thr = math.sqrt((2 * math.log(math.log(RC_T))) / RC_T)
    centre = [means[j] if means[j] <= -sds[j] * thr else 0.0 for j in range(k)]
    rc = np.max(root * (boot[:, :k] - means[:k]), axis=1)
    spa = np.maximum(0.0, np.max(root * (boot[:, :k] - means[:k] + np.array(centre)) / sds[:k], axis=1))
    p_rc = float(np.mean(rc >= v))
    p_spa = float(np.mean(spa >= t_obs))
    return {"v": v, "tObs": t_obs, "pRc": p_rc, "pSpa": p_spa, "recentred": sum(1 for c in centre if c != 0), "rc": rc, "spa": spa}


def rc_desc(now: dict, base: dict, poor: int) -> str:
    def recentred_by(n: int) -> str:
        return " and recentring" if n else ""
    intro = (
        f"SIMULATED universe of ten strategies, one with a true edge, plus {poor} poor strategies. Each test reads its own observed statistic against its own null: "
        f"the Reality Check's maximum √T·d̄ is {js_fixed(now['v'], 2)}, and the SPA-style maximum, studentized by each strategy's standard deviation, is {js_fixed(now['tObs'], 2)}. "
    )
    if poor == 0:
        if now["pRc"] == now["pSpa"]:
            pair = (f"With no poor strategies both p-values are {js_fixed(now['pRc'], 3)}: in this universe studentization{recentred_by(now['recentred'])} "
                    f"{'do' if now['recentred'] else 'does'} not change the share of resamples at or above the observed statistic. ")
        else:
            pair = (f"With no poor strategies the Reality Check's p-value is {js_fixed(now['pRc'], 3)} and the SPA-style p-value {js_fixed(now['pSpa'], 3)}; they differ because the SPA-style statistic is studentized"
                    + (f" and keeps {now['recentred']} strateg{'y' if now['recentred'] == 1 else 'ies'} below its threshold at {'its' if now['recentred'] == 1 else 'their'} own mean{'' if now['recentred'] == 1 else 's'}" if now["recentred"] else "")
                    + ". ")
        return intro + pair + "Adding poor strategies tends to raise the Reality Check's p-value, because each is recentred at zero and competes for the maximum."
    if now["pRc"] == base["pRc"]:
        rc = f"The Reality Check's p-value stays at {js_fixed(now['pRc'], 3)}: recentred at zero, the poor strategies lift no further resample's maximum to the observed V. "
    else:
        rc = f"The Reality Check's p-value goes from {js_fixed(base['pRc'], 3)} with no poor strategies to {js_fixed(now['pRc'], 3)}, because every poor strategy is recentred at zero and competes for the maximum. "
    escaped = poor - now["recentred"] + base["recentred"]
    if now["pSpa"] != base["pSpa"]:
        spa = (f"The SPA-style p-value moves from {js_fixed(base['pSpa'], 3)} to {js_fixed(now['pSpa'], 3)}, because {escaped} poor strateg"
               + ("y escapes" if escaped == 1 else "ies escape") + " the recentring threshold.")
    else:
        spa = f"The SPA-style p-value stays at {js_fixed(now['pSpa'], 3)}."
    return intro + rc + spa


def rc_expected(seed: int, poor: int, u: dict | None = None) -> dict:
    u = u or universe(seed)
    now = rc_spa(u, 10 + poor)
    base = rc_spa(u, 10)
    median_flag = " (a median draw)" if (seed == 2001 and poor == 0) else ""
    readout = (
        f"Universe {seed}{median_flag}, {poor} poor strategies: Reality Check p = {js_fixed(now['pRc'], 3)}; "
        f"SPA-style p = {js_fixed(now['pSpa'], 3)}, with {now['recentred']} of {10 + poor} strategies recentred at their own means."
    )
    return {"readout": readout, "desc": rc_desc(now, base, poor), "pRc": now["pRc"], "pSpa": now["pSpa"], "recentred": now["recentred"]}
