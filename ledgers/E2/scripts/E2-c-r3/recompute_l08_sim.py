"""Independent re-implementation of the L08 seeded simulation (verifier, round 3)."""
import random, math
from fractions import Fraction as F

def sim(shade, seed=20261028, N=20000, n=5, a=2000, lo=5000, hi=15000):
    rng = random.Random(seed)
    profits = []
    for _ in range(N):
        v = rng.randint(lo, hi)
        sig = [v + rng.randint(-a, a) for _ in range(n)]
        bids = [s - shade for s in sig]
        order = sorted(range(n), key=lambda i: (-bids[i], i))
        w = order[0]
        profits.append(v - bids[w])
    return profits

def se_total(p):
    N = len(p)
    num = N * sum(x * x for x in p) - sum(p) ** 2
    return math.floor(math.sqrt(num / (N - 1)) + 0.5)

naive = sim(0); shaded = sim(1334)
print("naive total", sum(naive), "se", se_total(naive))
print("shaded total", sum(shaded), "se", se_total(shaded))
print("shaded - naive", sum(shaded) - sum(naive), "== 1334*20000:", sum(shaded) - sum(naive) == 1334 * 20000)
exact_naive = F(-20000) * F(85418692002000, 64048012001)
print("exact naive", float(exact_naive), "diff in SE:", (sum(naive) - float(exact_naive)) / se_total(naive))
