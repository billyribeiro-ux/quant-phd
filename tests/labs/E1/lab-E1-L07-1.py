"""E1 L07 lab 1: surplus integrals in exact arithmetic, and the deadweight loss of each market structure.

Inputs are illustrative parameters, not data. Trade demand is Q(f) = a - b f units at a fee of f cents per unit, so the
inverse demand is P(Q) = (a - Q) / b cents per unit. Each exchange has a constant marginal cost of c cents per unit and
no fixed cost. The competitive benchmark sets the fee at c, which gives the volume d = a - b c. Three cases are run: the
reference case (a, b, c) = (120, 1, 20) and two further cases. No random draws are used, and no file is read.

Part A: the midpoint rule with n steps is applied to the integral of P over [0, Q] and to the integral of P - c over
[0, Q]. Both integrands are linear, so the midpoint rule is exact for every n. The lab checks equality with the
antiderivatives in exact Fractions for n = 1, 2, 10 and 97, at Q = d/2, 2d/3 and d, and checks that the total surplus
equals (2 d Q - Q^2) / (2 b) at the same volumes.
Part B: for the reference case, each structure's volume, fee, consumer surplus, producer surplus (the exchange profit,
since there is no fixed cost), total surplus and deadweight loss against the competitive total surplus are printed. The
Cournot figures are for the two exchanges together. Each money value is exact, followed by its integer-cent value, which
is the exact value rounded half up.
Part C: for each case, the lab checks that the deadweight loss equals (d - Q)^2 / (2 b) for every structure, that the
Bertrand loss is zero, that the monopoly loss exceeds the Cournot loss, which is positive, and that the monopoly profit
exceeds the Cournot profit of the two exchanges together.

Every comparison is made on exact values. The list of cases is finite, so the lab checks these inputs only. The closed
forms for every input are proved on the page.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from fractions import Fraction
from functools import partial

CASES = ((120, 1, 20), (90, 3, 10), (200, 4, 5))  # (a, b, c): demand intercept, demand slope, marginal cost
MIDPOINT_COUNTS = (1, 2, 10, 97)


def inverse_demand(q: Fraction, a: int, b: int) -> Fraction:
    """The fee in cents per unit at which q units trade: P(q) = (a - q) / b."""
    return (a - q) / b


def excess_price(q: Fraction, a: int, b: int, c: int) -> Fraction:
    """The margin P(q) - c in cents per unit at which the q-th unit adds to total surplus."""
    return inverse_demand(q, a, b) - c


def midpoint_integral(f: Callable[[Fraction], Fraction], lower: Fraction, upper: Fraction, n: int) -> Fraction:
    """Midpoint Riemann sum of f over [lower, upper] with n equal steps, in exact arithmetic."""
    step = (upper - lower) / n
    total = Fraction(0)
    for i in range(n):
        total += f(lower + (i + Fraction(1, 2)) * step) * step
    return total


def cents_half_up(x: Fraction) -> int:
    """The exact non-negative value x in whole cents, rounded half up to the nearest cent."""
    if x < 0:
        raise ValueError("cents_half_up is for non-negative values")
    return math.floor(x + Fraction(1, 2))


def total_surplus(q: Fraction, a: int, b: int, c: int) -> Fraction:
    """Total surplus W(q) = integral from 0 to q of (P(x) - c) dx, by the midpoint rule with n = 10."""
    return midpoint_integral(lambda x: excess_price(x, a, b, c), Fraction(0), q, 10)


def consumer_surplus(q: Fraction, fee: Fraction, a: int, b: int) -> Fraction:
    """Consumer surplus: the integral from 0 to q of P(x) dx, minus fee times q, by the midpoint rule with n = 10."""
    return midpoint_integral(lambda x: inverse_demand(x, a, b), Fraction(0), q, 10) - fee * q


def structures(a: int, b: int, c: int) -> dict[str, tuple[Fraction, Fraction]]:
    """Each structure's (volume in units, fee in cents): monopoly, Cournot with two exchanges, and Bertrand."""
    d = Fraction(a - b * c)
    return {
        "monopoly": (d / 2, Fraction(a + b * c, 2 * b)),
        "cournot": (2 * d / 3, Fraction(a + 2 * b * c, 3 * b)),
        "bertrand": (d, Fraction(c)),
    }


def part_a() -> None:
    print("Part A: midpoint sums of linear integrands equal the antiderivatives")
    for a, b, c in CASES:
        d = Fraction(a - b * c)
        for q in (d / 2, 2 * d / 3, d):
            exact_surplus = (2 * d * q - q * q) / (2 * b)
            exact_margin = (a * q - q * q / 2) / b - c * q
            exact_price = (a * q - q * q / 2) / b
            for n in MIDPOINT_COUNTS:
                margin_sum = midpoint_integral(partial(excess_price, a=a, b=b, c=c), Fraction(0), q, n)
                price_sum = midpoint_integral(partial(inverse_demand, a=a, b=b), Fraction(0), q, n)
                if margin_sum != exact_margin or price_sum != exact_price:
                    raise AssertionError(f"midpoint sum differs from the antiderivative at a={a}, b={b}, Q={q}, n={n}")
            if total_surplus(q, a, b, c) != exact_surplus:
                raise AssertionError(f"total surplus differs from (2 d Q - Q^2)/(2 b) at a={a}, b={b}, Q={q}")
        counts = ", ".join(str(n) for n in MIDPOINT_COUNTS)
        print(
            f"  (a, b, c) = ({a}, {b}, {c}), d = {d}: integrals of P and P - c equal the antiderivatives "
            f"for n = {counts} and Q = d/2, 2d/3, d"
        )


def part_b() -> None:
    a, b, c = CASES[0]
    d = Fraction(a - b * c)
    w_star = total_surplus(d, a, b, c)
    print(f"Part B: reference case (a, b, c) = ({a}, {b}, {c}), d = {d}, competitive total surplus {w_star}")
    for name, (q, fee) in structures(a, b, c).items():
        cs = consumer_surplus(q, fee, a, b)
        ps = (fee - c) * q
        w = total_surplus(q, a, b, c)
        dwl = w_star - w
        if cs + ps != w:
            raise AssertionError(f"{name}: consumer plus producer surplus differs from total surplus")
        print(
            f"  {name}: volume {q}, fee {fee}, consumer surplus {cs} ({cents_half_up(cs)} cents), "
            f"producer surplus {ps} ({cents_half_up(ps)} cents), total {w} ({cents_half_up(w)} cents), "
            f"deadweight loss {dwl} ({cents_half_up(dwl)} cents)"
        )


def part_c() -> None:
    print("Part C: deadweight loss, ordering and profit on every case")
    for a, b, c in CASES:
        d = Fraction(a - b * c)
        w_star = total_surplus(d, a, b, c)
        losses: dict[str, Fraction] = {}
        profits: dict[str, Fraction] = {}
        for name, (q, fee) in structures(a, b, c).items():
            dwl = w_star - total_surplus(q, a, b, c)
            if dwl != (d - q) ** 2 / (2 * b):
                raise AssertionError(f"{name} deadweight loss differs from (d - Q)^2 / (2 b) at a={a}, b={b}, c={c}")
            losses[name] = dwl
            profits[name] = (fee - c) * q
        if losses["bertrand"] != 0:
            raise AssertionError("Bertrand deadweight loss is not zero")
        if not losses["monopoly"] > losses["cournot"] > 0:
            raise AssertionError("the ordering monopoly loss > Cournot loss > 0 fails")
        if not profits["monopoly"] > profits["cournot"]:
            raise AssertionError("monopoly profit does not exceed the Cournot profit of the two exchanges")
        share_m = losses["monopoly"] / w_star
        share_c = losses["cournot"] / w_star
        print(
            f"  (a, b, c) = ({a}, {b}, {c}), d = {d}: loss monopoly {losses['monopoly']}, Cournot {losses['cournot']}, "
            f"Bertrand {losses['bertrand']}; loss as a share of the competitive total surplus: monopoly {share_m}, "
            f"Cournot {share_c}; profit monopoly {profits['monopoly']}, Cournot two exchanges together "
            f"{profits['cournot']}"
        )


def main() -> None:
    part_a()
    part_b()
    part_c()


main()
