"""CF1 lab L01: net present value of SIMULATED projects.

SIMULATED: no project in this lab is a real company's. The fixed project in Part A and Part D and the
counterexample in Part E are typed in; the projects in Parts B and C are generated from a seeded random number
generator. Money is entered in integer cents; discounted values are computed in floating point and printed
in dollars to two decimals. Standard library only; no network; every result printed is computed by the code below.
The section titles restate typed-in inputs.
"""

from __future__ import annotations

import itertools
import random
from collections.abc import Sequence

SEED = 20261027
RATE = 0.08
TOLERANCE = 1e-6


def npv_dollars(flows_cents: Sequence[int], rate: float) -> float:
    """Net present value in dollars of flows_cents[t], received at the end of period t, at a rate per period.

    The rate must exceed -1, so that every discount factor (1 + rate) ** -t is finite and positive.
    """
    if rate <= -1.0:
        raise ValueError("the rate must exceed -1")
    total = 0.0
    for t, flow in enumerate(flows_cents):
        total += flow / 100.0 / (1.0 + rate) ** t
    return total


def annuity_npv_dollars(outlay_cents: int, level_cents: int, years: int, rate: float) -> float:
    """Closed form in dollars: minus the outlay plus level times the M1 annuity factor (1 - (1 + r)^-n) / r."""
    factor = (1.0 - (1.0 + rate) ** -(years + 1)) / rate
    return -outlay_cents / 100.0 + level_cents / 100.0 * factor


def replication_balance_path(flows_cents: Sequence[int], rate: float) -> list[float]:
    """Balance of the loan that replicates the project, in dollars, at each date.

    The owner borrows NPV minus the date-0 flow at date 0 and then pays the project's later flows out of the loan.
    The balance B_t satisfies B_0 = NPV - C_0 and B_t = (1 + rate) * B_(t-1) - C_t, and must end at zero.
    """
    balance = npv_dollars(flows_cents, rate) - flows_cents[0] / 100.0
    path = [balance]
    for t in range(1, len(flows_cents)):
        balance = (1.0 + rate) * balance - flows_cents[t] / 100.0
        path.append(balance)
    return path


def main() -> None:
    rng = random.Random(SEED)

    print("A. One SIMULATED five-year project: outlay of 10,000 dollars, then yearly inflows, in dollars")
    project = [-1_000_000, 300_000, 320_000, 340_000, 360_000, 380_000]
    print("flows:", " ".join(f"{flow / 100:.2f}" for flow in project))
    rates = [0.00, 0.05, 0.10, 0.15, 0.20]
    values = [npv_dollars(project, r) for r in rates]
    for r, value in zip(rates, values, strict=True):
        print(f"NPV at {r:.2f}: {value:.2f}")
    decreasing = all(a > b for a, b in itertools.pairwise(values))
    print("NPV strictly decreasing in the rate on this grid:", decreasing)
    print(f"NPV at the lab rate {RATE:.2f}: {npv_dollars(project, RATE):.2f}")

    print()
    print("B. Two hundred seeded level-annuity projects: sum of discounted flows against the closed form")
    worst = 0.0
    accepted = 0
    for _ in range(200):
        outlay = rng.randint(50_000, 2_000_000)
        level = rng.randint(10_000, 400_000)
        years = rng.randint(1, 15)
        rate = rng.uniform(0.02, 0.15)
        flows = [-outlay] + [level] * years
        summed = npv_dollars(flows, rate)
        closed = annuity_npv_dollars(outlay, level, years, rate)
        worst = max(worst, abs(summed - closed))
        if summed > 0:
            accepted += 1
    print("largest gap between the two computations, in dollars, below 1e-6:", worst < TOLERANCE)
    print("projects with NPV above zero, out of 200:", accepted)

    print()
    print("C. Additivity: NPV of the sum of two projects equals the sum of their NPVs (fifty seeded pairs)")
    additive = True
    for _ in range(50):
        first = [rng.randint(-500_000, 100_000) for _ in range(4)]
        second = [rng.randint(-500_000, 100_000) for _ in range(4)]
        combined = [a + b for a, b in zip(first, second, strict=True)]
        gap = npv_dollars(combined, RATE) - (npv_dollars(first, RATE) + npv_dollars(second, RATE))
        additive = additive and abs(gap) < TOLERANCE
    print("additivity holds to within 1e-6 dollars for all fifty pairs:", additive)

    print()
    print("D. Replication: a loan of NPV minus the date-0 flow pays the later flows and ends at zero")
    path = replication_balance_path(project, RATE)
    print(f"opening loan balance at date 0, in dollars: {path[0]:.2f}")
    print(f"balance at date 5, in dollars: {path[-1]:.6f}")
    print("the balance ends at zero to within 1e-6 dollars:", abs(path[-1]) < TOLERANCE)

    print()
    print("E. A positive undiscounted sum can hide a negative NPV")
    counterexample = [-100_000, 60_000, 60_000]
    print(f"undiscounted sum, in dollars: {sum(counterexample) / 100:.2f}")
    print(f"NPV at 20 percent, in dollars: {npv_dollars(counterexample, 0.20):.2f}")


main()
