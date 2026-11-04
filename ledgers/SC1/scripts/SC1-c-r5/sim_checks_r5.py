"""Independent check of the seeded simulations printed on L07 Part B/C (nesting violations) and L08 Part C (z values).

Run: python -I -W error ledgers/SC1/scripts/SC1-c-r5/sim_checks_r5.py
"""

from __future__ import annotations

import math
import random
from fractions import Fraction


def l07_nesting() -> None:
    rng = random.Random(20260507)
    fine = 256
    grids = (4, 16, 64, 256)
    viol = 0
    counts = {n: 0 for n in grids}
    for _ in range(400):
        path = [0.0]
        for _ in range(fine):
            path.append(path[-1] + rng.gauss(0.0, math.sqrt(1.0 / fine)))
        gm = {}
        for n in grids:
            gm[n] = max(path[j] for j in range(0, fine + 1, fine // n))
            counts[n] += gm[n] >= 1.0
        for c, f in zip(grids, grids[1:]):
            viol += gm[c] > gm[f]
    print("L07 nesting violations (coarse above fine):", viol)
    print("L07 counts reaching level 1:", counts)


def l08_partc() -> None:
    rng = random.Random(20260508)
    steps = 256
    paths = []
    for _ in range(1000):
        pos = 0
        first = steps
        for k in range(1, steps + 1):
            pos += 1 if rng.random() < 0.5 else -1
            if pos >= 1:
                first = k
                break
        paths.append(first)
    # exact truncated means by fraction DP: P(nu_1 > k) = P(max_{j<=k} S_j < 1)
    dist = {0: Fraction(1)}  # position -> probability, walks not yet at level 1
    survive = []
    for k in range(256):
        survive.append(sum(dist.values()))
        nxt: dict[int, Fraction] = {}
        for pos, p in dist.items():
            for s in (1, -1):
                q = pos + s
                if q >= 1:
                    continue
                nxt[q] = nxt.get(q, Fraction(0)) + p / 2
        dist = nxt
    for n in (16, 64, 256):
        exact = sum(survive[:n])
        vals = [min(c, n) for c in paths]
        mu = sum(vals) / len(vals)
        var = sum((v - mu) ** 2 for v in vals) / (len(vals) - 1)
        se = math.sqrt(var / len(vals))
        print(f"L08 C N={n}: sample mean {mu:.4f} se {se:.4f} exact {float(exact):.6f} z {(mu - float(exact)) / se:+.4f}")


if __name__ == "__main__":
    l07_nesting()
    l08_partc()
