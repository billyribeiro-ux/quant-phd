"""Round 8 (SC1-d): independent recomputation of every number the SC1 project page prints or quotes for seed 0.

Written from the page's specification text (instance draw order, gauss draw order, ddof-1 standard error), not from
the lab code. Prints the values the page quotes so they can be compared line by line.
"""
import itertools
import math
import random

# instance (spec: horizon, level, grid size, path count from random.Random(1_000_003 * seed + 54_321))
rng = random.Random(1_000_003 * 0 + 54_321)
H = round(rng.uniform(0.25, 4.0), 3)
a = round(rng.uniform(0.25, 2.5), 3)
n_steps = rng.randint(4, 256)
N = rng.randint(400, min(800, 200_000 // n_steps))
print(f"instance H={H} a={a} grid_size_drawn={n_steps} N={N}")
tail = math.erfc(a / math.sqrt(2 * H))
print(f"continuous tail erfc(a/sqrt(2H)) = {tail:.6f}")


def simpson_2_tail(level, horizon, m=20000):
    top = level + 14 * math.sqrt(horizon)
    h = (top - level) / m
    dens = lambda x: math.exp(-x * x / (2 * horizon)) / math.sqrt(2 * math.pi * horizon)
    s = dens(level) + dens(top) + sum((4 if k % 2 else 2) * dens(level + k * h) for k in range(1, m))
    return 2 * s * h / 3


quad = simpson_2_tail(a, H)
print(f"quadrature 2P(B_H>=a) = {quad:.6f}; |quad - tail| = {abs(quad - tail):.2e}")


def grid_hits(n, stride_list):
    """path-major draws, sd = sqrt(H/n); returns dict stride -> list of hit flags per path (max over k with k % s == 0)."""
    r = random.Random(0)
    sd = math.sqrt(H / n)
    out = {s: 0 for s in stride_list}
    for _ in range(N):
        pos = 0.0
        best = {s: -math.inf for s in stride_list}
        for k in range(1, n + 1):
            pos += r.gauss(0.0, sd)
            for s in stride_list:
                if k % s == 0 and pos > best[s]:
                    best[s] = pos
        for s in stride_list:
            if best[s] >= a:
                out[s] += 1
    return out


def se_of(hits):
    p = hits / N
    var = (N * p * (1 - p)) / (N - 1)  # sample variance of 0/1 indicators with ddof 1
    return p, math.sqrt(var) / math.sqrt(N)


p1, se1 = se_of(grid_hits(1, [1])[1])
target = tail / 2
tse = math.sqrt(target * (1 - target) / N)
band = 5 * tse + 1 / N
print(f"one step: p={p1:.6f} se={se1:.6f}; target={target:.6f} target_se={tse:.6f} band={band:.6f} diff={abs(p1-target):.6f}; inside={abs(p1-target)<=band}; diff/se_sample={abs(p1-target)/se1:.2f}; diff/target_se(=0.016300/0.010735 check)={(p1-target)/se1:.4f}")
for n in (4, 16, 64, 256):
    h = grid_hits(n, [1])[1]
    p, se = se_of(h)
    print(f"grid n={n}: hits={h} p={p:.6f} se={se:.6f} tail-p={tail-p:.6f} within5se={abs(tail-p)<=5*se}")
nest = grid_hits(256, [1, 4, 16, 64, 256])
fine = nest[1]
for s, c in ((4, 64), (16, 16), (64, 4), (256, 1)):
    print(f"nested stride {s}: coarse count {nest[s]} fine {fine} at_most={nest[s] <= fine}")
# walk counts
mx = 0
en = 0
for steps in itertools.product((1, -1), repeat=12):
    sums = list(itertools.accumulate(steps))
    mx += max(sums) >= 3
    en += sums[-1] >= 3
print(f"walk n=12 a=3: max>=3 {mx}, end>=3 {en}, total {2**12}")
# lab 2
mx6 = 0; e2 = 0; e3 = 0
for steps in itertools.product((1, -1), repeat=6):
    sums = list(itertools.accumulate(steps))
    mx6 += max(sums) >= 2
    e2 += sums[-1] >= 2
    e3 += sums[-1] >= 3
print(f"lab2 n=6 a=2: max>=2 {mx6}, end>=2 {e2}, end>=3 {e3}, identity {e2 + e3} == {mx6}: {mx6 == e2 + e3}")
