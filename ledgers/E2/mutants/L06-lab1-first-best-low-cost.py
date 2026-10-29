"""E2 L06 lab 1: a two-action effort problem with an affine contract under limited liability.

Inputs are illustrative, not data. The output is X = 1,000,000 cents (10,000 CU) on success and 0 on failure.
Success has probability 3/4 under high effort and 1/4 under low effort. High effort costs 100,000 cents (1,000 CU)
and low effort costs 0. The agent is risk neutral with quasi-linear utility, and its outside option is 0.
The contract pays the agent a fixed amount alpha and a share beta of the output on success, so the payment is
alpha on failure and alpha + beta * X on success.

Part A prints five illustrative shares from the grid of 101 shares 0.00 to 1.00 in steps of 0.01. Each row uses
alpha = 0 (limited liability, Assumption 3 on the page) and gives the agent's utility under each action, the action
the agent takes (high effort on a tie), and the principal's expected profit in cents.
Part B searches all 101 grid shares for the best one, and prints its profit beside the first-best profit and the
agency cost (first best minus best profit).
Part C: risk neutrality without limited liability. For three shares, alpha is set to the value that makes the
participation constraint bind, which can be negative, and the profit is printed. It equals the first-best profit.

Probabilities and expectations are exact Fractions. Money is computed exactly and printed in integer cents.
No random draws are used, so every run prints the same lines.
"""

from __future__ import annotations

import math
from fractions import Fraction

OUTPUT = 1_000_000  # cents on success
P_HIGH_EFFORT = Fraction(3, 4)  # probability of success under high effort
P_LOW_EFFORT = Fraction(1, 4)  # probability of success under low effort
COST_HIGH = 100_000  # cents, cost of high effort to the agent
COST_LOW = 0  # cents, cost of low effort to the agent

E_HIGH = P_HIGH_EFFORT * OUTPUT  # expected output under high effort, in cents
E_LOW = P_LOW_EFFORT * OUTPUT  # expected output under low effort, in cents
FIRST_BEST = E_HIGH - COST_LOW  # principal's profit when effort is observable and the agent is paid its cost


def cents(x: Fraction) -> int:
    """Round an exact amount half up to whole cents."""
    return math.floor(x + Fraction(1, 2))


def agent_choice(beta: Fraction) -> tuple[str, Fraction, Fraction]:
    """Return the action taken, and the utility under high effort and under low effort, at alpha = 0."""
    u_high = beta * E_HIGH - COST_HIGH
    u_low = beta * E_LOW - COST_LOW
    if u_high >= u_low and u_high >= 0:
        return "high", u_high, u_low
    if u_low >= 0:
        return "low", u_high, u_low
    return "refuses", u_high, u_low


def principal_profit(beta: Fraction) -> Fraction:
    """Principal's expected profit in cents at alpha = 0 and share beta, given the agent's choice."""
    action, _, _ = agent_choice(beta)
    if action == "high":
        return E_HIGH - beta * E_HIGH
    if action == "low":
        return E_LOW - beta * E_LOW
    return Fraction(0)


def main() -> None:
    print("Part A: contracts with alpha = 0, share beta from 0.00 to 1.00 (utilities and profit in cents)")
    print("beta | agent utility, high | agent utility, low | agent takes | principal profit")
    grid = [Fraction(k, 100) for k in range(0, 101)]
    for beta in grid:
        if beta not in (Fraction(0), Fraction(1, 10), Fraction(1, 5), Fraction(3, 10), Fraction(1)):
            continue
        action, u_high, u_low = agent_choice(beta)
        print(
            f"{float(beta):.2f} | {cents(u_high):19d} | {cents(u_low):18d} | {action:11s} | "
            f"{cents(principal_profit(beta)):16d}"
        )

    best = max(grid, key=lambda b: (principal_profit(b), -b))
    best_action, _, _ = agent_choice(best)
    print("Part B: the best grid share")
    print(f"best share on the grid: {float(best):.2f}, agent takes {best_action} effort")
    print(f"principal profit at the best share, in cents: {cents(principal_profit(best))}")
    print(f"first-best profit, in cents: {cents(FIRST_BEST)}")
    print(f"agency cost, first best minus best share, in cents: {cents(FIRST_BEST - principal_profit(best))}")
    print(f"low-effort profit at share 0.00, in cents: {cents(principal_profit(Fraction(0)))}")

    print("Part C: risk neutral agent, alpha may be negative (no limited liability)")
    for beta in (Fraction(1, 5), Fraction(1, 2), Fraction(1)):
        alpha = COST_HIGH - beta * E_HIGH
        profit = E_HIGH - (alpha + beta * E_HIGH)
        print(f"beta = {float(beta):.2f}: alpha = {cents(alpha)} cents, principal profit = {cents(profit)} cents")
    for beta in (Fraction(1, 5), Fraction(1, 2), Fraction(1)):
        alpha = COST_HIGH - beta * E_HIGH
        profit = E_HIGH - (alpha + beta * E_HIGH)
        print(f"beta = {float(beta):.2f}: profit equals first-best profit: {profit == FIRST_BEST}")


main()
