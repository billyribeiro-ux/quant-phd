"""SC1-a round 17: own check of the L03 q8 explanation bound 4 H^3 |P| (Proposition 2.4(a)) and the
sum of squared increments of s -> s^2 on [0, H] over random partitions. Run: python3 -I this_file.
"""

import random

rng = random.Random(17)
worst = 0.0
for trial in range(2000):
    H = rng.choice([0.5, 1.0, 2.0, 3.7])
    n = rng.randint(1, 60)
    cuts = sorted(rng.uniform(0, H) for _ in range(n - 1))
    pts = [0.0] + cuts + [H]
    total = sum((b * b - a * a) ** 2 for a, b in zip(pts, pts[1:], strict=False))
    mesh = max(b - a for a, b in zip(pts, pts[1:], strict=False))
    bound = 4 * H**3 * mesh * (len(pts) - 1)  # 4 H^3 |P| with |P| = number of intervals
    worst = max(worst, total / bound)
print("max ratio sum/(4 H^3 |P|) over 2000 random partitions:", round(worst, 6), "(must be <= 1)")
# mesh-scaling: uniform partitions into N steps, sum ~ 2 H^3 ... compare to mesh H/N
for H in (1.0, 2.0):
    for N in (4, 16, 64, 256):
        pts = [H * i / N for i in range(N + 1)]
        total = sum((b * b - a * a) ** 2 for a, b in zip(pts, pts[1:], strict=False))
        print(f"H={H} N={N} sum={total:.6f} bound 4H^3|P|={4 * H**3 * N:.3f} sum/mesh={total / (H / N):.6f}")
