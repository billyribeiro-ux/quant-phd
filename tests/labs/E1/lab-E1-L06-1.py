"""E1 L06 lab 1: Cournot best responses, their iteration, and the Bertrand fee, on exact grids.

Inputs are illustrative parameters, not data. Trade demand is Q(f) = a - b f units at a fee of f cents per unit, and
each exchange has a constant marginal cost of c cents per unit. Write d = a - b c, which is the volume at which the fee
equals marginal cost. Three cases are run: the reference case (a, b, c) = (120, 1, 20) and two further cases with the
same structure. No random draws are used, and no file is read.

Part A: the Cournot best response max(0, (d - q_j) / 2) is compared with the output that maximises an exchange's profit
q_i (d - q_i - q_j) / b over the grid of outputs i / 12 units, for each rival output q_j in a fixed list, skipping
any that exceeds d. Profit is in cents. The lab asserts that the closed form lies on the grid for each rival output
tested, and that the grid maximiser equals it; the printed counts are the rival outputs that passed both assertions.
Part B: simultaneous best responses are iterated from zero output for 30 steps, in exact Fractions. The lab checks that
the symmetric iterate equals (d / 3) (1 - (-1/2)^t) at every step t, and prints the first step at which the iterate is
within 10^-6 units of d / 3.
Part C: with the rival's fee at marginal cost, the lab scans fees in steps of 1/10 cent from 0 to a / b and counts the
fees that earn the largest profit. For four rival fees above marginal cost, it compares the profit from undercutting by
1/1000 cent with the profit from sharing the market at the rival's fee.

Every comparison is made on exact values. The grids are finite, so the lab checks these inputs only. The proofs that
cover all inputs are on the page.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction

CASES = ((120, 1, 20), (90, 3, 10), (200, 4, 5))  # (a, b, c): demand intercept, demand slope, marginal cost
RIVAL_OUTPUT_FRACTIONS = (Fraction(0), Fraction(10), Fraction(25), Fraction(100, 3), Fraction(50), Fraction(100))
OUTPUT_STEP = Fraction(1, 12)
FEE_STEP = Fraction(1, 10)
UNDERCUT = Fraction(1, 1000)
ITERATIONS = 30
TOLERANCE = Fraction(1, 10**6)


def margin_gap(a: int, b: int, c: int) -> Fraction:
    """d = a - b c in units: the volume at which the fee a/b - Q/b equals the marginal cost c."""
    return Fraction(a - b * c)


def cournot_profit(q_own: Fraction, q_rival: Fraction, b: int, d: Fraction) -> Fraction:
    """Profit in cents of an exchange trading q_own units against a rival trading q_rival units: q_own (d - Q) / b."""
    return q_own * (d - q_own - q_rival) / b


def best_response(q_rival: Fraction, d: Fraction) -> Fraction:
    """The closed-form Cournot best response max(0, (d - q_rival) / 2) in units."""
    return max(Fraction(0), (d - q_rival) / 2)


def grid_best_response(q_rival: Fraction, b: int, d: Fraction) -> Fraction:
    """The output on the grid i / 12, for i from 0 to 12 d, with the largest profit against q_rival."""
    best_q, best_pi = Fraction(0), None
    for i in range(int(d / OUTPUT_STEP) + 1):
        q = i * OUTPUT_STEP
        pi = cournot_profit(q, q_rival, b, d)
        if best_pi is None or pi > best_pi:
            best_q, best_pi = q, pi
    return best_q


def bertrand_profit(f_own: Fraction, f_rival: Fraction, a: int, b: int, c: int) -> Fraction:
    """Profit in cents at fee f_own. The lower fee takes the demand a - b f units; a tie splits it evenly."""
    demand = max(Fraction(0), a - b * f_own)
    if f_own < f_rival:
        volume = demand
    elif f_own == f_rival:
        volume = demand / 2
    else:
        volume = Fraction(0)
    return volume * (f_own - c)


def decimal_text(x: Fraction) -> str:
    """The value of x as a decimal at 60 significant digits. It is checked to be exact, so no value is rounded."""
    with localcontext() as ctx:
        ctx.prec = 60
        text = format(Decimal(x.numerator) / Decimal(x.denominator), "f")
    if Fraction(text) != x:
        raise AssertionError(f"{x} is not exact at 60 significant digits")
    return text


def part_a() -> None:
    print("Part A: Cournot best response against the grid maximiser of profit")
    for a, b, c in CASES:
        d = margin_gap(a, b, c)
        checked = 0
        for q_rival in RIVAL_OUTPUT_FRACTIONS:
            if q_rival > d:
                continue
            closed = best_response(q_rival, d)
            on_grid = (closed / OUTPUT_STEP).denominator == 1
            grid = grid_best_response(q_rival, b, d)
            if not on_grid or grid != closed:
                raise AssertionError(f"best response mismatch at a={a}, b={b}, c={c}, rival {q_rival}")
            checked += 1
        print(f"  (a, b, c) = ({a}, {b}, {c}), d = {d}: {checked} rival outputs, grid equals closed form at each")


def part_b() -> None:
    print("Part B: simultaneous best responses from zero output")
    for a, b, c in CASES:
        d = margin_gap(a, b, c)
        q = Fraction(0)
        first_within = None
        for t in range(ITERATIONS + 1):
            if q != d / 3 * (1 - Fraction(-1, 2) ** t):
                raise AssertionError(f"iterate differs from the closed form at step {t}")
            if first_within is None and abs(q - d / 3) < TOLERANCE:
                first_within = t
            q = best_response(q, d)
        print(
            f"  (a, b, c) = ({a}, {b}, {c}): {ITERATIONS} steps match (d/3)(1 - (-1/2)^t) exactly; "
            f"first step within 10^-6 of d/3 is {first_within}"
        )
    d = margin_gap(120, 1, 20)
    q_last = Fraction(0)
    for _ in range(ITERATIONS):
        q_last = best_response(q_last, d)
    print(f"reference case after {ITERATIONS} steps: gap to d/3 = {q_last - d / 3}")


def part_c() -> None:
    print("Part C: Bertrand fees on a grid of 1/10 cent, and undercutting above marginal cost")
    for a, b, c in CASES:
        top = Fraction(a, b)
        fees = [k * FEE_STEP for k in range(int(top / FEE_STEP) + 1)]
        profits = [bertrand_profit(f, Fraction(c), a, b, c) for f in fees]
        best = max(profits)
        winners = [f for f, pi in zip(fees, profits, strict=True) if pi == best]
        below = [pi for f, pi in zip(fees, profits, strict=True) if f < c]
        all_at_or_above = all(f >= c for f in winners)
        print(
            f"  (a, b, c) = ({a}, {b}, {c}): rival at c; best own profit {decimal_text(best)} cents, attained at "
            f"{len(winners)} of {len(fees)} grid fees, all at or above c: {all_at_or_above}; "
            f"largest profit below c: {decimal_text(max(below))} cents"
        )
        for share in (Fraction(1, 20), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)):
            rival = c + (top - c) * share
            undercut = rival - UNDERCUT
            undercut_profit = bertrand_profit(undercut, rival, a, b, c)
            shared_profit = bertrand_profit(rival, rival, a, b, c)
            print(
                f"    rival fee {decimal_text(rival)}: undercut by 1/1000 earns {decimal_text(undercut_profit)} cents, "
                f"sharing earns {decimal_text(shared_profit)} cents, undercut is larger: "
                f"{undercut_profit > shared_profit}"
            )


def main() -> None:
    part_a()
    part_b()
    part_c()


main()
