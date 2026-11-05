"""Independent recomputation of every number the SC1 project page prints or derives (verifier round 10).

Written from the page's stated conventions, not from the lab code: a different generator for the instance,
a different Simpson integrator, path maxima by cumulative sums, a dynamic program for the walk counts.
Run as: python -I recompute_r10.py
"""
import itertools
import math
import random

# instance (page section "Generated instances and the draw order")
def instance(seed):
    rng = random.Random(1_000_003 * seed + 54_321)
    H = round(rng.uniform(0.25, 4.0), 3)
    a = round(rng.uniform(0.25, 2.5), 3)
    n = rng.randint(4, 256)
    N = rng.randint(400, min(800, 200_000 // n))
    return H, a, n, N

H, a, n0, N = instance(0)
print("seed 0: H", H, "a", a, "N", N, "n_steps(make_instance)", n0)

# closed form, and an independent route through 1 - Phi
tail = math.erfc(a / math.sqrt(2 * H))
Phi = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
tail_phi = 2 * (1 - Phi(a / math.sqrt(H)))
print("tail erfc %.12f  via 2(1-Phi) %.12f  diff %.2e" % (tail, tail_phi, abs(tail - tail_phi)))

# composite trapezoid with Richardson (independent of the lab's Simpson rule)
def trap(level, horizon, m):
    top = level + 12 * math.sqrt(horizon)
    h = (top - level) / m
    f = lambda x: math.exp(-x * x / (2 * horizon)) / math.sqrt(2 * math.pi * horizon)
    s = 0.5 * (f(level) + f(top)) + sum(f(level + k * h) for k in range(1, m))
    return 2 * s * h
t1, t2 = trap(a, H, 20000), trap(a, H, 40000)
print("trapezoid 2P(B>=a): m=20000 %.12f  m=40000 %.12f  |richardson-trap - tail| %.2e" % (t2, t2, abs(2 * t2 - t1 - tail) if False else abs((4 * t2 - t1) / 3 - tail)))

# one-step: P(B_H >= a) estimate on N draws
rng = random.Random(0)
draws = [rng.gauss(0.0, math.sqrt(H)) for _ in range(N)]
hits1 = sum(1 for x in draws if x >= a)
p1 = hits1 / N
target = tail / 2
se_target = math.sqrt(target * (1 - target) / N)
band = 5 * se_target + 1 / N
se_sample = math.sqrt(p1 * (1 - p1) / (N - 1))
print("one-step hits", hits1, "estimate %.6f" % p1, "sample se %.6f" % se_sample)
print("target %.6f target se %.6f band %.6f" % (target, se_target, band))
print("tail minus estimate %.6f (printed 0.026948 in lab)" % (tail - p1))
print("estimate minus target %.6f inside band %s" % (p1 - target, abs(p1 - target) <= band))
print("0.016300/0.010735 = %.4f ; 0.016300/0.009218 = %.4f" % (0.016300 / 0.010735, 0.016300 / 0.009218))
print("64-step: 0.001799/0.012870 = %.4f" % (0.001799 / 0.012870))

# grid maxima by cumulative sums (independent of lab code): one stream, path by path, step by step
def grid_maxima(seed, H, N, n_fine):
    r = random.Random(seed)
    sd = math.sqrt(H / n_fine)
    out = []
    for _ in range(N):
        steps = [r.gauss(0.0, sd) for _ in range(n_fine)]
        out.append(list(itertools.accumulate(steps)))
    return out

for g in (1, 4, 16, 64, 256):
    paths = grid_maxima(0, H, N, g)
    hits = sum(1 for p in paths if max(p) >= a)
    est = hits / N
    se = math.sqrt(hits / N * (1 - hits / N) / (N - 1)) / 1.0
    se = math.sqrt(hits / N * (1 - hits / N) / (N - 1))
    print("grid %4d: hits %d est %.6f se %.6f  tail-est %.6f  |est-tail|/se %.2f"
          % (g, hits, est, se, tail - est, abs(est - tail) / se))

paths = grid_maxima(0, H, N, 256)
fine = sum(1 for p in paths if max(p) >= a)
for coarse_n in (64, 16, 4, 1):
    stride = 256 // coarse_n
    cnt = sum(1 for p in paths if max(p[stride - 1::stride]) >= a)
    print("nested coarse %3d: count %d, fine %d, coarse<=fine %s" % (coarse_n, cnt, fine, cnt <= fine))

# walk counts for n=12, a=3 by DP over (position, running max)
def dp_counts(n, lvl):
    states = {(0, 0): 1}  # (pos, max)
    for _ in range(n):
        nxt = {}
        for (pos, mx), c in states.items():
            for step in (1, -1):
                p2 = pos + step
                key = (p2, max(mx, p2))
                nxt[key] = nxt.get(key, 0) + c
        states = nxt
    total_max = sum(c for (pos, mx), c in states.items() if mx >= lvl)
    total_end = sum(c for (pos, mx), c in states.items() if pos >= lvl)
    return total_max, total_end

print("walk n=12 a=3 (DP): max>=3", dp_counts(12, 3)[0], " end>=3", dp_counts(12, 3)[1], " of", 2 ** 12)
print("walk n=6 a=2 (DP): max>=2", dp_counts(6, 2)[0], " end>=2", dp_counts(6, 2)[1], " end>=3", dp_counts(6, 3)[1])

# distinct levels and horizons over seeds 0-49
inst = [instance(s) for s in range(50)]
print("distinct levels seeds 0-49:", len({x[1] for x in inst}), " distinct horizons:", len({x[0] for x in inst}))
print("all steps in 4..256:", all(4 <= x[2] <= 256 for x in inst), " all N in 400..800:", all(400 <= x[3] <= 800 for x in inst),
      " max n*N:", max(x[2] * x[3] for x in inst))
