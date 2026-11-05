"""E4 L01 lab 1: Arrow-Debreu decomposition and valuation of a claim on four states, computed exactly.

Inputs are illustrative numbers, not data. The state space has four states. State s has the probability
STATE_PROBABILITIES[s], a positive exact Fraction, and the probabilities sum to exactly 1. A claim is a payoff vector
in whole cents, one entry per state. An Arrow-Debreu security s pays 1 in state s and 0 in every other state. Its
price PRICES[s] is a dimensionless exact Fraction, so a claim's value in cents is the sum of price times payoff.

Part A: the decomposition of the claim into Arrow-Debreu securities, checked state by state.
Part B: the value of the claim under the prices, and of a second claim.
Part C: linearity of the value map in the payoff, checked exactly on a combination with a negative weight.
Part D: the expected payoff under the probabilities, and the value when the prices are the probabilities.
Part E: a probability vector with a negative entry, and one whose entries do not sum to 1, are rejected.

No random draws are used, so every run prints the same lines.
"""

from __future__ import annotations

from fractions import Fraction

Payoff = tuple[Fraction, ...]

STATE_PROBABILITIES: Payoff = (Fraction(1, 8), Fraction(3, 8), Fraction(3, 8), Fraction(1, 8))
PRICES: Payoff = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 4), Fraction(1, 5))
CLAIM: Payoff = (Fraction(100), Fraction(40), Fraction(0), Fraction(250))
OTHER: Payoff = (Fraction(0), Fraction(60), Fraction(120), Fraction(30))


def check_probabilities(probabilities: Payoff) -> None:
    """Raise ValueError unless every probability is positive and the probabilities sum to exactly 1."""
    if any(p <= 0 for p in probabilities):
        raise ValueError("state probabilities must be positive")
    if sum(probabilities, Fraction(0)) != 1:
        raise ValueError("state probabilities must sum to 1")


def security(state: int, n_states: int) -> Payoff:
    """The payoff vector of the Arrow-Debreu security for one state: 1 in that state and 0 in every other state."""
    return tuple(Fraction(1 if t == state else 0) for t in range(n_states))


def value(payoff: Payoff, prices: Payoff) -> Fraction:
    """The value of a claim, the sum over states of price times payoff, in cents, as an exact Fraction."""
    if len(payoff) != len(prices):
        raise ValueError("payoff and prices must have one entry per state")
    return sum((q * x for q, x in zip(prices, payoff, strict=True)), Fraction(0))


def expected_payoff(payoff: Payoff, probabilities: Payoff) -> Fraction:
    """The probability-weighted average payoff in cents, the sum over states of probability times payoff."""
    return sum((p * x for p, x in zip(probabilities, payoff, strict=True)), Fraction(0))


def combine(a: Fraction, x: Payoff, b: Fraction, y: Payoff) -> Payoff:
    """The payoff a times x plus b times y, state by state, with exact Fractions."""
    return tuple(a * xi + b * yi for xi, yi in zip(x, y, strict=True))


def main() -> None:
    """Print Parts A to E. Every value is an exact Fraction, so the output is reproducible."""
    n_states = len(STATE_PROBABILITIES)
    check_probabilities(STATE_PROBABILITIES)

    print("Part A: decomposition of the claim into Arrow-Debreu securities")
    rebuilt = [Fraction(0)] * n_states
    for state in range(n_states):
        payoff_of_security = security(state, n_states)
        coefficient = CLAIM[state]
        print(f"security {state} coefficient {coefficient} pays {tuple(str(z) for z in payoff_of_security)}")
        for t in range(n_states):
            rebuilt[t] += coefficient * payoff_of_security[t]
    print(f"rebuilt payoff {tuple(str(z) for z in rebuilt)} claim {tuple(str(z) for z in CLAIM)}")
    print(f"decomposition_exact {tuple(rebuilt) == CLAIM}")

    print("Part B: value under the prices, in cents")
    print(f"value_of_claim {value(CLAIM, PRICES)} value_of_other {value(OTHER, PRICES)}")

    print("Part C: linearity of the value in the payoff")
    combined = combine(Fraction(2), CLAIM, Fraction(-1, 2), OTHER)
    lhs = value(combined, PRICES)
    rhs = 2 * value(CLAIM, PRICES) - Fraction(1, 2) * value(OTHER, PRICES)
    print(f"combined_payoff {tuple(str(z) for z in combined)}")
    print(f"value_of_combination {lhs} linear_combination_of_values {rhs} equal {lhs == rhs}")

    print("Part D: expected payoff and value at the probabilities")
    expected = expected_payoff(CLAIM, STATE_PROBABILITIES)
    print(f"expected_payoff_claim {expected}")
    print(f"value_at_probability_prices {value(CLAIM, STATE_PROBABILITIES)}")
    print(f"value_at_prices {value(CLAIM, PRICES)} equal_to_expected_payoff {value(CLAIM, PRICES) == expected}")

    print("Part E: invalid probability vectors are rejected")
    negative = (Fraction(1, 2), Fraction(1, 2), Fraction(1, 2), Fraction(-1, 2))
    overweight = (Fraction(1, 8), Fraction(3, 8), Fraction(3, 8), Fraction(1, 4))
    for label, bad in (("negative", negative), ("overweight", overweight)):
        try:
            check_probabilities(bad)
        except ValueError as exc:
            print(f"rejected {label} message {exc}")


main()
