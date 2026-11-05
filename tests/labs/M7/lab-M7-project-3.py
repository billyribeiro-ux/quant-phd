"""Rung 3 check: the certificate of the project, computed for three candidate answers to the worked example of Lab 1.

SIMULATED three-asset problem, not market data. The residuals are the four of the project page, restricted to the budget
and the lower bounds 0 <= w_i of this example, plus the check w_i <= 1 that the budget and those bounds imply (the
example has no sector caps and no turnover constraint). The primal residual is the largest violation among the
constraints it covers, and the dual residual is the largest violation of a multiplier's sign condition (zero when every
multiplier is non-negative). The stationarity residual is the largest absolute stationarity expression. The
complementary-slackness residual is not a violation: it is the largest absolute product of a multiplier and its
constraint. So a KKT point of this restricted problem, with its multipliers, has all four residuals at zero in exact
arithmetic. The three candidates are: the answer of Lab 1; the same answer with the sign of its bound multiplier
reversed; and the same answer with a weight moved by 1/1000 between the first two assets, which keeps the budget.
"""

from fractions import Fraction

# SIMULATED three-asset problem, not market data. The same numbers as Lab 1.
GAMMA = Fraction(2)
SIGMA = [
    [Fraction(4, 100), Fraction(1, 100), Fraction(0)],
    [Fraction(1, 100), Fraction(9, 100), Fraction(2, 100)],
    [Fraction(0), Fraction(2, 100), Fraction(16, 100)],
]
MU = [Fraction(5, 100), Fraction(3, 100), Fraction(-2, 100)]
N = 3


def residuals(w: list[Fraction], budget: Fraction, lower: list[Fraction], upper: list[Fraction]) -> dict[str, Fraction]:
    """Primal, stationarity, dual and complementary-slackness residuals of a weight vector and its multipliers."""
    primal = max([Fraction(0), abs(sum(w, Fraction(0)) - 1), *(-x for x in w), *(x - 1 for x in w)])
    stationarity = [
        GAMMA * sum((SIGMA[i][j] * w[j] for j in range(N)), Fraction(0)) - MU[i] + budget - lower[i] + upper[i]
        for i in range(N)
    ]
    dual = max([Fraction(0), *(-x for x in lower), *(-x for x in upper)])
    slackness = [abs(lower[i] * w[i]) for i in range(N)] + [abs(upper[i] * (w[i] - 1)) for i in range(N)]
    return {
        "primal": primal,
        "stationarity": max(abs(s) for s in stationarity),
        "dual": dual,
        "complementary": max(slackness),
    }


def main() -> None:
    # The Lab 1 answer: weights (9/11, 2/11, 0), budget multiplier -21/1100, and a lower-bound multiplier of 9/1100
    # on the third asset.
    w = [Fraction(9, 11), Fraction(2, 11), Fraction(0)]
    budget = Fraction(-21, 1100)
    lower = [Fraction(0), Fraction(0), Fraction(9, 1100)]
    upper = [Fraction(0), Fraction(0), Fraction(0)]
    zero = [Fraction(0)] * N
    report = residuals(w, budget, lower, upper)
    print("check A, Lab 1 answer:", {k: str(v) for k, v in report.items()})

    # Candidate B: the same weights with the sign of the bound multiplier reversed.
    flipped = [Fraction(0), Fraction(0), -Fraction(9, 1100)]
    report = residuals(w, budget, flipped, zero)
    print("check B, multiplier sign reversed:", {k: str(v) for k, v in report.items()})

    # Candidate C: a weight moved by 1/1000 from the second asset to the first, which keeps the budget.
    moved = [Fraction(9, 11) + Fraction(1, 1000), Fraction(2, 11) - Fraction(1, 1000), Fraction(0)]
    report = residuals(moved, budget, lower, upper)
    print("check C, weights moved by 1/1000:", {k: str(v) for k, v in report.items()})


main()
