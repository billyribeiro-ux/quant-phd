"""Rung 2 completed solution: the log-likelihood contribution of one logit choice, from its two certainty equivalents.

Standard library only. The certainty equivalents are in cents and are unrounded floats; the logit uses them directly.
"""

import math


def contribution(ce_a: float, ce_b: float, kappa: float, chosen: str) -> float:
    """The log-probability of the chosen alternative: log P(A) = -log(1 + exp(-z)) for A, and log(1 - P(A)) =
    -log(1 + exp(z)) for B, with z = kappa (CE_A - CE_B) / 10000."""
    z = kappa * (ce_a - ce_b) / 10_000.0
    if chosen == "A":
        return -math.log1p(math.exp(-z))
    return -math.log1p(math.exp(z))


def main() -> None:
    ce_a, ce_b, kappa = 1500.0, 2200.0, 2.0
    for chosen in ("A", "B"):
        value = contribution(ce_a, ce_b, kappa, chosen)
        probability = math.exp(value)
        print("chosen", chosen, "| log contribution:", f"{value:.9f}", "| probability:", f"{probability:.9f}")
    p_a = 1.0 / (1.0 + math.exp(-kappa * (ce_a - ce_b) / 10_000.0))
    print(
        "P(A) from the sigmoid:",
        f"{p_a:.9f}",
        "| check of the A branch:",
        abs(math.exp(contribution(ce_a, ce_b, kappa, "A")) - p_a) < 1e-12,
    )
    print(
        "the two probabilities sum to one:",
        abs(math.exp(contribution(ce_a, ce_b, kappa, "A")) + math.exp(contribution(ce_a, ce_b, kappa, "B")) - 1.0)
        < 1e-12,
    )


main()
