"""Independent re-derivation (SC1-c round 2) of every number on L07 and L08 pages.

Written from the mathematics, not copied from the lab twins: DP over walk positions with exact Fractions,
direct enumeration, and an independent re-simulation of the seeded paths with the same draw order.
Usage: python -I numbers_r2.py
"""

from __future__ import annotations

import math
import random
from fractions import Fraction
from itertools import product

out: list[str] = []


def emit(line: str) -> None:
    out.append(line)
    print(line)


# ---------- L07 Part A: exact tails by binomial sums, and the walk identity by brute force ----------
def count_endpoint_ge(n: int, m: int) -> int:
    # number of length-n sequences with S_n >= m, S_n = 2u - n, u = number of up steps
    total = 0
    for u in range(n + 1):
        if 2 * u - n >= m:
            total += math.comb(n, u)
    return total


def count_max_ge_bruteforce(n: int, m: int) -> int:
    hits = 0
    for steps in product((1, -1), repeat=n):
        s = 0
        top = 0
        for x in steps:
            s += x
            top = max(top, s)
        hits += top >= m
    return hits


identity_ok = 0
identity_total = 0
for n in range(1, 13):
    for m in range(1, n + 1):
        identity_total += 1
        brute = count_max_ge_bruteforce(n, m)
        identity_ok += brute == count_endpoint_ge(n, m) + count_endpoint_ge(n, m + 1)
emit(f"L07 Part A walk identity by brute force: {identity_ok} of {identity_total}; pairs sum n = {sum(range(1,13))}")

for n in (4, 16, 64, 256, 1024):
    m = math.isqrt(n)
    p = Fraction(count_endpoint_ge(n, m) + count_endpoint_ge(n, m + 1), 2**n)
    emit(f"L07 exact tail N={n} m={m}: {float(p):.10f} (fraction {p.numerator}/{p.denominator})")

# L07 E2 numbers: S16>=4 and S16>4
ge4 = count_endpoint_ge(16, 4)
gt4 = count_endpoint_ge(16, 5)
emit(f"L07 E2: #S16>=4 = {ge4}, #S16>4 = {gt4}, total {ge4 + gt4}, ratio {(ge4 + gt4) / 2**16:.9f}")
emit(f"L07 E2 terms: {[math.comb(16, u) for u in range(10, 17)]}")

# L07 E3: standard error of proportion 121/400 with divisor n-1
k, n = 121, 400
emit(f"L07 E3: k(n-k) = {k * (n - k)}, n^2(n-1) = {n * n * (n - 1)}, se = {math.sqrt(k * (n - k) / (n * n * (n - 1))):.6f}")
emit(f"L07 E1: 0.2275*400 = {0.2275 * 400:.6f}, 0.3025*400 = {0.3025 * 400:.6f}")

# ---------- closed forms ----------
def phi_cdf(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


two_one_minus_phi1 = 2.0 * (1.0 - phi_cdf(1.0))
emit(f"2(1-Phi(1)) = {two_one_minus_phi1:.12f}; erfc(1/sqrt2) = {math.erfc(1 / math.sqrt(2)):.12f}")
emit(f"1-Phi(1) = {1 - phi_cdf(1.0):.12f}; 2*0.1586552539 = {2 * 0.1586552539:.10f}")
emit(f"sqrt(2/pi) = {math.sqrt(2 / math.pi):.10f}")
emit(f"0.3173105 tolerance check |0.3173105-2(1-Phi(1))| = {abs(0.3173105 - two_one_minus_phi1):.3e}")
emit(f"0.158655 tolerance check |0.158655-(1-Phi(1))| = {abs(0.158655 - (1 - phi_cdf(1.0))):.3e}")
emit(f"0.797885 tolerance check |0.797885-sqrt(2/pi)| = {abs(0.797885 - math.sqrt(2 / math.pi)):.3e}")

# ---------- L07 Part B and C: independent re-simulation with the same draw order ----------
SEED = 20260507
PATHS = 400
FINE = 256
GRIDS = (4, 16, 64, 256)
rng = random.Random(SEED)
sd = math.sqrt(1.0 / FINE)
per_grid: dict[int, list[float]] = {g: [] for g in GRIDS}
violations = 0
for _ in range(PATHS):
    # independent construction: explicit loop over increments
    values = [0.0]
    level = 0.0
    for _j in range(FINE):
        level += rng.gauss(0.0, sd)
        values.append(level)
    maxima_here = {}
    for g in GRIDS:
        step = FINE // g
        best = -math.inf
        for j in range(0, FINE + 1, step):
            best = max(best, values[j])
        maxima_here[g] = best
        per_grid[g].append(best)
    for coarse, fine in zip(GRIDS, GRIDS[1:]):
        violations += maxima_here[coarse] > maxima_here[fine]
emit(f"L07 Part B re-sim: nesting violations = {violations}")
closed = 2.0 * (1.0 - phi_cdf(1.0))
for g in GRIDS:
    ind = [1.0 if v >= 1.0 else 0.0 for v in per_grid[g]]
    mean = sum(ind) / PATHS
    var = sum((x - mean) ** 2 for x in ind) / (PATHS - 1)
    se = math.sqrt(var / PATHS)
    emit(f"L07 Part B re-sim N={g}: count={int(sum(ind))} p={mean:.4f} se={se:.4f} diff={mean - closed:+.4f}")
target = math.sqrt(2 / math.pi)
for g in GRIDS:
    xs = per_grid[g]
    mean = sum(xs) / PATHS
    var = sum((x - mean) ** 2 for x in xs) / (PATHS - 1)
    se = math.sqrt(var / PATHS)
    emit(f"L07 Part C re-sim N={g}: mean={mean:.4f} se={se:.4f} diff={mean - target:+.4f}")
emit(f"L07 finest gap / se(256) = {(target - sum(per_grid[256]) / PATHS) / math.sqrt(sum((x - sum(per_grid[256]) / PATHS) ** 2 for x in per_grid[256]) / (PATHS - 1) / PATHS):.3f}")

# Simpson check of 1-Phi(1)
def dens(x: float) -> float:
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)


def simpson(a: float, b: float, n: int) -> float:
    h = (b - a) / n
    s = dens(a) + dens(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * dens(a + i * h)
    return s * h / 3


emit(f"L07 Part D: Simpson 1..13 = {simpson(1.0, 13.0, 2000):.12f}; erfc = {0.5 * math.erfc(1 / math.sqrt(2)):.12f}")

# ---------- L08 Part A: first passage counts by enumeration (independent: DP over first hit) ----------
def first_hit_counts(n: int, a: int) -> dict[int, int]:
    # DP over (position, hit yet?) for paths that have not yet reached a; count first hit step k
    counts: dict[int, int] = {}
    alive: dict[int, int] = {0: 1}
    for k in range(1, n + 1):
        nxt: dict[int, int] = {}
        hit_now = 0
        for pos, c in alive.items():
            for step in (1, -1):
                q = pos + step
                if q >= a:
                    hit_now += c
                else:
                    nxt[q] = nxt.get(q, 0) + c
        if hit_now:
            counts[k] = hit_now * 2 ** (n - k)  # steps after the first hit are free
        alive = nxt
    return counts


fh = first_hit_counts(12, 3)
emit(f"L08 Part A first-hit counts a=3 n=12 k=3..12: {[fh.get(k, 0) for k in range(3, 13)]}")
emit(f"L08 Part A sum = {sum(fh.values())}; P = {sum(fh.values())}/4096 = {sum(fh.values()) / 4096:.6f}")
ge3 = sum(math.comb(12, u) for u in range(13) if 2 * u - 12 >= 3)
emit(f"L08 Part A #S12>=3 = {ge3}; /4096 = {ge3 / 4096:.6f}")

# sequences checked
seq_total = 0
for n in range(1, 13):
    seq_total += n * 2**n
emit(f"L08 Part A sequences = sum n*2^n for n=1..12 = {seq_total}")

# pathwise agreement: kappa_a <= n iff max >= a, checked by brute force over all sequences
agree = 0
checked = 0
for n in range(1, 13):
    for a in range(1, n + 1):
        for steps in product((1, -1), repeat=n):
            s = 0
            top = 0
            hit = False
            for x in steps:
                s += x
                top = max(top, s)
                if s >= a:
                    hit = True
            checked += 1
            agree += hit == (top >= a)
emit(f"L08 Part A pathwise agreement brute force: {agree} of {checked}")

# ---------- L08 Part B: exact truncated means via DP on the walk (independent of Fraction tail formula) ----------
def truncated_mean(a: int, horizon: int) -> Fraction:
    # E[min(kappa, N)] = sum_{k=1}^{N} P(kappa >= k) = sum_{k=0}^{N-1} P(kappa > k)
    # P(kappa > k) = P(max_{j<=k} S_j < a) computed by DP keeping only paths still below a
    total = Fraction(0)
    alive: dict[int, int] = {0: 1}  # position -> count, paths with max < a so far (k = 0 included)
    for k in range(0, horizon):
        survive = sum(alive.values())
        total += Fraction(survive, 2**k)  # P(kappa > k)
        nxt: dict[int, int] = {}
        if k + 1 < horizon:
            for pos, c in alive.items():
                for step in (1, -1):
                    q = pos + step
                    if q < a:
                        nxt[q] = nxt.get(q, 0) + c
        alive = nxt
    return total


for h in (16, 64, 256):
    m = truncated_mean(1, h)
    emit(f"L08 Part B E[min(kappa_1,{h})] = {float(m):.9f}")

# ---------- L08 Part C: independent re-simulation (same draw order: one rng.random per step) ----------
SIM_SEED = 20260508
rng2 = random.Random(SIM_SEED)
capped: list[int] = []
for _ in range(1000):
    pos = 0
    first = 256
    for k in range(1, 257):
        pos += 1 if rng2.random() < 0.5 else -1
        if pos >= 1:
            first = k
            break
    capped.append(first)
for h in (16, 64, 256):
    xs = [min(c, h) for c in capped]
    mean = sum(xs) / len(xs)
    var = sum((x - mean) ** 2 for x in xs) / (len(xs) - 1)
    se = math.sqrt(var / len(xs))
    exact = float(truncated_mean(1, h))
    emit(f"L08 Part C re-sim N={h}: mean={mean:.4f} se={se:.4f} exact={exact:.4f} z={(mean - exact) / se:+.2f}")

# ---------- L08 Part D ----------
def fp_cdf(a: float, t: float) -> float:
    return math.erfc(a / math.sqrt(2 * t))


def fp_density(a: float, t: float) -> float:
    return a / (math.sqrt(2 * math.pi) * t ** 1.5) * math.exp(-a * a / (2 * t))


for t in (1.0, 2.0):
    h = 1e-5
    cd = (fp_cdf(1.0, t + h) - fp_cdf(1.0, t - h)) / (2 * h)
    emit(f"L08 Part D a=1 t={t:g}: cdf={fp_cdf(1.0, t):.10f} density={fp_density(1.0, t):.10f} "
         f"central={cd:.10f} diff={abs(cd - fp_density(1.0, t)):.2e}")
emit(f"L08 M2 f_1(1) = {1 / math.sqrt(2 * math.pi) * math.exp(-0.5):.10f}")
emit(f"L08 E3 t^-3/2 = {2 ** -1.5:.6f}, e^-1/4 = {math.exp(-0.25):.6f}, product {fp_density(1.0, 2.0):.6f}")
emit(f"L08 mode check: a^2/3 = {1 / 3:.6f}")

with open("ledgers/SC1/scripts/SC1-c-r2/out/numbers_r2.out", "w", encoding="utf-8") as fh_out:
    fh_out.write("\n".join(out) + "\n")
