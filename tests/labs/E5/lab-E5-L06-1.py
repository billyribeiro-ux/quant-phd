"""E5 L06 lab 1: the expectations-augmented Phillips curve, derived from the AS curve, on a seeded SIMULATED path.

SIMULATED: the unemployment path is generated from a seeded pseudo-random draw (random.Random(seed)). It is a
model path with no data behind it. The unemployment rate, inflation and the price level are model quantities.

Model (Lesson 6, Assumptions A1 to A3): short-run AS is Y = Ybar + nu (P - Pe) with nu = 200 (Lesson 5); the linear
output-unemployment relation Y - Ybar = -kappa (u - un) with kappa = 200 and natural rate un = 5 percent; expected
inflation is last period's inflation, pe_t = pi_(t-1) (adaptive expectations); inflation is the simple per-period rate
pi_t = (P_t - P_(t-1)) / P_(t-1). Unemployment rates are decimals, so 5 percent is 0.05.

Part A: one period. The price level and inflation from the AS and output-unemployment relations, against
the Phillips form pi_t = pe_t - beta_t (u_t - un) with beta_t = kappa / (nu P_(t-1)).
Part B: a seeded path of 12 periods. Each period checks the identity pi_t = pi_(t-1) - beta_t (u_t - un) exactly.
Part C: the one-period inflation change on a grid of unemployment rates at P_(t-1) = 6/5, where the change is
zero at the natural rate.

Every value is an exact fraction. A printed decimal is the exact fraction rounded half to even at six decimal
places.
"""

from __future__ import annotations

import random
from fractions import Fraction

YBAR = Fraction(1000)
NU = Fraction(200)
KAPPA = Fraction(200)
UN = Fraction(5, 100)
SEED = 20261028
PERIODS = 12
P_START = Fraction(6, 5)
PI_START = Fraction(3, 100)


def fmt(x: Fraction) -> str:
    """The exact value rounded half to even at six decimal places, with a minus sign where needed."""
    scaled = round(x * 10**6)
    sign = "-" if scaled < 0 else ""
    whole, frac = divmod(abs(scaled), 10**6)
    return f"{sign}{whole}.{frac:06d}"


def beta(price_prev: Fraction) -> Fraction:
    """The Phillips slope kappa / (nu P_(t-1)) for the previous price level, a positive number."""
    return KAPPA / (NU * price_prev)


def next_price(pe: Fraction, u: Fraction) -> Fraction:
    """The price level from AS and the output-unemployment relation.

    P = pe + (Y - Ybar) / nu, where Y - Ybar = -kappa (u - un).
    """
    return pe - KAPPA * (u - UN) / NU


def main() -> None:
    """Print Parts A, B and C. Every line is computed from the exact fractions and the seeded draws."""
    print("Part A: one period from the AS and output-unemployment relations, against the Phillips form")
    u_a = Fraction(6, 100)
    pe_a = P_START * (1 + PI_START)
    p_a = next_price(pe_a, u_a)
    pi_levels = (p_a - P_START) / P_START
    pi_form = PI_START - beta(P_START) * (u_a - UN)
    print(f"expected_price {fmt(pe_a)} price {fmt(p_a)}")
    print(f"inflation_from_levels {fmt(pi_levels)} inflation_from_phillips {fmt(pi_form)}")
    print(f"beta {fmt(beta(P_START))} identity_holds {pi_levels == pi_form}")

    print("Part B: seeded SIMULATED path of 12 periods, adaptive expectations")
    rng = random.Random(SEED)
    price, pi = P_START, PI_START
    zero_gap = 0
    no_change = 0
    all_hold = True
    no_change_only_at_zero_gap = True
    for t in range(1, PERIODS + 1):
        draw = rng.randint(-100, 100)
        gap = Fraction(draw, 10000)
        u = UN + gap
        pe = price * (1 + pi)
        new_price = next_price(pe, u)
        new_pi = (new_price - price) / price
        form = pi - beta(price) * (u - UN)
        hold = new_pi == form
        all_hold = all_hold and hold
        zero_gap += gap == 0
        no_change += new_pi == pi
        no_change_only_at_zero_gap = no_change_only_at_zero_gap and (new_pi != pi or gap == 0)
        print(
            f"t {t} unemployment_gap_bp {draw} unemployment {fmt(u * 100)} percent "
            f"inflation {fmt(new_pi)} change {fmt(new_pi - pi)} identity {hold}"
        )
        price, pi = new_price, new_pi
    print(f"identity_every_period {all_hold}")
    print(f"zero_gap_periods {zero_gap} no_change_periods {no_change}")
    print(f"no_change_only_at_natural_rate {no_change_only_at_zero_gap}")

    print("Part C: one-period inflation change at P(t-1) = 6/5, by unemployment rate")
    slope = beta(P_START)
    print(f"slope_at_price_6_5 {fmt(slope)}")
    signs_ok = True
    for step in range(-4, 5):
        u = UN + Fraction(step, 200)
        change = -slope * (u - UN)
        if step < 0:
            signs_ok = signs_ok and change > 0
        elif step > 0:
            signs_ok = signs_ok and change < 0
        else:
            signs_ok = signs_ok and change == 0
        print(f"unemployment {fmt(u * 100)} percent change {fmt(change)}")
    print(f"change_positive_below_un_zero_at_un_negative_above {signs_ok}")


main()
