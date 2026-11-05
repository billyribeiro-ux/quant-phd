"""Independent recomputation (round 9, SC1 slice d) of every number printed by Labs 1 and 3 and quoted in the
project page, the exemplars and the interpretation paragraphs. Standard library only. Written from the page's
specification, not from the lab code.

Usage: python -I recompute_r9.py
"""

import math
import random
from statistics import NormalDist

# Instance of seed 0, drawn in the page's fixed order.
rng = random.Random(1_000_003 * 0 + 54_321)
H = round(rng.uniform(0.25, 4.0), 3)
a = round(rng.uniform(0.25, 2.5), 3)
n_steps0 = rng.randint(4, 256)
N = rng.randint(400, min(800, 200_000 // n_steps0))
print(f"instance: H={H} a={a} N={N} (first grid size drawn {n_steps0})")

# Continuous tail, two ways.
tail = math.erfc(a / math.sqrt(2 * H))
tail_ncdf = 2 * (1 - NormalDist(0, math.sqrt(H)).cdf(a))
print(f"tail erfc={tail:.10f} via normal cdf={tail_ncdf:.10f} diff={abs(tail - tail_ncdf):.3e}")
print(f"tail rounded 6dp={tail:.6f}; half tail={tail / 2:.10f} rounded={tail / 2:.6f}")

# Simpson quadrature of 2 P(B_H >= a) with 20000 intervals, independent code.
def dens(x):
    return math.exp(-x * x / (2 * H)) / math.sqrt(2 * math.pi * H)

top = a + 14 * math.sqrt(H)
n_int = 20000
h = (top - a) / n_int
s = dens(a) + dens(top)
for k in range(1, n_int):
    s += (4 if k % 2 else 2) * dens(a + k * h)
quad = 2 * s * h / 3
print(f"quadrature={quad:.10f} |quad-tail|={abs(quad - tail):.3e}")

# One-step: P(B_H >= a) estimate from N draws of N(0,H) in order random.Random(0).gauss.
def one_step(seed, n_paths, level, horizon):
    r = random.Random(seed)
    ind = [1.0 if r.gauss(0.0, math.sqrt(horizon)) >= level else 0.0 for _ in range(n_paths)]
    m = sum(ind) / n_paths
    var = sum((x - m) ** 2 for x in ind) / (n_paths - 1)
    return m, math.sqrt(var) / math.sqrt(n_paths), sum(ind)

p1, se1, hits1 = one_step(0, N, a, H)
target = tail / 2
tse = math.sqrt(target * (1 - target) / N)
band = 5 * tse + 1 / N
print(f"one-step hits={hits1:.0f} est={p1:.6f} sample_se={se1:.6f} target={target:.6f} target_se={tse:.6f} band={band:.6f} diff={abs(p1 - target):.6f} inside={abs(p1 - target) <= band}")
print(f"diff/sample_se={abs(p1 - target) / se1:.4f} diff/target_se={abs(p1 - target) / tse:.4f}")
print(f"tail minus one-step estimate (page sign) = {tail - p1:.6f}; sampling error of bias estimate vs target bias = {(tail - p1) - target:.6f}")
print(f"0.016300/0.010735 = {0.016300 / 0.010735:.4f}; 0.016300/0.009218 = {0.016300 / 0.009218:.4f}; 0.001799/0.012870 = {0.001799 / 0.012870:.4f}")
print(f"target_se rounded 6dp: {tse:.6f}; 0.009218 matches: {round(tse, 6) == 0.009218}")

# Grid estimates on separate paths: path by path, step by step, from random.Random(0).
def grid_maxima(seed, n_paths, n_fine, strides):
    r = random.Random(seed)
    sd = math.sqrt(H / n_fine)
    out = {s: [] for s in strides}
    for _ in range(n_paths):
        pos = 0.0
        best = {s: -math.inf for s in strides}
        for k in range(1, n_fine + 1):
            pos += r.gauss(0.0, sd)
            for s in strides:
                if k % s == 0:
                    best[s] = max(best[s], pos)
        for s in strides:
            out[s].append(best[s])
    return out

for n in (1, 4, 16, 64, 256):
    m = grid_maxima(0, N, n, (1,))[1]
    hits = sum(1 for x in m if x >= a)
    est = hits / N
    ind = [1.0 if x >= a else 0.0 for x in m]
    mean = sum(ind) / N
    var = sum((x - mean) ** 2 for x in ind) / (N - 1)
    se = math.sqrt(var) / math.sqrt(N)
    print(f"grid n={n:3d}: hits={hits} est={est:.6f} se={se:.6f} tail-minus-est={tail - est:.6f} (|tail-est|/se={abs(tail - est) / se:.2f})")

# Nested counts on the 256-step paths; strides 1,4,16,64,256 give 256,64,16,4,1 steps.
nest = grid_maxima(0, N, 256, (1, 4, 16, 64, 256))
fine = sum(1 for x in nest[1] if x >= a)
for coarse_n, s in ((64, 4), (16, 16), (4, 64), (1, 256)):
    c = sum(1 for x in nest[s] if x >= a)
    print(f"nested coarse n={coarse_n} count={c} fine={fine} coarse<=fine {c <= fine}")

# Exact walk counts for n = 12, a = 3 by counting over binomial coefficients (independent of enumeration).
n, lev = 12, 3
ends_ge = sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= lev)
ends_ge_a1 = sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= lev + 1)
print(f"walk n=12 a=3: ends>=3 {ends_ge}, max>=3 (reflection) {ends_ge + ends_ge_a1}, total walks {2 ** n}")

# Enumeration cross-check of the same walk counts.
import itertools
mx = 0
ed = 0
for steps in itertools.product((1, -1), repeat=n):
    s_ = 0
    top_ = -10**9
    for st in steps:
        s_ += st
        top_ = max(top_, s_)
    mx += top_ >= lev
    ed += s_ >= lev
print(f"enumeration: max>=3 {mx} ends>=3 {ed}")
