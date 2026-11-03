"""Rung 1 worked example: one SIMULATED participant, three choice pairs, their certainty equivalents and likelihood.

Standard library only. The participant's parameters are stated values chosen for this example (gamma 0.40,
lambda 2.00, kappa 1.50). They are not estimates, and the participant is not a real person.
"""

import math
from fractions import Fraction

GAMMA = 0.40  # curvature of the value function, in [0, 1) for the prospect model
LAMBDA = 2.00  # loss-aversion coefficient
KAPPA = 1.50  # choice precision: the slope of the logit rule, per $100 of certainty-equivalent difference
WEALTH = 100_000  # starting wealth in cents ($1,000.00); used by the CRRA model only


def nearest_cent(amount: float) -> int:
    """The nearest whole cent of a float, with an exact half going up (toward plus infinity)."""
    return math.floor(amount + 0.5)


def crra_certainty_equivalent(prizes: list[int], probs: list[Fraction], gamma: float, wealth: int) -> float:
    """CRRA certainty equivalent as a change from wealth, in cents, unrounded: the sure amount whose utility of final
    wealth equals the lottery's expected utility of final wealth."""
    finals = [wealth + x for x in prizes]
    expected = sum(float(p) * math.pow(w, 1.0 - gamma) for p, w in zip(probs, finals, strict=True))
    return math.pow(expected, 1.0 / (1.0 - gamma)) - wealth


def prospect_value(x: int, gamma: float, lam: float) -> float:
    """Value of a change x from the reference point 0: x^(1-gamma) for a gain, -lambda (-x)^(1-gamma) for a loss."""
    if x >= 0:
        return math.pow(float(x), 1.0 - gamma)
    return -lam * math.pow(float(-x), 1.0 - gamma)


def prospect_certainty_equivalent(prizes: list[int], probs: list[Fraction], gamma: float, lam: float) -> float:
    """The sure change whose value equals the lottery's value (the probability-weighted sum of prospect values), in
    cents, unrounded. The inverse of the value function is taken on each side of zero."""
    total = sum(float(p) * prospect_value(x, gamma, lam) for x, p in zip(prizes, probs, strict=True))
    if total >= 0.0:
        return math.pow(total, 1.0 / (1.0 - gamma))
    return -math.pow(-total / lam, 1.0 / (1.0 - gamma))


def choice_probability_a(ce_a: float, ce_b: float, kappa: float) -> float:
    """P(choose A) = 1 / (1 + exp(-z)), z = kappa (CE_A - CE_B) / 10000: the difference is in units of $100."""
    z = kappa * (ce_a - ce_b) / 10_000.0
    return 1.0 / (1.0 + math.exp(-z))


def main() -> None:
    pairs = [
        ("pair 1", [2000, -1000], [Fraction(1, 2), Fraction(1, 2)], [500], [Fraction(1)], "A"),
        ("pair 2", [3000], [Fraction(1)], [4000, -2000], [Fraction(1, 4), Fraction(3, 4)], "B"),
        ("pair 3", [1500, 2500], [Fraction(1, 3), Fraction(2, 3)], [-500, 3000], [Fraction(1, 2), Fraction(1, 2)], "A"),
    ]
    total = 0.0
    for name, pa, qa, pb, qb, chosen in pairs:
        crra_a = nearest_cent(crra_certainty_equivalent(pa, qa, GAMMA, WEALTH))
        crra_b = nearest_cent(crra_certainty_equivalent(pb, qb, GAMMA, WEALTH))
        ce_a = prospect_certainty_equivalent(pa, qa, GAMMA, LAMBDA)
        ce_b = prospect_certainty_equivalent(pb, qb, GAMMA, LAMBDA)
        print(
            name, "| CRRA cents A, B:", crra_a, crra_b, "| prospect cents A, B:", nearest_cent(ce_a), nearest_cent(ce_b)
        )
        p_a = choice_probability_a(ce_a, ce_b, KAPPA)
        p_chosen = p_a if chosen == "A" else 1.0 - p_a
        total += math.log(p_chosen)
        print(name, "| P(A):", f"{p_a:.6f}", "| chosen:", chosen, "| log P(chosen):", f"{math.log(p_chosen):.6f}")
    print("log-likelihood of the three choices:", f"{total:.6f}")


main()