"""M3 L01 lab 1: rank, independence and span of integer vectors, in exact rational arithmetic.

Claims checked, on seeded integer vectors with entries from -3 to 3:
  (a) a list of k vectors is linearly independent exactly when the matrix having them as columns has
      rank k, where rank is the number of pivots that Gauss-Jordan elimination finds (Proposition 3.5
      of Lesson 1);
  (b) a list of more than n vectors in R^n is never linearly independent (Corollary 3.6 of Lesson 1);
  (c) for v4 = 2 v1 - v2 + v3 in R^4, the four vectors have rank 3 exactly when v1, v2, v3 are
      independent (the rank of the planted list equals the rank of v1, v2, v3);
  (d) x lies in the span of e1 and e2 in R^3 exactly when its third coordinate is 0 (Example 2.3
      of Lesson 1);
  (e) the standard basis e1, ..., e4 of R^4 is independent and has rank 4.
Every rank is computed with fractions.Fraction, so no rounding enters. The draws come from a linear
congruential generator with fixed constants, so the output is the same on every run. The lab checks
these claims on the listed seeded inputs only and says nothing about other inputs. Standard library only.
"""

from __future__ import annotations

from fractions import Fraction

LCG_MULTIPLIER = 1103515245
LCG_INCREMENT = 12345
LCG_MODULUS = 2**31
SEED = 20261028
DRAWS = 200
PLANTED_DRAWS = 100


class Lcg:
    """A linear congruential generator with fixed constants, so every run draws the same integers."""

    def __init__(self, seed: int) -> None:
        self.state = seed % LCG_MODULUS

    def below(self, n: int) -> int:
        """Return an integer from 0 to n - 1. Each call advances the state once."""
        self.state = (LCG_MULTIPLIER * self.state + LCG_INCREMENT) % LCG_MODULUS
        return (self.state >> 16) % n

    def entry(self, bound: int) -> int:
        """Return an integer from -bound to bound, inclusive."""
        return self.below(2 * bound + 1) - bound


def vector(gen: Lcg, n: int, bound: int = 3) -> list[Fraction]:
    """A vector in R^n with integer entries from -bound to bound, as exact fractions."""
    return [Fraction(gen.entry(bound)) for _ in range(n)]


def rank(columns: list[list[Fraction]]) -> int:
    """The rank of the matrix whose columns are the given vectors: the number of pivots found by elimination.

    Gauss-Jordan elimination is run on the matrix with those columns. Every column has the same length n.
    An empty list has rank 0.
    """
    if not columns:
        return 0
    n = len(columns[0])
    k = len(columns)
    m = [[columns[j][i] for j in range(k)] for i in range(n)]
    pivots = 0
    for c in range(k):
        p = next((i for i in range(pivots, n) if m[i][c] != 0), None)
        if p is None:
            continue
        m[pivots], m[p] = m[p], m[pivots]
        for i in range(n):
            if i != pivots and m[i][c] != 0:
                factor = m[i][c] / m[pivots][c]
                m[i] = [a - factor * b for a, b in zip(m[i], m[pivots], strict=True)]
        pivots += 1
        if pivots == n:
            break
    return pivots


def independent(columns: list[list[Fraction]]) -> bool:
    """True when the list is linearly independent: its rank equals the number of vectors."""
    return rank(columns) == len(columns)


def in_span(spanning: list[list[Fraction]], x: list[Fraction]) -> bool:
    """True when x lies in the span of the list: adding x does not raise the rank."""
    return rank([*spanning, x]) == rank(spanning)


def count_independent(gen: Lcg, n: int, k: int, draws: int) -> int:
    """How many of the draws are lists of k vectors in R^n that are linearly independent."""
    hits = 0
    for _ in range(draws):
        cols = [vector(gen, n) for _ in range(k)]
        hits += independent(cols)
    return hits


def planted(gen: Lcg) -> tuple[int, int, int]:
    """For PLANTED_DRAWS draws of v1, v2, v3 in Z^4, with v4 = 2 v1 - v2 + v3.

    Returns (the count of dependent four-vector lists, the count of independent triples, the count of
    four-vector lists with rank exactly 3).
    """
    dependent = triples = rank_three = 0
    for _ in range(PLANTED_DRAWS):
        v1 = vector(gen, 4)
        v2 = vector(gen, 4)
        v3 = vector(gen, 4)
        v4 = [2 * a - b + c for a, b, c in zip(v1, v2, v3, strict=True)]
        four = [v1, v2, v3, v4]
        dependent += not independent(four)
        triples += independent([v1, v2, v3])
        rank_three += rank(four) == 3
    return dependent, triples, rank_three


def main() -> None:
    gen = Lcg(SEED)
    a = count_independent(gen, 3, 3, DRAWS)
    b = count_independent(gen, 3, 4, DRAWS)
    c = count_independent(gen, 4, 4, DRAWS)
    d = count_independent(gen, 4, 5, DRAWS)
    print(f"R^3, 3 vectors: independent in {a} of {DRAWS} seeded lists")
    print(f"R^3, 4 vectors: independent in {b} of {DRAWS} seeded lists")
    print(f"R^4, 4 vectors: independent in {c} of {DRAWS} seeded lists")
    print(f"R^4, 5 vectors: independent in {d} of {DRAWS} seeded lists")

    dependent, triples, rank_three = planted(gen)
    print(f"planted v4 = 2 v1 - v2 + v3 in R^4: dependent in {dependent} of {PLANTED_DRAWS} seeded triples")
    print(f"v1, v2, v3 independent in {triples} of {PLANTED_DRAWS} seeded triples")
    print(f"planted list has rank 3 in {rank_three} of {PLANTED_DRAWS} seeded triples")
    print(f"rank 3 count equals the independent-triple count: {rank_three == triples}")

    e1 = [Fraction(1), Fraction(0), Fraction(0)]
    e2 = [Fraction(0), Fraction(1), Fraction(0)]
    print(f"(1, 2, 0) in span(e1, e2): {in_span([e1, e2], [Fraction(1), Fraction(2), Fraction(0)])}")
    print(f"(0, 0, 1) in span(e1, e2): {in_span([e1, e2], [Fraction(0), Fraction(0), Fraction(1)])}")
    agree = 0
    for _ in range(PLANTED_DRAWS):
        x = vector(gen, 3)
        agree += in_span([e1, e2], x) == (x[2] == 0)
    print(f"span membership agrees with the test x3 = 0 in {agree} of {PLANTED_DRAWS} seeded vectors")

    basis = [[Fraction(int(i == j)) for i in range(4)] for j in range(4)]
    print(f"standard basis e1, ..., e4 of R^4 is independent with rank 4: {independent(basis) and rank(basis) == 4}")


main()
