"""Independent recomputation of every number on the SC1 project page (VERIFIER_RULES 2.2 and 2.6).

Written from the page's text (project.html, Rung 3 'Generated instances and the draw order'), not from lab code.
Prints the values with the rounding the page uses, so each prose figure can be compared.
"""

from __future__ import annotations

import itertools
import math
import random
from statistics import NormalDist


def make_instance(seed: int) -> tuple[float, float, int, int]:
    rng = random.Random(1_000_003 * seed + 54_321)
    horizon = round(rng.uniform(0.25, 4.0), 3)
    level = round(rng.uniform(0.25, 2.5), 3)
    n_steps = rng.randint(4, 256)
    n_paths = rng.randint(400, min(800, 200_000 // n_steps))
    return horizon, level, n_steps, n_paths


def tail(a: float, t: float) -> float:
    return math.erfc(a / math.sqrt(2.0 * t))


def gauss_tail_normaldist(a: float, t: float) -> float:
    return 2.0 * (1.0 - NormalDist(0.0, math.sqrt(t)).cdf(a))


def grid_hits(H: float, a: float, N: int, n: int, seed: int) -> int:
    rng = random.Random(seed)
    sd = math.sqrt(H / n)
    hits = 0
    for _ in range(N):
        pos = 0.0
        best = -math.inf
        for _ in range(n):
            pos += rng.gauss(0.0, sd)
            best = max(best, pos)
        hits += best >= a
    return hits


def se_of(hits: int, N: int) -> float:
    p = hits / N
    var = N * p * (1 - p) / (N - 1)
    return math.sqrt(var) / math.sqrt(N)


H, a, n_steps, N = make_instance(0)
print(f"instance seed 0: H={H} a={a} n_steps={n_steps} N={N}")
T = tail(a, H)
print(f"tail erfc = {T!r} -> {T:.6f}")
print(f"tail via NormalDist = {gauss_tail_normaldist(a, H)!r}, diff {abs(gauss_tail_normaldist(a, H) - T):.2e}")
target = T / 2
print(f"target tail/2 = {target!r} -> {target:.6f}")
hits1 = grid_hits(H, a, N, 1, 0)
p1 = hits1 / N
se1 = se_of(hits1, N)
print(f"n=1: hits={hits1} p={p1!r} se={se1!r}")
band = 5 * se1 + 1 / N
print(f"band 5se+1/N = {band!r} -> {band:.6f}; |p - target| = {abs(p1 - target)!r} -> {abs(p1 - target):.6f}")
print(f"|p - target| / se = {abs(p1 - target) / se1:.3f}; inside band: {abs(p1 - target) <= band}")
print(f"tail - p1 = {T - p1:.6f}")
for n in (4, 16, 64, 256):
    h = grid_hits(H, a, N, n, 0)
    print(f"n={n}: hits={h} p={h / N:.6f} se={se_of(h, N):.6f} tail-p={T - h / N:.6f} within5se={abs(T - h / N) <= 5 * se_of(h, N)}")

# Nested counts on the 256-step paths (same draws as the page's Lab 3 construction: path by path, step by step).
rng = random.Random(0)
sd = math.sqrt(H / 256)
paths = []
for _ in range(N):
    pos = 0.0
    vals = []
    for _ in range(256):
        pos += rng.gauss(0.0, sd)
        vals.append(pos)
    paths.append(vals)
fine = sum(max(v) >= a for v in paths)
for coarse in (64, 16, 4, 1):
    stride = 256 // coarse
    c = sum(max(v[stride - 1 :: stride]) >= a for v in paths)
    print(f"nested coarse n={coarse}: count {c}, fine {fine}, coarse<=fine {c <= fine}")

# Walk counts, exact.
def walk(n: int, level: int) -> tuple[int, int]:
    mx = en = 0
    for steps in itertools.product((1, -1), repeat=n):
        s = list(itertools.accumulate(steps))
        mx += max(s) >= level
        en += s[-1] >= level
    return mx, en

print("walk n=12 a=3 (max, end):", walk(12, 3), "2^12 =", 2**12)
print("walk n=6 a=2 (max, end, end>=3):", walk(6, 2), walk(6, 3)[1])

# Decimal checks quoted in prose (exemplar B and project page).
print(f"1.5 se check: {0.0163 / 0.010735:.3f}")
print(f"64-step gap 0.001799 / se 0.012870 = {0.001799 / 0.012870:.3f}")
print(f"seed-0 horizon-range: H in [0.25,4.0]: {0.25 <= H <= 4.0}, a in [0.25,2.5]: {0.25 <= a <= 2.5}")
print(f"erfc(0)={math.erfc(0.0)}")
