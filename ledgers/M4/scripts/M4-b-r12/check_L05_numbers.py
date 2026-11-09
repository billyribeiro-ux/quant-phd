"""Independent recomputation of the L05 Lab 1 numbers (round 12, verifier slice b)."""
import math
import random

S1, S2, RHO, SEED = 0.02, 0.03, 0.6, 20260501


def draws(n, seed):
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        z1 = rng.gauss(0.0, 1.0)
        z2 = rng.gauss(0.0, 1.0)
        out.append((S1 * z1, S2 * (RHO * z1 + math.sqrt(1.0 - RHO * RHO) * z2)))
    return out


def cov(xs):
    n = len(xs)
    m1 = sum(x for x, _ in xs) / n
    m2 = sum(y for _, y in xs) / n
    s11 = sum((x - m1) ** 2 for x, _ in xs) / (n - 1)
    s22 = sum((y - m2) ** 2 for _, y in xs) / (n - 1)
    s12 = sum((x - m1) * (y - m2) for x, y in xs) / (n - 1)
    return [[s11, s12], [s12, s22]]


sigma = [[S1 * S1, RHO * S1 * S2], [RHO * S1 * S2, S2 * S2]]
print("sigma", sigma)
big = draws(20000, SEED)
for n in (100, 20000):
    s = cov(draws(n, SEED))
    err = max(abs(s[i][j] - sigma[i][j]) for i in range(2) for j in range(2))
    print("n", n, "s", s, "max_err", repr(err))
    if n == 100:
        for i, j in [(0, 0), (0, 1), (1, 1)]:
            print("  entry", i, j, "abs err", repr(abs(s[i][j] - sigma[i][j])))
s = cov(big)
print("E1 rel err s11 unrounded", repr((s[0][0] - sigma[0][0]) / sigma[0][0]))
print("E1 rel err printed s11", repr((0.00039491 - 0.0004) / 0.0004))
corr = s[0][1] / math.sqrt(s[0][0] * s[1][1])
print("corr", repr(corr), "err", repr(corr - RHO))
vals = []
for k in range(9):
    a = k * math.pi / 8
    w = (math.cos(a), math.sin(a))
    q = sum(w[i] * s[i][j] * w[j] for i in range(2) for j in range(2))
    vals.append(q)
    print("k", k, repr(q))
print("max k", vals.index(max(vals)), "min k", vals.index(min(vals)))
print("ratio max/min", repr(max(vals) / min(vals)), "round2", round(max(vals) / min(vals), 2))
print("ratio k3/k7", repr(vals[3] / vals[7]))
print("min quadratic sign all nonneg", all(v >= 0 for v in vals))
print("percentage variance factor", (100 * 0.02) ** 2 / 0.0004)
# Prefix property check
print("prefix", draws(100, SEED) == big[:100])
