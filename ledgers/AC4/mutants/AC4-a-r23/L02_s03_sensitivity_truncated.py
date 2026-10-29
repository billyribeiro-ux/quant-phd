"""AC4 lab L02: break-even under a mixed cost structure with a step cost.

SIMULATED: a single product in a single month. Every figure is invented for this lab and is not
any firm's. Money is integer cents and volume is integer units. Break-even points are exact
Fractions; a value is shown with two decimals only when it is printed. Standard library only;
no network; every number printed is computed below.

Cost structure, all in cents:
  price per unit                      2500
  variable cost per unit              1150 (materials and labour 1000; variable part of utilities 150)
  fixed cost per month                120000 (rent and the fixed part of utilities)
  step cost per month, above 2000 units  2700000 (a second shift)
"""

from __future__ import annotations

from fractions import Fraction

PRICE_CENTS = 2500
VARIABLE_CENTS = 1150
FIXED_CENTS = 120_000
STEP_CENTS = 2_700_000
STEP_ABOVE_UNITS = 2000
SCAN_LIMIT_UNITS = 5000
PLANNED_UNITS = 2500


def contribution_margin(price: int, variable: int) -> int:
    """Contribution margin per unit in cents: price minus variable cost. Raises ValueError if it is not positive."""
    margin = price - variable
    if margin <= 0:
        raise ValueError("contribution margin per unit must be positive for a break-even point to exist")
    return margin


def operating_income(units: int) -> int:
    """Operating income in cents at an integer volume of units. Raises ValueError for negative units.

    The step cost applies to every unit above STEP_ABOVE_UNITS, so the function jumps down at 2001 units.
    """
    if units < 0:
        raise ValueError("units must be a non-negative integer")
    step = STEP_CENTS if units > STEP_ABOVE_UNITS else 0
    return (PRICE_CENTS - VARIABLE_CENTS) * units - FIXED_CENTS - step


def break_even(fixed_cents: int, margin_cents: int) -> Fraction:
    """The single-segment break-even volume F / m, as an exact Fraction, in units."""
    return Fraction(fixed_cents, margin_cents)


def loss_runs(limit: int) -> list[tuple[int, int]]:
    """Maximal inclusive runs of integer volumes in [0, limit] at which operating income is negative."""
    runs: list[tuple[int, int]] = []
    start: int | None = None
    for units in range(limit + 1):
        loss = operating_income(units) < 0
        if loss and start is None:
            start = units
        elif not loss and start is not None:
            runs.append((start, units - 1))
            start = None
    if start is not None:
        runs.append((start, limit))
    return runs


def dollars(cents: int | Fraction) -> str:
    """Format cents as USD with two decimals, half up, for printing only."""
    value = Fraction(cents)
    scaled = (2 * value.numerator + value.denominator) // (2 * value.denominator)
    sign = "-" if scaled < 0 else ""
    whole, part = divmod(abs(scaled), 100)
    return f"{sign}{whole}.{part:02d}"


def main() -> None:
    """Print the margin, the single-formula break-even, the exact loss runs, and the sensitivities."""
    margin = contribution_margin(PRICE_CENTS, VARIABLE_CENTS)
    print(f"margin_cents_per_unit {margin} ratio {Fraction(margin, PRICE_CENTS)}")
    first = break_even(FIXED_CENTS, margin)
    first_whole = -(-first.numerator // first.denominator)
    print(f"single_formula_break_even_units {float(first):.2f} first_whole_unit {first_whole}")
    print(f"check operating_income(88) {dollars(operating_income(88))}", end=" ")
    print(f"operating_income(89) {dollars(operating_income(89))}")
    revenue = PRICE_CENTS * first
    print(f"revenue_break_even_usd {dollars(revenue)}")
    wrong = break_even(FIXED_CENTS + STEP_CENTS, margin)
    print(f"formula_with_step_cost_units {float(wrong):.2f}")
    for lo, hi in loss_runs(SCAN_LIMIT_UNITS):
        print(f"loss run units {lo} to {hi}")
    planned = operating_income(PLANNED_UNITS)
    print(f"planned_units {PLANNED_UNITS} operating_income_usd {dollars(planned)}")
    upper = break_even(FIXED_CENTS + STEP_CENTS, margin)
    safety = PLANNED_UNITS - upper
    print(f"margin_of_safety_units {float(safety):.2f} share_of_planned {float(safety / PLANNED_UNITS * 100):.2f}")
    contribution = margin * PLANNED_UNITS
    leverage = Fraction(contribution, planned)
    up_one = operating_income(PLANNED_UNITS + PLANNED_UNITS // 100)
    growth = Fraction(up_one - planned, planned) * 100
    print(f"operating_leverage {float(leverage):.2f} volume_up_1pct_income_change_pct {float(growth):.2f}")
    raised = break_even(FIXED_CENTS + 10_000, margin)
    print(f"fixed_plus_10000_cents_moves_break_even_units {int(float(raised - first) * 100) / 100:.2f}")
    for label, args in (("zero margin", (2500, 2500)), ("negative units", None)):
        try:
            if args is None:
                operating_income(-1)
            else:
                break_even(FIXED_CENTS, contribution_margin(*args))
        except ValueError as exc:
            print(f"ValueError for {label}: {exc}")
        else:
            print(f"no error for {label}")


main()
