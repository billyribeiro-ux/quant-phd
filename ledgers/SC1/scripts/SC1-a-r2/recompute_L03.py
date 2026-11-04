"""Round-2 independent recomputation of the L03 lab numbers and the L03 prose numbers.

Run: .venv/bin/python -I ledgers/SC1/scripts/SC1-a-r2/recompute_L03.py
The simulation draws come from one random.Random(SEED) in the order H = 1 then H = 2, and for each H the levels
k = 0..7, with 400 paths per level, each path drawing N Gaussian increments of variance H/N. The exact sums
use Fraction and the closed form H^4 (4N^2 - 1) / (3 N^3) is checked directly, not by the lab's function names.
"""

from __future__ import annotations

import math
import random
from fractions import Fraction as F

SEED = 20260503
PATHS = 400


def main() -> None:
    rng = random.Random(SEED)
    rows = []
    for H in (1.0, 2.0):
        for k in range(8):
            N = 2**k
            sd = math.sqrt(H / N)
            sums = []
            for _ in range(PATHS):
                acc = 0.0
                for _ in range(N):
                    x = rng.gauss(0.0, sd)
                    acc += x * x
                sums.append(acc)
            mean = sum(sums) / PATHS
            var = sum((s - mean) ** 2 for s in sums) / (PATHS - 1)
            se = math.sqrt(var / PATHS)
            z = (mean - H) / se
            pop_se = H * math.sqrt(2 / N) / 20
            rows.append((H, N, mean, se, z, pop_se))
            print(f"H={H:g} N={N:3d} mean={mean:.4f} se={se:.4f} z={z:.2f} pop_se={pop_se:.6f}")

    print("max |z| and the next largest:")
    zs = sorted(((abs(r[4]), r[0], r[1]) for r in rows), reverse=True)
    print("  largest", zs[0], "next", zs[1][0], "min over rows of |z| mean-H within 3 se:", all(abs(r[4]) <= 3 for r in rows))

    gaps = []
    for H, N, _mean, se, _z, pop in rows:
        gap = abs(se / pop - 1) * 100
        gaps.append((round(gap, 2), H, N, round(se, 4), round(pop, 6)))
    gaps.sort(reverse=True)
    print("largest relative gap between printed se and population se (percent, H, N, printed se, pop se):")
    for g in gaps[:4]:
        print("  ", g)

    print("H=1 N=1 pop se = sqrt(2)/20 =", round(math.sqrt(2) / 20, 4), "; H=2 N=128 pop se =", 2 * (1 / 8) / 20)

    # Exact sums: t^2 over equal partitions, Fraction arithmetic, closed form checked for each case.
    all_match = True
    for H in (F(1), F(2)):
        for k in range(8):
            N = 2**k
            pts = [H * j / N for j in range(N + 1)]
            total = sum(((pts[i + 1] ** 2 - pts[i] ** 2) ** 2 for i in range(N)), F(0))
            closed = H**4 * (4 * N * N - 1) / (3 * N**3)
            all_match &= total == closed
            if N in (2, 8, 128) or (H == F(1) and N == 1):
                print(f"exact H={H} N={N}: sum={total} ({float(total):.6f}) closed={closed}")
    print("exact closed form matches at all 16 levels:", all_match)
    print("recomputed: 4080/1536 =", F(4080, 1536), "; 16*255/1536 =", F(16 * 255, 1536))
    print("recomputed: 15/24 =", F(15, 24), "= 0.625")
    print("recomputed: E|Z| = 2 phi(0) = sqrt(2/pi) =", 2 / math.sqrt(2 * math.pi), math.sqrt(2 / math.pi))


if __name__ == "__main__":
    main()
