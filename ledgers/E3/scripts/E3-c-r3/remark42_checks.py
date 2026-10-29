"""Checks for L08 Remark 4.2 and the scope of its 'for a CRRA utility' key result.

(a) Counterexample to 'equals expected utility at the average prior only when the midpoint of the extreme priors is 1/2':
    prior set {0.2, 0.6} (two-outcome gamble, W1 = 110000, W0' = 95000): alpha-MEU(1/2) equals EU at the average prior 0.4,
    and the midpoint is 0.4, not 1/2.
(b) For a two-outcome gamble E_p u(f) is affine in p for ANY utility u, so the midpoint identity holds for every u;
    the page's proof (Remark 4.2, Problem P3) is written only for u(W) = -1/W (gamma = 2).

Usage: python -I ledgers/E3/scripts/E3-c-r3/remark42_checks.py
"""

from __future__ import annotations

import math
from fractions import Fraction

W1, W0 = 110000, 95000


def inv_ce(p: Fraction) -> Fraction:
    return 1 / (p / W1 + (1 - p) / W0)


def amef_half(p_min: Fraction, p_max: Fraction) -> Fraction:
    # alpha-MEU at alpha = 1/2 with u = -1/W: CE = 1/(0.5 max E[1/W] + 0.5 min E[1/W])
    g = lambda p: p / W1 + (1 - p) / W0  # noqa: E731
    return 1 / (Fraction(1, 2) * g(p_min) + Fraction(1, 2) * g(p_max))


a = Fraction(1, 5)
b = Fraction(3, 5)
avg = (a + b) / 2
print("(a) priors {0.2, 0.6}: average", avg, "midpoint", (a + b) / 2)
print("    alpha-MEU(1/2) =", float(amef_half(a, b)), " EU at average prior =", float(inv_ce(avg)), " equal:", amef_half(a, b) == inv_ce(avg))
print("    midpoint equals 1/2?", (a + b) / 2 == Fraction(1, 2))

# (b) affinity of E_p u(f) in p for a power utility with gamma = 3 (u(W) = W**(-2) / (-2))
def eu_power(p: float, gamma: float) -> float:
    u = lambda w: w ** (1 - gamma) / (1 - gamma)  # noqa: E731
    return p * u(W1) + (1 - p) * u(W0)

for p, q in [(1 / 3, 2 / 3)]:
    mid = (p + q) / 2
    print("(b) gamma=3: 0.5*Eu(1/3)+0.5*Eu(2/3) =", 0.5 * eu_power(p, 3) + 0.5 * eu_power(q, 3), " Eu(1/2) =", eu_power(mid, 3))
