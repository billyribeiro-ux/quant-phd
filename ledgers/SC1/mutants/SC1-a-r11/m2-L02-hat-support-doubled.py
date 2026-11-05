# MUTANT m2-L02-hat-support-doubled: Hat support has radius 2**(-(m-1)) instead of 2**(-m); the dyadic-fixed count and the grid check must move.
"""SC1 lab L02: a seeded partial sum of hat functions on [0, 1], with exact checks on dyadic points.

SIMULATED. The coefficients are standard normal draws from random.Random(SEED). The dyadic count and the grid-supremum
line are identities that hold for every seed; the bound lines describe one seeded sample. Standard library only; no
network; nothing is read from a file. The hat values at dyadic points are exact binary fractions, and every level
term beyond the depth of the point is exactly 0.0 there, so the dyadic checks compare identical floating-point sums.
Numbers are printed to six decimal places from unrounded values.
"""

from __future__ import annotations

import math
import random

SEED = 20260101
LEVELS = 8
GRID_DEPTH = 10


def hat(m: int, j: int, t: float) -> float:
    """The level-m hat max(0, 1 - 2**m |t - (2j - 1) 2**(-m)|), for m >= 1 and 1 <= j <= 2**(m-1).

    Its peak value 1 sits at the centre (2j - 1) 2**(-m), and it vanishes outside the open interval of radius 2**(-m).
    """
    centre = (2 * j - 1) / 2.0**m
    return max(0.0, 1.0 - 2.0 ** (m - 1) * abs(t - centre))


def partial_sum(xi0: float, coeffs: list[list[float]], levels: int, t: float) -> float:
    """Sigma_levels(t) = xi0 t + the sum over m = 1..levels and j of coeffs[m-1][j-1] 2**(-(m+1)/2) hat(m, j, t)."""
    total = xi0 * t
    for m in range(1, levels + 1):
        scale = 2 ** (-(m + 1) / 2)
        for j in range(1, 2 ** (m - 1) + 1):
            total += coeffs[m - 1][j - 1] * scale * hat(m, j, t)
    return total


def level_term_sup(coeffs_m: list[float], m: int) -> float:
    """The supremum over t in [0, 1] of |Y_m(t)|, where Y_m is the level-m term of the sum.

    At most one hat of level m is non-zero at any t, and each hat peaks at 1, so the supremum is the largest
    coefficient in absolute value times 2**(-(m+1)/2).
    """
    return max(abs(c) for c in coeffs_m) * 2 ** (-(m + 1) / 2)


def bound(m: int) -> float:
    """The bound lambda_m 2**(-(m+1)/2) with lambda_m = sqrt(4 m log 2), used in the proof of the page."""
    return math.sqrt(4 * m * math.log(2)) * 2 ** (-(m + 1) / 2)


def main() -> None:
    rng = random.Random(SEED)
    xi0 = rng.gauss(0.0, 1.0)
    coeffs = [[rng.gauss(0.0, 1.0) for _ in range(2 ** (m - 1))] for m in range(1, LEVELS + 1)]

    fixed_cases = 0
    fixed_equal = 0
    for n in range(5):
        for k in range(2**n + 1):
            t = k / 2**n
            base = partial_sum(xi0, coeffs, n, t)
            for levels in range(n, LEVELS + 1):
                fixed_cases += 1
                fixed_equal += partial_sum(xi0, coeffs, levels, t) == base
    print(f"dyadic values fixed from level n on (n <= 4, n <= M <= {LEVELS}): {fixed_equal} of {fixed_cases} cases")

    grid = [i / 2**GRID_DEPTH for i in range(2**GRID_DEPTH + 1)]
    sup_agree = 0
    for m in range(1, LEVELS + 1):
        scale = 2 ** (-(m + 1) / 2)
        grid_sup = max(
            abs(sum(coeffs[m - 1][j - 1] * hat(m, j, t) for j in range(1, 2 ** (m - 1) + 1)) * scale) for t in grid
        )
        sup_agree += grid_sup == level_term_sup(coeffs[m - 1], m)
    print(f"grid supremum of each level term equals the formula for levels 1 to {LEVELS}: {sup_agree == LEVELS}")

    within = 0
    for m in range(1, LEVELS + 1):
        observed = level_term_sup(coeffs[m - 1], m)
        ok = observed <= bound(m)
        within += ok
        print(f"m = {m}: observed sup {observed:.6f}, bound {bound(m):.6f}, observed <= bound: {ok}")
    print(f"levels whose observed sup is within the bound: {within} of {LEVELS}")

    tail_grid_sup = max(abs(partial_sum(xi0, coeffs, LEVELS, t) - partial_sum(xi0, coeffs, 4, t)) for t in grid)
    tail_bound = sum(bound(m) for m in range(5, LEVELS + 1))
    print(
        f"grid supremum of |Sigma_8 - Sigma_4|: {tail_grid_sup:.6f}; "
        f"sum of the bounds for levels 5 to 8: {tail_bound:.6f}"
    )


main()
