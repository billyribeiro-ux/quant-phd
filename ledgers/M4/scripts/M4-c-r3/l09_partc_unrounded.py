"""Unrounded Part C estimates of lab-M4-L09-1 (same seeds and draws as the twin), for the basis check of E2."""
import math, random, statistics
phi1 = statistics.NormalDist().cdf(1.0)
SEED, REP, MU, SIG = 2026, 4000, 3.5, math.sqrt(35 / 12)
for n in (5, 30, 200):
    rng = random.Random(SEED)
    hits = 0
    for _ in range(REP):
        total = sum(rng.randint(1, 6) for _ in range(n))
        z = (total / n - MU) / (SIG / math.sqrt(n))
        hits += z <= 1.0
    p = hits / REP
    se = math.sqrt(p * (1 - p) / REP)
    print(f"n={n} hits={hits} p={p:.5f} se={se:.6f} gap={p - phi1:+.6f} gap/se={(p - phi1) / se:.3f}")
