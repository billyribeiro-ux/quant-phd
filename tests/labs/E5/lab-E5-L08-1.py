"""E5 L08 lab 1: the Keynesian-cross multiplier, checked against a finite sum of stages of spending.

Standard library only (fractions). No randomness and no network, so every run prints the same lines.

Every input is an illustrative value chosen for the arithmetic, not an estimate: a marginal propensity to consume
c = 3/5, autonomous consumption a = 20,000 cents, investment I = 15,000 cents, government spending G = 30,000 cents,
and a change in spending of 10,000 cents (100 CU). The model is closed and holds prices and the interest rate fixed.
Amounts are in whole cents; a stage can carry a fraction of a cent, and such amounts are printed as exact fractions.

Part A: the stages of spending. Stage k adds c^k times the change in spending. The running total after N stages equals
the closed form dG (1 - c^N) / (1 - c), checked exactly for N = 1 to 30.
Part B: the gap between the running total and the multiplier total dG / (1 - c), which equals dG c^N / (1 - c).
Part C: the equilibrium Y = (a + I + G) / (1 - c) solved exactly at two levels of G, and the change in output per
cent of spending, which is 1 / (1 - c).
Part D: the lump-sum tax case, where the change in output is -c dTax / (1 - c), and the balanced budget, whose
multiplier is 1.
"""

from __future__ import annotations

from fractions import Fraction

C = Fraction(3, 5)
AUTONOMOUS = 20_000
INVESTMENT = 15_000
GOVERNMENT = 30_000
DELTA_G = 10_000
DELTA_T = 10_000
MAX_STAGES = 30
REPORT_STAGES = (1, 5, 10, 20, 30)


def running_total(change: Fraction, marginal: Fraction, stages: int) -> Fraction:
    """Sum of the first `stages` stages of a change in spending: stage k (from 0) adds change * marginal**k."""
    return sum((change * marginal**k for k in range(stages)), Fraction(0))


def closed_form(change: Fraction, marginal: Fraction, stages: int) -> Fraction:
    """The finite geometric sum change * (1 - marginal**stages) / (1 - marginal), for marginal != 1."""
    return change * (1 - marginal**stages) / (1 - marginal)


def equilibrium(autonomous: int, investment: int, government: int, marginal: Fraction, tax: int) -> Fraction:
    """Output in cents where Y = a + c (Y - T) + I + G, solved exactly: (a - cT + I + G) / (1 - c)."""
    return (autonomous - marginal * tax + investment + government) / (1 - marginal)


def main() -> None:
    """Print Parts A to D in a fixed order. Each line is an exact fraction, an integer or a fixed string."""
    print(
        f"inputs: c {C} a {AUTONOMOUS} I {INVESTMENT} G {GOVERNMENT} dG {DELTA_G} dTax {DELTA_T} "
        f"multiplier {1 / (1 - C)}"
    )

    print("Part A: stages of spending in cents, and the running total")
    first_stages = [DELTA_G * C**k for k in range(5)]
    print("stage_amounts " + " ".join(str(x) for x in first_stages))
    totals = [running_total(Fraction(DELTA_G), C, n) for n in range(1, 6)]
    print("running_totals " + " ".join(str(x) for x in totals))
    matches = all(
        running_total(Fraction(DELTA_G), C, n) == closed_form(Fraction(DELTA_G), C, n) for n in range(1, MAX_STAGES + 1)
    )
    print(f"closed_form_matches_stages_N_1_to_{MAX_STAGES} {matches}")

    print("Part B: gap between the running total and the multiplier total, dG / (1 - c)")
    total = Fraction(DELTA_G) / (1 - C)
    print(f"multiplier_total_cents {total}")
    for n in REPORT_STAGES:
        gap = total - running_total(Fraction(DELTA_G), C, n)
        exact = gap == Fraction(DELTA_G) * C**n / (1 - C)
        print(f"stages {n} gap_cents {float(gap):.6f} equals_dG_c_N_over_1_minus_c {exact}")

    print("Part C: equilibrium output at two levels of government spending")
    y0 = equilibrium(AUTONOMOUS, INVESTMENT, GOVERNMENT, C, 0)
    y1 = equilibrium(AUTONOMOUS, INVESTMENT, GOVERNMENT + DELTA_G, C, 0)
    print(f"Y_before {y0} Y_after {y1} change {y1 - y0}")
    fixed_point = y1 == AUTONOMOUS + INVESTMENT + GOVERNMENT + DELTA_G + C * y1
    print(f"after_satisfies_Y_equals_a_plus_I_plus_G_plus_cY {fixed_point}")
    per_cent = equilibrium(AUTONOMOUS, INVESTMENT, GOVERNMENT + 1, C, 0) - y0
    print(f"change_per_cent_of_spending {per_cent} equals_one_over_one_minus_c {per_cent == 1 / (1 - C)}")
    print(f"change_equals_multiplier_times_dG {y1 - y0 == DELTA_G / (1 - C)}")

    print("Part D: lump-sum tax and the balanced budget")
    # A lump-sum tax increase of dTax lowers disposable income by dTax, so stage 0 of the tax case is -c dTax:
    # the first fall in consumption spending.
    tax_first = -C * DELTA_T
    tax_total = tax_first / (1 - C)
    tax_stages = [tax_first * C**k for k in range(3)]
    print("tax_stage_amounts " + " ".join(str(x) for x in tax_stages))
    tax_matches = all(running_total(tax_first, C, n) == closed_form(tax_first, C, n) for n in range(1, MAX_STAGES + 1))
    print(f"tax_closed_form_matches_stages_N_1_to_{MAX_STAGES} {tax_matches}")
    tax_change = equilibrium(AUTONOMOUS, INVESTMENT, GOVERNMENT, C, DELTA_T) - y0
    print(f"tax_change {tax_change} equals_minus_c_dTax_over_1_minus_c {tax_change == tax_total}")
    balanced = (y1 - y0) + tax_change
    print(f"balanced_budget_change {balanced} equals_spending_change {balanced == DELTA_G}")


main()
