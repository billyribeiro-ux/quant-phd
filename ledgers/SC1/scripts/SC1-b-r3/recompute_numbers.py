"""Verifier round 3, SC1 slice b: independent recomputation of the numbers printed or quoted on L04, L05 and L06.

Standard library only. Run from the checkout root as:
    python3 -I -W error ledgers/SC1/scripts/SC1-b-r3/recompute_numbers.py

Sections:
  1. Lab L05 at 60 significant digits (Decimal): the 225 Simpson gaps of the Chapman-Kolmogorov check, the
     largest integrand mass for 12 <= |z| <= 40, and the quadrature error of the same Simpson rule. This decides
     whether the printed gaps are rounding error or quadrature error.
  2. Closed forms quoted on the pages, checked against math (double precision, ten digits is enough) and against
     the exact fraction arithmetic of L06.
  3. Exact counts for L06 Parts C and D from the binomial law, against the reflection identity.
"""

from __future__ import annotations

import math
from decimal import Decimal, getcontext
from fractions import Fraction
from math import comb

getcontext().prec = 60
PI = Decimal("3.14159265358979323846264338327950288419716939937510582097494459")
TWO_PI = 2 * PI
LOWER = Decimal(-12)
UPPER = Decimal(12)
INTERVALS = 2000
TIMES = (Decimal("0.5"), Decimal(1), Decimal(2))
POINTS = (Decimal(-1), Decimal("-0.25"), Decimal(0), Decimal("0.5"), Decimal(1))


def density(u: Decimal, x: Decimal, y: Decimal) -> Decimal:
    """Gaussian transition density p_u(x, y) = (2 pi u)^(-1/2) exp(-(y - x)^2 / (2 u)), in 60-digit arithmetic."""
    return (-((y - x) ** 2) / (2 * u)).exp() / (TWO_PI * u).sqrt()


def simpson(f, a: Decimal, b: Decimal, n: int) -> Decimal:
    """Composite Simpson rule with n (even) subintervals, the same rule as the lab twin."""
    h = (b - a) / n
    total = f(a) + f(b)
    for i in range(1, n):
        total += (4 if i % 2 == 1 else 2) * f(a + i * h)
    return total * h / 3


def ck_gap(s: Decimal, t: Decimal, x: Decimal, y: Decimal) -> Decimal:
    """Simpson value of the integral of p_s(x,z) p_t(z,y) over [-12,12], minus p_{s+t}(x,y)."""
    integral = simpson(lambda z: density(s, x, z) * density(t, z, y), LOWER, UPPER, INTERVALS)
    return integral - density(s + t, x, y)


def tail_mass(s: Decimal, t: Decimal, x: Decimal, y: Decimal) -> Decimal:
    """Integral of p_s(x,z) p_t(z,y) over 12 <= |z| <= 40, Simpson on each side."""

    def f(z: Decimal) -> Decimal:
        return density(s, x, z) * density(t, z, y)

    return simpson(f, Decimal(12), Decimal(40), INTERVALS) + simpson(f, Decimal(-40), Decimal(-12), INTERVALS)


def section_lab_l05() -> None:
    print("== 1. Lab L05 at 60 digits ==")
    worst_gap = Decimal(0)
    worst_gap_case = None
    worst_tail = Decimal(0)
    count = 0
    for s in TIMES:
        for t in TIMES:
            for x in POINTS:
                for y in POINTS:
                    g = abs(ck_gap(s, t, x, y))
                    count += 1
                    if g > worst_gap:
                        worst_gap = g
                        worst_gap_case = (s, t, x, y)
                    worst_tail = max(worst_tail, tail_mass(s, t, x, y))
    print(f"cases: {count}")
    print(f"largest |Simpson - exact| at 60 digits (quadrature error of the lab rule): {float(worst_gap):.3e}")
    print(f"  at case (s,t,x,y) = {tuple(float(v) for v in worst_gap_case)}")
    print(f"largest mass of the integrand for 12 <= |z| <= 40, 60 digits: {float(worst_tail):.3e}")
    dec_int = [simpson(lambda y: density(t, Decimal(0), y), LOWER, UPPER, INTERVALS) for t in TIMES]
    for t, v in zip(TIMES, dec_int):
        print(f"integral of p_{float(t):g}(0,y) over [-12,12] at 60 digits: {float(v):.15f}")
    print()


def section_closed_forms() -> None:
    print("== 2. Closed forms quoted on the pages (double precision) ==")
    print(f"erfc(1/sqrt2)       = {math.erfc(1 / math.sqrt(2)):.12f}  (L06 Part E prints 0.3173105079)")
    print(f"erfc(1/sqrt2)/2     = {math.erfc(1 / math.sqrt(2)) / 2:.12f}  (L06 Part E prints 0.1586552539)")
    print(f"P(B_1 >= 1)         = {0.5 * math.erfc(1 / math.sqrt(2)):.12f}  (L06 quiz, 0.1587)")
    print(f"e^(1/4)             = {math.exp(0.25):.12f}  (L04 prints 1.284025417)")
    print(f"e^1                 = {math.exp(1):.12f}  (L04 prints 2.718281828)")
    print(f"e^4                 = {math.exp(4):.12f}  (L04 prints 54.598150033)")
    print(f"e^8                 = {math.exp(8):.12f}  (L04 E2/E3 quote 2980.957987)")
    print(f"Phi(-1/sqrt2)       = {0.5 * math.erfc(0.5):.12f}  (L05 quiz, 0.23975)")
    print(f"(2 pi)^(-1/2)       = {1 / math.sqrt(2 * math.pi):.12f}  (L05 quiz p_1(0,0), 0.3989)")
    print(f"machine epsilon     = {2.0**-52:.3e}; 5.55e-16 / eps = {5.55e-16 / 2.0**-52:.3f}  (L05 quotes ~2.5)")
    print(f"gap ratio 5.55e-16 / 3.81e-29 = {5.55e-16 / 3.81e-29:.4e}  (L05 E1 quotes about 1.5e13)")
    print(f"|3.05e-16| / eps    = {3.05e-16 / 2.0**-52:.3f}  (L05 E3 quotes about 1.4)")
    print()


def section_counts() -> None:
    print("== 3. L06 exact counts from the binomial law ==")

    def count_sn_ge(n: int, level: int) -> int:
        """#{S_n >= level} for the simple random walk of length n: S_n = 2U - n with U up-steps."""
        return sum(comb(n, u) for u in range(n + 1) if 2 * u - n >= level)

    def count_sn_eq(n: int, level: int) -> int:
        return sum(comb(n, u) for u in range(n + 1) if 2 * u - n == level)

    def count_sn_gt(n: int, level: int) -> int:
        return sum(comb(n, u) for u in range(n + 1) if 2 * u - n > level)

    # Part C: N = 12, a = 3
    n, a = 12, 3
    m_ge = count_sn_ge(n, a) + count_sn_gt(n, a)
    print(f"Part C: #{{M_12 >= 3}} via Corollary 1.4 = {m_ge} (lab prints 1588 of 4096)")
    print(f"Part C: #{{S_12 = 4}} = {count_sn_eq(12, 4)} (lab prints 495); #{{S_12 = 2}} = {count_sn_eq(12, 2)}")
    # Part D: N = 10, a = 2
    tail = Fraction(count_sn_ge(10, 2) + count_sn_gt(10, 2), 2**10)
    above = Fraction(count_sn_gt(10, 2), 2**10)
    at = Fraction(count_sn_eq(10, 2), 2**10)
    print(f"Part D: P(M_10>=2) = {tail} (lab: 281/512)")
    print(f"Part D: 2 P(S_10>2) = {2 * above} (lab: 11/32)")
    print(f"Part D: P(S_10=2) = {at} (lab: 105/512)")
    print(f"Part D: difference equals P(S_10=2): {tail - 2 * above == at}")
    # Part B: 78 pairs
    print(f"Part B pairs: {sum(range(1, 13))} (lab: 78)")
    # Part A triples: sum over n of sum over a=1..n of (a + n)
    triples = sum(a + n for n in range(1, 13) for a in range(1, n + 1))
    print(f"Part A triples: {triples} (lab: 1014)")
    print()


if __name__ == "__main__":
    section_closed_forms()
    section_counts()
    section_lab_l05()
