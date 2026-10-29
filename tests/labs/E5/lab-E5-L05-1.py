"""E5 L05 lab 1: the linear AD-AS equilibrium, a demand shift traced exactly, and the long-run price level.

Inputs are illustrative model units, not data. Output is in index points, the price level is an index with
expected price level 1 at the base date, and every value is an exact fraction. Nothing is random.

The model (Assumptions A1 to A3 of Lesson 5): AD is Y = a - eta P with a, eta > 0; short-run AS is
Y = Ybar + nu (P - Pe) with nu > 0; potential output Ybar = 1000 index points; expected price level Pe = 1.

Part A: the short-run equilibrium price and output at a = 1160, and the residual of both equations.
Part B: a demand shift of +30 in a, the new equilibrium, and the exact changes beside their formulas: the price
change 30/(eta+nu) and the output change 30 nu/(eta+nu). It also prints the output share nu/(eta+nu) and the
price change per unit of a, 1/(eta+nu).
Part C: the long-run equilibrium, where expected prices equal the actual price, before and after the shift.
Part D: the output share nu/(eta+nu) and the price change for five slopes nu of the short-run AS curve.

Rounding rule: a printed decimal is the exact fraction rounded half to even at six decimal places.
"""

from __future__ import annotations

from fractions import Fraction

YBAR = Fraction(1000)
ETA = Fraction(100)
NU = Fraction(200)
PE = Fraction(1)
A_BASE = Fraction(1160)
SHOCK = Fraction(30)


def fmt(x: Fraction) -> str:
    """The exact value rounded half to even at six decimal places, with a minus sign where needed."""
    scaled = round(x * 10**6)
    sign = "-" if scaled < 0 else ""
    whole, frac = divmod(abs(scaled), 10**6)
    return f"{sign}{whole}.{frac:06d}"


def short_run(a: Fraction, eta: Fraction, nu: Fraction, ybar: Fraction, pe: Fraction) -> tuple[Fraction, Fraction]:
    """The price and output where AD (Y = a - eta P) meets short-run AS (Y = ybar + nu (P - pe)), with eta + nu > 0."""
    price = (a - ybar + nu * pe) / (eta + nu)
    return price, a - eta * price


def long_run(a: Fraction, eta: Fraction, ybar: Fraction) -> Fraction:
    """The price where expected prices equal the actual price and output is potential: Ybar = a - eta P."""
    return (a - ybar) / eta


def main() -> None:
    """Print Parts A to D. Every line is computed from the exact fractions above."""
    print("Part A: short-run equilibrium at a = 1160")
    p0, y0 = short_run(A_BASE, ETA, NU, YBAR, PE)
    print(f"price {fmt(p0)} output {fmt(y0)}")
    print(f"ad_residual {fmt(y0 - (A_BASE - ETA * p0))} as_residual {fmt(y0 - (YBAR + NU * (p0 - PE)))}")
    print(f"output_above_potential {y0 > YBAR}")

    print("Part B: demand shift of +30 in a")
    p1, y1 = short_run(A_BASE + SHOCK, ETA, NU, YBAR, PE)
    print(f"price {fmt(p1)} output {fmt(y1)}")
    print(f"delta_price {fmt(p1 - p0)} delta_output {fmt(y1 - y0)}")
    print(f"formula_delta_price {fmt(SHOCK / (ETA + NU))} formula_delta_output {fmt(SHOCK * NU / (ETA + NU))}")
    print(f"exact_match {p1 - p0 == SHOCK / (ETA + NU) and y1 - y0 == SHOCK * NU / (ETA + NU)}")
    print(f"output_share {fmt(NU / (ETA + NU))} price_share {fmt(1 / (ETA + NU))}")

    print("Part C: long-run equilibrium with expected price equal to the actual price")
    lr0 = long_run(A_BASE, ETA, YBAR)
    lr1 = long_run(A_BASE + SHOCK, ETA, YBAR)
    ly0 = A_BASE - ETA * lr0
    ly1 = A_BASE + SHOCK - ETA * lr1
    print(f"long_run_price_before {fmt(lr0)} long_run_price_after {fmt(lr1)}")
    print(f"long_run_price_change {fmt(lr1 - lr0)} long_run_output_before {fmt(ly0)} long_run_output_after {fmt(ly1)}")
    print(f"long_run_output_is_potential {ly0 == YBAR and ly1 == YBAR}")
    print(f"long_run_is_short_run_fixed_point {short_run(A_BASE + SHOCK, ETA, NU, YBAR, lr1)[0] == lr1}")

    print("Part D: output share and price change for five slopes of short-run AS")
    for slope in (Fraction(50), Fraction(100), Fraction(200), Fraction(400), Fraction(800)):
        share = slope / (ETA + slope)
        price_change = SHOCK / (ETA + slope)
        pa, ya = short_run(A_BASE, ETA, slope, YBAR, PE)
        pb, yb = short_run(A_BASE + SHOCK, ETA, slope, YBAR, PE)
        print(
            f"nu {slope} output_share {fmt(share)} price_change {fmt(pb - pa)} "
            f"output_change {fmt(yb - ya)} consistent {yb - ya == share * SHOCK and pb - pa == price_change}"
        )


main()
