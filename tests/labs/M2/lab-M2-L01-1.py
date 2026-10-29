"""M2 lab L01: the limit of a sequence, tabulated against its known limit, and an exact threshold.

Standard library only. No randomness and no network. The sequence is a_n = (2n + 1)/(n + 1), whose limit is 2
and whose exact distance from the limit is |a_n - 2| = 1/(n + 1). The terms are exact rational numbers
(fractions.Fraction), and the printed decimals are rounded only for display. The threshold search checks the
inequality |a_n - 2| < 1/1000 for each n from N to 5000 only. The fact that it holds for every n >= N is proved on
the page, not by the search.
"""

from __future__ import annotations

from fractions import Fraction

LIMIT = Fraction(2)


def a(n: int) -> Fraction:
    """The n-th term (2n + 1)/(n + 1) as an exact fraction, for an integer n >= 1."""
    if n < 1:
        raise ValueError(f"a needs n >= 1, got {n}")
    return Fraction(2 * n + 1, n + 1)


def error(n: int) -> Fraction:
    """The exact distance |a_n - 2| from the n-th term to the limit 2."""
    return abs(a(n) - LIMIT)


def least_threshold(epsilon: Fraction, search_limit: int) -> int:
    """The least N in 1..search_limit with |a_n - 2| < epsilon for every n from N to search_limit.

    Returns 0 when no N in that range works.
    """
    for big_n in range(1, search_limit + 1):
        if all(error(n) < epsilon for n in range(big_n, search_limit + 1)):
            return big_n
    return 0


def main() -> None:
    print("n, a_n, |a_n - 2|")
    for n in (1, 10, 100, 1000, 10000):
        print(f"{n}, {float(a(n)):.6f}, {float(error(n)):.6e}")
    big_n = least_threshold(Fraction(1, 1000), 5000)
    print(f"least N with |a_n - 2| < 0.001 for every n from N to 5000: {big_n}")
    print(f"error at n = 999: {float(error(999)):.6e}; error at n = 1000: {float(error(1000)):.6e}")
    print(f"the strict inequality fails at n = 999: {not error(999) < Fraction(1, 1000)}")


main()
