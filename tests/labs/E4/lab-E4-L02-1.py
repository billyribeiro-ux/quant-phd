"""E4 L02 lab 1: an Arrow-Debreu equilibrium of a two-agent exchange economy with logarithmic utility, exact.

Inputs are illustrative numbers, not data. There are three states with probabilities PROBS, which sum to exactly 1.
One good is delivered in each state. Agent i has the strictly positive endowment ENDOWMENTS[i] in those three states,
and the expected utility of a bundle x is the sum over states of PROBS[s] times ln(x[s]). All quantities are exact
Fractions, and no rounding occurs.

The economy is solved in closed form. The price of the good in state s is q[s] = PROBS[s] / aggregate[s], which
gives q times the aggregate endowment equal to 1 (the normalization). Each agent's wealth is w = q times its
endowment, and its demand is x[s] = PROBS[s] * w / q[s], with multiplier 1 / w.

Part A: the economy, the aggregate endowment and each agent's share of wealth, which sum to 1.
Part B: the equilibrium price vector and the normalization.
Part C: each agent's demand, with its budget residual, and the market-clearing residual in each state, all zero.
Part D: the first-order ratio PROBS[s] / (x[s] q[s]) for each agent in each state, which equals the agent's multiplier.
Part E: demand is unchanged when every price is multiplied by 3, so the prices are fixed only up to scale.
Part F: an economy with a negative endowment is rejected with a ValueError.

No random draws are used, so every run prints the same lines.
"""

from __future__ import annotations

from fractions import Fraction

Payoff = tuple[Fraction, ...]

PROBS: Payoff = (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4))
ENDOWMENTS: tuple[Payoff, ...] = (
    (Fraction(3), Fraction(4), Fraction(1)),
    (Fraction(1), Fraction(4), Fraction(3)),
)


def check_economy(probabilities: Payoff, endowments: tuple[Payoff, ...]) -> None:
    """Raise ValueError unless the probabilities are positive and sum to 1, and every endowment entry is positive."""
    if any(p <= 0 for p in probabilities):
        raise ValueError("state probabilities must be positive")
    if sum(probabilities, Fraction(0)) != 1:
        raise ValueError("state probabilities must sum to 1")
    for endowment in endowments:
        if any(e <= 0 for e in endowment):
            raise ValueError("endowments must be strictly positive in every state")


def aggregate(endowments: tuple[Payoff, ...]) -> Payoff:
    """The aggregate endowment in each state, the sum of the agents' endowments."""
    n_states = len(endowments[0])
    return tuple(sum((e[s] for e in endowments), Fraction(0)) for s in range(n_states))


def dot(a: Payoff, b: Payoff) -> Fraction:
    """The inner product of two vectors with one entry per state, as an exact Fraction."""
    return sum((x * y for x, y in zip(a, b, strict=True)), Fraction(0))


def equilibrium_prices(probabilities: Payoff, total: Payoff) -> Payoff:
    """The price of the good in each state, q[s] = probabilities[s] / total[s], normalized so that q . total = 1."""
    return tuple(p / t for p, t in zip(probabilities, total, strict=True))


def demand(probabilities: Payoff, prices: Payoff, wealth: Fraction) -> Payoff:
    """The logarithmic-utility demand x[s] = probabilities[s] * wealth / prices[s], for a positive wealth."""
    if wealth <= 0:
        raise ValueError("wealth must be positive")
    return tuple(p * wealth / q for p, q in zip(probabilities, prices, strict=True))


def main() -> None:
    """Print Parts A to F. Every value is an exact Fraction, so the output is reproducible."""
    check_economy(PROBS, ENDOWMENTS)
    total = aggregate(ENDOWMENTS)
    prices = equilibrium_prices(PROBS, total)
    wealth = [dot(prices, e) for e in ENDOWMENTS]

    print("Part A: economy, aggregate endowment and wealth shares")
    print(f"probabilities {tuple(str(p) for p in PROBS)} aggregate {tuple(str(z) for z in total)}")
    for i, e in enumerate(ENDOWMENTS, start=1):
        print(f"agent {i} endowment {tuple(str(z) for z in e)} wealth_share {wealth[i - 1]}")
    print(f"shares_sum_to_one {sum(wealth, Fraction(0)) == 1}")

    print("Part B: equilibrium prices and the normalization")
    print(f"prices {tuple(str(q) for q in prices)}")
    print(f"prices_dot_aggregate {dot(prices, total)}")

    print("Part C: demands, budget residuals and market clearing")
    demands = [demand(PROBS, prices, w) for w in wealth]
    for i, (x, e) in enumerate(zip(demands, ENDOWMENTS, strict=True), start=1):
        print(f"agent {i} demand {tuple(str(z) for z in x)}")
        print(f"agent {i} budget_residual {dot(prices, x) - dot(prices, e)}")
    for s in range(len(PROBS)):
        clearing = sum((x[s] for x in demands), Fraction(0)) - total[s]
        print(f"state {s} market_clearing_residual {clearing}")
    excess = tuple(
        sum((x[s] - e[s] for x, e in zip(demands, ENDOWMENTS, strict=True)), Fraction(0)) for s in range(len(PROBS))
    )
    print(f"walras_law_residual {dot(prices, excess)}")

    print("Part D: first-order ratio PROBS[s] / (x[s] q[s]) for each agent")
    for i, x in enumerate(demands, start=1):
        ratios = tuple(PROBS[s] / (x[s] * prices[s]) for s in range(len(PROBS)))
        same = all(r == 1 / wealth[i - 1] for r in ratios)
        print(f"agent {i} ratios {tuple(str(r) for r in ratios)} equal_to_one_over_wealth {same}")

    print("Part E: scaling every price by 3 leaves demand unchanged")
    scaled = tuple(3 * q for q in prices)
    for i, e in enumerate(ENDOWMENTS, start=1):
        again = demand(PROBS, scaled, dot(scaled, e))
        print(f"agent {i} demand_unchanged {again == demands[i - 1]}")

    print("Part F: an economy with a non-positive endowment is rejected")
    bad = ((Fraction(3), Fraction(4), Fraction(1)), (Fraction(1), Fraction(0), Fraction(3)))
    try:
        check_economy(PROBS, bad)
    except ValueError as exc:
        print(f"rejected message {exc}")


main()
