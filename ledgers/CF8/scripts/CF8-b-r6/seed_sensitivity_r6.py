"""Check the Section 3 claim 'a different seed would change the printed quantile and the printed counts' for seeds 0-9 (own code)."""
import random
def run(seed):
    rng = random.Random(seed)
    minima = []
    for _ in range(2000):
        flows = [rng.randint(-100000, 100000) for _ in range(12)]
        s = 0; lo = None
        for x in flows:
            s += x; lo = s if lo is None else min(lo, s)
        minima.append(lo)
    q = sorted(minima)[100 - 1]
    counts = tuple(sum(1 for m in minima if m < -b) for b in (0, 250000, 500000, 750000, 1000000, 1200000))
    return q, counts
base = run(2026)
for seed in range(10):
    q, c = run(seed)
    print("seed", seed, "q05", q, "counts", c, "differs from seed 2026 in quantile:", q != base[0], "in counts:", c != base[1])
print("seed 2026 check", base[0], base[1])
