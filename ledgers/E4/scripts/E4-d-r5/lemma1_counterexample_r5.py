"""Lemma 1 (project.html:266-268) with V constant but v not conditionally normal: a two-point payoff.

Usage: python -I lemma1_counterexample_r5.py. The payoff minus price is d +/- sqrt(V) with probability 1/2 each (mean
m - p = d, variance V = 1), a = 2, no cost. The lemma's optimal demand is d/(aV) with value -exp(-d^2/(2V)).
"""

import math

a, V, d = 2.0, 1.0, 1.0


def utility(x: float) -> float:
    return -0.5 * (math.exp(-a * x * (d + math.sqrt(V))) + math.exp(-a * x * (d - math.sqrt(V))))


xs = [i / 10000 for i in range(-200000, 200001)]
best = max(xs, key=utility)
print("lemma demand x* =", d / (a * V), "| utility there =", round(utility(d / (a * V)), 6))
print("lemma value -exp(-d^2/(2V)) =", round(-math.exp(-d * d / (2 * V)), 6))
print("numerical argmax on [-20, 20] =", best, "| utility there =", round(utility(best), 6))
