"""Round-2 independent recomputation of the L02 lab numbers, the L02 prose numbers and the Lemma 2.1 bound.

Run: .venv/bin/python -I ledgers/SC1/scripts/SC1-a-r2/recompute_L02.py
Hat values are computed exactly as Fractions by linear interpolation between the nodes 2**-m (value 1 at odd
multiples, 0 at even multiples), not from the page's closed form. Coefficients are the seeded draws, converted to
Fraction exactly. Level suprema are computed exactly on the 2**-10 grid and compared with max|c| * 2**(-(m+1)/2).
"""

from __future__ import annotations

import math
import random
from fractions import Fraction as F

SEED = 20260101
LEVELS = 8


def draws() -> tuple[float, list[list[float]]]:
    rng = random.Random(SEED)
    xi0 = rng.gauss(0.0, 1.0)
    coeffs = []
    for m in range(1, LEVELS + 1):
        row = []
        for _ in range(2 ** (m - 1)):
            row.append(rng.gauss(0.0, 1.0))
        coeffs.append(row)
    return xi0, coeffs


def hat_exact(m: int, j: int, t: F) -> F:
    """Level-m hat with centre (2j-1)/2**m, by interpolation between the nodes k/2**m (k = 0..2**m)."""
    nodes = F(1, 2**m)
    k = int(t / nodes)  # t lies in [k/2**m, (k+1)/2**m] (k = floor)
    if k >= 2**m:
        k = 2**m - 1
    left = F(k) * nodes
    right = F(k + 1) * nodes
    value_at = lambda idx: F(1) if idx % 2 == 1 and (idx + 1) // 2 == j else F(0)  # noqa: E731
    # node index idx = k means position idx/2**m; the hat peaks at odd index 2j-1 with value 1
    v_left = value_at(k)
    v_right = value_at(k + 1)
    frac = (t - left) / (right - left)
    return v_left + (v_right - v_left) * frac


def partial_sum_exact_zero_test(coeffs: list[list[float]], n: int, levels: int, t: F) -> bool:
    """True when every level-m hat with n < m <= levels vanishes exactly at t (so S_levels(t) = S_n(t))."""
    for m in range(n + 1, levels + 1):
        for j in range(1, 2 ** (m - 1) + 1):
            if hat_exact(m, j, t) != 0:
                return False
    return True


def main() -> None:
    xi0, coeffs = draws()
    print(f"recomputed draws: xi0 = {xi0:.6f}; level sizes {[len(r) for r in coeffs]}")

    # Lemma 2.2(d) / 216 count, exact.
    cases = 0
    equal = 0
    pairs = 0
    for n in range(5):
        pairs += 2**n + 1
        for k in range(2**n + 1):
            t = F(k, 2**n)
            for levels in range(n, LEVELS + 1):
                cases += 1
                equal += partial_sum_exact_zero_test(coeffs, n, levels, t)
    print(f"recomputed: dyadic fixed-from-level checks {equal} of {cases}; (depth,point) pairs = {pairs}")
    per_depth = [(n, 2**n + 1, (2**n + 1) * (LEVELS - n + 1)) for n in range(5)]
    print(f"recomputed: per-depth (depth, points, cases) = {per_depth}; sum of cases = {sum(c for _, _, c in per_depth)}")

    # Grid supremum of each level term, exact on the 2**-10 grid.
    grid = [F(i, 2**10) for i in range(2**10 + 1)]
    sup_equal = 0
    for m in range(1, LEVELS + 1):
        row = coeffs[m - 1]
        best = F(0)
        for t in grid:
            total = F(0)
            for j in range(1, 2 ** (m - 1) + 1):
                total += F(row[j - 1]) * hat_exact(m, j, t)
            best = max(best, abs(total))
        formula = max(abs(F(c)) for c in row)
        sup_equal += best == formula
    print(f"recomputed: grid sup of level term equals max|c| (exact), levels 1..8: {sup_equal == LEVELS}")

    # Observed sups and bounds (floats; the printed values are these, to six places).
    obs_within = 0
    for m in range(1, LEVELS + 1):
        observed = max(abs(c) for c in coeffs[m - 1]) * 2 ** (-(m + 1) / 2)
        bound = math.sqrt(4 * m * math.log(2)) * 2 ** (-(m + 1) / 2)
        obs_within += observed <= bound
        print(f"recomputed m={m}: observed {observed:.6f} bound {bound:.6f} within {observed <= bound}")
    print(f"recomputed: levels within bound: {obs_within} of {LEVELS}")

    # Tail: grid sup of |S_8 - S_4| in floats, using the exact hat values times float coefficients.
    def s_level(levels: int, t: F) -> float:
        total = float(xi0) * float(t)
        for m in range(1, levels + 1):
            scale = 2 ** (-(m + 1) / 2)
            for j in range(1, 2 ** (m - 1) + 1):
                total += coeffs[m - 1][j - 1] * scale * float(hat_exact(m, j, t))
        return total

    tail = max(abs(s_level(8, t) - s_level(4, t)) for t in grid)
    tail_bound = sum(math.sqrt(4 * m * math.log(2)) * 2 ** (-(m + 1) / 2) for m in range(5, LEVELS + 1))
    print(f"recomputed: grid sup |S_8 - S_4| = {tail:.6f}; sum of bounds levels 5..8 = {tail_bound:.6f}")

    # Page prose: sqrt(4 log 2) and half of it, the level-1 observed value implying |xi_11|.
    lam1 = math.sqrt(4 * math.log(2))
    print(f"recomputed: sqrt(4 log 2) = {lam1:.6f}; half = {lam1 / 2:.6f}")
    print(f"recomputed: |xi_1,1| implied by 0.116589 = {0.116589 * 2:.6f}")
    print(f"recomputed: Lemma 2.1 union bound 2^(m-1)*2*exp(-lambda_m^2/2) = 2^-m? ",
          all(abs(2 ** (m - 1) * 2 * math.exp(-(4 * m * math.log(2)) / 2) - 2 ** (-m)) < 1e-15 for m in range(1, 9)))
    print("recomputed: M_m identity sqrt(2 log 2) sqrt(m) 2^(-m/2) = lambda_m 2^(-(m+1)/2):",
          all(abs(math.sqrt(4 * m * math.log(2)) * 2 ** (-(m + 1) / 2) - math.sqrt(2 * math.log(2)) * math.sqrt(m) * 2 ** (-m / 2)) < 1e-15 for m in range(1, 60)))
    print("recomputed: sum over m of m r^m with r = 2^-1/2 vs r/(1-r)^2 =", sum(m * (2**-0.5) ** m for m in range(1, 400)), (2**-0.5) / (1 - 2**-0.5) ** 2)


if __name__ == "__main__":
    main()
