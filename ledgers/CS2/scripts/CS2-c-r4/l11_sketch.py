"""Verifier round 4: independent re-implementation of the L11 compactor sketch from Definition 2.1 (no code copied
from the twin), with exact-rank checks. Reports stored items, compactions, weight, and the printed-style excess.
Also runs the 39- and 40-value cases of problems E1 and M3 (ε = 1/10)."""
import bisect
import math
import random
from fractions import Fraction


def make(eps):
    levels = []  # levels[h] = list of stored values at weight 2**h
    stats = {"compactions": 0}

    def k(h):
        return 2 * math.ceil(Fraction((h + 1) * (h + 2), 2) / eps)

    def push(h, y):
        while len(levels) <= h:
            levels.append([])
        levels[h].append(y)
        if len(levels[h]) == k(h):
            ordered = sorted(levels[h])
            kept = [ordered[i] for i in range(1, len(ordered), 2)]  # 2nd, 4th, ... (1-based)
            levels[h] = []
            stats["compactions"] += 1
            for z in kept:
                push(h + 1, z)

    def add(x):
        push(0, x)

    return levels, add, stats, k


def weights(levels):
    return sum(len(b) * 2**h for h, b in enumerate(levels))


def quantile(levels, n, q):
    pairs = sorted((v, 2**h) for h, b in enumerate(levels) for v in b)
    cum = 0
    for v, w in pairs:
        cum += w
        if cum >= q * n:
            return v


# E1 / M3 cases at eps = 1/10
for count in (39, 40):
    levels, add, stats, k = make(Fraction(1, 10))
    rng = random.Random(7)
    for _ in range(count):
        add(rng.random())
    print("eps 1/10, n =", count, "stored", sum(len(b) for b in levels), "per level", [len(b) for b in levels],
          "weight", weights(levels), "compactions", stats["compactions"])

# lab case eps = 1/20 and 1/10, N = 5000, seed 2026 (same seed as the twin; values from random.Random(2026).random())
N = 5000
for eps in (Fraction(1, 20), Fraction(1, 10)):
    levels, add, stats, k = make(eps)
    rng = random.Random(2026)
    xs = [rng.random() for _ in range(N)]
    for x in xs:
        add(x)
    ordered = sorted(xs)
    worst_excess = 0.0
    worst_def = 0.0
    ok = True
    for qf in (Fraction(0), Fraction(1, 100), Fraction(1, 10), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4),
               Fraction(9, 10), Fraction(99, 100), Fraction(1)):
        v = quantile(levels, N, qf)
        below = bisect.bisect_left(ordered, v)
        atb = bisect.bisect_right(ordered, v)
        ok &= below <= qf * N + eps * N and atb >= qf * N - eps * N
        worst_excess = max(worst_excess, float((below - qf * N) / N))
        worst_def = max(worst_def, float((qf * N - atb) / N))
    print("eps", eps, "stored", sum(len(b) for b in levels), "compactions", stats["compactions"], "weight", weights(levels),
          "all pass", ok, "excess %.4f" % worst_excess, "deficit %.4f" % worst_def, "capacities", [k(h) for h in range(3)])
