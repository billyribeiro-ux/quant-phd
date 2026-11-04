"""E4 L03 lab 1: marginal rates of substitution at an Arrow-Debreu equilibrium, and a finite Pareto search.

Inputs are illustrative numbers, not data. This is the economy of Lesson L02: three states with probabilities PROBS,
an aggregate endowment equal to the sum of ENDOWMENTS, and two agents. Agent i's expected utility of a bundle x is the
sum over states of PROBS[s] times ln(x[s]). The equilibrium prices and demands are those of Lesson L02, which are
computed here in exact Fractions.

Part A: the marginal rate of substitution between states, (PROBS[s] / x[s]) / (PROBS[t] / x[t]), for each agent at
the equilibrium, checked exactly against the price ratio q[s] / q[t]. States are numbered 1 to 3 in the printed output,
as in the lesson, and indexed 0 to 2 in the code, so printed "states 1 2" is the code pair (0, 1).
Part B: a finite search. Agent 1 receives the fraction f[s] of the aggregate in state s, with f[s] in the grid
GRID, and agent 2 receives the rest. The search counts the grid allocations that make one agent strictly better off
and no agent worse off than the equilibrium, and the same count against the endowment allocation.

The utilities in Part B are floating-point. A comparison counts as worse when the new utility is below the reference by
more than TOL, and as better when it is above the reference by more than TOL, with TOL = 1e-12.

No random draws are used, so every run prints the same lines.
"""

from __future__ import annotations

import math
from fractions import Fraction
from itertools import product

Payoff = tuple[Fraction, ...]

PROBS: Payoff = (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4))
ENDOWMENTS: tuple[Payoff, ...] = (
    (Fraction(3), Fraction(4), Fraction(1)),
    (Fraction(1), Fraction(4), Fraction(3)),
)
GRID: tuple[Fraction, ...] = (Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1))
TOL = 1e-12


def dot(a: Payoff, b: Payoff) -> Fraction:
    """The inner product of two vectors with one entry per state, as an exact Fraction."""
    return sum((x * y for x, y in zip(a, b, strict=True)), Fraction(0))


def aggregate(endowments: tuple[Payoff, ...]) -> Payoff:
    """The aggregate endowment in each state."""
    n_states = len(endowments[0])
    return tuple(sum((e[s] for e in endowments), Fraction(0)) for s in range(n_states))


def equilibrium(probabilities: Payoff, endowments: tuple[Payoff, ...]) -> tuple[Payoff, Payoff, Payoff]:
    """Prices q[s] = PROBS[s] / aggregate[s], and demands x[s] = PROBS[s] * w / q[s] with wealth w = q . endowment."""
    total = aggregate(endowments)
    prices = tuple(p / t for p, t in zip(probabilities, total, strict=True))
    demands = []
    for endowment in endowments:
        wealth = dot(prices, endowment)
        demands.append(tuple(p * wealth / q for p, q in zip(probabilities, prices, strict=True)))
    return prices, demands[0], demands[1]


def utility(probabilities: Payoff, bundle: Payoff) -> float:
    """The expected log utility, the sum of PROBS[s] * ln(bundle[s]) as a float; a zero entry gives minus infinity."""
    total = 0.0
    for p, x in zip(probabilities, bundle, strict=True):
        if x == 0:
            return -math.inf
        total += float(p) * math.log(float(x))
    return total


def improves(candidate: tuple[float, float], reference: tuple[float, float]) -> bool:
    """True when no agent is worse off by more than TOL and at least one agent is better off by more than TOL."""
    no_one_worse = all(c >= r - TOL for c, r in zip(candidate, reference, strict=True))
    someone_better = any(c > r + TOL for c, r in zip(candidate, reference, strict=True))
    return no_one_worse and someone_better


def grid_allocations(total: Payoff) -> list[tuple[Payoff, Payoff]]:
    """Every allocation with agent 1 receiving GRID[k] of the aggregate in each state and agent 2 the rest."""
    found: list[tuple[Payoff, Payoff]] = []
    for fractions in product(GRID, repeat=len(total)):
        first = tuple(f * t for f, t in zip(fractions, total, strict=True))
        second = tuple((1 - f) * t for f, t in zip(fractions, total, strict=True))
        found.append((first, second))
    return found


def main() -> None:
    """Print Parts A and B. Exact Fractions in Part A and integer counts in Part B make the output reproducible."""
    total = aggregate(ENDOWMENTS)
    prices, x1, x2 = equilibrium(PROBS, ENDOWMENTS)
    print("Part A: marginal rates of substitution at the equilibrium")
    print(f"equilibrium_prices {tuple(str(q) for q in prices)}")
    for left, right in ((0, 1), (0, 2), (1, 2)):
        price_ratio = prices[left] / prices[right]
        mrs = []
        for bundle in (x1, x2):
            mrs.append((PROBS[left] / bundle[left]) / (PROBS[right] / bundle[right]))
        same = mrs[0] == mrs[1] == price_ratio
        print(
            f"states {left + 1} {right + 1} mrs_agent_1 {mrs[0]} mrs_agent_2 {mrs[1]} "
            f"price_ratio {price_ratio} all_equal {same}"
        )
    feasible = all(x1[s] + x2[s] == total[s] for s in range(len(total)))
    print(f"equilibrium_feasible {feasible}")

    print("Part B: finite search over the grid of allocations")
    reference_eq = (utility(PROBS, x1), utility(PROBS, x2))
    reference_endowment = (utility(PROBS, ENDOWMENTS[0]), utility(PROBS, ENDOWMENTS[1]))
    candidates = grid_allocations(total)
    print(f"grid_allocations {len(candidates)} grid_points_per_state {len(GRID)}")
    improving_eq = [(a, b) for a, b in candidates if improves((utility(PROBS, a), utility(PROBS, b)), reference_eq)]
    print(f"pareto_improvements_on_grid_at_equilibrium {len(improving_eq)}")
    improving_endow = [
        (a, b) for a, b in candidates if improves((utility(PROBS, a), utility(PROBS, b)), reference_endowment)
    ]
    print(f"pareto_improvements_on_grid_at_endowment {len(improving_endow)}")
    if improving_endow:
        first_a, first_b = improving_endow[0]
        print(
            f"first_improvement_at_endowment agent_1 {tuple(str(z) for z in first_a)} "
            f"agent_2 {tuple(str(z) for z in first_b)}"
        )


main()
