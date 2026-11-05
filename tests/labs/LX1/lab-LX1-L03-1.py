"""LX1 L03 lab 1: a stylised two-economy model of parity, real debt, the external-finance premium and output depth.

SIMULATED. Every number comes from a deterministic model with the parameters printed in Part A. The model uses no data
and describes no historical economy. Economy X keeps its parity for the whole horizon. Economy Y leaves parity after a
stated number of periods. The printed depths are the model's own values, so they answer a question about the
assumptions and not about any country.

Units and conventions. The nominal debt D is fixed in integer cents. The price index P_t is dimensionless with P_0 = 1,
so the real value of the debt, V_t = D / P_t, is in cents. Leverage L_t = V_t / N_t is a dimensionless ratio. The
premium psi_t and the output fall f_t are dimensionless fractions; a percentage is a fraction times 100. Every quantity
is an exact Fraction. Each value is rounded once, half up, only when it is printed.

Model, for t = 0, 1, ..., H with H = 12 periods:
    P_t = (1 - delta) ** min(t, m)     the price index: it falls by the fraction delta in each period on parity,
                                       and is flat after the economy leaves parity; m is the number of periods on parity
    V_t = D / P_t                      the real value of the fixed nominal debt, in cents
    N_t = N_0 - (V_t - V_0)            borrower net worth, in cents: it falls one for one with the rise in V_t
    L_t = V_t / N_t                    leverage, a dimensionless ratio
    psi_t = phi * (L_t - L_0)          the external-finance premium above its baseline, a dimensionless fraction
    f_t = beta * psi_t                the fall in output, as a fraction of baseline output
    depth(m) = max over t of f_t       the output depth for a parity duration m

Part A prints the parameters and the two paths. Part B prints the depth of each economy, the period where it is first
reached, whether X is deeper than Y, and the difference of the two depths. Part C prints the depth for every parity
duration m from 0 to H, and checks that it never falls as m rises and that it rises at every step from m to m + 1.
Part D prints the ratio of the two depths for three values of the product beta * phi.
"""

from __future__ import annotations

import math
from fractions import Fraction

DEBT_CENTS = 1_000_000
NET_WORTH_CENTS = 4_000_000
DELTA = Fraction(1, 50)
HORIZON = 12
PARITY_X = 12
PARITY_Y = 4
PHI = Fraction(1)
BETA = Fraction(1)


def round_half_up(amount: Fraction) -> int:
    """Round a Fraction to a whole number, with a tie going toward plus infinity."""
    return math.floor(amount + Fraction(1, 2))


def fixed_decimal(amount: Fraction, places: int) -> str:
    """Show a non-negative Fraction with a fixed number of decimal places, rounded half up, for display only.

    Raises ValueError for a negative amount, because the display rule here is written for magnitudes only.
    """
    if amount < 0:
        raise ValueError("fixed_decimal shows non-negative amounts only")
    scaled = round_half_up(amount * 10**places)
    whole, frac = divmod(scaled, 10**places)
    return f"{whole}.{frac:0{places}d}"


def price_index(parity_periods: int, t: int) -> Fraction:
    """Price index P_t = (1 - delta) ** min(t, m), with P_0 = 1.

    Raises ValueError when t is negative or the parity duration m is outside 0 to HORIZON.
    """
    if t < 0:
        raise ValueError("the period t must be non-negative")
    if not 0 <= parity_periods <= HORIZON:
        raise ValueError("the parity duration must be between 0 and HORIZON periods")
    return (1 - DELTA) ** min(t, parity_periods)


def real_debt(parity_periods: int, t: int) -> Fraction:
    """Real value of the fixed nominal debt at period t, in cents: V_t = D / P_t."""
    return Fraction(DEBT_CENTS) / price_index(parity_periods, t)


def leverage(real: Fraction) -> Fraction:
    """Leverage L = V / N for a real debt V in cents, with N = N_0 - (V - V_0) the borrower's net worth in cents.

    Raises ValueError when the net worth is not positive, because the leverage ratio is then undefined.
    """
    net_worth = Fraction(NET_WORTH_CENTS) - (real - Fraction(DEBT_CENTS))
    if net_worth <= 0:
        raise ValueError("borrower net worth must stay positive")
    return real / net_worth


def baseline_leverage() -> Fraction:
    """Leverage at t = 0, where V_0 = D and N_0 is the baseline net worth."""
    return leverage(Fraction(DEBT_CENTS))


def premium(parity_periods: int, t: int, phi: Fraction) -> Fraction:
    """External-finance premium above its baseline: psi_t = phi * (L_t - L_0)."""
    return phi * (leverage(real_debt(parity_periods, t)) - baseline_leverage())


def output_fall(parity_periods: int, t: int, phi: Fraction, beta: Fraction) -> Fraction:
    """Fall in output as a fraction of baseline output: f_t = beta * psi_t."""
    return beta * premium(parity_periods, t, phi)


def depth_path(parity_periods: int, phi: Fraction, beta: Fraction) -> list[Fraction]:
    """The output fall f_0, ..., f_H for a parity duration m."""
    return [output_fall(parity_periods, t, phi, beta) for t in range(HORIZON + 1)]


def depth(parity_periods: int, phi: Fraction, beta: Fraction) -> Fraction:
    """Output depth: the largest output fall over the horizon, a fraction of baseline output."""
    return max(depth_path(parity_periods, phi, beta))


def first_period_at_depth(parity_periods: int, phi: Fraction, beta: Fraction) -> int:
    """The earliest period t at which the output fall reaches its depth."""
    path = depth_path(parity_periods, phi, beta)
    top = max(path)
    return next(t for t, value in enumerate(path) if value == top)


def print_economy(label: str, parity_periods: int) -> None:
    """Print the price index, real debt, leverage, premium and output fall for each period."""
    print(f"economy {label}, parity held for {parity_periods} of {HORIZON} periods:")
    for t in range(HORIZON + 1):
        price = price_index(parity_periods, t)
        real = real_debt(parity_periods, t)
        lev = leverage(real)
        psi = premium(parity_periods, t, PHI)
        fall = output_fall(parity_periods, t, PHI, BETA)
        print(
            f"  t = {t:2d}: index {fixed_decimal(price, 4)}; real debt {round_half_up(real)} cents; "
            f"leverage {fixed_decimal(lev, 4)}; premium {fixed_decimal(psi, 4)}; "
            f"output fall {fixed_decimal(100 * fall, 2)} percent"
        )


def main() -> None:
    """Print Parts A to D in a fixed order."""
    print("Part A: SIMULATED model, parameters and paths")
    print(
        f"D = {DEBT_CENTS} cents; N_0 = {NET_WORTH_CENTS} cents; deflation per period on parity = 1/50; "
        f"H = {HORIZON} periods; phi = {PHI}; beta = {BETA}"
    )
    print(f"baseline leverage L_0 = V_0 / N_0 = {fixed_decimal(baseline_leverage(), 4)}")
    print_economy("X", PARITY_X)
    print_economy("Y", PARITY_Y)

    depth_x = depth(PARITY_X, PHI, BETA)
    depth_y = depth(PARITY_Y, PHI, BETA)
    print("Part B: output depth of each economy")
    print(
        f"economy X depth {fixed_decimal(100 * depth_x, 2)} percent of baseline output, "
        f"first reached at t = {first_period_at_depth(PARITY_X, PHI, BETA)}"
    )
    print(
        f"economy Y depth {fixed_decimal(100 * depth_y, 2)} percent of baseline output, "
        f"first reached at t = {first_period_at_depth(PARITY_Y, PHI, BETA)}"
    )
    print(f"X is deeper than Y: {depth_x > depth_y}")
    print(f"difference X minus Y: {fixed_decimal(100 * (depth_x - depth_y), 2)} percentage points")

    depths = [depth(m, PHI, BETA) for m in range(HORIZON + 1)]
    print("Part C: depth by parity duration m, in percent of baseline output")
    for m, value in enumerate(depths):
        print(f"m = {m:2d}: depth {fixed_decimal(100 * value, 2)} percent")
    never_falls = all(depths[m] <= depths[m + 1] for m in range(HORIZON))
    strict_steps = all(depths[m] < depths[m + 1] for m in range(HORIZON))
    print(f"depth never falls as the parity duration rises: {never_falls}")
    print(f"depth rises at every step from m to m + 1 for m = 0 to {HORIZON - 1}: {strict_steps}")

    print("Part D: the ratio of the two depths for three values of the product beta * phi")
    for phi, beta in ((Fraction(1, 2), Fraction(1)), (Fraction(1), Fraction(1)), (Fraction(3), Fraction(1))):
        ratio = depth(PARITY_X, phi, beta) / depth(PARITY_Y, phi, beta)
        print(f"phi = {phi}, beta = {beta}, product {phi * beta}: ratio of depths X to Y {fixed_decimal(ratio, 4)}")


main()
