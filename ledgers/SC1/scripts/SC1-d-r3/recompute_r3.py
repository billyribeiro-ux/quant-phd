"""Independent recomputation of every number the SC1 project page quotes (stdlib only, own code, not the lab's).

Usage: python recompute_r3.py   (prints the values to six places and the derived figures)
"""

from __future__ import annotations

import itertools
import math
import random

# seed-0 instance, drawn in the page's order from random.Random(1_000_003 * seed + 54_321)
rng = random.Random(1_000_003 * 0 + 54_321)
H = round(rng.uniform(0.25, 4.0), 3)
a = round(rng.uniform(0.25, 2.5), 3)
n_steps = rng.randint(4, 256)
N = rng.randint(400, min(800, 200_000 // n_steps))
print(f"instance: H={H} a={a} n_steps={n_steps} N={N}")

tail = math.erfc(a / math.sqrt(2 * H))
print(f"tail erfc(a/sqrt(2H)) = {tail:.6f} (unrounded {tail!r})")
print(f"tail/2 = {tail / 2:.6f}")

# Simpson on N(0,H) density, independent grid
def dens(x: float) -> float:
    return math.exp(-x * x / (2 * H)) / math.sqrt(2 * math.pi * H)

top = a + 12 * math.sqrt(H)
m = 4000
h = (top - a) / m
s = dens(a) + dens(top) + sum((4 if k % 2 else 2) * dens(a + k * h) for k in range(1, m))
quad = 2 * s * h / 3
print(f"quadrature = {quad:.6f}, |quad - tail| = {abs(quad - tail):.2e}")

# one-step estimate with the seeded draws
r = random.Random(0)
ind = [1.0 if r.gauss(0.0, math.sqrt(H)) >= a else 0.0 for _ in range(N)]
p1 = sum(ind) / N
var1 = sum((x - p1) ** 2 for x in ind) / (N - 1)
se1 = math.sqrt(var1) / math.sqrt(N)
target = tail / 2
print(f"one-step: p={p1:.6f} se={se1:.6f} hits={int(sum(ind))}")
print(f"target={target:.6f} band={5 * se1 + 1 / N:.6f} |p-target|={abs(p1 - target):.6f} ratio_se={abs(p1 - target) / se1:.3f}")
print(f"tail - p (full tail, as Lab 3 prints it for n=1) = {tail - p1:.6f}")

# grid estimates on paths drawn path-by-path, step-by-step, with sd = sqrt(H/n)
def grid_max_paths(n: int) -> list[float]:
    r2 = random.Random(0)
    sd = math.sqrt(H / n)
    out = []
    for _ in range(N):
        pos = 0.0
        best = -math.inf
        for _ in range(n):
            pos += r2.gauss(0.0, sd)
            best = max(best, pos)
        out.append(best)
    return out

for n in (1, 4, 16, 64, 256):
    mx = grid_max_paths(n) if n != 1 else None
    if n == 1:
        hits = sum(1 for _ in [0])  # placeholder replaced below
        r3 = random.Random(0)
        sd = math.sqrt(H)
        hits = sum(1 for _ in range(N) if r3.gauss(0.0, sd) >= a)
    else:
        hits = sum(1 for v in mx if v >= a)
    p = hits / N
    se = math.sqrt(p * (1 - p) / (N - 1)) * 1.0
    se = math.sqrt(N * p * (1 - p) / (N - 1)) / math.sqrt(N)
    print(f"grid n={n}: hits={hits} p={p:.6f} se={se:.6f} tail-p={tail - p:.6f} se_gap_ratio={abs(tail - p) / se:.3f}")

# nested: 256-step paths, coarse grids every (256/n)-th point
r4 = random.Random(0)
sd256 = math.sqrt(H / 256)
paths = []
for _ in range(N):
    pos = 0.0
    vals = []
    for _ in range(256):
        pos += r4.gauss(0.0, sd256)
        vals.append(pos)
    paths.append(vals)
fine = sum(1 for v in paths if max(v) >= a)
for coarse in (64, 16, 4, 1):
    st = 256 // coarse
    c = sum(1 for v in paths if max(v[st - 1 :: st]) >= a)
    print(f"nested fine={fine} coarse n={coarse} count={c} le_fine={c <= fine}")

# walks: n=12, a=3 by enumeration
mx_hits = end_hits = 0
for steps in itertools.product((1, -1), repeat=12):
    sums = list(itertools.accumulate(steps))
    mx_hits += max(sums) >= 3
    end_hits += sums[-1] >= 3
print(f"walks n=12 a=3: max>=3 {mx_hits}, end>=3 {end_hits}, total {2**12}")

# Lab 2: n=6, a=2
def counts(n: int, a_: int) -> tuple[int, int]:
    mh = eh = 0
    for steps in itertools.product((1, -1), repeat=n):
        sums = list(itertools.accumulate(steps))
        mh += max(sums) >= a_
        eh += sums[-1] >= a_
    return mh, eh

mh, eh = counts(6, 2)
_, e3 = counts(6, 3)
print(f"n=6 a=2: max {mh}, end>=2 {eh}, end>=3 {e3}, identity {eh + e3}")
