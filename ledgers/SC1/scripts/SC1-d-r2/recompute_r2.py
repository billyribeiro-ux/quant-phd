"""Independent recomputation of every number on project.html for seed 0 (own code, not the labs' code), with unrounded values."""

from __future__ import annotations

import itertools
import math
import random
import sys
from fractions import Fraction

sys.setrecursionlimit(10000)


def instance(seed: int) -> dict[str, float | int]:
    rng = random.Random(1_000_003 * seed + 54_321)
    h = round(rng.uniform(0.25, 4.0), 3)
    a = round(rng.uniform(0.25, 2.5), 3)
    n = rng.randint(4, 256)
    paths = rng.randint(400, min(800, 200_000 // n))
    return {"H": h, "a": a, "n": n, "N": paths}


def tail_exact_check(a: float, h: float) -> float:
    # erfc via the exact relation 2(1 - Phi(a/sqrt h)) computed with math.erf (independent path)
    return 2.0 * (1.0 - 0.5 * (1.0 + math.erf((a / math.sqrt(h)) / math.sqrt(2.0))))


inst = instance(0)
H, a, N = inst["H"], inst["a"], inst["N"]
print("H, a, N, n_steps(seed0 drawn grid size):", H, a, N, inst["n"])
tail = math.erfc(a / math.sqrt(2 * H))
print(f"tail unrounded {tail!r}  6dp {tail:.6f}")
print(f"tail/2 unrounded {tail / 2!r}  6dp {tail / 2:.6f}")
print(f"tail via 2(1-Phi) {tail_exact_check(a, H)!r} diff {abs(tail_exact_check(a, H) - tail):.3e}")

# Simpson on 2 P(B_H >= a), independent: 20000 panels over [a, a + 14 sqrt(H)]
top = a + 14 * math.sqrt(H)
m = 20000
hstep = (top - a) / m
s = 0.0
for k in range(m + 1):
    x = a + k * hstep
    w = 1 if k in (0, m) else (4 if k % 2 else 2)
    s += w * math.exp(-x * x / (2 * H))
quad = 2 * s * hstep / 3 / math.sqrt(2 * math.pi * H)
print(f"quadrature(20000 panels) {quad!r} diff from tail {abs(quad - tail):.3e}")

# one-step estimate with the lab's draw order (one gauss per path, sd sqrt(H)), N paths
rng = random.Random(0)
ind = [1.0 if rng.gauss(0.0, math.sqrt(H)) >= a else 0.0 for _ in range(N)]
p = sum(ind) / N
var = sum((x - p) ** 2 for x in ind) / (N - 1)
se = math.sqrt(var) / math.sqrt(N)
target = tail / 2
band = 5 * se + 1 / N
print(f"one-step p {p!r} se {se!r} target {target!r} band {band!r} diff {abs(p - target)!r}")
print(f"  rounded: p {p:.6f} se {se:.6f} target {target:.6f} band {band:.6f} diff {abs(p - target):.6f} inside {abs(p-target)<=band}")
print(f"  diff in SE units {abs(p - target) / se:.4f}")

# grid estimates (reference order: path by path, step by step)
def grid_maxima(n_fine: int) -> list[float]:
    rng = random.Random(0)
    sd = math.sqrt(H / n_fine)
    out = []
    for _ in range(N):
        pos = 0.0
        best = -math.inf
        for _ in range(n_fine):
            pos += rng.gauss(0.0, sd)
            best = max(best, pos)
        out.append(best)
    return out

rows = {}
for n in (1, 4, 16, 64, 256):
    mx = grid_maxima(n)
    hits = sum(1 for v in mx if v >= a)
    p = hits / N
    se = math.sqrt(N * p * (1 - p) / (N - 1)) / math.sqrt(N)
    rows[n] = (hits, p, se, tail - p)
    print(f"grid n={n}: hits {hits} p {p!r} se {se!r} tail-p {tail - p!r}  | 6dp p {p:.6f} se {se:.6f} tail-p {tail - p:.6f}")

# nested on the 256-step paths: coarse maxima on every s-th point
rng = random.Random(0)
sd = math.sqrt(H / 256)
fine = 0
coarse_counts = {s: 0 for s in (4, 16, 64, 256)}
for _ in range(N):
    pos = 0.0
    best_fine = -math.inf
    best = {s: -math.inf for s in coarse_counts}
    for k in range(1, 257):
        pos += rng.gauss(0.0, sd)
        best_fine = max(best_fine, pos)
        for s in coarse_counts:
            if k % s == 0:
                best[s] = max(best[s], pos)
    fine += best_fine >= a
    for s in coarse_counts:
        coarse_counts[s] += best[s] >= a
print("nested fine(256)", fine, "coarse by stride", coarse_counts, "(stride 4 = 64 steps, 16 = 16 steps, 64 = 4 steps, 256 = 1 step)")

# walk counts n=12, a=3 by enumeration (independent), and identity check
mx = en = 0
for steps in itertools.product((1, -1), repeat=12):
    s = list(itertools.accumulate(steps))
    mx += max(s) >= 3
    en += s[-1] >= 3
print("walk n=12 a=3: max>=3", mx, "end>=3", en, "of", 2**12)
# Lab 2: n=6, a=2
mx = en = en1 = 0
for steps in itertools.product((1, -1), repeat=6):
    s = list(itertools.accumulate(steps))
    mx += max(s) >= 2
    en += s[-1] >= 2
    en1 += s[-1] >= 3
print("lab2 n=6 a=2: max>=2", mx, "end>=2", en, "end>=3", en1, "identity", en + en1)
