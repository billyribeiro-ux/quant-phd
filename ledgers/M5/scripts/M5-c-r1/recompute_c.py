"""Independent recomputation for M5 slice c (L08-L10), round 1. Run: .venv/bin/python -I ledgers/M5/scripts/M5-c-r1/recompute_c.py

Re-derives the displayed numbers of L08, L09 and L10 from first principles (no lab code imported).
"""

from __future__ import annotations

import math
from fractions import Fraction

# ---- L08: grid operator on (0.25, 0.5, 0.75, 1.0), alpha = 1/2, beta = 0.9, u = sqrt
ALPHA = 0.5
GRID = (0.25, 0.5, 0.75, 1.0)


def feas(k: float) -> list[int]:
    out = k**ALPHA
    return [j for j, kp in enumerate(GRID) if kp <= out]


def bop(v: list[float], beta: float) -> list[float]:
    return [max(math.sqrt(k**ALPHA - GRID[j]) + beta * v[j] for j in feas(k)) for k in GRID]


def solve(beta: float, tol: float = 1e-12) -> tuple[list[float], int, list[list[float]]]:
    v = [0.0] * 4
    seq = [v]
    n = 0
    while True:
        nv = bop(v, beta)
        n += 1
        seq.append(nv)
        gap = max(abs(a - b) for a, b in zip(nv, v))
        v = nv
        if gap <= tol:
            return v, n, seq


v09, n09, seq09 = solve(0.9)
print("L08 count beta=0.9", n09, "V*", [round(x, 6) for x in v09])
print("L08 count beta=0.5", solve(0.5)[1], "beta=0.95", solve(0.95)[1])
print("L08 1/ln(1/beta) at 0.5,0.9,0.95", [round(1 / math.log(1 / b), 4) for b in (0.5, 0.9, 0.95)])
print("L08 E2 check: 0.5-state consumption utility", round(math.sqrt(0.5**ALPHA - 0.25), 6), "+4.5 =", round(math.sqrt(0.5**ALPHA - 0.25) + 4.5, 6))
print("L08 Example 1.2 sqrt(0.75)", round(math.sqrt(0.75), 6))

# worst sampled contraction ratio, full precision (seeded like the lab, recomputed here)
import random  # noqa: E402

rng = random.Random(20261028)
worst = 0.0
for _ in range(2000):
    v = [rng.uniform(-10, 10) for _ in GRID]
    w = [rng.uniform(-10, 10) for _ in GRID]
    bv, bw = bop(v, 0.9), bop(w, 0.9)
    worst = max(worst, max(abs(a - b) for a, b in zip(bv, bw)) / max(abs(a - b) for a, b in zip(v, w)))
print("L08 worst ratio repr", repr(worst), "minus beta", worst - 0.9, "exceeds beta strictly:", worst > 0.9)

# one-point grid: fixed point u/(1-beta) and a priori error u beta^n/(1-beta)
print("L08 one-point V* at 0.9", 0.5 / (1 - 0.9), "at 0.95", 0.5 / (1 - 0.95))
print("L08 E3 first n with n/2 > 1000", next(n for n in range(1, 10**6) if n / 2 > 1000))

# ---- L09: certificate on the same grid
seq = seq09
for n in (59, 103, 147):
    cur, prev = seq[n], seq[n - 1]
    cert = 9.0 * max(abs(a - b) for a, b in zip(cur, prev))
    err = max(abs(a - b) for a, b in zip(cur, v09))
    print("L09 stop n", n, "cert", round(cert, 10), "err", round(err, 10), "ratio err/cert", err / cert)
b = 0.9
u1 = math.sqrt(0.75)  # ||V1 - V0||
for n in (151, 152):
    print("L09 a priori bound n", n, b**n / (1 - b) * u1)
print("L09 0.9^10/0.1", b**10 / (1 - b))
print("L09 naive ratio", 0.0000085808 / 0.0000009534, "vs 9")
print("L09 M3 step 1e-3*(1-b)/b", 1e-3 * (1 - b) / b)

# ---- L10: Riemann-Stieltjes exact sums for f = x, G = x^2 on uniform partitions
for n in (4, 10, 100, 1000):
    right = sum(Fraction(i, n) * (Fraction(i, n) ** 2 - Fraction(i - 1, n) ** 2) for i in range(1, n + 1))
    left = sum(Fraction(i - 1, n) * (Fraction(i, n) ** 2 - Fraction(i - 1, n) ** 2) for i in range(1, n + 1))
    t = Fraction(2, 3)
    assert right == Fraction((n + 1) * (4 * n - 1), 6 * n * n), n
    assert left == Fraction(4 * n * n - 3 * n - 1, 6 * n * n), n
    assert right - t == Fraction(3 * n - 1, 6 * n * n) and left - t == -Fraction(3 * n + 1, 6 * n * n)
    print("L10 n", n, float(right), float(left), "right err <= 1/n:", abs(right - t) <= Fraction(1, n), "left err <= 1/n:", abs(left - t) <= Fraction(1, n))
print("L10 E1 errors at n=10", float(Fraction(29, 600)), float(-Fraction(31, 600)))
print("L10 P2 quick check, S-2/3 bound m on random partition seed-free grid")
rng2 = random.Random(7)
worst_ratio = 0.0
for _ in range(300):
    m = rng2.randint(1, 30)
    xs = sorted([0.0, 1.0] + [rng2.random() for _ in range(m)])
    xs = sorted(set(xs))
    tags = [lo + rng2.random() * (hi - lo) for lo, hi in zip(xs, xs[1:])]
    s = sum(tg * (hi**2 - lo**2) for tg, lo, hi in zip(tags, xs, xs[1:]))
    mesh = max(hi - lo for lo, hi in zip(xs, xs[1:]))
    worst_ratio = max(worst_ratio, abs(s - 2 / 3) / mesh)
print("L10 P2 worst |S-2/3|/mesh over 300 random partitions (should be < 1)", round(worst_ratio, 6))
print("L10 int_0^1 x d(x^3) = 3 * int x^3 =", 3 * 0.25)
