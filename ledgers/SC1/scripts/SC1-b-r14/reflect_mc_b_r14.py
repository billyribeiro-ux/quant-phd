"""SIMULATED supplementary check of Proposition 2.3 and Proposition 2.7 (round 14, SC1 slice b).

Seeded random walk on a grid of N steps on [0, 1] approximates Brownian motion. The grid version of the
reflected path reflects the grid path after the first grid index whose value is at least a. This is an
approximation of W at the continuous first passage time, so agreement is expected only to a few 1e-2.
It supports, and does not prove, the fixed-time law (Prop 2.3) and the two-time covariance (Prop 2.7).
Only the standard library is used. Seed 14, 20000 paths, N = 400, a = 0.5.
"""

from __future__ import annotations

import math
import random

SEED = 14
PATHS = 20000
N = 400
A = 0.5
DT = 1.0 / N
rng = random.Random(SEED)
sd = math.sqrt(DT)

b1_list: list[float] = []
w1_list: list[float] = []
bh_list: list[float] = []
wh_list: list[float] = []
hits = 0
for _ in range(PATHS):
    path = [0.0]
    for _k in range(N):
        path.append(path[-1] + sd * rng.gauss(0.0, 1.0))
    first = next((k for k in range(N + 1) if path[k] >= A), None)
    w = list(path)
    if first is not None:
        hits += 1
        for k in range(first, N + 1):
            w[k] = 2.0 * A - path[k]
    b1_list.append(path[N])
    w1_list.append(w[N])
    bh_list.append(path[N // 2])
    wh_list.append(w[N // 2])

print(f"SIMULATED seed={SEED} paths={PATHS} N={N} a={A}; paths reaching a on grid: {hits / PATHS:.4f}")


def mean(v: list[float]) -> float:
    return sum(v) / len(v)


def cov(x: list[float], y: list[float]) -> float:
    mx, my = mean(x), mean(y)
    return sum((a - mx) * (b - my) for a, b in zip(x, y, strict=True)) / (len(x) - 1)


for x in (-1.0, -0.5, 0.0, 0.5, 1.0):
    pb = sum(1 for v in b1_list if v <= x) / PATHS
    pw = sum(1 for v in w1_list if v <= x) / PATHS
    exact = 0.5 * math.erfc(-x / math.sqrt(2.0))
    print(f"P(B_1 <= {x:+.1f}) sim={pb:.4f} exact={exact:.4f} | P(W_1 <= {x:+.1f}) sim={pw:.4f}")
print(f"Var(B_1) sim={cov(b1_list, b1_list):.4f} (exact 1); Var(W_1) sim={cov(w1_list, w1_list):.4f} (exact 1)")
print(f"Cov(B_0.5, B_1) sim={cov(bh_list, b1_list):.4f} (exact 0.5); Cov(W_0.5, W_1) sim={cov(wh_list, w1_list):.4f} (exact 0.5)")
print(f"Var(W_0.5) sim={cov(wh_list, wh_list):.4f} (exact 0.5)")
