"""Kink check: is the prospect certainty equivalent C^1 across the sign change of the lottery value?

Lottery (+100, -100) with probability 1/2 each, gamma = 0.635210 (the Lab 3 curvature). Lambda is moved through the
point where the lottery value V changes sign (lambda = 1). One-sided difference quotients are compared at several steps.
"""
from fractions import Fraction as F

GAMMA = 0.635210


def ce(prizes, probs, lam, g=GAMMA):
    v = sum(float(p) * ((x ** (1 - g)) if x >= 0 else -lam * ((-x) ** (1 - g))) for x, p in zip(prizes, probs))
    if v >= 0:
        return v ** (1 / (1 - g))
    return -((-v / lam) ** (1 / (1 - g)))


prizes, probs, lam0 = [100, -100], [F(1, 2), F(1, 2)], 1.0
print("CE at lambda = 1:", ce(prizes, probs, lam0))
for d in [1e-3, 1e-4, 1e-5, 1e-6, 1e-7]:
    left = (ce(prizes, probs, lam0) - ce(prizes, probs, lam0 - d)) / d
    right = (ce(prizes, probs, lam0 + d) - ce(prizes, probs, lam0)) / d
    print("step %g  left-quotient %.6e  right-quotient %.6e" % (d, left, right))
