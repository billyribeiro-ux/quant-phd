"""M5 lab L02: the Cauchy test on partial sums, for a series that diverges and one that converges.

Standard library only. No randomness and no network. All partial sums are exact fractions.Fraction
values. The test for a tolerance eps asks whether |S_m - S_n| < eps for all m, n >= N, and the lab
checks it on finite ranges. A failure found in a finite range is a counterexample to the test
holding from N on, and it is exact. A pass in a finite range is evidence only for that range. The
proofs on the page establish the claims for all indices: Proposition 3.3 for the harmonic gaps,
Lemma 3.4 for the geometric identity, and Proposition 3.5 for the threshold N = 10.
"""

from __future__ import annotations

from collections.abc import Callable
from fractions import Fraction

HARMONIC_MAX_N = 200
GEOMETRIC_MAX_N = 20
GEOMETRIC_PAIR_LIMIT = 60
EPS_HARMONIC = Fraction(1, 2)
EPS_GEOMETRIC = Fraction(1, 1024)


def harmonic_partial(n: int) -> Fraction:
    """S_n = 1 + 1/2 + ... + 1/n for n >= 1, computed exactly."""
    return sum((Fraction(1, k) for k in range(1, n + 1)), Fraction(0))


def geometric_partial(n: int) -> Fraction:
    """G_n = 1/2 + 1/4 + ... + 1/2^n for n >= 0, computed exactly. Here G_n = 1 - 1/2^n."""
    return sum((Fraction(1, 2**k) for k in range(1, n + 1)), Fraction(0))


def cauchy_test_fails_from(partial: Callable[[int], Fraction], start: int, eps: Fraction, limit: int) -> bool:
    """True when some pair start <= n < m <= limit has |S_m - S_n| >= eps, so the test fails from start."""
    for n in range(start, limit + 1):
        for m in range(n + 1, limit + 1):
            if abs(partial(m) - partial(n)) >= eps:
                return True
    return False


def main() -> None:
    # Harmonic series: eps = 1/2 fails at each N in 1..HARMONIC_MAX_N; the pair (N, 2N) witnesses it.
    gaps = [harmonic_partial(2 * n) - harmonic_partial(n) for n in range(1, HARMONIC_MAX_N + 1)]
    print(f"harmonic partial sums, pairs (N, 2N) for N = 1 to {HARMONIC_MAX_N}")
    print(f"gaps S_2N - S_N that are at least 1/2: {sum(g >= EPS_HARMONIC for g in gaps)} of {len(gaps)}")
    print(f"smallest gap S_2N - S_N over these N: {min(gaps)}, at N = {gaps.index(min(gaps)) + 1}")
    failing = [n for n in range(1, HARMONIC_MAX_N + 1) if harmonic_partial(2 * n) - harmonic_partial(n) >= EPS_HARMONIC]
    print(
        f"indices N where the test with eps = 1/2 fails, N = 1 to {HARMONIC_MAX_N}: {len(failing)} of {HARMONIC_MAX_N}"
    )

    # Geometric series: exact identity for the tail, then the first index from which the test passes.
    identity = 0
    pairs = 0
    for n in range(0, GEOMETRIC_PAIR_LIMIT):
        for m in range(n + 1, GEOMETRIC_PAIR_LIMIT + 1):
            pairs += 1
            identity += geometric_partial(m) - geometric_partial(n) == Fraction(1, 2**n) - Fraction(1, 2**m)
    print(f"identity G_m - G_n = 1/2^n - 1/2^m for 0 <= n < m <= {GEOMETRIC_PAIR_LIMIT}: {identity} of {pairs} pairs")
    passing = [
        n
        for n in range(0, GEOMETRIC_MAX_N + 1)
        if not cauchy_test_fails_from(geometric_partial, n, EPS_GEOMETRIC, GEOMETRIC_PAIR_LIMIT)
    ]
    first = passing[0] if passing else -1
    print(f"first index N from which the test with eps = 1/1024 passes, N = 0 to {GEOMETRIC_MAX_N}: {first}")
    failing_geo = [n for n in range(0, GEOMETRIC_MAX_N + 1) if n not in passing]
    print(f"indices N in 0 to {GEOMETRIC_MAX_N} where it fails: {failing_geo[0]} to {failing_geo[-1]}")


main()
