"""Verifier round 6 (SC1 slice d): independent recomputation of every number in project.html's project labs and prose.

Written from the page's stated rules, not copied from the lab twins. Uses only the standard library.
Prints each quantity with full precision, the six-decimal rounding the page prints, and the ratios quoted in prose.
"""

import itertools
import math
import random
from statistics import NormalDist

PHI = NormalDist()


def instance(seed):
    r = random.Random(1_000_003 * seed + 54_321)
    h = round(r.uniform(0.25, 4.0), 3)
    a = round(r.uniform(0.25, 2.5), 3)
    steps = r.randint(4, 256)
    paths = r.randint(400, min(800, 200_000 // steps))
    return h, a, steps, paths


H, A, NSTEP, N = instance(0)
print(f"seed-0 instance: H={H!r} a={A!r} n_steps={NSTEP} N={N}  (page: H = 2.083, a = 2.474, N = 487)")

# Continuous tail by erfc and by the exact normal law (independent route).
tail = math.erfc(A / math.sqrt(2 * H))
tail_normal = 2 * (1 - PHI.cdf(A / math.sqrt(H)))
print(f"tail erfc = {tail!r}  -> {tail:.6f}")
print(f"tail via NormalDist = {tail_normal!r}  |difference| = {abs(tail - tail_normal):.3e}")

# Simpson's rule on 2 P(B_H >= a) with 20000 panels, independently written.
def simpson(lo, hi, f, n=20000):
    h = (hi - lo) / n
    s = f(lo) + f(hi) + sum((4 if k % 2 else 2) * f(lo + k * h) for k in range(1, n))
    return s * h / 3

dens = lambda x: math.exp(-x * x / (2 * H)) / math.sqrt(2 * math.pi * H)
quad = 2 * simpson(A, A + 14 * math.sqrt(H), dens)
print(f"Simpson 2P(B_H>=a) = {quad!r}  |quad - tail| = {abs(quad - tail):.3e}  (page: 9.13e-15 printed)")

target = tail / 2
print(f"target tail/2 = {target!r} -> {target:.6f}  (page: 0.043248)")
print(f"tail/2 = {target:.7f} exact digits check")

# Paths: one gauss per step, path by path, step by step, from random.Random(seed).
def grid_max_hits(n_steps, level=A):
    r = random.Random(0)
    hits = 0
    sd = math.sqrt(H / n_steps)
    maxima = []
    for _ in range(N):
        pos = 0.0
        best = -math.inf
        for _k in range(n_steps):
            pos += r.gauss(0.0, sd)
            best = max(best, pos)
        maxima.append(best)
        hits += best >= level
    return hits, maxima

def est_se(hits, n):
    p = hits / n
    var = (hits * (1 - p) ** 2 + (n - hits) * p * p) / (n - 1)  # sample variance of 0/1 values
    return p, math.sqrt(var) / math.sqrt(n)

print("grid rows (n, hits, estimate, se, tail - estimate):")
rows = {}
for n in (1, 4, 16, 64, 256):
    hits, _ = grid_max_hits(n)
    p, se = est_se(hits, N)
    rows[n] = (hits, p, se)
    print(f"  n={n:3d} hits={hits:3d} est={p:.6f} se={se:.6f} tail-est={tail - p:.6f} within5se={abs(tail-p) <= 5*se}")
ses = [rows[n][2] for n in rows]
print(f"  se range over the five grids: {min(ses):.6f} .. {max(ses):.6f}  (page: 0.009819 to 0.012870)")

# One-step check: estimate vs target band 5 sqrt(p(1-p)/N) + 1/N.
h1, p1, se1 = rows[1]
tse = math.sqrt(target * (1 - target) / N)
band = 5 * tse + 1 / N
print(f"one step: est-target = {p1 - target:.6f} (page 0.016300); band = {band:.6f} (page 0.048142); "
      f"ratio to se = {(p1 - target) / se1:.4f} (page 1.52)")
print(f"ratio 64-step tail-est to its se: {(tail - rows[64][1]) / rows[64][2]:.4f} (page 0.14 from 0.001799/0.012870)")

# Nested counts on the 256-step paths: coarse grids are every (256/n)-th point.
r = random.Random(0)
sd = math.sqrt(H / 256)
fine_paths = []
for _ in range(N):
    pos = 0.0
    vals = []
    for _k in range(256):
        pos += r.gauss(0.0, sd)
        vals.append(pos)
    fine_paths.append(vals)
fine = sum(max(v) >= A for v in fine_paths)
print(f"nested fine count (256 steps) = {fine} (page 40)")
for coarse_n in (64, 16, 4, 1):
    stride = 256 // coarse_n
    c = sum(max(v[stride - 1::stride]) >= A for v in fine_paths)
    print(f"  coarse n={coarse_n} count={c} at_most_fine={c <= fine}")

# Exact walk counts by the binomial route (independent of enumeration) and by enumeration.
def walks_ge(n, a):
    return sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= a)

n12 = 12
max12 = walks_ge(n12, 3) + walks_ge(n12, 4)
end12 = walks_ge(n12, 3)
print(f"n=12, a=3: reflection max count = {max12} (page 1588), end count = {end12} (page 794)")
enum_max = sum(1 for s in itertools.product((1, -1), repeat=12) if max(itertools.accumulate(s)) >= 3)
enum_end = sum(1 for s in itertools.product((1, -1), repeat=12) if sum(s) >= 3)
print(f"n=12, a=3 by enumeration: max={enum_max} end={enum_end}")
print(f"n=6, a=2: max={walks_ge(6,2)+walks_ge(6,3)} end>=2={walks_ge(6,2)} end>=3={walks_ge(6,3)} (page 29, 22, 7)")
enum6 = sum(1 for s in itertools.product((1, -1), repeat=6) if max(itertools.accumulate(s)) >= 2)
print(f"n=6, a=2 by enumeration of maxima: {enum6}")

# Scope check of prose: the claim 0.0865 for tail; 0.0595 estimate; 0.0107 se; 0.0163 / 0.0107
print(f"exemplar A ratio 0.0163/0.0107 = {0.0163/0.0107:.4f}")
print(f"exemplar B: 0.016300/0.010735 = {0.016300/0.010735:.4f}")
print(f"exemplar B: 0.026948 + 0.016300 = {0.026948 + 0.016300:.6f} vs tail/2 {target:.6f}")

# Lab 2 seed-free identity check for n=6..8 (the identity the lab checks) and n = 12 range.
bad = []
for n in range(1, 13):
    for a in range(1, n + 1):
        mx = sum(1 for s in itertools.product((1, -1), repeat=n) if max(itertools.accumulate(s)) >= a)
        if mx != walks_ge(n, a) + walks_ge(n, a + 1):
            bad.append((n, a))
print("reflection identity failures for n<=12:", bad)
